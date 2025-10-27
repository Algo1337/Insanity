import os, discord, yt_dlp

from src.discord_utils import *
from discord import ChannelType, FFmpegPCMAudio

__YT_GET_BASE__ = False
__YT_ARG_COUNT__ = 3
__YT_INVALID_ARG_ERR_ = discord.Embed(title = "Youtube", description = "A list of YT features", color = discord.Colour.red())
__YT_INVALID_ARG_ERR_.add_field(name = "**Download YT Song/Video**", value = "```>yt --file <url>```", inline = False)
__YT_INVALID_ARG_ERR_.add_field(name = "**Play YT Song/Video In VC**", value = "```>yt --file <url>```", inline = False)
__YT_INVALID_ARG_ERR_.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__YT_INVALID_ARG_ERR_.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__YT_INVALID_ARG_ERR_.set_footer(text = "https://insanity.bot")


FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

YDL_OPTIONS = {'format': 'bestaudio'}

YDL_OPTIONZ = {
    'format': 'bestaudio[protocol!=m3u8][ext=m4a]/bestaudio[protocol!=m3u8]/bestaudio',
    'quiet': True,
    'noplaylist': True
}

def download_video(url: str, outdir: str = "assets/yt") -> str:
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    ydl_opts = {
        'outtmpl': f'{outdir}/%(title)s.%(ext)s',
        'format': 'mp4/best',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)  # download + get info
        filename = ydl.prepare_filename(info)       # get actual filepath
        print(f"Saved {filename}")
        return filename

async def yt(base, message: DiscordUtils) -> bool:
    opt = message.Args[1]
    url = message.Args[2]

    if opt == "--play":

        if " " not in message.Client.content:
            return

        await message.Client.author.voice.channel.edit(mute=False, deafen=True)

        with yt_dlp.YoutubeDL(YDL_OPTIONZ) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info["url"]
            title = info.get("title")
            
        await asyncio.sleep(2)
        message.Client.guild.voice_client.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))

        await asyncio.sleep(5)
        while message.Client.guild.voice_client.is_playing():

            await asyncio.sleep(1)

        await message.Client.author.voice.channel.edit(mute=True, deafen=True)

    if opt == "--file":
        output = download_video(url)
        await asyncio.sleep(3)
        await message.send_embed("Video Download", f"The request video has successfully downloaded! '{output}'!")
        await message.send_message(file = discord.File(output))


    
