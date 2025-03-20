from typing import Any, Union

import instructor
from pydantic import BaseModel

from ..utils.runtime import RuntimeVar
from ..utils.structured_outputs import BatchProcessor, T_OutputType


class InstructorVendorProcessor(BatchProcessor):
    def __init__(
        self, model: dict[str, Any], schema: Union[type[T_OutputType], dict[str, Any]]
    ):
        super().__init__(model=model, schema=schema)
        model_cp = model.copy()
        self.provider, self.provider_model = model_cp.pop("model").split("/", 1)
        if "api_key" in model_cp and isinstance(model_cp["api_key"], RuntimeVar):
            model_cp["api_key"] = model_cp["api_key"].get()
        client_kwargs, self.inference_kwargs = self.separate_kwargs(model_cp)
        self.aclient = self._make_aclient(**client_kwargs)

    def separate_kwargs(
        self, kwargs: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        d1, d2 = {}, {}
        inf_args = ["temperature", "max_tokens"]
        for k, v in kwargs.items():
            if k in inf_args:
                d2[k] = v
            else:
                d1[k] = v
        return d1, d2

    def _make_aclient(self, **kwargs: Any) -> instructor.AsyncInstructor:
        raise NotImplementedError

    async def aprocess(
        self, prompt: Union[str, list[tuple[str, str]]], keep_pydantic: bool
    ) -> Union[dict[str, Any], BaseModel]:
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        else:
            messages = [{"role": item[0], "content": item[1]} for item in prompt]
        response = await self.aclient.chat.completions.create(
            model=self.provider_model,
            messages=messages,
            response_model=self.schema_model,
            **self.inference_kwargs,
        )
        return response if keep_pydantic else response.model_dump()

    def get_tecton_fields(self, as_attributes: bool = False) -> list:
        from tecton import Attribute
        from tecton.types import Field

        from ..tecton_utils.convert import to_tecton_type

        fields = [
            Field(name=name, dtype=to_tecton_type(v.annotation))
            for name, v in self.schema_model.model_fields.items()
        ]
        if as_attributes:
            return [Attribute(name=field.name, dtype=field.dtype) for field in fields]
        return fields


@BatchProcessor.register(lambda model: model["model"].startswith("openai/"))
class InstructorOpenAIProcessor(InstructorVendorProcessor):
    def _make_aclient(self, **kwargs: Any) -> instructor.AsyncInstructor:
        from openai import AsyncOpenAI

        return instructor.from_openai(AsyncOpenAI(**kwargs))


@BatchProcessor.register(lambda model: model["model"].startswith("anthropic/"))
class InstructorAnthropicProcessor(InstructorVendorProcessor):
    def _make_aclient(self, **kwargs: Any) -> instructor.AsyncInstructor:
        from anthropic import AsyncAnthropic

        return instructor.from_anthropic(AsyncAnthropic(**kwargs))
