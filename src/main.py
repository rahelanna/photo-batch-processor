from PIL import Image
from PIL.Image import Resampling
from pathlib import Path

input_dir = Path("input")
output_dir = Path("output")

supported_formats = {".jpg", ".jpeg", ".png"}

print("input:")

for path in input_dir.iterdir():
    extension = path.suffix.lower()
    if extension not in supported_formats:
        continue
    print(path.name)


    with Image.open(path) as img:
        width, height = img.size
        img_format = img.format
        img_mode = img.mode

        print(f"Size: {width} x {height}")
        print(f"Format: {img_format}")
        print(f"Mode: {img_mode}")


        scale = min(1, 1600 / width, 1600 / height)
        target_height = round(height * scale)
        target_width = round(width * scale)

        img_resize =  img.resize((target_width, target_height), Resampling.LANCZOS)
        img_resize.save(output_dir / path.name)

        print(f"Resized img size: {img_resize.size}")