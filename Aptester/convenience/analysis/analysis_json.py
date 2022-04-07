import json
from typing import Dict, Union
from convenience.file import File


class FileJson(File):
    def __init__(self, file_path):
        super().__init__(file_path)
        with open(file_path, "r") as f:
            self.data = json.load(f.read())

    def get_informations(self) -> Union[None, Dict[str]]:
        if not self.data["information"] is None:
            information = self.data["information"]
            data = {}

            if not information["author"] is None:
                data["author"] = information["author"]
            if not information["name"] is None:
                data["name"] = information["name"]
            if not information["description"] is None:
                data["description"] = information["description"]

            return data
        return None

    def get_configs(self):
        if not self.data["config"] is None:
            pass