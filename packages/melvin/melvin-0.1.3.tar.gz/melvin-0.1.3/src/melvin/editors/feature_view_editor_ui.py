import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class AggregationParam:
    name: str
    value: Any


@dataclass
class Aggregation:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    column: str = ""
    function: str = ""
    timeWindow: str = "timedelta(days=1)"
    params: Dict[str, Any] = field(default_factory=dict)
    name: str = ""


@dataclass
class SchemaField:
    name: str
    type: str


@dataclass
class FeatureEditorState:
    # Basic configuration
    data_source: str = ""
    entity_key: str = ""
    timestamp_field: str = ""
    feature_start_time: Optional[datetime] = None
    feature_name: str = ""

    # Schema information
    current_schema: List[SchemaField] = field(default_factory=list)
    show_schema: bool = False

    # Source type information
    is_streaming_mode: bool = False

    # UI navigation
    step: int = 1

    # Aggregations
    aggregations: List[Aggregation] = field(default_factory=list)

    # Advanced options
    is_continuous_mode: bool = True
    is_compaction_enabled: bool = False
    is_stream_tiling_enabled: bool = False
    leading_edge_type: str = "WALL_CLOCK_TIME"
    transformation_type: str = ""

    result_apply: bool = False
    result_cancel: bool = False
    session_object_key: str = None

    def to_dict(self) -> dict:
        """
        Builds a feature configuration dictionary from this editor state.

        Returns:
            Dict containing the complete feature configuration
        """
        return {
            "data_source": self.data_source,
            "entity_key": self.entity_key,
            "timestamp_field": self.timestamp_field,
            "feature_start_time": self.feature_start_time.isoformat() if self.feature_start_time else None,
            "transformation_type": self.transformation_type,
            "aggregations": [
                {
                    "id": agg.id,
                    "column": agg.column,
                    "function": agg.function,
                    "timeWindow": agg.timeWindow,
                    "params": agg.params,
                    "name": agg.name
                } for agg in self.aggregations
            ],
            "advanced_options": {
                "is_streaming_mode": self.is_streaming_mode,
                "is_continuous_mode": self.is_continuous_mode,
                "is_compaction_enabled": self.is_compaction_enabled,
                "is_stream_tiling_enabled": self.is_stream_tiling_enabled,
                "leading_edge_type": self.leading_edge_type
            }
        }

    def is_completed(self) -> bool:
        return self.result_apply or self.result_cancel


