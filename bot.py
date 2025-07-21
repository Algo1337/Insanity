import discord, requests, time, pytz, asyncio, random, os, math, pyttsx3, yt_dlp, imageio

from PIL import Image
from discord import ChannelType, FFmpegPCMAudio
from datetime import timezone
from translatepy import Translator
from gtts import gTTS
from PIL import Image
import imageio
import numpy as np
from rembg import remove

CURRENT_VC = None
WATCHING_VC = False
PLAYING = False
THRESHOLD = 300
CURRENT_REGION = None
LAST_REGION_USED = None
AVAILABLE_REGIONS = [
    'us-west', 
    'us-east', 
    'us-central', 
    'us-south'
    # 'singapore', 
    # 'japan', 
    # 'hongkong', 
    # 'brazil',
    # 'sydney', 
    # 'southafrica', 
    # 'india', 
    # 'rotterdam'
]

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

YDL_OPTIONS = {'format': 'bestaudio'}

GEMINI_HEADERS = {
    "x-goog-api-key": "AIzaSyAaRnav3DNdEhWlNcc4CO1dpcaZ6OzYChs",
    "Content-Type": "application/json"
}

MAX_SIZE = 512 * 1024  # 512KB
RESIZE_STEP = 0.9
GIF_FPS = 15

BLACKLISTED_TOKENS = []

class Compressor():
    def compress_image(name: str):
        path = name
        ext = os.path.splitext(path)[1].lower()

        try:
            if ext == ".png":
                out = Compressor.compress_png(path)
            elif ext == ".gif":
                out = Compressor.compress_gif(path)
            else:
                print("Unsupported file type. Use PNG or GIF.")
                return
        except:
            return

        print(f"Successfully compressed!")

    def compress_png(input_path):
        global MAX_SIZE
        global RESIZE_STEP
        global GIF_FPS
        img = Image.open(input_path)
        quality = 90
        scale = 1.0

        while True:
            temp_path = "test.png"
            resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
            resized.save(temp_path, optimize=True)

            if os.path.getsize(temp_path) <= MAX_SIZE or scale < 0.1:
                print(f"[✓] PNG compressed to {os.path.getsize(temp_path) / 1024:.1f} KB")
                return temp_path

            scale *= RESIZE_STEP  # reduce size

    def compress_gif(input_path):
        global MAX_SIZE
        global RESIZE_STEP
        global GIF_FPS

        scale = 1.0

        while True:
            frames = []

            try:
                reader = imageio.get_reader(input_path)
                for frame in reader:
                    image = Image.fromarray(frame)
                    image = image.resize((int(image.width * scale), int(image.height * scale)), Image.LANCZOS)
                    frames.append(image)
            except Exception as e:
                print(f"[!] Failed to read GIF: {e}")
                return None

            if not frames:
                print("[!] No frames found in GIF.")
                return None

            temp_path = "test.gif"
            frames[0].save(
                temp_path,
                save_all=True,
                append_images=frames[1:],
                loop=0,
                optimize=True,
                duration=int(1000 / GIF_FPS),
                disposal=2
            )

            if os.path.getsize(temp_path) <= MAX_SIZE or scale < 0.1:
                print(f"[✓] GIF compressed to {os.path.getsize(temp_path) / 1024:.1f} KB")
                return temp_path

            scale *= RESIZE_STEP

