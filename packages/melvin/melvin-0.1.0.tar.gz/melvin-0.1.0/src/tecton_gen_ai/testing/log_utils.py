import logging
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Dict, Iterator, List, Optional

import ipywidgets as widgets
from IPython.display import display

from ..utils.log import NOOP_LOGGER


class UILogHandler(logging.Handler):
    def __init__(self, diagram: bool):
        super().__init__()
        self.diagram = diagram
        self.history: List[List[str]] = []
        self.prompt: Dict[str, Any] = {}

    def emit(self, record: Any) -> None:
        if not self.diagram:
            self.emit_text(record)
        else:
            flow_event = getattr(record, "flow_event", None)
            if flow_event is not None:
                if flow_event.get("type") == "prompt":
                    self.prompt = flow_event
                    return
                diagram = self.build_diagram(flow_event)
                self.emit_diagram(diagram=diagram)

    def emit_text(self, record: Any) -> None:
        raise NotImplementedError

    def emit_diagram(self, diagram: Any) -> None:
        raise NotImplementedError

    def build_diagram(self, flow_event: Any) -> None:
        from .diagrams import plot_execution

        if flow_event["type"] == "llm":
            self.history.append([])
        else:
            self.history[-1].append(flow_event)
        prompt_uses_features = len(self.prompt.get("source_names", [])) > 0
        return plot_execution(self.history, prompt_uses_features)


class _WidgetLogHandler(UILogHandler):
    def __init__(self, output: widgets.Output, diagram: bool):
        super().__init__(diagram)
        self.output = output

    def emit_text(self, record: Any) -> None:
        with self.output:
            print(self.format(record))

    def emit_diagram(self, diagram: Any) -> None:
        with self.output:
            self.output.clear_output()
            display(diagram)


_UI_LOGGER = ContextVar("ui_logger", default=NOOP_LOGGER)


@contextmanager
def set_ui_logger(hanlder: Optional["UILogHandler"]) -> Iterator[logging.Logger]:
    if hanlder is None:
        logger = NOOP_LOGGER
    else:
        logger = logging.getLogger("widget")
        logger.handlers.clear()
        logger.addHandler(hanlder)
        logger.propagate = False
        logger.setLevel(logging.DEBUG)
    token = _UI_LOGGER.set(logger)
    try:
        yield logger
    finally:
        _UI_LOGGER.reset(token)


def get_ui_logger() -> logging.Logger:
    return _UI_LOGGER.get()
