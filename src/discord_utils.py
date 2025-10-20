import discord, enum, requests, asyncio

from .config import *

class Discord_Event_T(enum.Enum):
    e_none              = 0
    e_joined            = 1
    e_left              = 2
    e_message           = 3,
    e_message_del       = 4,
    e_vc                = 5

class DiscordUtils():
    Cmd         : str = ""
    Args        : list[str] = []
    Data        : str = ""
    dClient     = None
    Client      = None
    Client_T    : Discord_Event_T = Discord_Event_T.e_none
    LogChannel  : str | int = 1397686339520168108
    def __init__(self, dClient, message, event_t: Discord_Event_T):
        self.dClient = dClient
        self.Client_T = event_t
        self.Client = message
        if event_t == Discord_Event_T.e_message or event_t == Discord_Event_T.e_message_del:
            self.Data = message.content
            self.dClient = dClient
            self.Client_T = event_t
            if " " in message.content:
                self.Args = self.Data.split(" ")
                self.Cmd = self.Args[0]
            else:
                self.Args = []
                self.Cmd = self.Data

    def set_log_channel(self, channel: str | int) -> None:
        self.LogChannel = channel

    async def log(self, action: action_t, data: str | discord.Embed) -> None:
        channel = self.dClient.get_channel(self.LogChannel)
        
        if not channel:
            print("[ x ] Error, Unable to get log channel!")
            return
        
        if isinstance(data, str):
            await channel.send(data)
        else:
            await channel.send(embed = data)

    def get_arg(self, pos: int) -> str:
        return self.Args[pos]
    
    def get_flag_value(self, flag: str) -> str | None:
        i = 0
        for arg in self.Args:
            if arg == flag:
                return self.Args[i + 1]
            
            i += 1

        return None

    async def send_message(self, text: str, file = None, files = None) -> bool:
        if not text or text == "":
            return False
        
        try:
            resp_len = text.__len__()
            if resp_len > 1999:
                c = resp_len / 1999
                current = 0
                for _ in range(0, int(c)):
                    await self.Client.channel.send(text[current : current + 1999])
                    current += 1999

                    await asyncio.sleep(1)

                await self.Client.channel.send(text[current : resp_len])
                return
            
            await self.Client.channel.send(text, file = file, files = files)
        except:
            return False
        
        return False
    
    async def send_embed(self, title: str, desc: str, fields: dict = None, author_name: str = None, author_url: str = None, image: str = None, images: list[str] = None) -> bool:
        embed = discord.Embed(title = title, description = desc, color = discord.Colour.red())

        if image != None:
            embed.set_image(url = image)

        if fields != None:
            for field in fields:
                if isinstance(fields[field], list):
                    embed.add_field(name = field, value = fields[field][0], inline = fields[field][1])
                else:
                    embed.add_field(name = field, value = fields[field], inline = False)

        if author_name != None and author_url != None:
            embed.set_author(name = author_name, icon_url = author_url)
        elif author_name != None:
            embed.set_author(name = author_name)

        if author_url != None:
            embed.set_thumbnail(url = author_url)

        if image != None:
            embed.set_image(image = image)

        await self.Client.channel.send(embed = embed)

    def get_emojis(self) -> list:
        emojis = []

        for arg in self.Args:
            if arg.startswith("<") and arg.endswith(">"):
                emoji_args = arg.split(":")

                ## <:emoji_name:emoji_id>
                if emoji_args.__len__() == 3:
                    emojis.append(emoji_args[2][:-1])
                    continue
                elif emoji_args.__len__() == 2:
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
