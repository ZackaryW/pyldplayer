import logging
import os
import subprocess
import typing

class CachableProperty:
    def __init__(self, func):
        self.func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, None)
        if value is None:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value

    def __set__(self, obj, value):
        obj.__dict__[self.__name__] = value

    def __delete__(self, obj):
        if self.__name__ in obj.__dict__:
            del obj.__dict__[self.__name__]

#
def flatten_nested_dict(data: dict, parent_key: str = "", sep: str = ".") -> dict:
    """
    Flattens a nested dictionary into a single-level dictionary.

    Args:
        data (dict): The nested dictionary to be flattened.
        parent_key (str, optional): The parent key of the current dictionary. Defaults to ''.
        sep (str, optional): The separator used to join the parent key and the current key. Defaults to '.'.

    Returns:
        dict: The flattened dictionary.

    Example:
        >>> data = {'a': {'b': 1, 'c': {'d': 2}}}
        >>> flatten_nested_dict(data)
        {'a.b': 1, 'a.c.d': 2}
    """
    items = []
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_nested_dict(value, new_key, sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def parse_dotted_dict(data: dict):
    """
    Parses a dictionary with dotted keys into a nested dictionary.

    Args:
        data (dict): The dictionary to be parsed.

    Returns:
        dict: The parsed dictionary with nested structure.

    Example:
        >>> data = {'a.b': 1, 'a.c.d': 2}
        >>> parse_dotted_dict(data)
        {'a': {'b': 1, 'c': {'d': 2}}}
    """
    result = {}
    for key, value in data.items():
        keys = key.split(".")
        temp = result
        for k in keys[:-1]:
            temp = temp.setdefault(k, {})
        temp[keys[-1]] = value
    return result

# subproc
def open_detached(path: str, *args) -> None:
    """
    Opens a new process in a detached state.

    Args:
        path (str): The path to the executable file.
        *args: Additional arguments to be passed to the executable.

    Returns:
        None: This function does not return anything.

    Description:
        This function uses the `subprocess.Popen` method to create a new process
        and execute the specified executable file with the given arguments. The
        process is created in a detached state, meaning it runs independently
        of the parent process. The standard input, output, and error streams of
        the process are set to be pipes. The `creationflags` parameter is used
        to specify the creation flags for the process, including `DETACHED_PROCESS`,
        `CREATE_NEW_PROCESS_GROUP`, and `CREATE_BREAKAWAY_FROM_JOB`.

    Example:
        ```python
        open_detached("path/to/executable", "arg1", "arg2")
        ```
    """

    cmd = [path] + [str(arg) for arg in args]
    logging.info(f"Subprocess detached run: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            
            creationflags=(
                subprocess.DETACHED_PROCESS
                | subprocess.CREATE_NEW_PROCESS_GROUP
                | subprocess.CREATE_BREAKAWAY_FROM_JOB
            ),
          
        )
        logging.info(f"Subprocess started with PID: {process.pid}")
    except Exception as e:
        logging.error(f"Failed to start subprocess: {e}")

def query_bytes(
    path: str,
    *args,
    timeout: int = None,
):
    """
    Executes a subprocess and returns the captured output as bytes.

    Args:
        path (str): The path to the executable to run.
        *args: Additional arguments to pass to the executable.
        timeout (int, optional): The maximum time in seconds to wait for the subprocess to complete. If not provided, the `DEFAULT_QUERY_TIMEOUT` value will be used.

    Raises:
        subprocess.TimeoutExpired: If the subprocess takes longer than the specified timeout to complete.
        subprocess.CalledProcessError: If the subprocess returns a non-zero exit code.

    Returns:
        bytes: The captured output of the subprocess.
    """
    timeout = timeout or 5
    try:
        command = [path, *(str(arg) for arg in args)]
        proc = subprocess.run(command, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise e
    except subprocess.CalledProcessError as e:
        raise e

    return proc.stdout


def query(path: str, *args, timeout: int = None, strip: bool = False):
    """
    Executes a subprocess and returns the captured output as a string.

    Args:
        path (str): The path to the executable to run.
        *args: Additional arguments to pass to the executable.
        timeout (int, optional): The maximum time in seconds to wait for the subprocess to complete. If not provided, the `DEFAULT_QUERY_TIMEOUT` value will be used.

    Raises:
        subprocess.TimeoutExpired: If the subprocess takes longer than the specified timeout to complete.
        subprocess.CalledProcessError: If the subprocess returns a non-zero exit code.

    Returns:
        str: The captured output of the subprocess as a string.
    """
    raw = query_bytes(path, *args, timeout=timeout)
    return raw.decode("utf-8").strip() if strip else raw.decode("utf-8")
