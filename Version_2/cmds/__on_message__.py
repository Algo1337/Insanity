import discord, pytz, ipaddress

from datetime import timezone
from utils import *

____ON_MESSAGE___INFO__ = {
    "Get_Base": True
}

""" 
    TODO; Implement a new logger
"""
# def append_to_logs(msg: str) -> bool:
#     if not msg or msg == "":
#         return False
    
#     try:
#         fd = open("assets/messages.log", "a+")
#         fd.write(f"{msg}\n")
#         fd.close()
#         return True
#     except:
#         return False

async def blacklisted_token_check(msg: DiscordUtils, blacklisted_token: list[str]) -> tuple[bool, str]:
    msg_args = msg.Client.content.split(" ")
    for token in blacklisted_token:
        for tkn in msg_args:
            if token.lower() in tkn.lower() or token.lower() == tkn.lower():
                return True, token
            
            try:
                
                if ipaddress.ip_address(tkn):
                    # await msg.log(action_t.ON_MESSAGE_DELETE, "IP Detected", {"User": msg.Client.author.name, "ID": msg.Client.author.id})
                    return True, token
            except: continue

    return False, ""

async def __on_message__(base, message: DiscordUtils) -> bool:
    server = base.find_server_config(message.Client.guild.id)
    if message.Client.author.bot:
        return
    
    """ Command Check """
    if not message.Client.content.startswith(server.Prefix):
        server.LastMessage = message

    """ Sticker Check """
    if message.Client.content == "" and message.Client.guild.id == base.CreatorServerID:
        if message.Client.stickers or len(message.Client.stickers) > 0:
            for sticker in message.Client.stickers:
                message.Redirect = True
                message.rChannel = base.CreatorMemeID
                await message.redirect_message(f"``{message.Client.author.display_name}``/``{message.Client.author.name}`` Sent a sticker ``{sticker.name}`` from ``{message.Client.guild.name}`` -> ``{message.Client.channel.name}``")
                await message.redirect_message(f"{sticker.url}")
                message.Redirect = False

    """ Message Log """
    local_tz = pytz.timezone('America/Kentucky/Louisville')
    timestamp = message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y-%H:%M:%S')
    msg_id = message.Client.id
    server_name = message.Client.guild.name
    server_id = message.Client.guild.id
    channel_name = message.Client.channel.name
    channel_id = message.Client.channel.id
    display_name = message.Client.author.display_name
    username = message.Client.author.name
    userid = message.Client.author.id
    created_at = message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y-%H:%M:%S')

    print(f"\x1b[35m[MESSAGE: {timestamp}]\x1b[39m: {msg_id} | {server_name}({server_id}) - {channel_name}({channel_id})\n\x1b[32m{username}({userid}) - {display_name}: {message.Client.content}\x1b[39m")

    """ TODO; Implement a logger """
    # if not append_to_logs(f"[ MESSAGE: {timestamp} ]: {message.Client.id} | {message.Client.guild.name}-{message.Client.guild.id}/{message.Client.channel.name}-{message.Client.channel.id} | {message.Client.author.display_name}:{message.Client.author.name}: {message.Client.content}"):
    #     print("[ x ] Error, Failed to log message to file!\n")
    
    """ Blacklisted Token Check """
    ckh, string = (await blacklisted_token_check(message, server.BlacklistedTokens))
    if  ckh and f"{message.Client.author.id}" not in server.Whitlisted:
        # await message.log(action_t.ON_MESSAGE_DELETE, f"{message.Client.author.display_name}", {"Reason": f"BLACKLISTED_TOKEN -> ``{string}``", "Token": f"{string}", "Author": message.Client.author.name})
        await message.Client.delete()

    # if f"{message.Client.author.id}" not in server.Whitlisted:
    #     return False

    return True

async def LogMessage(message: DiscordUtils) -> bool:
    return True