def display_editor(state: FeatureEditorState, key_prefix="tecton_editor", compute_type="spark", on_ship_it=None):
    """
    Displays a compact embeddable Tecton Feature Creator within a Streamlit container.

    Parameters:
    -----------
    state : FeatureEditorState
        Dataclass instance that stores all the state for the editor
    key_prefix : str
        Prefix for all keys to avoid conflicts with the parent app
    compute_type : str
        The compute engine type (spark, rift, etc.)
    """
    # Create a container to isolate the editor
    editor_container = st.container()

    with editor_container:
        # Apply scoped CSS that only affects elements within this container
        css = f"""
        <style>
            /* Target only elements within our specific container */
            [data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMarkdownContainer"] > p:contains("{key_prefix}")) ~ div {{
                /* More compact elements */
                .stButton button {{padding: 0.15rem 0.4rem !important; font-size: 0.75rem !important; min-height: 0 !important;}}
                .stExpander {{border: none !important; box-shadow: none !important;}}
                div[data-testid="stExpander"] div[role="button"] p {{font-size: 0.9rem; font-weight: 600;}}
                .stTab {{font-size: 0.8rem;}}
                .streamlit-expanderHeader {{font-weight: 600; font-size: 0.9rem;}}
                .stAlert {{padding: 0.2rem !important; margin-bottom: 0.3rem !important;}}
                div[data-testid="stAlert"] > div > div > div {{font-size: 0.8rem; padding: 0.3rem !important;}}

                /* Reduce whitespace */
                .main .block-container {{padding: 0.3rem !important;}}
                .stMarkdown p {{margin-bottom: 0.15rem !important; line-height: 1.3 !important; font-size: 0.85rem !important;}}
                h1 {{font-size: 1rem !important; margin: 0.2rem 0 !important;}}
                h2 {{font-size: 0.9rem !important; margin: 0.2rem 0 !important;}}
                h3 {{font-size: 0.85rem !important; margin: 0.1rem 0 !important;}}
                h4 {{font-size: 0.8rem !important; margin: 0.1rem 0 !important;}}
                h5 {{font-size: 0.75rem !important; margin: 0.1rem 0 !important;}}

                /* Structure elements */
                .section-header {{border-bottom: 1px solid #eee; padding-bottom: 0.1rem; margin-bottom: 0.3rem;}}
                .schema-container {{background-color: #f0f0f0; border-radius: 4px; padding: 0.3rem; margin-top: 0.2rem;}}

                /* Ultra compact elements */
                div[data-testid="stVerticalBlock"] {{gap: 0.3rem !important;}}
                div.row-widget.stRadio > div {{gap: 0.3rem !important; flex-wrap: nowrap !important;}}
                div.row-widget.stRadio > div > label {{padding: 0.2rem 0.4rem !important; font-size: 0.75rem !important;}}
                .stTextInput input, .stNumberInput input, .stSelectbox, .stDateInput input {{
                    padding: 0.2rem !important;
                    min-height: 0 !important;
                    line-height: 1.2 !important;
                    font-size: 0.8rem !important;
                }}
                .stSelectbox > div > div {{min-height: 1.5rem !important;}}
                div.stTextArea > div > div > textarea {{
                    padding: 0.2rem !important;
                    min-height: 70px !important;
                    font-size: 0.8rem !important;
                }}
                hr {{margin: 0.3rem 0 !important;}}
            }}

            /* Hide fullscreen button */
            [data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMarkdownContainer"] > p:contains("{key_prefix}")) ~ div button[title="View fullscreen"] {{
                display: none;
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

        # Add a hidden marker to target our container with CSS
        st.markdown(f'<p style="display:none">{key_prefix}</p>', unsafe_allow_html=True)

        # Mock data sources with schemas
        dataSources = [
            {
                "name": "transactions_stream",
                "type": "stream",
                "subType": "kinesis",
                "schema": [
                    {"name": "user_id", "type": "String"},
                    {"name": "transaction_id", "type": "String"},
                    {"name": "merchant_id", "type": "String"},
                    {"name": "amount", "type": "Float64"},
                    {"name": "timestamp", "type": "Timestamp"},
                    {"name": "is_fraud", "type": "Bool"}
                ]
            },
            {
                "name": "user_events",
                "type": "stream",
                "subType": "kafka",
                "schema": [
                    {"name": "user_id", "type": "String"},
                    {"name": "event_type", "type": "String"},
                    {"name": "session_id", "type": "String"},
                    {"name": "device_type", "type": "String"},
                    {"name": "country", "type": "String"},
                    {"name": "timestamp", "type": "Timestamp"}
                ]
            },
            {
                "name": "customer_transactions",
                "type": "batch",
                "schema": [
                    {"name": "customer_id", "type": "String"},
                    {"name": "transaction_id", "type": "String"},
                    {"name": "amount", "type": "Float64"},
                    {"name": "category", "type": "String"},
                    {"name": "timestamp", "type": "Timestamp"}
                ]
            }
        ]

        # Aggregation functions
        aggregationFunctions = [
            {
                "name": "approx_count_distinct",
                "params": [{"name": "precision", "type": "number", "default": 8, "min": 4, "max": 16}],
                "supportedTypes": ["String", "Int32", "Int64"],
                "description": "Returns approximate number of distinct values"
            },
            {
                "name": "approx_percentile",
                "params": [
                    {"name": "percentile", "type": "number", "default": 0.5, "min": 0, "max": 1},
                    {"name": "precision", "type": "number", "default": 100, "min": 20, "max": 500}
                ],
                "supportedTypes": ["Float32", "Float64", "Int32", "Int64"],
                "description": "Returns approximate percentile value"
            },
            {
                "name": "count",
                "params": [],
                "supportedTypes": ["all"],
                "description": "Counts rows in a time window"
            },
            {
                "name": "first_distinct",
                "params": [{"name": "n", "type": "number", "default": 1, "min": 1, "max": 1000}],
                "supportedTypes": ["String", "Int64"],
                "description": "First N distinct values in time window"
            },
            {
                "name": "first",
                "params": [{"name": "n", "type": "number", "default": 1, "min": 1, "max": 1000}],
                "supportedTypes": ["String", "Int64", "Float32", "Float64", "Bool", "Array"],
                "description": "First N values in time window"
            },
            {
                "name": "last_distinct",
                "params": [{"name": "n", "type": "number", "default": 1, "min": 1, "max": 1000}],
                "supportedTypes": ["String", "Int64"],
                "description": "Last N distinct values in time window"
            },
            {
                "name": "last",
                "params": [{"name": "n", "type": "number", "default": 1, "min": 1, "max": 1000}],
                "supportedTypes": ["Int64", "Int32", "Float64", "Bool", "String", "Array"],
                "description": "Last value(s) in time window"
            },
            {
                "name": "max",
                "params": [],
                "supportedTypes": ["Int64", "Int32", "Float64", "String"],
                "description": "Maximum value in time window"
            },
            {
                "name": "mean",
                "params": [],
                "supportedTypes": ["Int64", "Int32", "Float64"],
                "description": "Mean of values in time window"
            },
            {
                "name": "min",
                "params": [],
                "supportedTypes": ["Int64", "Int32", "Float64", "String"],
                "description": "Minimum value in time window"
            },
            {
                "name": "stddev_pop",
                "params": [],
                "supportedTypes": ["Int64", "Int32", "Float64"],
                "description": "Population standard deviation in time window"
            },
            {
                "name": "stddev_samp",
                "params": [],
                "supportedTypes": ["Int64", "Int32", "Float64"],
                "description": "Sample standard deviation in time window"
            },
            {
                "name": "sum",
                "params": [],
                "supportedTypes": ["Int64", "Int32", "Float64"],
                "description": "Sum of values in time window"
            },
            {
                "name": "var_pop",
                "params": [],
                "supportedTypes": ["Int64", "Int32", "Float64"],
                "description": "Population variance in time window"
            },
            {
                "name": "var_samp",
                "params": [],
                "supportedTypes": ["Int64", "Int32", "Float64"],
                "description": "Sample variance in time window"
            }
        ]

        # Time window options
        timeWindowOptions = [
            {"label": "1 hour", "value": "timedelta(hours=1)"},
            {"label": "1 day", "value": "timedelta(days=1)"},
            {"label": "7 days", "value": "timedelta(days=7)"},
            {"label": "30 days", "value": "timedelta(days=30)"}
        ]

        # Helper functions for state management
        def is_column_compatible(column, function_name, schema):
            func = next((f for f in aggregationFunctions if f["name"] == function_name), None)
            if not func:
                return False

            columnSchema = next((col for col in schema if col.name == column), None)
            if not columnSchema:
                return False

            return "all" in func["supportedTypes"] or columnSchema.type in func["supportedTypes"]

        def init_aggregation():
            return Aggregation()

        def add_aggregation():
            state.aggregations.append(init_aggregation())

        def remove_aggregation(idx):
            if 0 <= idx < len(state.aggregations):
                state.aggregations.pop(idx)

        def on_data_source_change(selected_source):
            if selected_source:
                source = next((s for s in dataSources if s["name"] == selected_source), None)
                if source:
                    state.current_schema = [SchemaField(name=f["name"], type=f["type"]) for f in source["schema"]]
                    state.is_streaming_mode = source["type"] == "stream"
                    state.data_source = selected_source

                    # Try to set default timestamp field
                    timestamp_fields = [f["name"] for f in source["schema"] if f["type"] == "Timestamp"]
                    if timestamp_fields:
                        state.timestamp_field = timestamp_fields[0]

                    # Reset entity key
                    state.entity_key = ""
                else:
                    state.current_schema = []
                    state.is_streaming_mode = False
                    state.data_source = ""

        def toggle_schema():
            state.show_schema = not state.show_schema

        # Function to advance to next step
        def next_step():
            state.step = state.step + 1
            print(state.step)

        # Function to go back to previous step
        def prev_step():
            state.step = state.step - 1

        # Step-based interface
        if state.step == 1:
            # Step 1: Basic Configuration
            st.markdown("#### Data Source Configuration")

            col1, col2, col3 = st.columns(3)

            with col1:
                # Data Source selection
                source_options = [(s["name"], f"{s['name']} ({s['type']})")
                                for s in dataSources]
                selected_source = st.selectbox(
                    "Data Source",
                    options=[s[0] for s in source_options],
                    format_func=lambda x: next((s[1] for s in source_options if s[0] == x), x),
                    key=f"{key_prefix}_data_source",
                    index=None if not state.data_source else [s[0] for s in source_options].index(state.data_source)
                )

                if selected_source != state.data_source:
                    on_data_source_change(selected_source)

                # Schema display with toggle
                if state.current_schema:
                    show_schema = st.checkbox("Show Schema", value=state.show_schema, key=f"{key_prefix}_schema_toggle")
                    if show_schema != state.show_schema:
                        state.show_schema = show_schema

                    if state.show_schema:
                        st.markdown('<div class="schema-container">', unsafe_allow_html=True)
                        schema_df = pd.DataFrame([(field.name, field.type) for field in state.current_schema],
                                                columns=["Field", "Type"])
                        st.dataframe(schema_df, hide_index=True, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)


                    # Entity Key
                    if state.current_schema:
                        entity_options = [field.name for field in state.current_schema if "_id" in field.name]
                        # Safely handle entity key selection
                        try:
                            index = 0 if not state.entity_key else (
                                entity_options.index(state.entity_key) + 1 if state.entity_key in entity_options else 0
                            )
                        except ValueError:
                            index = 0

                        entity_key = st.selectbox(
                            "Entity Key",
                            options=[""] + entity_options,
                            key=f"{key_prefix}_entity_key",
                            help="Column that identifies your entity (user, product, etc.)",
                            index=index
                        )
                        state.entity_key = entity_key

                    # Timestamp Field
                    if state.current_schema and state.entity_key:
                        timestamp_options = [field.name for field in state.current_schema
                                        if field.type == "Timestamp" or "time" in field.name.lower()]
                        # Safely handle timestamp field selection
                        try:
                            timestamp_index = 0
                            if state.timestamp_field and state.timestamp_field in timestamp_options:
                                timestamp_index = timestamp_options.index(state.timestamp_field) + 1
                        except ValueError:
                            timestamp_index = 0

                        timestamp_field = st.selectbox(
                            "Timestamp Field",
                            options=[""] + timestamp_options,
                            key=f"{key_prefix}_timestamp_field",
                            help="Column containing event timestamps",
                            index=timestamp_index
                        )
                        state.timestamp_field = timestamp_field

                    # Feature Start Time
                    if state.entity_key and state.timestamp_field:
                        feature_start_time = st.date_input(
                            "Feature Start Time",
                            value=state.feature_start_time or datetime(datetime.now().year, 1, 1),
                            key=f"{key_prefix}_feature_start_time",
                            help="When to start collecting feature data"
                        )
                        state.feature_start_time = feature_start_time

                # Next button
                if state.data_source and state.entity_key and state.timestamp_field:
                    st.button("Next: Add Aggregations →", on_click=next_step, use_container_width=True)
                else:
                    if not state.data_source:
                        st.info("Please select a data source to continue")
                    elif not state.entity_key:
                        st.info("Please select an entity key to continue")
                    elif not state.timestamp_field:
                        st.info("Please select a timestamp field to continue")

        elif state.step == 2:
            # Display data source info from previous step
            st.markdown("#### Selected Data Source")
            st.markdown(f"**Source:** {state.data_source}")

            if state.current_schema:
                st.markdown("**Schema:**")
                schema_df = pd.DataFrame([(field.name, field.type) for field in state.current_schema],
                                        columns=["Field", "Type"])
                st.dataframe(schema_df, hide_index=True, use_container_width=True)

            # Step 2: Aggregations
            st.markdown("#### Aggregations")
            if not state.aggregations:
                st.info("No aggregations added yet. Click 'Add Aggregation' to get started.")

            # Aggregation display
            for idx, agg in enumerate(state.aggregations):
                # Column, Function, and Time Window in one row
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

                with col1:
                    if state.current_schema:
                        column_options = [field.name for field in state.current_schema]
                        # Safely handle column selection with fallback if column not in options
                        try:
                            index = 0 if not agg.column else (
                                column_options.index(agg.column) + 1 if agg.column in column_options else 0
                            )
                        except ValueError:
                            index = 0

                        selected_column = st.selectbox(
                            "Column",
                            options=[""] + column_options,
                            key=f"{key_prefix}_agg_{idx}_column",
                            index=index
                        )
                        agg.column = selected_column

                with col2:
                    if agg.column:
                        function_options = [f["name"] for f in aggregationFunctions]
                        def function_display(x):
                            if x and not is_column_compatible(agg.column, x, state.current_schema):
                                return f"{x} (incompatible)"
                            return x

                        # Safely handle function selection with fallback if function not in options
                        try:
                            index = 0 if not agg.function else (
                                function_options.index(agg.function) + 1 if agg.function in function_options else 0
                            )
                        except ValueError:
                            index = 0

                        selected_function = st.selectbox(
                            "Function",
                            options=[""] + function_options,
                            format_func=function_display,
                            key=f"{key_prefix}_agg_{idx}_function",
                            index=index
                        )
                        agg.function = selected_function

                # Function parameters if any
                if agg.function:
                    selected_function_obj = next((f for f in aggregationFunctions if f["name"] == agg.function), None)
                    if selected_function_obj and selected_function_obj["params"]:
                        param_cols = st.columns(len(selected_function_obj["params"]))

                        for i, param in enumerate(selected_function_obj["params"]):
                            with param_cols[i]:
                                param_name = param["name"]
                                if param_name not in agg.params:
                                    agg.params[param_name] = param["default"]

                                if param["name"] == "percentile":
                                    value = st.number_input(
                                        param["name"],
                                        min_value=float(param["min"]),
                                        max_value=float(param["max"]),
                                        value=float(agg.params[param_name]),
                                        step=0.01,
                                        key=f"{key_prefix}_agg_{idx}_param_{param_name}",
                                        format="%.2f"
                                    )
                                else:
                                    value = st.number_input(
                                        param["name"],
                                        min_value=int(param["min"]),
                                        max_value=int(param["max"]),
                                        value=int(agg.params[param_name]),
                                        step=1,
                                        key=f"{key_prefix}_agg_{idx}_param_{param_name}",
                                        format="%d"
                                    )
                                agg.params[param_name] = value

                with col3:
                    window_options = [opt["value"] for opt in timeWindowOptions]
                    def window_format_func(x):
                        return next((opt["label"] for opt in timeWindowOptions if opt["value"] == x), x)

                    if agg.function:
                        # Safely handle time window selection
                        try:
                            index = window_options.index(agg.timeWindow) if agg.timeWindow in window_options else 0
                        except ValueError:
                            index = 0

                        selected_window = st.selectbox(
                            "Time Window",
                            options=window_options,
                            format_func=window_format_func,
                            key=f"{key_prefix}_agg_{idx}_timeWindow",
                            index=index
                        )
                        agg.timeWindow = selected_window

                with col4:
                    st.write("")
                    st.write("")
                    st.button("X", key=f"{key_prefix}_remove_agg_{idx}",
                             on_click=lambda i=idx: remove_aggregation(i),
                             use_container_width=True,
                             help="Remove this aggregation")

                # Add a separator between aggregations
                if idx < len(state.aggregations) - 1:
                    st.markdown("---")

            has_valid_aggs = any(agg.column and agg.function for agg in state.aggregations) if state.aggregations else False

            cols = st.columns([1, 1, 1, 1])
            with cols[0]:
                st.button("← Back", on_click=prev_step, key=f"{key_prefix}_back_to_basic", use_container_width=True)
            with cols[1]:
                st.button("Add Aggregation", on_click=add_aggregation, key=f"{key_prefix}_add_aggregation_button",
                        help="Add a new aggregation to your feature", use_container_width=True)
            with cols[2]:
                st.button("Pro Mode 🦸", on_click=next_step, key=f"{key_prefix}_pro_mode", use_container_width=True, disabled=not has_valid_aggs)
            with cols[3]:
                st.button("Ship it 🚢", key=f"{key_prefix}_ship_it", use_container_width=True, disabled=not has_valid_aggs, on_click=on_ship_it)

        elif state.step == 3:
            # Step 3: Advanced Options
            st.markdown("#### Advanced Options")

            if state.is_streaming_mode:
                cols = st.columns(2)
                with cols[0]:
                    leading_edge_type = st.radio(
                        "Leading Edge Type",
                        options=["WALL_CLOCK_TIME", "LATEST_EVENT_TIME"],
                        horizontal=True,
                        key=f"{key_prefix}_leading_edge_type",
                        index=0 if state.leading_edge_type == "WALL_CLOCK_TIME" else 1,
                        help="Controls how aggregation windows are defined"
                    )
                    state.leading_edge_type = leading_edge_type

                with cols[1]:
                    if compute_type == "rift":
                        state.is_continuous_mode = True
                        st.radio(
                            "Processing Mode",
                            options=["Continuous", "Time Interval"],
                            horizontal=True,
                            index=0,
                            disabled=True,
                            key=f"{key_prefix}_processing_mode_display"
                        )
                        st.caption("Rift only supports continuous mode")
                    else:
                        continuous_mode = st.radio(
                            "Processing Mode",
                            options=["Continuous", "Time Interval"],
                            horizontal=True,
                            index=0 if state.is_continuous_mode else 1,
                            key=f"{key_prefix}_processing_mode"
                        )
                        state.is_continuous_mode = (continuous_mode == "Continuous")

            # Compaction options
            is_compaction_enabled = st.checkbox(
                "Enable Compaction",
                value=state.is_compaction_enabled,
                key=f"{key_prefix}_is_compaction_enabled",
                help="Improves performance for long windows"
            )
            state.is_compaction_enabled = is_compaction_enabled

            # Stream Tiling (only for stream + compaction)
            if state.is_streaming_mode and is_compaction_enabled:
                is_stream_tiling = st.checkbox(
                    "Enable Stream Tiling",
                    value=state.is_stream_tiling_enabled,
                    key=f"{key_prefix}_is_stream_tiling_enabled",
                    help="Pre-aggregates streaming data for better performance"
                )
                state.is_stream_tiling_enabled = is_stream_tiling

            cols = st.columns([1, 3])
            with cols[0]:
                st.button("← Back", on_click=prev_step, key=f"{key_prefix}_back_to_aggs", use_container_width=True)
            with cols[1]:
                st.button("Let me see it!", on_click=next_step, use_container_width=True)

        elif state.step == 4:
            # Step 4: Completion
            # Create feature configuration JSON
            feature_config = state.to_dict()

            # Display JSON configuration
            st.markdown("##### Feature Configuration")
            st.json(feature_config)

            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                st.button("← Back", on_click=prev_step, key=f"{key_prefix}_back_to_aggs", use_container_width=True)
            with col2:
                st.button("Ship it 🚢", key=f"{key_prefix}_ship_it", on_click=on_ship_it)


# Example of usage in your existing app:
#
# import streamlit as st
# from feature_editor import display_editor, FeatureEditorState
#
# st.set_page_config(page_title="My Main App")
# st.title("My Main Application")
#
# # Create the state instance
# editor_state = FeatureEditorState()
#
# # Embed the compact Feature Creator
# with st.expander("Create Feature"):
#     display_editor(
#         state=editor_state,
#         key_prefix="embedded_editor",
#         compute_type="spark"
#     )
