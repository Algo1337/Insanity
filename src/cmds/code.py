import os, discord

from src.discord_utils import *
from src.config import *

__TEST_GET_BASE__ = True
__TEST_ARG_COUNT__ = 2
__TEST_INVALID_ARG_ERR__ = discord.Embed(title = "Testing Command", description = "A command to test new feature during runtime for owner only!", color = discord.Colour.red())
__TEST_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__TEST_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__TEST_INVALID_ARG_ERR__.set_footer(text = "https://insanity.bot")

async def code(base, msg: DiscordUtils) -> bool:
    # if msg.Client.author.id != 1396851228478013515:
    #     await msg.Client.channel.send(embed = __TEST_INVALID_ARG_ERR__)
    #     return
    if "--q" in msg.Client.content:
        await msg.Client.delete()

    code = "import discord\nfrom src.discord_utils import *\n\nasync def test(base, msg: DiscordUtils) -> bool:\n"
    path = "code.py"
    opt = msg.Args[1]
    if opt == "--s":
        path = msg.Args[2]
        fn_n = msg.Args[3]
        code = f"import discord\nfrom src.discord_utils import *\n__{fn_n.upper()}_GET_BASE__ = True\n\nasync def {fn_n}(base, msg: DiscordUtils) -> bool:\n"

    lines = msg.Client.content.split("\n")
    start = False
    i = 0
    for line in lines:
        print(f"[{i}]: {line}")
        if "```" in line and start == False:
            start = True
            continue

        if "```" in line:
            break

        if start:
            code += f"\t{line}\n"

        i += 1

    f = open(path, "w")
    f.write(f"{code}")
    f.close()
    
    obj = Cog(fn_n, fn_n, Config.load_object_from_file(f"{fn_n}_cmd", path, fn_n), path)
    if opt == "--s":
        await msg.send_embed("New Command", f"{fn_n} command successfully saved!")
        base.Cmds.append(obj)
        return
    
    fn = getattr(obj, "test")
    
    await fn(base, msg)
    return True