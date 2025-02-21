
import logging
import sys

from utils.constants import LOG_FILE
from utils.decorators import grab_caller_name


class LoggerInitializer:
    def __init__(self) -> None:
        logging.basicConfig(
            format="%(asctime)s [%(process)d] [%(name)s] [%(levelname)s]: %(message)s",
            handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
            level=logging.DEBUG,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    @grab_caller_name
    def create_logger(self, name: str) -> logging.Logger:
        return logging.getLogger(name)


Logger = LoggerInitializer()
