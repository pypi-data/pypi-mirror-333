from functools import lru_cache, singledispatch
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from pydantic import BaseModel

from ..utils.config_wrapper import ConfigWrapper
from ..utils.runtime import RuntimeVar


@lru_cache
def _load_dependencies():
    from ..integrations import langchain
    from ..integrations import llama_index


@singledispatch
def make_llm_model(obj: Any) -> Any:
    """
    Make a LLM object. This is not for users to call directly.

    Args:

        obj: The object
    """
    if isinstance(obj, ConfigWrapper):
        return make_llm_model(obj.instantiate())
    if isinstance(obj, str):
        return make_llm_model({"model": obj})
    raise NotImplementedError(f"Unsupported type {type(obj)}")  # pragma: no cover


@singledispatch
def make_llm_model_conf(obj: Any) -> ConfigWrapper:
    """
    Make a config wrapper of a LLM object. This is not for users to call directly.

    Args:

        obj: The object
    """
    if isinstance(obj, ConfigWrapper):
        return obj
    if isinstance(obj, str):
        return make_llm_model_conf({"model": obj})
    raise NotImplementedError(f"Unsupported type {type(obj)}")  # pragma: no cover


def make_llm(obj: Any, conf: bool) -> Any:
    """
    Make a LLM object or the config wrapper. This is not for users to call directly.

    Args:

        obj: The object
        conf: whether to make a config wrapper
    """
    _load_dependencies()
    if conf:
        return make_llm_model_conf(obj)
    return make_llm_model(RuntimeVar.materialize(obj))


@singledispatch
def invoke_llm_model(
    obj: Any,
    prompt: Union[str, List[Tuple[str, str]]],
    output_schema: Union[Type[BaseModel], Type[str]] = str,
) -> Any:
    """
    Invoke a LLM object. This is not for users to call directly.

    Args:

        obj: The object
        prompt: The prompt
        output_schema: The output schema

    Returns:

        The output based on the output schema
    """
    raise NotImplementedError(f"Unsupported LLM type {type(obj)}")


def invoke_llm(
    obj: Any,
    prompt: Union[str, List[Tuple[str, str]]],
    output_schema: Union[Type[BaseModel], Type[str]] = str,
    template_kwargs: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Invoke a LLM object. This is not for users to call directly.

    Args:

        obj: The LLM object, commonly from `make_llm`
        prompt: The prompt, either a string or a list of tuples of (role, text).
            It can contain templates that will be rendered with `template_kwargs`
        output_schema: The output schema, defaults to str
        template_kwargs: The template kwargs, defaults to None

    Returns:

        The output based on the output schema
    """
    _load_dependencies()
    prompt = _build_prompt(prompt, template_kwargs)
    return invoke_llm_model(obj, prompt=prompt, output_schema=output_schema)


def _build_prompt(
    prompt: Union[str, List[Tuple[str, str]]],
    template_kwargs: Optional[Dict[str, Any]] = None,
) -> Union[str, List[Tuple[str, str]]]:
    if template_kwargs:
        if isinstance(prompt, str):
            prompt = prompt.format(**template_kwargs)
        else:
            prompt = [(role, text.format(**template_kwargs)) for role, text in prompt]
    return prompt
