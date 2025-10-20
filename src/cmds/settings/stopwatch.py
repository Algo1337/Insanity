import discord, random

from src.discord_utils import *

__STOPWATCH_GET_BASE__ = True
__STOPWATCH_ARG_COUNT__ = 0
__STOPWATCH_INVALID_ARG_ERR__ = discord.Embed(title = "Error", description = "Error", color = discord.Colour.red())


async def stopwatch(base, message: DiscordUtils) -> bool:
    await message.Client.delete()

    base.WatchingVC = False
    await message.send_embed("Stop VC Watch", "VC watch successfully stopped!")
    return True