import ast
import asyncio
import json
import os
import warnings
from time import sleep
from pprint import pformat
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from tabulate import tabulate

from paddlehelix import ApiException, Helixfold3Api, Helixfold3PriceQueryRequest, Helixfold3TaskBatchSubmitRequest, \
    TaskGetRequest, TaskCancelRequest
from paddlehelix.api.config import *
from paddlehelix.api.task import TaskUtil
from paddlehelix.cli.client import get_client
from paddlehelix.utils.file_util import download_file, parse_filename_from_url
from paddlehelix.utils.logger import create_logger
from paddlehelix.version.structures import list_type

warnings.filterwarnings("ignore")

def ask_yes_no(question, logger):
    """
    Asks the user to confirm an action.

    Args:
        question (str): The question to ask the user.
        logger: The logger instance.
    """
    while True:
        user_input = input(question + " (Y/N): ").strip().upper()
        if user_input in ['Y', 'N']:
            return user_input == 'Y'
        else:
            logger.warning("Invalid input, please input Y or N.")

def query_balance(client):
    """
    Query the current balance of the user.

    Args:
        client: The client instance. You can get it by calling `get_client()`.

    Returns:
        float: The current balance of the user.
    """
    balance_client_instance = client.balance_client_instance
    try:
        response = balance_client_instance.v1_finance_cash_balance_post(_request_timeout=DEFAULT_TIME_OUT)
    except ApiException as e:
        raise e
    balance = response['cashBalance']
    return balance

def query_price(client, output_dir):
    """
    Queries the price for unsubmitted tasks.

    Args:
        client: The client instance. You can get it by calling `get_client()`.
        output_dir (str): The directory to save the results.
    Returns:
        bool: `True` if the price query is successful, otherwise `False`.
    """
    logger = create_logger(output_dir, 'query_price.txt', name='query_price')
    table_path = os.path.join(output_dir, "table.csv")
    df = pd.read_csv(table_path)
    not_submitted_mask = (df['status'] == INITIALIZATION) | (df['status'] == NOT_STARTED)
    initial_mask = df['status'] == INITIALIZATION
    logger.info(f"Query price for unsubmitted tasks, total task number {not_submitted_mask.sum()} ...")

    # Query price, calculated by batch
    price_query_client_instance = client.helixfold3_client_instance
    for batch_start in range(0, len(df), QUERY_PRICE_BATCH_DATA_NUM):
        batch_indices = df.index[batch_start:batch_start + QUERY_PRICE_BATCH_DATA_NUM]
        batch_query_price_task_list = df.iloc[batch_indices]['data'].apply(ast.literal_eval).to_list()

        price_query_request = Helixfold3PriceQueryRequest(tasks=batch_query_price_task_list)
        try:
            response = price_query_client_instance.api_batch_submit_helixfold3_price_post(helixfold3_price_query_request=price_query_request, _request_timeout=DEFAULT_TIME_OUT)
        except ApiException as e:
            logger.error(f"ApiException when calling Helixfold3Api->batch_submit_helixfold3_price_post for the #{batch_indices[0]}-#{batch_indices[-1]} task!")
            logger.error(f"Please check your network connection and try submitting again under the same folder: {output_dir}")
            return False
        if response.code != 0:
            logger.error(f"\n{pformat(batch_query_price_task_list)}")
            logger.error(f"Failed to query price for the #{batch_indices[0]}-#{batch_indices[-1]} task! Message: {response.msg}")
            logger.error(f"If no problem found, please re-submit tasks from the same folder: {output_dir}")
            return False
        prices = [price.price for price in response.data.prices]
        sleep(MAX_CALLS_PER_PERIOD)
        for i, i_table in enumerate(batch_indices):
            if df.loc[i_table, 'status'] == INITIALIZATION:
                df.loc[i_table, 'status'] = NOT_STARTED
                df.loc[i_table, 'price'] = prices[i]

    total_prices = df[not_submitted_mask]['price'].sum()
    df.to_csv(table_path, index=False)
    logger.info(f"Total price for unsubmitted tasks: {total_prices:.2f}")
    return total_prices


