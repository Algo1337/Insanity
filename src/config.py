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