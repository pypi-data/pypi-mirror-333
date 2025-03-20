import os
from dataclasses import dataclass
from typing import Any

from pytest import raises

from melvin.tecton_gen_ai.utils.config_wrapper import (
    ExternalArgument,
    RuntimeVar,
    as_config,
    from_json_config,
    to_json_config,
)
from melvin.tecton_gen_ai.utils.hashing import to_uuid
from melvin.tecton_gen_ai.utils.runtime import runtime_context


@dataclass
class TestObj:
    """This is a test"""

    a: int
    b: Any

    def __eq__(self, other):
        return self.a == other.a and str(self.b) == str(other.b)

    def __str__(self):
        return f"TestObj(a={self.a}, b={self.b})"


class TestObj3:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self):
        return self.a + self.b

    def __json_config_dict__(self):
        return {"a": self.a, "b": self.b}


def test_config_wrapper():
    TestObjConfig = as_config(TestObj)
    w = TestObjConfig(a=1, b="hello")
    assert w.target_type == TestObj
    assert w.instantiate() == TestObj(a=1, b="hello")
    from_json_config(w.to_json()) == TestObj(a=1, b="hello")

    w0 = TestObjConfig(a=1, b=None)
    w = TestObjConfig(a=1, b=w0)
    assert w.instantiate() == TestObj(a=1, b=TestObj(a=1, b=None))
    obj = from_json_config(to_json_config(w))
    assert obj == TestObj(a=1, b=TestObj(a=1, b=None))
    assert isinstance(obj.b, TestObj)

    w0 = TestObjConfig(a=ExternalArgument(name="x"), b=None)
    w = TestObjConfig(a=ExternalArgument(name="y"), b=w0)
    assert w.instantiate({"x": 1, "y": 2}) == TestObj(a=2, b=TestObj(a=1, b=None))
    with raises(KeyError):
        w.instantiate()
    from_json_config(w.to_json(), {"x": 1, "y": 2}) == TestObj(
        a=2, b=TestObj(a=1, b=None)
    )

    w0 = TestObjConfig(a=RuntimeVar(name="x"), b=None)
    w = TestObjConfig(a=RuntimeVar(name="y"), b=w0)
    with runtime_context({"tecton_secrets": {"x": 3, "y": 4}}):
        assert w.instantiate() == TestObj(a=4, b=TestObj(a=3, b=None))
        assert from_json_config(w.to_json()) == TestObj(a=4, b=TestObj(a=3, b=None))

    w = to_json_config({"a": 1, "b": {"c": RuntimeVar(name="x")}})
    with runtime_context({"tecton_secrets": {"x": 3}}):
        assert from_json_config(w) == {"a": 1, "b": {"c": 3}}

    w = to_json_config(TestObj3(1, RuntimeVar(name="x")))
    with runtime_context({"tecton_secrets": {"x": 3}}):
        assert from_json_config(w).compute() == 4


def test_temp():
    from langchain_community.vectorstores.lancedb import LanceDB
    from langchain_openai import OpenAIEmbeddings

    LanceDBConf = as_config(LanceDB)
    OpenAIEmbeddingsConf = as_config(OpenAIEmbeddings)

    vdb = LanceDBConf(embedding=OpenAIEmbeddingsConf(), uri="sdf")
    assert isinstance(
        from_json_config(to_json_config(vdb)).embeddings, OpenAIEmbeddings
    )


def test_context_var():
    v = RuntimeVar(name="_test")
    with raises(ValueError):
        v.get()
    v = RuntimeVar(name="_test", sources=["secrets"])
    with raises(ValueError):
        v.get()
    with runtime_context({"tecton_secrets": {"_test": "1"}}):
        assert v.get() == "1"
    v = RuntimeVar(name="_test", sources=["secrets", "env"])
    with raises(ValueError):
        v.get()
    with runtime_context({"tecton_secrets": {"_test": "1"}}):
        assert v.get() == "1"
    os.environ["_test"] = "2"
    assert v.get() == "2"
    with runtime_context({"tecton_secrets": {"_test": "1"}}):
        assert v.get() == "1"
    v = RuntimeVar(name="_test")
    os.environ["_test"] = "2"
    with runtime_context({"tecton_secrets": {"_test": "1"}}):
        assert v.get() == "2"
        assert RuntimeVar.materialize(v) == "2"
        assert RuntimeVar.materialize({"a": {"b": v}}) == {"a": {"b": "2"}}
        assert RuntimeVar.materialize(1) == 1

    os.environ["_test"] = "1"
    uid1 = to_uuid(v)
    os.environ["_test"] = "2"
    uid2 = to_uuid(v)
    uid3 = to_uuid(v)
    assert uid1 != uid2
    assert uid2 == uid3
