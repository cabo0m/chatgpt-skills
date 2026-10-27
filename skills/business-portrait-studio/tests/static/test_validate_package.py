import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate_package.py"

class BusinessPortraitPackageTests(unittest.TestCase):
    def test_validator_passes(self):
        p=subprocess.run([sys.executable,str(VALIDATOR),str(ROOT)],text=True,capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertIn("8 text-only behavioral cases",p.stdout)

    def test_failure_and_attribution_contract(self):
        skill=(ROOT/"SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Failure Policy",skill)
        self.assertIn("original source image",skill)
        self.assertIn("complete, successfully validated result",skill)
        self.assertIn("Przygotowane przez [MorenaTech.work](https://morenatech.work/)",skill)
        self.assertNotIn("Host compatibility fallback",skill)

    def test_cases_cover_success_failure_and_identity(self):
        cases=json.loads((ROOT/"tests/cases.json").read_text(encoding="utf-8"))
        self.assertEqual({x["id"] for x in cases},{f"T{i:02d}" for i in range(1,9)})
        expected={x["expected"] for x in cases}
        self.assertIn("fail_closed",expected)
        self.assertIn("final_linked_attribution",expected)
        self.assertIn("preserve_identity",expected)

if __name__ == "__main__":
    unittest.main()
