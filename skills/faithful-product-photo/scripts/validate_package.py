#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

EXPECTED_NAME = "faithful-product-photo"
EXPECTED_VERSION = "0.2.0"
EXPECTED_CASE_IDS = {f"T{index:02d}" for index in range(1, 17)}

REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "requirements-optional.txt",
    "agents/openai.yaml",
    "assets/icon.svg",
    "references/product-integrity.md",
    "references/background-removal-contract.md",
    "references/packaging-and-text.md",
    "references/uncertainty-and-occlusion.md",
    "references/quality-gate.md",
    "references/failure-taxonomy.md",
    "references/privacy-and-rights.md",
    "examples/starter-prompts.md",
    "examples/positive-examples.md",
    "examples/negative-examples.md",
    "examples/usb-c-regression.md",
    "tests/README.md",
    "tests/cases.json",
    "tests/case-schema.json",
    "tests/manual-results-template.md",
    "tests/static/__init__.py",
    "tests/static/test_validate_package.py",
    "tests/static/test_inspect_alpha.py",
    "scripts/validate_package.py",
    "scripts/inspect_alpha.py",
    "scripts/generate_test_report.py",
]

TEXT_EXTENSIONS = {".md", ".json", ".txt", ".yml", ".yaml", ".py", ".svg"}
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9-]{10,}"),
    re.compile(r"ghp_[A-Za-z0-9]{10,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
]
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTO" + r"DO\b"),
    re.compile(r"\bTB" + r"D\b"),
]
ABSOLUTE_USER_PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:\\Users\\"),
    re.compile(r"/" + "Users/"),
    re.compile(r"/" + "home/" + r"[^/\s]+/"),
]


class ValidationError(Exception):
    pass


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{path}: invalid UTF-8 ({exc})") from exc


def parse_frontmatter(skill_path: Path):
    text = read_text(skill_path)
    if not text.startswith("---\n"):
        raise ValidationError("SKILL.md: missing YAML frontmatter")
    closing = text.find("\n---\n", 4)
    if closing == -1:
        raise ValidationError("SKILL.md: frontmatter not closed")
    frontmatter = text[4:closing]
    data = {}
    for line in frontmatter.splitlines():
        if not line or line.startswith("  "):
            continue
        if ":" not in line:
            raise ValidationError(f"SKILL.md: invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data, text[closing + 5:], text


def validate_links(md_path: Path, root: Path):
    text = read_text(md_path)
    for link in MARKDOWN_LINK_PATTERN.findall(text):
        target = link.strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "://" in target:
            continue
        target = target.split("#", 1)[0]
        resolved = (md_path.parent / target).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError as exc:
            raise ValidationError(f"{md_path}: link points outside package: {target}") from exc
        if not resolved.exists():
            raise ValidationError(f"{md_path}: broken relative link: {target}")


def validate_cases(root: Path):
    cases = json.loads(read_text(root / "tests/cases.json"))
    schema = json.loads(read_text(root / "tests/case-schema.json"))
    if not isinstance(cases, list):
        raise ValidationError("tests/cases.json must be an array")
    required = schema.get("required")
    if not isinstance(required, list) or not required:
        raise ValidationError("tests/case-schema.json missing required fields")

    ids = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValidationError("each test case must be an object")
        missing = [key for key in required if key not in case]
        if missing:
            raise ValidationError(f"{case.get('id')}: missing {missing}")
        case_id = case["id"]
        if not re.fullmatch(r"T[0-9]{2}", case_id):
            raise ValidationError(f"invalid case id: {case_id}")
        if case_id in ids:
            raise ValidationError(f"duplicate case id: {case_id}")
        ids.add(case_id)
        if case["input_asset"] is not None:
            raise ValidationError(f"{case_id}: public tests must keep input_asset null")
        if not isinstance(case["expected_output"], dict):
            raise ValidationError(f"{case_id}: expected_output must be object")
        if not case["risk_notes"]:
            raise ValidationError(f"{case_id}: risk_notes must not be empty")

    if ids != EXPECTED_CASE_IDS:
        raise ValidationError(f"case IDs mismatch: got {sorted(ids)} expected {sorted(EXPECTED_CASE_IDS)}")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = []

    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            errors.append(f"missing required path: {rel}")

    try:
        fm, body, full = parse_frontmatter(root / "SKILL.md")
        if fm.get("name") != EXPECTED_NAME:
            errors.append(f"frontmatter name must be {EXPECTED_NAME}")
        if full.count("\n") + 1 > 500:
            errors.append("SKILL.md exceeds 500 lines")
        metadata_match = re.search(r'(?m)^\s+version:\s+"?([^"\n]+)"?\s*$', full)
        version = metadata_match.group(1) if metadata_match else None
        if version != EXPECTED_VERSION:
            errors.append(f"metadata.version must be {EXPECTED_VERSION}, got {version!r}")
        required_phrases = [
            "Remove the scene, not the evidence.",
            "connector ownership",
            "fail closed",
            "real alpha",
            "catalog-reconstruction",
            "USB-C Regression Rule",
        ]
        for phrase in required_phrases:
            if phrase.lower() not in full.lower():
                errors.append(f"SKILL.md missing policy phrase: {phrase}")
    except (ValidationError, FileNotFoundError) as exc:
        errors.append(str(exc))

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}:
            errors.append(f"public package must not bundle user/product raster images: {path.relative_to(root)}")
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS:
            try:
                text = read_text(path)
            except ValidationError as exc:
                errors.append(str(exc))
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f"{path.relative_to(root)}: possible secret")
            for pattern in PLACEHOLDER_PATTERNS:
                if pattern.search(text):
                    errors.append(f"{path.relative_to(root)}: unresolved placeholder")
            for pattern in ABSOLUTE_USER_PATH_PATTERNS:
                if pattern.search(text):
                    errors.append(f"{path.relative_to(root)}: machine-specific user path")
            if path.suffix.lower() == ".md":
                try:
                    validate_links(path, root)
                except ValidationError as exc:
                    errors.append(str(exc))

    try:
        validate_cases(root)
    except (ValidationError, json.JSONDecodeError) as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: {EXPECTED_NAME} package {EXPECTED_VERSION}")
    print(f"PASS: {len(REQUIRED_PATHS)} required paths")
    print(f"PASS: {len(EXPECTED_CASE_IDS)} text-only behavioral cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
