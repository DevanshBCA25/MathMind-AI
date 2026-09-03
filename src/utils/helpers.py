from datetime import datetime

from src.utils.logger import logger
from src.utils.history import save_history


def log_info(message):
    logger.info(message)


def log_warning(message):
    logger.warning(message)


def log_error(message):
    logger.error(message)


def save_operation(module, operation, input_data, result):

    record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "module": module,
        "operation": operation,
        "input": input_data,
        "result": str(result),
    }

    save_history(record)

    logger.info(
        f"{module} | {operation} | {input_data} | {result}"
    )