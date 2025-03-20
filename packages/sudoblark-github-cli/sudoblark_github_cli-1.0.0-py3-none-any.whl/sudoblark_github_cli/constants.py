import logging
from enum import Enum

DEFAULT_LOG_FORMAT: str = "%(asctime)s - %(module)s - %(levelname)s - %(message)s"


class LogLevel(str, Enum):
    NOTSET = logging.getLevelName(logging.NOTSET)
    DEBUG = logging.getLevelName(logging.DEBUG)
    INFO = logging.getLevelName(logging.INFO)
    WARNING = logging.getLevelName(logging.WARNING)
    ERROR = logging.getLevelName(logging.ERROR)
    CRITICAL = logging.getLevelName(logging.CRITICAL)
