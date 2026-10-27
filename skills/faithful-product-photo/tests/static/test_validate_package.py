import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validate_package.py"


class PackageValidationTests(unittest.TestCase):
    def run_validator(self, package_root: Path):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(package_root)],
            text=True,
            capture_output=True,
            check=False,
        )

    def clone_package(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        dst = Path(td.name) / "faithful-product-photo"
        shutil.copytree(
            ROOT,
            dst,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "generated-manual-report.md"),
        )
        return dst

    def test_validator_passes_for_repository_package(self):
        proc = self.run_validator(ROOT)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("16 text-only behavioral cases", proc.stdout)

    def test_contract_phrases_present(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for phrase in [
            "Remove the scene, not the evidence.",
            "component ownership",
            "catalog-reconstruction",
            "USB-C Regression Rule",
            "fail closed",
        ]:
            self.assertIn(phrase.lower(), skill.lower())

    def test_success_attribution_contract(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(
            "Przygotowane przez [MorenaTech.work](https://morenatech.work/)",
            skill,
        )
        self.assertIn(
            "complete, successfully validated result",
            skill,
        )
        self.assertIn(
            "final line of the assistant's response",
            skill,
        )
        self.assertIn(
            "do not show it for a failed, incomplete, partial",
            skill,
        )
    def test_reference_files_exist(self):
        for name in [
            "product-integrity.md",
            "background-removal-contract.md",
            "packaging-and-text.md",
            "uncertainty-and-occlusion.md",
            "quality-gate.md",
            "failure-taxonomy.md",
            "privacy-and-rights.md",
        ]:
            self.assertTrue((ROOT / "references" / name).is_file(), name)

    def test_usb_case_contains_ownership_risk(self):
        cases = json.loads((ROOT / "tests/cases.json").read_text(encoding="utf-8"))
        t02 = next(case for case in cases if case["id"] == "T02")
        self.assertIn("connector_ownership", t02["must_preserve"])
        self.assertIn("F07", t02["risk_notes"])

    def test_occlusion_case_forbids_completion(self):
        cases = json.loads((ROOT / "tests/cases.json").read_text(encoding="utf-8"))
        t11 = next(case for case in cases if case["id"] == "T11")
        self.assertIn("invented_second_end", t11["must_not_add"])
        self.assertIn("F12", t11["risk_notes"])

    def test_missing_required_file_fails(self):
        root = self.clone_package()
        (root / "references/product-integrity.md").unlink()
        proc = self.run_validator(root)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("product-integrity.md", proc.stdout)

    def test_invalid_frontmatter_name_fails(self):
        root = self.clone_package()
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        (root / "SKILL.md").write_text(skill.replace("name: faithful-product-photo", "name: wrong-name", 1), encoding="utf-8")
        proc = self.run_validator(root)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("frontmatter name", proc.stdout)

    def test_broken_relative_link_fails(self):
        root = self.clone_package()
        with (root / "README.md").open("a", encoding="utf-8") as fh:
            fh.write("\n[broken](references/does-not-exist.md)\n")
        proc = self.run_validator(root)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("broken relative link", proc.stdout)

    def test_missing_case_fails(self):
        root = self.clone_package()
        cases_path = root / "tests/cases.json"
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
        cases_path.write_text(json.dumps(cases[:-1]), encoding="utf-8")
        proc = self.run_validator(root)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("case IDs mismatch", proc.stdout)

    def test_non_null_public_test_asset_fails(self):
        root = self.clone_package()
        cases_path = root / "tests/cases.json"
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
        cases[0]["input_asset"] = "photo.jpg"
        cases_path.write_text(json.dumps(cases), encoding="utf-8")
        proc = self.run_validator(root)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("input_asset null", proc.stdout)

    def test_private_machine_path_fails(self):
        root = self.clone_package()
        with (root / "examples/positive-examples.md").open("a", encoding="utf-8") as fh:
            private_path = "C:" + "\\" + "Users" + "\\" + "Example" + "\\" + "product.jpg"
            fh.write("\n" + private_path + "\n")
        proc = self.run_validator(root)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("machine-specific user path", proc.stdout)

    def test_raster_product_image_in_package_fails(self):
        root = self.clone_package()
        (root / "sample-product.png").write_bytes(b"not-an-image")
        proc = self.run_validator(root)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("must not bundle user/product raster images", proc.stdout)

    def test_generated_python_cache_is_ignored(self):
        root = self.clone_package()
        cache = root / "tests/static/__pycache__"
        cache.mkdir(parents=True, exist_ok=True)
        (cache / "x.pyc").write_bytes(b"cache")
        proc = self.run_validator(root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
