import logging
from PIL import Image, ImageOps
from PIL.Image import Resampling
from pathlib import Path

from src.metadata import extract_metadata


logger = logging.getLogger(__name__)
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

def process_image(path: Path, output_dir: Path, thumbnail_dir: Path, max_size: int, thumbnail_size: int, quality: int, output_format: str) -> dict:
    with Image.open(path) as image:
        img_format = image.format
        image = ImageOps.exif_transpose(image)
        metadata = extract_metadata(image, path, img_format)

        resized_image = resize_image(image, max_size)

        if output_format == "jpg":
            file_extension = ".jpg"
            pillow_format = "JPEG"
        elif output_format == "jpeg":
            file_extension = ".jpeg"
            pillow_format = "JPEG"
        elif output_format == "png":
            file_extension = ".png"
            pillow_format = "PNG"
        else:
            file_extension = ".webp"
            pillow_format = "WEBP"

        output_path = output_dir / path.with_suffix(file_extension).name

        if pillow_format == "JPEG" and resized_image.mode != "RGB":
            resized_image = resized_image.convert("RGB")

        if pillow_format == "PNG":
            resized_image.save(output_path, format=pillow_format)
        else:
            resized_image.save(output_path, format=pillow_format, quality=quality)
        logger.info(f"Saved processed image: {output_path}")

        thumbnail_image = create_thumbnail(image, thumbnail_size)
        thumbnail_image.save(thumbnail_dir / path.name)
        logger.info(f"Saved thumbnail image: {thumbnail_dir / path.name}")

    return metadata
