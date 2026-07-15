import discord

from utils import *

__LAST_INFO__ = {
    "Get_Base": True
}

async def last(base, message: DiscordUtils):
    server = base.find_server_config(message.Client.guild.id)

    if not server.LastMessage:
        await message.send_embed("Err", "No last message found!")
        return 

    await message.send_embed("Last Message", f"The last message", fields = {
        "**User**": [f"``{server.LastMessage.Client.author.name}``", True],
        "**ID**": [f"``{server.LastMessage.Client.author.id}``", True],
        "**Display** Name": [f"``{server.LastMessage.Client.author.display_name}``", True],
        "**Info**": [f"```{server.LastMessage.Client.content}```", False]
    })