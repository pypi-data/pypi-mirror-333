import pytest
from pydantic import BaseModel, Field
from tecton import resource_provider
import pandas as pd
from melvin.tecton_gen_ai.agent.base import AgentInputModel
from melvin.tecton_gen_ai.api import (
    Agent,
    prompt,
    tool,
    emitter,
    VectorDBConfig,
)
from melvin.tecton_gen_ai.testing import make_local_batch_feature_view


def test_hello_world(set_default_llm):
    agent = Agent(name="hello")
    assert isinstance(agent.invoke("hello"), str)


def test_prompt(set_default_llm):
    # simplest
    agent = Agent(name="hello", prompt="always start with hi")
    assert agent.invoke("hello").lower().startswith("hi")

    # with context
    def prompt1(name: str) -> str:
        return f"You are serving {name}!"

    agent = Agent(name="hello", prompt=prompt1)
    assert (
        "tecton" in agent.invoke("what is my name", context={"name": "tecton"}).lower()
    )

    # with feature view
    bfv = make_local_batch_feature_view(
        name="my_data",
        data=[{"user_id": "u1", "name": "Bob"}],
        entity_keys=["user_id"],
        description="User information",
    )

    @prompt(sources=[bfv])
    def sys_prompt(my_data) -> str:
        return "You are serving " + my_data["name"]

    agent = Agent(name="my_service", prompt=sys_prompt)
    res = agent.invoke("what is my name", context={"zip": "10065", "user_id": "u1"})
    assert "bob" in res.lower()


def test_structured_output(set_default_llm):
    class Output(BaseModel):
        number: int = Field(description="number mentioned in the answer")

    agent = Agent(name="hello", output_schema=Output)
    assert agent.invoke("what is 1+5") == {"number": 6}


def test_tool(set_default_llm):
    class Output(BaseModel):
        number: int = Field(description="number mentioned in the answer")

    def tecon_number_of_employees() -> int:
        """
        Get the number of employees in Tecton
        """
        return 120

    agent = Agent(
        name="my_service", tools=[tecon_number_of_employees], output_schema=Output
    )
    assert agent.invoke("how many employees in tecton") == {"number": 120}


def test_agent_as_tool(set_default_llm):
    class Output(BaseModel):
        number: int = Field(description="number mentioned in the answer")

    def number_of_employees_1() -> int:
        """
        Get the number of employees
        """
        return 120

    tecton_agent = Agent(
        name="tecton_agent",
        description="For all questions about Tecton",
        prompt="You are a useful agent",  # optional
        tools=[number_of_employees_1],
    )

    def number_of_employees_2(year: int) -> int:
        """
        Get the number of employees in a certain year

        Args:

            year: The year
        """
        return 1000 if year != 2024 else 2000

    class Input(AgentInputModel):
        year: int = Field(description="The year mentioned in the question")

    uber_agent = Agent(
        name="uber_agent",
        description="For all questions about Uber",
        input_schema=Input,
        prompt="You are a useful agent",  # optional
        tools=[number_of_employees_2],
    )

    agent = Agent(
        name="agent",
        tools=[tecton_agent, uber_agent],
        prompt="You are a useful agent",  # optional
        output_schema=Output,
    )

    assert agent.invoke("how many more employees in uber than tecton in 2023") == {
        "number": 880
    }

    assert agent.invoke("how many more employees in uber than tecton in 2024") == {
        "number": 1880
    }


@pytest.mark.skip("Resource implementation has bugs")
def test_resources(set_default_llm):
    class Output(BaseModel):
        number: int = Field(description="number mentioned in the answer")

    @resource_provider()
    def resource1() -> int:
        return 120

    @tool(resource_providers={"resource": resource1})
    def tecon_number_of_employees() -> int:
        """
        Get the number of employees in Tecton
        """

        from melvin.tecton_gen_ai.utils.runtime import get_runtime_context

        ctx = get_runtime_context()
        return ctx["tecton_resources"]["resource"]

    agent = Agent(
        name="my_service", tools=[tecon_number_of_employees], output_schema=Output
    )
    assert agent.invoke("how many employees in tecton") == {"number": 120}


def test_session(set_default_llm):
    class Output(BaseModel):
        number: int = Field(description="number mentioned in the answer")

    def get_color_in_the_bag() -> str:
        """
        Get the color in the bag
        """
        from melvin.tecton_gen_ai.api import set_session_var

        set_session_var("number", 123)
        return "red"

    agent1 = Agent(
        name="agent1",
        description="For all questions about color in the bag",
        tools=[get_color_in_the_bag],
    )

    def get_nubmer_of_gifts(color: str) -> int:
        """
        Get the number of gifts based on the color

        Args:

            color: The color
        """
        from melvin.tecton_gen_ai.api import get_session_var

        return get_session_var("number")

    agent = Agent(
        name="my_service",
        tools=[agent1, get_nubmer_of_gifts],
        output_schema=Output,
    )
    assert agent.invoke(
        "get color in the bag, then tell me how many gifts for that color"
    ) == {"number": 123}


