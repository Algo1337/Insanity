"""
    Insanity's Custom Discord Bot Cog Example
"""
import discord

from ..utils import *

async def help(message: DiscordUtils):
    await message.send_embed(
        "Help", "Welcome to Insanity V2", {}, 
        author_name = "Insanity", 
        author_url = "https://images-ext-1.discordapp.net/external/ucZeDO84rLbEbF6iPIw_RW5YfjsEBUMHDYgFv2tRAEQ/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1441933074697949247/1ac82574fd38e50e764835eb729ddba7.png?format=webp&quality=lossless"
    )