
from functools import cache
import json
import os
from pyldplayer._internal.model.leidians import LeidiansConfig
from pyldplayer.core.path import LDPath
from pyldplayer.utils import parse_dotted_dict, flatten_nested_dict

class ConfigCollection:
    def __init__(self, path : LDPath):
        self.__path = path

    @property
    def default_path(self):
        return os.path.join(self.__path.config_folder, 'leidians.config')
    
    def default_config(self, savedata : LeidiansConfig = None):
        if savedata:
            with open(self.default_path, 'w') as f: 
                json.dump(flatten_nested_dict(savedata), f, indent=4)
            return

        with open(self.default_path, 'r') as f:
            return LeidiansConfig(**parse_dotted_dict(json.load(f)))
    
    @cache
    def get_config(
        self,
        id : int
    ):
        with open(os.path.join(self.__path.config_folder, f'leidian{id}.config'), 'r') as f:
            return LeidiansConfig(**parse_dotted_dict(json.load(f)))
        
    def save_config(
        self,
        id : int,
        config : LeidiansConfig
    ):
        with open(os.path.join(self.__path.config_folder, f'leidian{id}.config'), 'w') as f:
            json.dump(flatten_nested_dict(config), f, indent=4)

    @classmethod
    def auto(cls):
        return cls(LDPath.auto())