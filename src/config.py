import os

class Config:
    PREFIX = ";"

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
    Commands = {

    }

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
    def retrieve_all_commands() -> dict:
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
                Files.update(Config.retrieve_all_commands(CURRENT_DIR))
                CURRENT_DIR = CURRENT_DIR.replace(f"/{item}", "")

        if len(Files) > 0:
            return Files
        
        return {}