def submit_task(client, output_dir):
    """
    Submits tasks in batches.

    Args:
        client: The client instance. You can get it by calling `get_client()`.
        output_dir (str): The directory to save the results.
    Returns:
        bool: `True` if the task submission is successful, otherwise `False`.
    """
    logger = create_logger(output_dir, 'submit_task.txt', name='submit_task')
    table_path = os.path.join(output_dir, "table.csv")
    df = pd.read_csv(table_path)

    ready_submit_mask = df['status'] == NOT_STARTED
    logger.info(f"Ready to submit {len(df[ready_submit_mask])} tasks!")

    # Process in batches
    batch_submit_instance = client.helixfold3_client_instance
    for batch_start in range(0, len(df[ready_submit_mask]), DEFAULT_TASK_COUNT_ONE_BATCH):
        batch_indices = df[ready_submit_mask].index[batch_start:batch_start + DEFAULT_TASK_COUNT_ONE_BATCH]
        ready_submit_task_list = df.iloc[batch_indices]['data'].apply(ast.literal_eval).to_list()

        batch_submit_request = Helixfold3TaskBatchSubmitRequest(tasks=ready_submit_task_list)
        try:
            response = batch_submit_instance.api_batch_submit_helixfold3_post(helixfold3_task_batch_submit_request=batch_submit_request, _request_timeout=DEFAULT_TIME_OUT)
        except ApiException as e:
            logger.error(f"ApiException when calling Helixfold3Api->batch_submit_helixfold3_post for the #{batch_indices[0]}-#{batch_indices[-1]} task!")
            logger.error(f"Please check your network connection and try submitting again under the same folder: {output_dir}")
            return False
        if response.code != 0:
            logger.error(f"\n{pformat(ready_submit_task_list)}")
            logger.error(f"Failed to submit task from #{batch_indices[0]} to #{batch_indices[-1]}!  Message: {response.msg}")
            logger.error(f"If no problem found, please re-submit tasks from the same folder: {output_dir}")
            return False
        task_ids = response.data.task_ids
        logger.info(f"Batch submit task: {task_ids}")
        # Update task_list and dataframe
        df.loc[batch_indices, 'task_id'] = task_ids
        df.loc[batch_indices, 'status'] = SUBMITTED

        sleep(MAX_CALLS_PER_PERIOD)

        # Save updated dataframe
        df.to_csv(table_path, index=False)
    return True


