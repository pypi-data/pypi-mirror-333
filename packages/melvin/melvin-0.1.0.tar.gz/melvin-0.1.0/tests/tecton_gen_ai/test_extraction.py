from pydantic import BaseModel, Field
from pytest import fixture

from src.tecton_gen_ai.api import llm_extraction
from src.tecton_gen_ai.testing import make_local_source
from src.tecton_gen_ai.tecton_utils._internal import get_local_source_attrs
from src.tecton_gen_ai.tecton_utils._tecton_utils import make_entity


@fixture
def mock_source():
    return make_local_source(
        "name_and_age",
        [
            {"s1": "my name is Jim", "s2": "my age is 20"},
            {"s1": "my name is John", "s2": "my age is 30"},
        ],
        description="User info",
    )


@fixture
def extraction_config():
    class ExtractName(BaseModel):
        name: str = Field(description="mentioned name")

    class ExtractAge(BaseModel):
        age: int = Field(description="mentioned age")

    return [
        {
            "column": "s1",
            "schema": ExtractName,
            "enable_local_cache": False,
        },
        {
            "column": "s2",
            "schema": ExtractAge,
            "enable_local_cache": False,
        },
    ]


def test_llm_extraction(set_default_llm, extraction_config, mock_source):
    entity = make_entity(name=str)
    e = llm_extraction(
        source=mock_source, extraction_config=extraction_config, entities=[entity]
    )
    attrs = get_local_source_attrs(mock_source)
    df = e.run_transformation(
        start_time=attrs["start_time"], end_time=attrs["end_time"]
    ).to_pandas()
    assert df[["name", "age"]].to_dict(orient="records") == [
        {"name": "Jim", "age": 20},
        {"name": "John", "age": 30},
    ]
