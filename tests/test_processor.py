from pathlib import Path
import pytest
from src.processor import calculate_target_size, create_thumbnail, resize_image, process_image, apply_grayscale
from src.main import process_directory
from PIL import Image, UnidentifiedImageError


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
        grayscale=False
    )

    assert (output_dir / "sample.webp").exists()
    assert (thumbnail_dir / "sample.jpg").exists()
    assert metadata["filename"] == "sample.jpg"

    with Image.open(output_dir / "sample.webp") as output_image:
        assert output_image.size == (1600, 800)
        assert output_image.format == "WEBP"

    with Image.open(thumbnail_dir / "sample.jpg") as thumbnail_image:
        assert thumbnail_image.size == (300, 150)


def test_process_image_rejects_invalid_image(tmp_path: Path) -> None:
    input_path = tmp_path / "broken.jpg"
    output_dir = tmp_path / "output"
    thumbnail_dir = output_dir / "thumbnails"

    output_dir.mkdir()
    thumbnail_dir.mkdir()

    input_path.write_text("this is not a real image", encoding="utf-8")

    with pytest.raises(UnidentifiedImageError):
        process_image(
            path=input_path,
            output_dir=output_dir,
            thumbnail_dir=thumbnail_dir,
            max_size=1600,
            thumbnail_size=300,
            quality=85,
            output_format="webp",
            grayscale=False
        )


def test_process_directory_continues_after_invalid_image(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    thumbnail_dir = output_dir / "thumbnails"

    input_dir.mkdir()
    output_dir.mkdir()
    thumbnail_dir.mkdir()

    valid_image_path = input_dir / "valid.jpg"
    broken_image_path = input_dir / "broken.jpg"

    image = Image.new("RGB", (800, 600))
    image.save(valid_image_path, format="JPEG")

    broken_image_path.write_text(
        "this is not a real image",
        encoding="utf-8",
    )

    metadata_records, processed_count = process_directory(
        input_dir=input_dir,
        output_dir=output_dir,
        thumbnail_dir=thumbnail_dir,
        max_size=1600,
        thumbnail_size=300,
        quality=85,
        output_format="webp",
        grayscale=False
    )

    assert processed_count == 1
    assert len(metadata_records) == 1
    assert metadata_records[0]["filename"] == "valid.jpg"
    assert (output_dir / "valid.webp").exists()
    assert not (output_dir / "broken.webp").exists()


def test_process_image_applies_exif_orientation(tmp_path: Path) -> None:
    input_path = tmp_path / "rotated.jpg"
    output_dir = tmp_path / "output"
    thumbnail_dir = output_dir / "thumbnails"

    output_dir.mkdir()
    thumbnail_dir.mkdir()

    image = Image.new("RGB", (1200, 800))

    exif = Image.Exif()
    exif[274] = 6

    image.save(
        input_path,
        format="JPEG",
        exif=exif,
    )

    metadata = process_image(
        path=input_path,
        output_dir=output_dir,
        thumbnail_dir=thumbnail_dir,
        max_size=1600,
        thumbnail_size=300,
        quality=85,
        output_format="webp",
        grayscale=False
    )

    assert metadata["width"] == 800
    assert metadata["height"] == 1200

    with Image.open(output_dir / "rotated.webp") as output_image:
        assert output_image.size == (800, 1200)


def test_process_image_converts_rgba_to_rgb_for_jpeg(tmp_path: Path) -> None:
    input_path = tmp_path / "transparent.png"
    output_dir = tmp_path / "output"
    thumbnail_dir = output_dir / "thumbnails"

    output_dir.mkdir()
    thumbnail_dir.mkdir()

    image = Image.new("RGBA", (800, 600), (255, 0, 0, 128))
    image.save(input_path, format="PNG")

    process_image(
        path=input_path,
        output_dir=output_dir,
        thumbnail_dir=thumbnail_dir,
        max_size=1600,
        thumbnail_size=300,
        quality=85,
        output_format="jpg",
        grayscale=False
    )

    output_path = output_dir / "transparent.jpg"

    assert output_path.exists()

    with Image.open(output_path) as output_image:
        assert output_image.format == "JPEG"
        assert output_image.mode == "RGB"
        assert output_image.size == (800, 600)

def test_process_image_converts_to_grayscale(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.jpg"
    output_dir = tmp_path / "output"
    thumbnail_dir = output_dir / "thumbnails"

    output_dir.mkdir()
    thumbnail_dir.mkdir()

    image = Image.new("RGB", (800, 600), (255, 0, 0))
    image.save(input_path, format="JPEG")

    process_image(
        path=input_path,
        output_dir=output_dir,
        thumbnail_dir=thumbnail_dir,
        max_size=1600,
        thumbnail_size=300,
        quality=85,
        output_format="png",
        grayscale=True,
    )

    with Image.open(output_dir / "sample.png") as output_image:
        assert output_image.mode == "L"
    with Image.open(thumbnail_dir / "sample.jpg") as thumbnail_image:
        assert thumbnail_image.mode == "L"


def test_apply_grayscale_when_enabled() -> None:
    image = Image.new("RGB", (100, 100))

    result = apply_grayscale(image, True)

    assert result.mode == "L"


def test_apply_grayscale_when_disabled() -> None:
    image = Image.new("RGB", (100, 100))

    result = apply_grayscale(image, False)

    assert result.mode == "RGB" 