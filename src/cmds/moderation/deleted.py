import discord

from src.discord_utils import *

__DELETED_GET_BASE__ = True
__DELETED_ARG_COUNT__ = 0
__DELETED_INVALID_ARG_ERR__ = discord.Embed(title = "Deleted Message", description = "List of deleted message commands", color = discord.Colour.red())
__DELETED_INVALID_ARG_ERR__.add_field(name = "***Display the last 3 deleted messages***", value = "```>deleted```", inline = False)
__DELETED_INVALID_ARG_ERR__.add_field(name = "***Display user messages***", value = "```>delete <@user> <count>```", inline = False)
__DELETED_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__DELETED_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__DELETED_INVALID_ARG_ERR__.set_footer(text = "http://insanity.host")

def get_deleted_msgs(guild_id: int, user_id = None, maxc = 3) -> str:
    if guild_id and guild_id == 0:
        return ""
    
    f = open("assets/deleted.log", "r")
    lines = f.read().split("\n")[::-1]
    data = []
    count = 0
    for line in lines:
        if user_id != None:
            if f"{guild_id}" in line and f"{user_id}" in line:
                data.append(f"{line}\n")
                count += 1

        elif f"{guild_id}" in line:
            data.append(f"{line}\n")
            count += 1

        if count == maxc:
            break
        
    f.close()
    return data

async def deleted(base, message: DiscordUtils) -> bool:
    await message.Client.delete()

    if "--h" in message.Data:
        await message.Client.channel.send(embed = __DELETED_INVALID_ARG_ERR__)
        return True
        
    if " " in message.Client.content:
        user_id = message.Args[1].replace("<@", "").replace(">", "")
        maxc = 3
        if len(message.Args) > 1:
            maxc = int(message.Args[2])

        data = get_deleted_msgs(message.Client.guild.id, user_id, maxc)
    else:
        data = get_deleted_msgs(message.Client.guild.id)

    embed = discord.Embed(title = "Deleted Messages", description = "The last deleted message: ", color = discord.Colour.red())
    c = 0
    for line in data:
        embed.add_field(name = f"***Result #{c}***", value = f"```{data[c]}```", inline = False)
        c += 1
    
    embed.set_author(name = "Insanity")
    embed.set_footer(text = "https://insanity.host")

    await message.Client.channel.send(embed = embed)
    return True