import discord

from src.discord_utils import *

__SAY_GET_BASE__ = True
__SAY_ARG_COUNT__ = 2
__SAY_INVALID_ARG_ERR__ = discord.Embed(title = "Say", description = "Error, Invalid arguments provided!\nUsage: ;say <?channel> <text>", color = discord.Colour.red())
__SAY_INVALID_ARG_ERR__.set_author(name = "Insanity")
__SAY_INVALID_ARG_ERR__.set_footer(text = "http://insanity.host")

async def say(base, message: DiscordUtils) -> bool:
    await message.Client.delete()
    
    if " " not in message.Data:
        await message.Client.channel.send(embed = __SAY_INVALID_ARG_ERR__)
        return
    
    """
        Detect channel within second [1] argument
    """
    channel = None
    if message.Args[1].startswith("<#") and message.Args[1].endswith(">"):
        channel = base.get_channel(int(message.Args[1].replace("<#", "").replace(">", "")))

    """
        Send to channel if set
    """
    if channel == None:
        await message.Client.channel.send(" ".join(message.Args[1:]))
    else:
        await channel.send(" ".join(message.Args[2:]))

    return True