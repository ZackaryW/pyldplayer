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
