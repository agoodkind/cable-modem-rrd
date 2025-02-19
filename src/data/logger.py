import inspect
import logging
import os
import sys
from functools import wraps

from common import LOG_FILE


def grab_caller_name(func) -> logging.Logger:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> logging.Logger:
        caller_name = os.path.basename(inspect.stack()[1].filename)
        return func(self, caller_name, *args, **kwargs)
    return wrapper


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
