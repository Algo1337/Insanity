import os, sys, subprocess, discord, random, cv2, imageio
import imageio.v3 as iio

from src.discord_utils import *

TARGET = 512 * 1024

__COMPRESS_ARG_COUNT__ = 2
__COMPRESS_INVALID_ARG_ERR__ = discord.Embed(title = "Image/Gif Compressor", description = "Private NIGGA, FUCK OFF", color = discord.Colour.red())
__COMPRESS_INVALID_ARG_ERR__.set_author(name = "Insanity", icon_url = "https://images-ext-1.discordapp.net/external/7bqZYfRkXl8ptusN1g9UbNJyef772k0uG-htjp6dOLU/%3Fsize%3D512/https/cdn.discordapp.com/icons/1370013148983201792/d26c2fddc3bdaf3a2fbd047c4fe4ec87.png?format=webp&quality=lossless")
__COMPRESS_INVALID_ARG_ERR__.set_footer(text = "https://insanity.host")

async def compress(base, message: DiscordUtils) -> bool:
    url = message.Args[1]
    opt = ".png"

    if "--gif" in message.Args: 
        opt = ".gif"
    
    r = random.randint(0, 99999999)
    filename = f"assets/images/{r}{opt}"
    print(f"Downloading {url} -> {filename} -> images/{r}_compressed{opt}")
    DiscordUtils.download_image(url, filename)

    if url.endswith(".mp4"):
        cap = cv2.VideoCapture(filename)
        frames = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)

        cap.release()
        os.remove(filename)

        imageio.mimsave(filename, frames, fps=10)

    await asyncio.sleep(5)
    Compressor.compress_gif(filename, f"assets/images/{r}_compressed{opt}")
    await asyncio.sleep(2)

    embed = discord.Embed(title = "Img/Gif Compressor", description = "The file has been compressed to 512KB, Ready for discord sticker/emoji", color = discord.Colour.red())
    embed.set_image(url = f"attachment://assets/images/{r}_compressed{opt}")
    await message.Client.channel.send(file = discord.File(f"assets/images/{r}_compressed{opt}", filename = f"assets/images/{r}_compressed{opt}"), embed = embed)

    os.remove(filename)

    if "--save" not in message.Args:
        os.remove(f"assets/images/{r}_compressed{opt}")

    return True

class Compressor():
    MAX_SIZE: float     = 512 * 1024
    RESIZE_STEP: float  = 0.9
    GIF_FPS: int        = 15
    def compress_image(name: str, compress_output: str):
        path = name
        ext = os.path.splitext(path)[1].lower()

        if ext == ".png":
            out = Compressor.compress_png(path, compress_output)
        elif ext == ".gif":
            out = Compressor.compress_gif(path, compress_output)
        else:
            print("Unsupported file type. Use PNG or GIF.")
            return

        print(f"Successfully compressed!")

    def compress_png(input_path, temp_path):
        #img = Image.open(input_path)
        img = iio.imread(input_path)
        quality = 90
        scale = 1.0

        while True:
            resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
            resized.save(temp_path, optimize=True)

            if os.path.getsize(temp_path) <= Compressor.MAX_SIZE or scale < 0.1:
                print(f"[✓] PNG compressed to {os.path.getsize(temp_path) / 1024:.1f} KB")
                return temp_path

            scale *= Compressor.RESIZE_STEP  # reduce size

    @staticmethod
    def size(p): return os.path.getsize(p)

    @staticmethod
    def run(inp, outp, lossy, fps, width):
        vf = []

        if fps:
            vf.append(f"fps={fps}")

        if width:
            vf.append(f"scale={width}:-1:flags=lanczos")

        vf_str = ",".join(vf)

        if vf_str:
            vf_complex = (
                f"{vf_str},split[s0][s1];"
                f"[s0]palettegen[p];"
                f"[s1][p]paletteuse=dither=bayer:bayer_scale=5"
            )
        else:
            vf_complex = (
                "split[s0][s1];"
                "[s0]palettegen[p];"
                "[s1][p]paletteuse=dither=bayer:bayer_scale=5"
            )

        cmd = [
            "ffmpeg", "-y",
            "-i", inp,
            "-filter_complex", vf_complex,
            "-loop", "0",
            outp
        ]

        subprocess.run(cmd, check=True)

    @staticmethod
    def compress_gif(input_path, temp_path):
        width=None
        fps=None
        for lossy in [20,40,60,80,120,160,200]:
            try:
                Compressor.run(input_path,temp_path,lossy,fps,width)
            except Exception:
                print("ffmpeg with gif lossy not available. Install a build with gif support.")
                return
            if Compressor.size(temp_path)<=TARGET: return
            fps = 15 if fps is None else max(5,fps-2)
            width = 640 if width is None else max(160,int(width*0.8))
        print("Could not reach target exactly; produced smallest attempted GIF.")
