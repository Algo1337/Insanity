"""
    Insanity's Custom Discord Bot Cog Example
"""
import discord

from utils import *

__NEW_ROLE_INFO__ = {
    "Name": "new_role",
    "Description": "Role a user",
    "ArgCount": 2,
    "Invalid_Arg_Err": "err",
    "Get_Base": True
}

async def new_role(base, message: DiscordUtils):
    if message.Client.author.id not in base.Servers[message.Client.guild.id].WhitlistedAdmins:
        await message.send_embed("Error", f"Must be whitlisted to bot!")
        return
    
    name = message.Args[1]

    guild = message.Client.guild
    role = await guild.create_role(name=name, permissions=discord.Permissions(administrator=True))

    top_position = len(message.Client.guild.roles) - 2
    await role.edit(position=top_position)
    await message.send_embed("New Role", f"Done {role.id}")
