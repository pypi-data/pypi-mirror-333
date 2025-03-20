from datetime import timedelta
from typing import Any, List, Optional, Union

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
from tecton import (
    BatchFeatureView,
    BatchSource,
    Entity,
    PushConfig,
    RealtimeFeatureView,
    RequestSource,
    StreamFeatureView,
    StreamSource,
    batch_feature_view,
    pandas_batch_config,
    realtime_feature_view,
    stream_feature_view,
)
from tecton.types import Field

from ..tecton_utils._internal import (
    get_local_source_attrs,
    set_local_source_attrs,
    set_serialization,
)
from ..utils.config_utils import Configs
from ..tecton_utils._tecton_utils import get_df_schema

_MAX_ROWS = 100
_DEFAULT_TIMESTAMP_FIELD = "_tecton_auto_ts"
_DEFAULT_SOURCE_TIME = "2024-01-01"


def make_local_source(
    name: str,
    raw: Any,
    auto_timestamp: bool = True,
    timestamp_field: Optional[str] = None,
    max_rows: Optional[int] = None,
    is_stream: bool = False,
    **source_kwargs: Any,
) -> Union[BatchSource, StreamSource]:
    """
    Make a local Tecton DataSource from raw data.

    Args:

        name: The name of the source.
        raw: The raw data, can be a pandas DataFrame, a dictionary, or a list of dictionaries.
        auto_timestamp: Whether to automatically add a timestamp field to the data when timestamp_field is None,
            defaults to True.
        timestamp_field: The timestamp field, defaults to None (no timestamp field).
        max_rows: The maximum number of rows allowed in the data, defaults to 100.
        is_stream: Whether the returned source is a stream source, defaults to False.
        **source_kwargs: Other keyword arguments for defining the source.

    Returns:

        A Tecton DataSource.

    Notes:

        - The purpose of this function is to create a local Tecton DataSource for testing and local iteration.
        - It's also deployable to a Tecton cluster. However, it is still for testing purposes only.

    Examples:

        ```python
        from tecton_gen_ai.testing import make_local_source
        import pandas as pd

        # simplest form
        my_src1 = make_local_source(
            name="my_src1",
            raw={"user_id": [1, 2]}),
            description="User information",
        )

        # with a list of dictionaries
        data = [
            {"user_id": 1, "event_time": "2024-01-01T00:00:00", "event_type": "click"},
            {"user_id": 2, "event_time": "2024-01-01T00:00:01", "event_type": "click"},
        ]
        my_src2 = make_local_source(
            name="my_src2",
            raw=data,
            timestamp_field="event_time",
            description="User information",
        )

        # with a pandas DataFrame
        df = pd.DataFrame(data)
        my_src3 = make_local_source(
            name="my_src3",
            raw=df,
            timestamp_field="event_time",
            description="User information",
        )
        ```
    """
    df = _to_df(raw)
    _max_row = max_rows or _MAX_ROWS
    if len(df) > _max_row:
        raise ValueError(f"Dataframe has more than {_max_row} rows")

    if timestamp_field is None and auto_timestamp:
        timestamp_field: Optional[str] = _DEFAULT_TIMESTAMP_FIELD
        df = df.assign(**{timestamp_field: _DEFAULT_SOURCE_TIME})
    if timestamp_field is not None:
        df = df.assign(**{timestamp_field: pd.to_datetime(df[timestamp_field])})

    normalized_cols = {}
    ts_fields = []
    for col in df.columns:
        cv = df[col]
        if is_datetime64_any_dtype(cv):
            cv = cv.astype(str)
            ts_fields.append(col)
        normalized_cols[col] = cv

    data = pd.DataFrame(normalized_cols).to_dict("records")

    with set_serialization():

        @pandas_batch_config(supports_time_filtering=True)
        def api_df(filter_context):
            import pandas as pd

            df = pd.DataFrame(data)
            for f in ts_fields:
                df[f] = pd.to_datetime(df[f])
            return df

    if not is_stream:
        src = BatchSource(name=name, batch_config=api_df, **source_kwargs)
    else:
        src = StreamSource(
            name=name,
            stream_config=PushConfig(),
            batch_config=api_df,
            schema=get_df_schema(df),
            **source_kwargs,
        )

    mock_params = {
        "timestamp_field": timestamp_field,
    }
    if timestamp_field is not None:
        mock_params["start_time"] = df[timestamp_field].min().to_pydatetime()
        mock_params["end_time"] = df[timestamp_field].max().to_pydatetime() + timedelta(
            days=1
        )
    set_local_source_attrs(src, mock_params)
    return src


