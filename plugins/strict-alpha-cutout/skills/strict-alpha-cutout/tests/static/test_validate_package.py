import ast
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = PACKAGE_ROOT / "scripts" / "validate_package.py"


class StrictAlphaPackageTest(unittest.TestCase):
    def copy_package(self, name: str = "strict-alpha-cutout") -> Path:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        target = Path(tempdir.name) / name
        shutil.copytree(PACKAGE_ROOT, target)
        for cache in target.rglob("__pycache__"):
            shutil.rmtree(cache)
        for pyc in target.rglob("*.pyc"):
            pyc.unlink()
        return target

    def run_validator(self, root: Path):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(root)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_package(self):
        root = self.copy_package()
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_skill_md_is_rejected(self):
        root = self.copy_package()
        (root / "SKILL.md").unlink()
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SKILL.md", result.stdout)

    def test_wrong_package_name_is_rejected(self):
        root = self.copy_package("wrong-name")
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("strict-alpha-cutout", result.stdout)

    def test_version_mismatch_is_rejected(self):
        root = self.copy_package()
        skill = (root / "SKILL.md").read_text(encoding="utf-8").replace('version: "0.2.0"', 'version: "9.9.9"')
        (root / "SKILL.md").write_text(skill, encoding="utf-8")
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("metadata.version", result.stdout)

    def test_image_artifact_is_rejected(self):
        root = self.copy_package()
        (root / "sample.png").write_bytes(b"not-an-image")
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sample.png", result.stdout)

    def test_runtime_cache_is_rejected(self):
        root = self.copy_package()
        cache = root / "tests" / "static" / "__pycache__"
        cache.mkdir(parents=True)
        (cache / "x.pyc").write_bytes(b"cache")
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("runtime cache", result.stdout)

    def test_strict_binary_contract_is_present(self):
        skill = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("every background pixel must have alpha exactly `0`", skill)
        self.assertIn("every preserved foreground pixel must have alpha exactly `255`", skill)
        self.assertIn("any alpha value from `1` through `254` is a failure", skill)
        self.assertIn("Do not silently switch modes.", skill)

    def test_chat_only_attribution_contract(self):
        skill = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Chat-Only Attribution", skill)
        self.assertIn("Przygotowane przez [MorenaTech.work](https://morenatech.work/)", skill)
        self.assertIn("never include the attribution line in the image-generation or image-editing prompt", skill)
        self.assertIn("https://morenatech.work/", skill)
        self.assertIn("https://morenatech.work/", skill)

    def test_image_tool_prompt_explicitly_forbids_branding(self):
        skill = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Tool Prompt Boundary", skill)
        self.assertIn("Do not add any logo, watermark, badge, text, signature, URL, QR code, frame, border, branding, promotional element, new object, new accessory, or new background.", skill)
        self.assertIn("Never copy creator attribution or promotional text into the image-generation or image-editing prompt.", skill)

    def test_no_promotional_cta(self):
        skill = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("do not add a CTA, recommendation, sales copy", skill)
        self.assertNotIn("similar automations", skill.lower())
        self.assertNotIn("podobnych automatyzacji", skill.lower())

    def test_python_scripts_parse(self):
        for relative in ["scripts/inspect_alpha.py", "scripts/canonicalize_alpha.py", "scripts/validate_package.py"]:
            source = (PACKAGE_ROOT / relative).read_text(encoding="utf-8")
            ast.parse(source, filename=relative)

    def test_negative_examples_cover_prompt_leakage(self):
        negative = (PACKAGE_ROOT / "examples" / "negative-examples.md").read_text(encoding="utf-8")
        self.assertIn("creator attribution is copied into the image-generation or image-editing prompt", negative)
        self.assertIn("MorenaTech logo, watermark, badge, URL, creator credit, frame, or promotional message", negative)


if __name__ == "__main__":
    unittest.main()
