import pandas as pd
import pyarrow as pa
from pydantic import Field
from pydantic.fields import FieldInfo
from tecton.types import (
    Array,
    Bool,
    Float64,
    Float32,
    Int32,
    Int64,
    Map,
    String,
    Timestamp,
    SdkDataType,
)
from tecton_core.data_types import DataType, ArrayType, MapType

import datetime
from typing import Annotated, Any, Tuple, get_args, get_origin, List, Dict, Union


def to_tecton_type(type: Any) -> Any:
    """
    Convert an object to a Tecton type

    Args:

        type: The Python type annotation

    Returns:

        Any: The Tecton type
    """
    if get_origin(type) is Annotated:
        type = get_args(type)[0]
    if isinstance(type, pa.DataType):
        if pa.types.is_string(type):
            return String
        if pa.types.is_int32(type):
            return Int32
        if pa.types.is_integer(type):
            return Int64
        if pa.types.is_floating(type):
            return Float64
        if pa.types.is_boolean(type):
            return Bool
        if pa.types.is_timestamp(type):
            return Timestamp
        if pa.types.is_list(type):
            return Array(to_tecton_type(type.value_type))
        raise ValueError(f"Unsupported type {type}")
    if type is str:
        return String
    if type is int:
        return Int64
    if type is float:
        return Float64
    if type is bool:
        return Bool
    if type is pd.Timestamp or type is datetime.datetime:
        return Timestamp
    if get_origin(type) is list:
        return Array(to_tecton_type(get_args(type)[0]))
    if get_origin(type) is dict:
        k = to_tecton_type(get_args(type)[0])
        v = to_tecton_type(get_args(type)[1])
        return Map(k, v)
    raise ValueError(f"Unsupported type {type}")


def tecton_type_to_python_annotation(dtype: Union[SdkDataType, DataType]) -> Any:
    tp = dtype.tecton_type if isinstance(dtype, SdkDataType) else dtype
    if String.tecton_type == tp:
        return str
    elif Int32.tecton_type == tp:
        return int
    elif Int64.tecton_type == tp:
        return int
    elif Float32.tecton_type == tp:
        return float
    elif Float64.tecton_type == tp:
        return float
    elif Bool.tecton_type == tp:
        return bool
    elif Timestamp.tecton_type == tp:
        return datetime.datetime
    elif isinstance(dtype, (Array, ArrayType)):
        return List[tecton_type_to_python_annotation(dtype.element_type)]
    elif isinstance(dtype, (Map, MapType)):
        return Dict[
            tecton_type_to_python_annotation(tp.key_type),
            tecton_type_to_python_annotation(tp.value_type),
        ]
    raise ValueError(f"Unsupported tecton type {type(tp)}")


def parse_python_annotation(annotation: Any) -> Tuple[Any, FieldInfo]:
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        if len(args) != 2:
            raise ValueError(
                "Annotated should have exactly 2 arguments, type and description"
            )
        if isinstance(args[1], str):
            return args[0], Field(description=args[1])
        elif isinstance(args[1], FieldInfo):
            return args[0], args[1]
        else:
            raise ValueError("Invalid Annotated type")
    return annotation, Field()
