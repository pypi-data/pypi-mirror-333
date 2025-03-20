from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from tecton import Attribute, DataSource, Entity, batch_feature_view
from tecton.framework.data_source import FilteredSource
from tecton.types import Field, Int64, String

from ..agent.base import VectorDBConfig

from ..utils.config_wrapper import to_json_config
from ._internal import assert_param_not_null_or_get_from_mock, set_serialization
from .convert import to_tecton_type
from .deco import _internal_tool

_DEFAULT_TOP_K = 5
_SEARCH_TOOL_PREFIX = "search_"


def source_as_knowledge(
    source: Union[DataSource, FilteredSource],
    vector_db_config: VectorDBConfig,
    vectorize_column: str,
    feature_start_time: Optional[datetime] = None,
    batch_schedule: timedelta = timedelta(days=1),
    timestamp_field: Optional[str] = None,
    ingestion_kwargs: Optional[Dict[str, Any]] = None,
    serving_kwargs: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Convert a Tecton data source to a knowledge base. This function will
    create an ingestion pipeline to vectorize the data source and store it
    to the designated vector store. It will also create a real-time search
    tool to search the knowledge base.

    Args:

        source: The data source
        vector_db_config: The vector store configuration
        vectorize_column: The column to vectorize
        feature_start_time: The feature start time, defaults to None.
            When None, it requires the source to be a mock source created for testing purpose.
        batch_schedule: The batch schedule, defaults to timedelta(days=1)
        timestamp_field: The timestamp field, defaults to None.
            When None, it requires the source to be a mock source created for testing purpose.
        name: The name of the knowledge base, defaults to None.
            When None, it will use the name of the source.
        description: The description of the knowledge base, defaults to None.
            When None, it will use the description of the source.
        filter: The vector db metadata filter fields, defaults to None.
            The format is a list of tuples (column_name, data_type, description).
        ingestion_kwargs: The ingestion (batch feature view) kwargs, defaults to None.
        serving_kwargs: The serving (real-time feature view) kwargs, defaults to None.

    Returns:

        Tuple: The batch feature view and the search tool

    Notes:

        - This is currently in private preview, metadata filtering is not supported by all vector stores.
        - The knowledge when added to an agent will also be a tool, so it will be used automatically during chat.

    Examples:

        ```python
        from tecton_gen_ai.testing import make_local_source
        from tecton_gen_ai.testing.utils import make_local_vector_db_config

        df = [
            {"zip":"98005", "item_id":1, "description":"pencil"},
            {"zip":"98005", "item_id":2, "description":"car"},
            {"zip":"98005", "item_id":3, "description":"paper"},
            {"zip":"10065", "item_id":4, "description":"boat"},
            {"zip":"10065", "item_id":5, "description":"cheese"},
            {"zip":"10065", "item_id":6, "description":"apple"},
        ]

        src = make_local_source(
            "for_sale",
            df,
            description="Items information",  # required for source_as_knowledge
        )
        vdb_conf = make_local_vector_db_config()  # for testing purpose

        # Create a knowledge base from the source
        from tecton_gen_ai.api import source_as_knowledge

        knowledge = source_as_knowledge(
            src,
            vector_db_config=vdb_conf,
            vectorize_column="description",
            filter = [("zip", str, "the zip code of the item for sale")]
        )

        # Serve the knowledge base
        from tecton_gen_ai.api import Agent

        service = Agent(name="app", knowledge=[knowledge])

        # Test locally

        # search without filter
        print(agent.search("for_sale", query="fruit"))
        # search with filter
        print(agent.search("for_sale", query="fruit", top_k=3, filter={"zip": "27001"}))
        print(agent.search("for_sale", query="fruit", top_k=3, filter={"zip": "10065"}))
        ```
    """

    feature_start_time = assert_param_not_null_or_get_from_mock(
        feature_start_time, source, "start_time"
    )
    timestamp_field = assert_param_not_null_or_get_from_mock(
        timestamp_field, source, "timestamp_field"
    )
    name = vector_db_config.name
    if name is None:
        if isinstance(source, FilteredSource):
            name = source.source.name
        else:
            name = source.name
    if name is None or name == "":
        raise ValueError("name is required")
    description = vector_db_config.description
    if description is None:
        if isinstance(source, FilteredSource):
            description = source.source.description
        else:
            description = source.description
    if description is None or description == "":
        raise ValueError("description is required")

    # sources = [source] if secrets is None else [source, secrets]
    # TODO: Add secrets
    sources = [source]
    filter_entites = [
        Entity(
            name=name,
            join_keys=[Field(name=name, dtype=to_tecton_type(field.annotation))],
            description=field.description,
        )
        for name, field in vector_db_config.filter_model.model_fields.items()
    ]
    vconf = to_json_config(vector_db_config)
    ikwargs = ingestion_kwargs or {}
    batch_deco = batch_feature_view(
        name=name + "_batch",
        sources=sources,
        entities=[
            Entity(
                name=name + "_" + vectorize_column,
                join_keys=[Field(vectorize_column, String)],
            )
        ]
        + filter_entites,
        mode="pandas",
        offline=True,
        online=False,
        features=[
            Attribute(name="dummy", dtype=Int64),
        ],
        feature_start_time=feature_start_time,
        batch_schedule=batch_schedule,
        timestamp_field=timestamp_field,
        description=description,
        **ikwargs,
    )

    def ingest(bs, *args):
        from langchain_core.vectorstores import VectorStore

        from ..utils.config_wrapper import from_json_config
        from ..utils.hashing import to_uuid
        from ..utils.pandas_utils import to_records

        if len(bs) == 0:
            return bs.assign(dummy=0)

        vs: VectorStore = from_json_config(vconf).make_instance()
        texts = bs[vectorize_column].tolist()
        ids = [to_uuid(x) for x in texts]
        metadatas = to_records(bs, timestamp_to="str")
        vs.add_texts(texts=texts, metadatas=metadatas, ids=ids)

        return bs.head(1).assign(dummy=1)

    with set_serialization():
        # if secrets is None:
        if True:

            def ingest_0(bs):
                return ingest(bs)

            batch_fv = batch_deco(ingest_0)
        else:

            def ingest_1(bs, secrets):
                return ingest(bs, secrets)

            batch_fv = batch_deco(ingest_1)

    fdict_desc = "\n".join(
        f"{name}({field.annotation}): {field.description}"
        for name, field in vector_db_config.filter_model.model_fields.items()
    )

    desc = f"""Search the knowledge base of {name}: {description}

Args:
query (str): the search query string
top_k (int): the top k results to return, default is {_DEFAULT_TOP_K}
filter (str): a json dictionary of filters name and values to apply to the search, default is None

Returns:

List[Dict[str, Any]]: search results

Available filter names:

{fdict_desc}
"""
    skwargs = serving_kwargs or {}

    @_internal_tool(
        name=_SEARCH_TOOL_PREFIX + name,
        description=desc,
        subtype="search",
        source_names=[name],
        **skwargs,
    )
    def search(query: str, top_k: int = 5, filter: str = "") -> "List[Dict[str, Any]]":
        """dummy"""

        import json

        from ..agent.base import _get_vdb_instance
        from ..integrations.langchain import langchain_vector_search

        _, vs, filter_keys = _get_vdb_instance(vconf)

        if len(filter_keys) == 0:
            params = {}
        else:
            ft = {k: v for k, v in json.loads(filter).items() if k in filter_keys}
            params = {"filter": ft}

        res = langchain_vector_search(vs, query, top_k, **params)

        jres = []
        for x in res:
            jres.append(x.metadata)
        return jres

    return batch_fv, search
