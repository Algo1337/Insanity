import os, importlib, enum

class op_t(enum.Enum):
    __read_db__ = "read"
    __add_id__ = "add"
    __rm_id__ = "rm"

class db_t(enum.Enum):
    __SKIDS_PATH__              : str = "assets/skids.log"
    __BLACKLIST_JOIN_PATH__     : str = "assets/blacklist_join.log"
    __BLACKLISTED_TOKENS_PATH__ : str = "assets/blacklisted_token.log"
    __ADMINS_PATH__             : str = "assets/admins.log"

def database(db: db_t, op: op_t, query: int | str) -> bool | str:
    if op == op_t.__read_db__:
        """ Read Database """
        file = open(db, "r")
        data = file.read().split("\n")
        file.close()

        return data
    elif op == op_t.__add_id__:
        """ Add Query to File """
        file = open(db, "a")
        file.write(f"{query}\n")
        file.close()

        return True
    elif op == op_t.__rm_id__:
        """ Remove Query from file """
        new_db = ""
        file = open(db, "r")
        data = file.read().split("\n")
        for line in data:
            if query not in line:
                new_db += f"{line}\n"

        file.close()
        file = open(db, "w")
        file.write(new_db)
        file.close()

        return True
    
    return False

class Cog:
    name                : str = ""
    cmd                 : str = ""
    invalid_args_err    : str = ""
    lib                 : None
    handler             : None
    ArgCount            : int = 0
    ArgErr              : str = ""
    SendBase            : int = 0
    filepath            : str = ""
    def __init__(self, name: str, cmd: str, lib, filepath: str, invalid_args_err: str = ""):
        self.name = name
        self.cmd = cmd
        self.lib = lib
        if hasattr(self.lib, self.cmd):
            self.handler = getattr(lib, self.cmd)

        if hasattr(lib, f"__{self.cmd.upper()}_GET_BASE__"):
            self.SendBase = getattr(self.lib, f"__{self.cmd.upper()}_GET_BASE__")

        if hasattr(lib, f"__{self.cmd.upper()}_ARG_COUNT__"):
            self.ArgCount = getattr(self.lib, f"__{self.cmd.upper()}_ARG_COUNT__")

        if hasattr(lib, f"__{self.cmd.upper()}_INVALID_ARG_ERR__"):
            self.ArgErr = getattr(self.lib, f"__{self.cmd.upper()}_INVALID_ARG_ERR__")

        self.filepath = filepath
        self.invalid_args_err = invalid_args_err

class Config:
    PREFIX = ">"
    SKID_PATH = "assets/skids.log"
    BLACKLIST_JOIN_PATH: str = "assets/blacklist_join.log"
    BLACKLISTED_TOKENS_PATH: str = "assets/blacklisted_token.log"
    ADMINS_PATH: str = "assets/admins.log"
    def get_token() -> str:
        f = open("/cfg/token.cfg", "r")
        t = f.read()
        f.close()

        return t
    
    """
        {
            "file": "filepath"
        }
    """
    def retrieve_all_commands(dir: str, inner_dir: int = 0, Cmds: list[Cog] = None) -> dict:
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
                Cmds.append(Cog(name, name, Config.load_object_from_file(f"{name}_cmd", f"{CURRENT_DIR}/{item}", name), f"{CURRENT_DIR}/{item}"))

            if os.path.isdir(f"{CURRENT_DIR}/{item}"):
                dir += f"/{item}"
                Files.update(Config.retrieve_all_commands(dir, inner_dir + 1, Cmds))
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
        # return getattr(module, object_name)