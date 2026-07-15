import discord

from utils import *

__err__ = discord.Embed(title = "Blacklist Token", description = "Blacklist a token from messages!", color = discord.Colour.red())
__err__.add_field(name = "**Blacklist Token**", value = ">bltoken --add <token>", inline = False)
__err__.add_field(name = "**Remove Blacklist Token**", value = ">bltoken --rm <token>", inline = False)
__err__.add_field(name = "**View Blacklisted Tokens**", value = ">bltoken --view --all", inline = False)
__err__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__err__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__err__.set_footer(text = "https://insanity.bot")

__BLTOKEN_INFO__ = {
    "Name": "bltoken",
    "Description": "Blacklist a token",
    "ArgCount": 3,
    "Invalid_Arg_Err": __err__,
    "Get_Base": True
}

async def bltoken(base, message: DiscordUtils):
    server = base.find_server_config(message.Client.guild.id)
    opt = message.Args[1]
    user_q = message.Args[2]

    if opt == "--add":
        server.BlacklistedTokens.append(user_q)
        await message.send_embed("Blacklisted Tokens", f"Token: {user_q} successfully blacklisted!")
    elif opt == "--rm":
        server.BlacklistedTokens.remove(user_q)
        await message.send_embed("Blacklisted Tokens", f"Token: {user_q} removed from blacklist!")
    elif opt == "--view":
        n = ""
        i = 0
        for tkn in server.BlacklistedTokens:
            n += f"{tkn}\n"

        await message.send_embed("Blacklisted Tokens", f"List Of Blacklisted Tokens\n\n```{n}```")