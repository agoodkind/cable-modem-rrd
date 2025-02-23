import inspect
from functools import wraps
import os
from typing import Callable

from annotated_types import T


def grab_caller_name(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> T:
        caller_name = os.path.basename(inspect.stack()[1].filename)
        return func(self, caller_name, *args, **kwargs)

    return wrapper
