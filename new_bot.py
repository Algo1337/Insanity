import discord

from src.config import *
from src.discord_utils import *

class Insanity(discord.Client, Config):
    Cmds:               list[str] = []
    Commands:           list[Cog] = []
    OnMessage:          Cog
    OnMessageDelete:    Cog
    Whitlist:           list[int] = []
    Blacklistjoin:      dict[int, int] = {}
    WatchingVC:         bool = False
    CurrentRegion:      str = ""
    LastRegion:         str = ""
    async def on_ready(self):
        self.Cmds = []
        self.Commands = Config.retrieve_all_commands("/src/cmds", 0, self.Cmds)
        await self.change_presence(
            status = discord.Status.dnd,
            activity = discord.Streaming(name = "Insanity API Streaming", url = "https://insanity.bot")
        )
        print(f"[ + ] Firing up {self.user}....!")

        for cmd in self.Cmds:
            print(f"Cmd: {cmd.name} loaded....!")

            if cmd.name == "__on_message__":
                self.OnMessage = cmd

            if cmd.name == "__on_message_delete__":
                self.OnMessageDelete = cmd

    """
        [ On Join ]
    """
    async def on_guild_join(self, member):
        if member.guild.id not in self.Blacklistjoin:
            return
        
        if member.guild.id in self.Blacklistjoin:
            if member.id in self.Blacklistjoin[member.guild.id]:
                member.kick()
                chan = await self.get_channel(member.guild.text_channels, name = "logs")
                chan.send(f"{member.name} tried joining but is blacklisted!")


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
                if cmd.SendBase != 0 and cmd.SendBase != None:
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

try:
    inits = discord.Intents.all()
    inits.message_content = True

    bot = Insanity(intents = inits, Config = Config())
    bot.run(Config.get_token())
except:
    print(f"\x1b[31m[ - ]\x1b[0m Exiting....!")
    exit(0)