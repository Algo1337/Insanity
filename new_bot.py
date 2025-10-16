import discord

# from tkinker import tk

from src.config import *
from src.discord_utils import *

COMMANDS_DIR = "/src/cmds"

# class Notifications:
#     gui: tk.Tk
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.overrideredirect(True)
#         self.root.geometry(f"400x200+10+10")
#         self.root.configure(bg="black")
#         self.root.attributes("-topmost", True)
#         self.root.attributes("-alpha", 1.0)

#         self.root.bind("<Escape>", lambda e: self.root.destroy())

#     def display_notifications(self) -> None:
#         # self.root.mainloop()
#         # root.after(1000, update)
#         pass

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

        self.BlacklistedTokens = database(db_t.__BLACKLISTED_TOKENS_PATH__, op_t.__read_db__, 0)
        self.BlacklistedTokens.pop(len(self.BlacklistedTokens) - 1)

        # self.BlacklistedSkids = Config.get_skids()
        self.BlacklistedSkids = database(db_t.__SKIDS_PATH__, op_t.__read_db__, 0)
        self.BlacklistedSkids.pop(len(self.BlacklistedSkids) - 1)

        self.Whitlist = database(db_t.__ADMINS_PATH__, op_t.__read_db__, 0)

        self.Blacklistjoin = database(db_t.__BLACKLIST_JOIN_PATH__, op_t.__read_db__, 0)
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