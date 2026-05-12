import discord
from src.discord_utils import *
__DICK_GET_BASE__ = True
__DICK_ARG_COUNT__ = 2
__DICK_INVALID_ARG_ERR__ = None

async def dick(base, msg: DiscordUtils) -> bool:
	await msg.Client.channel.send("hi");
