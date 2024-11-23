
import typing
import pyldplayer.i.console as I
from pyldplayer.coms.appattr import ContainLDAppAttrI, LDAppAttr
from pyldplayer.coms.console import LDConsole
from pyldplayer.model.queryObj import QueryObj

class LDBatchConsole(I.LDConsoleI, ContainLDAppAttrI):
    """
    A wrapper class for executing LDPlayer console commands in batch mode.

    This class provides functionality to execute commands across multiple LDPlayer instances
    that match specified query criteria. It supports:
    - Batch execution of supported commands
    - Pre and post execution callbacks
    - Query-based instance selection
    - Automatic command routing to single or batch execution

    The class maintains separate callback lists at both class and instance levels.
    Class level callbacks are shared across all instances while instance callbacks
    are specific to each instance.

    Attributes:
        pre_callbacks (List[Callable]): List of callbacks to execute before each command
        post_callbacks (List[Callable]): List of callbacks to execute after each command
    """
    pre_callbacks : typing.List[typing.Callable] = []
    post_callbacks : typing.List[typing.Callable] = []

    def __init__(self, attr : LDAppAttr = None):
        ContainLDAppAttrI.__init__(self, attr)
        self.__console = LDConsole(self.attr)

    def __getattribute__(self, key : str):
        if key.startswith("_"):
            return super().__getattribute__(key)
        if key in I.BATCHABLE_COMMANDS:
            return self.__batch_command(key)
        if key in I.VARIED_EXEC_LIST or key in I.SIMPLE_EXEC_LIST:
            return getattr(self.__console, key)
        return super().__getattribute__(key)

    def __batch_command(self, key : str):
        def wrapper( query, *args, **kwargs):
            queryObj = QueryObj.parse(query)
            consoleMethod = getattr(self.__console, key)
            for meta in self.__console.list2():
                if queryObj.validate(meta):
                    for callback in self.pre_callbacks:
                        callback(meta)
                    consoleMethod(index = meta["id"], *args, **kwargs)
                    for callback in self.post_callbacks:
                        callback(meta)

        return wrapper
    
    @classmethod
    def cls_add_pre_callback(cls, callback : typing.Callable):
        cls.pre_callbacks.append(callback)

    @classmethod
    def cls_add_post_callback(cls, callback : typing.Callable):
        cls.post_callbacks.append(callback)

    def add_pre_callback(self, callback : typing.Callable):
        self.pre_callbacks.append(callback)

    def add_post_callback(self, callback : typing.Callable):
        self.post_callbacks.append(callback)

    def add_interval(self, pre : bool = False, interval : int = 5):
        w = {}
        exec(
            f"""def w(meta):
    import time
    time.sleep({interval})""",
            {}, w
        )

        if pre:
            self.pre_callbacks.append(w["w"])
        else:
            self.post_callbacks.append(w["w"])
