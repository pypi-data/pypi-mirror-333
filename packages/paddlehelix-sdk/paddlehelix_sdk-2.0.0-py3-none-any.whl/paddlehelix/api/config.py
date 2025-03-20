"""
Common request variables.
"""

# 请求变量
SCHEME = "http://"
HOST = "chpc.bj.baidubce.com"
BALANCE_HOST = 'billing.baidubce.com'


# API 返回状态
ApiTaskStatusDoing = 2  # 运行中
ApiTaskStatusCancel = 3  # 取消
ApiTaskStatusSucc = 1  # 成功
ApiTaskStatusFailed = -1  # 执行失败
ApiTaskStatusSubmitFailed = -2  # 提交失败
ApiTaskStatusUnknown = 0  # 未知状态

# 单个任务在 SDK 流程中的状态
INITIALIZATION = -3
NOT_STARTED = 0
SUBMITTED = 1
QUERIED = 2
DOWNLOADED = 3
FAILED = -1
CANCELLED = -2

STATUS_TO_STR = {
    ApiTaskStatusSubmitFailed: "Submission Failed",
    ApiTaskStatusFailed: "Execution Failed",
    ApiTaskStatusSucc: "Success",
    ApiTaskStatusDoing: "Running",
    ApiTaskStatusCancel: "Cancelled",
    ApiTaskStatusUnknown: "Unknown Status"
}

TASK_STATUS_TO_STR = {
    INITIALIZATION: "INITIALIZATION",
    NOT_STARTED: "NOT_STARTED",
    SUBMITTED: "SUBMITTED",
    QUERIED: "DONE",
    DOWNLOADED: "DONE and DOWNLOADED",
    FAILED: "FAILED",
    CANCELLED: "CANCELLED"
}

# 超时重试参数
DEFAULT_RETRY_COUNT = 3
DEFAULT_TIME_OUT = 10

# CPS限流参数
MAX_CALLS_PER_PERIOD = 1
PERIOD = 1

# 提交任务参数
DEFAULT_TASK_COUNT_ONE_BATCH = 20
MAX_TASK_COUNT_ONE_BATCH = 2
DEFAULT_SUBMIT_INTERVAL = 1


# 轮询任务参数
DEFAULT_POLLING_INTERVAL_SECONDS = 30
MIN_POLLING_INTERVAL_SECONDS = 2

# query params
QUERY_BATCH_NUM = 50
QUERY_BATCH_INTERVAL = 15

# 询价单批次数量
QUERY_PRICE_BATCH_DATA_NUM = 100


DOWNLOAD_NUM = 10