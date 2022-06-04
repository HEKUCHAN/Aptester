import json
from typing import NamedTuple, Dict, List, Any

from Aptester.judgment.reader import Reader


class TestCase(NamedTuple):
    name: str
    input: str
    out: str


class ReaderJson(Reader):
    def __init__(self, path) -> None:
        super().__init__(path)

        # initial variables
        if "tests" in self.f:
            self.tests = self.f["tests"]
        else:
            self.tests = None

        if "config" in self.f:
            self.config = self.f["config"]
        else:
            self.config = None

        if "information" in self.f:
            self.information = self.f["information"]
        else:
            self.information = None

    def open(self) -> None:
        with open(self.path, mode='r') as f:
            self.f = json.load(f)

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

if __name__ == "__main__":
    file = ReaderJson("./example/files/sample.json")
    file.get_tests()
