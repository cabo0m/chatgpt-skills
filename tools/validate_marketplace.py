#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
PLUGINS = ROOT / "plugins"
MARKET = ROOT / ".agents" / "plugins" / "marketplace.json"
EXPECTED = {
    "business-portrait-studio",
    "faithful-product-photo",
    "old-photo-revival",
    "room-rescue",
    "still-me-portrait",
    "strict-alpha-cutout",
}


def version_of(skill_md: Path):
    text = skill_md.read_text(encoding="utf-8")
    match = re.search(r'(?m)^\s+version:\s*"?([^"\n]+)"?\s*$', text)
    if not match:
        raise AssertionError(f"Missing version in {skill_md}")
    return match.group(1).strip()


def main():
    errors = []
    try:
        market = json.loads(MARKET.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: marketplace JSON: {exc}")
        return 1

    names = {item.get("name") for item in market.get("plugins", [])}
    if names != EXPECTED:
        errors.append(f"marketplace names mismatch: {sorted(names)}")

    for item in market.get("plugins", []):
        name = item.get("name")
        source = item.get("source", {})
        path = source.get("path", "")
        if source.get("source") != "local":
            errors.append(f"{name}: marketplace source must be local")
        if not path.startswith("./plugins/"):
            errors.append(f"{name}: invalid source path {path!r}")
        if item.get("policy", {}).get("installation") != "AVAILABLE":
            errors.append(f"{name}: installation policy must be AVAILABLE")
        if "authentication" not in item.get("policy", {}):
            errors.append(f"{name}: authentication policy missing")

        plugin_root = ROOT / path[2:] if path.startswith("./") else ROOT / path
        manifest_path = plugin_root / "plugin.json"
        bundled_skill = plugin_root / "skills" / name / "SKILL.md"
        source_skill = SKILLS / name / "SKILL.md"
        if not manifest_path.is_file():
            errors.append(f"{name}: plugin.json missing")
            continue
        if not bundled_skill.is_file():
            errors.append(f"{name}: bundled SKILL.md missing")
            continue

        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{name}: invalid plugin.json: {exc}")
            continue

        if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            errors.append(f"{name}: wrong plugin schema")
        if manifest.get("name") != name:
            errors.append(f"{name}: manifest name mismatch")
        if manifest.get("version") != version_of(source_skill):
            errors.append(f"{name}: plugin/source version mismatch")
        if manifest.get("author", {}).get("name") != "MorenaTech":
            errors.append(f"{name}: publisher missing")
        if manifest.get("author", {}).get("url") != "https://morenatech.work/":
            errors.append(f"{name}: publisher URL missing")
        if bundled_skill.read_bytes() != source_skill.read_bytes():
            errors.append(f"{name}: bundled skill is out of sync")


    def package_files(root):
        result = {}
        for candidate in root.rglob("*"):
            if not candidate.is_file():
                continue
            rel = candidate.relative_to(root)
            if "__pycache__" in rel.parts or candidate.suffix == ".pyc" or candidate.name == ".DS_Store":
                continue
            result[rel.as_posix()] = candidate
        return result

    for name in sorted(EXPECTED):
        source_files = package_files(SKILLS / name)
        bundled_files = package_files(PLUGINS / name / "skills" / name)
        if set(source_files) != set(bundled_files):
            missing = sorted(set(source_files) - set(bundled_files))
            extra = sorted(set(bundled_files) - set(source_files))
            errors.append(f"{name}: package file set mismatch; missing={missing}, extra={extra}")
            continue
        for rel in sorted(source_files):
            if source_files[rel].read_bytes() != bundled_files[rel].read_bytes():
                errors.append(f"{name}: bundled package file out of sync: {rel}")
    for p in PLUGINS.rglob("*"):
        if p.name == "__pycache__" or p.suffix == ".pyc":
            errors.append(f"runtime cache in plugin package: {p.relative_to(ROOT)}")

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1
    print(f"PASS: MorenaTech marketplace with {len(EXPECTED)} installable plugins")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())