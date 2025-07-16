import discord, requests, time, pytz, asyncio, random, os, math, pyttsx3, yt_dlp


from discord import ChannelType, FFmpegPCMAudio
from datetime import timezone
from translatepy import Translator
from gtts import gTTS

CURRENT_VC = None
WATCHING_VC = False
PLAYING = False
THRESHOLD = 200
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

class Temp:
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
        if message.content.startswith(";") and (message.author.id != 1235776145819959318 and message.author.id != 1163512624483405976):
            await message.channel.send("Error, Only the creators can use this bot!")
            return
        
        """
                [TESTING]: Custom Command
            @command: -help
        """
        if message.content == ";help":
            await message.delete()
            await message.channel.send("> - List of commands\n```\n;help\n;clean <?amount> (delete this bot's messages only)\n;join\n;watchvc <vc_id>\n;switch\n;leavevc\n;vcsay <text> (vcsayq for quiet operation)\n;sayvc <text>\n;yt <url>\n;stop\n;nuke```")
            return
        
        """
                [TESTING]: Custom Command
            @command: -clean
        """
        if message.content == ";clean":
            await message.delete()

            msg_count = 100
            if " " in message.content:
                msg_count = int(message.content.split(" ")[1])

            async for msg in message.channel.history(limit=msg_count, oldest_first=False):
                if msg.author.id == self.user.id:
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
            
            text = " ".join(message.content.split(" ")[1:])
            tts = gTTS(text, lang='en', tld='co.uk')
            tts.save("test.mp3")

            vc = message.author.voice.channel

            if not message.guild.voice_client:
                await asyncio.sleep(5)

            await vc.guild.me.edit(mute=False, deafen=True)
            audio_source = FFmpegPCMAudio(
                "test.mp3",
                options='-filter:a "volume=5"'
            )
            message.guild.voice_client.play(audio_source, after=lambda e: print("Done"))
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
        if message.content.startswith(";sayvc"):
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
            
            if not message.guild.voice_client:
                await asyncio.sleep(5)

            text = " ".join(message.content.split(" ")[1:])
            engine = pyttsx3.init()
            engine.setProperty('rate', 125)
            engine.setProperty('volume', 1.0)

            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.save_to_file(text, 'test.mp3')
            engine.runAndWait()
            
            await vc.guild.me.edit(mute=False, deafen=True)
            await asyncio.sleep(5)
            audio_source = FFmpegPCMAudio(
                "test.mp3",
                options='-filter:a "volume=5"'
            )
            message.guild.voice_client.play(audio_source, after=lambda e: print("Done"))
            while message.guild.voice_client.is_playing():
                await asyncio.sleep(1)

            os.remove("test.mp3")
            await vc.guild.me.edit(mute=True, deafen=True)
            if message.content.startswith(";sayvcq"):
                return
            
            await message.channel.send(f"[ + ] TTS \"{text}\" Done")

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
            await cloned_channel.edit(category=old_category, position=old_position)

            await cloned_channel.send(f"✅ {message.author.mention} nuked")
            await old_channel.delete(reason="Nuked")

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

        if message.content.startswith(";steal"):
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
                Possible formarts:
                    ;steal --sticker png_name
                    ;steal --sticker --gif gif_name
                    ;steal --emoji png_name
                    ;steal --emoji --gif gif_name
                    ;steal --image name
                    ;steal --image --gif name
            """

            if "--sticker" in args: # Cannot send a sticker with text so from reply
                if not replied_msg:
                    await message.channel.send("Error, You must reply to the sticker with command!")
                    return
                
                if len(args) > 2:
                    return
                
                for sticker in replied_msg.stickers:
                    Temp.download_image(sticker.url, sticker.name + file_t)

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

                
                


        
try:
    intents = discord.Intents.all()
    intents.message_content = True

    bot = Algo(intents=intents)
    bot.run("MTM3MDA3ODk4MzQ3MDg0MTkyNw.GiOSsU.UOoDdMXUVaBRy27KU3CvTrw-eW9EqFBtnKfdr8")
except KeyboardInterrupt:
    exit(0)
