
import logging
import typing
import inspect
import pyldplayer._internal.iconsole as I
from pyldplayer._internal.model.list2meta import List2Meta
from pyldplayer.core.path import LDPath
from pyldplayer.utils import open_detached, query, queryCtx


class Console(I.IConsole):
    def __init__(self, path : LDPath):
        self.__path = path

    @property
    def path(self) -> LDPath:
        return self.__path

    @classmethod
    def auto(cls):
        return cls(LDPath.auto())
    
    def list2(self) -> typing.List[List2Meta]:
        """
        Retrieves a list of List2Meta objects by querying the ldconsole_path with the "list2" command.
        
        Returns:
            typing.List[List2Meta]: A list of List2Meta objects representing the retrieved data.
        """
        res = query(self.path.ldconsole_path, "list2")
        res = res.decode()
        reslines = res.splitlines()
        return [List2Meta(**{k : v if not v.isdigit() else int(v) for k, v in zip(List2Meta.__annotations__, resline.split(","))}) for resline in reslines]

    def globalsetting(
        self,
        fps: typing.Optional[int] = None,
        audio: typing.Optional[bool] = None,
        fastplay: typing.Optional[bool] = None,
        cleanmode: typing.Optional[bool] = None,
    ):
        """
        Sets global settings for the console.

        Args:
            fps (int, optional): The frames per second setting. Defaults to None.
            audio (bool, optional): Whether to enable audio. Defaults to None.
            fastplay (bool, optional): Whether to enable fast play. Defaults to None.
            cleanmode (bool, optional): Whether to enable clean mode. Defaults to None.

        Returns:
            Console: The current Console instance.
        """
        arglist = []
        if fps is not None:
            arglist.extend(["--fps", str(fps)])
        if audio is not None:
            arglist.extend(["--audio", 1 if audio else 0])
        if fastplay is not None:
            arglist.extend(["--fastplay", 1 if fastplay else 0])
        if cleanmode is not None:
            arglist.extend(["--cleanmode", 1 if cleanmode else 0])
        open_detached(self.path.ldconsole_path, "globalsetting", *arglist)
        return self

    def modify(
        self,
        name: typing.Optional[typing.Optional[str]] = None,
        index: typing.Optional[typing.Optional[int]] = None,
        resolution: typing.Optional[str] = None,
        cpu: typing.Optional[typing.Literal[1, 2, 3, 4]] = None,
        memory: typing.Optional[
            typing.Literal[256, 512, 768, 1024, 2048, 4096, 8192]
        ] = None,
        manufacturer: typing.Optional[str] = None,
        model: typing.Optional[str] = None,
        pnumber: typing.Optional[int] = None,
        imei: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        imsi: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        simserial: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        androidid: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        mac: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        autorotate: typing.Optional[bool] = None,
        lockwindow: typing.Optional[bool] = None,
        root: typing.Optional[bool] = None,
    ):
        arglist = []
        if not name and not index:
            raise ValueError("Either name or index must be provided")
        if name is not None and isinstance(name, str):
            arglist.extend(["--name", name])
        else:
            arglist.extend(["--index", str(index)])

        if resolution is not None:
            arglist.extend(["--resolution", resolution])
        if cpu is not None:
            arglist.extend(["--cpu", str(cpu)])
        if memory is not None:
            arglist.extend(["--memory", str(memory)])
        if manufacturer is not None:
            arglist.extend(["--manufacturer", manufacturer])
        if model is not None:
            arglist.extend(["--model", model])
        if pnumber is not None:
            arglist.extend(["--pnumber", str(pnumber)])
        if imei is not None:
            arglist.extend(["--imei", str(imei)])
        if imsi is not None:
            arglist.extend(["--imsi", str(imsi)])
        if simserial is not None:
            arglist.extend(["--simserial", str(simserial)])
        if androidid is not None:
            arglist.extend(["--androidid", str(androidid)])
        if mac is not None:
            arglist.extend(["--mac", str(mac)])
        if autorotate is not None:
            arglist.extend(["--autorotate", 1 if autorotate else 0])
        if lockwindow is not None:
            arglist.extend(["--lockwindow", 1 if lockwindow else 0])
        if root is not None:
            arglist.extend(["--root", 1 if root else 0])
        open_detached(self.path.ldconsole_path, "modify", *arglist)

def _create_simple_exec_method(command: str):
    def method(self) -> None:
        logging.info(f"Running exec command: {command}")
        open_detached(self.path.ldconsole_path, command)
    return method   

for se in I.SIMPLE_EXEC_LIST:
    setattr(Console, se, _create_simple_exec_method(se))


def _create_varied_method(func: typing.Callable, methodToUse : typing.Callable):
    def method(self, *args, **kwargs):
        logging.info(f"Running exec command: {func.__name__}")

        # Start building the command list with the base command
        command_list = [func.__name__]

        # Get the signature of the function
        sig = inspect.signature(func)
        parameters = list(sig.parameters.values())

        # Check if 'name' and 'index' are in the parameters
        has_name_param = any(param.name == 'name' for param in parameters)
        has_index_param = any(param.name == 'index' for param in parameters)

        # Handle the special case of a single positional argument
        if len(args) == 1 and has_name_param and has_index_param:
            if 'name' not in kwargs and isinstance(args[0], str):
                kwargs['name'] = args[0]
            elif 'index' not in kwargs and isinstance(args[0], int):
                kwargs['index'] = args[0]
            else:
                # If the single argument does not match, treat it as a normal argument
                for i, arg in enumerate(args):
                    if i < len(parameters):
                        param_name = parameters[i].name
                        command_list.extend([f"--{param_name}", arg])
        else:
            # Handle multiple positional arguments
            for i, arg in enumerate(args):
                if i < len(parameters):
                    param_name = parameters[i].name
                    command_list.extend([f"--{param_name}", arg])

        # Handle keyword arguments
        for param in parameters[len(args):]:
            param_name = param.name
            param_type = param.annotation

            if param_name in kwargs:
                param_value = kwargs[param_name]
                if param_value is not None:
                    command_list.extend([f"--{param_name}", param_value])
            else:
                if param_type is I.SOptional:
                    raise ValueError(f"Mandatory parameter '{param_name}' is missing")

        # Execute the command
        return methodToUse(self.path.ldconsole_path, *command_list)

    return method

for ve in I.VARIED_EXEC_LIST:
    func = getattr(I.IConsole, ve)
    setattr(Console, ve, _create_varied_method(func, open_detached))

def _simple_query_method(command : str):
    def method(self) -> None:
        logging.info(f"Running query command: {command}")
        return query(self.path.ldconsole_path, command)
    return method

for sq in I.SIMPLE_QUERY_LIST:
    setattr(Console, sq, _simple_query_method(sq))

for eq in I.VARIED_QUERY_LIST:
    func = getattr(I.IConsole, eq)
    
    setattr(Console, eq, _create_varied_method(func, query))