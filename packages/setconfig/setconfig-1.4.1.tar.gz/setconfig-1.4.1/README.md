# setconfig 🔌

> [!TIP]
> Don't forget to star this repo if you like it! ⭐

Some developers prefer to use `@dataclass` while others prefer `BaseModel`.
This holy war is not going to end soon.
So now they can use the same loader and config file in different parts/microservices of one project.

Currently supported:
- [x] [`@dataclass`](https://docs.python.org/3/library/dataclasses.html)
- [x] Pydantic [`BaseModel`](https://docs.pydantic.dev/latest/api/base_model)
- [x] Python [`SimpleNamespace`](https://docs.python.org/3/library/types.html#types.SimpleNamespace) (dotted dict)

Features:
- [x] Loading from streams
- [x] Multiple config files
- [x] Value overriding
- [x] Tuple-friendly


## Installation

```bash
pip install setconfig
```


## Usage sample

### Dataclass, full sample [here](examples/example_dataclass.py)

```python
from dataclasses import dataclass
from setconfig import load_config

@dataclass
class Node:
    host: str
    port: int

@dataclass
class Config:
    nodes: list[Node]

config = load_config('config.yaml', into=Config)

print(config)
# >>> Config(nodes=[Node(host='1.1.1.1', port=1000)])
print(config.nodes[0].host)
# >>> '1.1.1.1'
```

### Pydantic, full sample [here](examples/example_pydantic.py)

```python
from pydantic import BaseModel
from setconfig import load_config

class Node(BaseModel):
    host: str
    port: int

class Config(BaseModel):
    nodes: list[Node]

config = load_config('config.yaml', into=Config)

print(config)
# >>> Config(nodes=[Node(host='1.1.1.1', port=1000)])
print(config.nodes[0].host)
# >>> '1.1.1.1'
```

### SimpleNamespace, full sample [here](examples/example_simple.py)

```python
from setconfig import load_config

config = load_config('config.yaml')

print(config)
# >>> Config(nodes=[Node(host='1.1.1.1', port=1000)])
print(config.nodes[0].host)
# >>> '1.1.1.1'
```

### Features

#### Loading from string/StringIO/etc

```python
from setconfig import load_config_stream

config = load_config_stream('done: true')
```

#### Multiple config files, full sample [here](examples/example_multi.py)

```python
config = load_config('config.base.yaml', 'config.dev.yaml', 'config.feature-x.yaml', into=Config)
```

Configs are processed in the order they are passed to `load_config` (from left to right), where
last overrides the previous ones

#### Value overriding, full sample [here](examples/example_override.py)

```python
config = load_config('config.yaml', into=Config, override={'timeout': 10})
```

#### Extra parsing params

```python
config = load_config('config.yaml', into=Config, check_types=False)
```

Where `check_types` is a dacite flag, see https://github.com/konradhalas/dacite#type-checking

#### Tuple-friendly

There is [known issue](https://github.com/konradhalas/dacite/issues/227) in `dacite` that raises type error
when loading list into tuple. [Pull request with fix is ready](https://github.com/konradhalas/dacite/pull/228)
since May 2023, but not merged yet... That's why `setconfig` has its own fix


## FAQ

### Why only YAML?

> There should be one-- and preferably only one --obvious way to do it
> 
> [(c) Zen of Python](https://peps.python.org/pep-0020/#the-zen-of-python)

### I want to use structure from `X` package

Create an issue or PR :)


## More

PyPI: https://pypi.org/project/setconfig

Repository: https://github.com/abionics/setconfig

Developer: Alex Ermolaev (Abionics)

Email: abionics.dev@gmail.com

License: MIT (see LICENSE.txt)
