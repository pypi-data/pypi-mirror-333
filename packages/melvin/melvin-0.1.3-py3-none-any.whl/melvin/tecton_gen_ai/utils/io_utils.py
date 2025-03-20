import os
from contextlib import contextmanager
from typing import Any, Callable, Iterator, Optional
from uuid import uuid4

import cloudpickle
from pyarrow.fs import FileSelector, FileSystem, FileType

from .hashing import to_uuid


def safe_write(uri: str, write_func: Callable):
    _SafePathObject(uri).safe_write(write_func)


@contextmanager
def safe_read(uri: str):
    obj = _SafePathObject(uri)
    with obj.safe_read() as f:
        yield f


@contextmanager
def create_temp_dir(base_uri: str, key: Any) -> Iterator[str]:
    dir_path = os.path.join(base_uri, to_uuid(key))
    fs, path = FileSystem.from_uri(dir_path)
    info = fs.get_file_info(path)
    existed = False
    if info.type == FileType.Directory:
        existed = True
    elif info.type != FileType.NotFound:
        raise FileExistsError(f"{dir_path} exists and it is not a directory")
    if not existed:
        fs.create_dir(path, recursive=True)
    yield dir_path
    if not existed:
        fs.delete_dir(path)


def write_object(key: Any, value: Any, base_uri: str) -> None:
    _key = to_uuid(key)
    path = os.path.join(base_uri, _key)
    safe_write(path, lambda f: cloudpickle.dump(value, f))


def read_object(key: Any, base_uri: str) -> Any:
    path = os.path.join(base_uri, to_uuid(key))
    with safe_read(path) as f:
        return cloudpickle.load(f)


class _SafePathObject:
    """
    A lockless thread safe file reader/writer
    """

    def __init__(self, uri: str):
        self.uri = uri
        self.fs, self.path = FileSystem.from_uri(uri)
        self.info = self.fs.get_file_info(self.path)
        if self.info.type == FileType.File or self.info.type == FileType.Unknown:
            raise FileExistsError(f"{uri} exists and it is not a directory")

    @contextmanager
    def safe_read(self):
        path = self._find_ready_path()
        if path is None:
            raise FileNotFoundError(f"{self.uri} is not ready")
        with self.fs.open_input_stream(path) as f:
            yield f

    def safe_write(self, write_func: Callable) -> None:
        if self._find_ready_path() is not None:
            return
        if self.info.type == FileType.NotFound:
            self.fs.create_dir(self.path, recursive=True)
        path = os.path.join(self.path, str(uuid4()))
        done = path + ".done"
        with self.fs.open_output_stream(path) as f:
            write_func(f)
        with self.fs.open_output_stream(done) as f:
            pass

    def _find_ready_path(self) -> Optional[str]:
        if self.info.type == FileType.NotFound:
            return None
        files = self.fs.get_file_info(FileSelector(self.path, recursive=False))
        for file in files:
            if file.path.endswith(".done"):
                return file.path[:-5]
        return None
