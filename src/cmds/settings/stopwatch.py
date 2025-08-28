import discord, random

from src.discord_utils import *

__STOPVC_GET_BASE__ = True
__STOPVC_ARG_COUNT__ = 0
__STOPVC_INVALID_ARG_ERR__ = ""


async def watchvc(base, message: DiscordUtils) -> bool:
    base.WatchingVC = False
    await message.send_embed("Stop VC Watch", "VC watch successfully stopped!")
    return True