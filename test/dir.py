import os, sys

CommandsDir = "/src/cmds/"

Files = {}

"""
    {
        "file": "filepath"
    }
"""
def check_dir(dir: str) -> int:
    CURRENT_DIR = os.getcwd() + dir
    if not dir or dir == "":
        return

    Files = {}

    dir_list = os.listdir(CURRENT_DIR)
    for item in dir_list:
        if item.endswith(".py"):
            Files[item] = f"{CURRENT_DIR}{item}"
        if os.path.isdir(f"{CURRENT_DIR}{item}"):
            CURRENT_DIR += f"/{item}"
            check_dir(CURRENT_DIR)
            CURRENT_DIR = CURRENT_DIR.replace(f"/{item}", "")

    if len(Files) > 0:
        return Files
    
    return {}

check_dir(CommandsDir)