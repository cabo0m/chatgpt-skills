#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

EXPECTED_NAME="business-portrait-studio"
EXPECTED_VERSION="0.3.0"
REQUIRED=[
 "SKILL.md","README.md","CHANGELOG.md","agents/openai.yaml","assets/icon.svg",
 "references/business-portrait-contract.md","references/frontal-reconstruction.md",
 "references/still-me-portrait-bridge.md","examples/starter-prompts.md",
 "tests/cases.json","tests/case-schema.json","tests/static/test_validate_package.py"
]

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
    errors=[]
    for rel in REQUIRED:
        if not (root/rel).exists(): errors.append("missing required path: "+rel)
    skill=(root/"SKILL.md").read_text(encoding="utf-8")
    if not re.search(r"(?m)^name:\s*business-portrait-studio\s*$",skill): errors.append("wrong frontmatter name")
    if not re.search(r'(?m)^\s+version:\s*"0\.3\.0"\s*$',skill): errors.append("wrong metadata.version")
    for phrase in ["## Failure Policy","original source image","complete, successfully validated result",
                   "Przygotowane przez [MorenaTech.work](https://morenatech.work/)"]:
        if phrase not in skill: errors.append("missing contract phrase: "+phrase)
    if "Host compatibility fallback" in skill: errors.append("legacy pre-tool attribution fallback remains")
    cases=json.loads((root/"tests/cases.json").read_text(encoding="utf-8"))
    if {c.get("id") for c in cases}!={f"T{i:02d}" for i in range(1,9)}: errors.append("case IDs mismatch")
    for path in root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or ".pytest_cache" in path.parts: continue
        if path.suffix.lower() in {".png",".jpg",".jpeg",".webp",".gif",".bmp",".tif",".tiff"}:
            errors.append("public package must not bundle user portrait raster images: "+str(path.relative_to(root)))
    if errors:
        for e in errors: print("FAIL:",e)
        return 1
    print(f"PASS: {EXPECTED_NAME} package {EXPECTED_VERSION}")
    print(f"PASS: {len(REQUIRED)} required paths")
    print("PASS: 8 text-only behavioral cases")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
