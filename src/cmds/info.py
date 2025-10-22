import discord

from src.discord_utils import *

__INFO_GET_BASE__ = True
__INFO_ARG_COUNT__ = 2
__INFO_INVALID_ARG_ERR__ = discord.Embed(title = "Info", description = "A list of info commands", color = discord.Colour.red())
__INFO_INVALID_ARG_ERR__.add_field(name = "**My Server**", value = ">info --server", inline = False)
__INFO_INVALID_ARG_ERR__.add_field(name = "**My Info**", value = ">info --me", inline = False)
__INFO_INVALID_ARG_ERR__.add_field(name = "**User Info**", value = ">info --user <@tag/user_id>", inline = False)
__INFO_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__INFO_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__INFO_INVALID_ARG_ERR__.set_footer(text = "https://insanity.bot")

async def info(base, msg: DiscordUtils) -> bool:
    opt = msg.Args[1]

    if opt == "--me":
        await msg.send_embed("Info", f"""User Info""", {
            "ID":               [f"{msg.Client.author.id}", True],
            "Name":             [f"{msg.Client.author.name}", True],
            "Display_name":     [f"{msg.Client.author.display_name}", True],
            "Discriminator":    [f"{msg.Client.author.discriminator}", True],
            "Bot":              [f"{msg.Client.author.bot}", True],
            "Created_at":       [f"{msg.Client.author.created_at}", True],
            "Joined_at":        [f"{msg.Client.author.joined_at}", True],
            "Guild":            [f"{msg.Client.author.guild}", True],
            "Top Role":         [f"{msg.Client.author.top_role}", True],
            "Status":           [f"{msg.Client.author.status}", True]
        }, author_name = msg.Client.author.name, author_url = msg.Client.author.avatar.url)
    elif opt == "--user":
        userid = msg.Args[2].replace("<@", "").replace(">", "")

        user = await msg.Client.guild.fetch_member(userid)
        await msg.send_embed("Info", f"""User Info""", {
            "ID":               [f"{user.id}", True],
            "Name":             [f"{user.name}", True],
            "Display_name":     [f"{user.display_name}", True],
            "Discriminator":    [f"{user.discriminator}", True],
            "Bot":              [f"{user.bot}", True],
            "Created_at":       [f"{user.created_at}", True],
            "Joined_at":        [f"{user.joined_at}", True],
            "Guild":            [f"{user.guild}", True],
            "Top Role":         [f"{user.top_role}", True],
            "Status":           [f"{user.status}", True]
        }, author_name = user.name, author_url = user.avatar.url)

    return True