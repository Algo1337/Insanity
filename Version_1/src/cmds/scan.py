import discord, pytz, ipaddress

from src.discord_utils import *

__SCAN_GET_BASE__ = True
__SCAN_ARG_COUNT__ = 0
__SCAN_INVALID_ARG_ERR__ = discord.Embed(title = "Info", description = "A list of info commands", color = discord.Colour.red())
__SCAN_INVALID_ARG_ERR__.add_field(name = "**My Server**", value = ">info --server", inline = False)
__SCAN_INVALID_ARG_ERR__.add_field(name = "**My Info**", value = ">info --me", inline = False)
__SCAN_INVALID_ARG_ERR__.add_field(name = "**User Info**", value = ">info --user <@tag/user_id>", inline = False)
__SCAN_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__SCAN_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__SCAN_INVALID_ARG_ERR__.set_footer(text = "https://insanity.bot")

def _append_to_logs(msg: str) -> bool:
    if not msg or msg == "":
        return False
    
    try:
        fd = open("assets/messages.log", "a+")
        fd.write(f"{msg}\n")
        fd.close()
        return True
    except:
        return False
    
async def scan(base, message: DiscordUtils) -> bool:
    parts = message.Client.content[6:].split()

    if len(parts) != 3:
        await message.send_message(
            "Usage: `.scan <server id> <channel id> <target message id>`"
        )
        return

    try:
        guild_id = int(parts[0])
        channel_id = parts[1]
        target_message_id = int(parts[2])
    except ValueError:
        await message.send_message(
            "Server ID, channel ID, and message ID must be numbers."
        )
        return

    guild = base.get_guild(guild_id)

    if guild is None:
        await message.send_message(
            f"Server not found or bot isn't in server `{guild_id}`."
        )
        return

    channel = discord.utils.find(
        lambda c: c.name.lower() == channel_id.lower(),
        guild.text_channels
    )

    if channel is None:
        try:
            channel = await base.fetch_channel(channel_id)
        except discord.NotFound:
            await message.send_message("Channel not found.")
            return
        except discord.Forbidden:
            await message.send_message(
                "I don't have permission to access that channel."
            )
            return

    if not isinstance(channel, discord.TextChannel):
        await message.send_message("That isn't a text channel.")
        return

    await message.send_message(
        f"Scanning **{guild.name}** → **#{channel.name}** up to `{target_message_id}`..."
    )

    messages = []

    try:
        async for msg in channel.history(
            limit=None,
            before=discord.Object(id=target_message_id + 1)
        ):
            messages.append(msg)

    except discord.Forbidden:
        await message.send_message(
            "I don't have permission to read message history in that channel."
        )
        return

    messages.reverse()

    for msg in messages:
        local_tz = pytz.timezone('America/Kentucky/Louisville')
        timestamp = msg.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')
        print(f"[ MESSAGE: {timestamp} ]: \x1b[33m{msg.id}\x1b[39m | \x1b[31m{msg.guild.name}-{msg.guild.id}/{msg.channel.name}-{msg.channel.id}\x1b[0m | \x1b[32m{msg.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')}\x1b[0m \x1b[33m{msg.author.display_name}:{msg.author.name}\x1b[0m: {msg.content}")
        if not _append_to_logs(f"[ MESSAGE: {timestamp} ]: {msg.id} | {msg.guild.name}-{msg.guild.id}/{msg.channel.name}-{msg.channel.id} | {msg.author.display_name}:{msg.author.name}: {msg.content}"):
            print("[ x ] Error, Failed to log message to file!\n")

        # print(
        #     f"[{msg.id}] "
        #     f"{msg.created_at} "
        #     f"{msg.author} ({msg.author.id}): "
        #     f"{msg.content}"
        # )

    await message.send_message(
        f"Logged `{len(messages)}` messages from **#{channel.name}**."
    )