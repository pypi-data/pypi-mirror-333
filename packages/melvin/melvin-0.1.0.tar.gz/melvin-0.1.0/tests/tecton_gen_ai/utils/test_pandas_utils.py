from src.tecton_gen_ai.utils.pandas_utils import to_records
import pandas as pd
from pytest import raises

from datetime import datetime


def test_to_records():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3],
            "b": [4, 5, 6],
            "c": [7, 8, 9],
        }
    )
    assert to_records(df) == [
        {"a": 1, "b": 4, "c": 7},
        {"a": 2, "b": 5, "c": 8},
        {"a": 3, "b": 6, "c": 9},
    ]
    df = pd.DataFrame(
        {
            "a": [1, 2, 3],
        }
    )
    df["b"] = pd.to_datetime("2022-01-01")
    assert isinstance(to_records(df)[0]["b"], pd.Timestamp)
    assert to_records(df) == [
        {"a": 1, "b": pd.Timestamp("2022-01-01")},
        {"a": 2, "b": pd.Timestamp("2022-01-01")},
        {"a": 3, "b": pd.Timestamp("2022-01-01")},
    ]
    assert not isinstance(to_records(df, timestamp_to="py")[0]["b"], pd.Timestamp)
    assert to_records(df, timestamp_to="py") == [
        {"a": 1, "b": datetime(2022, 1, 1, 0, 0)},
        {"a": 2, "b": datetime(2022, 1, 1, 0, 0)},
        {"a": 3, "b": datetime(2022, 1, 1, 0, 0)},
    ]
    assert to_records(df, timestamp_to="str") == [
        {"a": 1, "b": "2022-01-01 00:00:00"},
        {"a": 2, "b": "2022-01-01 00:00:00"},
        {"a": 3, "b": "2022-01-01 00:00:00"},
    ]
    with raises(ValueError):
        to_records(df, timestamp_to="invalid")
