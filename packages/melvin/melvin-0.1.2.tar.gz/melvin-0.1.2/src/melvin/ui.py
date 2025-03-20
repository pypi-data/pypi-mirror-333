from datetime import datetime
import streamlit as st
from agents import build_agent
from constants import MELVIN_PATH
from lib import parse_args
from utils import (
    _code,
    display,
    initialize_tecton_account_info_if_needed,
    get_tecton_account_info,
    load_object,
    set_code_container,
)
from editors.feature_view_editor_agent import display_fv_editor

from melvin.tecton_gen_ai.api import Configs
from melvin.tecton_gen_ai.testing import set_dev_mode
from melvin.tecton_gen_ai.testing.log_utils import UILogHandler, set_ui_logger
from melvin.tecton_gen_ai.utils.log import cost_monitor

# We need to do this hack because set_dev_mode below actually overrides some env vars that get_current_tecton_account_info depends on
initialize_tecton_account_info_if_needed()
print(get_tecton_account_info())

set_dev_mode()

st.set_page_config(page_title="Tecton Copilot", layout="wide")

def _print_record(record) -> bool:
    flag = getattr(record, "copilot_flag", None)
    msg = record.msg
    if flag == "log":
        st.markdown(msg)
    elif flag == "log_with_details":
        print(record)
        st.markdown(msg)
        with st.popover("Query Details"):
            st.markdown(record.details)
    elif flag == "image":
        image_html = (
            f'<img src="data:image/png;base64,{record.image_base64 }" width="800"/>'
        )
        st.markdown(image_html, unsafe_allow_html=True)
    elif flag == "error":
        if "\n" in msg:
            with st.popover("Error Details"):
                st.error(msg.replace("\n", "  \n"))
        else:
            st.error(msg.replace("\n", "  \n"))
    elif flag == "success":
        st.success(msg.replace("\n", "  \n"))
    else:
        return False
    return True


def _display_chart(chart_id):
    import plotly.io as pio

    fig = pio.from_json(load_object(chart_id))
    st.plotly_chart(fig, use_container_width=True, key=chart_id)


def _display_flowchart(diagram_json):
    import json

    from streamlit_flow import streamlit_flow
    from streamlit_flow.elements import StreamlitFlowEdge, StreamlitFlowNode
    from streamlit_flow.layouts import LayeredLayout
    from streamlit_flow.state import StreamlitFlowState

    diagram = json.loads(diagram_json.strip())
    rand_id = diagram["rand_id"]
    prefix = "x" + rand_id + "_"
    chart_id = "chart_" + rand_id

    if chart_id not in st.session_state:
        nodes = []

        input_nodes = set(edge[0] for edge in diagram["edges"])
        output_nodes = set(edge[1] for edge in diagram["edges"])
        for node, tp in zip(diagram["nodes"], diagram["types"]):
            if node in input_nodes and node not in output_nodes:
                node_type = "input"
            elif node in output_nodes and node not in input_nodes:
                node_type = "output"
            else:
                node_type = "default"
            nodes.append(
                StreamlitFlowNode(
                    id=prefix + node,
                    pos=(0, 0),
                    data={"content": f"**{node}**\n\n({tp})"},
                    node_type=node_type,
                    source_position="right",
                    target_position="left",
                    draggable=True,
                )
            )

        edges = []
        for edge in diagram["edges"]:
            edge = StreamlitFlowEdge(
                id=prefix + edge[0] + "-" + edge[1],
                source=prefix + edge[0],
                target=prefix + edge[1],
                animated=False,
                marker_end={"type": "arrow"},
            )
            edges.append(edge)

        state = StreamlitFlowState(nodes, edges)
        st.session_state[chart_id] = state
    else:
        state = st.session_state[chart_id]

    streamlit_flow(
        chart_id + "_render",
        state,
        fit_view=True,
        layout=LayeredLayout(direction="right"),
        height=300,
        show_minimap=False,
        show_controls=True,
        pan_on_drag=True,
        allow_zoom=False,
        hide_watermark=True,
    )


