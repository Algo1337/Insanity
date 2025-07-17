import os, imageio
from PIL import Image

class Compressor():
    MAX_SIZE: float     = 512 * 1024
    RESIZE_STEP: float  = 0.9
    GIF_FPS: int        = 15
    def compress_image(name: str):
        path = name
        ext = os.path.splitext(path)[1].lower()

        if ext == ".png":
            out = Compressor.compress_png(path)
        elif ext == ".gif":
            out = Compressor.compress_gif(path)
        else:
            print("Unsupported file type. Use PNG or GIF.")
            return

        print(f"Successfully compressed!")

    def compress_png(input_path):
        img = Image.open(input_path)
        quality = 90
        scale = 1.0

        while True:
            temp_path = "test.png"
            resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
            resized.save(temp_path, optimize=True)

            if os.path.getsize(temp_path) <= Compressor.MAX_SIZE or scale < 0.1:
                print(f"[✓] PNG compressed to {os.path.getsize(temp_path) / 1024:.1f} KB")
                return temp_path

            scale *= Compressor.RESIZE_STEP  # reduce size

    def compress_gif(input_path):
        reader = imageio.get_reader(input_path)
        frames = []
        scale = 1.0

        while True:
            frames.clear()
            for frame in reader:
                image = Image.fromarray(frame)
                image = image.resize((int(image.width * scale), int(image.height * scale)), Image.LANCZOS)
                frames.append(image)

            temp_path = "test.gif"
            frames[0].save(
                temp_path,
                save_all=True,
                append_images=frames[1:],
                loop=0,
                optimize=True,
                duration=int(1000 / Compressor.GIF_FPS),
                disposal=2
            )

            if os.path.getsize(temp_path) <= Compressor.MAX_SIZE or scale < 0.1:
                print(f"[✓] GIF compressed to {os.path.getsize(temp_path) / 1024:.1f} KB")
                return temp_path

            scale *= Compressor.RESIZE_STEP  # reduce size