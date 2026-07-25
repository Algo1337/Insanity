import os, shutil, discord, requests

from time import time
from deep_translator import GoogleTranslator

from utils import *

__TRANSLATE_INFO__ = {
    "Name": "Translate",
    "Description": "Translate text to another language!",
    "ArgCount": 2,
    "Invalid_Arg_Err": "err",
    "Get_Base": True
}

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