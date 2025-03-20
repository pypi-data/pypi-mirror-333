import inspect
import json
import logging
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from functools import lru_cache, singledispatch
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import pandas as pd
from pydantic import BaseModel, Field, create_model

from ..factories.llm import _load_dependencies, make_llm
from ..factories.vector_db import make_vector_db
from ..utils._dev_utils import is_dev_mode
from ..utils._resource_alternatives import code_to_func
from ..utils._serialization import (
    openai_function_to_pydantic,
    openai_properties_to_pydantic,
    to_openai_function,
    to_openai_properties,
)
from ..utils.config_utils import Configs
from ..utils.config_wrapper import (
    _str_to_type,
    _type_to_str,
    from_json_config,
    to_json_config,
)
from ..utils.log import NOOP_LOGGER
from ..utils.runtime import RuntimeVar

_DEFAULT_TOP_K = 5
_SEARCH_TOOL_PREFIX = "search_"


class AgentInputModel(BaseModel):
    query: str = Field(description="The query to the agent")
    chat_history: List[Tuple[str, str]] = Field(
        description="The chat history in a list of role message pairs.", default=[]
    )


@singledispatch
def invoke_agent(
    llm,
    client: "AgentBase",
    input: Dict[str, Any],
    output_schema: Union[Type[str], Type[BaseModel]] = str,
    **kwargs: Any,
) -> Any:
    """
    Invoke an agent. This is not for users to call directly.

    Args:

        llm: The language model object in a specific framework (e.g. LangChain)
        client: The agent client
        message: The message (question)
        chat_history: The chat history
        output_schema: The output schema, can be `str` or a pydantic model, defaults to `str`
        **kwargs: Additional arguments for the agent

    Returns:

        Any: The response in the format of `output_schema`
    """
    raise NotImplementedError(f"Unsupported type {type(llm)}")  # pragma: no cover


@singledispatch
def invoke_emitters(
    llm,
    client: "AgentBase",
    message: str,
    chat_history: Any = None,
    **kwargs: Any,
) -> None:
    """
    Invoke an agent's emitters. This is not for users to call directly.

    Args:

        llm: The language model object in a specific framework (e.g. LangChain)
        client: The agent client
        message: The message (question)
        chat_history: The chat history
        **kwargs: Additional arguments for the agent
    """
    raise NotImplementedError(f"Unsupported type {type(llm)}")  # pragma: no cover


@singledispatch
def make_agent(
    llm,
    client: "AgentBase",
    output_schema: Union[Type[str], Type[BaseModel]] = str,
    initial_message: Optional[str] = None,
    initial_chat_history: Optional[List[Tuple[str, str]]] = None,
    **kwargs: Any,
) -> Any:
    """
    Make an agent. This is not for users to call directly.

    Args:

        llm: The language model object in a specific framework (e.g. LangChain)
        client: The agent client
        output_schema: The output schema, can be `str` or a pydantic model, defaults to `str`
        initial_message: The initial message, defaults to None
        initial_chat_history: The initial chat history, defaults to None
        **kwargs: Additional arguments for creating the agent

    Returns:

        Any: The agent object
    """
    raise NotImplementedError(f"Unsupported type {type(llm)}")  # pragma: no cover


