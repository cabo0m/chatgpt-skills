import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

try:
    from PIL import Image
except ImportError:
    Image = None


@unittest.skipIf(Image is None, "Pillow not installed")
class AlphaInspectorTests(unittest.TestCase):
    def test_binary_png_passes_strict_mode(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ok.png"
            img = Image.new("RGBA", (4, 4), (10, 20, 30, 0))
            img.putpixel((1, 1), (10, 20, 30, 255))
            img.save(path)
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts/inspect_alpha.py"), str(path), "--strict-binary"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_intermediate_alpha_fails_strict_mode(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad.png"
            img = Image.new("RGBA", (4, 4), (10, 20, 30, 0))
            img.putpixel((1, 1), (10, 20, 30, 128))
            img.putpixel((2, 2), (10, 20, 30, 255))
            img.save(path)
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts/inspect_alpha.py"), str(path), "--strict-binary"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(proc.returncode, 1)
            self.assertIn("strict binary", proc.stderr.lower())


if __name__ == "__main__":
    unittest.main()
