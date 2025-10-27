import discord, random

from src.discord_utils import *

__STEAL_GET_BASE__ = True
__STEAL_ARG_COUNT__ = 2
__STEAL_INVALID_ARG_ERR__ = discord.Embed(title = "Steal", description = "", color = discord.Colour.red())
__STEAL_INVALID_ARG_ERR__.add_field(name = "**Steal Emoji Image [REPLY]**", value = "```>steal --emoji --png```", inline = False)
__STEAL_INVALID_ARG_ERR__.add_field(name = "**Steal Emoji Gif [REPLY]**", value = "```>steal --emoji --gif```", inline = False)
__STEAL_INVALID_ARG_ERR__.add_field(name = "**Steal Sticker Image [REPLY]**", value = "```>steal --sticker --png```", inline = False)
__STEAL_INVALID_ARG_ERR__.add_field(name = "**Steal Sticker Gif [REPLY]**", value = "```>steal --sticker --gif```", inline = False)
__STEAL_INVALID_ARG_ERR__.add_field(name = "**Steal Emoji Image**", value = "```>steal --emoji --png <url>```", inline = False)
__STEAL_INVALID_ARG_ERR__.add_field(name = "**Steal Emoji Gif**", value = "```>steal --emoji --gif <url>```", inline = False)
__STEAL_INVALID_ARG_ERR__.add_field(name = "**Steal Sticker Image**", value = "```>steal --sticker --png <url>```", inline = False)
__STEAL_INVALID_ARG_ERR__.add_field(name = "**Steal Sticker Gif**", value = "```>steal --sticker --gif <url>```", inline = False)
__STEAL_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png?format=webp&quality=lossless")
__STEAL_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png?format=webp&quality=lossless")


def do_steal(url: str, output: str) -> bool:
    DiscordUtils.download_image(url, output)


async def steal(base, message: DiscordUtils) -> bool:
    opt = message.Args[1]
    img_t = message.Args[2].replace("--", ".")

    original = None
    if message.Client.reference:
        original = await message.Client.channel.fetch_message(message.Client.reference.message_id)

        if opt == "--emoji":
            emojis = message.get_emojis()
            if len(emojis) == 0:
                await message.send_embed("Steal | Error", "No emojis in message detected....!\n")
                return
            
            r = random.randint(0, 99999999)
            filename = f"images/{r}{img_t}"
            for emoji in emojis:
                do_steal(f"https://cdn.discordapp.com/emojis/{emoji}{img_t}", filename)
            
            await message.send_embed("Steal", f"Emojis Successfully Downloaded: ```{', '.join(emojis)}```")
            return
        elif opt == "--sticker":
            stkr = None
            for sticker in original.stickers:
                print(f"{sticker.name} => {sticker.url}")

                r = random.randint(0, 99999999)
                filename = f"images/{r}{img_t}"

                stkr = sticker
                DiscordUtils.download_image(sticker.url, filename)
            
            await message.send_embed("Steal", f"Sticker Successfully Downloaded {stkr.name}")
            return

    emojis = message.get_emojis()
    if len(emojis) == 0:
        await message.send_embed("Steal | Error", "No emojis in message detected....!\n")
        return
    
    r = random.randint(0, 99999999)
    filename = f"images/{r}{img_t}"
    for emoji in emojis:
        do_steal(f"https://cdn.discordapp.com/emojis/{emoji}{img_t}", filename)

    return True