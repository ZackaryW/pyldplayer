from dataclasses import dataclass
import json
from typing import TypedDict


class SMP(TypedDict):
    reduceInertia: bool
    keyboardShowGreet: bool
    joystickShowGreet: bool
    keyboardFirstGreet: bool
    joystickFirstGreet: bool
    keyboardShowHints: bool
    joystickShowHints: bool
    keyboardIgnoreVersion: int
    joystickIgnoreVersion: int
    noticeTimes: int
    noticeHash: int
    resolutionRelatives: dict

@dataclass
class SMPFile:
    _path : str
    smp: SMP
    

    @classmethod
    def load(cls, path : str):
        with open(path, "r") as f:
            data = json.load(f)
        
        return cls(smp=SMP(**data), _path=path)
    
    def save(self):
        with open(self._path, "w") as f:
            json.dump(self.smp, f, indent=4)
