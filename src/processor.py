from PIL import Image
from PIL.Image import Resampling


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