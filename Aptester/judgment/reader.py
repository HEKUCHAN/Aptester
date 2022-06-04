from pathlib import Path
from typing import Dict, List

from Aptester.conveniences.error import *
from Aptester.conveniences.static import *
from Aptester.judgment.serializer import TestCase

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

    def get_tests(self) -> List[TestCase]:
        test_cases: List[TestCase] = []
        for name, test in self.tests.items():
            if isinstance(test, Dict):
                test_cases.append(
                    TestCase(name, *test.values())
                )
            elif isinstance(test, List):
                test_cases.append(
                    TestCase(
                        name=name,
                        input=self._parse(test[0]),
                        out=self._parse(test[1])
                    )
                )

        return test_cases

    @classmethod
    def _parse(cls, items) -> str:
        if cls.is_unlist(items):
            return items
        elif cls.is_one_dimension(items):
            items = "".join(map(lambda x: str(x) + '\n', items))
            return items
        elif cls.is_two_dimension(items):
            string = ""
            for item in items:
                string += " ".join(map(str, item)) + '\n'

            return string
        else:
            raise ValueError(
                "The input or output of the Testcase file is more than a 3-dimensional array.")

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
