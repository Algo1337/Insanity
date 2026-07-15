import discord

from utils import *

__PREFIX_INFO__ = {
    "Name": "Prefix",
    "Description": "Change the command prefix!",
    "ArgCount": 2,
    "Invalid_Arg_Err": "Invalid arguments",
    "Get_Base": True
}

async def prefix(base, message: DiscordUtils):
    if message.Args >= 2:
        base.Servers[message.Client.guild.id].Prefix = message.Args[1]