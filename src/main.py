from PIL import Image, ImageOps
from PIL.Image import Resampling
from PIL.ExifTags import TAGS
from pathlib import Path
import csv

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

metadata_records = []

print("input:")

for path in input_dir.iterdir():
    extension = path.suffix.lower()
    if extension not in supported_formats:
        continue
    print(path.name)
    processed_count += 1


    with Image.open(path) as img:
        img_format = img.format
        img_size = path.stat().st_size
        img = ImageOps.exif_transpose(img)
        width, height = img.size
        img_mode = img.mode
        exif_data = img.getexif()

        camera_make = None
        camera_model = None
        captured_at = None

        for tag_id, tag_value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name == "Make":
                camera_make = tag_value.rstrip("\x00")
            if tag_name == "Model":
                camera_model = tag_value.rstrip("\x00")
            if tag_name == "DateTime":
                captured_at = tag_value

        metadata = {
            'filename' : path.name,
            'width' : width,
            'height' : height,
            'size' : img_size,
            'format' : img_format,
            'camera_make' : camera_make,
            'camera_model' : camera_model,
            'captured_at' : captured_at,
        }

        metadata_records.append(metadata)
        print(f"Metadata: {metadata}")

        scale = min(1, 1600 / width, 1600 / height)
        target_height = round(height * scale)
        target_width = round(width * scale)

        img_resize =  img.resize((target_width, target_height), Resampling.LANCZOS)
        output_path = output_dir / path.with_suffix(".webp").name
        img_resize.save(output_path, format="webp", quality=85)

        print(f"Resized img size: {img_resize.size}")
        print(f"Saved resize image to: {output_path}")

        img_thumbnail = img.copy()
        img_thumbnail.thumbnail((300, 300), Resampling.LANCZOS)
        img_thumbnail.save(thumbnail_dir / path.name)

        print(f"Thumbnail size: {img_thumbnail.size}")

print(metadata_records)

csv_path = output_dir / "metadata.csv"

fieldnames = [
        "filename",
        "width",
        "height",
        "size",
        "format",
        "camera_make",
        "camera_model",
        "captured_at",
    ]

with open(csv_path, mode = "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in metadata_records:
        writer.writerow(row)

if processed_count > 0:
    print(f"Processed {processed_count} images")
else:
    print("No supported images found in input directory. Supported formats: .jpg, .jpeg, .png")

