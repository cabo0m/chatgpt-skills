import json
import re
import sys
from pathlib import Path


EXPECTED_NAME = "old-photo-revival"
EXPECTED_VERSION = "0.2.0"
EXPECTED_CASE_IDS = {f"T{index:02d}" for index in range(1, 15)}
IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".webp",
    ".tif",
    ".tiff",
    ".svg",
}
TEXT_EXTENSIONS = {
    ".md",
    ".json",
    ".txt",
    ".yml",
    ".yaml",
}
REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "references/restoration-modes.md",
    "references/identity-preservation.md",
    "references/reconstruction-and-uncertainty.md",
    "references/colorization-guidelines.md",
    "references/quality-checklist.md",
    "references/failure-taxonomy.md",
    "references/privacy-and-rights.md",
    "examples/starter-prompts.md",
    "examples/positive-examples.md",
    "examples/negative-examples.md",
    "examples/uncertainty-messages.md",
    "tests/cases.json",
    "tests/case-schema.json",
    "tests/manual-results-template.md",
    "tests/README.md",
    "tests/static/__init__.py",
    "tests/static/test_validate_package.py",
    "tests/static/test_inspect_image.py",
    "scripts/validate_package.py",
    "scripts/inspect_image.py",
    "scripts/generate_test_report.py",
    "requirements-optional.txt",
]
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9-]{10,}"),
    re.compile(r"ghp_[A-Za-z0-9]{10,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
    re.compile(r"api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}", re.IGNORECASE),
]
PLACEHOLDER_PATTERNS = [
    re.compile(r"\b" + "TO" + "DO" + r"\b"),
    re.compile(r"\b" + "TB" + "D" + r"\b"),
    re.compile(r"<" + "insert", re.IGNORECASE),
]
WINDOWS_USERS_PATTERN = re.compile(r"[A-Za-z]:\\Users\\")
UNIX_USERS_PATTERN = re.compile(r"/Users/")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PYCACHE_PATTERN = re.compile(r"__pycache__")


class ValidationError(Exception):
    pass


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{path}: file is not valid UTF-8 ({exc})") from exc


def parse_frontmatter(skill_path: Path):
    text = read_text(skill_path)
    if not text.startswith("---\n"):
        raise ValidationError(f"{skill_path}: missing YAML frontmatter")
    closing = text.find("\n---\n", 4)
    if closing == -1:
        raise ValidationError(f"{skill_path}: frontmatter is not properly closed")

    raw_lines = text[4:closing].splitlines()
    data = {}
    current_parent = None
    for line in raw_lines:
        if not line.strip():
            continue
        if line.startswith("  "):
            if current_parent is None or ":" not in line.strip():
                raise ValidationError(f"{skill_path}: invalid nested frontmatter line '{line}'")
            key, value = [part.strip() for part in line.strip().split(":", 1)]
            data.setdefault(current_parent, {})[key] = value.strip('"')
            continue

        if ":" not in line:
            raise ValidationError(f"{skill_path}: invalid frontmatter line '{line}'")
        key, value = [part.strip() for part in line.split(":", 1)]
        if value:
            data[key] = value.strip('"')
            current_parent = None
        else:
            data[key] = {}
            current_parent = key

    body = text[closing + 5 :]
    return data, body, text


def validate_links(markdown_path: Path, root: Path):
    text = read_text(markdown_path)
    for link in MARKDOWN_LINK_PATTERN.findall(text):
        target = link.strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "://" in target:
            continue
        normalized = target.split("#", 1)[0]
        target_path = (markdown_path.parent / normalized).resolve()
        try:
            target_path.relative_to(root.resolve())
        except ValueError as exc:
            raise ValidationError(f"{markdown_path}: link points outside package: {target}") from exc
        if not target_path.exists():
            raise ValidationError(f"{markdown_path}: broken relative link: {target}")


