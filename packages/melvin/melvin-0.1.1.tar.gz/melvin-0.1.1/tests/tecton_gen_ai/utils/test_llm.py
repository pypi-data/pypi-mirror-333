import pytest
from pydantic import BaseModel, Field
from pytest import raises

from src.tecton_gen_ai.utils.config_wrapper import from_json_config, to_json_config
from src.tecton_gen_ai.utils.llm import LLMGenerationConfig

ENGINES = ["langchain", "instructor"]


@pytest.mark.parametrize("engine", ENGINES)
def test_llm_gen(set_default_llm, engine):
    conf = from_json_config(to_json_config(LLMGenerationConfig()))
    assert "2" in conf.invoke({"question": "1+1=?"})

    conf = from_json_config(
        to_json_config(LLMGenerationConfig(prompt="Solve a math problem 1+1"))
    )
    assert "2" in conf.invoke()

    class Output(BaseModel):
        answer: int = Field(description="The number as the answer")

    conf = from_json_config(
        to_json_config(
            LLMGenerationConfig(
                llm="openai/gpt-4o", output_schema=Output, engine=engine
            )
        )
    )
    assert 2 == conf.invoke({"question": "1+1"})["answer"]
    assert 2 == conf.invoke({"question": "1+1"}, keep_pydantic=True).answer

    LLMGenerationConfig().assert_template_args(["question"])
    with raises(ValueError):
        LLMGenerationConfig(prompt="abc").assert_template_args(["question"])
    LLMGenerationConfig(prompt="abc").assert_template_args([])
    lg = LLMGenerationConfig(prompt=[("system", "a{x}"), ("user", "b{y}")])
    lg.assert_template_args(["x", "y"])
    with raises(ValueError):
        lg.assert_template_args(["x"])
