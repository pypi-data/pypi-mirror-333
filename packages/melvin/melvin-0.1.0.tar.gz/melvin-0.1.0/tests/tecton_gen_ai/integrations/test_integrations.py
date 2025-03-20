import json
from dataclasses import dataclass

from pytest import fixture

from src.tecton_gen_ai.api import Agent
from src.tecton_gen_ai.testing import make_local_batch_feature_view


@dataclass
class OpenAIConfig:
    model: str
    seed: int
    temperature: float
    response_format: dict

    def to_langchain_kwargs(self):
        return {
            "model": self.model,
            "seed": self.seed,
            "temperature": self.temperature,
            "model_kwargs": {"response_format": self.response_format},
        }

    def to_llamaindex_kwargs(self):
        return {
            "model": self.model,
            "additional_kwargs": {"response_format": self.response_format},
            "temperature": self.temperature,
        }


@fixture
def model_config():
    return OpenAIConfig(
        model="gpt-4o-2024-08-06",
        seed=0,
        temperature=0,
        response_format={"type": "json_object"},
    )


@fixture
def langchain_llm(model_config):
    import langchain
    from langchain_openai import ChatOpenAI

    from src.tecton_gen_ai.utils.config_wrapper import as_config

    langchain.debug = True

    Conf = as_config(ChatOpenAI)

    return Conf(**model_config.to_langchain_kwargs())


@fixture
def llamaindex_llm(model_config):
    from llama_index.llms.openai import OpenAI

    from src.tecton_gen_ai.utils.config_wrapper import as_config

    Conf = as_config(OpenAI)

    return Conf(**model_config.to_llamaindex_kwargs())


@fixture
def mock_agent_service(tecton_unit_test, mock_knowledge):
    user_info = make_local_batch_feature_view(
        "user_info",
        {"user_id": "user2", "name": "Jim"},
        ["user_id"],
        description="Getting user name",
    )

    def sys_prompt():
        return (
            # "You are serving user whose user_id " + user_id + ". "
            "The result should be in json format, the key is always 'result'"
        )

    def get_tecton_employee_count() -> int:
        """
        Returns the number of employees in Tecton
        """
        return 110

    def get_tecton_female_employee_count() -> int:
        """
        Returns the number of female employees in Tecton
        """
        return 60

    return lambda llm: Agent(
        name="test",
        tools=[
            get_tecton_employee_count,
            get_tecton_female_employee_count,
            user_info,
        ],
        prompt=sys_prompt,
        knowledge=[mock_knowledge],
        llm=llm,
    )


def _test_langchain_agent(mock_agent_service, langchain_llm):
    client = mock_agent_service(langchain_llm)
    res = client.invoke(
        "how many employees in tecton that are not female",
        context={"user_id": "user2"},
    )
    assert json.loads(res)["result"] == 50

    agent = client.make_local_agent(langchain_llm.instantiate())
    with client.set_context({"user_id": "user2"}):
        res = agent.invoke({"input": "what is my name"})
    assert "jim" in json.loads(res)["result"].lower()

    with client.set_context({"user_id": "user2", "zip": "10065"}):
        res = agent.invoke({"input": "what food are for sale"})
    assert "apple" in res.lower()


def test_llamaindex_agent(mock_agent_service, llamaindex_llm):
    client = mock_agent_service(llamaindex_llm)
    res = client.invoke(
        "how many employees in tecton that are not female",
        context={"user_id": "user2"},
    )
    assert json.loads(res)["result"] == 50

    agent = client.make_local_agent(llamaindex_llm.instantiate())
    with client.set_context({"user_id": "user2"}):
        res = str(agent.chat("what is my name"))
    assert "jim" in json.loads(res)["result"].lower()

    with client.set_context({"user_id": "user2", "zip": "10065"}):
        res = str(agent.chat("what food are for sale"))
    assert "apple" in res.lower()
