import logging
import subprocess

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
