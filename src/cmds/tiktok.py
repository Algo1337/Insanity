import os, shutil, discord, requests as req
from time import time

from src.discord_utils import *

__TIKTOK_GET_BASE__ = True
__TIKTOK_ARG_COUNT__ = 2
ICON = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png"

__TIKTOK_INVALID_ARG_ERR__ = discord.Embed(title = "TikTok", description = "A list of TikTok features", color = discord.Colour.red())
__TIKTOK_INVALID_ARG_ERR__.add_field(name = "**Download TikTok Video**", value = "```>tiktok <url>```", inline = False)
__TIKTOK_INVALID_ARG_ERR__.set_thumbnail(url = ICON)
__TIKTOK_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = ICON)
__TIKTOK_INVALID_ARG_ERR__.set_footer(text = "https://insanity.host")

async def tiktok(base, message: DiscordUtils) -> bool:
    url = message.Args[1]
    h = {"User-Agent": "Mozilla/5.0"}
    r = req.get(f"https://www.tikwm.com/api/?url={url}", headers=h).json()
    if "data" not in r:
        await message.send_embed("TikTok | Error", "bad url", author_name = "Insanity", author_url = ICON)
        return True

    d = r["data"]
    title = d.get("title", "vid")
    name = "".join(x for x in title if x.isalnum())[:50] or "vid"
    path = f"{name}.mp4"
    if os.path.exists(path): path = f"{name}_{int(time())}.mp4"

    with req.get(d["play"], stream=True, headers=h) as rx, open(path, "wb") as f:
        shutil.copyfileobj(rx.raw, f)

    print(f"[ + ] Saved {path}")

    fname = os.path.basename(path)
    max_bytes = message.Client.guild.filesize_limit
    size = os.path.getsize(path)
    if size > max_bytes:
        mb = size // 1024 // 1024
        limit_mb = max_bytes // 1024 // 1024
        print(f"[ x ] Error, file too large ({mb}MB > {limit_mb}MB)\n")
        await message.send_embed("TikTok | Error", f"File too large ({mb}MB > {limit_mb}MB)\n", {
            "**Link**": f"```{d['play']}```"
        }, author_name = "Insanity", author_url = ICON)
        try: os.remove(path)
        except: pass
        return True

    try:
        await message.Client.channel.send(file = discord.File(path, filename = fname))
    except:
        print("[ x ] Error, could not upload file to Discord!\n")
        await message.send_embed("TikTok | Error", "could not upload file to Discord!\n", {
            "**Link**": f"```{d['play']}```"
        }, author_name = "Insanity", author_url = ICON)

    try: os.remove(path)
    except: pass

    return True