class Temp:
    gif_path: str       = "NCA-Bot/test.gif"
    output_path: str    = 'output.gif'
    def get_token() -> str:
        f = open("token.cfg", "r")
        t = f.read()
        f.close()

        return t

    def get_flag_value(args: list, flag: str) -> str:
        count = 0
        for arg in args:
            if arg == flag:
                return args[count + 1]
            
            count += 1

        return ""
    
    def get_emojis(args: list) -> list:
        emojis = []

        for arg in args:
            if arg.startswith("<") and arg.endswith(">"):
                emoji_args = arg.split(":")

                ## <:emoji_name:emoji_id>
                if len(emoji_args) == 3:
                    emojis.append(emoji_args[2][:-1])
                    continue
                elif len(emoji_args) == 2:
                    emojis.append(emoji_args[1][:-1])
                    continue

        return emojis

    def download_image(url: str, output: str) -> int:
        try:
            req = requests.get(url)
            if req.status_code != 200: 
                print("[ - ] Error, Failed to make the request....!\n")
            f = open(output, "wb")
            f.write(req.content)
            f.close()
        except:
            return 0
        
        return 1

    def remove_bg_from_gif() -> None:
        reader = imageio.get_reader(self.gif_path)
        frames = []

        for i, frame in enumerate(reader):
            # Convert frame to PIL image
            pil_img = Image.fromarray(frame)

            # Remove background
            img_bytes = pil_img.convert("RGBA").tobytes()
            input_pil = pil_img.convert("RGBA")
            output_pil = remove(input_pil)

            # Append processed frame
            frames.append(output_pil)

        # Save output as new GIF
        frames[0].save(self.output_path,
                    save_all=True,
                    append_images=frames[1:],
                    duration=reader.get_meta_data()['duration'],
                    loop=0,
                    disposal=2)


