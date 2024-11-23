from dataclasses import asdict, dataclass
import json
from typing import TypedDict, Optional
import typing

from pyldplayer.utils import parse_dotted_dict, flatten_nested_dict


class HotkeySettings(TypedDict):
    backKey: dict
    homeKey: dict
    appSwitchKey: dict
    menuKey: dict
    zoomInKey: dict
    zoomOutKey: dict
    bossKey: dict
    shakeKey: dict
    operationRecordKey: dict
    fullScreenKey: dict
    showMappingKey: dict
    videoRecordKey: dict
    mappingRecordKey: dict
    keyboardModelKey: dict


class KeyConfig(TypedDict):
    modifiers: int
    key: int


class ResolutionSettings(TypedDict):
    width: int
    height: int


class AdvancedSettings(TypedDict):
    resolution: ResolutionSettings
    resolutionDpi: int
    cpuCount: int
    memorySize: int
    micphoneName: Optional[str]
    speakerName: Optional[str]


class BasicSettings(TypedDict):
    left: int
    top: int
    width: int
    height: int
    realHeigh: int
    realWidth: int
    isForstStart: bool
    mulFsAddSize: int
    mulFsAutoSize: int
    verticalSync: bool
    fsAutoSize: int
    noiceHypeVOpen: bool
    autoRun: bool
    rootMode: bool
    heightFrameRate: bool
    adbDebug: int
    autoRotate: bool
    isForceLandscape: bool
    standaloneSysVmdk: bool
    lockWindow: bool
    disableMouseFastOpt: bool
    cjztdisableMouseFastOpt_new: int
    HDRQuality: int
    qjcjdisableMouseFast: int
    fps: int
    astc: bool
    rightToolBar: bool


class NetworkSettings(TypedDict):
    networkEnable: bool
    networkSwitching: bool
    networkStatic: bool
    networkAddress: str
    networkGateway: str
    networkSubnetMask: str
    networkDNS1: str
    networkDNS2: str
    networkInterface: Optional[str]


class PropertySettings(TypedDict):
    phoneIMEI: str
    phoneIMSI: str
    phoneSimSerial: str
    phoneAndroidId: str
    phoneModel: str
    phoneManufacturer: str
    macAddress: str
    phoneNumber: Optional[str]


class StatusSettings(TypedDict):
    sharedApplications: str
    sharedPictures: str
    sharedMisc: str
    closeOption: int
    playerName: str


@dataclass
class LeidianConfig:
    _path : str
    propertySettings: PropertySettings
    statusSettings: StatusSettings
    basicSettings: BasicSettings
    networkSettings: NetworkSettings
    advancedSettings: typing.Optional[AdvancedSettings] = None
    hotkeySettings: typing.Optional[HotkeySettings] = None
    

    @classmethod
    def load(cls, path : str):
        with open(path, 'r') as f:
            data = json.load(f)
            data = parse_dotted_dict(data)

        return cls(**data, _path=path)

    def save(self):
        with open(self._path, 'w') as f:
            json.dump(flatten_nested_dict(asdict(self)), f, indent=4)

