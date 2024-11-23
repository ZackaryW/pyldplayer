from functools import cached_property
import os
import typing

class LDAppAttrMeta(type):
    _pathes : dict[str, 'LDAppAttr'] = {}
    _first : str = None
    _defaultMethodOverloads : typing.ClassVar[typing.List[typing.Callable]] = []

    def __call__(cls, root : str = None):
        if not root:
            if cls._first:
                root = cls._first
            elif cls._defaultMethodOverloads:
                for method in cls._defaultMethodOverloads:
                    root = method()
                    if root:
                        break
                
        if not root:
            raise ValueError("path is required")

        if root in cls._pathes:
            return cls._pathes[root]

        assert os.path.exists(root), f"Path '{root}' does not exist"
        root = os.path.abspath(root)

        if any(root in path for path in cls._pathes):
            raise ValueError(f"Path '{root}' cannot be a subpath of an existing LDPlayer installation")

        cls._pathes[root] = super().__call__(root)
        if cls._first is None:
            cls._first = root
        return cls._pathes[root]

class LDAppAttr(metaclass=LDAppAttrMeta):
    def __init__(self, root : str):
        self.__root = root

    @property
    def root(self):
        return self.__root

    @cached_property
    def dnconsole(self):
        return os.path.join(self.root, "dnconsole.exe")

    @cached_property
    def ldconsole(self):
        return os.path.join(self.root, "ldconsole")

    @cached_property
    def vmfolder(self):
        return os.path.join(self.root, "vms")

    @cached_property
    def customizeConfigs(self):
        return os.path.join(self.vmfolder, "customizeConfigs")
    
    @cached_property
    def recommendedConfigs(self):
        return os.path.join(self.vmfolder, "recommendedConfigs")

    @cached_property
    def operationRecords(self):
        return os.path.join(self.vmfolder, "operationRecords")

    @cached_property
    def config(self):
        return os.path.join(self.vmfolder, "config")

    @classmethod
    def setDefault(cls, path : str):
        assert path, "path is required"
        cls._first = cls(path)

    @classmethod
    def _registerDefaultMethodOverload(cls, method : typing.Callable):
        cls._defaultMethodOverloads.append(method)

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
    return os.environ.get("LDPLAYER_PATH", None)
  
    
