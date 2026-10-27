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
INSPECT_SCRIPT = PACKAGE_ROOT / "scripts" / "inspect_image.py"


class InspectImageNoPillowTest(unittest.TestCase):
    def test_missing_pillow_message(self):
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        image_path = Path(tempdir.name) / "plain.bin"
        image_path.write_bytes(b"demo")
        code = f"""
import builtins
import runpy
import sys

real_import = builtins.__import__

def fake_import(name, *args, **kwargs):
    if name == "PIL":
        raise ImportError("blocked")
    return real_import(name, *args, **kwargs)

builtins.__import__ = fake_import
sys.argv = ["inspect_image.py", r"{image_path}"]
runpy.run_path(r"{INSPECT_SCRIPT}", run_name="__main__")
"""
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Pillow is required", result.stdout + result.stderr)


@unittest.skipIf(Image is None, "Pillow is required for image inspection tests")
class InspectImageTest(unittest.TestCase):
    def create_image(self, mode, size=(400, 300), exif_orientation=None):
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        path = Path(tempdir.name) / "image.png"
        image = Image.new(mode, size, color=128 if mode == "L" else (128, 128, 128, 255) if "A" in mode else (128, 128, 128))
        save_kwargs = {}
        if exif_orientation is not None:
            exif = Image.Exif()
            exif[274] = exif_orientation
            save_kwargs["exif"] = exif
        image.save(path, **save_kwargs)
        return path

    def run_script(self, image_path: Path):
        return subprocess.run(
            [sys.executable, str(INSPECT_SCRIPT), str(image_path)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_reads_grayscale(self):
        result = self.run_script(self.create_image("L"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("grayscale", result.stdout.lower())

    def test_reads_rgb(self):
        result = self.run_script(self.create_image("RGB"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("rgb", result.stdout.lower())

    def test_warns_on_very_small_image(self):
        result = self.run_script(self.create_image("RGB", size=(64, 64)))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("very small", result.stdout.lower())

    def test_reports_exif(self):
        path = self.create_image("RGB", exif_orientation=6)
        result = self.run_script(path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Has EXIF: yes", result.stdout)
        self.assertIn("Orientation: 6", result.stdout)
