import discord

from utils import *

__LEAVE_INFO__ = {
    "Name": "Leave",
    "Description": "Leave VC",
    "ArgCount": 0,
    "Invalid_Arg_Err": "",
    "Get_Base": True
}

async def leave(base, message: DiscordUtils) -> bool:
    voice_client = discord.utils.get(base.voice_clients, guild=message.Client.guild)
    if not voice_client:
        return False

    await voice_client.disconnect()
    await message.send_embed("Leave VC", "Succesffully left vc!")
    return True