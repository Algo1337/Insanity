import discord, pytz, ipaddress

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

async def blacklisted_token_check(msg: DiscordUtils, blacklisted_token: list[str]) -> tuple[bool, str]:
    msg_args = msg.Client.content.split(" ")
    for token in blacklisted_token:
        for tkn in msg_args:
            if token.lower() in tkn.lower() or token.lower() == tkn.lower():
                return True, token
            
            try:
                if ipaddress.ip_address(tkn):
                    await msg.log(action_t.ON_MESSAGE_DELETE, "IP Detected", {"User": msg.Client.author.name, "ID": msg.Client.author.id})
                    # return True
            except: continue

    return False, ""

async def __on_message__(base, message: DiscordUtils) -> bool:
    local_tz = pytz.timezone('America/Kentucky/Louisville')
    timestamp = message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')
    print(f"[ MESSAGE: {timestamp} ]: \x1b[33m{message.Client.id}\x1b[39m | \x1b[31m{message.Client.guild.name}-{message.Client.guild.id}/{message.Client.channel.name}-{message.Client.channel.id}\x1b[0m | \x1b[32m{message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')}\x1b[0m \x1b[33m{message.Client.author.display_name}:{message.Client.author.name}\x1b[0m: {message.Client.content}")
    if not append_to_logs(f"[ MESSAGE: {timestamp} ]: {message.Client.id} | {message.Client.guild.name}-{message.Client.guild.id}/{message.Client.channel.name}-{message.Client.channel.id} | {message.Client.author.display_name}:{message.Client.author.name}: {message.Client.content}"):
        print("[ x ] Error, Failed to log message to file!\n")

    if message.Client.author.bot:
        return False
    
    ckh, string = (await blacklisted_token_check(message, base.BlacklistedTokens))
    if  ckh and f"{message.Client.author.id}" not in base.Whitlist:
        await message.log(action_t.ON_MESSAGE_DELETE, f"Reason: Blacklisted Word -> {string}\n\nContent:\n\n{message.Client.content}")
        await message.Client.delete()

    if f"{message.Client.author.id}" not in base.Whitlist:
        return False

    return True

async def LogMessage(message: DiscordUtils) -> bool:
    return True