from pathlib import Path

from src.processor import calculate_target_size, create_thumbnail, resize_image, process_image
from PIL import Image


def test_calculate_target_size_landscape() -> None:
    result = calculate_target_size(4000, 1844, 1600)
    assert result == (1600, 738)

def test_calculate_target_size_portrait() -> None:
    result = calculate_target_size(1844, 4000, 1600)
    assert result == (738, 1600)

def test_calculate_target_size_not_upscale() -> None:
    result = calculate_target_size(1089, 700, 1600)
    assert result == (1089, 700)

def test_create_thumbnail() -> None:
    image = Image.new("RGB", (4000, 2000))
    thumbnail = create_thumbnail(image, 300)
    assert thumbnail.size == (300, 150)

def test_create_thumbnail_not_upscale() -> None:
    image = Image.new("RGB", (120, 80))
    thumbnail = create_thumbnail(image, 300)
    assert thumbnail.size == (120, 80)

def test_resize_image() -> None:
    image = Image.new("RGB", (4000, 2000))
    resized = resize_image(image, 1600)
    assert resized.size == (1600, 800)

def test_process_image_creates_output_files(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.jpg"
    output_dir = tmp_path / "output"
    thumbnail_dir = tmp_path / "thumbnail"

    output_dir.mkdir()
    thumbnail_dir.mkdir()

    image = Image.new("RGB", (2000, 1000))
    image.save(input_path, format="JPEG")

    metadata = process_image(
        path=input_path,
        output_dir=output_dir,
        thumbnail_dir=thumbnail_dir,
        max_size=1600,
        thumbnail_size=300,
        quality=85,
        output_format="webp",
    )

    assert (output_dir / "sample.webp").exists()
    assert (thumbnail_dir / "sample.jpg").exists()
    assert metadata["filename"] == "sample.jpg"

    with Image.open(output_dir / "sample.webp") as output_image:
        assert output_image.size == (1600, 800)
        assert output_image.format == "WEBP"

    with Image.open(thumbnail_dir / "sample.jpg") as thumbnail_image:
        assert thumbnail_image.size == (300, 150)
