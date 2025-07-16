import discord

from src.config import Config

class NCA_Bot(discord.Client):
    async def on_ready(self):
        print(f"[ + ] Firing up {self.user}....!")

    async def on_message(self, message):
        if message.author.bot:
            return
        
try:
    intents = discord.Intent.all()
    intents.message_content = True

    bot = NCA_Bot(intents = intents)
    bot.run(Config.get_token())
except:
    print(f"\x1b[31m[ - ]\x1b[0m Exiting....!")
    exit(0)