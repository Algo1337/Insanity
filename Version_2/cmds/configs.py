import discord

from utils import *

__CONFIGS_INFO__ = {
    "Name": "Help",
    "Description": "List of commands on the bot!",
    "ArgCount": 0,
    "Invalid_Arg_Err": "err",
    "Get_Base": True
}

async def configs(base, msg: DiscordUtils):
    servers = ""
    for cfg in base.Servers:
        servers += f"{cfg} | {base.Servers[cfg].ServerName} | {base.Servers[cfg].Prefix}\n"

    await msg.send_message(f"Servers Configured With Insanity\n\n```{servers}```")