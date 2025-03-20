from datetime import datetime
from typing import Annotated, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field
from pytest import raises

from melvin.tecton_gen_ai.utils._serialization import (
    to_openai_properties,
    openai_function_to_pydantic,
    openai_properties_to_pydantic,
    openai_type_to_python_type,
    to_openai_function,
)


class Input1(BaseModel):
    """
    hello
    world"""

    a: str = Field(description="a description")
    b: int = Field(description="b description")
    c: float = Field(description="c description", default=0.1)
    d: bool = Field(description="d description")
    e: List[str] = Field(description="e description")
    f: Dict[str, int] = Field(description="f description")
    g: datetime = Field(description="g description")
    h: List[Tuple[str, str]] = Field(description="h description", default=[])
    i: Optional[List[Tuple[str, str]]] = Field(description="i description")


class Input2(BaseModel):
    pass


class Input3(BaseModel):
    """hello"""

    a: str


class Output(BaseModel):
    a: int = Field(description="a description")


def test_to_openai_function():
    res = to_openai_function(Input1, "test1")
    assert res["description"] == "\nhello\nworld"
    model = openai_function_to_pydantic(res, name="Input1")
    assert model.__doc__ == "\nhello\nworld"
    _assert_eq(Input1, model)

    def f(a: str) -> int:
        """hello"""
        pass

    res = openai_function_to_pydantic(to_openai_function(f, "test1"), name="Input3")
    _assert_eq(Input3, res)


def test_openai_type_to_python_type():
    assert openai_type_to_python_type({"type": "integer"}) is int
    assert openai_type_to_python_type({"type": "number"}) is float
    assert openai_type_to_python_type({"type": "boolean"}) is bool
    assert openai_type_to_python_type({"type": "string"}) is str
    assert (
        openai_type_to_python_type({"type": "array", "items": {"type": "string"}})
        == List[str]
    )
    assert (
        openai_type_to_python_type(
            {"type": "object", "additionalProperties": {"type": "integer"}}
        )
        == Dict[str, int]
    )
    assert (
        openai_type_to_python_type({"type": "string", "format": "date-time"})
        == datetime
    )
    with raises(NotImplementedError):
        openai_type_to_python_type({"type": "string", "format": "date"})


def test_extract_parameters_into_openai_properties():
    class Dummy:
        pass

    def f(
        a: str,
        b: Dummy,
        c: Annotated[int, Field(description="hello")],
        d: Annotated[str, "world"],
    ):
        pass

    res = to_openai_properties(f, ["a", "c", "d"])
    actual = openai_properties_to_pydantic(res, name="Expected")

    class Expected(BaseModel):
        a: str
        c: int = Field(description="hello")
        d: str = Field(description="world")

    _assert_eq(Expected, actual)

    class Expected2(BaseModel):
        a: str
        d: str = Field(description="world")

    res = to_openai_properties(Expected, ["a", "d"])
    actual = openai_properties_to_pydantic(res, name="Expected2")

    _assert_eq(Expected2, actual)

    res = to_openai_properties([("a", str), ("d", Annotated[str, "world"])], ["a", "d"])
    actual = openai_properties_to_pydantic(res, name="Expected2")

    _assert_eq(Expected2, actual)


def _assert_eq(a: BaseModel, b: BaseModel):
    expected = a.model_json_schema()
    del expected["title"]
    actual = b.model_json_schema()
    del actual["title"]
    assert expected == actual
