import discord

from utils import *

____ON_JOIN_INFO__ = {
    "Get_Base": True
}

async def __on_join__(base, message: DiscordUtils) -> bool:
    server = base.find_server_config(message.Client.guild.id)
    print(f"[ + ] New Server Member: {message.Client.name} | {message.Client.id}")

    if f"{message.Client.id}" in server.BlacklistedSkids:
        all_roles = []
        new_roles = [ discord.utils.get(message.Client.guild.roles, name = "skidfield") ]
        
        for role in message.Client.roles:
            if role.name == "@everyone": continue
            all_roles.append(role)

        await message.Client.remove_roles(*all_roles, reason = "FFA Stripped")
        await message.Client.add_roles(*new_roles, reason = "Sent to jail")

    """ Auto kick disabled """
    # if f"{message.Client.id}" in server.BlacklistedSkids:
    #     await message.Client.kick()

    return True