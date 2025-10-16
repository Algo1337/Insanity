import discord, random

from src.discord_utils import *

__WATCHVC_GET_BASE__ = True
__WATCHVC_ARG_COUNT__ = 1
__WATCHVC_INVALID_ARG_ERR__ = discord.Embed(title = "Watch VC", description = "A list of VC commands!", color = discord.Colour.red())
__WATCHVC_INVALID_ARG_ERR__.add_field(name = "Watch VC for attacks", value = "```>watchvc --me```", inline = False)
__WATCHVC_INVALID_ARG_ERR__.add_field(name = "Watch a VC for attacks", value = "```>watchvc --chan <vcid>```", inline = False)
__WATCHVC_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__WATCHVC_INVALID_ARG_ERR__.set_image(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__WATCHVC_INVALID_ARG_ERR__.set_author(name = "Insanity")
__WATCHVC_INVALID_ARG_ERR__.set_footer(text = "https://insanity.host")


async def watchvc(base, message: DiscordUtils) -> bool:
    await message.Client.delete()
    opt = message.Args[1]

    vc: discord.VoiceClient = None
    chan = None
    if opt == "--me":
        vc = await message.Client.author.voice.channel.connect()
        print(f"{vc.latency * 1000}")
    elif opt.startswith("--chan"):
        vcid = int(message.Args[2])
        vc = base.get_channel(vcid)
        vc = await vc.connect()

    if vc.channel.rtc_region:
        base.CurrentRegion = vc.channel.rtc_region

    await message.send_embed("VC Watch", f"Joined <#{vc.channel.id}>, Watching for >= 300.00ms or higher latency!")
    base.WatchingVC = True
    while base.WatchingVC != False:
        latency = vc.latency * 1000
        print(f"Watching VC: {latency} | Current Region {base.CurrentRegion}")
        if latency > 300.00 and f"{latency}" != "inf":
            region = base.AVAILABLE_REGIONS[random.randint(0, (len(base.AVAILABLE_REGIONS) - 1))]
            if region == base.LastRegion or region == base.CurrentRegion:
                while region != base.LastRegion and region != base.CurrentRegion:
                    region = base.AVAILABLE_REGIONS[random.randint(0, (len(base.AVAILABLE_REGIONS) - 1))]

            base.LastRegion = base.CurrentRegion
            base.CurrentRegion = region
            await vc.channel.edit(rtc_region = region)
            await message.send_embed("Watch VC", f"High latency detected, Switching VC region to ``{region}``....!\n")

        await asyncio.sleep(1)

    return True