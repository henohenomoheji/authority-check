import json
import logging
from uuid import uuid4


LOGGER_NAME = "image_interpretation"


def get_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def new_request_id() -> str:
    return str(uuid4())


def log_event(**payload: object) -> None:
    get_logger().info(json.dumps(payload, ensure_ascii=False))
