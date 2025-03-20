import inspect
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from pydantic import BaseModel, Field, create_model
from tecton import (
    Attribute,
    DataSource,
    Entity,
    FeatureView,
    RequestSource,
    realtime_feature_view,
)
from tecton.framework.data_source import FilteredSource
from tecton.types import Field as TectonField
from tecton.types import String

from ..constants import _OUTPUT_JSON_FIELD, _TECTON_MOCK_OBJECT_ATTR
from ..utils._extra_attrs import get_attr, has_attr, set_attr
from ..utils.config_utils import Configs
from ._tecton_utils import make_request_source, set_conf
from .convert import tecton_type_to_python_annotation

_REQUEST = make_request_source(
    name=str, input=str, session_path=str, _dummy_request_ts=datetime
)


def is_local_source(source: Any) -> bool:
    src = _get_orig_source(source)
    return has_attr(src, _TECTON_MOCK_OBJECT_ATTR)


def get_local_source_attrs(sourcre: Any) -> Dict[str, Any]:
    src = _get_orig_source(sourcre)
    return get_attr(src, _TECTON_MOCK_OBJECT_ATTR)


def set_local_source_attrs(source: Any, attrs: Dict[str, Any]) -> None:
    src = _get_orig_source(source)
    set_attr(src, _TECTON_MOCK_OBJECT_ATTR, attrs)


def _get_orig_source(source: Any) -> DataSource:
    if isinstance(source, FilteredSource):
        return source.source
    if isinstance(source, DataSource):
        return source
    raise ValueError(f"{source} is not a DataSource or FilteredSource")


class FuncWrapper:
    def __init__(
        self,
        name: str,
        func: Callable,
        sources: Optional[List[FeatureView]] = None,
        input_schema: Optional[BaseModel] = None,
        assert_entity_defined: bool = False,
    ):
        self.name = name
        self.func = func
        self.sources = sources or []
        ap = _ArgumentParser(input_schema or func, self.sources, assert_entity_defined)
        (
            self.views,
            self.llm_args,
            self.feature_args,
            self.entity_args,
            self.has_request_source,
            self.should_add_request_source,
        ) = (
            ap.views,
            ap.llm_args,
            ap.feature_args,
            ap.entitye_args,
            ap.has_request_source,
            ap.should_add_request_source,
        )

    def make_prompt(self, **rtfv_kwargs: Any) -> FeatureView:
        return self.make_feature_view(**rtfv_kwargs)

    def make_feature_view(self, **rtfv_kwargs: Any) -> FeatureView:
        name = self.name
        func = self.func
        func_name = func.__name__
        doc = func.__doc__
        has_request_source = self.has_request_source
        rtfv_kwargs = Configs.get_default().get_rtfv_config(rtfv_kwargs)
        fv_names = [fv.name for fv in self.views]
        deco = realtime_feature_view(
            name=name,
            description=doc,
            sources=[_REQUEST] + self.views,
            mode="python",
            features=[Attribute(_OUTPUT_JSON_FIELD, String)],
            context_parameter_name="context",
            **rtfv_kwargs,
        )

        def service(request_context, *fvs, context=None):
            try:
                import json

                from ..constants import _OUTPUT_JSON_FIELD
                from ..utils.runtime import runtime_context

                if name != request_context["name"]:
                    return {_OUTPUT_JSON_FIELD: "{}"}
                if has_request_source:
                    pos_args: List[Any] = [json.loads(request_context["input"])]
                    params = {}
                else:
                    pos_args: List[Any] = []
                    params = json.loads(request_context["input"])
                try:  # make tecton compiler embed this function
                    f = func  # running locally
                except Exception:  # tecton runtime can't really get this function
                    f = globals()[func_name]  # running on server
                ctx = {"tecton_request": params.copy()}
                for key, fv in zip(fv_names, fvs):
                    params[key] = fv
                with runtime_context(
                    ctx,
                    tecton_context=context,
                    session_path=request_context.get("session_path"),
                ):
                    res = f(*pos_args, **params)
                    return {_OUTPUT_JSON_FIELD: json.dumps({"result": res})}
            except Exception:
                from traceback import format_exc

                return {_OUTPUT_JSON_FIELD: json.dumps({"error": format_exc()})}

        return self._wrap(deco, service)

    def _wrap(self, deco: Any, service: Any) -> Any:
        with set_serialization():
            if len(self.views) == 0:

                def _wrapper(request_context, context=None):
                    return service(request_context, context=context)

                return deco(_wrapper)
            if len(self.views) == 1:

                def _wrapper(request_context, fv1, context=None):
                    return service(request_context, fv1, context=context)

                return deco(_wrapper)
            if len(self.views) == 2:

                def _wrapper(request_context, fv1, fv2, context=None):
                    return service(request_context, fv1, fv2, context=context)

                return deco(_wrapper)
            if len(self.views) == 3:

                def _wrapper(request_context, fv1, fv2, fv3, context=None):
                    return service(request_context, fv1, fv2, fv3, context=context)

                return deco(_wrapper)
            if len(self.views) == 4:

                def _wrapper(request_context, fv1, fv2, fv3, fv4, context=None):
                    return service(request_context, fv1, fv2, fv3, fv4, context=context)

                return deco(_wrapper)
            if len(self.views) == 5:

                def _wrapper(request_context, fv1, fv2, fv3, fv4, fv5, context=None):
                    return service(
                        request_context, fv1, fv2, fv3, fv4, fv5, context=context
                    )

                return deco(_wrapper)
        raise NotImplementedError("Too many sources")


