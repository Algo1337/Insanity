import discord

from src.config import *
from src.discord_utils import *

__WHITLIST_GET_BASE__ = True
__WHITLIST_ARG_COUNT__ = 3
__WHITLIST_INVALID_ARG_ERR__ = discord.Embed(title = "Whitlist | Error", description = "Invalid argument(s) provided!", color = discord.Colour.red())
__WHITLIST_INVALID_ARG_ERR__.add_field(name = "***Whitlist User***", value = "```>whitlist <--add/rm> <userid/@tag>```", inline = False)
__WHITLIST_INVALID_ARG_ERR__.set_image(url = "https://media.discordapp.net/attachments/1400104223508533309/1400134712839770193/test.png")
__WHITLIST_INVALID_ARG_ERR__.set_author(name = "Insanity")
__WHITLIST_INVALID_ARG_ERR__.set_footer(text = "https://insanity.host")

async def whitlist(base, message: DiscordUtils) -> bool:
    await message.Client.delete()
    
    opt = message.Args[1]
    if opt == "--view":
        whilisted_users = ""
        for user in base.Whitlist:
            whilisted_users += f"<@{user}>\n"

        await message.send_embed("Whitlisted Users", whilisted_users)
        return
    
    if len(message.Args) < 3:
        return
    
    user_id = message.Args[2].replace("<@", "").replace(">", "")
    if opt == "--add":
        base.Whitlist.append(user_id)
        await message.send_embed("Whitlist", f"User: <@{user_id}> has been successfully added!", image = "https://media.discordapp.net/attachments/1400104223508533309/1400134712839770193/test.png?ex=688b8890&is=688a3710&hm=6e8c70c936bfbb7a6cbd9fb727e14d7a95d8b64d9be770a2d76044fc558a0c5e&=&format=webp&quality=lossless")

        database(db_t.__ADMINS_PATH__, op_t.__add_id__, user_id)
        return True
    else:
        base.Whitlist.remove(user_id)
        
        database(db_t.__ADMINS_PATH__, op_t.__rm_id__, user_id)
        await message.send_embed("Whitlist", f"User: <@{user_id}> has been successfully removed!", image = "https://media.discordapp.net/attachments/1400104223508533309/1400134712839770193/test.png?ex=688b8890&is=688a3710&hm=6e8c70c936bfbb7a6cbd9fb727e14d7a95d8b64d9be770a2d76044fc558a0c5e&=&format=webp&quality=lossless")
    return True