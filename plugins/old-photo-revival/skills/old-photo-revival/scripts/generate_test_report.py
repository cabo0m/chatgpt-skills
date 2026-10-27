import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def summarize(cases, manual_results):
    results_by_case = {entry["case_id"]: entry for entry in manual_results}
    mode_stats = defaultdict(lambda: {"count": 0, "passes": 0})
    identity_scores = []
    critical_failures = 0
    inference_failures = 0
    baseline_wins = 0
    skill_wins = 0
    ties = 0
    needs_fix = []

    for case in cases:
        case_id = case["id"]
        mode = case["mode"]
        result = results_by_case.get(case_id)
        if not result:
            continue
        mode_stats[mode]["count"] += 1
        if result.get("decision") == "pass":
            mode_stats[mode]["passes"] += 1
        else:
            needs_fix.append(case_id)
        if isinstance(result.get("identity_score"), (int, float)):
            identity_scores.append(result["identity_score"])
        if result.get("critical_failure"):
            critical_failures += 1
        if result.get("inference_discipline") == 0:
            inference_failures += 1
        comparison = result.get("comparison")
        if comparison == "skill":
            skill_wins += 1
        elif comparison == "baseline":
            baseline_wins += 1
        elif comparison == "tie":
            ties += 1

    pass_count = sum(1 for result in manual_results if result.get("decision") == "pass")
    total = len(manual_results)
    pass_rate = (pass_count / total) * 100 if total else 0.0
    median_identity = statistics.median(identity_scores) if identity_scores else None
    return {
        "pass_rate": pass_rate,
        "median_identity": median_identity,
        "critical_failures": critical_failures,
        "inference_failures": inference_failures,
        "mode_stats": mode_stats,
        "baseline_wins": baseline_wins,
        "skill_wins": skill_wins,
        "ties": ties,
        "needs_fix": needs_fix,
    }


def render_report(cases_path: Path, manual_path: Path | None):
    cases = load_json(cases_path)
    manual_results = load_json(manual_path) if manual_path else []
    summary = summarize(cases, manual_results)
    lines = [
        "# Old Photo Revival Test Report",
        "",
        f"- Cases in corpus: {len(cases)}",
        f"- Manual results loaded: {len(manual_results)}",
        f"- Pass rate: {summary['pass_rate']:.1f}%",
        f"- Median identity score: {summary['median_identity'] if summary['median_identity'] is not None else 'n/a'}",
        f"- Critical failures: {summary['critical_failures']}",
        f"- Inference-discipline failures: {summary['inference_failures']}",
        f"- Skill wins: {summary['skill_wins']}",
        f"- Baseline wins: {summary['baseline_wins']}",
        f"- Ties: {summary['ties']}",
        "",
        "## Per Mode",
        "",
    ]
    for mode, values in sorted(summary["mode_stats"].items()):
        count = values["count"]
        passes = values["passes"]
        mode_rate = (passes / count) * 100 if count else 0.0
        lines.append(f"- {mode}: {passes}/{count} pass ({mode_rate:.1f}%)")
    lines.extend(["", "## Cases Needing Improvement", ""])
    if summary["needs_fix"]:
        for case_id in summary["needs_fix"]:
            lines.append(f"- {case_id}")
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) not in {2, 3}:
        print("Usage: python scripts/generate_test_report.py <cases.json> [manual_results.json]")
        return 2
    cases_path = Path(argv[1])
    manual_path = Path(argv[2]) if len(argv) == 3 else None
    print(render_report(cases_path, manual_path), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
