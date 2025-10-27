import discord

from src.discord_utils import *

__LAST_GET_BASE__ = True
__LAST_ARG_COUNT__ = 0
__LAST_INVALID_ARG_ERR__ = None

async def last(base, msg: DiscordUtils) -> bool:
    if not base.LastMessage:
        await msg.send_embed("Last Message", "No last message logged!")
        return
    
    info = {
        "User":             [base.LastMessage.Client.author.name, True],
        "ID":               [f"{base.LastMessage.Client.author.id}", True],
        "Display Name":     [base.LastMessage.Client.author.display_name, True],
    }

    if "`" not in base.LastMessage.Client.content:
        info["Content"] = [f"```{base.LastMessage.Client.content}```", False]
    else:
        info["Content"] = [f"{base.LastMessage.Client.content}", False]

    await msg.send_embed("Last Message", f"{base.LastMessage.Client.content}", info)
    return True