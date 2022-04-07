from enum import IntEnum
from typing import Union
from pathlib import Path
from os import PathLike, path


class FileSuffix(IntEnum):
    TEXT = 0
    JSON = 1
    YAML = 2
    OTHER = 4


class File:
    def __init__(self, file_path: Union[str, bytes, PathLike]):
        if type(file_path) == Path:
            file_path = file_path.resolve()
        else:
            file_path = Path(file_path).resolve()

        if file_path.suffix == ".txt" or file_path.suffix == ".text":
            __suffix = FileSuffix.TEXT
        elif file_path.suffix == ".json":
            __suffix = FileSuffix.JSON
        elif file_path.suffix == ".yaml" or file_path.suffix == ".yml":
            __suffix = FileSuffix.YAML
        else:
            __suffix = FileSuffix.OTHER

        self.path: Path = file_path
        self.suffix: FileSuffix = __suffix

    def is_valid(self, exc: bool = False) -> Union[bool, None]:
        if exc and not path.isfile(self.path):
            return FileNotFoundError(self.path)
        return path.isfile(self.path)
