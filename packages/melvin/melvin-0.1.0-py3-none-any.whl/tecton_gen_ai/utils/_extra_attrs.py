from typing import Tuple, Any, Dict

_ATTR_STORE: Dict[int, Tuple[Any, Dict[str, Any]]] = {}


def set_attr(obj: Any, key: str, value: Any) -> None:
    if id(obj) not in _ATTR_STORE:
        _ATTR_STORE[id(obj)] = (obj, {key: value})
    else:
        _ATTR_STORE[id(obj)][1][key] = value


def get_attr(obj: Any, key: str) -> Any:
    return _ATTR_STORE[id(obj)][1][key]


def has_attr(obj: Any, key: str) -> bool:
    if id(obj) not in _ATTR_STORE:
        return False
    return key in _ATTR_STORE[id(obj)][1]