class Algo(discord.Client):
    async def on_ready(self):

        print(f"[ + ] Fired up {self.user}")

    async def on_message(self, message):
        global CURRENT_VC
        global WATCHING_VC
        global THRESHOLD
        global CURRENT_REGION
        global LAST_REGION_USED
        global AVAILABLE_REGIONS
        global GEMINI_HEADERS

        local_tz = pytz.timezone('America/Kentucky/Louisville')
        print(f"[ + ] Message: \x1b[31m{message.guild.name}/{message.channel.name}\x1b[0m | \x1b[32m{message.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')}\x1b[0m \x1b[33m{message.author.display_name}:{message.author.name}\x1b[0m: {message.content}")

        """
            Ignore bots
        """
        if message.author.bot:
            return
        
        """
            Restricting to 3 users
        """
        if message.content.startswith(";") and (message.author.id != 1235776145819959318 and message.author.id != 1163512624483405976 and message.author.id != 1325956676192309350 and message.author.id != 1356119677406810184):
            await message.channel.send("Error, Only the creators can use this bot!")
            return
        
        """
                [TESTING]: Custom Command
            @command: -help
        """
        if message.content == ";help":
            await message.delete()
            await message.channel.send("> - List of commands | Keep in mind: ``?`` stands for optional argument\n```\n;help\n;clean <?count> <?@user> (delete this bot's messages only)\n;join\n;watchvc <vc_id>\n;switch\n;leavevc\n;vcsay <text> (vcsayq for quiet operation)\n;sayvc <text> (sayvcq for quiet operation)\n;yt <url>\n;stop\n;nuke\n;translate <lang> (Must reply to the message that you want translated)\n;factcheck <?question> (Must reply to the message factchecking)\n;compress <image_url> <png/gif>```")
            return

        if message.content.startswith(";say"):
            await message.delete()
            if " " not in message.content:
                await message.channel.send("Error, Must provide what you want said!\n;say <?channel> <text>")

            args = message.content.split(" ")
            channel = message.channel
            text = " ".join(args[1:])
            if len(args) > 1:
                if args[1].startswith("<#") and args[1].endswith(">"):
                    channel = self.get_channel(int(args[1].replace("<#", "").replace(">", "")))
                    text = " ".join(args[2:])

            await channel.send(text)

        """
                [TESTING]: Custom Command
            @command: -clean
        """
        if message.content.startswith(";clean"):
            await message.delete()

            args = message.content.split(" ")
            user_id = self.user.id
            msg_count = 100

            """
                ;clean 
                ;clean <?count>
                ;clean <?count> <@user>
            """
            if len(args)> 0:
                if args[1].isdigit():
                    msg_count = int(args[1])

            if len(args) > 2:
                user_id = int(args[2].replace("<", "").replace("@", "").replace(">", ""))

            async for msg in message.channel.history(limit=msg_count, oldest_first=False):
                if msg.author.id == user_id:
                    await msg.delete()
                    time.sleep(1)

        """
                [TESTING]: Custom Command
            @command: -servers
        """
        if message.content == ";servers":
            servers = ""
            for guild in self.guilds:
                servers += f"{guild.name}\n"

            await message.channel.send(f"> - List of servers\n\n```{servers}```")


        """
                [TESTING]: Custom Command
            @command: -join
        """
        if message.content == ";join":
            await message.delete()
            vc = await message.author.voice.channel.connect()
            await vc.guild.me.edit(mute=True, deafen=True)

        """
                [TESTING]: Custom Command
            @command: -watchvc
        """
        if message.content.startswith(";watchvc"):
            await message.delete()

            if WATCHING_VC == True:
                await message.channel.send("VC watch is already running, you must stop it first using ``;stopwatch``!")
                return

            """ Disconnect if alreay in a VC """
            existing_vc = discord.utils.get(self.voice_clients, guild=message.guild)
            print("Voice clients:", self.voice_clients)
            print("existing_vc:", existing_vc)
            if existing_vc and existing_vc.is_connected():
                await existing_vc.disconnect(force=True)
                asyncio.sleep(3)

            parts = message.content.split()
            if len(parts) < 2:
                await message.channel.send("Usage: `=join <voice_channel_id>`")
                return

            channel_id = int(parts[1])
            voice_channel = self.get_channel(channel_id)

            if not isinstance(voice_channel, discord.VoiceChannel):
                await message.channel.send("Channel ID is not a voice channel or doesn't exist.")
                return

            vc = await voice_channel.connect()
            await vc.guild.me.edit(mute=True, deafen=True)
            await message.channel.send(f"Joined voice channel: {voice_channel.name}\n✅ Started watching `{vc.channel.name}` with threshold {THRESHOLD} ms.")

            WATCHING_VC = True
            while WATCHING_VC != False:
                await asyncio.sleep(1)

                if not vc or not vc.is_connected():
                    break

                latency_ms = vc.latency * 1000
                print(f"\x1b[31m[WATCHING_VC]\x1b[39m Current region: {vc.endpoint.split('.')[0] if vc.endpoint else 'unknown'} | Threshold: {THRESHOLD}ms | Latency: {latency_ms}ms | Waiting for attacks")

                if latency_ms > float(THRESHOLD) and not math.isinf(latency_ms):
                    await message.channel.send("[ - ] Voice channel server has started lagging! Fixing...")
                    new_region = AVAILABLE_REGIONS[random.randint(0, len(AVAILABLE_REGIONS) - 1)]
                    if new_region == CURRENT_REGION or new_region == LAST_REGION_USED:
                        while new_region != CURRENT_REGION and new_region != LAST_REGION_USED:
                            new_region = AVAILABLE_REGIONS[random.randint(0, len(AVAILABLE_REGIONS) - 1)]
                        
                        await voice_channel.edit(rtc_region=new_region)
                        await asyncio.sleep(5)
                        await message.channel.send(f"Fixed....!")
                    else:
                        await voice_channel.edit(rtc_region=new_region)
                        await asyncio.sleep(5)
                        await message.channel.send(f"Fixed....!")

        """
                [TESTING]: Custom Command
            @command: -switch
        """
        if message.content == ";switch":
            await message.delete()

            if not message.author.voice:
                await message.channel.send("Error, Must be in a VC already!")
                return
            
            new_region = AVAILABLE_REGIONS[random.randint(0, len(AVAILABLE_REGIONS) - 1)]
            if new_region == CURRENT_REGION or new_region == LAST_REGION_USED:
                new_region = AVAILABLE_REGIONS[random.randint(0, len(AVAILABLE_REGIONS) - 1)]
                
            vc = message.author.voice.channel
            await vc.edit(rtc_region=new_region)
            await asyncio.sleep(5)
            await message.channel.send(f"Switched ``{vc.name}`` region to {new_region}")

        """
                [TESTING]: Custom Command
            @command: -leave
        """
        if message.content == ";leavevc":
            await message.delete()

            for vc in self.voice_clients:
                if vc.guild == message.guild:
                    await vc.disconnect()
                    await message.channel.send("Disconnected from the voice channel.")
                    break
            else:
                await message.channel.send("I'm not in a voice channel.")
            return
        
        if message.content == ";stopwatch":
            if WATCHING_VC == False:
                await message.channel.send("Error, VC watch is not running!")
                return 
            
            WATCHING_VC = False
            await message.channel.send("VC watch successfully stopped....!")
        
        """
                [TESTING]: Custom Command
            @command: -vcsay
        """
        if message.content.startswith(";vcsay"):
            await message.delete()

            """ Check for arguments """
            if " " not in message.content:
                return
            
            """ Check if user is in a VC to join """
            if not message.author.voice:
                await message.channel.send("Error, Must be in VC!")
                return

            """ Check if the bot is not in the same VC with user and not in another one """
            if message.guild.voice_client == None:
                await message.author.voice.channel.connect()
            elif message.guild.voice_client != message.author.voice:
                await message.guild.voice_client.move_to(message.author.voice.channel)
            
            args = message.content.split(" ")
            volume = 5
            text = " ".join(args[1:])
            if args[1].isdigit():
                volume = int(args[1])
                text = " ".join(args[2:])
            else:
                text = " ".join(args[1:])
                
            tts = gTTS(text, lang='en', tld='co.uk')
            tts.save("test.mp3")

            vc = message.author.voice.channel
            await vc.guild.me.edit(mute=False, deafen=True)
            audio_source = FFmpegPCMAudio("test.mp3", options= f'-filter:a "volume={volume}"')
            message.guild.voice_client.play(audio_source)
            while message.guild.voice_client.is_playing():
                await asyncio.sleep(1)

            os.remove("test.mp3")
            await vc.guild.me.edit(mute=True, deafen=True)
            if message.content.startswith(";vcsayq"):
                return
            
            await message.channel.send(f"[ + ] TTS \"{text}\" Done")

        """
                [TESTING]: Custom Command
            @command: -sayvc
        """
        if message.content.startswith(";vcs"):
            await message.delete()

            """ Check for arguments """
            if " " not in message.content:
                return
            
            """ Check if user is in a VC to join """
            if not message.author.voice:
                await message.channel.send("Error, Must be in VC!")
                return

            """ Check if the bot is not in the same VC with user and not in another one """
            if message.guild.voice_client == None:
                await message.author.voice.channel.connect()
            elif message.guild.voice_client != message.author.voice:
                await message.guild.voice_client.move_to(message.author.voice.channel)

            vc = message.author.voice.channel
            gender = 0 ## Male
            if "--female" in message.content:
                gender = 1

            volume = 5
            args = message.content.split(" ")
            text = " ".join(args[1:]).replace("--female", "")
            if args[1].isdigit():
                volume = int(args[1])
                text = " ".join(args[2:]).replace("--female", "")
            else:
                text = " ".join(args[1:]).replace("--female", "")

            engine = pyttsx3.init()
            engine.setProperty('rate', 125)
            engine.setProperty('volume', 1.0)

            voices = engine.getProperty('voices')
            # for voice in voices:
            #     if voice.id == "roa/es-419":
            #         engine.setProperty('voice', voice.id)
            #     print(f"{voice.id} | {voice.name} | {voice.languages} | {voice.gender} | {voice.age}")

            engine.setProperty('voice', voices[gender].id)
            engine.save_to_file(text, 'test.mp3')
            engine.runAndWait()
            
            await vc.guild.me.edit(mute=False, deafen=True)
            await asyncio.sleep(5)
            audio_source = FFmpegPCMAudio("test.mp3", options=f'-filter:a "volume={volume}"')
            message.guild.voice_client.play(audio_source, after=lambda e: print("Done"))
            while message.guild.voice_client.is_playing():
                await asyncio.sleep(1)

            os.remove("test.mp3")
            await vc.guild.me.edit(mute=True, deafen=True)
            if message.content.startswith(";sayvcq"):
                return
            
            await message.channel.send(f"[ + ] TTS \"{text}\" Done")

        if message.content == ";voices":
            engine = pyttsx3.init()
            engine.setProperty('rate', 125)
            engine.setProperty('volume', 1.0)
            voices = ""
            choices = engine.getProperty('voices')
            for voice in choices:
                voices += f"> - {voice.id} | {voice.name} | {voice.languages} | {voice.gender}\n"

            await message.channel.send(f"**List of voices**\n{voices[:1950]}")

        """
                [TESTING]: Custom Command
            @command: -yt
        """
        if message.content.startswith(";yt"):
            await message.delete()

            if " " not in message.content:
                return
            
            await message.author.voice.channel.edit(mute=False, deafen=True)
            await asyncio.sleep(5)

            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(message.content.split(" ")[1], download=False)
                audio_url = info["url"]
                title = info.get("title")
            
            message.guild.voice_client.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))
            while message.guild.voice_client.is_playing():

                await asyncio.sleep(1)

            await message.author.voice.channel.edit(mute=True, deafen=True)

        """
                [TESTING]: Custom Command
            @command: -stop
        """
        if message.content == ";stop":
            await message.delete()

            if not message.guild.voice_client.is_playing():
                await message.channel.send("Error, Nothing is playing to stop!")
                return
            
            message.guild.voice_client.stop()

        """
                [TESTING]: Custom Command
            @command: -nuke
        """
        if message.content == ";nuke":
            if not message.guild:
                return

            bot_member = message.guild.me
            perms = message.channel.permissions_for(bot_member)

            if not perms.manage_channels:
                await message.channel.send("❌ I need `Manage Channels` permission to do this.")
                return

            old_channel = message.channel
            old_category = old_channel.category
            old_position = old_channel.position

            cloned_channel = await old_channel.clone(reason="Nuked Channel, Remade")
            await cloned_channel.edit(category=old_category, position=old_position, topic="NCA ON TOP!")

            await cloned_channel.send(f"✅ {message.author.mention} nuked")
            await old_channel.delete(reason="Nuked")

        if message.content.startswith(";topic"):
            if " " not in message.content:
                return

            text = " ".join(message.content.split(" ")[1:])
            await message.channel.edit(topic = text)
            await message.channel.send("Topic Set")

        if message.content.startswith(";vctopic"):
            if " " not in message.content:
                return

            text = " ".join(message.content.split(" ")[1:])
            await message.author.voice.channel.edit(topic = text)
            await message.channel.send("Topic Set")


        """
                [TESTING]: Custom Command
            @command: -p
        """
        if message.content == ";p":
            pass

        """
                [TESTING]: Custom Command
            @command: -translate
        """
        if message.content.startswith(";translate"):
            if " " not in message.content:
                return
            
            args = message.content.split(" ")
            lang = "en"
            if len(args) > 1:
                lang = args[1]

            replied_msg = None
            if not message.reference:
                return
            
            replied_msg = await message.channel.fetch_message(message.reference.message_id)

            translator = Translator()
            translation = translator.translate(replied_msg.content, lang)
            await message.channel.send(translation)

        """
                [TESTING]: Custom Command
            @command: -factcheck
        """
        if message.content.startswith(";factcheck"):
            if not message.reference:
                return 
            
            replied_msg = await message.channel.fetch_message(message.reference.message_id)
            q = "Fact-check this\n"
            if " " in message.content:
                q = " ".join(message.content.split(' ')[1:]) + "\n"

            q += f"{replied_msg.content}\n"
            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": q}
                        ]
                    }
                ]
            }

            response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent", headers=GEMINI_HEADERS, json=data)
            if response.ok:
                content = response.json()
                text_output = content["candidates"][0]["content"]["parts"][0]["text"]
                if len(text_output) > 1996:
                    await message.reply(text_output[:1996] + "...")
                    return
                await message.reply(text_output)
            else:
                print("Error:", response.status_code, response.text)

        """
                [TESTING]: Custom Command
            @command: -ai
        """
        if message.content.startswith(";ai"):
            if " " not in message.content:
                return
            
            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": " ".join(message.content.split(" ")[1:])}
                        ]
                    }
                ]
            }

            response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent", headers=GEMINI_HEADERS, json=data)
            if response.ok:
                content = response.json()
                text_output = content["candidates"][0]["content"]["parts"][0]["text"]
                resp_len = len(text_output)
                for i in range(0, resp_len):
                    if i + 1996 > resp_len:
                        await message.channel.send(text_output[i : resp_len])
                        break

                    await message.channel.send(text_output[i : i + 1996])
                    i += 1996

                await message.reply(text_output)
            else:
                print("Error:", response.status_code, response.text)

        """
                [TESTING]: Custom Command
            @command: -steal
        """
        if message.content.startswith(";steal"):
            await message.delete()

            args = message.content.split(" ")
            if message.reference:
                replied_msg = await message.channel.fetch_message(message.reference.message_id)

            name = ""
            file_t = ""
            if len(args) > 2 and "--gif" in args:
                file_t = ".gif"
            else:
                file_t = ".png"
            
            """
                Possible formats:
                    ;steal --sticker
                    ;steal --sticker --gif
                    ;steal --emoji
                    ;steal --emoji --gif
                    ;steal --image
                    ;steal --image --gif
                    ;steal --avatar
                    ;steal --avatar --gif
            """

            if "--sticker" in args: # Cannot send a sticker with text so from reply
                if not replied_msg:
                    await message.channel.send("Error, You must reply to the sticker with command!")
                    return
                
                if len(args) > 2:
                    return
                
                for sticker in replied_msg.stickers:
                    Temp.download_image(sticker.url, f"images/{sticker.name}{file_t}")

            elif "--emoji" in args:
                if message.reference:
                    replied_msg = await message.channel.fetch_message(message.reference.message_id)
                    emojis = Temp.get_emojis(replied_msg.content.split(" "))
                    for e in emojis: Temp.download_image(f"https://cdn.discordapp.com/emojis/{e}{file_t}", f"images/{e}{file_t}")
                    await message.channel.send(f"Successfully downloaded {len(emojis)} emoji!")
                    return 

                emojis = Temp.get_emojis(message.content.split(" "))
                for e in emojis: Temp.download_image(f"https://cdn.discordapp.com/emojis/{e}{file_t}", f"images/{e}{file_t}")
                await message.channel.send(f"Successfully downloaded {len(emojis)} emoji!")

            elif "--link" in args:
                url = args[1]
                if message.reference:
                    replied_msg = await message.channel.fetch_message(message.reference.message_id)
                    url = replied_msg.content

                file_t = ".png"
                if "--gif" in args:
                    file_t = ".gif"

                Temp.download_image(url, f"images/dadadad_{random.randint(1, 999999)}{file_t}")
                await message.channel.send("Image saved!")
            
            elif "--avatar" in args:
                Temp.download_image(message.mentions[0].display_avatar.url, f"images/{message.mentions[0].id}{file_t}")
                await message.channel.send(f"Successfully downloaded {args[len(args) - 1]}'s avatar!")

        """
                [TESTING]: Custom Command
            @command: -compress
        """
        if message.content.startswith(";compress"):
            args = message.content.split(" ")
            url = args[1]
            if message.reference:
                replied_msg = await message.channel.fetch_message(message.reference.message_id)
                if replied_msg:
                    url = replied_msg.content
            
            file_t = ".png"
            if args[len(args) - 1] == "--gif":
                file_t = ".gif"
            
            path = f"test{file_t}"
            await message.channel.send(f"Downloading image...")
            Temp.download_image(url, path)
            Compressor.compress_image(path)
            await message.channel.send(f"Successfully adjusted the {file_t[1:]} to sticker/emoji requirement 512KB", file = discord.File(path, filename=path))
            os.remove(f"test{file_t}")

        # if message.content == ";test":
            # for attachment in message.attachments:

























"""

        [ WARNING; DO NOT SCROLL ANYMORE ]

"""







































try:
    intents = discord.Intents.all()
    intents.message_content = True

    bot = Algo(intents=intents)
    bot.run(Temp.get_token())
except KeyboardInterrupt:
    exit(0)