def polling_task_status(client, output_dir):
    """
    Polls the status of tasks and downloads the results.

    Args:
        client: The client instance. You can get it by calling `get_client()`.
        output_dir (str): The directory to save the results.

    Returns:
        bool: `True` if the task submission is successful, otherwise `False`.
    """

    logger = create_logger(output_dir, 'polling task.txt', name='polling_task')
    logger.info("Starting task status polling!")
    table_path = os.path.join(output_dir, "table.csv")
    save_dir = os.path.join(os.path.dirname(table_path), "result")
    df = pd.read_csv(table_path, dtype={'download_url': str})

    download_futures = []
    exe = ThreadPoolExecutor(max_workers=4)

    def _check_download_futures():
        for fut in download_futures:
            if fut.done():
                download_futures.remove(fut)
                idx = fut.result()
                df.loc[idx, 'status'] = DOWNLOADED
                df.loc[idx, 'storage_path'] = os.path.join(save_dir, parse_filename_from_url(df.loc[idx, 'download_url']))
                logger.info(f"Task #{idx} downloaded.")
                if fut.exception() is not None:
                    logger.error(f"Task #{idx} download failed! Please restart the submission to retry!")
                    raise fut.exception()

    # 如果表中有未下载的任务，优先启动他们的下载
    to_down = df['status'] == QUERIED
    for idx, row in df[to_down].iterrows():
        download_futures.append(exe.submit(download_file, idx, df.loc[idx, 'download_url'], save_dir))

    # 开始轮询，发现已完成的任务则启动下载
    while True:
        # Get tasks that need to query status
        query_mask = df['status'] == SUBMITTED
        tasks_to_query = df[query_mask]

        get_task_info_instance = client.task_client_instance
        for idx, row in tasks_to_query.iterrows():
            task_id = int(row['task_id'])
            get_task_info_request = TaskGetRequest(task_id=task_id)
            try:
                response = get_task_info_instance.api_task_info_post(task_get_request=get_task_info_request, _request_timeout=DEFAULT_TIME_OUT)
            except ApiException as e:
                logger.error(f"ApiException when calling TaskApi->get_task_info for the task with id {task_id}!")
                logger.error(f"Please check your network connection and try submitting again under the same folder: {output_dir}")
                return False
            if response.code != 0:
                logger.error(f"Failed to get task info for the task with id {task_id}! Message: {response.msg}")
                logger.error(f"If no problem found, please re-submit tasks from the same folder: {output_dir}")
                return False
            status = response.data.status

            if status == ApiTaskStatusSucc:
                df.loc[idx, 'status'] = QUERIED
                df.loc[idx, 'download_url'] = json.loads(response.data.result)['download_url']
                download_futures.append(exe.submit(download_file, idx, df.loc[idx, 'download_url'], save_dir))
            elif status == ApiTaskStatusFailed:
                df.loc[idx, 'status'] = FAILED
            elif status == ApiTaskStatusCancel:
                df.loc[idx, 'status'] = CANCELLED
            logger.info(f"Task #{idx}, Task_id: {task_id}, Status: {STATUS_TO_STR[status]}")
            sleep(MAX_CALLS_PER_PERIOD)

            while len(download_futures) >= 10:
                try:
                    _check_download_futures()
                except Exception as e:
                    return False
                sleep(MAX_CALLS_PER_PERIOD)
                # update
                df.to_csv(table_path, index=False)

        while download_futures:
            try:
                _check_download_futures()
            except Exception as e:
                return False
            sleep(MAX_CALLS_PER_PERIOD)
        df.to_csv(table_path, index=False)
        if not (df['status'] == SUBMITTED).any():
            return True


