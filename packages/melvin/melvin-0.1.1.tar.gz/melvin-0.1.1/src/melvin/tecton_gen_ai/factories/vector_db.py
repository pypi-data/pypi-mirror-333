from functools import singledispatch
from typing import Any

from ..utils.config_wrapper import ConfigWrapper
from ..utils.runtime import RuntimeVar

from .llm import _load_dependencies


def make_vector_db(obj: Any, conf: bool) -> Any:
    """
    Make a vector database object or the config wrapper. This is not for users to call directly.

    Args:

        obj: The object
        conf: whether to make a config wrapper
    """
    _load_dependencies()
    if conf:
        return make_vector_db_conf(obj)
    return make_vector_db_instance(RuntimeVar.materialize(obj))


@singledispatch
def make_vector_db_instance(obj: Any) -> Any:
    """
    Make a vector database object. This is not for users to call directly.

    Args:

        obj: The object
    """
    if isinstance(obj, ConfigWrapper):
        return make_vector_db(obj.instantiate())
    raise NotImplementedError(f"Unsupported type {type(obj)}")


@singledispatch
def make_vector_db_conf(obj: Any) -> ConfigWrapper:
    """
    Make a config wrapper of a vector database object. This is not for users to call directly.

    Args:

        obj: The object
    """
    if isinstance(obj, ConfigWrapper):
        return obj
    raise NotImplementedError(f"Unsupported type {type(obj)}")
