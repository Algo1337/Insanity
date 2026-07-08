import discord

from src.discord_utils import *

__SERVERS_GET_BASE__ = True
__SERVERS_ARG_COUNT__ = 0
__SERVERS_INVALID_ARG_ERR__ = discord.Embed(title = "Info", description = "A list of info commands", color = discord.Colour.red())
__SERVERS_INVALID_ARG_ERR__.add_field(name = "**My Server**", value = ">info --server", inline = False)
__SERVERS_INVALID_ARG_ERR__.add_field(name = "**My Info**", value = ">info --me", inline = False)
__SERVERS_INVALID_ARG_ERR__.add_field(name = "**User Info**", value = ">info --user <@tag/user_id>", inline = False)
__SERVERS_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__SERVERS_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__SERVERS_INVALID_ARG_ERR__.set_footer(text = "https://insanity.bot")

async def servers(base, message: DiscordUtils) -> bool:
    embed: discord.Embed = discord.Embed(title = "Server List", description = "List of server the bot is in!", color = discord.Colour.red())
    for guild in base.guilds:
        embed.add_field(name = guild.name, value = f"{guild.id}", inline = False)

    await message.Client.channel.send(embed = embed)
    return True