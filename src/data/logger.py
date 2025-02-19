import inspect
import logging
import os
from functools import wraps

from common import LOG_FILE


def grab_caller_name(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        caller_name = os.path.basename(inspect.stack()[1].filename)
        return func(self, caller_name, *args, **kwargs)
    return wrapper


class LoggerInitializer:
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s [%(process)d] [%(name)s] [%(levelname)s]: %(message)s',
            filename=LOG_FILE,
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')

    @grab_caller_name
    def create_logger(self, name):
        return logging.getLogger(name)


Logger = LoggerInitializer()
