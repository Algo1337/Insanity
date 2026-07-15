import discord

from utils import *

__DELETED_INFO__ = {
    "Name": "Deleted",
    "Description": "Display the last deleted message",
    "Get_Base": True
}

async def deleted(base, message: DiscordUtils):
    server = base.find_server_config(message.Client.guild.id)

    if not server.LastDeleted:
        await message.send_embed("Err", "No last message found!")
        return 

    await message.send_embed("Last Message", f"The last message", fields = {
        "**User**": [f"``{server.LastDeleted.Client.author.name}``", True],
        "**ID**": [f"``{server.LastDeleted.Client.author.id}``", True],
        "**Display** Name": [f"``{server.LastDeleted.Client.author.display_name}``", True],
        "**Info**": [f"```{server.LastDeleted.Client.content}```", False]
    })