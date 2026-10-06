from PIL import Image, ImageOps
from pathlib import Path
import csv

from src.processor import  resize_image, create_thumbnail
from src.metadata import extract_metadata

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
        img = ImageOps.exif_transpose(img)

        metadata = extract_metadata(img, path, img_format)

        metadata_records.append(metadata)
        print(f"Metadata: {metadata}")

        img_resize = resize_image(img, 1600)
        output_path = output_dir / path.with_suffix(".webp").name
        img_resize.save(output_path, format="webp", quality=85)

        print(f"Resized img size: {img_resize.size}")
        print(f"Saved resize image to: {output_path}")

        img_thumbnail = create_thumbnail(img, max_size=300)
        img_thumbnail.save(thumbnail_dir / path.name)

        print(f"Thumbnail size: {img_thumbnail.size}")


csv_path = output_dir / "metadata.csv"

if metadata_records:
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

