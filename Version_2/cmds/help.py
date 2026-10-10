"""
    Insanity's Custom Discord Bot Cog Example
"""
import discord

from datetime import datetime
from utils import *

__HELP_INFO__ = {
    "Name": "Help",
    "Description": "List of commands on the bot!",
    "ArgCount": 0,
    "Get_Base": True
}

async def help(base, message: DiscordUtils):
    cmds = {}
    if len(message.Args) == 0:
        for cog in base.Cogs.Commands:
            args = cog.FILEPATH.split("/")
            category = args[len(args) - 2]

            if category == base.Cogs.DEFAULT_DIR.split("/")[len(base.Cogs.DEFAULT_DIR.split("/")) - 1]:
                continue

            cmds[category] = [f"+help {category}", False]

        await message.send_embed(
            "Help", "Welcome to Insanity V2", cmds, 
            author_name = "Insanity", 
            author_url = "https://images-ext-1.discordapp.net/external/ucZeDO84rLbEbF6iPIw_RW5YfjsEBUMHDYgFv2tRAEQ/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1441933074697949247/1ac82574fd38e50e764835eb729ddba7.png?format=webp&quality=lossless",
            image = "https://images-ext-1.discordapp.net/external/ucZeDO84rLbEbF6iPIw_RW5YfjsEBUMHDYgFv2tRAEQ/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1441933074697949247/1ac82574fd38e50e764835eb729ddba7.png?format=webp&quality=lossless"
        )

        return


    category = message.Args[1]
    if not category or category == "":
        return

    for cog in base.Cogs.Commands:
        args = cog.FILEPATH.split("/")
        ctg = args[len(args) - 2]

        if category == ctg:
            try: cmds[f"{base.Servers[message.Client.guild.id].Prefix}{cog.COMMAND}"] = [cog.INFO["Description"], False]
            except: continue

    await message.send_embed(
        "Help", "Welcome to Insanity V2", cmds, 
        author_name = "Insanity", 
        author_url = "https://images-ext-1.discordapp.net/external/ucZeDO84rLbEbF6iPIw_RW5YfjsEBUMHDYgFv2tRAEQ/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1441933074697949247/1ac82574fd38e50e764835eb729ddba7.png?format=webp&quality=lossless",
        image = "https://images-ext-1.discordapp.net/external/ucZeDO84rLbEbF6iPIw_RW5YfjsEBUMHDYgFv2tRAEQ/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1441933074697949247/1ac82574fd38e50e764835eb729ddba7.png?format=webp&quality=lossless"
    )