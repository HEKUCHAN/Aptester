from os import PathLike
from typing import TypeAlias, Union
from __future__ import annotations


StrOrBytesPath = Union[str, bytes, PathLike[str], PathLike[bytes]]
