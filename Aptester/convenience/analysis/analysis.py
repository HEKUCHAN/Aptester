from os import PathLike
from typing import Union
from pathlib import Path
from convenience import File, FileSuffix, FileJson, FileText, FileYaml


class Analysis:
    def __init__(self, file_path: Union[str, bytes, PathLike]):
        __file = File(file_path)

        if __file.suffix == FileSuffix.TEXT or __file.suffix == FileSuffix.OTHER:
            __file_object = FileText(__file)
        elif __file.suffix == FileSuffix.JSON:
            __file_object = FileJson(__file)
        elif __file.suffix == FileSuffix.YAML:
            __file_object = FileYaml(__file)

        self.file = __file_object

    @classmethod
    def is_can_analysis(cls, file_path):
        file = File(file_path)
        if file.is_valid():
            return True
        return False
