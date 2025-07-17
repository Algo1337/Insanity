import discord, enum, requests

class Discord_Event_T(enum.Enum):
    e_joined = 1
    e_left = 2
    e_message = 3,
    e_vc = 4

class DiscordUtils():
    Cmd: str
    Args: list[str]
    Data: str
    Client = None
    def __init__(self, message):
        self.Client = message
        self.Data = message.content
        if " " in self.Data:
            self.Args = self.Data.splt(" ")
            self.Cmd = self.Args[0]
        else:
            self.Args = []
            self.Cmd = self.Data

    def get_emojis(self) -> list:
        emojis = []

        for arg in self.Args:
            if arg.startswith("<") and arg.endswith(">"):
                emoji_args = arg.split(":")

                ## <:emoji_name:emoji_id>
                if len(emoji_args) == 3:
                    emojis.append(emoji_args[2][:-1])
                    continue
                elif len(emoji_args) == 2:
                    emojis.append(emoji_args[1][:-1])
                    continue

        return emojis

    @staticmethod
    def download_image(url: str, output: str) -> int:
        try:
            req = requests.get(url)
            if req.status_code != 200: 
                print("[ - ] Error, Failed to make the request....!\n")
            f = open(output, "wb")
            f.write(req.content)
            f.close()
        except:
            return 0
        
        return 1
