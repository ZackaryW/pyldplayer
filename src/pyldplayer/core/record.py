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

    def get(self, name: str):
        rawstr = self.getStr(name)
        raw = json.loads(rawstr)
        return OperationRecord(**raw)
    
    @cache
    def getStr(self, name: str):
        if not name.endswith(".record"):
            name += ".record"
        if not os.path.exists(os.path.join(self.__path.operation_records_folder, name)):
            raise FileNotFoundError(f"Record {name} not found")

        with open(os.path.join(self.__path.operation_records_folder, name), "r") as f:
            return f.read()
    
    def save(self, name: str, record: OperationRecord):
        self.getStr.cache_clear()

        with open(os.path.join(self.__path.operation_records_folder, name), "w") as f:
            json.dump(asdict(record), f, indent=4)

    @classmethod
    def auto(cls):
        return cls(LDPath.auto())
