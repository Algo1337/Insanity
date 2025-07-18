import os, sys

CommandsDir = "/src/cmds/"
CURRENT_DIR = os.getcwd() + CommandsDir

Files = {}

def check_dir(dir: str) -> int:
    if dir == "":
        return 0

    global Files
    global CURRENT_DIR

    dir_list = os.listdir(CURRENT_DIR)
    for item in dir_list:
        if item.endswith(".py"):
            Files[item] = f"{CURRENT_DIR}{item}"
        if os.path.isdir(f"{CURRENT_DIR}{item}"):
            CURRENT_DIR += f"/{item}"
            check_dir(CURRENT_DIR)
            CURRENT_DIR = CURRENT_DIR.replace(f"/{item}", "")

    return 1

check_dir(CURRENT_DIR)
for file in Files:
    print(f"{file} | {Files[file]}")

# if len(sys.argv) < 2:
#     print(f"[ x ] Error, Invalid arguments\nUsage: {sys.argv[0]} <commands_dir>")
#     exit(0)