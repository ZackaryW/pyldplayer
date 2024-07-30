from functools import cache
import json
import typing
from pyldplayer._internal.model.kmp import KeyboardMapping
from pyldplayer._internal.model.smp import SMP
from pyldplayer.core.path import LDPath
import os

class MappingCollection:
    def __init__(self, path: LDPath):
        self.__path = path

    @classmethod
    def auto(cls):
        return cls(LDPath.auto())

    def pathes(
        self,
        category: typing.Literal["custom", "recommended"] = "custom",
        type: typing.Literal["kmp", "smp"] = "kmp",
    ):
        path = self.__path.customize_configs_folder
        if category == "recommended":
            path = self.__path.recommended_configs_folder

        for filepath in os.listdir(path):
            filepath: str
            if not filepath.endswith(f".{type}"):
                continue

            yield os.path.join(self.__path.customize_configs_folder, filepath)

    def names(
        self,
        category: typing.Literal["custom", "recommended"] = "custom",
        type: typing.Literal["kmp", "smp"] = "kmp"
    ):
        path = self.__path.customize_configs_folder
        if category == "recommended":
            path = self.__path.recommended_configs_folder

        for filepath in os.listdir(path):
            filepath: str
            if not filepath.endswith(f".{type}"):
                continue
            # only name remove extension
            yield os.path.splitext(os.path.basename(filepath))[0]

    @cache
    def get(
        self, 
        name : str,
        category: typing.Literal["custom", "recommended"] = "custom",
        type: typing.Literal["kmp", "smp"] = "kmp"
    ):
        if not name.endswith(f".{type}"):
            name += f".{type}"

        path = self.__path.customize_configs_folder
        if category == "recommended":
            path = self.__path.recommended_configs_folder

        if not os.path.exists(path / name):
            raise FileNotFoundError(f"Record {name} not found")

        with open(path / name, "r") as f:
            raw = json.load(f)

        match type:
            case "kmp": 
                return KeyboardMapping(**raw)
            case "smp": 
                return SMP(**raw)

        raise TypeError(f"Type {type} not supported")            
    
    def save(
        self,
        name: str,
        mapping: typing.Union[KeyboardMapping, SMP],
        category: typing.Literal["custom", "recommended"] = "custom",
    ):
        
        category_path : str = self.__path.customize_configs_folder
        if category == "recommended":
            category_path = self.__path.recommended_configs_folder
        self.get.cache_clear()


        if isinstance(mapping, dict) and any(k in SMP.__annotations__ for k in mapping):
            with open(category_path / f"{name}.smp", "w") as f:
                json.dump(mapping, f, indent=4)

        else:
            with open(category_path / f"{name}.kmp", "w") as f:
                json.dump(mapping, f, indent=4)

    

