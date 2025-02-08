
SIMPLE_EXEC_LIST = [
    "rock",
    "zoomOut",
    "zoomIn",
    "sortWnd",
    "quitall"
]

VARIED_EXEC_LIST = [
    "quit",
    "launch",
    "reboot",
    "copy",
    "add",
    "remove",
    "rename",
    "installapp",
    "uninstallapp",
    "runapp",
    "killapp",
    "locate",
    "adb",
    "setprop",
    "downcpu",
    "backup",
    "restore",
    "action",
    "scan",
    "pull",
    "push",
    "backupapp",
    "restoreapp",
    "launchex",
    "operaterecord",
]

SIMPLE_QUERY_LIST = ["list", "runninglist"]

VARIED_QUERY_LIST = ["isrunning", "getprop", "operatelist", "operateinfo"]

BATCHABLE_COMMANDS = [
    "modify",
    "quit",
    "launch",
    "reboot",
    "installapp",
    "uninstallapp",
    "runapp",
    "killapp",
    "pull",
    "push",
    "backupapp",
    "restoreapp",
    "launchex",
]

FULL_COMMANDS_LIST = SIMPLE_EXEC_LIST + VARIED_EXEC_LIST + SIMPLE_QUERY_LIST + VARIED_QUERY_LIST

FULL_COMMANDS_LIST.extend(["list2", "modify", "globalsetting"])