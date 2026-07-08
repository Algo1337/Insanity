import discord

from src.discord_utils import *

__BAN_GET_BASE__ = True
__BAN_ARG_COUNT__ = 2
__BAN_INVALID_ARG_ERR__ = discord.Embed(
    title = "Ban",
    description = "Error, Invalid arguments provided!\nUsage ;ban <user_id> <?reason>",
    color = discord.Colour.red()
)
__BAN_INVALID_ARG_ERR__.set_author(name = "Insanity")
__BAN_INVALID_ARG_ERR__.set_footer(text = "http://insanity.host")

async def ban(base, message: DiscordUtils) -> bool:
    if not (message.Client.author.guild_permissions.administrator and message.Client.author.guild_permissions.manage_messages):
        await message.send_embed("Ban | Error", "You must be an adminstrator of this server to use this command!\n")
        return

    if message.Args[1].replace("<@", "").replace(">", "").isdigit() == False:
        await message.send_embed("Ban | Error", "Missing user id or tag!", image = "https://media.discordapp.net/attachments/1400104223508533309/1400134712839770193/test.png?ex=688b8890&is=688a3710&hm=6e8c70c936bfbb7a6cbd9fb727e14d7a95d8b64d9be770a2d76044fc558a0c5e&=&format=webp&quality=lossless")
        return False
    
    userid = int(message.Args[1].replace("<@", "").replace(">", ""))
    userobj = await message.Client.guild.fetch_member(userid)

    if not userobj or userobj == None:
        await message.send_embed("Ban | Error", "Missing user id or tag!", image = "https://media.discordapp.net/attachments/1400104223508533309/1400134712839770193/test.png?ex=688b8890&is=688a3710&hm=6e8c70c936bfbb7a6cbd9fb727e14d7a95d8b64d9be770a2d76044fc558a0c5e&=&format=webp&quality=lossless")
        return False
    
    reason = None
    if len(message.Args) > 2:
        reason = " ".join(message.Args[2:])
    
    await message.Client.guild.ban(userobj, reason = reason)
    await message.send_embed("Ban", f"User <@{userobj.id}> successfully banned for:\n\n```{reason}```", image = "https://media.discordapp.net/attachments/1400104223508533309/1400134712839770193/test.png?ex=688b8890&is=688a3710&hm=6e8c70c936bfbb7a6cbd9fb727e14d7a95d8b64d9be770a2d76044fc558a0c5e&=&format=webp&quality=lossless", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
    return True