from __future__ import annotations

import argparse
import json
from pathlib import Path


def inspect_alpha(path: Path, mode: str = "strict-binary") -> dict[str, object]:
    try:
        from PIL import Image
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("Pillow is required for alpha inspection") from exc

    with Image.open(path) as image:
        fmt = (image.format or "").upper()
        bands = image.getbands()
        has_alpha = "A" in bands
        result: dict[str, object] = {
            "path": str(path),
            "format": fmt,
            "mode": image.mode,
            "alpha_mode": mode,
            "has_alpha": has_alpha,
        }

        if fmt != "PNG" or not has_alpha:
            result.update(
                {
                    "pass": False,
                    "reason": "output must be a PNG with a real alpha channel",
                    "alpha_0_pixels": 0,
                    "alpha_255_pixels": 0,
                    "intermediate_alpha_pixels": 0,
                }
            )
            return result

        histogram = image.getchannel("A").histogram()
        alpha_0 = int(histogram[0])
        alpha_255 = int(histogram[255])
        intermediate = int(sum(histogram[1:255]))
        nonzero = int(sum(histogram[1:]))

        if mode == "strict-binary":
            passed = alpha_0 > 0 and alpha_255 > 0 and intermediate == 0
            reason = (
                "strict binary alpha validated"
                if passed
                else "strict-binary requires background alpha 0, foreground alpha 255, and zero pixels with alpha 1..254"
            )
        elif mode == "natural-edge":
            passed = alpha_0 > 0 and nonzero > 0
            reason = "alpha channel present" if passed else "natural-edge still requires transparent background and visible foreground"
        else:
            raise ValueError(f"unsupported mode: {mode}")

        result.update(
            {
                "pass": passed,
                "reason": reason,
                "alpha_0_pixels": alpha_0,
                "alpha_255_pixels": alpha_255,
                "intermediate_alpha_pixels": intermediate,
            }
        )
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect PNG alpha for Strict Alpha Cutout.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--mode", choices=["strict-binary", "natural-edge"], default="strict-binary")
    args = parser.parse_args()

    try:
        result = inspect_alpha(args.image, args.mode)
    except (OSError, RuntimeError, ValueError) as exc:
        print(json.dumps({"pass": False, "error": str(exc)}, ensure_ascii=False))
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
