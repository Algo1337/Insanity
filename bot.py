import discord, requests, time, pytz, asyncio, random, os, math, pyttsx3, yt_dlp

from discord import ChannelType, FFmpegPCMAudio
from datetime import timezone
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
        local_tz = pytz.timezone('America/Kentucky/Louisville')
        print(f"[ + ] Message: \x1b[31m{message.guild.name}/{message.channel.name}\x1b[0m | \x1b[32m{message.created_at.replace(tzinfo=timezone.utc).astimezone(local_tz).strftime('%m-%d-%Y %H:%M:%S')}\x1b[0m \x1b[33m{message.author.display_name}:{message.author.name}\x1b[0m: {message.content}")

        """
            Ignore bots
        """
        if message.author.bot:
            return
        
        """
            Restricting to 2 users
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
            await message.channel.send("> - List of commands\n```\n;help\n;clean <?amount> (delete this bot's messages only)\n;join\n;watchvc <vc_id>\n;switch\n;leavevc\n;vcsay <text> (vcsayq for quiet operation)\n;sayvc <text>\n;yt <url>\n;stop```")
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
        
try:
    intents = discord.Intents.all()
    intents.message_content = True

    bot = Algo(intents=intents)
    bot.run("MTM3MDA3ODk4MzQ3MDg0MTkyNw.GVxS8M._lRStsHT1LPHi2eZqpdAFjT7waAk7v2FiDeYgs")
except KeyboardInterrupt:
    exit(0)
