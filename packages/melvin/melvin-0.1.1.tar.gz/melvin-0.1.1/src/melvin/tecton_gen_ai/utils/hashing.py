from ..constants import _TECTON_CHECKPOINT_ATTR, UUID_ATTR


import json
import uuid
from datetime import date, datetime
from typing import Any


def to_uuid(obj: Any) -> str:
    def _to_serializable(obj):
        if obj is None:
            return float("nan")
        elif isinstance(obj, (str, int, float, bool)):
            return obj
        elif isinstance(obj, (set, tuple, list)):
            return list(_to_serializable(x) for x in obj)
        elif isinstance(obj, dict):
            return {_to_serializable(k): _to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif hasattr(obj, _TECTON_CHECKPOINT_ATTR):
            return getattr(obj, _TECTON_CHECKPOINT_ATTR)
        elif hasattr(obj, UUID_ATTR):
            return getattr(obj, UUID_ATTR)()
        raise NotImplementedError(f"Type {type(obj)} is not serializable")

    return str(uuid.uuid5(uuid.NAMESPACE_DNS, json.dumps(_to_serializable(obj))))
