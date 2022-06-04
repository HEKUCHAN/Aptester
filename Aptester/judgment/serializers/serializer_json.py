import json

from Aptester.judgment.reader import Reader

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

if __name__ == "__main__":
    file = ReaderJson("./example/files/sample.json")
    file.get_tests()
