import discord, random

from src.discord_utils import *

__SWITCH_ARG_COUNT__ = 2
__SWITCH_INVALID_ARG_ERR__ = discord.Embed(title = "Switch", description = "List of VC switch region commands")
__SWITCH_INVALID_ARG_ERR__.add_field(name = "***Switch Current VC***", value = "```>switch --vc```", inline = False)
__SWITCH_INVALID_ARG_ERR__.add_field(name = "***Switch a VC***", value = "```>switch <vc_id>```", inline = False)
__SWITCH_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__SWITCH_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__SWITCH_INVALID_ARG_ERR__.set_footer(text = "http://insanity.host")

async def switch(base, message: DiscordUtils) -> bool:
    opt = message.Args[1].replace("<@", "").replace(">", "")

    if opt == "--vc":
        channel = message.Client.author.voice.channel
        region = base.AVAILABLE_REGIONS[random.randint(0, len(base.AVAILABLE_REGIONS) - 1)]
        if region == base.CurrentRegion or region == base.LastRegion:
            while region != base.CurrentRegion and region != base.LastRegion:
                region = base.AVAILABLE_REGIONS[random.randint(0, len(base.AVAILABLE_REGIONS) - 1)]

        await channel.edit(rtc_region = region)
        await message.send_embed("Switch Region VC", f"Successfully changed <#{channel.id}> region to ``{region}``", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
    elif opt.isdigit():
        channel_id = int(opt)
        channel = discord.utils.get(message.Client.guild.channels, id = channel_id)
        region = base.AVAILABLE_REGIONS[random.randint(0, len(base.AVAILABLE_REGIONS) - 1)]
        if region == base.CurrentRegion or region == base.LastRegion:
            while region != base.CurrentRegion and region != base.LastRegion:
                region = base.AVAILABLE_REGIONS[random.randint(0, len(base.AVAILABLE_REGIONS) - 1)]

        await channel.edit(rtc_region = region)
        await message.send_embed("Switch Region VC", f"Successfully changed <#{channel.id}> region to ``{region}``", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")


    return True