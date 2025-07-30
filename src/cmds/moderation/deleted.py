import discord

from src.discord_utils import *

def get_deleted_msgs(guild_id: int) -> str:
    if guild_id and guild_id == 0:
        return ""
    
    f = open("assets/deleted.log", "r")
    lines = f.read().split("\n")[::-1]
    data = []
    count = 0
    for line in lines:
        if f"{guild_id}" in line:
            data.append(f"{line}\n")
            count += 1

        if count == 3:
            break
        
    f.close()
    return data

async def deleted(message: DiscordUtils) -> bool:
    await message.Client.delete()

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