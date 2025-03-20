import json
from functools import lru_cache
from time import time

# for executing function declarations
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union  # noqa

from httpx import Client as HttpClient

from ..constants import _INPUT_JSON_FIELD, _OUTPUT_JSON_FIELD
from ..utils._serialization import deserialize_pydantic
from ..utils.config_wrapper import from_json_config, to_json_config
from ..utils.runtime import RuntimeVar, get_runtime_context
from .base import AgentBase, AgentInputModel, FeatureServiceConfig, ToolWrapper


@lru_cache
def _get_tecton_client(
    url: Any, api_key: Any, workspace: Any, timeout_sec: float
) -> Any:
    from tecton_client import TectonClient

    http_client = HttpClient(timeout=timeout_sec)
    return TectonClient(
        url=url, api_key=api_key, default_workspace_name=workspace, client=http_client
    )


def get_agent(
    name: str,
    url: Optional[str] = None,
    workspace: Optional[str] = None,
    api_key: Union[str, RuntimeVar, None] = None,
    metastore_update_interval: Any = "60s",
) -> AgentBase:
    """
    Create a client connecting to a deployed agent service.

    Args:

        name: The agent name
        url: The Tecton URL, defaults to None (will use the default tecton url from the environment)
        workspace: The workspace name, defaults to None (will use the environment variable TECTON_WORKSPACE)
        api_key: The API key defaults to None (will use the environment variable TECTON_API_KEY)
        metastore_update_interval: The interval expression to update the metastore, defaults to "60s"

    Returns:

        Agent: The client agent
    """
    return _AgentClientRemote(
        name=name,
        url=url,
        workspace=workspace,
        api_key=api_key,
        metastore_update_interval=metastore_update_interval,
    )


class _AgentClientRemote(AgentBase):
    def __init__(
        self,
        name: str,
        url: Optional[str] = None,
        workspace: Optional[str] = None,
        api_key: Union[str, RuntimeVar, None] = None,
        metastore_update_interval: Any = "60s",
    ):
        import pandas as pd

        super().__init__(name=name)

        self.service = FeatureServiceConfig(
            url=url,
            workspace=workspace,
            api_key=api_key,
            service=name,
        )
        self.interval = pd.to_timedelta(metastore_update_interval).total_seconds()
        self.last_check = 0
        self._static_metastore = None
        self._orig_key = api_key

    def __json_config_dict__(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "url": self.service.url,
            "workspace": self.service.workspace,
            "api_key": self._orig_key,
            "metastore_update_interval": self.interval,
        }

    @property
    def metastore(self) -> Dict[str, Any]:
        current = time()
        if self._static_metastore is None or current - self.last_check > self.interval:
            self._static_metastore = self._invoke(
                self.name + "_metastore",
                [],
                [],
                {},
                feature_type="metastore",
                timeout_sec=5,
            )
            self.last_check = current
        return self._static_metastore

    @property
    def input_schema(self) -> Type[AgentInputModel]:
        return deserialize_pydantic(self.metastore["input_schema"])

    @property
    def output_schema(self) -> Union[Type[str], Type[AgentInputModel]]:
        schema = self.metastore["output_schema"]
        if schema == "str":
            return str
        return deserialize_pydantic(schema)

    def export_tools(self, names: Optional[list[str]] = None) -> List[ToolWrapper]:
        tools = []
        for name in self.metastore.get("tools", {}).keys():
            if names is None or name in names:
                tools.append(_RemoteTool(self, name))
        return tools

    def _get_tecton_client(self, timeout_sec: float) -> Any:
        return _get_tecton_client(
            url=self.service.url,
            api_key=self.service.api_key,
            workspace=self.service.workspace,
            timeout_sec=timeout_sec,
        )

    def _invoke_entrypoint(
        self,
        message: str,
        timeout_sec: float,
        chat_history: Optional[List[Tuple[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        agent_name: Optional[str] = None,
    ) -> Union[str, Dict[str, Any]]:
        target_name = agent_name or self.name
        ctx = {
            "query": message,
            "chat_history": [list(x) for x in (chat_history or [])],
        }
        if context:
            ctx.update(context)
        input_json = json.dumps(ctx)
        session_path = get_runtime_context().get("session_path")
        client = self._get_tecton_client(timeout_sec=timeout_sec)
        gf = client.get_features(
            feature_service_name=target_name,
            request_context_map={
                _INPUT_JSON_FIELD: input_json,
                "session_path": session_path,
            },
        )
        fd = gf.get_features_dict()
        key = target_name + "." + _OUTPUT_JSON_FIELD
        resp = json.loads(fd[key])
        if "error" in resp:
            raise Exception(resp["error"])
        return resp["result"]

    def _get_feature_value(
        self,
        name: str,
        key_map: Dict[str, Any],
        request_map: Dict[str, Any],
        feature_type: str,
        timeout_sec: float,
    ):
        if feature_type == "prompt_not_in_use":  # pragma: no cover
            # TODO: prompt FCO: fix or delete?
            request_context_map = {
                "name": name,
                **request_map,
            }
        else:
            request_context_map = {
                "name": name,
                "input": json.dumps(request_map),
                "session_path": get_runtime_context().get("session_path"),
            }
        request_context_map["_dummy_request_ts"] = None
        client = self._get_tecton_client(timeout_sec=timeout_sec)
        gf = client.get_features(
            feature_service_name=self.name + "_" + name,
            join_key_map=key_map,
            request_context_map=request_context_map,
        )
        fd = gf.get_features_dict()
        if feature_type == "prompt_not_in_use":  # pragma: no cover
            # TODO: prompt FCO: fix or delete?
            return fd[name + ".prompt"]
        else:
            resp = json.loads(fd[name + "." + _OUTPUT_JSON_FIELD])
            if "error" in resp:
                raise Exception(resp["error"])
            result = resp["result"]
            return result


class _RemoteTool(ToolWrapper):
    subtype: str = "remote_tool"

    def __init__(
        self,
        agent: _AgentClientRemote,
        tool_name: str,
    ):
        self.agent = agent
        self._tool_name = tool_name
        self.metadata = agent.metastore["tools"][tool_name]

    @property
    def use_when(self) -> Optional[Callable]:
        return None

    @property
    def metastore_key(self) -> str:
        return self.tool_name

    @property
    def tool_name(self) -> str:
        return self.agent.name + "_" + self._tool_name

    def make_metadata(self):
        meta = self.metadata.copy()
        meta["agent_json"] = to_json_config(self.agent)
        meta["remote_name"] = self._tool_name
        base = self.make_base_metadata()
        base.pop("use_when")
        meta.update(base)
        return meta

    @classmethod
    def invoke(cls, agent: AgentBase, name: str, kwargs: Dict[str, Any]) -> Any:
        meta = agent.metastore["tools"][name]
        ctx = (
            agent._get_context()
        )  # TODO: should we pass the context to the remote agent?
        ctx.update(kwargs)
        _agent = from_json_config(meta["agent_json"])
        return _agent.invoke_tool(
            name=meta["remote_name"],
            kwargs=ctx,
        )
