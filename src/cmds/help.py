"""
    Insanity's Custom Discord Bot Cog Example
"""
import discord

from src.discord_utils import *

async def help(message: DiscordUtils):

    if message.Args.__len__() > 1:
        if message.Args[1] == "-info":
            await message.send_embed("Fun", "List of info commands\n\nKeep in mind: ``?`` stands for optional argument", {
                "**Servers I'm In**": "```>servers```",
                "**All Commands**": "```>commands```",
                "**My Info**": "```>info --me```",
                "**Server Info**": "```>info --server```",
                "**Permission Check**": "```>info --perms```"
            }, author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
        elif message.Args[1] == "-fun":
            await message.send_embed("Fun", "List of fun commands\n\nKeep in mind: ``?`` stands for optional argument", {
                "**Say**": "```>say <?@chat> <text>```"
            }, author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
        elif message.Args[1] == "-vc":
            await message.send_embed("VC", "List of VC commands\n\nKeep in mind: ``?`` stands for optional argument", {
                "**Join VC**": "```>join```",
                "**TTS**": "```>tts <?volume> <text>```",
                "**TTS2**": "```>tts2 <volume> <text>```",
                "**Play Youtube**": "```>yt <url>```",
                "**Stop Youtube**": "```>stopyt```"
            }, author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
        elif message.Args[1] == "-mod":
            await message.send_embed("Mod", "List of moderation commands\n\nKeep in mind: ``?`` stands for optional argument", {
                "**Nuke**": "```>nuke```",
                "**Kick**": "```>kick```",
                "**Compress**": "```>compress```",
                "**Logs**": "```>logs```",
                "**Ban**": "```>ban```",
                "**Deleted Messages**": "```>deleted```",
            }, author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
        elif message.Args[1] == "-settings":
            await message.send_embed("Settings", "List of setting(s) commands\n\nThese commands are for whitlisted users only!\n\nKeep in mind: ``?`` stands for optional argument", {
                "**Watch VC**": "```>watchvc```",
                "**Stop Watch**": "```>stopwatch```",
                "**Switch VC Region**": "```>switch```",
                "**Blacklist Token": "```>bltoken```",
                "**Whitlist user**": "```>whitlist```",
                "**Blacklist Skid**": "```>skid```",
                "**Steal**": "```>steal```"
            }, author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
        return

    await message.send_embed("Help", "A list of categories of commands\n\nKeep in mind: ``?`` stands for optional argument", {
        "Info": "```>help -info```",
        "Fun": "```>help -fun```",
        "VC": "```>help -vc```",
        "Mod": "```>help -mod```",
        "Settings": "```>help -settings```"
    }, author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")