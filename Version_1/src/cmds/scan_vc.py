import discord, pytz, ipaddress, random

from src.discord_utils import *

__SCAN_VC_GET_BASE__ = True
__SCAN_VC_ARG_COUNT__ = 0
__SCAN_VC_INVALID_ARG_ERR__ = discord.Embed(title = "Info", description = "A list of info commands", color = discord.Colour.red())
__SCAN_VC_INVALID_ARG_ERR__.add_field(name = "**My Server**", value = ">info --server", inline = False)
__SCAN_VC_INVALID_ARG_ERR__.add_field(name = "**My Info**", value = ">info --me", inline = False)
__SCAN_VC_INVALID_ARG_ERR__.add_field(name = "**User Info**", value = ">info --user <@tag/user_id>", inline = False)
__SCAN_VC_INVALID_ARG_ERR__.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__SCAN_VC_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png")
__SCAN_VC_INVALID_ARG_ERR__.set_footer(text = "https://insanity.bot")

def _append_to_logs(msg: str) -> bool:
    if not msg or msg == "":
        return False
    
    try:
        fd = open("assets/messages.log", "a+")
        fd.write(f"{msg}\n")
        fd.close()
        return True
    except:
        return False
    
def scan_voice_channels(guild):
    results = []

    for channel in guild.voice_channels:
        if channel.members:
            results.append({
                "id": channel.id,
                "name": channel.name,
                "members": [
                    {
                        "id": member.id,
                        "name": member.display_name,
                        "username": member.name,
                        "screen_share": member.voice.self_stream,
                        "mute": member.voice.mute,
                        "deafen": member.voice.deaf,
                        "smute": member.voice.self_mute,
                        "sdeafen": member.voice.self_deaf
                    }
                    for member in channel.members
                ]
            })

    return results

async def scan_vc(base, message: DiscordUtils) -> bool:
    guild = base.get_guild(int(message.Args[1]))

    vcs = scan_voice_channels(guild)

    for vc in vcs:
        headers = [
            "Member", "Username", "ID", "Stream",
            "Admin Mute", "Admin Deafen",
            "User Mute", "User Deafen"
        ]

        widths = [
            24, 20, 19, 6, 11, 13, 10, 12
        ]

        width = sum(widths) + len(widths) * 3 + 1

        colors = [
            # "\x1b[30m",
            "\x1b[31m",
            "\x1b[32m",
            "\x1b[33m",
            "\x1b[34m",
            "\x1b[35m",
            "\x1b[36m",
            "\x1b[37m",
        ]
        last = ""

        def row(values, color=None):
            if color is None:
                color = random.choice(colors)

            return "│ " + " │ ".join(
                f"{color}{str(value):<{w}}\x1b[0m"
                for value, w in zip(values, widths)
            ) + " │"

        top = "╭" + "┬".join("─" * (w + 2) for w in widths) + "╮"
        mid = "├" + "┼".join("─" * (w + 2) for w in widths) + "┤"
        bottom = "╰" + "┴".join("─" * (w + 2) for w in widths) + "╯"

        print(f"\n{top}")
        print(row(headers))
        print(mid)

        for i, member in enumerate(vc["members"]):
            values = [
                member["name"],
                member["username"],
                member["id"],
                "YES" if member["screen_share"] else "NO",
                "YES" if member["mute"] else "NO",
                "YES" if member["deafen"] else "NO",
                "YES" if member["smute"] else "NO",
                "YES" if member["sdeafen"] else "NO",
            ]

            color = random.choice(colors)

            if color == last:
                while color == last:
                    color = random.choice(colors)

            last = color

            print(row(values, color))

            if i != len(vc["members"]) - 1:
                print(mid)

        print(bottom)