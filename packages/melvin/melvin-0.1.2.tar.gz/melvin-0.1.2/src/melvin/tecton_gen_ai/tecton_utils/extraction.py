import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict
from tecton import (
    BatchFeatureView,
    DataSource,
    Entity,
    Secret,
    batch_feature_view,
    resource_provider,
)
from tecton.framework.data_source import FilteredSource

from ..utils.config_utils import Configs
from ..utils.config_wrapper import to_json_config, from_json_config
from ._internal import assert_param_not_null_or_get_from_mock, set_serialization
from ..utils.structured_outputs import _DEFAULT_LOCAL_CONCURRENCY, BatchProcessor


class LlmExtractionConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    column: str
    processor: BatchProcessor
    local_concurrency: int = _DEFAULT_LOCAL_CONCURRENCY
    enable_local_cache: bool = False

    @staticmethod
    def parse(
        obj: Union[Dict[str, Any], "LlmExtractionConfig"],
    ) -> "LlmExtractionConfig":
        if isinstance(obj, dict):
            obj = obj.copy()
            model = obj.pop("model", Configs.get_default().llm)
            schema = obj.pop("schema")
            processor = BatchProcessor.make(model, schema)
            obj["processor"] = processor
            return LlmExtractionConfig.model_validate(obj)
        return obj

    # TODO: replace with __json_config_dict__
    def to_json_str(self) -> str:
        data = {
            "processor": to_json_config(self.processor),
            "column": self.column,
            "local_concurrency": self.local_concurrency,
            "enable_local_cache": self.enable_local_cache,
        }
        return json.dumps(data)

    @staticmethod
    def from_json_str(json_str: str) -> "LlmExtractionConfig":
        data = json.loads(json_str)
        processor = from_json_config(data["processor"])
        return LlmExtractionConfig(
            processor=processor,
            column=data["column"],
            local_concurrency=data["local_concurrency"],
            enable_local_cache=data["enable_local_cache"],
        )


def llm_extraction(
    source: Union[DataSource, FilteredSource],
    extraction_config: List[Union[LlmExtractionConfig, Dict[str, Any]]],
    entities: List[Entity],
    feature_start_time: Optional[datetime] = None,
    batch_schedule: timedelta = timedelta(days=1),
    timestamp_field: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    online: bool = True,
    offline: bool = True,
    secrets: Optional[Dict[str, Secret]] = None,
    **fv_kwargs: Any,
) -> BatchFeatureView:
    """
    Run LLM Feature Extraction on a Tecton data source and output to a batch feature view.
    This function will create an ingestion pipeline to call LLM transformations
    to extract structured data from a text column according to the provided schema.

    Args:

        source: The data source
        extraction_config: The LLM extraction configuration
        feature_start_time: The feature start time, defaults to None.
            When None, it requires the source to be a mock source created for testing purpose.
        batch_schedule: The batch schedule, defaults to timedelta(days=1)
        timestamp_field: The timestamp field, defaults to None.
            When None, it requires the source to be a mock source created for testing purpose.
        name: The name of the knowledge base, defaults to None.
            When None, it will use the name of the source.
        description: The description of the knowledge base, defaults to None.
            When None, it will use the description of the source.
        fv_kwargs: Additional kwargs to pass to the batch feature view decorator

    Returns: The batch feature view containing the output

    """

    # TODO: refactor this configuration resolution to be shared with
    # logic for `source_as_knowledge`
    feature_start_time = assert_param_not_null_or_get_from_mock(
        feature_start_time, source, "start_time"
    )
    timestamp_field = assert_param_not_null_or_get_from_mock(
        timestamp_field, source, "timestamp_field"
    )
    if name is None:
        if isinstance(source, FilteredSource):
            name = source.source.name
        else:
            name = source.name
    if name is None or name == "":
        raise ValueError("name is required")
    if description is None:
        if isinstance(source, FilteredSource):
            description = source.source.description
        else:
            description = source.description

    if len(extraction_config) == 0:
        raise ValueError("extraction_config is required")

    configs = [LlmExtractionConfig.parse(config) for config in extraction_config]
    config_json_arr = [x.to_json_str() for x in configs]
    features = {}
    for config in configs:
        for attr in config.processor.get_tecton_fields(as_attributes=True):
            if attr.name in features:
                raise ValueError(f"Duplicate feature name: {attr.name}")
            features[attr.name] = attr

    resource_kwargs = dict(
        name=name + "_batch_resource",
        description=description,
    )
    if secrets is not None:
        resource_kwargs["secrets"] = secrets
    resource_kwargs = Configs.get_default().base_config | resource_kwargs

    kwargs = dict(
        name=name + "_batch",
        sources=[source],
        entities=entities,
        mode="pandas",
        features=fv_kwargs.get("features", list(features.values())),
        feature_start_time=feature_start_time,
        batch_schedule=batch_schedule,
        timestamp_field=timestamp_field,
        description=description,
        online=online,
        offline=offline,
    )
    if secrets is not None:
        kwargs["secrets"] = secrets
    bfv_kwargs = Configs.get_default().get_bfv_config() | fv_kwargs | kwargs

    def extract(bs, context):
        import pandas as pd

        _configs = context.resources["configs"]
        dfs = [bs.drop(columns=[conf.column for conf in _configs])]
        for conf in _configs:
            dicts = conf.processor.batch_process(
                bs[conf.column],
                concurrency=conf.local_concurrency,
                enable_cache=conf.enable_local_cache,
            )
            dfs.append(pd.DataFrame(dicts))
        return pd.concat(dfs, axis=1)

    with set_serialization():

        @resource_provider(**resource_kwargs)
        def _resource_provider(context=None):
            from ..tecton_utils.extraction import LlmExtractionConfig
            from ..utils.runtime import runtime_context

            with runtime_context({}, tecton_context=context):
                return [
                    LlmExtractionConfig.from_json_str(conf) for conf in config_json_arr
                ]

        @batch_feature_view(
            **bfv_kwargs, resource_providers={"configs": _resource_provider}
        )
        def batch_fv(bs, context):
            return extract(bs, context)

    return batch_fv
