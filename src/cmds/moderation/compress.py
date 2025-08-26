import os, discord, random, cv2, imageio

from src.discord_utils import *
from src.compressor import *

__COMPRESS_ARG_COUNT__ = 2
__COMPRESS_INVALID_ARG_ERR__ = discord.Embed(title = "Image/Gif Compressor", description = "Private NIGGA, FUCK OFF", color = discord.Colour.red())
__COMPRESS_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png?format=webp&quality=lossless")
__COMPRESS_INVALID_ARG_ERR__.set_footer(text = "https://insanity.host")

async def compress(base, message: DiscordUtils) -> bool:
    url = message.Args[1]
    opt = ".png"

    if "--gif" in message.Args: 
        opt = ".gif"
    
    r = random.randint(0, 99999999)
    filename = f"images/{r}{opt}"
    print(f"Downloading {url} -> {filename} -> images/{r}_compressed{opt}")
    DiscordUtils.download_image(url, filename)

    if url.endswith(".mp4"):
        cap = cv2.VideoCapture(filename)
        frames = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)

        cap.release()
        os.remove(filename)

        imageio.mimsave(filename, frames, fps=10)

    await asyncio.sleep(2)
    Compressor.compress_gif(filename, f"images/{r}_compressed{opt}")
    await asyncio.sleep(2)

    embed = discord.Embed(title = "Img/Gif Compressor", description = "The file has been compressed to 512KB, Ready for discord sticker/emoji", color = discord.Colour.red())
    embed.set_image(url = f"attachment://images/{r}_compressed{opt}")
    await message.Client.channel.send(file = discord.File(f"images/{r}_compressed{opt}", filename = f"images/{r}_compressed{opt}"), embed = embed)

    os.remove(filename)

    if "--save" not in message.Args:
        os.remove(f"images/{r}_compressed{opt}")

    return True