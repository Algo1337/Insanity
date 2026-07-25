import discord, random

from utils import *

__err__ = discord.Embed(title = "Switch", description = "List of VC switch region commands")
__err__.add_field(name = "***Switch Current VC***", value = "```>switch --vc```", inline = False)
__err__.add_field(name = "***Switch a VC***", value = "```>switch <vc_id>```", inline = False)
__err__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__err__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__err__.set_footer(text = "http://insanity.host")

__SWITCH_INFO__ = {
    "Name": "Switch",
    "Description": "Switch VC",
    "ArgCount": 2,
    "Invalid_Arg_Err": __err__,
    "Get_Base": False
}

async def switch(base, message: DiscordUtils) -> bool:
    server = base.find_server_config(message.Client.guild.id)
    opt = message.Args[1].replace("<@", "").replace(">", "")

    if opt == "--vc":
        channel = message.Client.author.voice.channel
        region = base.AvailableRegions[random.randint(0, len(base.AvailableRegions) - 1)]
        if region == server.CurrentRegion or region == server.LastRegion:
            while region != server.CurrentRegion and region != server.LastRegion:
                region = base.AvailableRegions[random.randint(0, len(base.AvailableRegions) - 1)]

        await channel.edit(rtc_region = region)
        await message.send_embed("Switch Region VC", f"Successfully changed <#{channel.id}> region to ``{region}``", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
    elif opt.isdigit():
        channel_id = int(opt)
        channel = discord.utils.get(message.Client.guild.channels, id = channel_id)
        region = base.AvailableRegions[random.randint(0, len(base.AvailableRegions) - 1)]
        if region == server.CurrentRegion or region == server.LastRegion:
            while region != server.CurrentRegion and region != server.LastRegion:
                region = base.AvailableRegions[random.randint(0, len(base.AvailableRegions) - 1)]

        await channel.edit(rtc_region = region)
        await message.send_embed("Switch Region VC", f"Successfully changed <#{channel.id}> region to ``{region}``", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")


    return True