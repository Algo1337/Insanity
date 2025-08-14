import discord, pytz

from datetime import timezone
from src.discord_utils import *

____ON_MESSAGE___GET_BASE__ = True

def append_to_logs(msg: str) -> bool:
    if not msg or msg == "":
        return False
    
    try:
        fd = open("assets/messages.log", "a+")
        fd.write(f"{msg}\n")
        fd.close()
        return True
    except:
        return False

def blacklisted_token_check(args: list[str], blacklisted_token: list[str]) -> bool:
    for arg in args:
        if arg in blacklisted_token:
            return True

    return False


async def __on_message__(base, message: DiscordUtils) -> bool:
    
    local_tz = pytz.timezone('America/Kentucky/Louisville')
    timestamp = message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')
    print(f"[ MESSAGE: {timestamp} ]: \x1b[33m{message.Client.id}\x1b[39m | \x1b[31m{message.Client.guild.name}-{message.Client.guild.id}/{message.Client.channel.name}-{message.Client.channel.id}\x1b[0m | \x1b[32m{message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')}\x1b[0m \x1b[33m{message.Client.author.display_name}:{message.Client.author.name}\x1b[0m: {message.Client.content}")
    if not append_to_logs(f"[ MESSAGE: {timestamp} ]: {message.Client.id} | {message.Client.guild.name}-{message.Client.guild.id}/{message.Client.channel.name}-{message.Client.channel.id} | {message.Client.author.display_name}:{message.Client.author.name}: {message.Client.content}"):
        print("[ x ] Error, Failed to log message to file!\n")

    if blacklisted_token_check(message.Args, base.BlacklistedTokens) and f"{message.Client.author.id}" not in base.Whitlist:
        await message.Client.delete()
    
    if message.Client.author.bot:
        return False

    if f"{message.Client.author.id}" not in base.Whitlist:
        return False

    return True

async def LogMessage(message: DiscordUtils) -> bool:
    return True