def execute(output_dir,
            quiet=False,
            ignore_balance=False,
            **kwargs):
    """
    Executes the task submission process.

    Args:
        output_dir (str): Specifies the directory for storing logs and results.
            - If this path was previously used for a submitted task, the system will automatically read the status files from the directory and resume execution from where the last task left off.
            - If you want to start a new task from scratch, provide a new, unused directory.

        quiet (bool): Determines whether to skip the confirmation prompt before submitting the task.
            - If set to `True`, the system will automatically submit the task without asking for confirmation.
            - If set to `False`, the system will prompt the user for confirmation before submission.

        ignore_balance (bool): **(Internal use only)** A developer-only flag. Do not use this parameter.

        input_data (str): Specifies the input data path for the task.
            - The input data can be:
                - A JSON file
                - A folder containing multiple JSON files
                - A JSON object
                - A list of JSON objects

        data (dict, optional): A JSON object for input data.
            - **Deprecated:** It is recommended to use `input_data` instead, as this parameter may be removed in future versions.

        data_list (list, optional): A list of JSON objects.
            - **Deprecated:** It is recommended to use `input_data` instead, as this parameter may be removed in future versions.

        file_path (str, optional): Specifies the path to a JSON file containing task data.
            - **Deprecated:** It is recommended to use `input_data` instead, as this parameter may be removed in future versions.

        file_dir (str, optional): Specifies the path to a directory containing multiple JSON files as task data.
            - **Deprecated:** It is recommended to use `input_data` instead, as this parameter may be removed in future versions.

    Returns:
        bool: `True` if the task submission is successful, otherwise `False`.
    """
    client = get_client()

    # 1. 结果路径初始化，读取或初始化任务表格
    table_path = os.path.join(output_dir, "table.csv")
    if not os.path.isdir(output_dir) or not os.path.exists(table_path):
        os.makedirs(output_dir, exist_ok=True)
        logger = create_logger(output_dir, 'main.txt', name='main')
        logger.info("Creating a new folder {} to store task data and results.".format(output_dir))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            warnings.simplefilter("default", category=DeprecationWarning)
            try:
                task_list = TaskUtil.parse_task_data_list_from_all_kinds_input(**kwargs)
            except ValueError as e:
                logger.error(f"Input Error!")
                logger.error(f"{e}")
                return False
        df = pd.DataFrame()
        df['data'] = task_list
        df['task_id'] = -1
        df['download_url'] = ""
        df['status'] = INITIALIZATION
        df['price'] = np.nan
        df.to_csv(table_path, index=False)
    else:
        logger = create_logger(output_dir, 'main.txt', name='main')
        logger.info(f"There is an old submission under folder: {output_dir}, checking status ...")
        df = pd.read_csv(table_path)

        if len(df['data']) > 0:
            logger.info(f"Found tasks:")
            for index, row in df.iterrows():
                logger.info(f"{row['data']}")
            logger.info(f"Old submission under folder: {output_dir} ...")
            if not quiet and not ask_yes_no(f"Do you want to restart the submission under folder: {output_dir} ?", logger):
                logger.info(f"Exit.")
                return False
        else:
            logger.error(f"Task records are invalid under folder: {output_dir}")
            logger.error(f"Exit! Please check the folder or start a new submission!")
            return False

    # 2. 询价
    if ((df['status'] == INITIALIZATION) | (df['status'] == NOT_STARTED)).any():
        total_prices = query_price(client, output_dir)
        if not total_prices:
            return False

    # 3 提交任务
    df = pd.read_csv(table_path)
    if (df['status'] == NOT_STARTED).any():
        # 3.1 询问余额，与待提交任务的价格比较
        if not ignore_balance:
            try:
                balance = query_balance(client)
            except Exception as e:
                logger.error("ApiException when calling BceApi->v1_finance_cash_balance: %s\n" % e)
                return False
            logger.info(f"Current balance: {balance}")
            total_prices = df[df['status'] == NOT_STARTED]['price'].sum()
            if total_prices > balance:
                logger.info("Insufficient balance! Exit!")
                return False
            else:
                if not quiet and not ask_yes_no(f"Sufficient balance! Please confirm to start the submission:", logger):
                    logger.info(f"Exit.")
                    return False
        else:
            logger.warning("Debug mode! Skip balance checking. Contunue ...")

        # 3.2
        if not submit_task(client, output_dir):
            return False

    # 4. 轮询任务运行状态
    df = pd.read_csv(table_path)
    if (df['status'] == SUBMITTED).any():
        if not polling_task_status(client, output_dir):
            return False

    logger.info("Finished!")

    df = pd.read_csv(table_path)
    success_count = len(df[df['status'] == DOWNLOADED])
    failed_count = len(df[df['status'] == FAILED])
    cancelled_count = len(df[df['status'] == CANCELLED])
    logger.info(
        f"Task completed! Successful tasks: {success_count}, Failed tasks: {failed_count}, Cancelled tasks: {cancelled_count}")

    if failed_count > 0:
        failed_tasks = df[df['status'] == FAILED][['task_id']]
        failed_tasks['index'] = failed_tasks.index
        logger.info("### Failed Tasks\n" + tabulate(failed_tasks, headers=['Index', 'Task ID'], tablefmt='grid'))

    if cancelled_count > 0:
        cancelled_tasks = df[df['status'] == CANCELLED][['task_id']]
        cancelled_tasks['index'] = cancelled_tasks.index
        logger.info(
            "### Cancelled Tasks\n" + tabulate(cancelled_tasks, headers=['Index', 'Task ID'], tablefmt='grid'))

    df['status'] = df['status'].apply(lambda x: TASK_STATUS_TO_STR[x])
    logger.info('\n'+ df[['task_id', 'status', 'price', 'storage_path']].to_markdown(index=False, tablefmt='grid'))
    logger.info("The submission summary printed above are stored in: {}".format(table_path))
    return True
