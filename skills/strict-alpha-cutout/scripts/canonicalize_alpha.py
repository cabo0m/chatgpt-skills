from __future__ import annotations

import argparse
from pathlib import Path


def canonicalize_alpha(source: Path, output: Path, threshold: int = 128) -> None:
    if not 1 <= threshold <= 254:
        raise ValueError("threshold must be between 1 and 254")

    try:
        from PIL import Image
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("Pillow is required for alpha canonicalization") from exc

    with Image.open(source) as image:
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        binary_alpha = alpha.point(lambda value: 255 if value >= threshold else 0, mode="L")
        rgba.putalpha(binary_alpha)
        output.parent.mkdir(parents=True, exist_ok=True)
        rgba.save(output, format="PNG")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Threshold the alpha channel of an existing cutout. "
            "This does not perform segmentation and must not be used on an ordinary source photo as a background-removal substitute."
        )
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--threshold", type=int, default=128)
    args = parser.parse_args()

    try:
        canonicalize_alpha(args.source, args.output, args.threshold)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2

    print(f"WROTE: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
