import importlib
import json
from datetime import datetime
from functools import lru_cache
from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from typing_extensions import ParamSpec

from .runtime import RuntimeVar

T = TypeVar("T")
P = ParamSpec("P")

_TECTON_OBJECT_KEY = "__tecton_config_object__"


def as_config(object_type: Callable[P, T]) -> Callable[P, Any]:
    class _Wrapper(ConfigWrapper[object_type]):
        pass

    return _Wrapper


def to_json_config(obj: Any) -> str:
    if isinstance(obj, dict):
        obj = _DictConfig(**obj)
    tf = _EncodeTraverser()
    return json.dumps(tf(obj))


def from_json_config(
    json_str: str,
    external_kwargs: Optional[Dict[str, Any]] = None,
    use_cache: bool = True,
) -> Any:
    if use_cache:
        res = _from_json_config(json_str, json.dumps(external_kwargs))
    res = ConfigWrapper.from_json(json_str).instantiate(external_kwargs)
    if isinstance(res, _DictConfig):
        return res._kwargs
    return res


@lru_cache
def _from_json_config(json_str: str, kwargs: str) -> Any:
    return ConfigWrapper.from_json(json_str).instantiate(json.loads(kwargs))


class ExternalArgument(BaseModel):
    name: str


class ConfigWrapper(Generic[T]):
    def __init__(self, **kwargs: Any):
        self._kwargs = kwargs

    @property
    def target_type(self) -> Type[T]:
        return self.__class__.__orig_bases__[0].__args__[0]

    def instantiate(self, external_kwargs: Optional[Dict[str, Any]] = None) -> T:
        tf = _InitTraverser(external_kwargs)
        return self.target_type(**tf(self._kwargs))

    def to_json(self) -> str:
        return to_json_config(self)

    @staticmethod
    def from_json(json_str: str) -> "ConfigWrapper":
        tf = _DecodeTraverser()
        obj = tf(json.loads(json_str))
        if not isinstance(obj, ConfigWrapper):
            raise ValueError("Expected ObjectConfig object")
        return obj


class _DictConfig(ConfigWrapper[dict]):
    pass


class _Traverser:
    def __call__(self, obj: Any) -> Any:
        if isinstance(obj, list):
            return [self(o) for o in obj]
        if isinstance(obj, tuple):
            return tuple(self(o) for o in obj)
        if isinstance(obj, dict):
            return {self(k): self(v) for k, v in obj.items()}
        return obj


class _InitTraverser(_Traverser):
    def __call__(self, obj: Any) -> Any:
        if isinstance(obj, ConfigWrapper):
            return obj.instantiate(self._external_kwargs)
        if isinstance(obj, ExternalArgument):
            return self._external_kwargs[obj.name]
        if isinstance(obj, RuntimeVar):
            return obj.get()
        return super().__call__(obj)

    def __init__(self, external_kwargs: Optional[Dict[str, Any]]):
        self._external_kwargs = external_kwargs or {}


class _EncodeTraverser(_Traverser):
    def __call__(self, obj: Any) -> Any:
        if isinstance(obj, ExternalArgument):
            return {_TECTON_OBJECT_KEY: "arg", "name": obj.name}
        if isinstance(obj, RuntimeVar):
            return {
                _TECTON_OBJECT_KEY: "context_var",
                "name": obj.name,
                "sources": obj.sources,
            }
        if hasattr(obj, "__json_config_dict__"):
            obj = as_config(obj.__class__)(**obj.__json_config_dict__())
        if isinstance(obj, ConfigWrapper):
            data = {_TECTON_OBJECT_KEY: "conf"}
            data.update(self(obj._kwargs))
            data[_TECTON_OBJECT_KEY + "type"] = _type_to_str(obj.target_type)
            return data
        if isinstance(obj, datetime):
            return {_TECTON_OBJECT_KEY: "ts", "value": obj.isoformat()}
        return super().__call__(obj)


class _DecodeTraverser(_Traverser):
    def __call__(self, obj: Any) -> Any:
        if isinstance(obj, dict) and _TECTON_OBJECT_KEY in obj:
            params = obj.copy()
            otype = params.pop(_TECTON_OBJECT_KEY)
            if otype == "arg":
                return ExternalArgument(name=params["name"])
            if otype == "context_var":
                return RuntimeVar(name=params["name"], sources=params["sources"])
            if otype == "conf":
                tp = _str_to_type(params.pop(_TECTON_OBJECT_KEY + "type"))
                return as_config(tp)(**self(params))
            if otype == "ts":
                return datetime.fromisoformat(params["value"])
            raise ValueError(f"Unknown object type {otype}")
        return super().__call__(obj)


def _type_to_str(tp: Type) -> str:
    return f"{tp.__module__}.{tp.__qualname__}"


def _str_to_type(s: str) -> Type:
    parts = s.split(".")
    mod = ".".join(parts[:-1])
    obj = parts[-1]
    
    # Fix for relative imports - if it's a tecton_gen_ai module, ensure it has the right prefix
    if "tecton_gen_ai" in mod:
        # Remove src. prefix if it exists (for backward compatibility)
        if mod.startswith("src."):
            mod = mod[4:]  # Remove 'src.'
        # Ensure it starts with 'melvin.'
        if not mod.startswith("melvin."):
            mod = f"melvin.{mod}"
        
    return getattr(importlib.import_module(mod), obj)
