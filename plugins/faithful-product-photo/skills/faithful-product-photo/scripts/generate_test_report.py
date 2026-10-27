#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cases = json.loads((ROOT / "tests/cases.json").read_text(encoding="utf-8"))

lines = [
    "# Faithful Product Photo - Generated Manual Test Report",
    "",
    "Tester:",
    "Date:",
    "Client / model:",
    "Skill version: 0.2.1",
    "",
    "| Case | Title | Mode | PASS / FAIL / BLOCKED | Failure code | Notes |",
    "|---|---|---|---|---|---|",
]
for case in cases:
    lines.append(f"| {case['id']} | {case['title']} | {case['mode']} |  |  |  |")

out = ROOT / "tests/generated-manual-report.md"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(out)
