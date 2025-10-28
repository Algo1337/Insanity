import discord, pytz

from datetime import datetime, timezone
from src.discord_utils import *

____ON_MESSAGE_DELETE___GET_BASE__ = True

def append_to_logs(msg: str) -> bool:
    if not msg or msg == "":
        return False
    
    try:
        fd = open("assets/deleted.log", "a+")
        fd.write(f"{msg}\n")
        fd.close()
        return True
    except:
        return False
    
async def __on_message_delete__(base, message: DiscordUtils) -> bool:
    print(f"{base.user}")
    local_tz = pytz.timezone('America/Kentucky/Louisville')
    timestamp = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")

    base.LastDeleted = message

    print(f"[ DELETED MESSAGE: {timestamp} ] \x1b[33m{message.Client.id}\x1b[39m | \x1b[31m{message.Client.guild.name}-{message.Client.guild.id}/{message.Client.channel.name}-{message.Client.channel.id}\x1b[0m | \x1b[32m{message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')}\x1b[0m \x1b[33m{message.Client.author.display_name}:{message.Client.author.name}\x1b[0m: {message.Client.content}")

    channel = discord.utils.get(message.Client.guild.text_channels, name = "logs")
    if channel:
        await channel.send(embed = discord.Embed(title = f"Logs | Message Deleted", description = f"<@{message.Client.author.id}> has deleted their message!\n\nMessage:```{message.Client.content}```", colour = discord.Colour.red()))
                           
    await message.log(action_t.ON_MESSAGE_DELETE, f"{message.Client.author.display_name}", {"Reason": "DELETED_MESSAGE", "Author": message.Client.author.name})

    if not append_to_logs(f"[ DELETED MESSAGE: {timestamp} ] {message.Client.id} | {message.Client.guild.name}-{message.Client.guild.id}/{message.Client.channel.name}-{message.Client.channel.id} | {message.Client.author.display_name}:{message.Client.author.name}: {message.Client.content}"):
        print("[ x ] Error, Failed to log message to file!\n")

    return True