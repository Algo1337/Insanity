import discord

from src.discord_utils import *

____ON_JOIN___GET_BASE__ = True

async def __on_join__(base, message: DiscordUtils) -> bool:
    
    if not message.Client:
        print("NONE")

    print(f"[ + ] Join {message.Client.name} {message.Client.id}")
    print(base.BlacklistedSkids)

    if f"{message.Client.id}" in base.BlacklistedSkids:
        print("HERE")
        await asyncio.sleep(3)
        all_roles = []
        new_roles = [ discord.utils.get(message.Client.guild.roles, name = "skidfield") ]
        
        for role in message.Client.roles:
            if role.name == "@everyone": continue
            all_roles.append(role)

        await message.Client.remove_roles(*all_roles, reason = "FFA Stripped")
        await message.Client.add_roles(*new_roles, reason = "Sent to jail")

    if f"{message.Client.id}" in base.Blacklistjoin:
        await message.Client.kick()

    return True