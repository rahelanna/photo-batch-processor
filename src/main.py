import argparse
import logging
from pathlib import Path

from src.processor import  process_image
from src.metadata import  export_metadata_csv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

parser = argparse.ArgumentParser(
    description="Process input directory and output directory and extract metadata")

parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("--max-size", type=int, default=1600)
parser.add_argument("--quality", type=int, default=85)
parser.add_argument("--thumbnail-size", type=int, default=300)
parser.add_argument("--format", type=str,choices=["jpg", "png", "jpeg", "webp"], default="webp")

args = parser.parse_args()

if not 0 <= args.quality <= 100:
    parser.error(f"quality must be between 0 and 100")
if args.max_size <= 0:
    parser.error(f"max_size must be greater than 0")
if args.thumbnail_size <= 0:
    parser.error(f"thumbnail_size must be greater than 0")

input_dir = Path(args.input)
output_dir = Path(args.output)
thumbnail_dir = output_dir / "thumbnails"

output_dir.mkdir(parents=True, exist_ok=True)
thumbnail_dir.mkdir(parents=True, exist_ok=True)

if input_dir.exists() and input_dir.is_dir():
    logger.info(f"Found input directory: {input_dir}")
else:
    logger.error(f"Input directory does not exist: {input_dir}")
    exit(1)

supported_formats = {".jpg", ".jpeg", ".png"}
processed_count = 0

metadata_records = []

for path in input_dir.iterdir():
    extension = path.suffix.lower()
    if extension not in supported_formats:
        continue
    logger.info(f"Processing image: {path.name}")

    try:

        metadata = process_image(
            path=path,
            output_dir=output_dir,
            thumbnail_dir=thumbnail_dir,
            max_size=args.max_size,
            thumbnail_size=args.thumbnail_size,
            quality=args.quality,
            output_format=args.format,)

        metadata_records.append(metadata)
        processed_count += 1
    except Exception as e:
        logger.error(f"Failed to process image: {path.name}, error: {e}")


csv_path = output_dir / "metadata.csv"

export_metadata_csv(metadata_records, csv_path)

if processed_count > 0:
    logger.info(f"Processed {processed_count} images")
else:
    print("No supported images found in input directory. Supported formats: .jpg, .jpeg, .png")

