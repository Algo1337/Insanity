import discord, random

from utils import *

__STOP_INFO__ = {
    "Name": "Stop",
    "Description": "",
    "ArgCount": 0,
    "Invalid_Arg_Err": discord.Embed(
        title = "Error", 
        description = "Error", 
        color = discord.Colour.red()
    ),
    "Get_Base": True
}

async def stop(base, message: DiscordUtils) -> bool:
    server = base.find_server_config(message.Client.guild.id)

    server.WatchingVC = False
    await message.send_embed("Stop VC Watch", "VC watch successfully stopped!")
    return True