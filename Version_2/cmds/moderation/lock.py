import discord

from src.discord_utils import *

__LOCK_GET_BASE__ = True
__LOCK_ARG_COUNT__ = 2
__LOCK_INVALID_ARG_ERR__ = discord.Embed(title = "Lock Channel", description = "List of lock channel commands", color = discord.Colour.red())
__LOCK_INVALID_ARG_ERR__.add_field(name = "Lock a user from channel", value = "```>lock --add <@tag>```", inline = False)
__LOCK_INVALID_ARG_ERR__.add_field(name = "Remove lock from user", value = "```>lock --rm <@tag>```", inline = False)
__LOCK_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__LOCK_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__LOCK_INVALID_ARG_ERR__.set_footer(text = "http://insanity.host")

async def lock(base, msg: DiscordUtils) -> bool:
    return True