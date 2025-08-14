import discord

from src.discord_utils import *
from src.config import *

__BLTOKEN_GET_BASE__ = True
__BLTOKEN_ARG_COUNT__ = 3
__BLTOKEN_INVALID_ARG_ERR__ = discord.Embed(title = "Blacklist Token", description = "Blacklist a token from channels", color = discord.Colour.red())
__BLTOKEN_INVALID_ARG_ERR__.add_field(name = "**Add token to blacklist**", value = "```>bltoken --add <user_id>```", inline = False)
__BLTOKEN_INVALID_ARG_ERR__.add_field(name = "**Remove token from blacklist**", value = "```>bltoken --rm <user_id>```", inline = False)
__BLTOKEN_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__BLTOKEN_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__BLTOKEN_INVALID_ARG_ERR__.set_footer(text = "https://insanity.bot")

async def bltoken(base, message: DiscordUtils) -> bool:
    opt = message.Args[1]
    token = message.Args[2]

    if opt == "--add":
        base.BlacklistedTokens.append(token)
        Config.add_blacklisted_tokens(token)
        await message.send_embed("Blacklist Token", "Token has successfully been added to blacklist")
    elif opt == "--rm": 
        await message.send_embed("Blacklist Token", "Token has successfully been added to blacklist")

        if token in base.BlacklistedTokens:
            base.BlacklistedTokens.remove(token)

        # i = 0
        # for tkn in base.BlacklistedTokens:
        #     if tkn == token:
        #         base.BlacklistedTokens.remove(i)

        #     i += 1