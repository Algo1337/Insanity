import discord, pytz

from datetime import datetime, timezone
from utils import *

____ON_MESSAGE_DELETE___INFO__ = {
    "Get_Base": True
}
    
async def __on_message_delete__(base, message: DiscordUtils) -> bool:
    server = base.find_server_config(message.Client.guild.id)
    if message.Client.author.bot:
        return
    
    """ Command Check """
    if message.Client.content.startswith(server.Prefix) == False:
        server.LastDeleted = message

    """ Message Log """
    local_tz = pytz.timezone('America/Kentucky/Louisville')
    timestamp = message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')
    msg_id = message.Client.id
    server_name = message.Client.guild.name
    server_id = message.Client.guild.id
    channel_name = message.Client.channel.name
    channel_id = message.Client.channel.id
    display_name = message.Client.author.display_name
    username = message.Client.author.name
    userid = message.Client.author.id
    created_at = message.Client.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')
    print(f"\x1b[35m[DELETED MESSAGE: {timestamp}]\x1b[39m: {msg_id} | {server_name}({server_id}) - {channel_name}({channel_id})\n\x1b[32m{username}({userid}) - {display_name}: {message.Client.content}\x1b[39m")

    """ Log Delete """
    channel = discord.utils.get(message.Client.guild.text_channels, name = "logs")
    if channel:
        await channel.send(embed = discord.Embed(title = f"Logs | Message Deleted", description = f"<@{message.Client.author.id}> has deleted their message!\n\nMessage:```{message.Client.content}```", colour = discord.Colour.red()))
                           
    # await message.log(action_t.ON_MESSAGE_DELETE, f"{message.Client.author.display_name}", {"Reason": "DELETED_MESSAGE", "Author": message.Client.author.name})

    # if not append_to_logs(f"[ DELETED MESSAGE: {timestamp} ] {message.Client.id} | {message.Client.guild.name}-{message.Client.guild.id}/{message.Client.channel.name}-{message.Client.channel.id} | {message.Client.author.display_name}:{message.Client.author.name}: {message.Client.content}"):
    #     print("[ x ] Error, Failed to log message to file!\n")

    return True