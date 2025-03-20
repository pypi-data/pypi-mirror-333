import os
import tempfile
from contextlib import contextmanager
from contextvars import ContextVar
from functools import lru_cache
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

from ..constants import _DEV_MODE_AGENT_KEY

from .io_utils import read_object, write_object

_AGENT_CONTEXT = ContextVar("agent_context", default=None)
_DEFAULT_SOURCES = ["env", "secrets", "resources"]
_ALLOWED_SOURCES = ["env", "secrets", "resources", "session", "tecton", "request"]
_RUNTIME_CONTEXT_SECRETS_KEY = "tecton_secrets"
_RUNTIME_CONTEXT_RESOURCES_KEY = "tecton_resources"
_RUNTIME_CONTEXT_REQUEST_KEY = "tecton_request"
_RUNTIME_CONTEXT_SESSION_KEY = "session_path"


class RuntimeVar(BaseModel):
    name: str
    sources: List[str] = Field(default=_DEFAULT_SOURCES)

    @field_validator("sources")
    @classmethod
    def _validate_sources(cls, v: Any):
        for x in v:
            if x not in _ALLOWED_SOURCES:
                raise ValueError(f"sources must be one of {_ALLOWED_SOURCES}, got {x}")
        return v

    def get(self, required: bool = True, default: Any = None) -> Optional[Any]:
        for src in self.sources:
            if src == "env":
                if self.name in os.environ:
                    return os.environ[self.name]
                continue
            if src == "tecton":
                try:
                    from tecton import conf

                    res = conf.get_or_none(self.name)
                    if res:
                        return res
                    continue
                except ImportError:
                    continue
            if src == "secrets":
                ctx = get_runtime_context()
                secrets = ctx.get(_RUNTIME_CONTEXT_SECRETS_KEY, {})
                if self.name in secrets:
                    return secrets[self.name]
            if src == "resources":
                ctx = get_runtime_context()
                resources = ctx.get(_RUNTIME_CONTEXT_RESOURCES_KEY, {})
                if self.name in resources:
                    return resources[self.name]
            if src == "request":
                ctx = get_runtime_context()
                request = ctx.get(_RUNTIME_CONTEXT_REQUEST_KEY, {})
                if self.name in request:
                    return resources[self.name]
            if src == "session":
                ctx = get_runtime_context()
                session_path = ctx.get(_RUNTIME_CONTEXT_SESSION_KEY)
                if session_path:
                    return read_object(key=self.name, base_uri=session_path)
        if not required:
            return default
        raise ValueError(f"Value {self.name} not found in {self.sources}")

    @staticmethod
    def materialize(obj: Any) -> Any:
        if isinstance(obj, RuntimeVar):
            return obj.get()
        if isinstance(obj, dict):
            return {k: RuntimeVar.materialize(v) for k, v in obj.items()}
        return obj

    def __uuid__(self) -> Any:
        return self.get()


def get_runtime_context() -> Dict[str, Any]:
    return _AGENT_CONTEXT.get() or {}


def get_runtime_var(
    name: str,
    sources: list[str] = _DEFAULT_SOURCES,
    required: bool = True,
    default: Any = None,
) -> Optional[str]:
    return RuntimeVar(name=name, sources=sources).get(
        required=required, default=default
    )


def get_runtime_resource(
    name: str, required: bool = True, default: Any = None
) -> Optional[Any]:
    return get_runtime_var(
        name, sources=["resources"], required=required, default=default
    )


def get_or_create_session_path(input_session_path: Optional[str] = None) -> str:
    if input_session_path:
        return input_session_path
    ctx = get_runtime_context()
    session_path = ctx.get(_RUNTIME_CONTEXT_SESSION_KEY)
    if not session_path:
        session_path = _make_session_path()
    return session_path


def set_session_var(name: str, value: Any) -> None:
    ctx = get_runtime_context()
    session_path = ctx.get(_RUNTIME_CONTEXT_SESSION_KEY)
    if not session_path:
        raise ValueError("Session not set")
    write_object(key=name, value=value, base_uri=session_path)


def get_session_var(name: str, required: bool = True, default: Any = None) -> Any:
    return get_runtime_var(
        name, sources=["session"], required=required, default=default
    )


@contextmanager
def runtime_context(
    context: Dict[str, Any],
    tecton_context: Any = None,
    session_path: Optional[str] = None,
):
    ctx = dict(get_runtime_context())
    ctx.update(context)
    if session_path:
        ctx[_RUNTIME_CONTEXT_SESSION_KEY] = session_path
    if tecton_context is not None:
        if hasattr(tecton_context, "secrets"):
            ctx[_RUNTIME_CONTEXT_SECRETS_KEY] = tecton_context.secrets
        if hasattr(tecton_context, "resources"):
            ctx[_RUNTIME_CONTEXT_RESOURCES_KEY] = tecton_context.resources
    token = _AGENT_CONTEXT.set(ctx)
    try:
        yield
    finally:
        _AGENT_CONTEXT.reset(token)


def make_agent_client_in_rtfv(service_name, connection_json=None):
    ctx = get_runtime_context()
    dev_agent = ctx.get(_DEV_MODE_AGENT_KEY)
    if dev_agent is not None:
        return dev_agent
    else:
        return _make_remote_agent_client_in_rtfv(service_name, connection_json)


@lru_cache
def _make_remote_agent_client_in_rtfv(name, connection_json):
    from ..agent.client import get_agent
    from ..utils.config_wrapper import from_json_config

    address = from_json_config(connection_json)

    return get_agent(
        name=name,
        url=address.url,
        workspace=address.workspace,
        api_key=address.api_key,
    )


def _make_session_path() -> str:
    if "TRANSFORM_SERVER_GROUP_CONFIGURATION_PATH" in os.environ:
        base_path = os.environ["TRANSFORM_SERVER_GROUP_CONFIGURATION_PATH"]
    else:
        base_path = tempfile.gettempdir()
    return os.path.join(base_path, "sessions", str(uuid4()))
