import discord
from src.discord_utils import *
__NEWW_GET_BASE__ = True

async def neww(base, msg: DiscordUtils) -> bool:
	await msg.send_embed("Hi", msg.Args[0])
