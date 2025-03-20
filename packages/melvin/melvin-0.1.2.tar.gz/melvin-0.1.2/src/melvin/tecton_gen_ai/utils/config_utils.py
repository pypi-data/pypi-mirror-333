from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Dict, Iterator

import pandas as pd
from pydantic import BaseModel, Field

from ..constants import DEFAULT_TIMEOUT


class Configs(BaseModel):
    """
    The base configs for the feature view, LLM model, and feature service
    """

    llm: Any = Field(description="The LLM model", default=None)
    default_timeout: str = Field(
        description="The default timeout", default=DEFAULT_TIMEOUT
    )
    base_config: Dict[str, Any] = Field(
        description="The base config for all tecton objects", default={}
    )
    fv_base_config: Dict[str, Any] = Field(
        description="The base config for all types of feature views", default={}
    )
    bfv_config: Dict[str, Any] = Field(
        description="The config for the batch feature view", default={}
    )
    sfv_config: Dict[str, Any] = Field(
        description="The config for the stream feature view", default={}
    )
    rtfv_config: Dict[str, Any] = Field(
        description="The config for the realtime feature view", default={}
    )
    feature_service_config: Dict[str, Any] = Field(
        description="The config for the feature service", default={}
    )
    agent_invoke_kwargs: Dict[str, Any] = Field(
        description="The kwargs for the agent invoke", default={}
    )

    def update(self, other: "Configs") -> "Configs":
        """
        Update the configs with the other configs

        Args:

            other: The other configs

        Returns:

                The updated configs
        """
        return Configs(
            llm=other.llm or self.llm,
            default_timeout=other.default_timeout or self.default_timeout,
            base_config=self.base_config | other.base_config,
            fv_base_config=self.fv_base_config | other.fv_base_config,
            bfv_config=self.bfv_config | other.bfv_config,
            sfv_config=self.sfv_config | other.sfv_config,
            rtfv_config=self.rtfv_config | other.rtfv_config,
            feature_service_config=self.feature_service_config
            | other.feature_service_config,
            agent_invoke_kwargs=self.agent_invoke_kwargs | other.agent_invoke_kwargs,
        )

    def get_bfv_config(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the config for the batch feature view merged with the base config

        Args:

            configs: The additional configs to merge

        Returns:

            The config for the batch feature view
        """
        return self.merge(
            self.base_config, self.fv_base_config, self.bfv_config, *configs
        )

    def get_rtfv_config(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the config for the realtime feature view merged with the base config

        Args:

            configs: The additional configs to merge

        Returns:

            The config for the realtime feature view
        """
        return self.merge(
            self.base_config, self.fv_base_config, self.rtfv_config, *configs
        )

    def get_sfv_config(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the config for the stream feature view merged with the base config

        Args:

            configs: The additional configs to merge

        Returns:

            The config for the stream feature view
        """
        return self.merge(
            self.base_config, self.fv_base_config, self.sfv_config, *configs
        )

    def get_agent_invoke_kwargs(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the kwargs for the agent invoke merged with the base config

        Args:

            configs: The additional configs to merge

        Returns:

            The kwargs for the agent invoke
        """
        return self.merge(self.base_config, self.agent_invoke_kwargs, *configs)

    def get_timeout_sec(self, timeout: Any) -> float:
        """
        Get the timeout in seconds

        Args:

            timeout: The timeout, if None, it will use the default timeout

        Returns:

            The timeout in seconds
        """
        return pd.to_timedelta(timeout or self.default_timeout).total_seconds()

    def set_default(self) -> None:
        """
        Set this config set to be the the default for the feature view,
        LLM model, and feature service

        Examples:

            ```python
            from tecton_gen_ai.api import Configs

            Configs(llm="openai/gpt-4o").set_default()
            ```
        """
        _TECTON_GEN_AI_CONFIG.set(self)

    @contextmanager
    def update_default(self) -> Iterator["Configs"]:
        """
        Update the default configs for the feature view, LLM model, and feature service

        Examples:

            ```python
            from tecton_gen_ai.api import Configs

            Configs(llm="openai/gpt-4o").set_default()

            with Configs(fv_base_config={"name": "my_fv"}).update_default():
                conf = Configs.get_default()
                assert conf.fv_base_config["name"] == "my_fv"
                assert conf.llm == "openai/gpt-4o"

            conf = Configs.get_default()
            assert len(conf.fv_base_config)==0
            ```
        """
        old_config = _TECTON_GEN_AI_CONFIG.get()
        try:
            token = _TECTON_GEN_AI_CONFIG.set(old_config.update(self))
            yield
        finally:
            _TECTON_GEN_AI_CONFIG.reset(token)

    @staticmethod
    def get_default() -> "Configs":
        """
        Get the current default configs for the feature view, LLM model, and feature service

        Returns:

            The default configs

        Examples:

            Examples:

            ```python
            from tecton_gen_ai.api import Configs

            Configs(llm="openai/gpt-4o").set_default()

            with Configs(fv_base_config={"name": "my_fv"}).update_default():
                conf = Configs.get_default()
                assert conf.fv_base_config["name"] == "my_fv"
                assert conf.llm == "openai/gpt-4o"

            conf = Configs.get_default()
            assert len(conf.fv_base_config)==0
            ```
        """
        return _TECTON_GEN_AI_CONFIG.get()

    def merge(self, *dicts: Dict[str, Any]) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        secrets: Dict[str, Any] = {}
        resources: Dict[str, Any] = {}
        for d in dicts:
            secrets.update(d.get("secrects", {}))
            resources.update(d.get("resource_providers", {}))
            res.update(d)
        if len(secrets) > 0:
            res["secrets"] = secrets
        if len(resources) > 0:
            res["resource_providers"] = resources
        return res


_TECTON_GEN_AI_CONFIG = ContextVar("tecton_gen_ai_config", default=Configs())
