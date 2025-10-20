import os, discord, random, cv2, imageio

from src.discord_utils import *

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
    filename = f"images/{r}{opt}"
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

    await asyncio.sleep(2)
    Compressor.compress_gif(filename, f"images/{r}_compressed{opt}")
    await asyncio.sleep(2)

    embed = discord.Embed(title = "Img/Gif Compressor", description = "The file has been compressed to 512KB, Ready for discord sticker/emoji", color = discord.Colour.red())
    embed.set_image(url = f"attachment://images/{r}_compressed{opt}")
    await message.Client.channel.send(file = discord.File(f"images/{r}_compressed{opt}", filename = f"images/{r}_compressed{opt}"), embed = embed)

    os.remove(filename)

    if "--save" not in message.Args:
        os.remove(f"images/{r}_compressed{opt}")

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
        img = Image.open(input_path)
        quality = 90
        scale = 1.0

        while True:
            resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
            resized.save(temp_path, optimize=True)

            if os.path.getsize(temp_path) <= Compressor.MAX_SIZE or scale < 0.1:
                print(f"[✓] PNG compressed to {os.path.getsize(temp_path) / 1024:.1f} KB")
                return temp_path

            scale *= Compressor.RESIZE_STEP  # reduce size

    def compress_gif(input_path, temp_path, target_size_kb=512):
        img = Image.open(input_path)
        
        # Reduce size (scale down)
        scale_factor = 0.8  # start smaller if needed
        width, height = img.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Reduce colors
        img = img.convert("P", palette=Image.ADAPTIVE, colors=64)

        # Save with optimization
        frames = []
        for frame in ImageSequence.Iterator(img):
            frames.append(frame.copy())

        # Try multiple quality attempts until under size
        for colors in [64, 48, 32, 16]:
            for scale in [0.8, 0.7, 0.6, 0.5]:
                test_img = img.resize((int(width * scale), int(height * scale)), Image.LANCZOS)
                test_img = test_img.convert("P", palette=Image.ADAPTIVE, colors=colors)

                frames_resized = []
                for frame in frames:
                    f = frame.resize((int(width * scale), int(height * scale)), Image.LANCZOS)
                    f = f.convert("P", palette=Image.ADAPTIVE, colors=colors)
                    frames_resized.append(f)

                buffer = io.BytesIO()
                frames_resized[0].save(
                    buffer,
                    format="GIF",
                    save_all=True,
                    append_images=frames_resized[1:],
                    optimize=True,
                    loop=0
                )
                size_kb = len(buffer.getvalue()) / 1024
                if size_kb <= target_size_kb:
                    with open(temp_path, "wb") as f:
                        f.write(buffer.getvalue())
                    print(f"Saved under {target_size_kb}KB at {colors} colors, {scale:.2f} scale ({size_kb:.1f}KB)")
                    return True
        print("Could not compress under target size.")
        return False