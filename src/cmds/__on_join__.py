import discord

async def __on_join__(base, message: discord.Message) -> bool:
    if f"{message.Client.id}" in base.Blacklistjoin:
        await message.Client.kick()

    return True