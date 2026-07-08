import discord

from src.discord_utils import *

__LEAVEVC_GET_BASE__ = True
__LEAVEVC_ARG_COUNT__ = 0

async def leavevc(base, message: DiscordUtils) -> bool:
    voice_client = discord.utils.get(base.voice_clients, guild=message.Client.guild)
    if not voice_client:
        return False

    await voice_client.disconnect()
    await message.send_embed("Leave VC", "Succesffully left vc!")
    return True