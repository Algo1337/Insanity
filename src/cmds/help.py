"""
    Insanity's Custom Discord Bot Cog Example
"""
import discord

from src.discord_utils import *

async def help(message: DiscordUtils):
    if len(message.Args) > 0:
        if message.Args[1] == "-info":
            await message.send_embed("Help", "List of info commands", {
                "**My Info**": ["```>info --me```", False],
                "**Server Info**": ["```>info --server```", False],
                "**Permission Check**": ["```>info --perms```", False]
            })
        elif message.Args[1] == "-fun":
            await message.send_embed("Help", "List of fun commands", {
                "**Say**": ["```>say <text>```", False]
            })
        elif message.Args[1] == "-vc":
            await message.send_embed("VC", "List of VC commands", {
                "**Join VC**": ["```>join <vc>```", False],
                "**TTS**": ["```>tts <?volume> <text>```", False],
                "**TTS2**": ["```>tts2 <volume> <text>```", False],
                "**Watch VC**": ["```>watchvc <vc>```", False]
            })
        # elif message.Args[1] == "-settings"
        return

    await message.send_embed("Help", "A list of categories of commands", {
        "Info": "```>help -info```",
        "Fun": "```>help -fun```",
        "VC": "```>help -vc```",
        "Mod": "```>help -mod```",
        "Settings": "```>help settings```"
    })