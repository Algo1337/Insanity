import sys, shutil, discord
from time import time
from pathlib import Path
import requests as req
from src.discord_utils import *

__TIKTOK_GET_BASE__ = True
__TIKTOK_ARG_COUNT__ = 2
__TIKTOK_INVALID_ARG_ERR__ = discord.Embed(title="TikTok", description=">tiktok <url>", color=discord.Colour.red())

async def tiktok(b, m: DiscordUtils) -> bool:
    url = m.Args[1]
    h = {"User-Agent": "Mozilla/5.0"}
    r = req.get(f"https://www.tikwm.com/api/?url={url}", headers=h).json()
    if "data" not in r: return await m.send_message("bad url")
    d = r["data"]
    name = "".join(x for x in d.get("title", "vid") if x.isalnum())[:50] or "vid"
    path = Path(f"{name}.mp4")
    
    if path.exists(): path = Path(f"{name}_{int(time())}.mp4")
    
    with req.get(d["play"], stream=True, headers=h) as rx, open(path, "wb") as f:
        shutil.copyfileobj(rx.raw, f)

    await m.Client.channel.send(content=d.get("title", "vid"), file=discord.File(path))
    try: path.unlink()
    except: pass

    return True