import discord

class Insanity(discord.Client):
    AVAILABLE_REGIONS:  list[str] = [           # Available Regions
        'us-west',
        'us-east',
        'us-central',
        'us-south',
        'singapore',
        'japan',
        'hongkong',
        'brazil',
        'sydney',
        'southafrica',
        'india',
        'rotterdam',
        'russia',
        'europe',
        'frankfurt',
        'london',
        'dubai'
    ]
    
    async def on_ready(self):
        await self.change_presence(
            status = discord.Status.dnd,
            activity = discord.Streaming(name = "Insanity API", url = "https://insanity.bot")
        )

        print(f"[ + ] Firing up {self.user}....!")

    """
        [ On Join ]
    """
    async def on_guild_join(self, guild):
        print(f"[ + ] Join {guild.id}")

    async def on_guild_leave(self, guild):
        print(f"[ + ] Join {guild.id}")
        
    async def on_member_join(self, member):
        pass

    """
        [ On Message Delete ]
    """
    async def on_message_delete(self, message):
        pass
                
    async def on_member_remove(self, member):
        pass

    async def on_message(self, message):
        if message.content == "+help":
            await message.channel.send("Insanity V2.0; Hello")
        print(f"{message.content}")

inits = discord.Intents.all()
inits.message_content = True

print("[ + ] Initializing Insanity bot....!")
bot = Insanity(intents = inits)
print("[ + ] Running bot...!")
bot.run("")