import os
import pickle
import uuid
from datetime import date, datetime
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

import pandas as pd
import pyarrow.fs as pfs
from typing_extensions import ParamSpec

from ..constants import _TECTON_CHECKPOINT_ATTR
from ..utils.hashing import to_uuid

from ._tecton_utils import get_cache_base_path

T = TypeVar("T")
P = ParamSpec("P")


def make_deterministic(obj: Any, key_obj: Any) -> Any:
    """Make an object deterministic by adding a checkpoint attribute to it.
    It's a no-op for primitive types and datetimes.

    Args:

        obj: The object to make idempotent
        key_obj: The key object to generate the determinitic key for the object

    Returns:

        The object with the checkpoint
    """
    if obj is None:
        return obj
    if isinstance(obj, (int, float, bool, str, date, datetime)):
        return obj
    if isinstance(obj, pd.DataFrame):
        setattr(obj, _TECTON_CHECKPOINT_ATTR, to_uuid(key_obj))
        return obj
    raise NotImplementedError(f"Type {type(obj)} is not supported")


def checkpoint(
    func: Callable[..., T],
    *args: Any,
    idempotency_key: Any = None,
    **kwargs: Any,
) -> T:
    """Checkpoint a function call. If the function has already been
    called with the same arguments, it will return the result from the cache.

    Args:

        func: The function to checkpoint
        args: The arguments to the function
        kwargs: The keyword arguments to the function
        idempotency_key: The extra key to change the function's idempotency, defaults to None

    Returns:

        The result of the function
    """
    uid = _func_to_uuid(func, *args, idempotency_key=idempotency_key, **kwargs)
    fs, base_path = get_cache_base_path()
    file_folder = os.path.join(base_path, uid + ".parquet")
    selector = pfs.FileSelector(
        file_folder,
        recursive=True,
        allow_not_found=True,
    )
    result = None
    for task in fs.get_file_info(selector):
        if task.path.endswith("/SUCCESS"):
            with fs.open_input_file(task.path) as f:
                data_type = pickle.load(f)
            file_path = os.path.join(
                task.path.rsplit("/", 1)[0],
                "data",
            )
            if issubclass(data_type, pd.DataFrame):
                result = pd.read_parquet(file_path, engine="pyarrow", filesystem=fs)
            else:
                with fs.open_input_file(file_path) as f:
                    result = pickle.load(f)
            break
    if result is None:
        task_folder = os.path.join(file_folder, "task_" + str(uuid.uuid4()))
        file_path = os.path.join(task_folder, "data")
        success_path = os.path.join(task_folder, "SUCCESS")
        result = func(*args, **kwargs)
        fs.create_dir(task_folder, recursive=True)
        if isinstance(result, pd.DataFrame):
            result.to_parquet(file_path, engine="pyarrow", filesystem=fs)
        else:
            with fs.open_output_stream(file_path) as f:
                pickle.dump(result, f)
        with fs.open_output_stream(success_path) as f:
            pickle.dump(type(result), f)
    return make_deterministic(result, uid)


def with_checkpoint(
    func: Optional[Callable[P, T]] = None,
    idempotency_key: Any = None,
) -> Callable[P, T]:
    """Decorator to checkpoint a function call. If the function has already been
    called with the same arguments, it will return the result from the cache.

    Args:

        func: The function to checkpoint
        idempotency_key: The extra key to change the function's idempotency, defaults to None

    Example:

        ```python
        @with_checkpoint
        def func1(a: int, b: str) -> pd.DataFrame:
            return random.random()

        @with_checkpoint(idempotency_key=2)
        def func2(df: pd.DataFrame) -> int:
            return 1
        ```
    """

    def _wrap(_func: Callable[P, T]) -> Callable[P, T]:
        @wraps(_func)
        def run(*args: P.args, **kwargs: P.kwargs) -> T:
            return checkpoint(
                _func,
                *args,
                idempotency_key=idempotency_key,
                **kwargs,
            )

        return run

    if func is not None:
        return _wrap(func)
    return _wrap


def _func_to_uuid(
    func: Callable[P, T],
    *args: Any,
    idempotency_key: Any = None,
    **kwargs: Any,
) -> str:
    return to_uuid(
        (
            func.__module__,
            func.__qualname__,
            args,
            kwargs,
            idempotency_key,
        )
    )
