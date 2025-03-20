from src.tecton_gen_ai.utils.io_utils import (
    safe_write,
    safe_read,
    create_temp_dir,
    write_object,
    read_object,
)
from pytest import raises
import os


def test_safe_read_write(tmp_path):
    uri = str(tmp_path / "test1")
    with raises(FileNotFoundError):
        with safe_read(uri) as f:
            pass
    safe_write(uri, lambda f: f.write(b"hello"))
    with safe_read(uri) as f:
        assert f.read() == b"hello"
    safe_write(uri, lambda f: f.write(b"hello2"))  # no op since file exists
    with safe_read(uri) as f:
        assert f.read() == b"hello"
    uri = str(tmp_path / "test2")
    with open(uri, "w") as f:
        f.write("hello")
    with raises(FileExistsError):
        safe_write(uri, lambda f: f.write(b"hello"))
    path = tmp_path / "test3"
    # create a directory
    path.mkdir()
    path1 = path / "a"
    with open(str(path1), "w") as f:
        f.write("hello")
    path2 = path / "b"
    with open(str(path2), "w") as f:
        f.write("hello2")
    with raises(FileNotFoundError):
        with safe_read(str(path)) as f:
            pass
    path3 = path / "b.done"
    path3.touch()
    with safe_read(str(path)) as f:
        assert f.read() == b"hello2"


def test_create_temp_dir(tmp_path):
    with create_temp_dir(str(tmp_path), 1) as dir_path:
        path = os.path.join(dir_path, "a")
        with open(path, "w") as f:
            f.write("hello")
        with create_temp_dir(str(tmp_path), 1) as dir_path1:
            assert dir_path == dir_path1
            assert os.path.exists(dir_path)
        assert os.path.exists(dir_path)

    assert not os.path.exists(dir_path)


def test_read_write_object(tmp_path):
    with create_temp_dir(str(tmp_path), 1) as dir_path:
        write_object(1, "hello", dir_path)
        assert read_object(1, dir_path) == "hello"
        write_object(1, "hello2", dir_path)  # not overwritable
        assert read_object(1, dir_path) == "hello"
        write_object(2, "hello2", dir_path)
        assert read_object(2, dir_path) == "hello2"
        with raises(FileNotFoundError):
            read_object(3, dir_path)
