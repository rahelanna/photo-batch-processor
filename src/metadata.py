from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import csv


def extract_metadata(image: Image.Image, path: Path, image_format: str | None) -> dict:
    width, height = image.size
    img_size = path.stat().st_size
    exif_data = image.getexif()

    camera_make = None
    camera_model = None
    captured_at = None

    for tag_id, tag_value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        if tag_name == "Make":
            camera_make = tag_value.rstrip("\x00").strip()
        if tag_name == "Model":
            camera_model = tag_value.rstrip("\x00").strip()
        if tag_name == "DateTime":
            captured_at = tag_value

    metadata = {
        'filename': path.name,
        'width': width,
        'height': height,
        'size': img_size,
        'format': image_format,
        'camera_make': camera_make,
        'camera_model': camera_model,
        'captured_at': captured_at,
    }
    return metadata


def export_metadata_csv(metadata_records: list[dict], csv_path: Path) -> None:
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

        with open(csv_path, mode="w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in metadata_records:
                writer.writerow(row)
