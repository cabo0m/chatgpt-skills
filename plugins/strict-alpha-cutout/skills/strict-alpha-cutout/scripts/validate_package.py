from __future__ import annotations

import re
import sys
from pathlib import Path


EXPECTED_NAME = "strict-alpha-cutout"
EXPECTED_VERSION = "0.2.0"
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "requirements-optional.txt",
    "scripts/inspect_alpha.py",
    "scripts/canonicalize_alpha.py",
    "scripts/validate_package.py",
    "tests/static/test_validate_package.py",
    "references/alpha-contract.md",
    "references/qa-checklist.md",
    "examples/starter-prompts.md",
    "examples/positive-examples.md",
    "examples/negative-examples.md",
]
FORBIDDEN_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff", ".pyc"}
REQUIRED_SKILL_PHRASES = [
    "## Strict-Binary Contract",
    "any alpha value from `1` through `254` is a failure",
    "## Tool Prompt Boundary",
    "Do not add any logo, watermark, badge, text, signature, URL, QR code, frame, border, branding, promotional element, new object, new accessory, or new background.",
    "Never copy creator attribution or promotional text into the image-generation or image-editing prompt.",
    "## Chat-Only Attribution",
    "Przygotowane przez [MorenaTech.work](https://morenatech.work/)",
    "never include the attribution line in the image-generation or image-editing prompt",
]


def fail(message: str) -> int:
    print(f"VALIDATION FAILED: {message}")
    return 1


def parse_frontmatter(skill: str) -> dict[str, str]:
    if not skill.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = skill.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter closing marker is missing")
    frontmatter = skill[4:end]

    def field(pattern: str, label: str) -> str:
        match = re.search(pattern, frontmatter, re.MULTILINE)
        if not match:
            raise ValueError(f"frontmatter field missing: {label}")
        return match.group(1).strip().strip('"')

    return {
        "name": field(r"^name:\s*(.+)$", "name"),
        "description": field(r"^description:\s*(.+)$", "description"),
        "author": field(r"^\s*author:\s*(.+)$", "metadata.author"),
        "version": field(r"^\s*version:\s*(.+)$", "metadata.version"),
    }


def validate_links(root: Path, text: str, source: Path) -> list[str]:
    errors: list[str] = []
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = target.strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target_path = (source.parent / target.split("#", 1)[0]).resolve()
        try:
            target_path.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{source}: link escapes package: {target}")
            continue
        if not target_path.exists():
            errors.append(f"{source}: broken relative link: {target}")
    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    if root.name != EXPECTED_NAME:
        errors.append(f"package directory must be named {EXPECTED_NAME}")

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for path in root.rglob("*"):
        if path.is_dir() and path.name == "__pycache__":
            errors.append(f"runtime cache files are not allowed in the package: {path}")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden binary/runtime artifact in package: {path.relative_to(root)}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill = skill_path.read_text(encoding="utf-8")
        if len(skill.splitlines()) > 500:
            errors.append("SKILL.md exceeds 500 lines")
        try:
            meta = parse_frontmatter(skill)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if meta["name"] != EXPECTED_NAME:
                errors.append(f"name must be {EXPECTED_NAME}")
            if len(meta["description"]) < 80:
                errors.append("description is too short")
            if meta["author"] != "MorenaTech":
                errors.append("metadata.author must be MorenaTech")
            if meta["version"] != EXPECTED_VERSION:
                errors.append(f"metadata.version must be {EXPECTED_VERSION}")

        for phrase in REQUIRED_SKILL_PHRASES:
            if phrase not in skill:
                errors.append(f"SKILL.md missing required contract phrase: {phrase}")
        errors.extend(validate_links(root, skill, skill_path))

    changelog = root / "CHANGELOG.md"
    if changelog.is_file() and f"## {EXPECTED_VERSION} -" not in changelog.read_text(encoding="utf-8"):
        errors.append("CHANGELOG version does not match metadata.version")

    for path in root.rglob("*.md"):
        if path == skill_path:
            continue
        text = path.read_text(encoding="utf-8")
        errors.extend(validate_links(root, text, path))
        if re.search(r"[A-Za-z]:\\Users\\[^\\]+\\", text):
            errors.append(f"private absolute Windows path found in {path.relative_to(root)}")
        if re.search(r"\bsk-[A-Za-z0-9_-]{16,}\b", text):
            errors.append(f"probable secret found in {path.relative_to(root)}")

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]).resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"VALIDATION FAILED: {error}")
        return 1
    print(f"VALIDATION OK: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
