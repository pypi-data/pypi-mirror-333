import asyncio
import base64
import os
import tempfile
import threading
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import pyarrow as pa
from pyarrow.fs import FileSystem
from tecton import Attribute, BatchSource, Entity, RequestSource, pandas_batch_config
from tecton.types import Field
from tecton_core import conf as tecton_conf

from .convert import to_tecton_type

_CACHE_PREFIX = "_tecton_cache"


def make_entity(description: Optional[str] = None, **fields) -> Entity:
    """
    Make a Tecton entity

    Args:

        description: The description of the entity, defaults to None
        **fields: The fields, where the key is the field name and the value is the
            field type in type annotation format. For example, ``name=str``

    Returns:

        Entity: The entity

    Examples:

        ```python
        from ..tecton_utils import make_entity

        user = make_entity(user_id=int, description="User entity")
        ```
    """
    _fields = [Field(k, to_tecton_type(v)) for k, v in fields.items()]
    name = _fields[0].name
    return Entity(name=name, description=description, join_keys=_fields)


def make_request_source(**fields) -> RequestSource:
    """
    Make a Tecton request source

    Args:

        **fields: The fields, where the key is the field name and the value is the
            field type in type annotation format. For example, ``name=str``

    Returns:

        RequestSource: The request source

    Examples:

        ```python
        from ..tecton_utils import make_request_source

        params = make_request_source(name=str, field1=int, field2=float, field3=bool)
        ```
    """
    return RequestSource(
        schema=[Field(k, to_tecton_type(v)) for k, v in fields.items()]
    )


def get_df_schema(df: pd.DataFrame, as_attributes: bool = False) -> List[Any]:
    """
    Get the Tecton schema of the DataFrame

    Args:

        df: The DataFrame
        as_attributes: Whether to return the schema as attributes, defaults to False

    Returns:

        List[Any]: The schema of the DataFrame
    """
    res: List[Any] = []
    for field in pa.Schema.from_pandas(df):
        res.append((field.name, to_tecton_type(field.type)))
    if not as_attributes:
        return [Field(name, type) for name, type in res]
    return [Attribute(name, type) for name, type in res]


def set_secrets_env(secrets_dict: Dict[str, Any]) -> None:
    """
    Set the secrets in the environment variables

    Args:

        secrets_dict: A dictionary of secrets

    Examples:

        ```python
        from tecton import Secret

        secrets = set_secrets_env({"env_var_name": Secret(scope="", key="")})

        @batch_feature_view(
            sources=[your_source, secrets],
            ...
        )
        def your_feature_view(your_source, secrets):
            # no need to do anything with secrets, they are already set in the environment
            ...
        ```
    """

    @pandas_batch_config(
        secrets=secrets_dict,
    )
    def api_secrets(secrets):
        import os

        import pandas as pd

        for k, v in secrets.items():
            os.environ[k] = v

        return pd.DataFrame([[0]], columns=["dummy"])

    return BatchSource(name="secrets", batch_config=api_secrets)


def get_cache_base_path() -> Tuple[FileSystem, str]:
    """
    Get the base path for the cache

    Returns:

        Tuple[FileSystem, str]: The filesystem and the path
    """
    if "MATERIALIZATION_TASK_PARAMS" in os.environ:
        try:
            from tecton_proto.materialization.params_pb2 import (
                MaterializationTaskParams,
            )
        except ImportError:
            from tecton_proto.materialization.params__client_pb2 import (
                MaterializationTaskParams,
            )

        params = MaterializationTaskParams()
        params.ParseFromString(
            base64.standard_b64decode(os.environ["MATERIALIZATION_TASK_PARAMS"])
        )
        store_path = params.offline_store_path.rstrip("/")
        if not store_path.endswith("data"):
            raise ValueError(f"Invalid offline store path: {store_path}")
        path = store_path.rsplit("/", 2)[0]
    elif "TECTON_CACHE_PATH" in os.environ:
        path = os.environ["TECTON_CACHE_PATH"]
    else:
        path = tempfile.gettempdir()

    fs, p = FileSystem.from_uri(os.path.join(path, _CACHE_PREFIX))
    fs.create_dir(p, recursive=True)
    return fs, p


def run_async(coro: Any) -> Any:
    """
    Run the coroutine asynchronously in both Tecton and Jupyter notebooks

    Args:

        coro: The coroutine to run

    Returns:

        Any: The result of the coroutine
    """

    res = [None]
    exc = [None]

    def _run():
        loop = asyncio.new_event_loop()
        try:
            res[0] = loop.run_until_complete(coro)
        except Exception as e:
            exc[0] = e
        finally:
            loop.close()

    _thread = threading.Thread(target=_run)
    _thread.start()
    _thread.join()

    if exc[0] is None:
        return res[0]
    raise exc[0]


def run_async_jobs(jobs: List[Any], concurrency: int) -> List[Any]:
    """
    Run the list of coroutines asynchronously in both Tecton and Jupyter notebooks

    Args:

        jobs: The list of coroutines to run
        concurrency: The number of concurrent jobs to run

    Returns:

        List[Any]: The results of the coroutines
    """

    async def _run(job, sem):
        async with sem:
            return await job

    async def _gather():
        sem = asyncio.Semaphore(concurrency)
        _jobs = [_run(job, sem) for job in jobs]
        return await asyncio.gather(*_jobs)

    return run_async(_gather())


def featurize_async(
    df: pd.DataFrame,
    input_column: str,
    output_column: str,
    featurizer: Any,
    concurrency: int,
    dedup=True,
    mini_batch_size=0,
):
    """
    Featurize a DataFrame using asynchronous featurizer

    Args:

        df: The DataFrame to featurize
        input_column: The input column
        output_column: The output column
        featurizer: The async featurizer function
        concurrency: The number of concurrent jobs to run
        dedup: Whether to deduplicate the results, defaults to True
        mini_batch_size: The mini batch size, defaults to 0

    Returns:

        pd.DataFrame: The DataFrame with the output column

    Note:

        If the featurizer transforms single items, mini_batch_size must be 0,
        else you must specify the mini_batch_size to be a positive number
    """

    def _extract(values: List[Any]) -> List[Any]:
        if len(values) == 0:
            return []

        if dedup:
            keys = list(set(values))
            features = _extract(keys)
            _dict = dict(zip(keys, features))
            return [_dict[x] for x in values]

        if mini_batch_size == 0:
            return run_async_jobs(
                [featurizer(value) for value in values],
                concurrency=concurrency,
            )
        else:
            jobs = []
            for i in range(0, len(values), mini_batch_size):
                jobs.append(featurizer(values[i : i + mini_batch_size]))
            arrays = run_async_jobs(jobs, concurrency=concurrency)
            return [item for sublist in arrays for item in sublist]

    features = _extract(df[input_column].tolist())
    return df.assign(**{output_column: features})


@contextmanager
def set_conf(conf: dict):
    old_conf = {}
    for k, v in conf.items():
        old_conf[k] = tecton_conf.get_or_none(k)
        tecton_conf.set(k, v)
    try:
        yield
    finally:
        for k, v in old_conf.items():
            tecton_conf.set(k, v)
