import discord

from utils import *

__COMMANDS_INFO__ = {
    "Name": "Commands",
    "Description": "List of loaded commands",
    "Get_Base": True
}

async def commands(base, message: DiscordUtils):
    cmds: str = ""
    for cmd in base.Cogs.Commands:
        cmds += f"{cmd.COMMAND}\n"

    await message.send_embed("Commands", f"```{cmds}```")