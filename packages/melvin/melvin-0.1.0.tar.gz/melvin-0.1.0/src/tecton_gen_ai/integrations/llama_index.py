from typing import Any, Dict, Optional, Type, Union

from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent.runner.base import AgentRunner
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from ..agent.base import AgentBase, _IntegratedAgent, invoke_agent, make_agent
from ..factories.llm import make_llm_model


@make_llm_model.register(FunctionCallingLLM)
def make_llama_index_model(obj: FunctionCallingLLM) -> FunctionCallingLLM:
    return obj


@invoke_agent.register(FunctionCallingLLM)
def _invoke_llama(
    llm: FunctionCallingLLM,
    client: AgentBase,
    input: Dict[str, Any],
    output_schema: Union[Type[str], Type[BaseModel]] = str,
    **kwargs: Any,
) -> str:
    runner = make_llama_index_agent_runner(
        llm, client, output_schema=output_schema, **kwargs
    )
    client.logger.debug(
        "Invoking LlamaIndex agent with %s",
        input,
    )
    message = input.get("message")
    res = runner.chat(message, chat_history=input.get("chat_history"))
    if issubclass(output_schema, BaseModel):
        messages = ChatPromptTemplate(
            message_templates=[
                ChatMessage(role=MessageRole.USER, content=message),
                ChatMessage(role=MessageRole.ASSISTANT, content=str(res)),
                ChatMessage(
                    role=MessageRole.USER, content="convert the response to structured"
                ),
            ]
        )
        res = llm.structured_predict(output_cls=output_schema, prompt=messages)
        return res
    else:
        return str(res)


@make_agent.register(FunctionCallingLLM)
def make_llama_index_agent_runner(
    llm: FunctionCallingLLM,
    client: AgentBase,
    output_schema: Union[Type[str], Type[BaseModel]] = str,
    initial_input: Optional[Dict[str, Any]] = None,
    **runner_kwargs: Any,
) -> AgentRunner:
    agent = _LlamaIndexAgent(client, llm, input=initial_input)
    return agent.make_agent_runner(**runner_kwargs)


class _LlamaIndexAgent(_IntegratedAgent):
    def make_agent_runner(self, **kwargs):
        agent_worker = _TectonFunctionCallingAgentWorker.from_tools(
            self.tools,
            llm=self.llm,
            verbose=kwargs.get("verbose", False),
            allow_parallel_tool_calls=True,
            tecton_agent=self,
        )
        agent = agent_worker.as_agent(**kwargs)
        return agent

    def _make_tool(self, name):
        from llama_index.core.tools import FunctionTool

        def f(**kwargs):
            pass

        model = self._get_tool_schema(name)
        _tool = FunctionTool.from_defaults(
            fn=f, fn_schema=model, name=name, description=model.__doc__
        )
        _tool._fn = lambda **kwargs: self.client.invoke_tool(name, kwargs)
        return _tool


class _TectonFunctionCallingAgentWorker(FunctionCallingAgentWorker):
    def __init__(self, *args, tecton_agent: _LlamaIndexAgent, **kwargs):
        super().__init__(*args, **kwargs)
        self._tecton_agent = tecton_agent

    def _make_messages(self, question, history):
        history = history or []
        history = self._add_sys_prompt(history)
        return history + [("human", question)]

    def get_all_messages(self, task):
        sys_prompt = self._tecton_agent.client.invoke_system_prompt()
        self.prefix_messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=sys_prompt)
        ]
        return super().get_all_messages(task)
