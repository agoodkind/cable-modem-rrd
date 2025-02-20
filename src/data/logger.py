import inspect
import logging
import os
import sys
from functools import wraps
from typing import Callable

from annotated_types import T
from constants import LOG_FILE
from utils import grab_caller_name


class LoggerInitializer:
    def __init__(self):
        logging.basicConfig(
            format="%(asctime)s [%(process)d] [%(name)s] [%(levelname)s]: %(message)s",
            handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
            level=logging.DEBUG,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    @grab_caller_name
    def create_logger(self, name) -> logging.Logger:
        return logging.getLogger(name)


Logger = LoggerInitializer()
