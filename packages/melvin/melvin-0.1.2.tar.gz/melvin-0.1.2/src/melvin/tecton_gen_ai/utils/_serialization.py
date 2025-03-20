import inspect
import json
from datetime import datetime
from functools import lru_cache
from textwrap import dedent
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Type, Union

from pydantic import BaseModel, Field, create_model


def serialize_pydantic(obj: Type[BaseModel]) -> str:
    return json.dumps(to_openai_function(obj))


@lru_cache
def deserialize_pydantic(model_json: str) -> Type[BaseModel]:
    return openai_function_to_pydantic(json.loads(model_json))


def to_openai_function(
    obj: Union[Callable, Type[BaseModel]],
    name: Optional[str] = None,
    exclude_args: Optional[Iterator[str]] = None,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    exclude = set(exclude_args or [])

    if inspect.isclass(obj) and issubclass(obj, BaseModel):
        from openai import pydantic_function_tool

        res = dict(pydantic_function_tool(obj))["function"]
    else:
        from langchain_core.utils.function_calling import convert_to_openai_function

        res = convert_to_openai_function(obj)
    res["name"] = name or res["name"]
    if description is not None or obj.__doc__ is not None:
        res["description"] = description or dedent(obj.__doc__)
    properties = res["parameters"]["properties"]
    for key in list(properties.keys()):
        if key in exclude:
            del properties[key]
    return res


def openai_function_to_pydantic(
    model: Dict[str, Any], name: Optional[str] = None
) -> Type[BaseModel]:
    return openai_properties_to_pydantic(
        model["parameters"]["properties"],
        name=name or model["name"],
        description=model.get("description"),
    )


def to_openai_properties(
    func: Union[Callable, Type[BaseModel], List[Tuple[str, Any]]], args: List[str]
) -> Dict[str, Any]:
    if inspect.isclass(func) and issubclass(func, BaseModel):
        new_fields = {
            k: (v.annotation, v) for k, v in func.model_fields.items() if k in args
        }
        model = create_model("temp", **new_fields)
    else:
        from ..tecton_utils.convert import parse_python_annotation

        if isinstance(func, list):
            annotations = func
        else:
            annotations = list(func.__annotations__.items())
        fields: Dict[str, Any] = {}
        for k, v in annotations:
            if k not in args:
                continue
            v, field = parse_python_annotation(v)
            fields[k] = (v, field)
        model = create_model("temp", **fields)
    res = to_openai_function(model)
    return res["parameters"]["properties"]


def openai_properties_to_pydantic(
    properties: Dict[str, Any],
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Type[BaseModel]:
    fields = {}
    for name, value in properties.items():
        dtype = openai_type_to_python_type(value)
        fparams = {}
        if "description" in value:
            fparams["description"] = value["description"]
        if "default" in value:
            fparams["default"] = value["default"]
        fields[name] = (dtype, Field(**fparams))
    return create_model(name or "temp", __doc__=description, **fields)


def openai_type_to_python_type(tp: Dict[str, Any]) -> Any:
    if "anyOf" in tp:
        tps = [openai_type_to_python_type(t) for t in tp["anyOf"]]
        return Union[tuple(tps)]
    value = tp.get("type")
    if value == "integer":
        return int
    if value == "number":
        return float
    if value == "boolean":
        return bool
    if value == "string":
        format = tp.get("format", "")
        if format == "":
            return str
        if format == "date-time":
            return datetime
        raise NotImplementedError(f"Unsupported string format {format}")
    if value == "null":
        return None
    if value == "array":
        if "items" in tp:
            items = tp["items"]
            return List[openai_type_to_python_type(items)]
        if "prefixItems" in tp:
            pitems = [openai_type_to_python_type(t) for t in tp["prefixItems"]]
            return Tuple[tuple(pitems)]
    if value == "object":
        additional = tp.get("additionalProperties")
        if additional is not None:
            return Dict[str, openai_type_to_python_type(additional)]
    raise NotImplementedError(f"Unsupported openai data type {tp}")


def _annotation(_type: Any) -> str:
    if _type is None:
        return "None"
    if _type in (str, int, float, bool):
        return _type.__name__
    if _type is Any:
        return "Any"
    if _type.__origin__ is list:
        return f"List[{_annotation(_type.__args__[0])}]"
    if _type.__origin__ is dict:
        return (
            f"Dict[{_annotation(_type.__args__[0])}, {_annotation(_type.__args__[1])}]"
        )
    raise NotImplementedError(f"Unsupported annotation ype {_type}")
