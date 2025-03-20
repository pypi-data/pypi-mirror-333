import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Union

from pydantic import BaseModel, Field, create_model

from ..factories.llm import make_llm
from ..factories.vector_db import make_vector_db
from .config_wrapper import to_json_config
from .llm import LLMGenerationConfig

_DEFAULT_SEARCH_TYPE = "mmr"
_DEFAULT_TOP_K = 5


class VectorDB:
    def __init__(
        self, provider: str, *, embedding: Union[str, Dict[str, Any]], **kwargs
    ):
        self.provider = provider
        self.embedding = embedding
        self.kwargs = kwargs
        _embedding = make_llm(embedding, conf=False)
        self.instance = make_vector_db(
            {"provider": provider, "embedding": _embedding, **kwargs}, conf=False
        )

    def __json_config_dict__(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "embedding": self.embedding,
            **self.kwargs,
        }

    def ingest(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ):
        from ..integrations.langchain import langchain_vector_ingest

        return langchain_vector_ingest(
            self.instance, texts=texts, metadatas=metadatas, ids=ids
        )

    def search(
        self,
        query: str,
        top_k: int = _DEFAULT_TOP_K,
        search_type: str = _DEFAULT_SEARCH_TYPE,
        filter: Optional[Dict[str, Any]] = None,
        text_key: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        from ..integrations.langchain import langchain_vector_search

        if filter is not None and len(filter) > 0:
            params = {"filter": filter}
        else:
            params = {}

        res = langchain_vector_search(
            self.instance,
            query,
            top_k=top_k,
            search_type=search_type,
            **params,
        )
        jres = []
        for x in res:
            if text_key is None:
                jres.append(x.metadata)
            else:
                metadata = x.metadata.copy()
                metadata[text_key] = x.page_content
                jres.append(metadata)
        return jres

    def retriever(
        self,
        func: Any = None,
        *,
        name: Optional[str] = None,
        filter: Optional[Type[BaseModel]] = None,
        top_k: int = _DEFAULT_TOP_K,
        search_type: str = _DEFAULT_SEARCH_TYPE,
        text_key: Optional[str] = None,
        description: Optional[str] = None,
        use_when: Optional[Callable] = None,
        generation: Optional[LLMGenerationConfig] = None,
        timeout: Any = None,
        **rtfv_kwargs: Any,
    ):
        from ..tecton_utils.deco import _internal_tool

        def _wrapper(_func: Callable):
            retriever_func_name = _func.__name__
            if set(inspect.getfullargspec(_func).args) != set(
                ["query", "filter", "result"]
            ):
                raise ValueError(
                    "Function must have and only have the following input variables: "
                    "`def func(query: str, filter: dict, result: list[dict[str, Any]])`"
                )
            filter_kwargs = (
                {}
                if filter is None
                else {
                    name: (field.annotation, field)
                    for name, field in filter.model_fields.items()
                }
            )
            input_model = create_model(
                name or _func.__name__,
                query=(
                    str,
                    Field(description="query for searching the vector database"),
                ),
                **filter_kwargs,
                __doc__=description or _func.__doc__,
            )
            conf = to_json_config(self)
            if generation is not None:
                generation.assert_template_args(["query", "context"])
            generation_json = to_json_config(generation) if generation else None

            @_internal_tool(
                name=name or retriever_func_name,
                description=description or _func.__doc__,
                subtype="retriever",
                use_when=use_when,
                timeout=timeout,
                input_schema=input_model,
                **rtfv_kwargs,
            )
            def _inner(**kwargs):
                from ..utils.config_wrapper import from_json_config

                vdb = from_json_config(conf)

                filter = kwargs.copy()
                query = filter.pop("query")

                res = vdb.search(
                    query=query,
                    top_k=top_k,
                    search_type=search_type,
                    filter=filter,
                    text_key=text_key,
                )

                try:  # make tecton compiler embed this function
                    f = _func  # running locally
                except Exception:  # tecton runtime can't really get this function
                    f = globals()[retriever_func_name]  # running on server

                retrieval_res = f(query=query, filter=filter, result=res)
                if generation_json:
                    gen = from_json_config(generation_json)
                    retrieval_res = gen.invoke(
                        {"query": query, "context": retrieval_res}
                    )

                return retrieval_res

            return _inner

        if func is None:
            return lambda _func: _wrapper(_func)
        return _wrapper(func)
