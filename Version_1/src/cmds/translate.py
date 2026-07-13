import os, shutil, discord, requests
from time import time
from deep_translator import GoogleTranslator

from src.discord_utils import *

__TRANSLATE_GET_BASE__ = True
__TRANSLATE_ARG_COUNT__ = 2
__TRANSLATE_INVALID_ARG_ERR__ = "err"

async def translate(base, msg: DiscordUtils):
    target = ""
    for element in msg.Args:
        if element.startswith("--"):
            target = element
            break

        
    msg.Args.remove(target)
    query = " ".join(msg.Args)
    text = GoogleTranslator(source="auto", target=target.replace("--", "")).translate(
        query.replace(f"{msg.Args[0]} ", "")
    )

    await msg.send_message(text)