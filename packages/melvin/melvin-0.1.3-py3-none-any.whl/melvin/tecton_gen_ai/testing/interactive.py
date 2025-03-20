import logging
import re
from typing import Any, Callable, Dict, Optional

import ipywidgets as widgets
from IPython.display import HTML, Markdown, display

from ..agent.base import AgentBase
from ..testing.log_utils import (
    _WidgetLogHandler,
    get_ui_logger,
    set_ui_logger,
)

from .utils import print_md


def qna(
    client: AgentBase,
    *,
    query: Optional[str] = None,
    context: Any = None,
    debug: bool = True,
    diagram: bool = False,
) -> Any:
    def _run(message: str) -> str:
        logger = get_ui_logger()
        logger.setLevel(logging.DEBUG)
        with client.set_logger(logger):
            return client.invoke(message, context=context)

    if not query:
        return single_turn(
            _run, realtime=False, markdown=True, debug=debug, diagram=diagram
        )

    if not debug:
        res = client.invoke(query, context=context)
    else:
        debugo = widgets.Output()
        display(debugo)
        handler = _WidgetLogHandler(debugo, diagram=diagram)
        with set_ui_logger(hanlder=handler):
            res = _run(query)
    print_md(res)


def auto_complete(
    client: AgentBase,
    search_name: str,
    handle: Any,
    top_k: int = 5,
    debug: bool = False,
) -> Any:
    if isinstance(handle, str):

        def _handle(x):
            return x[handle]

    elif handle is None:

        def _handle(x):
            return str(x)

    else:
        _handle = handle
    return single_turn(
        lambda x: "\n".join(_handle(x) for x in client.search(search_name, x, top_k)),
        realtime=True,
        markdown=False,
        debug=debug,
    )


def chat(
    client: AgentBase, debug: bool = True, context: Optional[Dict[str, Any]] = None
) -> Any:
    chat = _Chat(client, context=context)
    chat.display()


def single_turn(
    on_compute: Callable[[str], str],
    realtime: bool = False,
    markdown: bool = False,
    debug: bool = True,
    diagram: bool = False,
) -> Any:
    # Create a text input widget
    text_input = widgets.Text(
        value="",
        placeholder="Type something",
        disabled=False,
        continuous_update=realtime,
        layout=widgets.Layout(
            width="90%",
            border_radius="10px",
        ),
    )

    output = widgets.Output()
    debugo = widgets.Output()

    def on_event(change):
        with output:
            if not realtime:
                output.clear_output()
                display(Markdown("Generating response..."))
        handler = _WidgetLogHandler(debugo, diagram=diagram) if debug else None
        with set_ui_logger(hanlder=handler):
            res = on_compute(change["new"])
        with output:
            output.clear_output()
            if markdown:
                display(Markdown(res))
            else:
                print(res)

    text_input.observe(on_event, names="value")

    items = [text_input, output]
    if debug:
        accordion = widgets.Accordion(children=[debugo], titles=("Debug",))
        items.append(accordion)

    vbox = widgets.VBox(items)

    # Display the text input widget
    display(vbox)


class _Chat:
    def __init__(self, client: AgentBase, context: Optional[Dict[str, Any]] = None):
        self.box = widgets.Output()
        self.input = widgets.Textarea(
            value="",
            placeholder="Chat with AI",
            rows=5,
            disabled=False,
            layout=widgets.Layout(width="90%"),
        )
        self.submit = widgets.Button(
            description="Submit", layout=widgets.Layout(width="100px")
        )
        hbox = widgets.HBox([self.submit, self.input])
        self.vbox = widgets.VBox([self.box, hbox])
        self.history = []
        self.client = client
        self.context = context

    def display(self):
        display(_CSS)
        self.submit.on_click(self.on_submit)
        display(self.vbox)

    def append(self, role: str, text: str):
        import markdown

        self.history.append((role, text))
        rs = "chat_user" if role == "user" else "chat_agent"
        _text = markdown.markdown(text, extensions=["fenced_code", "codehilite"])
        _text = re.sub("(^<P>|</P>$)", "", _text, flags=re.IGNORECASE)
        q = (
            f'<div class="chat_outer"><div class="chat_role">{role}:'
            f'</div><div class="chat_text {rs}">{_text}</div></div>'
        )
        self.box.append_display_data(HTML(q))

    def on_submit(self, change):
        question = self.input.value
        self.input.disabled = True
        self.input.value = "Generating response ..."
        self.submit.disabled = True
        try:
            self.ask(question)
        finally:
            self.input.value = ""
            self.input.disabled = False
            self.submit.disabled = False

    def ask(self, message: str):
        self.append("user", message)
        response = self.client.invoke(
            message,
            chat_history=self.history,
            context=self.context,
        )
        self.append("ai", response)
        return response


_CSS = HTML(
    """<style>
.chat_outer {
  overflow: hidden;
}

.chat_role {
  width: 100px;
  float: left;
  text-align: right;
  font-weight: bold;
  padding-right: 10px;
}

.chat_text {
  overflow: auto;
}

.chat_agent {
  background-color: #f0fff0;
}

.chat_user {
  background-color: #f0f0ff;
}
</style>"""
)
