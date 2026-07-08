import discord

from src.discord_utils import *

__KICK_GET_BASE__ = True
__KICK_ARG_COUNT__ = 2
__KICK_INVALID_ARG_ERR__ = discord.Embed(title = "Kick", description = "List of kick commands", color = discord.Colour.red())
__KICK_INVALID_ARG_ERR__.add_field(name = "***Kick a user***", value = "```>kick <@user_id>```", inline = False)
__KICK_INVALID_ARG_ERR__.add_field(name = "***Kick all with role***", value = "```>kick <@role>```", inline = False)
__KICK_INVALID_ARG_ERR__.add_field(name = "***Kick user with string in name***", value = "```>kick --userstring <query>```", inline = False)
__KICK_INVALID_ARG_ERR__.add_field(name = "***Kick all joiners within a timeframe***", value = "```>kick <start_timestamp> <end_timestamp>```", inline = False)
__KICK_INVALID_ARG_ERR__.add_field(name = "***Kick everyone***", value = "```>kick --all```", inline = False)
__KICK_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__KICK_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__KICK_INVALID_ARG_ERR__.set_footer(text = "http://insanity.host")

async def kick(base, message: DiscordUtils) -> bool:
    return True