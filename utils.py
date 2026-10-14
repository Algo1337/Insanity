import discord, enum, requests, asyncio, pytz

from datetime import datetime, timezone

class Discord_Event_T(enum.Enum):
    e_none              = 0
    e_joined            = 1
    e_left              = 2
    e_message           = 3,
    e_message_del       = 4,
    e_vc                = 5,
    e_kick              = 6

class op_t(enum.Enum):
    __read_db__ = "read"
    __add_id__ = "add"
    __rm_id__ = "rm"

class db_t(enum.Enum):
    __SKIDS_PATH__              : str = "assets/skids.log"
    __BLACKLIST_JOIN_PATH__     : str = "assets/blacklist_join.log"
    __BLACKLISTED_TOKENS_PATH__ : str = "assets/blacklisted_token.log"
    __ADMINS_PATH__             : str = "assets/admins.log"

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
    LogChannel  : int = None

    """
        Some Message Default Settings
    """
    __Embed_Thumbnail       : str = None
    __Embed_Author_Name     : str = None
    __Embed_Author_Image    : str = None
    __Embed_Footer          : str = None
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

    def set_default_embed_info(self, thumbnail: str, author_name: str, author_image: str, footer: str) -> None:
        self.__Embed_Thumbnail = thumbnail
        self.__Embed_Author_Name = author_name
        self.__Embed_Author_Image = author_image
        self.__Embed_Footer = footer

    def add_default_embed_info(self, embed: discord.Embed) -> None:
        if self.__Embed_Author_Name or self.__Embed_Author_Image:
            embed.set_author(name = self.__Embed_Author_Name, url = self.__Embed_Author_Image)

        if self.__Embed_Footer:
            embed.set_footer(text = self.__Embed_Footer)

        if self.__Embed_Thumbnail:
            embed.set_thumbnail(url = self.__Embed_Thumbnail)

    """ Log to discord channel """
    async def log(self, action: Discord_Event_T, data: str, fields: dict[str, str] = None) -> None:
        if self.LogChannel == None:
            return
    
        local_tz = pytz.timezone('America/Kentucky/Louisville')
        timestamp = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        if self.Client_T == Discord_Event_T.e_message or self.Client_T == Discord_Event_T.e_message_del:
            timestamp = self.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y-%H:%M:%S')
        else:
            timestamp = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")

        channel = self.dClient.get_channel(self.LogChannel)

        embed = discord.Embed(title = "Insanity Logs", description = f"New Log!\n\n{data}", color = discord.Colour.red())
        embed.add_field(name = "Action", value = action.name, inline = True)
        embed.add_field(name = "Timestamp", value = f"{timestamp}", inline = True)
        
        if fields != None:
            for field in fields:
                if isinstance(fields[field], list):
                    embed.add_field(name = field, value = fields[field][0], inline = fields[field][1])
                else:
                    embed.add_field(name = field, value = fields[field], inline = False)

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
        
        await channel.send(embed = embed)

    def get_arg(self, pos: int) -> str:
        return self.Args[pos]

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
            embed.set_image(url = image)

        self.add_default_embed_info(embed)
        await self.Client.channel.send(embed = embed)

    def get_emojis(self, data: str = None) -> list:
        emojis = []

        args = self.Args
        if data != None:
            args = data.split(" ")

        for arg in args:
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
            return 1
        except:
            print("Error Saving....!")
            return 0
        
        return 1

    @staticmethod
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
            lines: list[str] = []
            file = open(db, "r")
            data = file.read().split("\n")
            for line in data:
                if query not in line:
                    lines.append(line)

            file.close()
            file = open(db, "w")
            file.write("\n".join(lines))
            file.close()

            return True
        
        return False

    def get_bot_token() -> str:
        f = open("/cfg/token.cfg", "r")
        t = f.read()
        f.close()

        return t