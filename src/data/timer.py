import time
from contextlib import contextmanager

from logger import Logger

logger = Logger.create_logger()

@contextmanager
def timer():
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(f"Elapsed time: {elapsed_time:.4f} seconds")