import discord

from utils import *

__err__ = discord.Embed(title = "Info", description = "A list of info commands", color = discord.Colour.red())
__err__.add_field(name = "**My Server**", value = ">info --server", inline = False)
__err__.add_field(name = "**My Info**", value = ">info --me", inline = False)
__err__.add_field(name = "**User Info**", value = ">info --user <@tag/user_id>", inline = False)
__err__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__err__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__err__.set_footer(text = "https://insanity.bot")

__SERVERS_INFO__ = {
    "Name": "Servers",
    "Description": "List all servers the bot is in!",
    "ArgCount": 0,
    "Invalid_Arg_Err": __err__,
    "Get_Base": True
}

async def servers(base, message: DiscordUtils) -> bool:
    embed: discord.Embed = discord.Embed(
        title = __SERVERS_INFO__["Name"],
        description = __SERVERS_INFO__["Description"],
        color = discord.Colour.red()
    )

    for guild in base.guilds:
        if guild.id in base.Servers:
            embed.add_field(name = guild.name, value = f"{guild.id} | {guild.member_count} Members", inline = False)

    await message.Client.channel.send(embed = embed)
    return True