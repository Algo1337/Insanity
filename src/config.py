import os, importlib

class Cog:
    name: str           = ""
    cmd: str            = ""
    invalid_args_err    = ""
    lib: None
    handler: None
    ArgCount: int       = 0
    ArgErr: str         = ""
    SendBase: int       = 0
    filepath: str       = ""
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

    """
        { "ServerID": {
                "THRESHOLD": 200,
                "LastRegion": "us-east",
                "CurrentRegion": "us-west",
                "VC": "voice_channel_id"
            }
        }
    """
    VC_WATCH = {}

    """ 
        { ServerID: "VC" }
    """
    MUSIC_PLAYING = {}

    """
        Available regions, Some server do not accept all
    """
    AVAILABLE_REGIONS = [
        'us-west', 
        'us-east', 
        'us-central', 
        'us-south'
        'singapore', 
        'japan', 
        'hongkong', 
        'brazil',
        'sydney', 
        'southafrica', 
        'india', 
        'rotterdam'
    ]

    """
        { "help" { 
                "args": 0,
                "on_err": "",
                "invalid_args": ""
                "fn": void
            }
        }
    """
    Commands: dict = {}
    BLACKLIST_JOIN_PATH: str = "assets/blacklist_join.log"
    BLACKLISTED_TOKENS_PATH: str = "assets/blacklisted_token.log"
    ADMINS_PATH: str = "assets/admins.log"
    def get_token() -> str:
        f = open("token.cfg", "r")
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
                # if inner_dir > 0:
                #     args = dir.split("/")
                #     dir = "/".join(args[:len(args) - 2])

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

    @staticmethod
    def get_blacklistjoin_list() -> list[str]:
        f = open(Config.BLACKLIST_JOIN_PATH, "r")
        ids = f.read().split("\n")

        f.close()
        return ids

    @staticmethod
    def add_blacklistjoin(user_id: int) -> bool:
        f = open(Config.BLACKLIST_JOIN_PATH, "a")
        f.write(f"{user_id}\n")

        f.close()
        return True

    @staticmethod
    def get_blacklisted_tokens() -> list[str]:
        f = open(Config.BLACKLISTED_TOKENS_PATH, "r")
        ids = f.read().split("\n")

        f.close()
        return ids

    @staticmethod
    def add_blacklisted_tokens(token: str) -> bool:
        f = open(Config.BLACKLISTED_TOKENS_PATH, "a")
        f.write(f"{token}\n")

        f.close()
        return True

    @staticmethod
    def get_admins_list() -> list[str]:
        f = open(Config.ADMINS_PATH, "r")
        ids = f.read().split("\n")
        print(ids)

        f.close()
        return ids

    @staticmethod
    def add_admins_list(uid: int) -> bool:
        f = open(Config.ADMINS_PATH, "a")
        f.write(f"{uid}\n")

        f.close()
        return True