import importlib
import inspect
from functools import lru_cache
from typing import Any, Iterable, List, Tuple

from ...api import Agent, Configs, tool
from ...utils.code_parser import get_declaration

_DEFAULT_GEN_AI_MODULES = tuple(
    [
        "tecton_gen_ai.api",
        "tecton_gen_ai.testing",
    ]
)


@lru_cache
def make_copilot(
    modules: Tuple = _DEFAULT_GEN_AI_MODULES,
    mode: str = "brute_force",
    llm: Any = None,
    name: str = "copilot",
) -> Agent:
    prefix = """You are a copilot that helps users use tecton_gen_ai package to build AI projects.
Your main task is generating code based on user's input."""
    objects = list(_FuncOrClass.from_expressions(modules))
    if (llm or Configs.get_default().llm) is None:
        raise ValueError("Please set the language model for the copilot.")
    if mode == "brute_force":
        declarations = "\n\n".join([obj.declaration for obj in objects])

        sys_prompt = f"""{prefix}

Here are the functions and classes you can use to generate code:

{declarations}
"""

        return Agent(name=name, prompt=sys_prompt, llm=llm)
    elif mode == "tools":
        tools = [obj.to_tool() for obj in objects]
        return Agent(name=name, prompt=prefix, tools=tools, llm=llm)
    else:
        raise ValueError(f"Invalid mode: {mode}")


def assist(
    question: str,
    modules: Tuple = _DEFAULT_GEN_AI_MODULES,
    llm: Any = None,
    mode: str = "brute_force",
) -> Any:
    """
    Get the copilot's response to the user's question.

    TODO: not using tools seem to provide much better results.
    """
    from IPython.display import Markdown, display

    agent = make_copilot(modules=tuple(modules), mode=mode, name="copilot", llm=llm)
    resp = agent.invoke(question)
    display(Markdown(resp))


def chat(
    llm: Any = None,
    mode: str = "brute_force",
    modules: Tuple = _DEFAULT_GEN_AI_MODULES,
) -> None:
    """
    Chat with the copilot in notebook to generate code based on user's input.
    """

    from ...interactive import chat as _chat

    agent = make_copilot(modules=tuple(modules), mode=mode, name="copilot", llm=llm)
    _chat(agent)


class _FuncOrClass:
    def __init__(self, obj: Any):
        self.obj = obj
        self.declaration = get_declaration(obj, entrypoint_only=False)
        self.callable_declaration = get_declaration(obj, entrypoint_only=True)
        self.name = obj.__name__
        self.doc = (obj.__doc__ or "").split("Args:")[0].strip()

    @property
    def tool_description(self) -> str:
        return (
            f"Get the declaration of {self.name}. "
            f"The purpose of {self.name}:\n{self.doc}"
        )

    @property
    def tool_name(self) -> str:
        return f"get_declaration_of_{self.name}"

    def to_tool(self) -> Any:
        description = self.tool_description
        name = self.tool_name

        @tool(name=name, description=description)
        def _tool() -> str:
            return self.declaration

        return _tool

    @staticmethod
    def from_expressions(expressions: List[str]) -> Iterable["_FuncOrClass"]:
        for expr in expressions:
            try:
                module = importlib.import_module(expr)
                names = [name for name in dir(module) if not name.startswith("_")]
            except Exception:
                parts = expr.rsplit(".", 1)
                module = importlib.import_module(parts[0])
                names = [parts[1]]
            objs = [getattr(module, name) for name in names]
            yield from [
                _FuncOrClass(x)
                for x in objs
                if inspect.isclass(x) or inspect.isfunction(x)
            ]
