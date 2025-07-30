import discord

from src.discord_utils import *

"""
    @Command: nuke

    Formats:
        ;nuke --channel                                     # Clone. Delete Current, Reposition New
        ;nuke --msg <msg_count>                             # Delete upto msg_count
        ;nuke --user <@tag> <?count(Default set to 100)>    # Delete user's messages up a count, 100 if not provided
"""

__NUKE_GET_BASE__ = True
__NUKE_ARG_COUNT__ = 2
__NUKE_INVALID_ARG_ERR__ = discord.Embed(title = "Nuke | Error", description = "Invalid arguments provided", color = discord.Colour.red())
__NUKE_INVALID_ARG_ERR__.add_field(name = "***Channel nuke***", value = "```>nuke --channel```", inline = False)
__NUKE_INVALID_ARG_ERR__.add_field(name = "***Message nuke***", value = "```>nuke --msg <count>```", inline = False)
__NUKE_INVALID_ARG_ERR__.add_field(name = "***User nuke***", value = "```>nuke --user <@tag> <?count(Default: 100)>```", inline = False)
__NUKE_INVALID_ARG_ERR__.set_author(name = "Insanity")
__NUKE_INVALID_ARG_ERR__.set_footer(text = "https://insanity.bot")

async def nuke(base, message: DiscordUtils) -> bool:
    await message.send_embed("TEST", "TEST", image = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
    return True