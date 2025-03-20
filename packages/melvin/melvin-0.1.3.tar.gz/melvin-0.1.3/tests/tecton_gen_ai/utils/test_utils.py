from dataclasses import dataclass
from typing import List

from pydantic import BaseModel
from pytest import raises
from tecton import Entity, RequestSource
from tecton.types import Field as TectonField
from tecton.types import Int32, Int64, String

from melvin.tecton_gen_ai.tecton_utils._internal import _ArgumentParser, entity_to_pydantic


def test_entity_to_pydantic():
    def _assert(keys, description, schema):
        model = entity_to_pydantic(
            Entity(name="a", join_keys=keys, description=description), keys
        )
        actual = model.model_json_schema()
        del actual["title"]
        expected = schema.model_json_schema()
        del expected["title"]
        assert actual == expected

    class Expected(BaseModel):
        """hello"""

        a: str
        b: int

    _assert(
        [
            TectonField("a", String),
            TectonField("b", Int64),
        ],
        "hello",
        Expected,
    )


def test_parse_arguments():
    def _parse_arguments(f, fvs, assert_entity_defined):
        ap = _ArgumentParser(f, fvs, assert_entity_defined)
        return ap.llm_args, ap.feature_args, ap.entitye_args, ap.has_request_source

    fvs = [
        _mock_fv("fv1", ["c", "d"]),
        _mock_fv("fv2", ["c", "d"]),
    ]

    def ff1(c, d, a, fv1, b, fv2):
        pass

    def ff2(a, fv1, b, fv2):
        pass

    def ff3(d, a, fv1, b, fv2):
        pass

    assert _parse_arguments(ff1, fvs, assert_entity_defined=True) == (
        ["c", "d", "a", "b"],
        ["fv1", "fv2"],
        ["c", "d"],
        False,
    )

    assert _parse_arguments(ff2, fvs, assert_entity_defined=False) == (
        ["a", "b"],
        ["fv1", "fv2"],
        ["c", "d"],
        False,
    )

    assert _parse_arguments(ff1, [], assert_entity_defined=False) == (
        ["c", "d", "a", "fv1", "b", "fv2"],
        [],
        [],
        False,
    )

    with raises(ValueError):
        _parse_arguments(ff2, fvs, assert_entity_defined=True)

    with raises(ValueError):
        _parse_arguments(ff3, fvs, assert_entity_defined=True)

    rfvs = [
        RequestSource(schema=[TectonField("a", String), TectonField("b", Int32)]),
        _mock_fv("fv1", ["c", "d"]),
        _mock_fv("fv2", ["c", "d"]),
    ]

    def ff4(req, fv1, fv2):  # with request_source
        pass

    assert _parse_arguments(ff4, rfvs, assert_entity_defined=False) == (
        ["a", "b"],
        ["fv1", "fv2"],
        ["c", "d"],
        True,
    )

    with raises(ValueError):
        _parse_arguments(ff1, rfvs, assert_entity_defined=False)


def _mock_fv(name, keys):
    @dataclass
    class MockFV:
        name: str
        join_keys: List[str]

    return MockFV(name, keys)
