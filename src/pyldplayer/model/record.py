from dataclasses import asdict, dataclass, field
import json
from typing import List, Optional, TypedDict


@dataclass
class Point:
    id: int
    x: int
    y: int
    state: Optional[int] = None


@dataclass
class Operation:
    timing: int
    operationId: str
    points: List[Point] = field(default_factory=list)


class RecordInfo(TypedDict):
    loopType: int
    loopTimes: int
    circleDuration: int
    loopInterval: int
    loopDuration: int
    accelerateTimes: int
    accelerateTimesEx: int
    recordName: str
    createTime: str
    playOnBoot: bool
    rebootTiming: int


class ReturnInfo(TypedDict):
    file: str
    info: RecordInfo


@dataclass
class LDRecord:
    _path : str
    recordInfo: RecordInfo
    operations: List[Operation] = field(default_factory=list)
    

    @classmethod
    def load(cls, path : str):
        with open(path, "r") as f:
            data = json.load(f)
        
        return cls(**data, _path=path)

    def save(self):
        with open(self._path, "w") as f:
            json.dump(asdict(self), f, indent=4)


