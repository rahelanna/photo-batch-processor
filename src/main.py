from PIL import Image
from PIL.Image import Resampling

with Image.open("../input/sample.jpg") as img:
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
    img_resize.save("../output/sample.jpg")

    print(f"Resized img size: {img_resize.size}")