import pandas as pd
from typing import List, Dict, Any
from pandas.api.types import is_datetime64_any_dtype


def to_records(
    df: pd.DataFrame, timestamp_to: str = "original"
) -> List[Dict[str, Any]]:
    """
    Convert a DataFrame to a list of dictionaries

    Args:

        df: The DataFrame
        timestamp_to: The timestamp field to convert to, defaults to "original",
            which will keep the original pandas Timestamp. When set to "py", it will
            convert the timestamp to a Python datetime object. When set to "str", it
            will convert the timestamp to a string.

    Returns:

        List[Dict[str,Any]]: The list of dictionaries
    """
    cols: Dict[str, pd.Series] = {}
    for col in df.columns:
        s = df[col]
        if is_datetime64_any_dtype(s):
            if timestamp_to == "original":
                cols[col] = s
            elif timestamp_to == "py":
                cols[col] = pd.Series(s.dt.to_pydatetime(), dtype=object)
            elif timestamp_to == "str":
                cols[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                raise ValueError(f"Unsupported timestamp_to {timestamp_to}")
        else:
            cols[col] = df[col]
    return pd.DataFrame(cols).to_dict(orient="records")
