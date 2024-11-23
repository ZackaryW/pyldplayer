from dataclasses import asdict, dataclass
import json
from typing import TypedDict
import typing
from ..utils import flatten_nested_dict, parse_dotted_dict


class WindowsPosition(TypedDict):
    x: int
    y: int

class BasicSettings(TypedDict):
    lastIp : typing.Optional[str]

@dataclass
class LeidiansConfig:
    nextCheckupdateTime: int
    hasPluginLast: bool
    strp: str
    lastZoneArea: str
    lastZoneName: str
    vipMode: bool
    isBaseboard: bool
    basicSettings: BasicSettings
    noiceUserRed: bool
    isFirstInstallApk: bool
    cloneFromSmallDisk: bool
    languageId: str
    mulTab: bool
    exitFullscreenEsc: bool
    disableMouseRightOpt: bool
    nextUpdateTime: int
    ignoreVersion: str
    framesPerSecond: int
    reduceAudio: bool
    displayMode: bool
    vmdkFastMode: bool
    windowsAlignType: int
    windowsRowCount: int
    windowsAutoSize: bool
    sortwndnotoutscreen: bool
    moreScreenSortInSame: bool
    windowsOrigin: WindowsPosition
    windowsOffset: WindowsPosition
    batchStartInterval: int
    batchNewCount: int
    batchCloneCount: int
    windowsRecordPos: bool
    multiPlayerSort: int
    isSSD: bool
    fromInstall: bool
    productLanguageId: str
    channelOpenId: str
    channelLastOpenId: str
    operaRecordFirstDo: bool
    remoteEntranceVersion: int
    _path: str

    @classmethod
    def load(cls, path : str):
        with open(path, 'r') as f:
            data = json.load(f)
            data = parse_dotted_dict(data)

        
            data = {k : v for k, v in data.items() if k in cls.__dataclass_fields__}

        return cls(**data, _path=path)

    def save(self):
        with open(self._path, 'w') as f:
            json.dump(flatten_nested_dict(asdict(self)), f, indent=4)
