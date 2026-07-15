import os, enum, requests, asyncio, importlib, discord

class Discord_Event_T(enum.Enum):
    e_none              = 0
    e_joined            = 1
    e_left              = 2
    e_message           = 3,
    e_message_del       = 4,
    e_vc                = 5,
    e_kick              = 6

class Cog:
    HANDLE              : None                          # Loaded Python File
    FILEPATH            : str = None                    # Command Filepath
    NAME                : str = None                    # Name Of The Command
    COMMAND             : str = None                    # Discord Command
    CMD_HANDLER         : None                          # Command Handler
    ARG_COUNT           : int = 0                       # Argument Count
    INVALID_ARGS_ERR    : str | discord.Embed = None    # Invalid argument error
    PASS_BASE           : int = 0                       # Pass the discord ctx base
    INFO                : dict = None
    def __init__(self, name: str, cmd: str, lib, filepath: str, invalid_args_err: str = ""):
        self.NAME = name
        self.COMMAND = cmd
        self.HANDLE = lib
        if hasattr(self.HANDLE, self.COMMAND):
            self.CMD_HANDLER = getattr(lib, self.COMMAND)

        if hasattr(lib, f"__{self.COMMAND.upper()}_INFO__"):
            info: dict = getattr(self.HANDLE, f"__{self.COMMAND.upper()}_INFO__")
            if "Get_Base" in info:
                self.PASS_BASE = info["Get_Base"]
            else: self.PASS_BASE = False

            if "ArgCount" in info:
                self.ARG_COUNT = info["ArgCount"]
            else: self.ARG_COUNT = 0

            if "Invalid_Arg_Err" in info:
                self.INVALID_ARGS_ERR = info["Invalid_Arg_Err"]

            self.INFO = info
        else:
            print(f"| '{self.COMMAND}' Missing Info", end = " ")
        print("")

        self.FILEPATH = filepath
        self.INVALID_ARGS_ERR = invalid_args_err

class dCog:
    DEFAULT_DIR         : str = "/cmds"
    Commands            : list[Cog] = []
    def __init__(self, dir_path: str = None):
        if dir_path:
            self.DEFAULT_DIR = dir_path

        dCog.retrieve_all_commands(self.DEFAULT_DIR, 0, self.Commands)
    
    @staticmethod
    def retrieve_all_commands(dir: str, inner_dir: int = 0, Cmds: list = None) -> dict:
        CURRENT_DIR = os.getcwd() + dir
        if not dir or dir == "":
            return

        Files = {}

        dir_list = os.listdir(CURRENT_DIR)
        i = 0
        for item in dir_list:
            if item.endswith(".py"):
                Files[item] = f"{CURRENT_DIR}/{item}"
                print(f"Loading Command: {Files[item]}", end = " ")
                name = item.replace(".py", "")
                Cmds.append(Cog(name, name, dCog.load_object_from_file(f"{name}_cmd", f"{CURRENT_DIR}/{item}", name), f"{CURRENT_DIR}/{item}"))

            if os.path.isdir(f"{CURRENT_DIR}/{item}"):
                dir += f"/{item}"
                Files.update(dCog.retrieve_all_commands(dir, inner_dir + 1, Cmds))
                dir = dir.replace(f"/{item}", "")

            i += 1

        if len(Files) > 0:
            return Files
        
        return {}

    @staticmethod
    def load_object_from_file(name: str, path: str, object_name):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module
        # return getattr(module, object_name) # gets the actual function from file