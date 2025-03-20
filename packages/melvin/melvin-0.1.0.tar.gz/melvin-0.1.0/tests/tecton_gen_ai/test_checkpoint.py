import os
import random
from datetime import date, datetime

import pandas as pd
from pytest import raises

from src.tecton_gen_ai.tecton_utils.checkpoint import make_deterministic, with_checkpoint
from src.tecton_gen_ai.utils.hashing import to_uuid


def test_to_uuid():
    assert to_uuid(None) != ""
    assert to_uuid(None) == to_uuid(float("nan"))
    assert to_uuid(None) != to_uuid(0)
    assert to_uuid([1, "a"]) != to_uuid(1)
    assert to_uuid([1, "a"]) != to_uuid([1, "b"])
    assert to_uuid([1, "a"]) == to_uuid([1, "a"])
    assert to_uuid((1, "a")) == to_uuid([1, "a"])
    # dicts must keep the same order
    assert to_uuid({"a": 1, "b": "a"}) != to_uuid({"b": "a", "a": 1})
    assert to_uuid({"a": 1, "b": "a"}) == to_uuid({"a": 1, "b": "a"})
    assert to_uuid(date(2021, 1, 1)) == to_uuid(date(2021, 1, 1))
    assert to_uuid(date(2021, 1, 1)) != to_uuid(date(2021, 1, 2))
    assert to_uuid(datetime(2021, 1, 1, 1, 1, 1)) == to_uuid(
        datetime(2021, 1, 1, 1, 1, 1)
    )
    assert to_uuid(datetime(2021, 1, 1, 1, 1, 1)) != to_uuid(
        datetime(2021, 1, 1, 1, 1, 2)
    )
    with raises(NotImplementedError):
        to_uuid(object())
    df = pd.DataFrame([[1, 2]], columns=["a", "b"])
    with raises(NotImplementedError):
        to_uuid(df)
    df = make_deterministic(df, 1)
    assert to_uuid(df) == to_uuid(df)


def test_checkpoint(tmp_path):
    @with_checkpoint
    def _checkpoint_tester_1(a: int, b: str) -> float:
        """Test1"""
        return random.random()

    @with_checkpoint(idempotency_key=2)
    def _checkpoint_tester_2(a: float, b: str) -> pd.DataFrame:
        """Test2"""
        return pd.DataFrame([[int(10 + a * 20), random.random()]], columns=["a", "b"])

    @with_checkpoint
    def _checkpoint_tester_3(df: pd.DataFrame) -> pd.DataFrame:
        df["b"] = df["b"] + df["a"] + random.random()
        return df

    os.environ["TECTON_CACHE_PATH"] = str(tmp_path)

    random.seed(0)
    assert _checkpoint_tester_1.__doc__ == "Test1"

    assert _checkpoint_tester_1(1, "a") == _checkpoint_tester_1(1, "a")
    assert _checkpoint_tester_1(1, "a") > 0
    assert _checkpoint_tester_1(1, "a") != _checkpoint_tester_1(1, "b")

    assert _checkpoint_tester_2(1, "a").equals(_checkpoint_tester_2(1, "a"))
    assert _checkpoint_tester_2(1, "a").iloc[0, 0] > 0
    assert not _checkpoint_tester_2(1, "a").equals(_checkpoint_tester_2(1, "b"))

    a1 = _checkpoint_tester_1(1, "a")
    b1 = _checkpoint_tester_2(a1, "a")
    a2 = _checkpoint_tester_1(1, "a")
    b2 = _checkpoint_tester_2(a2, "a")
    assert b1.equals(b2)
    a3 = _checkpoint_tester_1(1, "b")
    b3 = _checkpoint_tester_2(a3, "a")
    assert not b1.equals(b3)
    b4 = _checkpoint_tester_2(a1, "b")
    assert not b1.equals(b4)

    assert _checkpoint_tester_3(b1).equals(_checkpoint_tester_3(b1))
    assert not _checkpoint_tester_3(b1).equals(_checkpoint_tester_3(b2))

    del os.environ["TECTON_CACHE_PATH"]
