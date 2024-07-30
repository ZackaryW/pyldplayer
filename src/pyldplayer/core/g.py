
from pyldplayer.core.path import LDPath

_global_path : LDPath = None

def Global(path : str = None):
    global _global_path
    if path:
        _global_path = LDPath(path)
        return _global_path
    
    if _global_path:
        return _global_path
    
    raise Exception("Global path not set")

    
__all__ = ["Global"]

