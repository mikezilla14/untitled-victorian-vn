#!/usr/bin/env python3
"""Compare JSONL runtime captures to balance_targets matrix assertions."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RELEASE = "release-1-mvp"

if str(ROOT / "main-game" / "pipeline" / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "main-game" / "pipeline" / "tools"))

from balance_model import load_balance_targets  # noqa: E402


REQUIRED_EVENT_TYPES = ("run_start", "grain_enter", "run_end")
MATRIX_RUN_IDS = (
    "P1_corruption_forward",
    "P2_cautious",
    "P3_low_corruption",
    "P4_deadline_1",
    "P5_deadline_2",
    "P6_anxiety_collapse",
    "P7_penance",
)


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def capture_dir() -> Path:
    return ROOT / "main-game" / "non-prod-game" / "debug_captures"


def load_events(path: Path) -> list[dict]:
    events: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events


def summarize_capture(run_id: str, events: list[dict]) -> dict:
    event_types = {e.get("event") for e in events}
    endings = [e.get("ending_id") for e in events if e.get("event") == "ending"]
    labels = [e.get("label") for e in events if e.get("event") == "grain_enter"]
    gates = [e for e in events if e.get("event") == "gate"]
    choices = [e for e in events if e.get("event") == "choice"]
    rollbacks = [e for e in events if e.get("event") == "rollback_event"]
    last_snapshot = events[-1].get("snapshot", {}) if events else {}
    stats = last_snapshot.get("stats", {})
    contains_rollback = any(
        e.get("contains_rollback") for e in events if e.get("event") == "run_end"
    ) or bool(rollbacks)

    structure_ok = all(t in event_types for t in REQUIRED_EVENT_TYPES)
    has_choice_or_gate = bool(choices or gates)

    return {
        "run_id": run_id,
        "event_count": len(events),
        "structure_ok": structure_ok,
        "has_choice_or_gate": has_choice_or_gate,
        "contains_rollback": contains_rollback,
        "endings": endings,
        "last_label": labels[-1] if labels else "",
        "final_stats": stats,
        "gate_count": len(gates),
        "choice_count": len(choices),
    }


def evaluate_assertions(run_id: str, events: list[dict], assertions: list) -> list[dict]:
    summary = summarize_capture(run_id, events)
    stats = summary["final_stats"]
    endings = set(summary["endings"])
    labels = {e.get("label") for e in events if e.get("event") == "grain_enter"}
    confrontation_seen = any(
        e.get("event") == "flag" and e.get("flag") == "confrontation" for e in events
    ) or any(label.startswith("confrontation_") for label in labels if label)

    rows: list[dict] = []
    for assertion in assertions:
        if isinstance(assertion, str):
            continue
        if not isinstance(assertion, dict) or len(assertion) != 1:
            continue
        key, value = next(iter(assertion.items()))
        passed = False
        detail = ""
        if key == "assert_ending":
            passed = value in endings or value in labels
            detail = f"endings={sorted(endings)}"
        elif key == "assert_ending_one_of":
            passed = bool(endings & set(value)) or bool(labels & set(value))
            detail = f"endings={sorted(endings)}"
        elif key == "assert_stat_floor":
            passed = all(stats.get(k, 0) >= v for k, v in value.items())
            detail = f"stats={stats}"
        elif key == "assert_reaches_day_at_least":
            day = stats.get("current_day")
            if day is None:
                for e in reversed(events):
                    snap = e.get("snapshot", {})
                    flags = snap.get("flags", {})
                    if "current_day" in flags:
                        day = flags["current_day"]
                        break
            passed = day is not None and day >= value
            detail = f"day={day}"
        elif key == "assert_event_seen":
            if value == "confrontation":
                passed = confrontation_seen
                detail = f"confrontation_seen={confrontation_seen}"
            else:
                passed = value in {e.get("event") for e in events}
                detail = f"event={value}"
        else:
            detail = "unsupported_assertion"
        rows.append(
            {
                "run_id": run_id,
                "assertion": key,
                "expected": json.dumps(value, sort_keys=True),
                "passed": passed,
                "detail": detail,
            }
        )
    return rows


def build_report(release_slug: str, capture_filter: str | None) -> str:
    targets = load_balance_targets(ROOT / "main-game" / "draft" / "releases" / "planning" / "balance" / "balance_targets.yaml")
    mapping = {row["run_id"]: row for row in targets.get("matrix_execution_mapping", [])}
    cap_dir = capture_dir()
    run_ids = [capture_filter] if capture_filter else list(MATRIX_RUN_IDS)

    lines = [
        "# Runtime vs model comparison",
        "",
        f"**Release:** `{release_slug}`",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Capture dir:** `{_rel(cap_dir)}`",
        "",
        "## Summary",
        "",
        "| Run | Capture | Structure | Assertions | Rollback | Notes |",
        "|---|---|---|---|---|---|",
    ]

    assertion_rows: list[dict] = []
    missing: list[str] = []

    for run_id in run_ids:
        path = cap_dir / f"{run_id}.jsonl"
        if not path.exists():
            lines.append(f"| `{run_id}` | missing | — | — | — | No JSONL file |")
            missing.append(run_id)
            continue
        events = load_events(path)
        summary = summarize_capture(run_id, events)
        spec = mapping.get(run_id, {})
        assertions = spec.get("assertions", [])
        if assertions:
            results = evaluate_assertions(run_id, events, assertions)
            assertion_rows.extend(results)
            assertion_pass = all(r["passed"] for r in results) if results else False
        else:
            assertion_pass = False
        structure = summary["structure_ok"] and summary["has_choice_or_gate"]
        notes = []
        if summary["endings"]:
            notes.append("ending=" + summary["endings"][-1])
        if not summary["has_choice_or_gate"]:
            notes.append("no choice/gate events")
        lines.append(
            f"| `{run_id}` | present | {'PASS' if structure else 'INCOMPLETE'} | "
            f"{'PASS' if assertion_pass else 'FAIL' if assertions else 'n/a'} | "
            f"{'yes' if summary['contains_rollback'] else 'no'} | "
            f"{'; '.join(notes) or '—'} |"
        )

    lines.extend(["", "## Assertion detail", ""])
    if assertion_rows:
        lines.append("| Run | Assertion | Expected | Pass | Detail |")
        lines.append("|---|---|---|---|---|")
        for row in assertion_rows:
            lines.append(
                f"| `{row['run_id']}` | `{row['assertion']}` | `{row['expected']}` | "
                f"{'yes' if row['passed'] else 'no'} | {row['detail']} |"
            )
    else:
        lines.append("_No capture files with assertions to evaluate._")

    if missing:
        lines.extend(["", "## Missing captures", ""])
        for run_id in missing:
            lines.append(f"- `{run_id}.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`")

    lines.extend(
        [
            "",
            "## Limits",
            "",
            "- Compares final snapshots and ending labels only; does not replay rollback vectors yet.",
            "- Abstract simulator (`simulate_balance.py`) may disagree until P1–P7 captures exist.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare JSONL runtime captures to balance matrix.")
    parser.add_argument("--release", default=DEFAULT_RELEASE)
    parser.add_argument("--capture", help="Single run_id (e.g. P1_corruption_forward)")
    parser.add_argument(
        "--output",
        help="Markdown output path (default: pipeline releases qa folder)",
    )
    args = parser.parse_args()

    report = build_report(args.release, args.capture)
    out = (
        Path(args.output)
        if args.output
        else ROOT / "main-game" / "pipeline" / "releases" / args.release / "qa" / "runtime_model_comparison.md"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"Wrote {_rel(out)}")
    if "missing |" in report and args.capture is None:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
