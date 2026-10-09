from pathlib import Path
from PIL import Image
from src.metadata import extract_metadata, export_metadata_csv


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


def test_export_metadata_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "metadata.csv"
    metadata_records = [
        {
            "filename": "sample.jpg",
            "width": 800,
            "height": 600,
            "size": 12345,
            "format": "JPEG",
            "camera_make": "Canon",
            "camera_model": "EOS Test",
            "captured_at": "2026:10:09 16:45:00",
        }
    ]

    export_metadata_csv(metadata_records, csv_path)

    assert csv_path.exists()

    content = csv_path.read_text(encoding="utf-8")

    assert "filename,width,height,size,format,camera_make,camera_model,captured_at" in content
    assert "sample.jpg,800,600,12345,JPEG,Canon,EOS Test,2026:10:09 16:45:00" in content


def test_export_metadata_csv_with_no_records(tmp_path: Path) -> None:
    csv_path = tmp_path / "metadata.csv"

    export_metadata_csv([], csv_path)

    assert not csv_path.exists()