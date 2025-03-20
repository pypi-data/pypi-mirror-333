import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LogColors:
    DEBUG = "\033[96m"
    INFO = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    CRITICAL = "\033[41m\033[97m"
    RESET = "\033[0m"


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        level_color = {
            logging.DEBUG: LogColors.DEBUG,
            logging.INFO: LogColors.INFO,
            logging.WARNING: LogColors.WARNING,
            logging.ERROR: LogColors.ERROR,
            logging.CRITICAL: LogColors.CRITICAL,
        }.get(record.levelno, LogColors.RESET)

        message = super().format(record)
        return f"{level_color}{message}{LogColors.RESET}"


formatter = ColoredFormatter(
    "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d:%(funcName)s | %(message)s"
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d:%(funcName)s | %(message)s"
)
maxBytes = 30 * 1024 * 1024  # 30MB
file_handler = RotatingFileHandler(__name__ + ".log", maxBytes=maxBytes, backupCount=3)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
