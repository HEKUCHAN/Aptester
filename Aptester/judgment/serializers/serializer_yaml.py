import yaml

from Aptester.judgment.reader import Reader


class ReaderYaml(Reader):
    def __init__(self, path) -> None:
        super().__init__(path)

    def open(self) -> None:
        with open(self.path) as f:
            self.f = yaml.load_safe(f)
            print(self.f)


if __name__ == "__main__":
    file = ReaderYaml("./example/files/sample.yml")
    file.get_tests()
