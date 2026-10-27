#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow is required: pip install Pillow", file=sys.stderr)
    raise SystemExit(2)


def inspect(path: Path) -> dict:
    with Image.open(path) as img:
        fmt = img.format
        mode = img.mode
        size = list(img.size)
        has_alpha = "A" in img.getbands()
        result = {
            "path": str(path),
            "format": fmt,
            "mode": mode,
            "size": size,
            "has_alpha": has_alpha,
        }
        if not has_alpha:
            result.update({
                "transparent_pixels": 0,
                "opaque_pixels": 0,
                "intermediate_alpha_pixels": 0,
                "unique_alpha_values": [],
            })
            return result

        alpha = img.getchannel("A")
        hist = alpha.histogram()
        unique = [idx for idx, count in enumerate(hist) if count]
        result.update({
            "transparent_pixels": hist[0],
            "opaque_pixels": hist[255],
            "intermediate_alpha_pixels": sum(hist[1:255]),
            "unique_alpha_values": unique,
        })
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect PNG alpha without modifying the image.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--strict-binary", action="store_true",
                        help="Fail unless alpha values are a subset of {0,255}.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    if not args.image.exists():
        print(f"File not found: {args.image}", file=sys.stderr)
        return 2

    data = inspect(args.image)
    if args.as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for key, value in data.items():
            print(f"{key}: {value}")

    ok = True
    if data["format"] != "PNG":
        ok = False
        print("FAIL: output is not PNG", file=sys.stderr)
    if not data["has_alpha"]:
        ok = False
        print("FAIL: output has no alpha channel", file=sys.stderr)
    else:
        if data["transparent_pixels"] == 0:
            ok = False
            print("FAIL: no fully transparent pixels", file=sys.stderr)
        if data["opaque_pixels"] == 0:
            ok = False
            print("FAIL: no fully opaque pixels", file=sys.stderr)
        if args.strict_binary and data["intermediate_alpha_pixels"]:
            ok = False
            print("FAIL: strict binary mode contains alpha 1..254", file=sys.stderr)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
