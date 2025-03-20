import asyncio
import os
from typing import Protocol

import diskcache


class CacheProtocol(Protocol):
    def set(self, key, val): ...
    def get(self, key): ...
    async def aset(self, key, val): ...
    async def aget(self, key): ...


class _DiskCache(diskcache.Cache, CacheProtocol):
    async def aset(self, key, val):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.set, key, val)

    async def aget(self, key):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get, key)


def _cache_dir(*extra_paths: str):
    """Get the cache directory tied to the user

    Example: `~/.cache/$appname/$version`
    """
    path = os.environ.get("XDG_CACHE_HOME", "")
    if not path.strip():
        path = os.path.expanduser("~/.cache")
    return os.path.join(path, *extra_paths)


def get_cache(*extra_paths: str) -> CacheProtocol:
    cache_dir = _cache_dir("tecton-gen-ai", "structured_outputs", *extra_paths)
    # NOTE: default size limit of 1GB (https://grantjenks.com/docs/diskcache/api.html#constants)
    return _DiskCache(cache_dir)
