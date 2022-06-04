from pathlib import Path

from Aptester.conveniences.error import *
from Aptester.conveniences.static import *

class Reader:
    def __init__(
        self,
        path: str
    ):
        self.path = Path(path).resolve()

        self.is_valid()
        self.open()

    def is_valid(self):
        if not self.path.exists():
            raise FileNotFoundError

        if self.path.is_dir():
            raise FileTypeError

        if self.path.name.lower() == 'aptester':
            pass
        elif not self.path.suffix in SUPPORTED_SUFFIX:
            raise NotSupportedFileSuffix


    def open(self):
        with open(self.path, mode='r') as f:
            self.f = f.read()

    @classmethod
    def is_unlist(cls, item) -> bool:
        return not isinstance(item, list)

    @classmethod
    def is_one_dimension(cls, item) -> bool:
        item_types = list(set(map(type, item)))
        return not list in item_types

    @classmethod
    def is_two_dimension(cls, item) -> bool:
        item_types = list(set(map(type, item[0])))
        return not list in item_types
