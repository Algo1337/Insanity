import discord

from ...discord_utils import *

"""
    @Command: nuke

    Formats:
        ;nuke                                               # Clone. Delete Current, Reposition New
        ;nuke <msg_count>                                   # Delete upto msg_count
        ;nuke --user <@tag> <?count(Default set to 100)>    # Delete user's messages up a count, 100 if not provided
"""
async def nuke(client: DiscordUtils) -> None:
    pass