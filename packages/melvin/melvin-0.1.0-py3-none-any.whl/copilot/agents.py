import os

from constants import FILE_DIR
from prompts import sys_prompt
from tecton_utils import APIGraphBuilder
from tools import (
    create_feature_repo,
    find_tecton_feature_repositories,
    fix_syntax_issues,
    generate_flowchart_representation,
    get_feature_service_configuration,
    get_feature_view_code,
    get_feature_view_configuration,
    get_source_code,
    get_source_code_lineno,
    list_data_sources,
    list_entities,
    list_feature_services,
    list_feature_views,
    list_transformations,
    list_workspaces,
    move_to_folder,
    query_cost_data,
    save_modified_code,
    tecton_cli_execute,
    tecton_cli_help,
    validate_with_tecton_plan,
)
from utils import _get_source_code, _log
from chart_agent import _make_chart_agent
from src.tecton_gen_ai.api import Agent, RuntimeVar, VectorDB, get_agent
from diagnostics_agent import _make_agent as _make_diagnostics_agent
from editors.feature_view_editor_agent import make_fv_editor_agent

def _build_api_retriever():
    import shutil

    builder = APIGraphBuilder()
    vpath = "/tmp/tecton_api.db"
    shutil.rmtree(vpath, ignore_errors=True)
    vdb = VectorDB("lancedb", embedding="openai/text-embedding-3-small", uri=vpath)
    vdb.ingest(
        texts=[name for name in builder.graph.keys()],
        metadatas=[dict(ref=name) for name in builder.graph.keys()],
    )

    @vdb.retriever(name="tecton_api_reference", top_k=5)
    def tecton_api_reference_retriever(query, filter, result) -> str:
        """
        The retriever that helps users find relevant API reference of Tecton.
        It is always helpful to query the API reference before modifying code.

        The input query should be a list of names of the function or class in Tecton.
        They should be separated by comma.
        """

        names = list(set(x["ref"] for x in result).union(["Aggregate", "Entity"]))
        _log(f":mag: Querying API reference: {query}")
        _log(f"Constructing API specs using: {names}")
        code = builder.build_code(names)
        print(code)
        return code

    return tecton_api_reference_retriever


def _build_example_retriever():
    import shutil

    import pandas as pd

    examples = pd.read_parquet(
        os.path.join(FILE_DIR, "data", "examples.parquet")
    ).to_dict(orient="records")

    vpath = "/tmp/tecton_examples.db"
    shutil.rmtree(vpath, ignore_errors=True)
    vdb = VectorDB("lancedb", embedding="openai/text-embedding-3-small", uri=vpath)
    vdb.ingest(
        texts=[obj["text"] for obj in examples],
        metadatas=[dict(code=obj["code"], title=obj["text"]) for obj in examples],
    )

    @vdb.retriever(name="tecton_examples", top_k=5)
    def tecton_examples_retriever(query, filter, result) -> str:
        """
        The retriever that helps users find relevant Tecton code examples.
        It is always helpful to query the examples retriever before modifying code.

        Input query examples:

        "examples of a Entity"
        "examples of a KinesisConfig"
        "examples of a KafkaConfig"
        "examples of a batch feature view"
        "examples of a count distinct aggregation feature view"
        "examples of a percentile aggregation feature view"
        "examples of a stream feature view"
        "examples of an aggregation stream feature view"
        "examples of a realtime feature view"
        "examples of a realtime feature view that transforms data from another feature view"
        "examples of a fraud feature"
        "examples of a recsys case"
        "examples of a test"

        The output will be a collection of python code examples.
        """
        code = set(x["code"] for x in result)
        prefix = "==== Python Coce Example ====\n\n"
        res = "\n\n".join([prefix + c for c in code])
        _log(":mag: Querying Tecton Examples: " + query)
        return res

    return tecton_examples_retriever


def _build_syntax_agent():
    return Agent(
        "syntax_agent",
        description="A syntax fixer to iteratively fix syntax issues in the feature definition code",
        prompt="""You are going to use get_source_code and fix_syntax_issues
in a loop to fix the python syntax issues of the feature definition code.

Try fix for at most 5 times, if you still have syntax issues, you should
respond with the error message and ask for help.""",
        tools=[get_source_code_lineno, fix_syntax_issues],
        llm={
            "model": "openai/o3-mini-2025-01-31",
            "max_tokens": 2048,
        },
    )


def _build_validation_agent():
    def _prompt() -> str:
        gotchas_file = os.path.join(FILE_DIR, "data", "gotchas.md")
        with open(gotchas_file) as f:
            gotchas = f.read()
        return f"""
You are going to validate the feature code, there should be two steps:

1. first, validate the code using gotchas rules. Both the gotchas rules and the code are provided below.
2. second, if you get gotcha violations validate that the gotcha violation is actually correct. If it doesn't seem correct, IGNORE the gotcha validation error.
3. if you don't find any valid violated gotcha rules you absolutely must call validate_with_tecton_plan to validate the code with the command `tecton plan`. ONLY skip this step if you don't find violated gotcha rules


The output will be one of the following:
- Success message if both validations pass.
- Error message if either of the validations fail.
- Warning message if the code change has minor issues.

The result message should be under 500 words. If you know how to fix the issue, provide a recommendation.

=== Gotchas ===

{gotchas}


=== Source Code ===

```python
{_get_source_code()}
```
"""

    agent = Agent(
        "validate_code_change",
        description="""A validator to validate the feature definition code using both `tecton plan` and other gotcha rules

The input query should be empty because it will not be used.

The output will be one of the following:
- Success message if the code change is valid
- Error message if the code change has critical issues
- Warning message if the code change has minor issues
""",
        prompt=_prompt,
        tools=[validate_with_tecton_plan],
        llm={
            "model": "anthropic/claude-3-5-sonnet-20241022",
            "temperature": 0,
            "max_tokens": 1024,
        },
    )
    return agent


def build_agent():
    tecdoc = get_agent(
        "tecbot",
        workspace="tecdoc",
        url="https://dev-gen-ai.tecton.ai",
        api_key=RuntimeVar(name="TECTON_API_KEY"),
    )
    api_retriever = _build_api_retriever()
    examples = _build_example_retriever()
    doc_retriever = tecdoc.export_tools(names=["search_tecton_v11"])[0]
    tools = [
        doc_retriever,
        create_feature_repo,
        move_to_folder,
        get_source_code,
        save_modified_code,
        validate_with_tecton_plan,
        # validator,
        # syntax_agent,
        api_retriever,
        examples,
        tecton_cli_help,
        tecton_cli_execute,
        find_tecton_feature_repositories,
        list_workspaces,
        list_feature_services,
        list_feature_views,
        list_transformations,
        get_feature_view_code,
        get_feature_view_configuration,
        get_feature_service_configuration,
        list_data_sources,
        list_entities,
        generate_flowchart_representation,
        query_cost_data,
        # generate_graph,
        _make_chart_agent(),
        _make_diagnostics_agent(doc_retriever),
        make_fv_editor_agent()
    ]

    agent = Agent("tecbot", prompt=sys_prompt, tools=tools)
    return agent