def test_emitter(set_default_llm):
    fruit_mentions = []
    budget_mentions = []

    class Output(BaseModel):
        number: int = Field(description="number mentioned in the answer")

    def emit_fruit_mention(fruit: str) -> None:
        """
        When a fruit is mentioned, emit the fruit
        """
        fruit_mentions.append(fruit)

    @emitter(use_history=True)
    def emit_budget_mention(budget: int) -> int:
        """
        When a budget is mentioned, emit the budget
        """
        budget_mentions.append(budget)

    agent = Agent(
        name="my_service",
        emitters=[emit_fruit_mention, emit_budget_mention],
        output_schema=Output,
    )

    # by default, emitter only extracts the lastest message
    fruit_mentions = []
    budget_mentions = []
    assert agent.invoke("i have one apple") == {"number": 1}
    assert fruit_mentions == ["apple"]
    assert budget_mentions == []

    fruit_mentions = []
    budget_mentions = []
    assert agent.invoke(
        "i like number 3",
        chat_history=[("user", "i have an apple"), ("assistant", "ok")],
    ) == {"number": 3}
    assert fruit_mentions == []
    assert budget_mentions == []

    # when use_history=True, emitter considers all messages
    fruit_mentions = []
    budget_mentions = []
    assert agent.invoke(
        "my budget is 20",
        chat_history=[("user", "i have an apple"), ("assistant", "ok")],
    ) == {"number": 20}
    assert fruit_mentions == []
    assert budget_mentions == [20]

    # multiple emissions
    fruit_mentions = []
    budget_mentions = []
    assert agent.invoke(
        "i have an apple and an orange, and i like number 4",
        chat_history=[("user", "my budget is 20"), ("assistant", "ok")],
    ) == {"number": 4}
    assert fruit_mentions == ["apple", "orange"]
    assert budget_mentions == [20]


def test_tool_selection(set_default_llm):
    class Output(BaseModel):
        number: int = Field(description="number mentioned in the answer")

    def _should_include1(input):
        return "dummy_company" in input["message"] and input.get("sign", False)

    @tool(use_when=_should_include1)
    def number_of_employees(company_name: str) -> int:
        """
        Get the number of employees
        """
        return 120

    def _should_include2(input):
        return any("age" in x for x in input.get("chat_history", []))

    @tool(use_when=_should_include2)
    def age_of_company(company_name: str) -> int:
        """
        Get the age of the company
        """
        return 7

    agent = Agent(
        name="agent",
        prompt="If you don't know, return 0",
        tools=[number_of_employees, age_of_company],
        output_schema=Output,
    )

    assert agent.invoke("how many employees") == {"number": 0}
    assert agent.invoke("how many employees in dummy_company") == {"number": 0}
    assert agent.invoke(
        "how many employees in dummy_company", context={"sign": True}
    ) == {"number": 120}

    assert agent.invoke("how old dummy_company") == {"number": 0}
    assert agent.invoke(
        "how old dummy_company",
        chat_history=[("user", "age"), ("assistant", "what age")],
    ) == {"number": 7}


def test_emitter_selection(set_default_llm):
    fruit_mentions = []

    class Output(BaseModel):
        number: int = Field(description="number mentioned in the answer")

    def _should_include(input):
        return "apple" in input["message"] and input.get("sign", False)

    @emitter(use_when=_should_include)
    def emit_fruit_mention(fruit: str) -> None:
        """
        When a fruit is mentioned, emit the fruit
        """
        fruit_mentions.append(fruit)

    agent = Agent(
        name="my_service",
        emitters=[emit_fruit_mention],
        output_schema=Output,
    )

    # when context is not provided
    fruit_mentions = []
    agent.invoke("i have one apple and one orange")
    assert fruit_mentions == []

    # when the message mentioned apple
    fruit_mentions = []
    agent.invoke("i have one apple and one orange", context={"sign": True})
    assert fruit_mentions == ["apple", "orange"]

    # when the message doesn't mention apple
    fruit_mentions = []
    agent.invoke("i have one orange")
    assert fruit_mentions == []


def test_vector_search(set_default_llm, tecton_vector_db_test_config):
    from melvin.tecton_gen_ai.factories.vector_db import make_vector_db

    class Output(BaseModel):
        number: int = Field(description="number mentioned in the answer")

    class Filter(BaseModel):
        zip: int = Field(description="the zip code of the item for sale")

    vdb = make_vector_db(tecton_vector_db_test_config, conf=False)
    data = [
        {"zip": 98005, "item_id": 1, "description": "pencil"},
        {"zip": 98005, "item_id": 2, "description": "orange"},
        {"zip": 98005, "item_id": 3, "description": "paper"},
        {"zip": 10065, "item_id": 4, "description": "boat"},
        {"zip": 10065, "item_id": 5, "description": "cheese"},
        {"zip": 10065, "item_id": 6, "description": "apple"},
    ]
    df = pd.DataFrame(data)
    vdb.add_texts(texts=df["description"], metadatas=data, ids=df["item_id"].tolist())
    conf = VectorDBConfig(
        name="search_item",
        vector_db=tecton_vector_db_test_config,
        description="Search items, some result may not be related with the question",
    )
    agent = Agent(name="search", tools=[conf], output_schema=Output)
    res = agent.invoke("search for food, then tell me the number of fruit")
    assert res == {"number": 2}

    conf = VectorDBConfig(
        name="search_item",
        vector_db=tecton_vector_db_test_config,
        filter=Filter,
        description="Search items, some result may not be related with the question",
    )
    agent = Agent(name="search", tools=[conf], output_schema=Output)
    res = agent.invoke(
        "search for food, then tell me the number of fruit", context={"zip": 10065}
    )
    assert res == {"number": 1}
    res = agent.invoke("search for food in 10065, then tell me the number of fruit")
    assert res == {"number": 1}
    # TODO: how to prevent queries overwriting the context var
