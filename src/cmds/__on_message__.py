import discord, pytz

from datetime import timezone
from src.discord_utils import *

__CURRNET_ADMINS__ = [
    1396851228478013515,
    1235776145819959318,
    1163510493546291240,
    1353514131973476413,
    1086011435584331857,
    1383824779873878126
]

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


async def __on_message__(base, message: DiscordUtils) -> bool:
    global __CURRNET_ADMINS__
    
    local_tz = pytz.timezone('America/Kentucky/Louisville')
    timestamp = message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')
    print(f"[ MESSAGE: {timestamp} ]: \x1b[33m{message.Client.id}\x1b[39m | \x1b[31m{message.Client.guild.name}-{message.Client.guild.id}/{message.Client.channel.name}-{message.Client.channel.id}\x1b[0m | \x1b[32m{message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')}\x1b[0m \x1b[33m{message.Client.author.display_name}:{message.Client.author.name}\x1b[0m: {message.Client.content}")
    if not append_to_logs(f"[ MESSAGE: {timestamp} ]: {message.Client.id} | {message.Client.guild.name}-{message.Client.guild.id}/{message.Client.channel.name}-{message.Client.channel.id} | {message.Client.author.display_name}:{message.Client.author.name}: {message.Client.content}"):
        print("[ x ] Error, Failed to log message to file!\n")

    if len(base.Whitlist) == 0:
        base.Whitlist = __CURRNET_ADMINS__
    
    if message.Client.author.bot:
        return False

    if message.Client.author.id not in __CURRNET_ADMINS__:
        return False

    return True

async def LogMessage(message: DiscordUtils) -> bool:
    return True