"""
    Insanity's Custom Discord Bot Cog Example
"""
import discord

from src.discord_utils import *

# Optional: Create an embed for invalid argument error
embed = discord.Embed(title="Help", description = "Error, Invalid arguments\nType ;help for a list of commands")
embed.set_author(name="Bot")
embed.set_footer(text="Footer text here.")

## Declare the amount of arguments for this command accepted
## Since this is help, it doesn't need none upon execution
__HELP_ARG_COUNT__ = 0

## For Cmds with argument, A variable with the starting and ending prefix must be valid
## Starting with '__', command name in all capital, and ending with '_INVALID_ARG_ERR__'
## You can use a string or an embed (discord.Embed)
__HELP_INVALID_ARG_ERR__ = embed

async def help(message: DiscordUtils):
    if len(message.Args) > 0 and message.Args[1] == "-fun":
        await message.send_embed("Help", "working on it bub", {
            "**Say**": ["```;say <text>```", True]
        })
        return

    await message.send_embed("Help", "A list of categories of commands", {
        "Info": "```;help -info",
        "Fun": "```;help -fun```",
        "VC": "```;help -vc```",
        "Mod": "```;help -mod```",
        "Settings": "```;help settings```"
    })