def validate_cases(cases_path: Path, schema_path: Path):
    try:
        cases = json.loads(read_text(cases_path))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{cases_path}: invalid JSON ({exc})") from exc

    try:
        schema = json.loads(read_text(schema_path))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{schema_path}: invalid JSON ({exc})") from exc

    if not isinstance(cases, list):
        raise ValidationError(f"{cases_path}: expected a JSON array")

    required = schema.get("required")
    if not isinstance(required, list) or not required:
        raise ValidationError(f"{schema_path}: missing or invalid required field list")

    seen_ids = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValidationError(f"{cases_path}: each case must be an object")
        missing = [key for key in required if key not in case]
        if missing:
            raise ValidationError(f"{cases_path}: case missing fields {missing}")
        case_id = case["id"]
        if not isinstance(case_id, str) or not re.fullmatch(r"T[0-9]{2}", case_id):
            raise ValidationError(f"{cases_path}: invalid case id {case_id!r}")
        if case_id in seen_ids:
            raise ValidationError(f"{cases_path}: duplicate case id {case_id}")
        seen_ids.add(case_id)
        if not isinstance(case["expected_output"], dict):
            raise ValidationError(f"{cases_path}: case {case_id} expected_output must be an object")
        if set(case["expected_output"].keys()) != {"count", "transparent"}:
            raise ValidationError(f"{cases_path}: case {case_id} expected_output must contain only count and transparent")
        if not isinstance(case["expected_output"]["count"], int) or case["expected_output"]["count"] < 0:
            raise ValidationError(f"{cases_path}: case {case_id} expected_output.count must be a non-negative integer")
        if not isinstance(case["expected_output"]["transparent"], bool):
            raise ValidationError(f"{cases_path}: case {case_id} expected_output.transparent must be a boolean")
        for key in ["must_preserve", "may_change", "must_not_add", "risk_notes"]:
            if not isinstance(case[key], list):
                raise ValidationError(f"{cases_path}: case {case_id} field {key} must be a list")
        for key in ["title", "mode", "user_prompt_pl", "user_prompt_en", "expected_behavior"]:
            if not isinstance(case[key], str) or len(case[key].strip()) < 3:
                raise ValidationError(f"{cases_path}: case {case_id} field {key} must be a non-empty string")

    missing_ids = sorted(EXPECTED_CASE_IDS - seen_ids)
    if missing_ids:
        raise ValidationError(f"{cases_path}: missing required test cases {', '.join(missing_ids)}")


def validate_changelog(changelog_path: Path):
    changelog_text = read_text(changelog_path)
    expected_header = f"## {EXPECTED_VERSION} -"
    if expected_header not in changelog_text:
        raise ValidationError(f"{changelog_path}: expected changelog header '{expected_header}' matching frontmatter version")


def scan_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in {"SKILL.md", "README.md", "CHANGELOG.md"}:
            continue
        text = read_text(path)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                raise ValidationError(f"{path}: probable secret detected")
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(text):
                raise ValidationError(f"{path}: release placeholder detected")
        if WINDOWS_USERS_PATTERN.search(text) or UNIX_USERS_PATTERN.search(text):
            raise ValidationError(f"{path}: absolute private path detected")


def validate_no_images(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            raise ValidationError(f"{path}: image files are not allowed in v0.1 package")


def validate_no_runtime_cache(root: Path):
    for path in root.rglob("*"):
        if PYCACHE_PATTERN.search(str(path)) or path.suffix.lower() == ".pyc":
            raise ValidationError(f"{path}: runtime cache files are not allowed in the package")


def validate_required_paths(root: Path):
    for relative in REQUIRED_PATHS:
        path = root / relative
        if not path.exists():
            raise ValidationError(f"{path}: required path is missing")


def validate_package(root: Path):
    if not root.exists() or not root.is_dir():
        raise ValidationError(f"{root}: package root does not exist or is not a directory")
    if root.name != EXPECTED_NAME:
        raise ValidationError(f"{root}: package directory name must be {EXPECTED_NAME}")
    validate_required_paths(root)
    validate_no_images(root)
    validate_no_runtime_cache(root)
    skill_path = root / "SKILL.md"
    frontmatter, body, skill_text = parse_frontmatter(skill_path)
    if len(skill_text.splitlines()) > 500:
        raise ValidationError(f"{skill_path}: SKILL.md must be 500 lines or fewer")
    if frontmatter.get("name") != EXPECTED_NAME:
        raise ValidationError(f"{skill_path}: name must be {EXPECTED_NAME}")
    description = frontmatter.get("description", "").strip()
    if len(description) < 40:
        raise ValidationError(f"{skill_path}: description is required and must be descriptive")
    if "guarantee" in description.lower() or "exact reconstruction" in description.lower() or "historically accurate" in description.lower():
        raise ValidationError(f"{skill_path}: description overclaims certainty")
    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        raise ValidationError(f"{skill_path}: metadata block is required")
    if metadata.get("author") != "MorenaTech":
        raise ValidationError(f"{skill_path}: metadata.author must be MorenaTech")
    if metadata.get("version") != EXPECTED_VERSION:
        raise ValidationError(f"{skill_path}: metadata.version must be {EXPECTED_VERSION}")
    if "license" in frontmatter:
        raise ValidationError(f"{skill_path}: license must be omitted until explicitly decided")
    if not body.strip():
        raise ValidationError(f"{skill_path}: body must not be empty")
    validate_links(skill_path, root)
    validate_links(root / "README.md", root)
    validate_cases(root / "tests/cases.json", root / "tests/case-schema.json")
    validate_changelog(root / "CHANGELOG.md")
    scan_text_files(root)


def main(argv):
    if len(argv) != 2:
        print("Usage: python scripts/validate_package.py <package_root>")
        return 2
    root = Path(argv[1]).resolve()
    try:
        validate_package(root)
    except ValidationError as exc:
        print(f"VALIDATION FAILED: {exc}")
        return 1
    print(f"VALIDATION OK: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
