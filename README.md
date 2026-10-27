# Photo Batch Processor



A Python command-line application for batch image processing and metadata extraction.

The application processes supported images from an input directory without modifying the original files. It can resize images, generate thumbnails, convert output formats, apply grayscale processing, extract basic EXIF metadata, and export metadata to CSV.

## Features

- Batch processing for `.jpg`, `.jpeg`, and `.png` images
- Aspect-ratio preserving resize
- Configurable maximum image size
- Thumbnail generation
- JPEG, PNG, and WebP output
- Configurable output quality
- Optional grayscale processing
- EXIF orientation handling
- Basic metadata extraction
- CSV metadata export
- Error handling for invalid or corrupted images
- Structured logging
- Automated tests with pytest

## Installation

Clone the repository:

```bash
git clone https://github.com/rahelanna/photo-batch-processor.git
cd photo-batch-processor
```

Create a virtual environment.

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the application with an input directory and an output directory:

```bash
python -m src.main input output
```

Example with custom options:

```bash
python -m src.main input output --max-size 1600 --quality 85 --format webp
```

Enable grayscale processing:

```bash
python -m src.main input output --grayscale
```

Available options:

```text
input                   Input directory containing images
output                  Output directory for processed files
--max-size              Maximum width or height in pixels (default: 1600)
--quality               Output quality from 0 to 100 (default: 85)
--thumbnail-size        Maximum thumbnail width or height in pixels (default: 300)
--format                Output format: jpg, jpeg, png, or webp (default: webp)
--grayscale             Convert processed images and thumbnails to grayscale
```

## Input and Output

The application reads supported images from the input directory.

Supported input formats:

```text
.jpg
.jpeg
.png
```

Example input directory:

```text
input/
    photo1.jpg
    photo2.png
    photo3.jpeg
```

Processed images are written to the output directory. Thumbnails are stored in a separate `thumbnails` subdirectory, and extracted metadata is written to `metadata.csv`.

Example output structure:

```text
output/
    photo1.webp
    photo2.webp
    photo3.webp
    metadata.csv
    thumbnails/
        photo1.jpg
        photo2.png
        photo3.jpeg
```

The original input files are never modified.

## Example Metadata Output

The application exports extracted metadata to `metadata.csv`.

Example:

```csv
filename,width,height,size,format,camera_make,camera_model,captured_at
photo1.jpg,4000,3000,2458123,JPEG,Canon,EOS 80D,2025:08:14 12:35:20
photo2.png,1920,1080,845231,PNG,,,
```

Metadata fields may be empty when the source image does not contain the corresponding EXIF information.

## Examples

The repository includes a small example dataset under the `examples/` directory.

```text
examples/
    input/
        sample.jpg
    output/
        sample.webp
        metadata.csv
        thumbnails/
            sample.jpg
```

You can reproduce the example output with:

```bash
python -m src.main examples/input examples/output --max-size 800 --quality 85 --format webp
```

## Testing

The project uses `pytest` for automated testing.

Run the full test suite with:

```bash
python -m pytest
```

The tests cover the main image-processing and application behavior, including:

- target size calculation
- image resizing
- thumbnail generation
- output format conversion
- grayscale processing
- EXIF metadata extraction
- EXIF orientation handling
- CSV metadata export
- invalid image handling
- batch processing behavior
- CLI argument validation
- missing input directory handling

## Technologies and Libraries

- Python 3
- Pillow
- pathlib
- argparse
- csv
- logging
- pytest
- Git
- GitHub

## Known Limitations

- Supported input formats are limited to JPEG and PNG images.
- Output formats are limited to JPEG, PNG, and WebP.
- The application processes images from a single input directory and does not recursively scan subdirectories.
- EXIF metadata availability depends on the source image. Some images may not contain camera or capture date information.
- The application extracts only a small subset of EXIF metadata.
- Thumbnails keep the original input filename and format.
- The application does not preserve all original metadata in processed output images.
- Corrupted or unreadable images are skipped and reported through logging.
- Permission-related filesystem errors may stop the application when required directories or metadata output cannot be accessed.

## Future Improvements

- Recursive processing of nested input directories
- Additional input and output image formats
- More extensive EXIF metadata extraction
- Optional metadata preservation in processed images
- Configurable thumbnail output format
- More flexible resize options, such as separate maximum width and height
- Additional image-processing options, such as rotation or basic color adjustments
- Progress reporting for large batches
- More detailed logging configuration
- Continuous integration for automated test runs

## Project Structure

```text
photo-batch-processor/
    src/
        __init__.py
        main.py
        processor.py
        metadata.py
    tests/
        test_main.py
        test_metadata.py
        test_processor.py
    input/
    output/
    README.md
    requirements.txt
    .gitignore
```

Main responsibilities:

- `src/main.py` - command-line interface, argument validation, directory handling, batch orchestration, and application-level error handling
- `src/processor.py` - image resizing, thumbnail generation, grayscale processing, format conversion, and image saving
- `src/metadata.py` - EXIF metadata extraction and CSV export
- `tests/` - automated tests for CLI behavior, metadata handling, image processing, and error cases
