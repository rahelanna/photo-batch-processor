from PIL import Image, ImageOps
from PIL.Image import Resampling
from pathlib import Path
from src.metadata import extract_metadata


def calculate_target_size(width, height, max_size) -> tuple[int, int]:

    scale = min(1, max_size / width, max_size / height)
    target_width = round(width * scale)
    target_height = round(height * scale)

    return target_width, target_height


def resize_image(image: Image.Image, max_size: int) -> Image.Image:
    width, height = image.size
    target_width, target_height = calculate_target_size(width, height, max_size)

    resized_image = image.resize((target_width, target_height), Resampling.LANCZOS)
    return resized_image


def create_thumbnail(image: Image.Image, max_size: int) -> Image.Image:
    img_thumbnail = image.copy()
    img_thumbnail.thumbnail((max_size, max_size), Resampling.LANCZOS)
    return img_thumbnail

def process_image(path: Path, output_dir: Path, thumbnail_dir: Path, max_size: int, thumbnail_size: int, quality: int) -> dict:
    with Image.open(path) as image:
        img_format = image.format
        image = ImageOps.exif_transpose(image)
        metadata = extract_metadata(image, path, img_format)

        resized_image = resize_image(image, max_size)
        output_path = output_dir / path.with_suffix(".webp").name
        resized_image.save(output_path, format="webp", quality=quality)

        thumbnail_image = create_thumbnail(image, thumbnail_size)
        thumbnail_image.save(thumbnail_dir / path.name)

    return metadata
