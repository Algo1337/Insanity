import discord, random, os

from gtts import gTTS
from discord import ChannelType, FFmpegPCMAudio

from src.discord_utils import *


__TTS_ARG_COUNT__ = 2

async def tts(base, message: DiscordUtils) -> bool:
    await message.Client.delete()
    if not message.Client.author.voice:
        await message.send_embed("TTS | Error", "You must be in a VC to use this!", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
        return
    
    """
        Check if in a VC already
    """
    if message.Client.guild.voice_client and message.Client.guild.voice_client.channel.id != message.Client.author.voice.channel.id:
        await message.send_embed("Join", f"Leaving VC: ``{message.Client.guild.voice_client.channel.name}`` for the VC your in!", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
        await message.Client.guild.voice_client.disconnect()

        vc = await message.Client.author.voice.channel.connect()
        await vc.guild.me.edit(mute=True, deafen=True)
        await message.send_embed("Join", f"Successfully joined ``{message.Client.author.voice.channel.name}``", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")

    vc = message.Client.author.voice.channel
    volume = 5
    text = " ".join(message.Args[1:])
    if len(message.Args) > 1 and message.Args[1].isdigit():
        volume = int(message.Args[1])
        text = text.replace(f"{message.Args[1]} ", "")

    if message.Args[len(message.Args) - 2].startswith("--repeat="):
        text = text.replace(f"{message.Args[len(message.Args) - 2]} ", "").replace(f"{message.Args[len(message.Args) - 2]} ", "")

    if "--q" in message.Args:
        text = text.replace("--q", "")

    tts = gTTS(text, lang="en", tld="co.uk")
    name = random.randint(0, 99999)
    tts.save(f"{name}.mp3")

    await vc.guild.me.edit(mute=False, deafen=True)
    if message.Args[len(message.Args) - 2].startswith("--repeat="):
        repeat_count = int(message.Args[len(message.Args) - 2].replace("--repeat=", ""))
        for _ in range(0, repeat_count):
            audio_source = FFmpegPCMAudio(f"{name}.mp3", options= f'-filter:a "volume={volume}"')
            message.Client.guild.voice_client.play(audio_source)
            await asyncio.sleep(1/2)
            while message.Client.guild.voice_client.is_playing():
                await asyncio.sleep(1)
    else:
        audio_source = FFmpegPCMAudio(f"{name}.mp3", options= f'-filter:a "volume={volume}"')
        message.Client.guild.voice_client.play(audio_source)
        await asyncio.sleep(1/2)
        while message.Client.guild.voice_client.is_playing():
            await asyncio.sleep(1)

    os.remove(f"{name}.mp3")
    await vc.guild.me.edit(mute=True, deafen=True)
    
    if message.Args[len(message.Args) - 1] == "--q":
        return True
            
    await message.send_embed("TTS", f"[ + ] TTS \"{text}\" @ volume: {volume} Done", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
    return True