import discord

from utils import *

__err__ = discord.Embed(title = "Join | Error", description = "List of Join VC Commands", color = discord.Colour.red())
__err__.add_field(name = "Join Current VC", value = "```>join --me```", inline = False)
__err__.add_field(name = "Join Current VC", value = "```>join <vc_id>```", inline = False)
__err__.set_author(name = "Insanity")
__err__.set_footer(text = "https://insanity.host")

__JOIN_INFO__ = {
    "Name": "Join",
    "Description": "Join VC",
    "Get_Base": True,
    "ArgCount": 2,
    "Invalid_Arg_Err": __err__
}

async def join(base, message: DiscordUtils) -> bool:
    server = base.find_server_config(message.Client.guild.id)
    join_query = message.Args[1].replace("<#", "").replace(">", "")
    
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