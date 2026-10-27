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
    for relative in ["references", "examples", "tests/static", "scripts"]:
        (root / relative).mkdir(parents=True, exist_ok=True)

    write_file(
        root / "SKILL.md",
        textwrap.dedent(
            """\
            ---
            name: room-rescue
            description: Restyle, declutter, brighten, and visually refresh an existing room while preserving real geometry, fixed elements, and layout across no-remodel room update workflows.
            compatibility: Requires an agent client with image-editing support.
            metadata:
              author: MorenaTech
              version: "0.2.0"
            ---

            See [reference](references/architecture-preservation.md).
            """
        ),
    )
    write_file(root / "README.md", "Read [skill](SKILL.md).\n")
    write_file(root / "CHANGELOG.md", "## 0.2.0 - Unreleased\n\n- Initial release.\n")
    write_file(root / "references/architecture-preservation.md", "# Architecture\n")
    write_file(root / "references/edit-modes.md", "# Modes\n")
    write_file(root / "references/small-space-rules.md", "# Small spaces\n")
    write_file(root / "references/quality-checklist.md", "# Quality\n")
    write_file(root / "references/failure-taxonomy.md", "# Failures\n")
    write_file(root / "references/realism-and-safety.md", "# Safety\n")
    write_file(root / "references/privacy.md", "# Privacy\n")
    write_file(root / "examples/starter-prompts.md", "# Prompts\n")
    write_file(root / "examples/positive-examples.md", "# Positive\n")
    write_file(root / "examples/negative-examples.md", "# Negative\n")
    write_file(root / "tests/README.md", "# Tests\n")
    write_file(root / "tests/manual-results-template.md", "# Manual\n")
    write_file(root / "tests/static/__init__.py", "# Init\n")
    write_file(root / "tests/static/test_validate_package.py", "# placeholder test file\n")
    write_file(root / "scripts/validate_package.py", "# placeholder validator\n")
    write_file(root / "scripts/generate_test_report.py", "# placeholder report generator\n")
    write_file(root / "requirements-optional.txt", "# none\n")
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
                "mode": "declutter-and-brighten",
                "input_asset": None,
                "user_prompt_pl": f"Polish prompt {case_id}",
                "user_prompt_en": f"English prompt {case_id}",
                "must_preserve": ["room_geometry"],
                "may_change": ["lighting"],
                "must_not_add": ["extra_space"],
                "expected_behavior": "edit",
                "expected_output": {"count": 1, "transparent": False},
                "risk_notes": ["architecture_drift"],
            }
        )
    cases[0]["must_preserve"] = [
        "room_geometry",
        "camera_viewpoint",
        "windows",
        "cabinetry_layout",
        "sink_position",
        "cooker_position",
        "floor",
        "table_position",
        "circulation_width",
        "cabinet_color",
        "countertops",
        "wide_angle_distortion",
    ]
    cases[0]["must_not_add"] = ["extra_space", "straightened_perspective"]
    write_file(root / "tests/cases.json", json.dumps(cases))


