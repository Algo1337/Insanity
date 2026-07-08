import discord

from src.discord_utils import *

__COMMANDS_GET_BASE__ = True
__COMMANDS_ARG_COUNT__ = 0
__COMMANDS_INVALID_ARG_ERR__ = discord.Embed(title = "Dick n balls", description = "Dick n balls", color = discord.Colour.red())

async def commands(base, msg: DiscordUtils) -> bool:
    cmds = ""
    for cmd in base.Cmds:
        if not cmds.startswith("__"):
            cmds += f"{cmd.name}\n"

    await msg.send_embed("Command(s) Loaded", f"Found {len(base.Commands)} commands!\n\n```{cmds}```")
    return True