from pathlib import Path

from src.processor import  process_image
from src.metadata import  export_metadata_csv

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

    metadata = process_image(
        path=path,
        output_dir=output_dir,
        thumbnail_dir=thumbnail_dir,
        max_size=1600,
        thumbnail_size=300,
        quality=85)

    metadata_records.append(metadata)
    processed_count += 1


csv_path = output_dir / "metadata.csv"

export_metadata_csv(metadata_records, csv_path)

if processed_count > 0:
    print(f"Processed {processed_count} images")
else:
    print("No supported images found in input directory. Supported formats: .jpg, .jpeg, .png")

