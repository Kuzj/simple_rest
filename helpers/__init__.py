from collections import namedtuple
from typing import (Dict, NamedTuple)

def dict2namedtuple(name: str, d: Dict) -> NamedTuple:
    return namedtuple(name, d.keys())(**d)