class ValidatePackageTest(unittest.TestCase):
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
        root = Path(tempdir.name) / "room-rescue"
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
            write_file(root / "SKILL.md", (root / "SKILL.md").read_text(encoding="utf-8").replace("room-rescue", "wrong-name", 1))

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
                    name: room-rescue
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

    def test_over_500_lines(self):
        def mutate(root: Path):
            lines = ["---", "name: room-rescue", "description: long enough description for tests.", "compatibility: ok", "metadata:", "  author: MorenaTech", '  version: "0.2.0"', "---"]
            lines.extend("line" for _ in range(501))
            write_file(root / "SKILL.md", "\n".join(lines) + "\n")

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("500", result.stdout)

    def test_broken_link(self):
        root = self.with_package(lambda p: write_file(p / "README.md", "Broken [link](references/missing.md)\n"))
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing.md", result.stdout)

    def test_invalid_json(self):
        root = self.with_package(lambda p: write_file(p / "tests/cases.json", "{"))
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cases.json", result.stdout)

    def test_missing_t01(self):
        def mutate(root: Path):
            cases = json.loads((root / "tests/cases.json").read_text(encoding="utf-8"))
            write_file(root / "tests/cases.json", json.dumps(cases[1:]))

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("T01", result.stdout)

    def test_missing_t14(self):
        def mutate(root: Path):
            cases = json.loads((root / "tests/cases.json").read_text(encoding="utf-8"))
            write_file(root / "tests/cases.json", json.dumps(cases[:-1]))

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("T14", result.stdout)

    def test_image_in_repo(self):
        def mutate(root: Path):
            (root / "sample.png").write_bytes(b"png")

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sample.png", result.stdout)

    def test_private_path(self):
        def mutate(root: Path):
            private_path = "C:" + "\\" + "Users" + "\\" + "Name" + "\\" + "room.jpg"
            write_file(root / "examples/positive-examples.md", private_path)

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("private path", result.stdout.lower())

    def test_probable_secret(self):
        def mutate(root: Path):
            fake_secret = "sk-" + "test-" + "1234567890abcdef"
            write_file(root / "README.md", fake_secret)

        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("secret", result.stdout.lower())

    def test_version_mismatch(self):
        root = self.with_package(lambda p: write_file(p / "CHANGELOG.md", "## 9.9.9 - Unreleased\n"))
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("CHANGELOG", result.stdout)

    def test_failure_categories_present(self):
        failures = (PACKAGE_ROOT / "references/failure-taxonomy.md").read_text(encoding="utf-8")
        self.assertIn("architecture_drift", failures)
        self.assertIn("space_expansion", failures)
        self.assertIn("geometry_drift", failures)
        self.assertIn("perspective_correction_drift", failures)
        self.assertIn("room_width_drift", failures)
        self.assertIn("layout_drift", failures)
        self.assertIn("cabinet_replacement", failures)
        self.assertIn("cabinet_recolor_without_request", failures)
        self.assertIn("camera_viewpoint_drift", failures)
        self.assertIn("fixed_installation_drift", failures)
        self.assertIn("fixed_fixture_replacement", failures)
        self.assertIn("catalog_redesign_drift", failures)
        self.assertIn("renovation_overreach", failures)

    def test_t01_geometry_preservation_present(self):
        cases = json.loads((PACKAGE_ROOT / "tests/cases.json").read_text(encoding="utf-8"))
        t01 = next(case for case in cases if case["id"] == "T01")
        self.assertIn("room_geometry", t01["must_preserve"])
        self.assertIn("camera_viewpoint", t01["must_preserve"])
        self.assertIn("cabinet_color", t01["must_preserve"])
        self.assertIn("countertops", t01["must_preserve"])
        self.assertIn("wide_angle_distortion", t01["must_preserve"])
        self.assertIn("straightened_perspective", t01["must_not_add"])

    def test_skill_contains_same_room_contract(self):
        skill = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Same Room / Same Geometry Contract", skill)
        self.assertIn("preserve exact framing", skill)
        self.assertIn("preserve wide-angle distortion", skill)
        self.assertIn("Do not widen the room.", skill)
        self.assertIn("Do not change cabinet color.", skill)

    def test_manual_template_contains_new_gate_questions(self):
        template = (PACKAGE_ROOT / "tests/manual-results-template.md").read_text(encoding="utf-8")
        self.assertIn("Classification:", template)
        self.assertIn("Same width and depth:", template)
        self.assertIn("Same framing and perspective:", template)
        self.assertIn("Not a remodel or catalog redesign:", template)

    def test_manual_case_txx_documented(self):
        tests_readme = (PACKAGE_ROOT / "tests/README.md").read_text(encoding="utf-8")
        self.assertIn("TXX Narrow Kitchen No Renovation", tests_readme)
        self.assertIn("brown cabinets", tests_readme)
        self.assertIn("catalog renovation", tests_readme)
    def test_chat_only_attribution_contract(self):
        skill = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Chat-Only Attribution", skill)
        self.assertIn("Przygotowane przez [MorenaTech.work](https://morenatech.work/)", skill)
        self.assertIn("never add MorenaTech branding", skill)
        self.assertIn("never include the attribution line in the image-generation or image-editing prompt", skill)
        self.assertIn("do not add a CTA, recommendation, sales copy", skill)
        self.assertIn("https://morenatech.work/", skill)