def _display(markdown: str, visualize: bool):
    def _show_block(type: str, code: str):
        if type == "diagram":
            if visualize:
                try:
                    _display_flowchart(code)
                except Exception as e:
                    st.code(f"Error displaying diagram: {e}")
            else:
                st.code(code, language="json")
        elif type == "chart":
            if visualize:
                try:
                    _display_chart(code.strip())
                except Exception as e:
                    st.code(f"Error displaying chart: {e}")
            else:
                st.code(code)
        elif type == "editor":
            if visualize:
                try:
                    display_fv_editor(code.strip(), st.session_state.simulate_user_prompt_fn)
                except Exception as e:
                    st.code(f"Error displaying editor: {e}")
            else:
                st.code(code)
        else:
            st.code(code)

    display(markdown, st.markdown, _show_block)


class WorkLogHandler(UILogHandler):
    def __init__(self):
        super().__init__(diagram=False)
        self.records = []

    def emit_text(self, record) -> None:
        if _print_record(record):
            self.records.append(record)


if "copilot" not in st.session_state:
    args = parse_args()
    with Configs(
        llm=args["llm"], agent_invoke_kwargs={"max_iterations": 30}
    ).update_default():
        st.session_state.copilot = build_agent()
        print("Copilot initialized")

st.image(MELVIN_PATH, width=200)
st.title("Hi, I'm Melvin! Your Tecton Co-Pilot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

chat_col, code_col = st.tabs(["Chat", "Source Code"])

with code_col:
    code_container = st.empty()
    set_code_container(code_container)

_code()

with chat_col:
    container = st.container()
    with container:
        # Display chat messages from history on app rerun
        last = len(st.session_state.messages) - 1
        last_time = None
        for i, message in enumerate(st.session_state.messages):
            avatar = MELVIN_PATH if message["role"] == "assistant" else None
            time = message["time"]
            with st.chat_message(message["role"], avatar=avatar):
                _display(message["content"], visualize=True)
                if "log" in message:
                    is_last = i == last
                    with st.expander("Actions", expanded=False):
                        for record in message["log"]:
                            _print_record(record)
                if message["role"] == "assistant":
                    response_sec = (message["time"] - last_time).total_seconds()
                    cost = message.get("cost", 0)
                    # with time, response time and cost
                    st.caption(
                        f"Time: {time:%Y-%m-%d %H:%M:%S},  Latency: {response_sec:.2f}s, Cost: ${cost:.4f}"
                    )
                else:
                    st.caption(f"Time: {time:%Y-%m-%d %H:%M:%S}")
            last_time = message["time"]


def on_submit(prompt_override: str = None):
    prompt = prompt_override or st.session_state.user_input
    chat_history = [(x["role"], x["content"]) for x in st.session_state.messages]
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "time": datetime.now()}
    )

    # Display assistant response in chat message container
    with container:
        # Display user message in chat message container
        with st.chat_message("user"):
            _display(prompt, visualize=False)
        ct = st.chat_message("assistant", avatar=MELVIN_PATH)
        with ct:
            empty = st.empty()
            with empty.container():
                with st.status("Working on it ...", expanded=True, state="running"):
                    handler = WorkLogHandler()
                    with set_ui_logger(handler) as logger:
                        with st.session_state.copilot.set_logger(logger):
                            with cost_monitor() as monitor:
                                try:
                                    response = st.session_state.copilot.invoke(
                                        prompt, chat_history=chat_history
                                    )
                                except Exception as e:
                                    response = "Error encountered: " + str(e)
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response,
                            "log": handler.records,
                            "cost": monitor.total_cost,
                            "time": datetime.now(),
                        }
                    )
            with empty.container():
                _display(response, visualize=False)

st.session_state.simulate_user_prompt_fn = on_submit

# React to user input
st.chat_input(
    "Ask anything about Tecton and your Tecton code ...",
    key="user_input",
    on_submit=on_submit,
)
