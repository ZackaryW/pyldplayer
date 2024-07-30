from functools import cache
import json
import os
from pyldplayer._internal.model.record import OperationRecord
from pyldplayer.core.path import LDPath
from dataclasses import asdict

class RecordCollection:
    def __init__(self, path: LDPath):
        self.__path = path

    def pathes(self):
        for filepath in os.listdir(self.__path.operation_records_folder):
            filepath: str
            if not filepath.endswith(".record"):
                continue

            yield os.path.join(self.__path.operation_records_folder, filepath)

    def names(self):
        for filepath in os.listdir(self.__path.operation_records_folder):
            filepath: str
            if not filepath.endswith(".record"):
                continue
            # only name remove extension
            yield os.path.splitext(os.path.basename(filepath))[0]

    @cache
    def get(self, name: str):
        if not name.endswith(".record"):
            name += ".record"

        if not os.path.exists(self.__path.operation_records_folder / name):
            raise FileNotFoundError(f"Record {name} not found")

        with open(self.__path.operation_records_folder / name, "r") as f:
            raw = json.load(f)

        return OperationRecord(**raw)

    def save(self, name: str, record: OperationRecord):
        self.get.cache_clear()

        with open(self.__path.operation_records_folder / name, "w") as f:
            json.dump(asdict(record), f, indent=4)

    @classmethod
    def auto(cls):
        return cls(LDPath.auto())
