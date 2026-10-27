import sys
from pathlib import Path


VERY_SMALL_LIMIT = 256


def main(argv):
    if len(argv) != 2:
        print("Usage: python scripts/inspect_image.py <image_path>")
        return 2

    image_path = Path(argv[1])
    if not image_path.exists():
        print(f"ERROR: file does not exist: {image_path}")
        return 1

    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow is required for local image inspection. Install the version from requirements-optional.txt.")
        return 1

    with Image.open(image_path) as image:
        width, height = image.size
        mode = image.mode
        exif = image.getexif()
        orientation = exif.get(274) if exif else None
        if mode in {"1", "L", "LA"}:
            color_family = "grayscale"
        elif "A" in image.getbands():
            color_family = "RGBA"
        else:
            color_family = "RGB"

        print(f"Format: {image.format}")
        print(f"Size: {width}x{height}")
        print(f"Mode: {mode}")
        print(f"Color family: {color_family}")
        print(f"Has EXIF: {'yes' if exif else 'no'}")
        print(f"Orientation: {orientation if orientation is not None else 'not present'}")
        print(f"Resolution note: {'very small image' if width < VERY_SMALL_LIMIT or height < VERY_SMALL_LIMIT else 'size is not flagged as very small'}")
        if width < VERY_SMALL_LIMIT or height < VERY_SMALL_LIMIT:
            print("Warning: the image is very small and may not support faithful restoration of fine detail.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
