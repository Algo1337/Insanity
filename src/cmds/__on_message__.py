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

def append_to_logs(msg: str) -> bool:
    if not msg or msg == "":
        return False
    
    try:
        fd = open("assets/messages.log", "r+")
        fd.write(msg)
        fd.close()
        return True
    except:
        return False


async def __on_message__(message: DiscordUtils) -> bool:
    global __CURRNET_ADMINS__
    
    if message.Client.author.bot:
        return False
    
    local_tz = pytz.timezone('America/Kentucky/Louisville')
    timestamp = message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')
    if not append_to_logs(f"[ MESSAGE: {timestamp} ] {message.Client.guild.name}/{message.Client.channel.name} | {message.Client.author.display_name}:{message.Client.author.name}: {message.Client.content}"):
        print("[ x ] Error, Failed to log message to file!\n")

    if message.Client.author.id not in __CURRNET_ADMINS__:
        return False

    return True

async def LogMessage(message: DiscordUtils) -> bool:
    return True