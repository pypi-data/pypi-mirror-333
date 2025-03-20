from contextlib import contextmanager
from functools import singledispatch
from logging import Logger
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents.format_scratchpad.tools import format_to_tool_messages
from langchain.agents.output_parsers.tools import ToolsAgentOutputParser
from langchain.chains.base import Chain
from langchain_community.callbacks import get_openai_callback
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import StructuredTool
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel

from ..agent.base import (
    AgentBase,
    _IntegratedAgent,
    invoke_agent,
    invoke_emitters,
    make_agent,
)
from ..factories.llm import (
    invoke_llm_model,
    make_llm,
    make_llm_model,
    make_llm_model_conf,
)
from ..factories.vector_db import make_vector_db_conf, make_vector_db_instance
from ..utils.config_wrapper import as_config
from ..utils.hashing import to_uuid
from ..utils.log import report_cost

_LLM_PROVIDERS: dict[str, Callable] = {}


@make_llm_model.register(BaseChatModel)
def make_langchain_model(obj: BaseChatModel) -> BaseChatModel:
    return obj


@invoke_llm_model.register(BaseChatModel)
def invoke_langchain_model(
    llm: BaseChatModel,
    prompt: Union[str, List[Tuple[str, str]]],
    output_schema: Union[Type[BaseModel], Type[str]] = str,
) -> Any:
    with track_llm_cost():
        if output_schema is not str:
            llm = llm.with_structured_output(output_schema)
            return llm.invoke(prompt)
        return llm.invoke(prompt).content


@make_llm_model.register(Embeddings)
def make_langchain_embedding_model(obj: Embeddings) -> Embeddings:
    return obj


@make_llm_model.register(dict)
def make_langchain_model_from_dict(
    model_conf: dict,
) -> Union[BaseChatModel, Embeddings]:
    model, conf = _parse_dict(model_conf)
    return model(**conf)


@make_llm_model_conf.register(dict)
def make_langchain_model_conf_from_dict(model_conf: dict) -> dict:
    model, conf = _parse_dict(model_conf)
    return as_config(model)(**conf)


@contextmanager
def track_llm_cost():
    with get_openai_callback() as cb:
        try:
            yield cb
        finally:
            report_cost(cb.total_cost, cb.successful_requests)


