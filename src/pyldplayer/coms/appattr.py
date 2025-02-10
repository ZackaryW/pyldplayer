from functools import cached_property
import os
import typing

class LDAppAttrMeta(type):
    _pathes : dict[str, 'LDAppAttr'] = {}
    _first : 'LDAppAttr' = None
    _defaultMethodOverloads : typing.ClassVar[typing.List[typing.Callable]] = []

    def __call__(cls, root : str = None, **kwargs):
        if not root and cls._first:
            return cls._first

        if not root and cls._defaultMethodOverloads:
            for method in cls._defaultMethodOverloads:
                root = method()
                if root:
                    break

        if not root:
            raise ValueError("path is required")

        assert os.path.exists(root), f"Path '{root}' does not exist"
        root = os.path.abspath(root)

        if root in cls._pathes:
            return cls._pathes[root]

        if any(root in path for path in cls._pathes):
            raise ValueError(f"Path '{root}' cannot be a subpath of an existing LDPlayer installation")

        cls._pathes[root] = super().__call__(root, **kwargs)
        
        if cls._first is None:
            cls._first = cls._pathes[root]
        
        return cls._pathes[root]
    
    def _registerDefaultMethodOverload(cls, method : typing.Callable):
        cls._defaultMethodOverloads.append(method)



class LDAppAttr(metaclass=LDAppAttrMeta):
    def __init__(self, root : str, **kwargs):
        self.__root = root
        self.__map = {
            "dnconsole" : kwargs.get("dnconsole", os.path.join(self.root, "dnconsole.exe")),
            "ldconsole" : kwargs.get("ldconsole", os.path.join(self.root, "ldconsole")),
            "vmfolder" : kwargs.get("vmfolder", os.path.join(self.root, "vms")),
            "customizeConfigs" : kwargs.get("customizeConfigs", os.path.join(self.root, "customizeConfigs")),
            "recommendedConfigs" : kwargs.get("recommendedConfigs", os.path.join(self.root, "recommendedConfigs")),
            "operationRecords" : kwargs.get("operationRecords", os.path.join(self.root, "operationRecords")),   
            "config" : kwargs.get("config", os.path.join(self.root, "config")),
        }

    @cached_property
    def valid(self):
        return all(os.path.exists(path) for path in self.__map.values())

    @property
    def root(self):
        return self.__root

    @property
    def dnconsole(self):
        return self.__map["dnconsole"]

    @property
    def ldconsole(self):
        return self.__map["ldconsole"]

    @property
    def vmfolder(self):
        return self.__map["vmfolder"]

    @property
    def customizeConfigs(self):
        return self.__map["customizeConfigs"]
    
    @property
    def recommendedConfigs(self):
        return self.__map["recommendedConfigs"]

    @property
    def operationRecords(self):
        return self.__map["operationRecords"]
    
    @property
    def config(self):
        return self.__map["config"]

    @classmethod
    def setDefault(cls, path : str):
        assert path, "path is required"
        cls._first = cls(path)

    def __hash__(self):
        return hash(self.root)

class ContainLDAppAttrMeta(type):
    _instances : typing.ClassVar[typing.Dict[typing.Tuple[LDAppAttr, typing.Type], 'ContainLDAppAttrI']] = {}

    def __call__(cls, attr : LDAppAttr = None, *args, **kwargs):
        if attr is None:
            attr = LDAppAttr()

        if (attr, cls) in cls._instances:
            return cls._instances[(attr, cls)]

        instance = super().__call__(attr, *args, **kwargs)
        cls._instances[(attr, cls)] = instance
        return instance

class ContainLDAppAttrI(metaclass=ContainLDAppAttrMeta):
    def __init__(self, attr: LDAppAttr = None):
        self.__attr = attr
        assert isinstance(attr, LDAppAttr)

    @property
    def attr(self):
        return self.__attr


"""
conviniently detect LDPlayer path from environment variable
"""
@LDAppAttr._registerDefaultMethodOverload
def detect_os_env():
    try:
        import dotenv
        dotenv.load_dotenv()
    except ImportError:
        pass


    return os.environ.get("LDPLAYER_PATH", None)
  
    
