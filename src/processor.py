import logging
from pathlib import Path

from PIL import Image, ImageOps
from PIL.Image import Resampling

from src.metadata import extract_metadata


logger = logging.getLogger(__name__)


def calculate_target_size(
        width: int,
        height: int,
        max_size: int
) -> tuple[int, int]:

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


def get_output_format(output_format: str) -> tuple[str, str]:
    formats = {
        "jpg": (".jpg", "JPEG"),
        "jpeg": (".jpeg", "JPEG"),
        "png": (".png", "PNG"),
        "webp": (".webp", "WEBP"),
    }

    return formats[output_format]

def save_output_image(
    image: Image.Image,
    output_path: Path,
    pillow_format: str,
    quality: int,
) -> None:
    if pillow_format == "JPEG" and image.mode != "RGB":
        image = image.convert("RGB")

    if pillow_format == "PNG":
        image.save(output_path, format=pillow_format)
    else:
        image.save(
            output_path,
            format=pillow_format,
            quality=quality,
        )


def process_image(path: Path, output_dir: Path, thumbnail_dir: Path, max_size: int, thumbnail_size: int, quality: int, output_format: str, grayscale: bool) -> dict:
    with Image.open(path) as image:
        img_format = image.format
        image = ImageOps.exif_transpose(image)
        metadata = extract_metadata(image, path, img_format)

        resized_image = resize_image(image, max_size)

        resized_image = apply_grayscale(resized_image, grayscale)

        file_extension, pillow_format = get_output_format(output_format)

        output_path = output_dir / path.with_suffix(file_extension).name

        save_output_image(resized_image, output_path, pillow_format, quality)

        logger.info(f"Saved processed image: {output_path}")

        thumbnail_image = create_thumbnail(image, thumbnail_size)
        thumbnail_image = apply_grayscale(thumbnail_image, grayscale)
        thumbnail_image.save(thumbnail_dir / path.name)
        logger.info(f"Saved thumbnail image: {thumbnail_dir / path.name}")

    return metadata


def apply_grayscale(image: Image.Image, enabled: bool) -> Image.Image:
    if not enabled:
        return image

    return image.convert("L")