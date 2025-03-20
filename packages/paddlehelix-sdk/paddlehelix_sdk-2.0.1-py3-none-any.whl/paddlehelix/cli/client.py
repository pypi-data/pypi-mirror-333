"""
API Client
"""
import argparse
import json
import os
import platform

from paddlehelix import Configuration, ApiClient
from paddlehelix.api.config import SCHEME, HOST, BALANCE_HOST
from paddlehelix.api.helixfold3_api import Helixfold3Api
from paddlehelix.api.task_api import TaskApi
from paddlehelix.api.bce_api import BceApi
from paddlehelix.utils.logger import create_logger


def get_config_file_path():
    """Returns the path to the configuration file."""
    system_name = platform.system()

    if system_name == "Windows":
        # Windows: 使用 AppData 目录
        config_dir = os.path.join(os.getenv('APPDATA'), "PaddleHelix")
    else:
        # Linux / macOS: 使用用户主目录下的 .config 目录
        config_dir = os.path.join(os.path.expanduser("~"), ".config", "PaddleHelix")

    os.makedirs(config_dir, exist_ok=True)

    config_file = os.path.join(config_dir, "config.json")
    return config_file

def load_config(config_file):
    """Loads AK and SK from the configuration file."""

    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            config = json.load(file)
        return config.get("PADDLEHELIX_API_AK"), config.get("PADDLEHELIX_API_SK")
    return None, None

def save_config(ak, sk, config_file):
    """Saves AK and SK to the configuration file."""
    config = {
        "PADDLEHELIX_API_AK": ak,
        "PADDLEHELIX_API_SK": sk
    }

    with open(config_file, "w") as file:
        json.dump(config, file, indent=4)


def get_ak_sk_from_envs():
    """Gets AK and SK from environment variables."""
    return os.getenv("PADDLEHELIX_API_AK"), os.getenv("PADDLEHELIX_API_SK")

def get_client(ak=None, sk=None):
    """Gets the API client.

    Attempts to obtain Access Key (AK) and Secret Key (SK) in the following order:
    1. If AK and SK are provided as arguments, saves them to config file and env vars
    2. If AK and SK args not provided, checks env vars
    3. If not found in env vars, tries loading from config file
    4. If not found in config file, prompts user for manual input

    Args:
        ak (str, optional): Access Key. Defaults to None.
        sk (str, optional): Secret Key. Defaults to None.

    Returns:
        object: API client instance.
    """

    logger = create_logger(name='client')
    if ak and sk:    # 如果 ak 和 sk 都被提供
        logger.info("PaddleHelix API Access Key and Secret Key have been provided as arguments.")
        save_config(ak, sk, get_config_file_path())
        # 设置环境变量
        os.environ["PADDLEHELIX_API_AK"] = ak
        os.environ["PADDLEHELIX_API_SK"] = sk
        _ak, _sk = ak, sk
    else:
        _ak, _sk = get_ak_sk_from_envs()
        config_file_path = get_config_file_path()

        if not _ak or not _sk:     # 如果环境变量中没有 ak 或 sk
            logger.info(
                "PaddleHelix API Access Key or Secret Key not found in environment variables. Attempting to load from configuration file.")
            _ak, _sk = load_config(config_file_path)

            if _ak is None or _sk is None:     # 如果配置文件中没有 ak 或 sk
                logger.info(
                    "PaddleHelix API Access Key or Secret Key not found in the configuration file. Please enter them manually.")
                _ak = input("Please enter your PaddleHelix API Access Key: ")
                _sk = input("Please enter your PaddleHelix API Secret Key: ")
                save_config(_ak, _sk, config_file_path)
                logger.info(
                    f"The PaddleHelix API Access Key and Secret Key have been saved to the configuration file at {config_file_path}, and will be automatically loaded on the next use.")
            else:
                logger.info("PaddleHelix API Access Key and Secret Key successfully loaded from the configuration file.")

        else:
            logger.info("PaddleHelix API Access Key and Secret Key have been successfully loaded from the environment variables.")
            if os.path.exists(config_file_path):
                logger.info('Updating the configuration file.')
            else:
                logger.info(
                    f"The PaddleHelix API Access Key and Secret Key have been saved to the configuration file at {config_file_path}, and will be automatically loaded on the next use.")
            save_config(_ak, _sk, config_file_path)


    paddlehelix_configuration = Configuration(
        host="".join([SCHEME, HOST]),
        api_key={
            'access key': _ak,
            'secret key': _sk
        }
    )

    balance_configuration = Configuration(
        host="".join([SCHEME, BALANCE_HOST]),
        api_key={
            'access key': _ak,
            'secret key': _sk
        }
    )
    helixfold3_client = ApiClient(paddlehelix_configuration)
    task_client = ApiClient(paddlehelix_configuration)
    balance_client = ApiClient(balance_configuration)

    class APIClient:
        balance_client_instance = BceApi(balance_client)
        helixfold3_client_instance = Helixfold3Api(helixfold3_client)
        task_client_instance = TaskApi(task_client)

    return APIClient

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PaddleHelix API 客户端')
    parser.add_argument('--ak', type=str, help='PaddleHelix API Access Key')
    parser.add_argument('--sk', type=str, help='PaddleHelix API Secret Key')
    args = parser.parse_args()

    client = get_client(args.ak, args.sk)