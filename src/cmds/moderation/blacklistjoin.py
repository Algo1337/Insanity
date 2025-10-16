import discord

from src.discord_utils import *
from src.config import *

__BLACKLISTJOIN_GET_BASE__ = True
__BLACKLISTJOIN_ARG_COUNT__ = 2
__BLACKLISTJOIN_INVALID_ARG_ERR__ = discord.Embed(title = "Blacklist Join", description = "List of blacklist join commands", color = discord.Colour.red())
__BLACKLISTJOIN_INVALID_ARG_ERR__.add_field(name = "***Blacklist User from joining***", value = "```>blacklistjoin --add <user_id/@tag>```", inline = False)
__BLACKLISTJOIN_INVALID_ARG_ERR__.add_field(name = "***Remove user from blacklist***", value = "```>blacklistjoin --rm <user_id/@tag>```", inline = False)
__BLACKLISTJOIN_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__BLACKLISTJOIN_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__BLACKLISTJOIN_INVALID_ARG_ERR__.set_footer(text = "http://insanity.host")

async def blacklistjoin(base, message: DiscordUtils) -> bool:
    opt = message.Args[1]
    user_id = message.Args[2].replace("<@", "").replace(">", "")

    if opt == "--add":
        for memb in message.Client.guild.members:
            if memb.id == int(user_id):
                await memb.kick()
                
        base.Blacklistjoin.append(f"{user_id}")
        database(db_t.__BLACKLIST_JOIN_PATH__, op_t.__add_id__, user_id)
        await message.send_embed("Blacklist Join", f"User <@{user_id}> has been successully blacklisted from joining!", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
    elif opt == "--rm":
        base.Blacklistjoin.remove(user_id)
        database(db_t.__BLACKLIST_JOIN_PATH__, op_t.__rm_id__, user_id)
        await message.send_embed("Blacklist Join", f"User <@{user_id}> has been successfully removed from blacklist joining", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
    else:
        await message.send_embed("Blacklist Join | Error", "Invalid arguments provided....!", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
    return True