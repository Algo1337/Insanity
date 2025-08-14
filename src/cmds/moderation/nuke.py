import discord

from src.discord_utils import *

"""
    @Command: nuke

    Formats:
        ;nuke --channel                                     # Clone. Delete Current, Reposition New
        ;nuke --msg <msg_count>                             # Delete upto msg_count
        ;nuke --user <@tag> <?count(Default set to 100)>    # Delete user's messages up a count, 100 if not provided
"""

__NUKE_GET_BASE__ = True
__NUKE_ARG_COUNT__ = 2
__NUKE_INVALID_ARG_ERR__ = discord.Embed(title = "Nuke | Error", description = "Invalid arguments provided", color = discord.Colour.red())
__NUKE_INVALID_ARG_ERR__.add_field(name = "***Channel nuke***", value = "```>nuke --channel```", inline = False)
__NUKE_INVALID_ARG_ERR__.add_field(name = "***Message nuke***", value = "```>nuke --msg <count>```", inline = False)
__NUKE_INVALID_ARG_ERR__.add_field(name = "***Substring Included nuke***", value = "```>nuke --substring <string> <count>```", inline = False)
__NUKE_INVALID_ARG_ERR__.add_field(name = "***User nuke***", value = "```>nuke --user <@tag> <?count(Default: 100)>```", inline = False)
__NUKE_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__NUKE_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__NUKE_INVALID_ARG_ERR__.set_footer(text = "https://insanity.bot")

async def nuke(base, message: DiscordUtils) -> bool:
    await message.Client.delete()
    opt = message.Args[1]

    perms = message.Client.channel.permissions_for(message.Client.guild.me)
    if not perms.manage_channels and message.Client.author.id not in base.Whitlist:
        await message.send_embed("Nuke | Error", "You do not have the permissions to use this command!", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
    
    if opt == "--channel":
        old_channel = message.Client.channel
        old_category = old_channel.category
        old_position = old_channel.position

        cloned_channel = await old_channel.clone(reason = "Channel reset")
        await cloned_channel.edit(category = old_category, position = old_position, topic = f"{message.Client.guild.name} on TOP")

        await old_channel.delete(reason = "reset")
        embed = discord.Embed(title = f"Nuked", description = "Channel has been nuked", color = discord.Colour.red())
        embed.set_image(url = "https://media.discordapp.net/attachments/1399019763186798723/1403746906387120290/nukegif.gif?ex=6898acae&is=68975b2e&hm=16c7142c80ab0ca56fc24a938d2168106ffb106af5d43ff79cd736823c063d6c&=")
        embed.set_footer(text = "https://insanity.host")
        embed.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
        await cloned_channel.send(embed = embed)
    elif opt == "--msg":
        if message.Args[2].isdigit() == False:
           await message.Client.channel.send(embed = __NUKE_INVALID_ARG_ERR__)
           return False
         
        count = int(message.Args[2])
        if count < 1000:
            await message.Client.channel.purge(limit = count)
        else:
            async for msg in message.Client.channel.history(limit = count, oldest_first = False):
                await msg.delete()
                await asyncio.sleep(1/2)

        await message.send_embed("Nuke", f"Successfully nuked {count} messages!", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png", image = "https://images-ext-1.discordapp.net/external/N_WaNv_Tu5Cayp-_qfXPO5sb5yQf4Hy14k1_eqcYTVo/https/i.imgur.com/887rAyP.mp4")
    elif opt == "--substring":
        sub = " ".join(message.Args[2: len(message.Args) - 1])
        count = message.Args[len(message.Args) - 1]

        await message.Client.channel.send(sub)
        if count.isdigit() == False:
           await message.Client.channel.send(embed = __NUKE_INVALID_ARG_ERR__)
        
        count = int(count)
        del_count = 0
        async for msg in message.Client.channel.history(limit = count, oldest_first = False):
            if sub in msg.content:
                await msg.delete()
                del_count += 1
                await asyncio.sleep(1/2)

        await message.send_embed("Nuke", f"Successfully nuked {del_count} messages containing ``{sub}``!", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
    elif opt == "--user":
        user_id = message.Args[2].replace("<@", "").replace(">", "")
        count = message.Args[len(message.Args) - 1]
        if user_id.isdigit() == False or count.isdigit() == False:
           await message.Client.channel.send(embed = __NUKE_INVALID_ARG_ERR__)
        
        user_id = int(user_id)
        count = int(count)
        del_count = 0
        async for msg in message.Client.channel.history(limit = count, oldest_first = False):
            if msg.author.id == user_id:
                await msg.delete()
                del_count += 1
                await asyncio.sleep(1/2)

        await message.send_embed("Nuke", f"Successfully nuked {del_count} of <@{user_id}>'s messages!", author_name = "Insanity", author_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
        
    return True