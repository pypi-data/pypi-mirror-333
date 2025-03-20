from pytest import fixture

from src.tecton_gen_ai.api import Configs, RuntimeVar, VectorDBConfig, source_as_knowledge
from src.tecton_gen_ai.tecton_utils._tecton_utils import set_conf
from src.tecton_gen_ai.testing import make_local_source, set_dev_mode
from src.tecton_gen_ai.testing.utils import make_local_vector_db_config
from pydantic import BaseModel, Field


class Filter(BaseModel):
    zip: int = Field(description="Zip code")


@fixture
def tecton_unit_test():
    set_dev_mode()

    with set_conf(
        {
            "TECTON_FORCE_FUNCTION_SERIALIZATION": "false",
            "DUCKDB_EXTENSION_REPO": "",
            "TECTON_SKIP_OBJECT_VALIDATION": "true",
            "TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE": "rift",
            "TECTON_BATCH_COMPUTE_MODE": "rift",
        }
    ):
        yield


@fixture
def tecton_vector_db_test_config(tmp_path):
    path = str(tmp_path / "test.db")
    return make_local_vector_db_config(path, remove_if_exists=True)


@fixture
def mock_knowledge(tecton_unit_test, tecton_vector_db_test_config):
    data = [
        {"zip": 98005, "item_id": 1, "description": "pencil"},
        {"zip": 98005, "item_id": 2, "description": "car"},
        {"zip": 98005, "item_id": 3, "description": "paper"},
        {"zip": 10065, "item_id": 4, "description": "boat"},
        {"zip": 10065, "item_id": 5, "description": "cheese"},
        {"zip": 10065, "item_id": 6, "description": "apple"},
    ]
    knowledge_src = make_local_source(
        "knowledge", data, auto_timestamp=True, description="Items for sale"
    )

    return source_as_knowledge(
        knowledge_src,
        VectorDBConfig(
            name=knowledge_src.name,
            vector_db=tecton_vector_db_test_config,
            filter=Filter,
        ),
        vectorize_column="description",
    )


@fixture
def set_default_llm(tecton_unit_test):
    with Configs(
        llm={
            "model": "openai/gpt-4o-2024-11-20",
            "api_key": RuntimeVar(name="OPENAI_API_KEY"),
            # "model": "anthropic/claude-3-5-sonnet-20241022",
            # "api_key": RuntimeVar(name="ANTHROPIC_API_KEY"),
            "temperature": 0,
        }
    ).update_default():
        yield