@contextmanager
def set_serialization():
    import os
    import sys

    if "ipykernel" in sys.modules or os.environ.get("TECTON_GEN_AI_DEV_MODE") == "true":
        yield
    else:  # not in notebook
        with set_conf({"TECTON_FORCE_FUNCTION_SERIALIZATION": "true"}):
            yield


def entity_to_pydantic(entity: Entity, fields: List[TectonField]) -> BaseModel:
    schema: Dict[str, str] = {}
    _fields = {item.name: item for item in fields}
    for name in entity.join_keys:
        schema[name] = (tecton_type_to_python_annotation(_fields[name].dtype), Field())
    return create_model(entity.name, **schema, __doc__=entity.description)


class _ArgumentParser:
    def __init__(
        self,
        func: Union[Callable, Type[BaseModel]],
        sources: List[Union[RequestSource, FeatureView]],
        assert_entity_defined: bool,
    ) -> Tuple[List[str], List[str], List[str], bool]:
        self.func = func
        if inspect.isclass(func) and issubclass(func, BaseModel):
            self.orig_args = list(func.model_fields.keys())
        else:
            self.orig_args = inspect.getfullargspec(func).args
        self.has_request_source = len(sources) > 0 and isinstance(
            sources[0], RequestSource
        )
        self.views: List[FeatureView] = (
            sources if not self.has_request_source else sources[1:]
        )
        if not self.has_request_source:
            self.llm_args, self.feature_args, self.entitye_args = (
                self._parse_arguments_no_request_sourcre(
                    self.orig_args,
                    assert_entity_defined,
                    assert_all_feature_args=False,
                )
            )
            self.view = sources
        else:
            _, self.feature_args, self.entitye_args = (
                self._parse_arguments_no_request_sourcre(
                    self.orig_args[1:],
                    assert_entity_defined,
                    assert_all_feature_args=True,
                )
            )
            self.llm_args = [x.name for x in sources[0].schema]
        self.should_add_request_source = (
            not self.has_request_source and len(self.llm_args) > 0
        )

    def _parse_arguments_no_request_sourcre(
        self,
        args: List[str],
        assert_entity_defined: bool,
        assert_all_feature_args: bool,
    ) -> Tuple[List[str], List[str], List[str]]:
        func = self.func
        feature_args = [source.name for source in self.views]
        if not set(feature_args).issubset(args):
            raise ValueError(
                f"All feature view names ({feature_args}) "
                f"must be defined in {func} arguments"
            )
        if len(self.views) == 0:
            entity_args: List[str] = []
        else:
            jk = self.views[0].join_keys
            for source in self.views[1:]:
                jk += source.join_keys
                # if set(jk) != set(source.join_keys):
                #    raise ValueError("All sources must have the same join keys")
            entity_args = list(dict.fromkeys(jk))
        if assert_entity_defined:
            if not set(entity_args).issubset(args):
                raise ValueError(
                    f"All entity keys ({entity_args}) must be defined in {func}"
                )
        llm_args = [x for x in args if x not in feature_args]
        if assert_all_feature_args and len(llm_args) > 0:
            raise ValueError(
                f"Only features and request source arguments are allowed: {llm_args}"
            )
        return llm_args, feature_args, entity_args


def assert_param_not_null_or_get_from_mock(obj, source, attr_name):
    if obj is not None:
        return obj
    if is_local_source(source):
        attrs = get_local_source_attrs(source)
        if attr_name in attrs:
            return attrs[attr_name]
    raise ValueError("Value can't be None")
