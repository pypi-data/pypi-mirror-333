import json
from typing import Any, Callable, Dict, List, Optional

import numpy as np

from ..constants import _OUTPUT_JSON_FIELD
from ..utils._serialization import to_openai_function
from ..utils.config_utils import Configs
from .base import AgentBase, ToolWrapper


class FunctionTool(ToolWrapper):
    def __init__(self, func: Callable):
        from ..tecton_utils.deco import _get_from_metastore, tool

        meta = dict(_get_from_metastore(func, lambda: tool(func)))
        if meta.get("type") != "tool":
            raise ValueError(f"Function {func} is not a tool")
        self._name = meta.pop("name")
        self.fv = meta.pop("fv")
        self._use_when = meta.pop("use_when")
        self._meta = meta

    @property
    def use_when(self) -> Optional[Callable]:
        return self._use_when

    @property
    def metastore_key(self) -> str:
        return self._name

    @property
    def tool_name(self) -> str:
        return self._name

    def make_metadata(self):
        return {**self.make_base_metadata(), **self._meta}

    def make_rtfv(self):
        return self.fv

    @classmethod
    def invoke(cls, agent: AgentBase, name: str, kwargs: Dict[str, Any]) -> Any:
        meta = agent.metastore["tools"][name]
        ctx = agent._get_context()
        ctx.update(kwargs)
        entity_args = meta.get("entity_args", [])
        llm_args = meta.get("llm_args", [])
        return agent._invoke(
            name,
            entity_args,
            llm_args,
            ctx,
            feature_type="tool",
            timeout_sec=meta["timeout_sec"],
        )


class SearchTool(FunctionTool):
    subtype: str = "search"

    @classmethod
    def invoke(cls, agent: AgentBase, name: str, kwargs: Dict[str, Any]) -> Any:
        kwargs = kwargs.copy()
        _filters = json.loads(kwargs.pop("filter", None) or "{}")
        _fctx = agent._get_context()
        _fctx.update(_filters)
        kwargs["filter"] = json.dumps(_fctx)
        return super().invoke(agent, name, kwargs)


def _transform_group_result(fv: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Transform the group result to a list of dictionaries

    Args:

        fv: a dict of single value or arrays

    Returns:

        List[Dict[str, Any]]: a list of dictionaries
    """
    cols: List[List[Any]] = [
        v.tolist() for v in fv.values() if isinstance(v, np.ndarray)
    ]
    if len(cols) == 0:
        return fv
    elif len(cols) < len(fv):
        raise ValueError("All columns must be numpy arrays or none")
    blobs = []
    keys = list(fv.keys())
    step = len(fv) // 2
    for i in range(step):
        key_name = keys[i].rsplit("_keys_", 1)[0]
        val_name = keys[i + step]
        blob = [{key_name: x, val_name: y} for x, y in zip(cols[i], cols[i + step])]
        blobs.extend(blob)
    return blobs


class FeatureViewTool(ToolWrapper):
    subtype: str = "fv"

    def __init__(
        self,
        fv: Any,
        queryable: bool,
        description: Optional[str] = None,
        use_when: Optional[Callable] = None,
        timeout: Any = None,
    ):
        if not hasattr(fv, "entities") or len(fv.entities) != 1:
            raise ValueError(f"FeatureView {fv} must have exactly one entity")
        self.description = description or fv.description
        if not self.description:
            raise ValueError(
                f"FeatureView {fv} must have a description or you "
                "should provide the description from `fv_as_tool`"
            )

        self.fv = fv
        self.queryable = queryable
        self.timeout = timeout
        self._use_when = use_when

    @property
    def use_when(self) -> Optional[Callable]:
        return self._use_when

    @property
    def metastore_key(self) -> str:
        return self.fv.name

    @property
    def tool_name(self) -> str:
        return "fv_tool_" + self.fv.name

    def make_metadata(self):
        from ..tecton_utils.deco import _get_source_names
        from ..tecton_utils._internal import entity_to_pydantic

        fv = self.fv
        # notice transformation_schema doesn't consider aggregation, so this is not the final schema
        # gettting entity schema from it is fine
        model = entity_to_pydantic(fv.entities[0], fv.transformation_schema())
        func = to_openai_function(
            model, name=self.tool_name, description=self.description
        )
        args = list(model.model_fields.keys())
        return {
            **self.make_base_metadata(),
            "queryable": self.queryable,
            "args": args,
            "function": func,
            "source_names": _get_source_names([fv]),
            "timeout_sec": Configs.get_default().get_timeout_sec(self.timeout),
        }

    def make_rtfv(self):
        from tecton import Attribute, realtime_feature_view
        from tecton.types import String

        from ..tecton_utils._internal import _REQUEST, set_serialization

        fv = self.fv
        tool_name = self.tool_name
        with set_serialization():

            @realtime_feature_view(
                name=tool_name,
                sources=[_REQUEST, fv],
                mode="python",
                features=[Attribute(_OUTPUT_JSON_FIELD, String)],
                **Configs.get_default().get_rtfv_config(),
            )
            def fv_tool(request_context, _fv) -> str:
                import json

                from ..constants import _OUTPUT_JSON_FIELD

                if tool_name != request_context["name"]:
                    return {_OUTPUT_JSON_FIELD: "{}"}
                res = _transform_group_result(_fv)
                return {_OUTPUT_JSON_FIELD: json.dumps({"result": res})}

            return fv_tool

    @classmethod
    def invoke(cls, agent: AgentBase, name: str, kwargs: Dict[str, Any]) -> Any:
        return agent.invoke_feature_view(name, kwargs)