class AgentBase:
    """
    The Tecton Agent. This class should not be used directly. Use `Agent` if
    you want to declare the agent or develop the agent locally. Use `get_agent`
    if you want to connect to a deployed agent.
    """

    def __init__(self, name: str):
        self.name = name
        self._current_context = ContextVar("current_context", default=None)
        self._current_logger = ContextVar("current_logger", default=NOOP_LOGGER)
        self.default_system_prompt: Optional[str] = None

    @property
    def logger(self) -> logging.Logger:
        """
        Get the current logger of the client. The logger can be controlled
        using the context manager `set_logger`.

        Returns:

            logging.Logger: The logger
        """
        return self._current_logger.get()

    @contextmanager
    def set_logger(self, logger: Optional[logging.Logger]):
        """
        Set the logger for the client. This is a context manager.

        Args:

            logger: The new logger, or None to use the no-op logger

        Example:

            ```python
            with client.set_logger(logger):
                # do something
            ```
        """
        _logger = logger or NOOP_LOGGER
        token = self._current_logger.set(_logger)
        try:
            yield
        finally:
            self._current_logger.reset(token)

    @contextmanager
    def set_context(self, context: Optional[Dict[str, Any]]):
        """
        Set the context for the client. This is a context manager. The context
        will be used as the arguments for the prompts, tools and knowledge.

        Args:

            context: The new context, or None to clear the context

        Example:

            ```python
            conext = {"a":1, "b":2}
            new_args = {"b":3, "c":4}
            with client.set_context(context):
                # the context will be used as the arguments of my_tool
                # new_args will override the context
                # the final arguments for my_tool will be {"a":1, "b":3, "c":4}
                client.invoke_tool("my_tool", new_args)
            ```

        """
        self.logger.debug("Setting context to %s", context)
        token = self._current_context.set(context or {})
        try:
            yield
        finally:
            self._current_context.reset(token)

    @property
    def metastore(self) -> Dict[str, Any]:
        """
        Get the metastore of the client. The metastore contains the metadata of
        the tools, prompts, knowledge and other resources. This function should
        not be used directly.
        """
        raise NotImplementedError

    @property
    def description(self) -> str:
        """
        The description of the agent. This is used for the system prompt.
        """
        return self.metastore.get("description", "").strip()

    @property
    def input_schema(self) -> Type[AgentInputModel]:
        """
        Get the input schema of the agent. This is used for the entrypoint.

        The input schema should be a pydantic model inheriting from `AgentInputModel`.
        """
        raise NotImplementedError

    @property
    def output_schema(self) -> Union[Type[str], Type[BaseModel]]:
        """
        Get the output schema of the agent. This is used for the entrypoint.

        The output schema should be a pydantic model or `str` type.
        """
        raise NotImplementedError

    def select_metastore(
        self,
        type: str,
        input: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Select items from the metastore using the `use_when` (if defined) which
        is based on the message and chat history.

        Args:

            type: The type of the items in the metastore, can be tools or emitters
            input: The python dict of the input of the agent, defined by `AgentInputModel`

        Returns:

            Dict[str, Any]: The selected items
        """
        if type not in ["tools", "emitters"]:
            raise ValueError(f"Unsupported metastore type {type}")
        items = self.metastore.get(type, {})
        res = {}
        for k, v in items.items():
            cond = v.get("use_when")
            if cond:
                func = code_to_func(cond)
                if func(input):
                    res[k] = v
            else:
                res[k] = v
        return res

    @property
    def entrypoint_timeout_sec(self) -> float:
        """
        Get the request timeout in seconds for the entrypoint. This is used for the entrypoint
        of the agent.
        """
        return self.metastore["entrypoint_timeout_sec"]

    def make_local_agent(
        self,
        llm: Any,
        output_schema: Union[Type[str], Type[BaseModel]] = str,
        **kwargs: Any,
    ) -> Any:
        """
        Make an agent for a specific LLM framework (Langchain or LLamaIndex). This
        agent will run the workflow locally using the local `llm`, but its prompt
        and tools may be from the service.

        Args:

            llm: The language model object in a specific framework (e.g. LangChain or LLamaIndex).
            output_schema: The output schema, can be `str` or a pydantic model, defaults to `str`
            **kwargs: Additional arguments for creating the agent

        Returns:

            Any: The agent object

        Example:

            ```python
            from tecton_gen_ai.api import Agent
            from tecton_gen_ai.utils.tecton_utils import make_request_source

            def sys_prompt(age:int):
                return f"You are talking to a {age} years old person."

            service = Agent(name="app", prompt=sys_prompt)

            agent = service.make_local_agent({"model":"openai/gpt-4o", "temperature":0})
            with client.set_context({"age": 3}):
                print(agent.invoke({"input":"why sky is blue"}))
            with client.set_context({"age": 30}):
                print(agent.invoke({"input":"why sky is blue"}))
            ```
        """
        llm = make_llm(llm, conf=False)
        if llm is None:
            raise ValueError("No LLM provided")
        _load_dependencies()
        return make_agent(
            llm,
            self,
            output_schema=output_schema,
            **kwargs,
        )

    def invoke(
        self,
        message: str,
        chat_history: Optional[List[Tuple[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        timeout: Any = None,
    ) -> Union[str, Dict[str, Any]]:
        """
        Invoke an agent. When developing the agent locally, this
        will use the LLM and output schema defined by `Agent`. When connecting to
        a deployed agent, this will use the agent's entrypoint.

        Args:

            message: The message (question)
            chat_history: The chat history in the format of [(role, message)], defaults to None
            context: The context variables to run the agent, this will override the context set by `set_context`
            timeout: The timeout expression, if None, it will use the entrypoint's timeout setting

        Returns:

            Union[str, Dict[str, Any]]: The response which can be a string or a python dict.

        Example:

            ```python
            from tecton_gen_ai.api import Agent

            def sys_prompt(age:int):
                return f"You are talking to a {age} years old person."

            agent = Agent(name="app", prompt=sys_prompt, llm="openai/gpt-4o", entrypoint_timeout=10)

            with agent.set_context({"age": 3}):
                print(agent.invoke("why sky is blue"))

            print(agent.invoke("why sky is blue", context={"age": 30}))

            # With structured output
            from pydantic import BaseModel, Field

            class Response(BaseModel):
                answer: str = Field(description="The answer to the question")

            agent = Agent(
                name="app",
                prompt=sys_prompt,
                llm="openai/gpt-4o",
                output_schema=Response
            )

            # The response will be a python dict {"answer": "..."}
            # It also overwrites the entrypoint's timeout
            agent.invoke("why sky is blue", context={"age": 30}, timeout="10s")
            ```

        """
        if timeout is None:
            timeout_sec = self.entrypoint_timeout_sec
        else:
            timeout_sec = pd.to_timedelta(timeout).total_seconds()
        return self._invoke_entrypoint(
            message=message,
            chat_history=chat_history,
            context=context,
            timeout_sec=timeout_sec,
        )

    def invoke_locally(
        self,
        message: str,
        local_llm: Any,
        chat_history: Optional[List[Tuple[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        output_schema: Union[Type[str], Type[BaseModel]] = str,
        **kwargs: Any,
    ) -> Union[str, Dict[str, Any]]:
        """
        Invoke an agent for a specific LLM framework. Compared to `make_local_agent`, this
        function is simpler, but it is less flexible than getting the agent object of the
        specific framework to invoke.

        Args:

            message: The message (question)
            local_llm: The language model object in a specific framework (e.g. LangChain or LLamaIndex).
                It will invoke the agent locally using the local LLM with the remote prompt and tools.
            chat_history: The chat history in the format of [(role, message)], defaults to None
            context: The context variables to run the agent, this will override the context set by `set_context`
            output_schema: The output schema, can be `str` or a pydantic model, defaults to `str`
            **kwargs: Additional arguments for invoking the agent

        Returns:

            The response, it is a string if `output_schema` is `str`, otherwise it is a python dict
            following the pydantic model.

        Example:

            ```python
            from tecton_gen_ai.api import Agent

            def sys_prompt(age:int):
                return f"You are talking to a {age} years old person."

            agent = Agent(name="app", prompt=sys_prompt)

            with agent.set_context({"age": 3}):
                print(agent.invoke_locally("why sky is blue", llm="openai/gpt-4o"))

            # With structured output
            from pydantic import BaseModel, Field

            class Response(BaseModel):
                answer: str = Field(description="The answer to the question")

            # The response will be a python dict {"answer": "..."}
            agent.invoke_locally("why sky is blue", llm="openai/gpt-4o", output_schema=Response)
            ```

        """
        _load_dependencies()
        local_llm = make_llm(local_llm, conf=False)
        input = context.copy() if context is not None else {}
        input["message"] = message
        input["chat_history"] = chat_history
        self._emit(
            local_llm=local_llm,
            input=input,
            context=context,
            **kwargs,
        )
        func = lambda: invoke_agent(  # noqa
            local_llm,
            self,
            input=input,
            output_schema=output_schema,
            **kwargs,
        )

        if context is not None:
            with self.set_context(context):
                res = func()
        else:
            res = func()
        self.logger.debug("Result of invoking agent: %s", res)

        return res

    def _emit(
        self,
        local_llm: Any,
        input: Dict[str, Any],
        context: Any,
        **kwargs,
    ):
        if len(self.metastore.get("emitters", {})) > 0:
            try:
                efunc = lambda: invoke_emitters(  # noqa
                    local_llm, self, input=input, **kwargs
                )
                if context is not None:
                    with self.set_context(context):
                        efunc()
                else:
                    efunc()
            except Exception as e:
                self.logger.error("Error in emitting", exc_info=e)

    def _invoke_entrypoint(
        self,
        message: str,
        timeout_sec: float,
        chat_history: Optional[List[Tuple[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        agent_name: Optional[str] = None,
    ) -> Union[str, Dict[str, Any]]:
        raise NotImplementedError

    def invoke_tool(self, name: str, kwargs: Optional[Dict[str, Any]] = None) -> Any:
        """
        Invoke a tool in the service.

        Args:

            name: The name of the tool
            kwargs: The arguments for the tool

        Returns:

            Any: The result of the tool

        Example:

            ```python
            from tecton_gen_ai.api import Agent

            def get_price_of_fruit(fruit:str) -> int:
                '''
                Get the price of a fruit

                Args:

                    fruit: The name of the fruit

                Returns:

                    int: The price of the fruit
                '''
                return 10 if fruit == "apple" else 5

            agent = Agent(name="app", tools=[get_price_of_fruit])

            print(atent.invoke_tool("get_price_of_fruit", {"fruit":"apple"}))
            ```
        """
        kwargs = kwargs or {}
        self.logger.debug("Invoking tool %s with %s", name, kwargs)
        meta = self.metastore["tools"][name]
        tool_cls = _str_to_type(meta["subtype_path"])
        return tool_cls.invoke(self, name, kwargs)

    def invoke_feature_view(
        self, name: str, kwargs: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Invoke a feature view in the service.

        Args:

            name: The name of the feature view
            kwargs: The arguments for the feature view, the keys should match the entity
                schema of the feature view.

        Returns:

            Any: The result of the feature view

        Example:

            ```python
            from tecton_gen_ai.testing import make_local_feature_view, set_dev_mode

            set_dev_mode()

            bfv = make_local_feature_view(
                "user_age",
                {"user_id": 1, "age": 30},
                ["user_id"],
                description="The age of a user",
            )

            from tecton_gen_ai.api import Agent
            agent = Agent(name="app", tools=[bfv])

            print(agent.invoke_feature_view("user_age", {"user_id":1}))
            ```

        """
        kwargs = kwargs or {}
        self.logger.debug("Invoking feature view as tool %s with %s", name, kwargs)
        tool_name = "fv_tool_" + name
        tool = self.metastore["tools"][name]

        ctx = self._get_context()
        ctx.update(kwargs)
        key_map = {k: ctx[k] for k in tool["args"]}

        return self._get_feature_value(
            tool_name, key_map, {}, feature_type="tool", timeout_sec=tool["timeout_sec"]
        )

    def invoke_emitter(self, name: str, kwargs: Optional[Dict[str, Any]] = None) -> Any:
        """
        Invoke an emitter in the service.

        Args:

            name: The name of the emitter
            kwargs: The arguments for the emitter

        Returns:

            Any: The result of the emitter

        Example:

            ```python
            from tecton_gen_ai.api import Agent
            from logging import getLogger

            def emit_fruit(fruit:str) -> None:
                '''
                log them fruit mentioned

                Args:

                    fruit: The name of the fruit
                '''
                logger = getLogger("fruit")
                logger.info(f"The price of {fruit} is 10")

            agent = Agent(name="app", emitters=[emit_fruit])

            print(atent.invoke_emitter("emit_fruit", {"fruit":"apple"}))
            ```
        """
        kwargs = kwargs or {}
        self.logger.debug("Invoking emitter %s with %s", name, kwargs)
        meta = self.metastore.get("emitters", {})[name]
        ctx = self._get_context()
        ctx.update(kwargs)
        entity_args = meta.get("entity_args", [])
        llm_args = meta.get("llm_args", [])
        return self._invoke(
            name,
            entity_args,
            llm_args,
            ctx,
            feature_type="emitter",
            timeout_sec=meta["timeout_sec"],
        )

    def invoke_prompt(self, kwargs: Optional[Dict[str, Any]] = None) -> str:
        """
        Invoke the prompt of the agent.

        Args:

            kwargs: The arguments for the prompt, it overrides the context set by `set_context`

        Returns:

            str: The result of the prompt

        Example:

            ```python
            from tecton_gen_ai.api import Agent

            def sys_prompt(age:int):
                return f"You are talking to a {age} years old person."

            agent = Agent(name="app", prompt=sys_prompt)

            print(agent.invoke_prompt({"age": 3}))
            ```
        """
        context = self._get_context()
        context.update(kwargs or {})
        metadata = self._get_sys_prompt()
        if metadata is None:
            return ""
        name = metadata["name"]
        match = all(key in context for key in metadata.get("keys", [])) and all(
            key in context for key in metadata.get("args", [])
        )
        if not match:
            raise ValueError(
                f"Context does not have all required keys for system prompt {name}."
            )
        entity_args = metadata.get("entity_args", [])
        llm_args = metadata.get("llm_args", [])
        self.logger.debug(
            "Invoking prompt %s with %s",
            name,
            context,
            extra={"flow_event": metadata},
        )
        return self._invoke(
            name,
            entity_args,
            llm_args,
            context,
            feature_type="prompt",
            timeout_sec=metadata["timeout_sec"],
        )

    def invoke_system_prompt(self, kwargs: Optional[Dict[str, Any]] = None) -> str:
        """
        Combine agent description, context variables and the prompt of the agent.

        Args:

            kwargs: The arguments for the prompt, it overrides the context set by `set_context`

        Returns:

            str: The result of the prompt

        Example:

            ```python
            from tecton_gen_ai.api import Agent

            def sys_prompt(age:int):
                return f"You are talking to a {age} years old person."

            agent = Agent(name="app", prompt=sys_prompt)

            print(agent.invoke_system_prompt({"age": 3}))
            ```
        """
        lines: List[str] = []
        context = self._get_context()
        context.update(kwargs or {})
        description = self.metastore.get("description", "").strip()
        if description != "":
            lines.append(f"Agent Description: {description}")
        if len(context) > 0:
            lines.append(f"All context for the conversation: {context}")
        lines.append(self.invoke_prompt(kwargs=kwargs))
        return "\n\n".join(lines)

    def search(
        self,
        name: str,
        query: str,
        top_k: int = _DEFAULT_TOP_K,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search a tool in the service.

        Args:

            name: The name of the search tool
            query: The query string
            top_k: The number of results to return, defaults to 5
            filter: The filter for the search, default to None (no filter)

        Returns:

            List[Dict[str, Any]]: The search results

        Example:

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
            vdb_conf = make_local_vector_db_config()

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
        self.logger.debug("Searching %s with query %s filter %s", name, query, filter)
        if query == "":
            return []
        return self.invoke_tool(
            _SEARCH_TOOL_PREFIX + name,
            dict(query=query, top_k=top_k, filter=json.dumps(filter or {})),
        )

    def _invoke(
        self,
        name: str,
        entity_args: List[str],
        llm_args: List[str],
        kwargs: Dict[str, Any],
        feature_type: str,
        timeout_sec: float,
    ):
        ctx_map = {}
        key_map = {}
        for k, v in kwargs.items():
            if k in entity_args:
                key_map[k] = v
            # elif k not in llm_args:
            #    raise ValueError(f"Unknown argument {k}")
            if k in llm_args:
                ctx_map[k] = v

        result = self._get_feature_value(
            name, key_map, ctx_map, feature_type=feature_type, timeout_sec=timeout_sec
        )
        self.logger.debug("Result of %s: %s", name, result)
        return result

    def _get_context(self) -> Dict[str, Any]:
        return (self._current_context.get() or {}).copy()

    def _get_feature_value(
        self,
        name: str,
        key_map: Dict[str, Any],
        request_map: Dict[str, Any],
        feature_type: str,
        timeout_sec: float,
    ):
        raise NotImplementedError

    def _get_sys_prompt(self) -> Optional[Dict[str, Any]]:
        return self.metastore.get("prompt")


class ToolWrapper:
    subtype: str = "tool"

    @property
    def use_when(self) -> Optional[Callable]:
        return None

    @property
    def metastore_key(self) -> str:
        raise NotImplementedError

    @property
    def tool_name(self) -> str:
        raise NotImplementedError

    def make_base_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.tool_name,
            "type": "tool",
            "subtype": self.subtype,
            "subtype_path": _type_to_str(self.__class__),
            "use_when": (inspect.getsource(self.use_when) if self.use_when else ""),
        }

    def make_metadata(self) -> Dict[str, Any]:
        raise NotImplementedError

    def make_rtfv(self) -> Any:
        return None

    @classmethod
    def invoke(cls, agent: AgentBase, name: str, kwargs: Dict[str, Any]) -> Any:
        raise NotImplementedError


class _IntegratedAgent:
    def __init__(
        self,
        client: AgentBase,
        llm: Any,
        is_emitter: bool = False,
        input: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.client = client
        self.llm = llm
        self.meta_key = "emitters" if is_emitter else "tools"
        self.tools = self._make_tools(input=input)

    def invoke(self, question, history=None, context=None, kwargs=None) -> str:
        raise NotImplementedError  # pragma: no cover

    def _add_sys_prompt(self, history):
        sys_prompt = ("system", self.client.invoke_system_prompt())
        history.insert(0, sys_prompt)
        return history

    def _get_tool_schema(self, name) -> BaseModel:
        meta = self.client.metastore[self.meta_key][name]
        return openai_function_to_pydantic(meta["function"])

    def _make_tool(self, name):
        raise NotImplementedError

    def _make_tools(self, input: Optional[Dict[str, Any]] = None) -> List[Any]:
        if input is None:  # no initial message
            return [
                self._make_tool(name)
                for name, value in self.client.metastore.get(self.meta_key, {}).items()
            ]
        else:
            return [
                self._make_tool(name)
                for name, value in self.client.select_metastore(
                    self.meta_key, input=input
                ).items()
            ]


@lru_cache
def _get_workspace(url: str, workspace: str, api_key: str) -> Any:
    import tecton

    tecton.login(url, tecton_api_key=api_key)
    return tecton.get_workspace(workspace)


class FeatureServiceConfig(ToolWrapper):
    subtype: str = "fs"

    def __init__(
        self,
        service: str,
        *,
        url: Optional[str] = None,
        workspace: Optional[str] = None,
        api_key: Union[RuntimeVar, str, None] = None,
        description: Optional[str] = None,
        use_when: Optional[Callable] = None,
        timeout: Any = None,
    ):
        def get_conf() -> Any:
            # lazy load to avoid rtfv tecton dependency
            from tecton import conf

            return conf

        if url is None and not is_dev_mode():
            url = get_conf().tecton_url()
        if workspace is None and not is_dev_mode():
            workspace = get_conf().get_or_raise("TECTON_WORKSPACE")
        if api_key is None and not is_dev_mode():
            api_key = RuntimeVar(
                name="TECTON_API_KEY", sources=["env", "secrets", "tecton"]
            )

        self.url = url
        self.workspace = workspace
        self._api_key = api_key
        self.service = service
        self.description = description
        self.timeout = timeout
        self._use_when = use_when

    @property
    def use_when(self) -> Optional[Callable]:
        return self._use_when

    @property
    def metastore_key(self) -> str:
        return self.workspace + "_" + self.service

    @property
    def tool_name(self) -> str:
        return self.metastore_key

    @property
    def api_key(self) -> str:
        if isinstance(self._api_key, RuntimeVar):
            return self._api_key.get()
        return self._api_key

    def get_emitter(
        self,
        streaming_source_name: str,
        description: Optional[str] = None,
        use_history: bool = False,
    ) -> Any:
        from tecton_core.schema import Schema

        from ..tecton_utils.convert import tecton_type_to_python_annotation
        from ..tecton_utils.deco import _internal_emitter

        fs_json = to_json_config(self)
        src = self._get_workspace().get_data_source(streaming_source_name)
        description = description or src.description
        if not description:
            raise ValueError("Description is required for emitter")
        schema = {
            k: (tecton_type_to_python_annotation(v), Field())
            for k, v in Schema(src._spec.schema.tecton_schema).to_dict().items()
        }
        ts_keys = [k for k, v in schema.items() if v[0] == datetime]
        if len(ts_keys) != 1:
            raise ValueError("One and only one timestamp key is allowed")
        schema.pop(ts_keys[0])
        model = create_model(streaming_source_name, **schema, __doc__=description)
        timeout_sec = Configs.get_default().get_timeout_sec(self.timeout)

        @_internal_emitter(
            name="_".join([streaming_source_name, "emitter"]),
            input_schema=model,
            description=description,
            use_history=use_history,
        )
        def _emitter(**kwargs) -> None:
            from ..utils._tecton_client_utils import ingest
            from ..utils.config_wrapper import from_json_config

            conf = from_json_config(fs_json)
            input = kwargs.copy()
            input[ts_keys[0]] = datetime.utcnow()
            ingest(
                cluster_url=conf.url,
                workspace=conf.workspace,
                api_key=conf.api_key,
                push_source_name=streaming_source_name,
                ingestion_records=[input],
                timeout_sec=timeout_sec,
            )

        return _emitter

    def get_all_emitters(self, use_history: bool = False) -> List[Any]:
        from tecton import StreamSource

        res = []
        ws = self._get_workspace()
        for src in ws.list_data_sources():
            if isinstance(ws.get_data_source(src), StreamSource):
                res.append(self.get_emitter(src, use_history=use_history))
        return res

    def make_metadata(self) -> Dict[str, Any]:
        from ..tecton_utils._internal import entity_to_pydantic

        fs = self._get_workspace().get_feature_service(self.service)
        description = self.description or fs.description
        if not description:
            raise ValueError(
                f"FeatureService {self.service} must have a description or you "
                "should provide the description"
            )
        fv = fs._feature_definitions.pop()
        model = entity_to_pydantic(fv.entities[0], fv.transformation_schema())
        func = to_openai_function(model, name=self.tool_name, description=description)
        args = list(model.model_fields.keys())
        return {
            **self.make_base_metadata(),
            "args": args,
            "function": func,
            "service_json": to_json_config(self),
            "timeout_sec": Configs.get_default().get_timeout_sec(self.timeout),
        }

    @classmethod
    def invoke(cls, agent: AgentBase, name: str, kwargs: Dict[str, Any]) -> Any:
        from .client import _get_tecton_client

        meta = agent.metastore["tools"][name]
        ctx = agent._get_context()
        ctx.update(kwargs)
        fs = from_json_config(meta["service_json"])
        client = _get_tecton_client(
            url=fs.url,
            workspace=fs.workspace,
            api_key=fs.api_key,
            timeout_sec=meta["timeout_sec"],
        )
        input_args = {k: ctx[k] for k in meta["args"]}
        # TODO: this may be over simplified. request_context_map is never used
        # it doesn't work if the feature is realtime
        gf = client.get_features(
            feature_service_name=fs.service,
            join_key_map=input_args,
        )
        return gf.get_features_dict()

    def __json_config_dict__(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "workspace": self.workspace,
            "api_key": self._api_key,
            "service": self.service,
            "description": self.description,
            "timeout": self.timeout,
        }

    def _get_workspace(self) -> Any:
        return _get_workspace(
            url=self.url,
            workspace=self.workspace,
            api_key=self.api_key,
        )


class VectorDBConfig(ToolWrapper):
    subtype: str = "vdb"

    def __init__(
        self,
        name: str,
        vector_db: Dict[str, Any],
        *,
        filter: Union[Dict[str, Any], Type[BaseModel], None] = None,
        top_k: int = 5,
        search_type: str = "mmr",
        description: Optional[str] = None,
        use_when: Optional[Callable] = None,
        timeout: Any = None,
    ):
        self.vector_db = vector_db
        self.description = description
        self.timeout = timeout
        if filter is None:
            self.filter: Dict[str, Any] = {}
        elif isinstance(filter, dict):
            self.filter = filter
        else:
            self.filter = to_openai_properties(
                filter, args=list(filter.model_fields.keys())
            )
        self.top_k = top_k
        self.search_type = search_type
        self.name = name
        self._use_when = use_when

    @property
    def use_when(self) -> Optional[Callable]:
        return self._use_when

    @property
    def metastore_key(self) -> str:
        return self.name

    @property
    def tool_name(self) -> str:
        return self.metastore_key

    @property
    def filter_keys(self) -> List[str]:
        return list(self.filter.keys())

    @property
    def filter_model(self) -> BaseModel:
        return openai_properties_to_pydantic(self.filter, name=self.name)

    def make_instance(self) -> Any:
        return make_vector_db(self.vector_db, conf=False)

    def make_metadata(self) -> Dict[str, Any]:
        params = {
            name: (field.annotation, field)
            for name, field in self.filter_model.model_fields.items()
        }
        input_model = create_model(
            self.name + "_input",
            query=(str, Field(description="The query to search the vector database")),
            **params,
        )
        args = list(input_model.model_fields.keys())
        return {
            **self.make_base_metadata(),
            "args": args,
            "function": to_openai_function(
                input_model, name=self.tool_name, description=self.description
            ),
            "vdb_json": to_json_config(self),
            "timeout_sec": Configs.get_default().get_timeout_sec(self.timeout),
        }

    def make_rtfv(self) -> Any:
        return None

    def __json_config_dict__(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "vector_db": self.vector_db,
            "top_k": self.top_k,
            "search_type": self.search_type,
            "description": self.description,
            "timeout": self.timeout,
            "filter": self.filter,
        }

    @classmethod
    def invoke(cls, agent: AgentBase, name: str, kwargs: Dict[str, Any]) -> Any:
        from ..integrations.langchain import langchain_vector_search

        meta = agent.metastore["tools"][name]
        ctx = agent._get_context()
        ctx.update(kwargs)
        conf, vdb, filter_keys = _get_vdb_instance(meta["vdb_json"])
        filter = {k: ctx[k] for k in filter_keys}
        params = {"filter": filter} if filter else {}
        res = langchain_vector_search(
            vdb, ctx["query"], top_k=conf.top_k, search_type=conf.search_type, **params
        )
        jres = []
        for x in res:
            jres.append(x.metadata)
        return jres


@lru_cache
def _get_vdb_instance(vdb_json: str) -> Tuple[VectorDBConfig, Any, List[str]]:
    conf = from_json_config(vdb_json)
    return conf, conf.make_instance(), conf.filter_keys
