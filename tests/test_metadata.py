from pathlib import Path
from PIL import Image
from src.metadata import extract_metadata


def test_extract_metadata_basic_fields(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.jpg"

    image = Image.new("RGB", (800, 600))
    image.save(image_path, format="JPEG")

    with Image.open(image_path) as loaded_image:
        metadata = extract_metadata(
            loaded_image,
            image_path,
            loaded_image.format,
        )

    assert metadata["filename"] == "sample.jpg"
    assert metadata["width"] == 800
    assert metadata["height"] == 600
    assert metadata["format"] == "JPEG"


def test_extract_metadata_exif_fields(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.jpg"

    image = Image.new("RGB", (800, 600))

    exif = Image.Exif()
    exif[271] = "Canon"
    exif[272] = "EOS Test"
    exif[306] = "2026:10:09 16:45:00"

    image.save(
        image_path,
        format="JPEG",
        exif=exif,
    )

    with Image.open(image_path) as loaded_image:
        metadata = extract_metadata(
            loaded_image,
            image_path,
            loaded_image.format,
        )

    assert metadata["camera_make"] == "Canon"
    assert metadata["camera_model"] == "EOS Test"
    assert metadata["captured_at"] == "2026:10:09 16:45:00"
