import discord

from src.discord_utils import *
from src.config import *

__NEWW_GET_BASE__ = True
__NEWW_ARG_COUNT__ = 0
__NEWW_INVALID_ARG_ERR__ = discord.Embed(title = "Testing Command", description = "A command to test new feature during runtime for owner only!", color = discord.Colour.red())
__NEWW_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__NEWW_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__NEWW_INVALID_ARG_ERR__.set_footer(text = "https://insanity.bot")

async def neww(base, msg: DiscordUtils) -> bool:
	await msg.log(action_t.__ON_MESSAGE__, "TESTING")
