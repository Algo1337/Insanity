import discord

from src.discord_utils import *

def get_deleted_msgs(guild_id: int) -> str:
    if guild_id and guild_id == 0:
        return ""
    
    f = open("assets/deleted.log", "r")
    lines = f.read().split("\n")
    data = []
    for line in lines:
        if f"{guild_id}" in line:
            data.append(f"{line}\n")
        
    f.close()
    return data

async def deleted(message: DiscordUtils) -> bool:
    data = get_deleted_msgs(message.Client.guild.id)
    r = "\n".join(data)
    if len(r) > 1999:
        await message.send_message(r)
        return True
    
    await message.send_embed("Deleted Message", f"```{r}```", image = "https://media.discordapp.net/attachments/1400104223508533309/1400134712839770193/test.png?ex=688b8890&is=688a3710&hm=6e8c70c936bfbb7a6cbd9fb727e14d7a95d8b64d9be770a2d76044fc558a0c5e&=&format=webp&quality=lossless")
    return True