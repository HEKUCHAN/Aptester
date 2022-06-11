import yaml

from Aptester.judgment.reader import Reader


class ReaderYaml(Reader):
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
        with open(self.path) as f:
            self.f = yaml.load(f, Loader=yaml.FullLoader)


if __name__ == "__main__":
    file = ReaderYaml("./example/files/sample.yml")
    file.get_tests()
