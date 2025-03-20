import asyncio
from typing import Any, Callable, TypeVar, Union

from pydantic import BaseModel

from . import _cache, _coroutine
from .hashing import to_uuid
from ._serialization import to_openai_function, openai_function_to_pydantic

_DEFAULT_LOCAL_CONCURRENCY = 5
T_OutputType = TypeVar("T_OutputType", bound=BaseModel)


def batch_generate_dicts(
    model: Union[str, dict[str, Any]],
    texts: list[str],
    schema: Union[type[T_OutputType], dict[str, Any]],
    concurrency: int = _DEFAULT_LOCAL_CONCURRENCY,
    enable_cache: bool = True,
) -> list[dict[str, Any]]:
    """
    Generate structured outputs for a list of texts

    Args:

        model: The model to use for generation
        texts: The list of texts to generate structured outputs for
        schema: The schema of the structured outputs
        concurrency: The number of concurrent requests to make, defaults to 5
        enable_cache: Whether to enable caching, defaults to True

    Returns:

        list[dict[str, Any]]: The structured outputs (python dicts)

    Examples:

        ```python
        from tecton_gen_ai.utils.structured_outputs import batch_generate_dicts
        from pydantic import BaseModel, Field

        model = "openai/gpt-4o"
        texts = ["I am 4", "She is 5"]

        class Age(BaseModel):
            age: int = Field(description="The age")

        outputs = batch_generate_dicts(model, texts, Age)
        ```
    """
    processor = BatchProcessor.make(model=model, schema=schema)
    return processor.batch_process(
        texts,
        concurrency=concurrency,
        keep_pydantic=False,
        enable_cache=enable_cache,
    )


def batch_generate(
    model: Union[str, dict[str, Any]],
    texts: list[str],
    schema: type[T_OutputType],
    concurrency: int = _DEFAULT_LOCAL_CONCURRENCY,
    enable_cache: bool = True,
) -> list[T_OutputType]:
    """
    Generate structured outputs for a list of texts

    Args:

        model: The model to use for generation
        texts: The list of texts to generate structured outputs for
        schema: The pydantic schema of the structured outputs
        concurrency: The number of concurrent requests to make, defaults to 5
        enable_cache: Whether to enable caching, defaults to True

    Returns:

        list[T_OutputType]: The structured outputs

    Examples:

        ```python
        from tecton_gen_ai.utils.structured_outputs import batch_generate

        model = "openai/gpt-4o"
        texts = ["I am 4", "She is 5"]

        class Age(BaseModel):
            age: int = Field(description="The age")

        outputs = batch_generate(model, texts, Age)
        ```
    """
    return [
        schema.model_validate(x)
        for x in batch_generate_dicts(
            model=model,
            texts=texts,
            schema=schema,
            concurrency=concurrency,
            enable_cache=enable_cache,
        )
    ]


class BatchProcessor:
    _PROCESSORS: list[
        tuple[Callable[[dict[str, Any]], bool], type["BatchProcessor"]]
    ] = []

    @staticmethod
    def register(fn: Callable[[dict[str, Any]], bool]):
        def _register(cls):
            BatchProcessor._PROCESSORS.append((fn, cls))
            return cls

        return _register

    @staticmethod
    def make(
        model: Union[str, dict[str, Any]],
        schema: Union[type[T_OutputType], dict[str, Any]],
    ) -> "BatchProcessor":
        if isinstance(model, str):
            model = {"model": model}
        _cls = BatchProcessor._get_cls(model)
        return _cls(model, schema)

    @staticmethod
    def _get_cls(model: dict[str, Any]) -> type["BatchProcessor"]:
        _load_dependencies()
        for fn, cls in BatchProcessor._PROCESSORS:
            if fn(model):
                return cls
        raise ValueError(f"Model {model} not supported")

    def __init__(
        self, model: dict[str, Any], schema: Union[type[T_OutputType], dict[str, Any]]
    ):
        self.model = model
        if isinstance(schema, dict):
            self.schema_model = openai_function_to_pydantic(schema)
            self.schema_dict = schema
        else:
            self.schema_model = schema
            self.schema_dict = to_openai_function(schema)

    def __json_config_dict__(self) -> dict[str, Any]:
        return {"model": self.model, "schema": self.schema_dict}

    def get_tecton_fields(self, as_attributes: bool = False) -> list:
        raise NotImplementedError

    async def aprocess(
        self, prompt: Union[str, list[tuple[str, str]]], keep_pydantic: bool
    ) -> Union[dict[str, Any], BaseModel]:
        raise NotImplementedError

    def batch_process(
        self,
        prompts: list[Union[str, list[tuple[str, str]]]],
        concurrency: int = _DEFAULT_LOCAL_CONCURRENCY,
        keep_pydantic: bool = False,
        enable_cache: bool = True,
    ) -> list[Union[dict[str, Any], BaseModel]]:
        # NOTE: default size limit of 1GB (https://grantjenks.com/docs/diskcache/api.html#constants)
        cache = _cache.get_cache("tecton-gen-ai", "structured_outputs")
        if enable_cache:
            base_key = to_uuid((self.schema_dict, self.model, keep_pydantic))
        else:
            base_key = ""

        async def fn(sem, prompt: Any) -> T_OutputType:
            async with sem:
                if not enable_cache:
                    return await self.aprocess(prompt, keep_pydantic=keep_pydantic)
                key = to_uuid((prompt, base_key))
                if (cached := await cache.aget(key)) is not None:
                    # Deserialize from JSON based on the return type
                    return cached

                result = await self.aprocess(prompt, keep_pydantic=keep_pydantic)
                await cache.aset(key, result)
                return result

        async def _gather():
            sem = asyncio.Semaphore(concurrency)
            _jobs = [fn(sem, prompt) for prompt in prompts]
            return await asyncio.gather(*_jobs)

        return _coroutine.run(_gather())


def _load_dependencies():
    try:
        from ..integrations import instructor  # noqa
    except ImportError:
        pass
