import io, os, imageio
from PIL import Image, ImageSequence

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
        # reader = imageio.get_reader(input_path)
        # frames = []
        # scale = 1.0

        # while True:
        #     frames.clear()
        #     for frame in reader:
        #         image = Image.fromarray(frame)
        #         image = image.resize((int(image.width * scale), int(image.height * scale)), Image.LANCZOS)
        #         frames.append(image)

        #     frames[0].save(
        #         temp_path,
        #         save_all=True,
        #         append_images=frames[1:],
        #         loop=0,
        #         optimize=True,
        #         duration=int(1000 / Compressor.GIF_FPS),
        #         disposal=2
        #     )

        #     if os.path.getsize(temp_path) <= Compressor.MAX_SIZE or scale < 0.1:
        #         print(f"[✓] GIF compressed to {os.path.getsize(temp_path) / 1024:.1f} KB")
        #         return temp_path

        #     scale *= Compressor.RESIZE_STEP  # reduce size