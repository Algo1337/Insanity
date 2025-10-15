import discord

from src.config import *
from src.discord_utils import *

COMMANDS_DIR = "/src/cmds"

class Cursor:
    x       : int = 0   # X Cursor
    y       : int = 0   # Y Cursor
    def __init__(self):
        self.x = 1
        self.y = 1

class TuiDisplay:
    def display_component() -> None:
        # Create Border
        pass

    def fill_component() -> None:
        # fill color
        pass

class TuiComponent(TuiDisplay):
    width           : int = 0   # Box Width
    height          : int = 0   # Height
    cursor          : Cursor    # Current Position
    buffer          : str = ""  # Buffer

    display_start   : int = 0
    def __init__(self, w: int, h: int, start: int):
        self.width = w 
        self.height = h
        self.display_start = start
        self.cursor = Cursor()
        
        print(f"\033[0;{self.display_start - 1}f", end = "", flush = True)

        # Set Top Border
        for c in range(0, self.width): print("-", end = "", flush = True)

        # Set Side Border and Bottom Border
        for i in range(2, self.height):
            print(f"\033[{i};{self.display_start - 1}f", end = "", flush = True)
            
            print("|", end = "", flush = True)
            for c in range(0, self.width - 2): print(" ", end = "", flush = True)
            print("|", end = "\n", flush = True)


        print(f"\033[{self.height};{self.display_start}f", end = "", flush = True)
        for c in range(1, self.width): print("-", end = "", flush = True)

    def print(self, data: str, flush: bool = False) -> bool:
        if len(data) > self.width - 2: # - 2 for box borders
            pass # Split text every self.width-length

        self.buffer += data

        if flush:
            for line in self.buffer.split("\n"):
                print(f"\033[{i};{self.display_start}f", end = "", flush = True)
                print(line, flush = True)

            self.buffer = ""

class tui_logger:
    # Terminal Settings
    Size        : int = 0

    # Components
    __BOT_BOX__ : TuiComponent = None
    __LOG_BOX__ : TuiComponent = None
    def __init__(self, bot_w: int, bot_h: int, logger_w: int, logger_h: int):
        self.__BOT_BOX__ = TuiComponent(bot_w, bot_h, 1)
        self.__LOG_BOX__ = TuiComponent(logger_w, logger_h, 41)


logger: tui_logger = tui_logger(40, 20, 40, 20)

class Insanity(discord.Client, Config):
    Cmds:               list[str] = []
    Commands:           list[Cog] = []          # Commands Loaded
    OnMessage:          Cog                     # OnMessage Cog Handler
    OnMessageDelete:    Cog                     # OnMessageDelete Cog Handler
    OnJoin:             Cog                     # OnJoin Cog Handler
    Whitlist:           list[int] = []          # Whitlisted Bot Admin
    Blacklistjoin:      dict[int, int] = {}     # Blacklisted User from joining
    BlacklistedSkids:   list[int] = []          # Strip roles and Force Skid Role
    BlacklistedTokens:  list[str] = []          # Blacklisted Token within messages
    WatchingVC:         bool = False            # Watch VC Status/Toggle
    CurrentRegion:      str = ""                # Current Region being watched for attacks
    LastRegion:         str = ""                # Last region, Incase it needs to change twice
    AVAILABLE_REGIONS:  list[str] = [           # Available Regions
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
        'india'
        # 'rotterdam'
    ]

    """
        Load cog to bot and fetch all settings from file
    """
    async def on_ready(self):
        self.Commands = Config.retrieve_all_commands(COMMANDS_DIR, 0, self.Cmds)

        self.BlacklistedTokens = Config.get_blacklisted_tokens()
        self.BlacklistedTokens.pop(len(self.BlacklistedTokens) - 1)
        self.BlacklistedSkids = Config.get_skids()

        self.Whitlist = Config.get_admins_list()


        self.Blacklistjoin = Config.get_blacklistjoin_list()
        await self.change_presence(
            status = discord.Status.dnd,
            activity = discord.Streaming(name = "Insanity API Streaming", url = "https://insanity.bot")
        )

        print(f"[ + ] Firing up {self.user}....!")

        print("Cmds:", end=" ")
        for cmd in self.Cmds:
            print(cmd.name, end=", ")

            if cmd.name == "__on_message__":
                self.OnMessage = cmd

            if cmd.name == "__on_message_delete__":
                self.OnMessageDelete = cmd

            if cmd.name == "__on_join__":
                self.OnJoin = cmd
        print(" loaded!")

    """
        [ On Join ]
    """
    async def on_guild_join(self, guild):
        print(f"[ + ] Join {guild.id}")
        
    async def on_member_join(self, member):
        msg = DiscordUtils(self, member, Discord_Event_T.e_joined)
        if self.OnJoin:
            if self.OnJoin.SendBase:
                if (await self.OnJoin.handler(self, msg)) == False:
                    return
                
            else:
                if (await self.OnJoin.handler(msg)) == False:
                    return
                
    async def vcmove(ctx, member: discord.Member, *, channel: discord.VoiceChannel):
        """Move a member to another voice channel."""
        if member.voice:
            await member.move_to(channel)
            await ctx.send(f"Moved {member.display_name} to {channel.name}.")
        else:
            await ctx.send(f"{member.display_name} is not in a voice channel.")

    """
        [ On Message Delete ]
    """
    async def on_message_delete(self, message):
        msg = DiscordUtils(self, message, Discord_Event_T.e_message_del)
        if self.OnMessageDelete:
            if self.OnMessageDelete.SendBase:
                if (await self.OnMessageDelete.handler(self, msg)) == False:
                    return
                
            else:
                if (await self.OnMessageDelete.handler(msg)) == False:
                    return

    async def on_message(self, message):
        msg = DiscordUtils(self, message, Discord_Event_T.e_message)
        if self.OnMessage:
            if self.OnMessage.SendBase:
                if (await self.OnMessage.handler(self, msg)) == False:
                    return
                
            else:
                if (await self.OnMessage.handler(msg)) == False:
                    return

        for cmd in self.Cmds:
            if cmd.name.startswith("__"):
                continue
            
            if f"{Config.PREFIX}{cmd.name}" == msg.Cmd and cmd.ArgCount == 0:
                if cmd.SendBase != False and cmd.SendBase != None:
                    await cmd.handler(self, msg)
                else:
                    await cmd.handler(msg)

                break

            if f"{Config.PREFIX}{cmd.name}" == msg.Cmd:
                if cmd.ArgCount > 0 and msg.Args.__len__() < cmd.ArgCount:
                    if isinstance(cmd.ArgErr, discord.Embed):
                        await message.channel.send(embed = cmd.ArgErr)
                        break

                    await message.channel.send(cmd.ArgErr)
                    break
                else:
                    if cmd.SendBase != None:
                        await cmd.handler(self, msg)
                    else:
                        await cmd.handler(msg)

Banner = r"""
╦╔╗╔╔═╗╔═╗╔╗╔╦╔╦╗╦ ╦
║║║║╚═╗╠═╣║║║║ ║ ╚╦╝
╩╝╚╝╚═╝╩ ╩╝╚╝╩ ╩  ╩ 
"""
print(Banner)
inits = discord.Intents.all()
inits.message_content = True

print("[ + ] Initializing Insanity bot....!")
bot = Insanity(intents = inits, Config = Config())
print("[ + ] Running bot...!")
bot.run(Config.get_token())