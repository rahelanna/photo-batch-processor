from PIL import Image
from PIL.Image import Resampling
from pathlib import Path

input_dir = Path("input")
output_dir = Path("output")
thumbnail_dir = output_dir / "thumbnails"

output_dir.mkdir(parents=True, exist_ok=True)
thumbnail_dir.mkdir(parents=True, exist_ok=True)

if input_dir.exists() and input_dir.is_dir():
    print("Input dir exists")
else:
    print("Input dir doesn't exist")
    exit(1)

supported_formats = {".jpg", ".jpeg", ".png"}
processed_count = 0

print("input:")

for path in input_dir.iterdir():
    extension = path.suffix.lower()
    if extension not in supported_formats:
        continue
    print(path.name)
    processed_count += 1


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

        img_thumbnail = img.copy()
        img_thumbnail.thumbnail((300, 300), Resampling.LANCZOS)
        img_thumbnail.save(thumbnail_dir / path.name)

        print(f"Thumbnail size: {img_thumbnail.size}")

if processed_count > 0:
    print(f"Processed {processed_count} images")
else:
    print("No supported images found in input directory. Supported formats: .jpg, .jpeg, .png")

