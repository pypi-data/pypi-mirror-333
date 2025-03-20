# This file contains lru_cached functions that are used to cache the results of function calls.
# They should be replaced when the resource implementation is fixed.

import inspect
from functools import lru_cache
from typing import Callable


@lru_cache
def code_to_func(code: str) -> Callable:
    exec(code.strip())
    for v in locals().values():
        if inspect.isfunction(v):
            return v
    raise ValueError("No function found")
