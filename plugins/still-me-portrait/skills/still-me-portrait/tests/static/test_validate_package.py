import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
VALIDATE_SCRIPT = PACKAGE_ROOT / "scripts" / "validate_package.py"


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_base_package(root: Path) -> None:
    for relative in [
        "references",
        "examples",
        "tests/static",
        "scripts",
    ]:
        (root / relative).mkdir(parents=True, exist_ok=True)

    write_file(
        root / "SKILL.md",
        textwrap.dedent(
            """\
            ---
            name: still-me-portrait
            description: Conservatively retouch and edit an existing portrait while preserving identity and natural features across supported portrait cleanup workflows.
            compatibility: Requires an agent client with image-editing support.
            metadata:
              author: MorenaTech
              version: "0.2.0"
            ---

            See [reference](references/identity-preservation.md).
            """
        ),
    )
    write_file(root / "README.md", "Read [skill](SKILL.md).\n")
    write_file(
        root / "CHANGELOG.md",
        "## 0.2.0 - Unreleased\n\n- Initial release.\n",
    )
    write_file(root / "references/identity-preservation.md", "# Identity\n")
    write_file(root / "references/edit-mode-contracts.md", "# Modes\n")
    write_file(root / "references/quality-checklist.md", "# Quality\n")
    write_file(root / "references/failure-taxonomy.md", "# Failures\n")
    write_file(root / "references/privacy-and-safety.md", "# Privacy\n")
    write_file(root / "examples/starter-prompts.md", "# Prompts\n")
    write_file(root / "examples/positive-examples.md", "# Positive\n")
    write_file(root / "examples/negative-examples.md", "# Negative\n")
    write_file(root / "tests/README.md", "# Tests\n")
    write_file(root / "tests/manual-results-template.md", "# Manual\n")
    write_file(root / "tests/static/__init__.py", "# Init\n")
    write_file(root / "tests/static/test_validate_package.py", "# placeholder test file\n")
    write_file(root / "tests/static/test_verify_alpha.py", "# placeholder alpha test file\n")
    write_file(root / "scripts/validate_package.py", "# placeholder validator\n")
    write_file(root / "scripts/verify_alpha.py", "# placeholder alpha verifier\n")
    write_file(root / "scripts/generate_test_report.py", "# placeholder report generator\n")
    write_file(root / "requirements-optional.txt", "Pillow==10.4.0\n")
    write_file(
        root / "tests/case-schema.json",
        json.dumps(
            {
                "required": [
                    "id",
                    "title",
                    "mode",
                    "input_asset",
                    "user_prompt_pl",
                    "user_prompt_en",
                    "must_preserve",
                    "may_change",
                    "must_not_add",
                    "expected_behavior",
                    "expected_output",
                    "risk_notes",
                ]
            }
        ),
    )

    cases = []
    for index in range(1, 15):
        case_id = f"T{index:02d}"
        cases.append(
            {
                "id": case_id,
                "title": f"Case {case_id}",
                "mode": "natural-retouch",
                "input_asset": None,
                "user_prompt_pl": f"Polish prompt {case_id}",
                "user_prompt_en": f"English prompt {case_id}",
                "must_preserve": ["identity"],
                "may_change": ["light"],
                "must_not_add": ["text"],
                "expected_behavior": "edit",
                "expected_output": {"count": 1, "transparent": False},
                "risk_notes": ["identity_drift"],
            }
        )
    write_file(root / "tests/cases.json", json.dumps(cases))


class ValidatePackageTest(unittest.TestCase):
    maxDiff = None

    def run_validator(self, package_root: Path):
        return subprocess.run(
            [sys.executable, str(VALIDATE_SCRIPT), str(package_root)],
            capture_output=True,
            text=True,
            check=False,
        )

    def with_package(self, mutator=None):
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        root = Path(tempdir.name) / "still-me-portrait"
        build_base_package(root)
        if mutator:
            mutator(root)
        return root

    def test_valid_package(self):
        root = self.with_package()
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_skill_md(self):
        root = self.with_package(lambda p: (p / "SKILL.md").unlink())
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SKILL.md", result.stdout)

    def test_invalid_name(self):
        def mutate(root: Path):
            write_file(root / "SKILL.md", (root / "SKILL.md").read_text(encoding="utf-8").replace("still-me-portrait", "wrong-name", 1))

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("name", result.stdout)

    def test_missing_description(self):
        def mutate(root: Path):
            write_file(
                root / "SKILL.md",
                textwrap.dedent(
                    """\
                    ---
                    name: still-me-portrait
                    compatibility: Requires an agent client.
                    metadata:
                      author: MorenaTech
                      version: "0.2.0"
                    ---
                    """
                ),
            )

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("description", result.stdout)

    def test_broken_relative_link(self):
        def mutate(root: Path):
            write_file(root / "README.md", "Broken [link](references/missing.md)\n")

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing.md", result.stdout)

    def test_over_500_lines(self):
        def mutate(root: Path):
            lines = ["---", "name: still-me-portrait", "description: long enough description for tests.", "compatibility: ok", 'metadata:', '  author: MorenaTech', '  version: "0.2.0"', "---"]
            lines.extend("line" for _ in range(501))
            write_file(root / "SKILL.md", "\n".join(lines) + "\n")

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("500", result.stdout)

    def test_invalid_cases_json(self):
        root = self.with_package(lambda p: write_file(p / "tests/cases.json", "{"))
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cases.json", result.stdout)

    def test_missing_test_case(self):
        def mutate(root: Path):
            cases = json.loads((root / "tests/cases.json").read_text(encoding="utf-8"))
            cases = [case for case in cases if case["id"] != "T14"]
            write_file(root / "tests/cases.json", json.dumps(cases))

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("T14", result.stdout)

    def test_image_file_accidentally_included(self):
        def mutate(root: Path):
            (root / "sample.png").write_bytes(b"png")

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sample.png", result.stdout)

    def test_probable_secret(self):
        def mutate(root: Path):
            fake_secret = "sk-" + "test-" + "1234567890abcdef"
            write_file(root / "README.md", f"Key {fake_secret}\n")

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("secret", result.stdout.lower())

    def test_absolute_private_path(self):
        def mutate(root: Path):
            private_path = "C:" + "\\" + "Users" + "\\" + "Name" + "\\" + "photo.png"
            write_file(root / "examples/positive-examples.md", f"Private path {private_path}\n")

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("absolute private path", result.stdout.lower())

    def test_version_mismatch(self):
        def mutate(root: Path):
            write_file(
                root / "CHANGELOG.md",
                "## 9.9.9 - Unreleased\n\n- Different version.\n",
            )

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("CHANGELOG", result.stdout)
    def test_chat_only_attribution_contract(self):
        skill = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Chat-Only Attribution", skill)
        self.assertIn("Przygotowane przez [MorenaTech.work](https://morenatech.work/)", skill)
        self.assertIn("never add MorenaTech branding", skill)
        self.assertIn("never include the attribution line in the image-generation or image-editing prompt", skill)
        self.assertIn("do not add a CTA, recommendation, sales copy", skill)
        self.assertIn("https://morenatech.work/", skill)
