import discord

from src.discord_utils import *

__LASTDEL_GET_BASE__ = True
__LASTDEL_ARG_COUNT__ = 0
__LASTDEL_INVALID_ARG_ERR__ = None

async def lastdel(base, msg: DiscordUtils) -> bool:
    if not base.LastDeleted:
        await msg.send_embed("Last Deleted Message", "No last deleted message logged!")
        return
    
    info = {
        "User":             [base.LastDeleted.Client.author.name, True],
        "ID":               [f"{base.LastDeleted.Client.author.id}", True],
        "Display Name":     [base.LastDeleted.Client.author.display_name, True],
    }

    if "`" not in base.LastDeleted.Client.content:
        info["Content"] = [f"```{base.LastDeleted.Client.content}```", False]
    else:
        info["Content"] = [f"{base.LastDeleted.Client.content}", False]

    await msg.send_embed("Last Message", f"The Last Message Captured", info)
    return True