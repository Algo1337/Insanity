import discord, random, os

from gtts import gTTS

from src.discord_utils import *

async def tts(message: DiscordUtils) -> bool:
    await message.Client.delete()
    if not message.Client.author.voice:
        await message.send_embed("TTS | Error", "You must be in a VC to use this!")
        return
    
    """
        Check if in a VC already
    """
    if message.Client.guild.voice_client and message.Client.guild.voice_client.channel.id != message.Client.author.voice.channel.id:
        await message.send_embed("Join", f"Leaving VC: ``{message.Client.guild.voice_client.channel.name}`` for the VC your in!")
        await message.Client.guild.voice_client.disconnect()

        vc = await message.Client.author.voice.channel.connect()
        await vc.guild.me.edit(mute=True, deafen=True)
        await message.send_embed("Join", f"Successfully joined ``{message.Client.author.voice.channel.name}``")

    volume = 5
    text = " ".join(message.Args[1:])
    if len(message.Args) > 0 and message.Args[1].isdigit():
        volume = int(message.Args[1])
        text = " ".join(message.Args[2:])

    tts = gTTS(text, lang="en", tld="co.uk")
    name = random.randint(0, 99999)
    tts.save(f"{name}.mp3")

    await vc.guild.me.edit(mute=False, deafen=True)
    audio_source = FFmpegPCMAudio(f"{name}.mp3", options= f'-filter:a "volume={volume}"')
    message.guild.voice_client.play(audio_source)
    while message.guild.voice_client.is_playing():
        await asyncio.sleep(1)

    os.remove("test.mp3")
    await vc.guild.me.edit(mute=True, deafen=True)
    if message.content.startswith(";vcsayq"):
            return
            
    await message.channel.send(f"[ + ] TTS \"{text}\" Done")