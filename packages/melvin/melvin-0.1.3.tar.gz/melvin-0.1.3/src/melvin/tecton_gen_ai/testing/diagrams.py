import pathlib
from typing import Any, List
from uuid import uuid4

from diagrams import Diagram, Edge
from diagrams.custom import Custom

_ICON_PATH = pathlib.Path(__file__).parent.parent.resolve() / "resources"
_DEFUALT_GRAPH_ATTR = {
    "pad": "0",
    "size": "10,6",
    "ratio": "0.3",
    "splines": "line",
}
_DEFUALT_NODE_ATTR = {
    "fontsize": "15",
    "fixedsize": "true",
}


class LLM(Custom):
    def __init__(self, label: str, **kwargs: Any):
        super().__init__(label, str(_ICON_PATH / "llm.png"), **kwargs)


class Input(Custom):
    def __init__(self, label: str, **kwargs: Any):
        super().__init__(label, str(_ICON_PATH / "input.png"), **kwargs)


class Output(Custom):
    def __init__(self, label: str, **kwargs: Any):
        super().__init__(label, str(_ICON_PATH / "input.png"), **kwargs)


class Prompt(Custom):
    def __init__(self, label: str, enriched: bool, **kwargs: Any):
        suffix = "-enriched" if enriched else ""
        super().__init__(label, str(_ICON_PATH / f"prompt{suffix}.png"), **kwargs)


class Tool(Custom):
    def __init__(self, label: str, **kwargs: Any):
        super().__init__(label, str(_ICON_PATH / "tool.png"), **kwargs)


class Table(Custom):
    def __init__(self, label: str, **kwargs: Any):
        super().__init__(label, str(_ICON_PATH / "table.png"), **kwargs)


class VectorDB(Custom):
    def __init__(self, label: str, **kwargs: Any):
        super().__init__(label, str(_ICON_PATH / "vdb.png"), **kwargs)


class FeatureTool(Custom):
    def __init__(self, label: str, **kwargs: Any):
        super().__init__(label, str(_ICON_PATH / "feature-tool.png"), **kwargs)


class KnowledgeTool(Custom):
    def __init__(self, label: str, **kwargs: Any):
        super().__init__(label, str(_ICON_PATH / "knowledge-tool.png"), **kwargs)


def plot_execution(
    history: List[List[Any]],
    prompt_uses_features: bool,
    graph_attr=_DEFUALT_GRAPH_ATTR,
    node_attr=_DEFUALT_NODE_ATTR,
) -> Diagram:
    def get_id():
        return str(uuid4())

    def edge(**kwargs: Any):
        return Edge(penwidth="2", **kwargs)

    class QuietDiagram(Diagram):
        def _repr_png_(self):
            return self.dot.pipe(format="png", quiet="true")

    with QuietDiagram(
        "", show=False, graph_attr=graph_attr, node_attr=node_attr, direction="LR"
    ) as diag:
        prompt = Prompt("System Prompt", prompt_uses_features)
        query = Input("Input")
        end = [query, prompt]
        for x in history:
            if len(x) == 0:
                new_end = LLM("LLM", id=get_id())
                end >> edge() >> new_end
            else:
                tools = []
                for tc in x:
                    tp = Tool
                    if tc["subtype"] == "fv":
                        tp = Table
                    elif tc["subtype"] == "retriever":
                        tp = VectorDB
                    elif tc.get("features", []):
                        tp = FeatureTool
                    elif "knowledge" in tc:
                        tp = KnowledgeTool
                    tool = tp(tc["value"], id=get_id())
                    tools.append(tool)
                new_end = tools
                if len(new_end) == 1:
                    new_end = new_end[0]
                end >> edge() >> LLM("LLM", id=get_id()) >> edge() >> new_end
            end = new_end
        end >> edge() >> Output("Output")

    return diag
