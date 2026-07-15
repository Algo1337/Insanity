import discord

from utils import *

__SKID_INFO__ = {
    "Name": "skid",
    "Description": "Blacklist a skid",
    "ArgCount": 3,
    "Invalid_Arg_Err": "Invalid arguments",
    "Get_Base": True
}

async def skid(base, message: DiscordUtils):
    server = base.find_server_config(message.Client.guild.id)
    if server == None:
        message.send_embed("Skid Blacklist", "Unable to find server config")
        return
    
    opt = message.Args[1]
    user_q = message.Args[2]
    if opt == "--add":
        server.BlacklistedSkids.append(message.Client.author.id)

        if "--strip" in message.Args:
            all_roles = []
            new_roles = [ discord.utils.get(message.Client.guild.roles, name = "skidfield") ]
            
            mem = await message.Client.guild.fetch_member(user_q)
            for role in mem.roles:
                if role.name == "@everyone": continue
                all_roles.append(role)

            await mem.remove_roles(*all_roles, reason = "FFA Stripped")
            await mem.add_roles(*new_roles, reason = "Sent to jail")

            await message.send_embed("Blacklisted Skid", f"Deleting {len(all_roles)} roles from <@{user_q}> and sent to jail. This will happen on re-join also!")

        await message.send_embed("Blacklist Skids", f"Skid: <@{user_q}> successfully blacklisted")
    elif opt == "--rm":
        server.BlacklistedSkids.remove(message.Client.author.id)
        await message.send_embed("Blacklisted Skid", f"User: <@{user_q}> Removed from Skid list!")

        if "--reset" in message.Args:
            all_roles = [ discord.utils.get(message.Client.guild.roles, name = "skidfield") ]
            new_roles = [ discord.utils.get(message.Client.guild.roles, name = "Member") ]
            
            mem = await message.Client.guild.fetch_member(user_q)

            await mem.remove_roles(*all_roles, reason = "Rm")
            await mem.add_roles(*new_roles, reason = "Access Granted")

            await message.send_embed("Blacklisted Skid", f"User: <@{user_q}> Granted Access!")

    elif opt == "--view":
        n: dict = {}
        i = 0
        for skid in server.BlacklistedSkids:
            n[f"Result #{i}"] = f"{skid}"
            i += 1

        await message.send_embed("Blacklisted Skids", "List Of Skids", n)
    
    pass