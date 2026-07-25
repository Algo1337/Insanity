"""
    Insanity's Custom Discord Bot Cog Example
"""
import discord

from utils import *

__ROLE_INFO__ = {
    "Name": "Role",
    "Description": "Role a user",
    "ArgCount": 3,
    "Invalid_Arg_Err": "err",
    "Get_Base": True
}

async def role(base, message: DiscordUtils):
    userid = message.Args[1].replace("<@", "").replace(">", "")
    roleid = message.Args[2].replace("<@&", "").replace(">", "")

    member = message.Client.guild.get_member(int(userid))
    role = message.Client.guild.get_role(int(roleid))

    if member is None or role is None:
        await message.send_embed("Role", f"Cannot grant <@{userid}> <@&{roleid}> role!")
        return

    await member.add_roles(role)
    await message.send_embed("Role", f"Role: <@&{roleid}> granted to <@{userid}>")