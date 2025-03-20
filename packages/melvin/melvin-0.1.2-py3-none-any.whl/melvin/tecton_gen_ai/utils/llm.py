from string import Formatter
from typing import Any, Dict, Iterable, List, Literal, Optional, Tuple, Type, Union

from pydantic import BaseModel

from ..factories.llm import _build_prompt, invoke_llm, make_llm
from ._serialization import deserialize_pydantic, serialize_pydantic
from .config_utils import Configs

_DEFAULT_LLM_GEN_PROMPT = "{question}"


class LLMGenerationConfig:
    """
    Configuration for an LLM generation. This configuration is json serializable and runnable.

    Args:

        llm: The LLM model to use. If None, the default LLM model will be used.
        prompt: The prompt to use, either a string or a list of tuples of strings (role, text), it can be a template.
            Default is "{question}".
        output_schema: The output schema, can be str, pr a Pydantic model or a string representation of it.
        engine: The engine to use, either "langchain" or "instructor". Default is "langchain".

    Examples:

        ```python
        from tecton_gen_ai.api import LLMGenerationConfig, Configs
        from pydantic import BaseModel, Field

        with Configs(llm="openai/gpt-4o").update_default():
            conf = LLMGenerationConfig()  # Use the default LLM model
            conf.invoke({"question": "1+1=?"})

        conf = LLMGenerationConfig(
            {"model": "openai/gpt-4o", "temperature":0},
            prompt="Solve a math problem 1+1"  # not a template
        )
        conf.invoke()

        class Output(BaseModel):
            answer: int = Field(description="The number as the answer")

        conf = LLMGenerationConfig(
            llm="openai/gpt-4o",
            output_schema=Output,
            prompt=[("system", "Solve a math problem"), ("user", "{question}")]  # template
        )
        conf.invoke({"question": "1+1"})["answer"]  # by default, the pydantic model is converted to a dict
        conf.invoke({"question": "1+1"}, keep_pydantic=True).answer  # keep the Pydantic model as the output
        ```
    """

    def __init__(
        self,
        llm: Union[str, Dict[str, Any], None] = None,
        prompt: Union[str, List[Tuple[str, str]]] = _DEFAULT_LLM_GEN_PROMPT,
        output_schema: Union[Type[BaseModel], Type[str], str] = str,
        engine: Literal["langchain", "instructor"] = "langchain",
    ):
        self.engine = engine
        self.llm = llm if llm is not None else Configs.get_default().llm
        self.prompt = (
            prompt if isinstance(prompt, str) else [[x[0], x[1]] for x in prompt]
        )
        if isinstance(output_schema, str):
            self.output_schema: Union[Type[BaseModel], Type[str]] = (
                deserialize_pydantic(output_schema) if output_schema != "str" else str
            )
        else:
            self.output_schema = output_schema
        if engine == "langchain":
            self._llm_instance = make_llm(self.llm, conf=False)
        elif engine == "instructor":
            if not issubclass(self.output_schema, BaseModel):
                raise NotImplementedError(
                    "Instructor engine only supports Pydantic output schema."
                )

            from .structured_outputs import BatchProcessor

            self._llm_instance = BatchProcessor.make(self.llm, self.output_schema)
        else:
            raise NotImplementedError(f"Unsupported engine {engine}")

    def invoke(
        self,
        template_kwargs: Optional[Dict[str, Any]] = None,
        keep_pydantic: bool = False,
    ) -> Union[str, BaseModel, Dict[str, Any]]:
        """
        Invoke the LLM model.

        Args:

            template_kwargs: The template keyword arguments, defaults to None (assuming the prompt is not a template).
            keep_pydantic: Whether to keep the Pydantic model as the output, or convert it to a dict.
                Default is False.

        Returns:

                The output based on the output schema.
        """
        if self.engine == "langchain":
            res = invoke_llm(
                self._llm_instance,
                prompt=self.prompt,
                output_schema=self.output_schema,
                template_kwargs=template_kwargs,
            )
            if not keep_pydantic and isinstance(res, BaseModel):
                return res.model_dump()
            return res
        elif self.engine == "instructor":
            # TODO: do we want to have a control on cache?
            prompt = _build_prompt(self.prompt, template_kwargs)
            res = self._llm_instance.batch_process(
                [prompt], keep_pydantic=keep_pydantic, enable_cache=False
            )[0]
            return res
        else:
            raise NotImplementedError(f"Unsupported engine {self.engine}")

    def assert_template_args(
        self, expected_args: Iterable[str]
    ) -> "LLMGenerationConfig":
        """
        Assert that the template arguments the prompt matches the given arguments.

        Args:

            expected_args: The expected template arguments.
        """
        args = set(expected_args)
        if isinstance(self.prompt, str):
            names = [
                fn for _, fn, _, _ in Formatter().parse(self.prompt) if fn is not None
            ]
        else:
            names = [
                fn
                for x in self.prompt
                for _, fn, _, _ in Formatter().parse(x[1])
                if fn is not None
            ]
        if args != set(names):
            raise ValueError(f"Expected {args}, got {names}")

    def __json_config_dict__(self) -> Dict[str, Any]:
        return {
            "engine": self.engine,
            "llm": self.llm,
            "prompt": self.prompt,
            "output_schema": (
                "str"
                if self.output_schema is str
                else serialize_pydantic(self.output_schema)
            ),
        }
