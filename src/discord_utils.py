import discord, enum, requests

class Discord_Event_T(enum.Enum):
    e_none      = 0
    e_joined    = 1
    e_left      = 2
    e_message   = 3,
    e_vc        = 4

class DiscordUtils():
    Cmd: str                    = ""
    Args: list[str]             = []
    Data: str                   = ""
    Client                      = None
    Client_T: Discord_Event_T   = Discord_Event_T.e_none
    def __init__(self, message, event_t: Discord_Event_T):
        if event_t == Discord_Event_T.e_message:
            self.Client = message
            self.Data = message.content
            self.Client_T = event_t
            if " " in self.Data:
                self.Args = self.Data.split(" ")
                self.Cmd = self.Args[0]
            else:
                self.Args = []
                self.Cmd = self.Data

    async def send_message(self, text: str, file = None, files = None) -> bool:
        if not text or text == "":
            return False
        
        try:
            await self.Client.channel.send(text, file = file, files = files)
        except:
            return False
        
        return False
    
    async def send_embed(self, title: str, desc: str, fields: dict = None, image: str = None, images: list[str] = None) -> bool:
        embed = discord.Embed(title = title, description = desc, color = discord.Colour.red())

        for field in fields:
            if isinstance(fields[field], list):
                embed.add_field(name = field, value = fields[field][0], inline = fields[field][1])
            else:
                embed.add_field(name = field, value = fields[field], inline = False)

        await self.Client.channel.send(embed = embed)

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
