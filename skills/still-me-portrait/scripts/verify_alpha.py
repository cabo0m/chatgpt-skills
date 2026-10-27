import sys
from pathlib import Path


def main(argv):
    if len(argv) != 2:
        print("Usage: python scripts/verify_alpha.py <image_path>")
        return 2

    image_path = Path(argv[1])
    if not image_path.exists():
        print(f"ERROR: file does not exist: {image_path}")
        return 1

    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow is required to verify alpha channels. Install the version from requirements-optional.txt.")
        return 1

    with Image.open(image_path) as image:
        if "A" not in image.getbands():
            print("ERROR: image has no alpha channel.")
            return 1

        alpha = image.getchannel("A")
        histogram = alpha.histogram()
        transparent = histogram[0]
        opaque = histogram[255]
        semi_transparent = sum(histogram[1:255])
        total = transparent + opaque + semi_transparent

        if total == 0:
            print("ERROR: image has no alpha samples.")
            return 1
        if transparent == 0 and semi_transparent == 0:
            print("ERROR: image alpha exists but the image is fully opaque.")
            return 1
        if opaque == 0 and semi_transparent == 0:
            print("ERROR: image is fully transparent.")
            return 1

        print(f"OK: transparent={transparent}, semi-transparent={semi_transparent}, opaque={opaque}, total={total}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
