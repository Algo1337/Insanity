import discord

from utils import *

__err__ = discord.Embed(title = "Whitlist | Error", description = "Invalid argument(s) provided!", color = discord.Colour.red())
__err__.add_field(name = "***Whitlist User***", value = "```>whitlist <--add/rm> <userid/@tag>```", inline = False)
__err__.set_image(url = "https://media.discordapp.net/attachments/1400104223508533309/1400134712839770193/test.png")
__err__.set_author(name = "Insanity")
__err__.set_footer(text = "https://insanity.host")

__WHITLIST_INFO__ = {
    "Name": "Whitlist",
    "Description": "Whitlist a user",
    "ArgCount": 3,
    "Invalid_Arg_Err": __err__,
    "Get_Base": True
}

async def whitlist(base, message: DiscordUtils) -> bool:
    server = base.find_server_config(message.Client.guild.id)  
    opt = message.Args[1]
    if opt == "--view":
        whilisted_users = ""
        for user in server.Whitlisted:
            whilisted_users += f"<@{user}>\n"

        await message.send_embed("Whitlisted Users", whilisted_users)
        return
    
    if len(message.Args) < 3:
        return
    
    user_id = message.Args[2].replace("<@", "").replace(">", "")
    if opt == "--add":
        server.Whitlisted.append(user_id)
        await message.send_embed("Whitlist", f"User: <@{user_id}> has been successfully added!")

        # database(db_t.__ADMINS_PATH__, op_t.__add_id__, user_id)
        return True
    else:
        server.Whitlisted.remove(user_id)
        
        # database(db_t.__ADMINS_PATH__, op_t.__rm_id__, user_id)
        await message.send_embed("Whitlist", f"User: <@{user_id}> has been successfully removed!")
    return True