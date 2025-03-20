from typing import Any, List

from langchain_community.vectorstores.lancedb import LanceDB
from langchain_core.documents import Document

from .langchain import unified_langchain_vector_search


@unified_langchain_vector_search.register(LanceDB)
def _lancedb_vector_search(
    vdb: LanceDB,
    query: str,
    top_k: int,
    search_type: str = "similarity",
    **params: Any,
) -> List[Document]:
    if "filter" in params:
        expr = " AND ".join([_kv_to_sql(k, v) for k, v in params.pop("filter").items()])
        if expr != "":
            params["filter"] = expr
            params["prefilter"] = params.get("prefilter", True)
    return vdb.search(query, search_type=search_type, k=top_k, **params)


def _kv_to_sql(key: str, value: Any) -> str:
    key = "metadata." + key
    if isinstance(value, str):
        return f"{key} = '{value}'"
    if isinstance(value, bool):
        return f"{key}" if value else f"NOT {key}"
    if isinstance(value, (int, float)):
        return f"{key} = {value}"
    raise ValueError(f"Unsupported value type {type(value)}")
