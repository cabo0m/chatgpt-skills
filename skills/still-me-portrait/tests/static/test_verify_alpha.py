import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
VERIFY_SCRIPT = PACKAGE_ROOT / "scripts" / "verify_alpha.py"


@unittest.skipIf(Image is None, "Pillow is required for alpha verification tests")
class VerifyAlphaTest(unittest.TestCase):
    def create_image(self, mode, size=(4, 4), alpha_pattern=None):
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        path = Path(tempdir.name) / "image.png"
        if mode == "RGB":
            image = Image.new("RGB", size, color=(255, 255, 255))
        else:
            image = Image.new("RGBA", size, color=(255, 255, 255, 255))
            if alpha_pattern is not None:
                for x in range(size[0]):
                    for y in range(size[1]):
                        r, g, b, _ = image.getpixel((x, y))
                        image.putpixel((x, y), (r, g, b, alpha_pattern(x, y)))
        image.save(path)
        return path

    def run_script(self, image_path: Path):
        return subprocess.run(
            [sys.executable, str(VERIFY_SCRIPT), str(image_path)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_transparent_rgba(self):
        path = self.create_image("RGBA", alpha_pattern=lambda x, y: 0 if x == 0 else 255)
        result = self.run_script(path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rgb_without_alpha(self):
        path = self.create_image("RGB")
        result = self.run_script(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("alpha", result.stdout.lower())

    def test_rgba_fully_opaque(self):
        path = self.create_image("RGBA", alpha_pattern=lambda x, y: 255)
        result = self.run_script(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fully opaque", result.stdout.lower())

    def test_rgba_fully_transparent(self):
        path = self.create_image("RGBA", alpha_pattern=lambda x, y: 0)
        result = self.run_script(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fully transparent", result.stdout.lower())

    def test_rgba_with_partial_transparency(self):
        path = self.create_image("RGBA", alpha_pattern=lambda x, y: 128 if x == y else 255)
        result = self.run_script(path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("semi-transparent", result.stdout.lower())
