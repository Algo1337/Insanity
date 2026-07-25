import discord, random

from utils import *

__err__ = discord.Embed(title = "Watch VC", description = "A list of VC commands!", color = discord.Colour.red())
__err__.add_field(name = "Watch VC for attacks", value = "```>watchvc --me```", inline = False)
__err__.add_field(name = "Watch a VC for attacks", value = "```>watchvc --chan <vcid>```", inline = False)
__err__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__err__.set_image(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__err__.set_author(name = "Insanity")
__err__.set_footer(text = "https://insanity.host")

__WATCH_INFO__ = {
    "Name": "Watch",
    "Description": "Watch for VC attacks",
    "Get_Base": True,
    "ArgCount": 1,
    "Invalid_Arg_Err": __err__
}

async def watch(base, message: DiscordUtils) -> bool:
    server = base.find_server_config(message.Client.guild.id)
    opt = message.Args[1]
    ms = float(message.Args[2])

    vc: discord.VoiceClient = None
    chan = None
    if opt == "--me":
        vc = await message.Client.author.voice.channel.connect()
        print(f"{vc.latency * 1000}")
    elif opt.startswith("--chan"):
        vcid = int(message.Args[2])
        ms = message.Args[3]
        vc = base.get_channel(vcid)
        vc = await vc.connect()

    if vc.channel.rtc_region:
        server.CurrentRegion = vc.channel.rtc_region

    await message.send_embed("VC Watch", f"Joined <#{vc.channel.id}>, Watching for >= {ms}ms or higher latency!")
    server.WatchingVC = True
    while server.WatchingVC != False:
        latency = vc.latency * 1000
        print(f"Watching VC: {latency} | Current Region {server.CurrentRegion}")
        if latency > ms and f"{latency}" != "inf":
            region = base.AvailableRegions[random.randint(0, (len(base.AvailableRegions) - 1))]
            if region == server.LastRegion or region == base.CurrentRegion:
                while region != server.LastRegion and region != server.CurrentRegion:
                    region = base.AvailableRegions[random.randint(0, (len(base.AvailableRegions) - 1))]

            server.LastRegion = server.CurrentRegion
            server.CurrentRegion = region
            await vc.channel.edit(rtc_region = region)
            await message.send_embed("Watch VC", f"High latency detected, Switching VC region to ``{region}``....!\n")

        await asyncio.sleep(1)

    return True