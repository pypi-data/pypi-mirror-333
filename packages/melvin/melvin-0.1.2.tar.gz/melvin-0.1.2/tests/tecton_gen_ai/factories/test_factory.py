from langchain_community.vectorstores.lancedb import LanceDB
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from melvin.tecton_gen_ai.factories.llm import invoke_llm, make_llm
from melvin.tecton_gen_ai.factories.vector_db import make_vector_db
from melvin.tecton_gen_ai.utils.config_wrapper import ConfigWrapper
from pydantic import BaseModel, Field
from pytest import raises


def test_make_llm():
    llm = make_llm("openai/text-embedding-3-small", conf=False)
    assert isinstance(llm, OpenAIEmbeddings)
    assert llm is make_llm(llm, conf=False)
    llm = make_llm({"model": "openai/gpt-4o-mini", "temperature": 0.1}, conf=False)
    assert isinstance(llm, ChatOpenAI)
    assert llm.temperature == 0.1
    assert llm is make_llm(llm, conf=False)

    llm_conf = make_llm("openai/gpt-4o-mini", conf=True)
    assert isinstance(llm_conf, ConfigWrapper)
    assert isinstance(llm_conf.instantiate(), ChatOpenAI)


def test_invoke_llm():
    llm = make_llm({"model": "openai/gpt-4o-mini", "temperature": 0}, conf=False)
    assert "2" in invoke_llm(llm, "result of 1+1")

    class Output(BaseModel):
        result: int = Field(description="The result")

    assert 2 == invoke_llm(llm, "result of 1+1", output_schema=Output).result
    assert (
        2
        == invoke_llm(
            llm,
            "result of {problem}",
            output_schema=Output,
            template_kwargs={"problem": "1+1", "dummy": 1},
        ).result
    )

    assert (
        2
        == invoke_llm(
            llm,
            [["system", "Solve a {a} problem"], ["user", "{b}"]],
            output_schema=Output,
            template_kwargs={"a": "math", "b": "1+1"},
        ).result
    )

    with raises(NotImplementedError):
        invoke_llm(1, "result of 1+1")


def test_make_vector_db():
    vdb = make_vector_db(
        {
            "provider": "lancedb",
            "uri": "/tmp/t.db",
            "embedding": "openai/text-embedding-3-small",
        },
        conf=False,
    )
    assert isinstance(vdb, LanceDB)
    assert isinstance(vdb.embeddings, OpenAIEmbeddings)
    assert vdb is make_vector_db(vdb, conf=False)

    vdb = make_vector_db(
        {
            "provider": "lancedb",
            "uri": "/tmp/t.db",
            "embedding": "openai/text-embedding-3-small",
        },
        conf=True,
    )
    assert isinstance(vdb, ConfigWrapper)
    vdb = vdb.instantiate()
    assert isinstance(vdb, LanceDB)
    assert isinstance(vdb.embeddings, OpenAIEmbeddings)