def langchain_llm_provider(name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        _LLM_PROVIDERS[name] = func
        return func

    return decorator


@langchain_llm_provider("openai")
def _make_openai_llm(model_name: str, conf: dict) -> Tuple[Type, Dict]:
    if "embedding" in model_name:
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings, conf
    else:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI, conf


@langchain_llm_provider("azure_openai")
def _make_azure_openai_llm(model_name: str, conf: dict) -> Tuple[Type, Dict]:
    if "embedding" in model_name:
        from langchain_openai import AzureOpenAIEmbeddings

        return AzureOpenAIEmbeddings, conf
    else:
        from langchain_openai import AzureChatOpenAI

        return AzureChatOpenAI, conf


@langchain_llm_provider("anthropic")
def _make_anthropic_llm(model_name: str, conf: dict) -> Tuple[Type, Dict]:
    from langchain_anthropic import ChatAnthropic

    return ChatAnthropic, conf


@langchain_llm_provider("bedrock")
def _make_bedrock_llm(model_name: str, conf: dict) -> Tuple[Type, Dict]:
    if "embed" in model_name:
        from langchain_aws import BedrockEmbeddings

        conf["model_id"] = conf.pop("model")
        return BedrockEmbeddings, conf
    else:
        from langchain_aws import ChatBedrock

        return ChatBedrock, conf


@langchain_llm_provider("google")
def _make_google_llm(model_name: str, conf: dict) -> Tuple[Type, Dict]:
    if "embed" in model_name:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings, conf
    else:
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI, conf


def _parse_dict(data: Dict[str, Any]) -> Tuple[Type, Dict]:
    conf = dict(data)
    parts = conf.pop("model").split("/", 1)
    provider, model_name = parts[0], parts[1]
    conf["model"] = model_name
    if provider in _LLM_PROVIDERS:
        return _LLM_PROVIDERS[provider](model_name, conf)
    raise NotImplementedError(f"{provider} not supported")


@make_vector_db_instance.register(VectorStore)
def make_langchain_vector_db_instance(obj: VectorStore) -> VectorStore:
    return obj


@make_vector_db_instance.register(dict)
def make_langchain_vector_db_instance_from_dict(
    vdb_conf: dict,
) -> VectorStore:
    vdb, conf = _parse_vdb_dict(vdb_conf)
    return vdb(**conf)


@make_vector_db_conf.register(dict)
def make_langchain_vector_db_conf_from_dict(vdb_conf: dict) -> dict:
    vdb, conf = _parse_vdb_dict(vdb_conf, as_conf=True)
    return as_config(vdb)(**conf)


def _parse_vdb_dict(data: Dict[str, Any], as_conf: bool = False) -> Tuple[Type, Dict]:
    conf = dict(data)
    provider = conf.pop("provider")
    embedding = make_llm(conf.pop("embedding"), conf=as_conf)
    conf["embedding"] = embedding
    if provider == "memory":
        from langchain_community.vectorstores.inmemory import InMemoryVectorStore

        return InMemoryVectorStore, conf
    if provider == "lancedb":
        from langchain_community.vectorstores.lancedb import LanceDB

        return LanceDB, conf
    if provider == "pinecone":
        from langchain_pinecone import PineconeVectorStore

        return PineconeVectorStore, conf
    raise NotImplementedError(f"{provider} not supported")


@invoke_agent.register(BaseChatModel)
def _invoke_langchain(
    llm: BaseChatModel,
    client: AgentBase,
    input: Dict[str, Any],
    output_schema: Union[Type[str], Type[BaseModel]] = str,
    **kwargs: Any,
) -> Any:
    with track_llm_cost():
        callbacks = list(kwargs.pop("callbacks", []))
        cb = _ExecutionCallback(client.logger, client)
        callbacks.append(cb)
        executor = make_langchain_agent_executor(
            llm,
            client,
            output_schema,
            initial_input=input,
            **kwargs,
        )
        chat_history = input.get("chat_history")
        client.logger.debug("Invoking LangChain agent with input: %s", input)
        _input = {"input": input["message"]}
        if chat_history:
            _input["chat_history"] = chat_history
        try:
            return executor.invoke(_input, {"callbacks": callbacks})
        except _StructuredOutput as e:
            return e.output


@invoke_emitters.register(BaseChatModel)
def _invoke_langchain_emitters(
    llm: BaseChatModel,
    client: AgentBase,
    input: Dict[str, Any],
    **kwargs: Any,
) -> None:
    agent = _LangChainAgent(client, llm, is_emitter=True, input=input)
    agent.run_emitters(input, **kwargs)


@make_agent.register(BaseChatModel)
def make_langchain_agent_executor(
    llm: BaseChatModel,
    client: AgentBase,
    output_schema: Union[Type[str], Type[BaseModel]] = str,
    initial_input: Optional[Dict[str, Any]] = None,
    **executor_kwargs: Any,
) -> Chain:
    agent = _LangChainAgent(
        client,
        llm,
        is_emitter=False,
        input=initial_input,
    )
    return agent.make_executor(output_schema=output_schema, **executor_kwargs)


@singledispatch
def unified_langchain_vector_search(
    vdb: VectorStore,
    query: str,
    top_k: int,
    search_type: str = "similarity",
    **params: Any,
) -> List[Document]:
    return vdb.search(query, k=top_k, search_type=search_type, **params)


def langchain_vector_search(
    vdb: VectorStore,
    query: str,
    top_k: int,
    search_type: str = "similarity",
    **params: Any,
) -> List[Document]:
    try:
        from .lancedb import _lancedb_vector_search  # noqa
    except ImportError:
        pass

    return unified_langchain_vector_search(
        vdb, query=query, top_k=top_k, search_type=search_type, **params
    )


def langchain_vector_ingest(
    vdb: VectorStore,
    texts: List[str],
    metadatas: Optional[List[Dict[str, Any]]] = None,
    ids: Optional[List[str]] = None,
) -> None:
    if ids is None:
        ids = [to_uuid(text) for text in texts]
    if metadatas is None:
        metadatas = [{} for _ in texts]
    vdb.add_texts(texts=texts, metadatas=metadatas, ids=ids)


class _LangChainAgent(_IntegratedAgent):
    def make_executor(self, output_schema: Any, **kwargs: Any) -> Chain:
        tools = self.tools
        prompt = self._make_prompt_template(tools)
        if len(tools) > 0:
            if output_schema is str:

                def parse(message: Dict[str, Any]) -> Any:
                    output = message["output"]
                    if isinstance(output, list):
                        output = output[0]["text"]
                    return output

                return (
                    _make_lc_agent_executor(
                        llm=self.llm, tools=tools, prompt=prompt, **kwargs
                    )
                    | parse
                )

            else:

                def _final_structured_output(**kwargs):
                    raise _StructuredOutput(kwargs)

                _final_tool = StructuredTool.from_function(
                    _final_structured_output,
                    description="""
Final output tool for structured output.
This tool must be used once and only once in the end to generate the final structured output.

"""
                    + (output_schema.__doc__ or ""),
                    args_schema=output_schema,
                    infer_schema=False,
                )
                return _make_lc_agent_executor(
                    llm=self.llm,
                    tools=tools + [_final_tool],
                    prompt=prompt,
                    bind_kwargs={"tool_choice": "any"},
                    **kwargs,
                )
        else:
            if issubclass(output_schema, BaseModel):
                llm = self.llm.with_structured_output(output_schema)

                return prompt | llm

            def parse(message: AIMessage) -> str:
                return message.content

            return prompt | self.llm | parse

    def run_emitters(self, input: Dict[str, Any], **kwargs: Any) -> None:
        message = input["message"]
        chat_history = input.get("chat_history")
        tools = self.tools
        if len(tools) == 0:
            return
        prompt = self._make_prompt_template(tools)
        metastore = self.client.metastore[self.meta_key]
        kwargs = kwargs.copy()
        kwargs["max_iterations"] = 3
        emitters_no_history = [e for e in tools if not metastore[e.name]["use_history"]]
        emitters_with_history = [e for e in tools if metastore[e.name]["use_history"]]
        if len(emitters_no_history) > 0:
            agent = create_tool_calling_agent(
                self.llm, emitters_no_history, prompt=prompt
            )
            executor = AgentExecutor(
                agent=agent, tools=emitters_no_history, **kwargs, verbose=True
            )
            executor.invoke({"input": message})
        if len(emitters_with_history) > 0:
            agent = create_tool_calling_agent(
                self.llm, emitters_with_history, prompt=prompt
            )
            executor = AgentExecutor(
                agent=agent, tools=emitters_with_history, **kwargs, verbose=True
            )
            executor.invoke({"input": message, "chat_history": chat_history})

    def _make_prompt_template(self, tools: List[Any]):
        templates = [
            MessagesPlaceholder("system_prompt"),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
        ]
        if len(tools) > 0:
            templates.append(MessagesPlaceholder("agent_scratchpad"))
        prompt = ChatPromptTemplate.from_messages(templates)
        prompt = prompt.partial(
            system_prompt=lambda: [("system", self.client.invoke_system_prompt())]
        )
        return prompt

    def _make_messages(self, question, history):
        history = history or []
        history = self._add_sys_prompt(history)
        return history + [("human", question)]

    def _make_tool(self, name):
        from langchain_core.tools import StructuredTool

        model = self._get_tool_schema(name)

        def f(**kwargs):
            pass

        _tool = StructuredTool.from_function(
            name=name,
            func=f,
            args_schema=model,
            infer_schema=False,
            description=model.__doc__,
        )
        if self.meta_key == "tools":
            _tool.func = lambda **kwargs: self.client.invoke_tool(name, kwargs)
        else:
            _tool.func = lambda **kwargs: self.client.invoke_emitter(name, kwargs)
        return _tool


class _ExecutionCallback(BaseCallbackHandler):
    def __init__(self, logger: Logger, client: AgentBase):
        self.metastore = client.metastore
        self.logger = logger

    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
    ) -> None:
        self.logger.debug("Chat model started", extra={"flow_event": {"type": "llm"}})

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        name = serialized.get("name")
        extra = {"flow_event": {"type": "tool", "value": name}}
        tool = self.metastore.get("tools", {}).get(name, {})
        extra["flow_event"]["subtype"] = tool.get("subtype", "")
        if tool.get("subtype") == "search":
            extra["flow_event"]["knowledge"] = tool.get("source_names", [])
        else:
            extra["flow_event"]["features"] = tool.get("source_names", [])
        self.logger.debug(f"Tool {name} started", extra=extra)


class _StructuredOutput(Exception):
    def __init__(self, output: Any):
        super().__init__()
        self.output = output


def _make_lc_agent_executor(
    llm: Any,
    tools: List[Any],
    prompt: Any,
    bind_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> AgentExecutor:
    # a copy from create_tool_calling_agent because it doesn't have bind_kwargs
    llm_with_tools = llm.bind_tools(tools, **(bind_kwargs or {}))

    agent = (
        RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_to_tool_messages(x["intermediate_steps"])
        )
        | prompt
        | llm_with_tools
        | ToolsAgentOutputParser()
    )

    ae = AgentExecutor(agent=agent, tools=tools, **kwargs)
    ae.agent.stream_runnable = False
    return ae
