import os
from pyldplayer.utils import CachableProperty


class LDPathMeta(type):
    _instances = {}

    def __call__(cls, path: str):
        if not os.path.exists(path):
            raise ValueError(f"Path '{path}' does not exist")

        path = os.path.abspath(path)

        if os.path.isfile(path):
            folder = os.path.dirname(path)
        else:
            folder = path

        folder = os.path.abspath(folder)

        if "dnconsole.exe" in os.listdir(path):
            cls._instances[folder] = super().__call__(folder)

            return cls._instances[folder]

        raise ValueError(f"Path '{path}' is not a valid LDPlayer installation")


class LDPath(metaclass=LDPathMeta):
    def __init__(self, path: str):
        self.__path = path

    @CachableProperty
    def vms_folder(self):
        return os.path.join(self.__path, "vms")

    @CachableProperty
    def dnconsole_path(self):
        return os.path.join(self.__path, "dnconsole.exe")

    @CachableProperty
    def ldconsole_path(self):
        return os.path.join(self.__path, "ldconsole")

    @CachableProperty
    def customize_configs_folder(self):
        return os.path.join(self.vms_folder, "customizeConfigs")

    @CachableProperty
    def recommended_configs_folder(self):
        return os.path.join(self.vms_folder, "recommendedConfigs")

    @CachableProperty
    def operation_records_folder(self):
        return os.path.join(self.vms_folder, "operationRecords")

    @CachableProperty
    def config_folder(self):
        return os.path.join(self.vms_folder, "config")

    @classmethod
    def auto(cls):
        from pyldplayer.core.g import Global

        try:
            return Global()
            
        except: # noqa
            if "PYLDPLAYER_PATH" in os.environ:
                return Global(os.environ["PYLDPLAYER_PATH"])
            
            
                


            