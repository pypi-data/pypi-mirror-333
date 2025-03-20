from threading import Lock
from typing import Callable, Dict, TypeVar

K = TypeVar('K')
V = TypeVar('V')

SENTINEL = object()

def compute_if_absent(obj: Dict[K, V], key: K, value_fn: Callable[[K], V], lock: Lock = None):
    try:
        if lock: lock.acquire()

        if obj.get(key, SENTINEL) is SENTINEL:
            value: K = value_fn(key)
            obj[key] = value

        return obj.get(key)
    finally:
        if lock: lock.release()

def new_map(*maps):
    m = {}
    for v in maps:
        m.update(v)

    return m

def from_map(keys, obj):
    return {k: obj[k] for k in keys}

def map_keys(key_map, obj):
    return {key_map[k]: v for k, v in obj.items() if k in key_map}

def get_values(obj, keys):
    return [obj.get(k) for k in keys if obj.get(k) is not None]
