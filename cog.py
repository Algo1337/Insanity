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
    def __init__(self, name: str, cmd: str, lib, filepath: str, invalid_args_err: str = ""):
        self.NAME = name
        self.COMMAND = cmd
        self.HANDLE = lib
        if hasattr(self.lib, self.cmd):
            self.CMD_HANDLER = getattr(lib, self.COMMAND)

        if hasattr(lib, f"__{self.COMMAND.upper()}_GET_BASE__"):
            self.PASS_BASE = getattr(self.lib, f"__{self.COMMAND.upper()}_GET_BASE__")

        if hasattr(lib, f"__{self.COMMAND.upper()}_ARG_COUNT__"):
            self.ARG_COUNT = getattr(self.lib, f"__{self.COMMAND.upper()}_ARG_COUNT__")

        if hasattr(lib, f"__{self.COMMAND.upper()}_INVALID_ARG_ERR__"):
            self.INVALID_ARGS_ERR = getattr(self.lib, f"__{self.COMMAND.upper()}_INVALID_ARG_ERR__")

        self.FILEPATH = filepath
        self.INVALID_ARGS_ERR = invalid_args_err

class dCog:
    Commands            : list[Cog]
    def __init__(self):
        dCog.retrieve_all_commands("src/cmds/", 0, self.Commands)
    
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