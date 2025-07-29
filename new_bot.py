import discord

from src.config import *
from src.discord_utils import *

class Insanity(discord.Client, Config):
    async def on_ready(self):
        self.Cmds = []
        self.Commands = Config.retrieve_all_commands("/src/cmds", 0, self.Cmds)
        print(f"[ + ] Firing up {self.user}....!")

        for cmd in self.Cmds:
            print(f"Cmd: {cmd.name} loaded....!")

            if cmd.name == "__on_message__":
                self.OnMessageHandler = cmd.handler

    async def on_message(self, message):
        msg = DiscordUtils(message, Discord_Event_T.e_message)
        if self.OnMessageHandler and (await self.OnMessageHandler(msg)) == False:
            return

        for cmd in self.Cmds:
            if cmd.name.startswith("__"):
                continue
            
            if f"{Config.PREFIX}{cmd.name}" == msg.Cmd and cmd.ArgCount == 0:
                await cmd.handler(msg)
                break

            if f"{Config.PREFIX}{cmd.name}" == msg.Cmd:
                if cmd.ArrCount > 0 and len(msg.Args) != cmd.ArgCount:
                    if isinstance(cmd.ArgErr, discord.Embed):
                        await message.channel.send(embed = cmd.ArgErr)
                        break

                    await message.channel.send(cmd.ArgErr)
                    break
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