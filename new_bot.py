import discord

# from tkinker import tk

from src.config import *
from src.discord_utils import *

COMMANDS_DIR = "/src/cmds"

# class NotifyGUI:
#     GuiHandler      : tk.Tk
#     Label           : tk.Label
#     Width           : int = 0
#     Height          : int = 0
#     Buffer          : str = ""
#     DisplayCounter  : int = 5
#     def __init__(self, width=400, height=100, x=100, y=100, opacity=1.0):
#         self.Width = width
#         self.Height = height

#         self.GuiHandler = tk.Tk()
#         self.GuiHandler.overrideredirect(True)  # no title bar or borders
#         self.GuiHandler.geometry(f"{width}x{height}+{x}+{y}")
#         self.GuiHandler.configure(bg="black")
#         self.GuiHandler.attributes("-topmost", True)  # stays above all windows
#         self.GuiHandler.attributes("-alpha", 1.0)  # transparency (1.0 = opaque, 0.0 = invisible)

#         noticeLabel = tk.Label(
#             self.GuiHandler,
#             text="New Notifications",
#             bg="black",
#             fg="white",
#             font=("Segoe UI", 14, "bold"),
#             wraplength=width - 20,
#             justify="center"
#         )
#         noticeLabel.pack(expand=True, fill="both", padx=10, pady=10) 

#         self.Label = tk.Label(
#             self.GuiHandler,
#             text="",
#             bg="black",
#             fg="white",
#             font=("Segoe UI", 9, "bold"),
#             wraplength=width - 20,
#             justify="left"
#         )
#         self.Label.pack(expand=True, fill="both", padx=5, pady=5)  
#         self.GuiHandler.bind("<Escape>", lambda e: NotifyGUI.destroy())

#     def add_text(self, data) -> None:
#         self.Buffer += f"{data}\n\n"
#         self.Height += 50

#     def update_text(self) -> None:
#         self.GuiHandler.geometry(f"{self.Width}x{self.Height}")
#         self.Label.config(text = self.Buffer)

#     def dispaly_gui(self) -> None:
#         # threading.Thread(target = self.GuiHandler.mainloop).start()
#         self.GuiHandler.after(500, self.update_text)

#     def hide_gui(self) -> None:
#         self.GuiHandler.destroy()

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
        'us-south',
        # 'singapore',
        # 'japan',
        # 'hongkong',
        # 'brazil',
        # 'sydney',
        # 'southafrica',
        # 'india',
        # 'rotterdam',
        # 'russia',
        # 'europe',
        # 'frankfurt',
        # 'london',
        # 'dubai'
    ]

    """
        Load cog to bot and fetch all settings from file
    """
    async def on_ready(self):
        self.Commands = Config.retrieve_all_commands(COMMANDS_DIR, 0, self.Cmds)
        # self.Gui = NotifyGUI()
        # self.Gui.dispaly_gui()
        self.BlacklistedTokens = database(db_t.__BLACKLISTED_TOKENS_PATH__, op_t.__read_db__, 0)
        self.BlacklistedTokens.pop(len(self.BlacklistedTokens) - 1)
        print(self.BlacklistedTokens)

        # self.BlacklistedSkids = Config.get_skids()
        self.BlacklistedSkids = database(db_t.__SKIDS_PATH__, op_t.__read_db__, 0)
        self.BlacklistedSkids.pop(len(self.BlacklistedSkids) - 1)

        self.Whitlist = database(db_t.__ADMINS_PATH__, op_t.__read_db__, 0)
        self.Whitlist.pop(len(self.Whitlist) - 1)

        self.Blacklistjoin = database(db_t.__BLACKLIST_JOIN_PATH__, op_t.__read_db__, 0)
        self.Blacklistjoin.pop(len(self.Blacklistjoin) - 1)
        await self.change_presence(
            status = discord.Status.dnd,
            activity = discord.Streaming(name = "Insanity API", url = "https://insanity.bot")
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
                
    async def on_member_remove(self, member):
        msg = DiscordUtils(self, member, Discord_Event_T.e_kick)
        msg.set_log_channel(1429855130081165364)

        # This fires for any leave, kick, or ban
        guild = member.guild
        async for entry in guild.audit_logs(limit=2, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id:
                if entry.action == discord.AuditLogAction.kick:
                    await msg.log(action_t.ON_REMOVE, f"User: {member} was kicked by {entry.user}")
                else:
                    await msg.log(action_t.ON_REMOVE, f"User: {member} was banned by {entry.user}")
                
                break

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        msg = DiscordUtils(self, message, Discord_Event_T.e_message)
        msg.set_log_channel(1429855130081165364)
        if message.content.startswith(Config.PREFIX):
            await msg.log(action_t.ON_MESSAGE, "")

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
bot.run(get_bot_token())