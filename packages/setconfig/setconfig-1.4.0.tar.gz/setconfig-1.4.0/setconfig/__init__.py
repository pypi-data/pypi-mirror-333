"""
Developed by Alex Ermolaev (Abionics)
Email: abionics.dev@gmail.com
License: MIT
"""

__version__ = '1.4.0'

from dataclasses import is_dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import TypeVar, Type, Any

import yaml
from dacite import from_dict, Config
from pydantic import BaseModel

DEFAULT_CONFIG_PATH = 'config.yaml'

T = TypeVar('T')


def load_config(
        *paths: Path | str,
        into: Type[T] | None = None,
        override: dict | None = None,
        **kwargs,
) -> T:
    if len(paths) == 0:
        paths = [DEFAULT_CONFIG_PATH]
    data = _merge_many([
        _load_yaml(path)
        for path in paths
    ])
    print(data)
    return load_config_dict(data, into, override, **kwargs)


def load_config_stream(
        stream: Any,
        into: Type[T] | None = None,
        override: dict | None = None,
        **kwargs,
) -> T:
    data = yaml.safe_load(stream)
    return load_config_dict(data, into, override, **kwargs)


def load_config_dict(
        data: dict,
        into: Type[T] | None = None,
        override: dict | None = None,
        **kwargs,
) -> T:
    if override:
        data = data | override
    if isinstance(into, SimpleNamespace) or into is None:
        return _parse_simple(data)
    if is_dataclass(into):
        config = Config(**kwargs)
        return from_dict(into, data, config)  # type: ignore
    if issubclass(into, BaseModel):
        return into.model_validate(data, **kwargs)  # type: ignore
    raise TypeError(f'Unsupported output class: {into}')


def _parse_simple(data: Any) -> Any:
    if isinstance(data, dict):
        parsed = {
            str(key): _parse_simple(value)
            for key, value in data.items()
        }
        return SimpleNamespace(**parsed)
    if isinstance(data, list | tuple):
        return data.__class__((
            _parse_simple(item)
            for item in data
        ))
    return data


def _load_yaml(path: Path | str) -> dict:
    with open(path, 'r') as file:
        return yaml.safe_load(file) or dict()


def _merge_many(data: list[dict]) -> dict:
    base = data.pop(0)
    for update in data:
        _merge_two(base, update)
    return base


def _merge_two(base: dict, update: dict):
    for key, value in update.items():
        base_value = base.get(key)
        if isinstance(base_value, dict) and isinstance(value, dict):
            _merge_two(base_value, value)
        else:
            base[key] = value
