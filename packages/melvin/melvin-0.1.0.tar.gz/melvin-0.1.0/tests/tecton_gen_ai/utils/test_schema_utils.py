from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import ClassVar

import pytest
from tecton.types import Array, Bool, Field, Float64, Int64, String, Struct, Timestamp

from src.tecton_gen_ai.tecton_utils._schema_utils import (
    get_tecton_fields_from_json_schema,
    load_to_rich_dict,
)


@dataclass
class ParseTestCase:
    json_str: str
    expected: dict


@dataclass
class TectonFieldExtractionTestCase:
    name: str
    schema: dict
    expected_fields: list[Field]
    parse_test_cases: list[ParseTestCase]
    test_cases: ClassVar[dict[str, "TectonFieldExtractionTestCase"]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        schema: dict,
        expected_fields: list[Field],
        parse_test_cases: list[ParseTestCase],
    ):
        cls.test_cases[name] = cls(name, schema, expected_fields, parse_test_cases)

    @classmethod
    def get_test_cases(cls) -> list[TectonFieldExtractionTestCase]:
        return list(cls.test_cases.values())

    @classmethod
    def get(cls, name: str) -> TectonFieldExtractionTestCase:
        if test_case := cls.test_cases.get(name):
            return test_case
        raise ValueError(f"Test case with name {name} not found")


TectonFieldExtractionTestCase.register(
    name="simple_schema",
    schema={
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "is_student": {"type": "boolean"},
        },
    },
    expected_fields=[
        Field(name="name", dtype=String),
        Field(name="age", dtype=Int64),
        Field(name="is_student", dtype=Bool),
    ],
    parse_test_cases=[
        ParseTestCase(
            json_str='{"name": "John", "age": 30, "is_student": false}',
            expected={"name": "John", "age": 30, "is_student": False},
        ),
    ],
)

TectonFieldExtractionTestCase.register(
    name="nested_schema",
    schema={
        "type": "object",
        "properties": {
            "person": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "birthdate": {"type": "string", "format": "date-time"},
                },
            },
            "scores": {
                "type": "array",
                "items": {"type": "number"},
            },
        },
    },
    expected_fields=[
        Field(
            name="person",
            dtype=Struct(
                [
                    Field(name="name", dtype=String),
                    Field(name="birthdate", dtype=Timestamp),
                ]
            ),
        ),
        Field(name="scores", dtype=Array(Float64)),
    ],
    parse_test_cases=[
        ParseTestCase(
            json_str='{"person": {"name": "John", "birthdate": "2023-01-01T00:00:00Z"}, "scores": [95.5, 88.0]}',
            expected={
                "person": {
                    "name": "John",
                    "birthdate": datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                },
                "scores": [95.5, 88.0],
            },
        ),
    ],
)

TectonFieldExtractionTestCase.register(
    name="ref_schema",
    schema={
        "definitions": {
            "person": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                },
            }
        },
        "type": "object",
        "properties": {
            "student": {"$ref": "#/definitions/person"},
        },
    },
    expected_fields=[
        Field(
            name="student",
            dtype=Struct(
                [Field(name="name", dtype=String), Field(name="age", dtype=Int64)]
            ),
        ),
    ],
    parse_test_cases=[
        ParseTestCase(
            json_str='{"student": {"name": "John", "age": 30}}',
            expected={"student": {"name": "John", "age": 30}},
        ),
    ],
)

TectonFieldExtractionTestCase.register(
    name="enum_ref_schema",
    # This tests both `enum` and the recursive reference to a ref
    schema={
        "defs": {  # Using 'defs' instead of 'definitions' (we want to test both scenarios since pydantic uses `defs`)
            "status": {"type": "string", "enum": ["active", "inactive", "pending"]},
            "employee": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "status": {"$ref": "#/defs/status"},
                },
            },
        },
        "type": "object",
        "properties": {
            "worker": {"$ref": "#/defs/employee"},
        },
    },
    expected_fields=[
        Field(
            name="worker",
            dtype=Struct(
                [
                    Field(name="name", dtype=String),
                    Field(name="status", dtype=String),
                ]
            ),
        ),
    ],
    parse_test_cases=[
        ParseTestCase(
            json_str='{"worker": {"name": "Alice", "status": "active"}}',
            expected={"worker": {"name": "Alice", "status": "active"}},
        ),
    ],
)


@pytest.mark.parametrize(
    "test_case", TectonFieldExtractionTestCase.get_test_cases(), ids=lambda x: x.name
)
def test_get_tecton_fields_from_json_schema(test_case: TectonFieldExtractionTestCase):
    fields = get_tecton_fields_from_json_schema(test_case.schema)
    assert len(fields) == len(test_case.expected_fields)
    for expected_field, field in zip(test_case.expected_fields, fields):
        assert expected_field.name == field.name
        assert expected_field.dtype == field.dtype


@pytest.mark.parametrize(
    "test_case", TectonFieldExtractionTestCase.get_test_cases(), ids=lambda x: x.name
)
def test_load_to_rich_dict(test_case: TectonFieldExtractionTestCase):
    for parse_test_case in test_case.parse_test_cases:
        result = load_to_rich_dict(parse_test_case.json_str, test_case.schema)
        assert result == parse_test_case.expected


if __name__ == "__main__":
    pytest.main()