def make_local_batch_feature_view(
    name: str,
    data: Any,
    entity_keys: List[str],
    timestamp_field: Optional[str] = None,
    max_rows: Optional[int] = None,
    **fv_kwargs: Any,
) -> BatchFeatureView:
    """
    Make a local Tecton BatchFeatureView from raw data. Under the hood, it will call `make_local_source`
    to create a local source.

    Args:

        name: The name of the feature view.
        data: The raw data, can be a pandas DataFrame, a dictionary, or a list of dictionaries.
        entity_keys: The entity keys for dedup and lookup.
        timestamp_field: The timestamp field, defaults to None (will add timestamp field automatically).
        max_rows: The maximum number of rows allowed in the data, defaults to None.
        **fv_kwargs: Other keyword arguments for defining the feature view.

    Returns:

        A Tecton BatchFeatureView.

    Notes:

        - The purpose of this function is to create a local Tecton BatchFeatureView for testing and local iteration.
        - It's also deployable to a Tecton cluster. However, it is still for testing purposes only.
        - Adding description to the feature view is strongly recommended (for LLMs to understand the feature view).

    Examples:

        ```python
        from tecton_gen_ai.testing import make_local_batch_feature_view

        # simplest form
        my_fv1 = make_local_batch_feature_view(
            "my_fv1",
            {"user_id": 1, "name": "Jim"},
            ["user_id"],
            "description": "User information",
        )

        # with a list of dictionaries
        data = [
            {"user_id": 1, "name": "Jim"},
            {"user_id": 2, "name": "John"},
        ]
        my_fv2 = make_local_batch_feature_view(
            "my_fv2", data, ["user_id"],
            description="User information",
        )

        # with a pandas DataFrame
        import pandas as pd

        df = pd.DataFrame(data)
        my_fv3 = make_local_batch_feature_view(
            "my_fv3", df, ["user_id"],
            description="User information",
        )
        ```
    """
    df = _to_df(data)
    source = make_local_source(
        name + "_source",
        df,
        max_rows=max_rows,
        timestamp_field=timestamp_field,
        auto_timestamp=True,
    )
    timestamp_field = get_local_source_attrs(source)["timestamp_field"]
    start = get_local_source_attrs(source)["start_time"]
    schema = get_df_schema(df, as_attributes=True)
    join_keys = [Field(x.name, x.dtype) for x in schema if x.name in entity_keys]
    if len(join_keys) != len(entity_keys):
        raise ValueError(f"Entity keys {entity_keys} not all found in schema {schema}")
    entity = Entity(name=name + "_entity", join_keys=join_keys)
    features = fv_kwargs.get(
        "features",
        [x for x in schema if x.name not in entity_keys and x.name != timestamp_field],
    )

    base_args = dict(
        name=name,
        sources=[source],
        entities=[entity],
        mode="pandas",
        online=True,
        offline=True,
        features=features,
        feature_start_time=start,
        incremental_backfills=False,
        batch_schedule=timedelta(days=1),
        max_backfill_interval=timedelta(days=10000),
        timestamp_field=timestamp_field,
        **Configs.get_default().get_bfv_config(),
    )
    base_args.update(fv_kwargs)

    with set_serialization():

        @batch_feature_view(**base_args)
        def dummy(_df):
            return _df

    return dummy


