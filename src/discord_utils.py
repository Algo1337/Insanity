import discord, enum, requests, asyncio

from .config import *
from datetime import datetime

class Discord_Event_T(enum.Enum):
    e_none              = 0
    e_joined            = 1
    e_left              = 2
    e_message           = 3,
    e_message_del       = 4,
    e_vc                = 5,
    e_kick              = 6

class DiscordUtils():
    Cmd         : str = ""
    Args        : list[str] = []
    Data        : str = ""
    dClient     = None
    Client      = None
    NoStdin     : bool = False
    NoStdout    : bool = False
    Redirect    : bool = False
    rChannel    : str | int = None
    Client_T    : Discord_Event_T = Discord_Event_T.e_none
    LogChannel  : int = 1429849671613808741
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

            if "--nostdout" in self.Args:
                self.NoStdout = True
                self.Args.remove("--nostdout")
                self.Data = self.Data.replace("--nostdout", "")

    def set_log_channel(self, channel: str | int) -> None:
        self.LogChannel = channel

    def set_redirect_channel(self, chan: int | str) -> None:
        self.Redirect = True
        self.rChannel = chan

    async def log(self, action: action_t, data: str, fields: dict[str, str] = None) -> None:
        local_tz = pytz.timezone('America/Kentucky/Louisville')
        
        if self.Client_T == Discord_Event_T.e_message or self.Client_T == Discord_Event_T.e_message_del:
            timestamp = self.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')
        else:
            timestamp = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")

        channel = self.dClient.get_channel(self.LogChannel)

        embed = discord.Embed(title = "Insanity Logs", description = f"New Log!\n\n{data}", color = discord.Colour.red())
        embed.add_field(name = "Timestamp", value = f"{timestamp}", inline = True)
        embed.add_field(name = "Action", value = action.name, inline = True)
        if hasattr(self.Client, "content"):
            if "```" in self.Client.content:
                embed.add_field(name = "Message", value = self.Client.content, inline = False)
            elif self.Client.stickers:
                embed.add_field(name = "Message", value = "Sticker Attachment", inline = False)
            else:
                embed.add_field(name = "Message", value = f"```{self.Client.content}```", inline = False)
        
        if not channel:
            print("[ x ] Error, Unable to get log channel!")
            return
        
        if fields != None:
            for field in fields:
                if isinstance(fields[field], list):
                    embed.add_field(name = field, value = fields[field][0], inline = fields[field][1])
                else:
                    embed.add_field(name = field, value = fields[field], inline = False)
        
        await channel.send(embed = embed)

    def get_arg(self, pos: int) -> str:
        return self.Args[pos]
    
    def get_flag_value(self, flag: str) -> str | None:
        i = 0
        for arg in self.Args:
            if arg == flag:
                return self.Args[i + 1]
            
            i += 1

        return None

    async def redirect_message(self, text: str, file = None, files = None) -> bool:
        if not text or text == "":
            return False
        
        channel = self.dClient.get_channel(self.rChannel)
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
            
            await channel.send(text, file = file, files = files)
        except:
            return False
        
        return False

    async def send_message(self, text: str, file = None, files = None) -> bool:
        if self.Redirect:
            await self.redirect_message(text, file, files)
            return
        
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
    
    async def redirect_embed(self, title: str, desc: str, fields: dict = None, author_name: str = None, author_url: str = None, image: str = None, images: list[str] = None) -> bool:
        channel = self.dClient.get_channel(self.rChannel)
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

        await channel.send(embed = embed)
    
    async def send_embed(self, title: str, desc: str, fields: dict = None, author_name: str = None, author_url: str = None, image: str = None, images: list[str] = None) -> bool:
        if self.NoStdout == True:
            return
        elif self.Redirect == True:
            await self.redirect_embed(title, desc, fields, author_name, author_url, image, images)
            return
        
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
    
    def get_flag_value(self, flag: str) -> tuple[str, int] | None:
        i = 0
        for arg in self.Args:
            if arg == flag:
                return self.Args[i], i

            i += 1

        return None

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
