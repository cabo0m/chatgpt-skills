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
    for relative in ["references", "examples", "tests/static", "scripts", "agents"]:
        (root / relative).mkdir(parents=True, exist_ok=True)

    write_file(
        root / "SKILL.md",
        textwrap.dedent(
            """\
            ---
            name: old-photo-revival
            description: Restore, repair, colorize, and naturally revive an existing old photograph while preserving recognizable identity, age, expression, pose, and historical character across conservative restoration workflows.
            compatibility: Requires an agent client with image-editing support.
            metadata:
              author: MorenaTech
              version: "0.2.0"
            ---

            See [reference](references/identity-preservation.md).

            ## Failure Policy
            Fail closed after one correction anchored to the original source image.

            ## Chat-Only Attribution
            After a complete, successfully validated result: `Przygotowane przez [MorenaTech.work](https://morenatech.work/)`
            """
        ),
    )
    write_file(root / "README.md", "Read [skill](SKILL.md).\n")
    write_file(root / "CHANGELOG.md", "## 0.2.0 - 2026-10-27\n\n- Initial release.\n")
    write_file(root / "references/restoration-modes.md", "# Modes\n")
    write_file(root / "references/identity-preservation.md", "# Identity\n")
    write_file(root / "references/reconstruction-and-uncertainty.md", "# Uncertainty\n")
    write_file(root / "references/colorization-guidelines.md", "# Color\n")
    write_file(root / "references/quality-checklist.md", "# Quality\n")
    write_file(root / "references/failure-taxonomy.md", "# Failures\n")
    write_file(root / "references/privacy-and-rights.md", "# Rights\n")
    write_file(root / "examples/starter-prompts.md", "# Prompts\n")
    write_file(root / "examples/positive-examples.md", "# Positive\n")
    write_file(root / "examples/negative-examples.md", "# Negative\n")
    write_file(root / "examples/uncertainty-messages.md", "# Uncertainty messages\n")
    write_file(root / "tests/README.md", "# Tests\n")
    write_file(
        root / "tests/manual-results-template.md",
        "\n".join(
            [
                "# Manual",
                "- colorization_strength:",
                "- local_color_separation_score:",
                "- neutral_balance_score:",
                "- skin_color_naturalness_score:",
                "- colorization_quality_score:",
                "- sepia_color_collapse:",
                "- estimated_colors_disclosed:",
                "- suitable_as_restore_only:",
                "- suitable_as_faithful_colorization:",
                "",
            ]
        ),
    )
    write_file(root / "tests/static/__init__.py", "# Init\n")
    write_file(root / "tests/static/test_validate_package.py", "# placeholder test file\n")
    write_file(root / "tests/static/test_inspect_image.py", "# placeholder image test file\n")
    write_file(root / "scripts/validate_package.py", "# placeholder validator\n")
    write_file(root / "scripts/inspect_image.py", "# placeholder inspector\n")
    write_file(root / "scripts/generate_test_report.py", "# placeholder report generator\n")
    write_file(root / "requirements-optional.txt", "Pillow==12.3.0\n")
    write_file(
        root / "agents/openai.yaml",
        "interface:\n  display_name: Old Photo Revival\npolicy:\n  allow_implicit_invocation: true\n  products:\n  - chatgpt\n",
    )
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
                "mode": "faithful-colorization" if case_id == "T10" else "restore-only",
                "input_asset": None,
                "user_prompt_pl": f"Polish prompt {case_id}",
                "user_prompt_en": f"English prompt {case_id}",
                "must_preserve": ["identity"] if case_id != "T10" else ["identity", "historical_character"],
                "may_change": ["damage_cleanup"] if case_id != "T10" else ["estimated_skin_tones", "local_color_separation", "neutral_balance", "natural_saturation"],
                "must_not_add": ["text"] if case_id != "T10" else ["uniform_warm_filter", "modern_makeup", "text"],
                "expected_behavior": "edit" if case_id != "T10" else "ask_about_known_colors_then_colorize_with_uncertainty_and_local_separation",
                "expected_output": {"count": 1, "transparent": False},
                "risk_notes": ["identity_drift"] if case_id != "T10" else ["sepia_color_collapse", "neutral_tone_loss", "local_color_separation_failure", "false_color_certainty", "beauty_model_drift"],
            }
        )
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
        root = Path(tempdir.name) / "old-photo-revival"
        build_base_package(root)
        if mutator:
            mutator(root)
        return root

    def test_valid_package(self):
        root = self.with_package()
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        manual_template = (root / "tests/manual-results-template.md").read_text(encoding="utf-8")
        self.assertIn("colorization_strength", manual_template)
        self.assertIn("local_color_separation_score", manual_template)
        self.assertIn("neutral_balance_score", manual_template)
        self.assertIn("skin_color_naturalness_score", manual_template)
        self.assertIn("colorization_quality_score", manual_template)
        self.assertIn("sepia_color_collapse", manual_template)
        self.assertIn("suitable_as_faithful_colorization", manual_template)

        cases = json.loads((root / "tests/cases.json").read_text(encoding="utf-8"))
        t10 = next(case for case in cases if case["id"] == "T10")
        self.assertIn("sepia_color_collapse", t10["risk_notes"])
        self.assertIn("neutral_tone_loss", t10["risk_notes"])
        self.assertIn("local_color_separation_failure", t10["risk_notes"])

    def test_colorization_contract_presence(self):
        skill = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("COLORIZATION MUST PRESERVE", skill)
        self.assertIn("uniform sepia or warm tint", skill)
        self.assertIn("Default strength: `natural`", skill)
        self.assertIn("PRINT NORMALIZATION", skill)
        self.assertIn("one automatic correction", skill)

    def test_colorization_strength_levels_documented(self):
        guidelines = (PACKAGE_ROOT / "references/colorization-guidelines.md").read_text(encoding="utf-8")
        self.assertIn("Default strength is `natural`", guidelines)
        self.assertIn("`conservative`", guidelines)
        self.assertIn("`natural`", guidelines)
        self.assertIn("`vivid`", guidelines)

    def test_uniform_sepia_failure_documented(self):
        failures = (PACKAGE_ROOT / "references/failure-taxonomy.md").read_text(encoding="utf-8")
        self.assertIn("sepia_color_collapse", failures)
        self.assertIn("For `faithful-colorization`, major sepia-color-collapse is an automatic fail", failures)

    def test_uncertainty_guards_remain_present(self):
        uncertainty = (PACKAGE_ROOT / "references/reconstruction-and-uncertainty.md").read_text(encoding="utf-8")
        self.assertIn("estimated", uncertainty.lower())
        self.assertIn("Do not replace uncertainty with uniform warm tinting", uncertainty)

    def test_print_normalization_and_first_pass_rules_documented(self):
        modes = (PACKAGE_ROOT / "references/restoration-modes.md").read_text(encoding="utf-8")
        self.assertIn("normalize photographed paper prints into clean reproductions when needed", modes)
        self.assertIn("explicit colorization request", modes)

        cases = json.loads((PACKAGE_ROOT / "tests/cases.json").read_text(encoding="utf-8"))
        t01 = next(case for case in cases if case["id"] == "T01")
        t10 = next(case for case in cases if case["id"] == "T10")
        self.assertIn("print_normalization_failure", t01["risk_notes"])
        self.assertIn("incomplete_colorization_first_pass", t10["risk_notes"])
        self.assertIn("single_automatic_color_correction_if_first_pass_is_still_sepia", t10["may_change"])

    def test_missing_skill_md(self):
        root = self.with_package(lambda p: (p / "SKILL.md").unlink())
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SKILL.md", result.stdout)

    def test_invalid_frontmatter(self):
        root = self.with_package(lambda p: write_file(p / "SKILL.md", "name: broken\n"))
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("frontmatter", result.stdout.lower())

    def test_invalid_name(self):
        def mutate(root: Path):
            write_file(root / "SKILL.md", (root / "SKILL.md").read_text(encoding="utf-8").replace("old-photo-revival", "wrong-name", 1))
        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("name", result.stdout)

    def test_over_500_lines(self):
        def mutate(root: Path):
            lines = ["---", "name: old-photo-revival", "description: long enough description for tests.", "compatibility: ok", "metadata:", "  author: MorenaTech", '  version: "0.2.0"', "---"]
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

    def test_missing_test_case(self):
        def mutate(root: Path):
            cases = json.loads((root / "tests/cases.json").read_text(encoding="utf-8"))
            write_file(root / "tests/cases.json", json.dumps(cases[:-1]))
        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("T14", result.stdout)

    def test_invalid_json(self):
        root = self.with_package(lambda p: write_file(p / "tests/cases.json", "{"))
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cases.json", result.stdout)

    def test_image_in_repo(self):
        def mutate(root: Path):
            (root / "sample.png").write_bytes(b"png")
        root = self.with_package(mutate)
        result = self.run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sample.png", result.stdout)

    def test_private_path(self):
        def mutate(root: Path):
            private_path = "C:" + "\\" + "Users" + "\\" + "Name" + "\\" + "photo.jpg"
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

    def test_chat_only_attribution_contract(self):
        skill = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        lower = skill.lower()
        self.assertIn("## Chat-Only Attribution", skill)
        self.assertIn("Przygotowane przez [MorenaTech.work](https://morenatech.work/)", skill)
        self.assertIn("complete, successfully validated result", lower)
        self.assertIn("final line of the chat response", lower)
        self.assertIn("never show it before invoking", lower)
        self.assertIn("do not show it for a failed, incomplete, partial", lower)
        self.assertIn("never add morenatech branding", lower)
        self.assertIn("never copy this attribution instruction", lower)

    def test_failure_policy_is_fail_closed_and_original_anchored(self):
        skill = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        lower = skill.lower()
        self.assertIn("## Failure Policy", skill)
        self.assertIn("fail closed", lower)
        self.assertIn("anchored to the original source image", lower)
        self.assertIn("do not chain a new edit from the failed output alone", lower)
        self.assertIn("never continue iterative regeneration", lower)

    def test_openai_agent_metadata_exists(self):
        metadata = (PACKAGE_ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("display_name: Old Photo Revival", metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertIn("- chatgpt", metadata)
