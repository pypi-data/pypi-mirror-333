import pathlib
from collections import namedtuple
from typing import Iterable


def container_to_tuple(container):
    if not hasattr(container, "__contains__"):
        raise TypeError
    values = []
    if not hasattr(container, "get"):
        contents = list(container)
        return_func = lambda x: tuple(x)  # noqa: E731
    else:
        keys = list(container.keys())
        Node = namedtuple("Node", keys)
        contents = [container[k] for k in keys]
        return_func = lambda x: Node(*x)  # noqa: E731
    for item in contents:
        if not hasattr(item, "__contains__") or hasattr(item, "capitalize"):  # not a container or a string
            values.append(item)
        else:
            values.append(container_to_tuple(item))
    return return_func(values)


def parse_configuration(lines: Iterable[str]):
    result = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", maxsplit=1)
        k, v = k.strip(), v.strip()
        keys = k.split(".")
        r = result
        for i in range(len(keys) - 1):
            if keys[i] not in r:
                r[keys[i]] = {}
            r = r[keys[i]]
        r[keys[-1]] = v

    return container_to_tuple(result)


def get_configuration(path: pathlib.Path):
    """Read PATH and make contents available as (nested) NamedTuple.

    :param path: File with configuration
    """
    with path.open("r") as f:
        return parse_configuration(f.readlines())
