import discord

from src.discord_utils import *
from src.config import *

__SKID_GET_BASE__ = True
__SKID_ARG_COUNT__ = 3
__SKID_INVALID_ARG_ERR__ = discord.Embed(title = "Force List Of Skids Lockup", description = "Strip roles and force skid jail\n\nUse ``--strip`` to strip role from users!", color = discord.Colour.red())
__SKID_INVALID_ARG_ERR__.add_field(name = "**Add Skid to Jail**", value = "```>nuke --add <@tag/userid>```", inline = False)
__SKID_INVALID_ARG_ERR__.add_field(name = "**Remove Skid from Jail**", value = "```>nuke --rm <@tag/userid>```", inline = False)
__SKID_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__SKID_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__SKID_INVALID_ARG_ERR__.set_footer(text = "https://insanity.bot")

def create_skid_blacklist(id: int, onjoin: bool) -> dict:
    return {id, onjoin};

async def skid(base, msg: DiscordUtils) -> True:
    opt = msg.Args[1]
    userid = msg.Args[2].replace("<@", "").replace(">", "")

    if opt == "--add":
        base.BlacklistedSkids.append(userid)
        # Config.add_blacklistskid(userid)
        database(db_t.__SKIDS_PATH__, op_t.__add_id__, userid)
        
        if "--strip" in msg.Args:
            all_roles = []
            new_roles = [ discord.utils.get(msg.Client.guild.roles, name = "skidfield") ]
            
            mem = await msg.Client.guild.fetch_member(userid)
            for role in mem.roles:
                if role.name == "@everyone": continue
                all_roles.append(role)

            await mem.remove_roles(*all_roles, reason = "FFA Stripped")
            await mem.add_roles(*new_roles, reason = "Sent to jail")

            await msg.send_embed("Blacklisted Skid", f"Deleting all <@{userid}> {len(all_roles)} roles and sent to jail")

        await msg.send_embed("Blacklisted Skid", f"Successfully blacklisted <@{userid}>!")
    elif opt == "--rm":
        if userid not in base.BlacklistedSkids:
            await msg.send_embed("Blacklisted Skid", "Error, The ugly skid isn't blacklisted!")
            return 
        
        base.BlacklistedSkids.remove(userid)
        database(db_t.__SKIDS_PATH__, op_t.__rm_id__, userid)

        if "--strip" in msg.Args:
            all_roles = [ discord.utils.get(msg.Client.guild.roles, name = "skidfield") ]
            new_roles = [ discord.utils.get(msg.Client.guild.roles, name = "Members") ]
            
            mem = await msg.Client.guild.fetch_member(userid)
            for role in mem.roles:
                if role.name == "@everyone": continue
                all_roles.append(role)

            await mem.remove_roles(*all_roles, reason = "Removed from jail")
            await mem.add_roles(*new_roles, reason = "Removed from jail")

        await msg.send_embed("Blacklisted Skid", f"Successfully removed <@{userid}> from the blacklisted skid list!")
    elif opt == "--view":
        fields = {}
        i = 0
        for uid in base.BlacklistedSkids:
            fields[f"Skid {i}"] = f"<@{uid}>"
            i += 1

        await msg.send_embed("Blacklisted Skids", "List Of Skids", fields)
        
    return True