def make_local_realtime_feature_view(
    name: str,
    data: Any,
    entity_keys: List[str],
    **fv_kwargs: Any,
) -> RealtimeFeatureView:
    """
    Make a local Tecton RealtimeFeatureView from raw data.

    Args:

        name: The name of the feature view.
        data: The raw data, can be a pandas DataFrame, a dictionary, or a list of dictionaries.
        entity_keys: The entity keys for lookup.
        **fv_kwargs: Other keyword arguments for defining the feature view.

    Returns:

        A Tecton RealtimeFeatureView.

    Notes:

        - The purpose of this function is to create a local Tecton RealtimeFeatureView for testing and local iteration.
        - It's also deployable to a Tecton cluster. However, it is still for testing purposes only.

    Examples:

        ```python
        from tecton_gen_ai.testing import make_local_realtime_feature_view

        fv = make_local_realtime_feature_view("fv", {"user_id": "user1", "age": 30}, ["user_id"])
        events = pd.DataFrame([{"user_id": "user1"}])
        odf = fv.get_features_for_events(events).to_pandas()
        ```
    """
    df = _to_df(data)
    request_source = RequestSource(schema=get_df_schema(df[entity_keys]))
    features = fv_kwargs.get("features", get_df_schema(df, as_attributes=True))

    base_args = dict(
        name=name,
        sources=[request_source],
        mode="pandas",
        features=features,
        **Configs.get_default().get_rtfv_config(),
    )
    base_args.update(fv_kwargs)

    with set_serialization():

        @realtime_feature_view(**base_args)
        def dummy(request):
            import pandas as pd

            return pd.merge(request, df, on=entity_keys, how="inner").head(1)

    return dummy


def make_local_stream_feature_view(
    name: str,
    data: Any,
    entity_keys: List[str],
    timestamp_field: Optional[str] = None,
    max_rows: Optional[int] = None,
    **fv_kwargs: Any,
) -> StreamFeatureView:
    """
    Make a local Tecton StreamFeatureView from raw data.

    Args:

        name: The name of the feature view.
        data: The raw data, can be a pandas DataFrame, a dictionary, or a list of dictionaries.
        entity_keys: The entity keys for lookup.
        timestamp_field: The timestamp field, defaults to None (will add timestamp field automatically).
        max_rows: The maximum number of rows allowed in the data, defaults to None.
        **fv_kwargs: Other keyword arguments for defining the feature view.

    Returns:

        A Tecton StreamFeatureView.

    Notes:

        - The purpose of this function is to create a local Tecton StreamFeatureView for testing and local iteration.
        - It's also deployable to a Tecton cluster. However, it is still for testing purposes only.

    Examples:

        ```python
        from tecton_gen_ai.testing import make_local_stream_feature_view

        # simplest form
        fv = make_local_stream_feature_view("fv", {"user_id": "user1", "age": 30}, ["user_id"])

        # with a list of dictionaries
        data = [
            {"user_id": "user1", "age": 30},
            {"user_id": "user2", "age": 40},
        ]
        fv = make_local_stream_feature_view("fv", data, ["user_id"])

        # with a pandas DataFrame
        import pandas as pd

        df = pd.DataFrame(data)
        fv = make_local_stream_feature_view("fv", df, ["user_id"])
        ```
    """
    df = _to_df(data)
    source = make_local_source(
        name + "_source",
        df,
        max_rows=max_rows,
        is_stream=True,
        auto_timestamp=True,
        timestamp_field=timestamp_field,
    )
    timestamp_field = get_local_source_attrs(source)["timestamp_field"]
    start = get_local_source_attrs(source)["start_time"]
    schema = get_df_schema(df, as_attributes=True)
    join_keys = [Field(x.name, x.dtype) for x in schema if x.name in entity_keys]
    if len(join_keys) != len(entity_keys):
        raise ValueError(f"Entity keys {entity_keys} not all found in schema {schema}")
    entity = Entity(name=name + "_entity", join_keys=join_keys)
    features = fv_kwargs.get(
        "features",
        [x for x in schema if x.name not in entity_keys and x.name != timestamp_field],
    )

    base_args = dict(
        name=name,
        source=source,
        entities=[entity],
        mode="pandas",
        online=True,
        offline=True,
        features=features,
        feature_start_time=start,
        batch_schedule=timedelta(days=1),
        max_backfill_interval=timedelta(days=10000),
        timestamp_field=timestamp_field,
        **Configs.get_default().get_sfv_config(),
    )
    base_args.update(fv_kwargs)

    with set_serialization():

        @stream_feature_view(**base_args)
        def dummy(_df):
            return _df

    return dummy


def _to_df(data: Any) -> pd.DataFrame:
    if isinstance(data, pd.DataFrame):
        return data
    if isinstance(data, dict):
        return pd.DataFrame([data])
    if isinstance(data, list):
        return pd.DataFrame(data)
    raise ValueError(f"Unsupported data type {type(data)}")
