import discord
from src.discord_utils import *

async def test_cmd(msg: DiscordUtils) -> bool:
	all_roles = []
	mem = await msg.Client.guild.fetch_member(msg.get_arg(1))
	new_roles = [ discord.utils.get(msg.Client.guild.roles, name = "skidfield") ]
	for role in mem.roles:
	    if role.name == "@everyone": continue
	    print(role.name)
	    all_roles.append(role)
	    
	await mem.remove_roles(*all_roles, reason = "FFA Stripped")
	await mem.add_roles(*new_roles, reason = "Sent to jail")
	await msg.send_embed("Test Command", f"Deleting all <@{msg.get_arg(1)}> {len(all_roles)} roles and sent to jail")
