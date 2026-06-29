#!/usr/bin/env python3
"""Compare JSONL runtime captures to balance_targets matrix assertions."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RELEASE = "release-1-mvp"
SCRIPTS = ROOT / "scripts"

if str(ROOT / "main-game" / "pipeline" / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "main-game" / "pipeline" / "tools"))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

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
ROLLBACK_CONTAMINATED = "ROLLBACK_CONTAMINATED"
RESOLVER_MISMATCH = "RESOLVER_MISMATCH"


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


def _coerce_int(value: Any) -> int:
    if value is None:
        return 0
    return int(value)


def normalize_release_day(day: int | None, expected_floor: int) -> int | None:
    """Map runtime slot index (1–5) to file-id day (101–105) when assertions use file ids."""
    if day is None:
        return None
    slot = int(day)
    floor = int(expected_floor)
    if floor >= 100 and slot < 20:
        return slot + 100
    return slot


def validate_balanced_effect_events(
    events: list[dict],
    *,
    config: dict[str, Any] | None = None,
) -> list[str]:
    """Re-resolve logged semantic profile events and compare to captured kwargs."""
    import balance_resolver

    cfg = config or balance_resolver.load_profiles()
    errors: list[str] = []

    for event in events:
        if event.get("event") != "balanced_effect":
            continue
        seq = event.get("seq", "?")
        profile = event.get("profile")
        if not profile:
            errors.append(f"seq {seq}: balanced_effect missing profile")
            continue

        intensity = event.get("intensity", "standard")
        witness = event.get("witness")
        base_witness = bool(event.get("base_witness"))

        try:
            expected = balance_resolver.resolve_balanced_effect(
                profile,
                intensity_override=intensity,
                witness=witness or None,
                base_witness=base_witness,
                config=cfg,
            )
        except ValueError as exc:
            errors.append(f"seq {seq}: {exc}")
            continue

        logged = event.get("resolved_kwargs") or {}
        for key, value in expected.items():
            if _coerce_int(logged.get(key)) != value:
                errors.append(
                    f"seq {seq}: resolved_kwargs[{key!r}]={logged.get(key)!r} "
                    f"!= resolver {value!r} for profile {profile!r}"
                )
        for key, value in logged.items():
            if key not in expected and _coerce_int(value) != 0:
                errors.append(
                    f"seq {seq}: unexpected resolved_kwargs[{key!r}]={value!r} "
                    f"for profile {profile!r}"
                )

    return errors


def summarize_capture(
    run_id: str,
    events: list[dict],
    *,
    config: dict[str, Any] | None = None,
) -> dict:
    event_types = {e.get("event") for e in events}
    endings = [e.get("ending_id") for e in events if e.get("event") == "ending"]
    labels = [e.get("label") for e in events if e.get("event") == "grain_enter"]
    gates = [e for e in events if e.get("event") == "gate"]
    choices = [e for e in events if e.get("event") == "choice"]
    rollbacks = [e for e in events if e.get("event") == "rollback_event"]
    balanced_effects = [e for e in events if e.get("event") == "balanced_effect"]
    last_snapshot = events[-1].get("snapshot", {}) if events else {}
    stats = last_snapshot.get("stats", {})
    contains_rollback = any(
        e.get("contains_rollback") for e in events if e.get("event") == "run_end"
    ) or bool(rollbacks)
    resolver_errors = validate_balanced_effect_events(events, config=config)

    structure_ok = all(t in event_types for t in REQUIRED_EVENT_TYPES)
    has_choice_or_gate = bool(choices or gates)
    balance_proof_valid = not contains_rollback and not resolver_errors

    return {
        "run_id": run_id,
        "event_count": len(events),
        "structure_ok": structure_ok,
        "has_choice_or_gate": has_choice_or_gate,
        "contains_rollback": contains_rollback,
        "balanced_effect_count": len(balanced_effects),
        "resolver_errors": resolver_errors,
        "balance_proof_valid": balance_proof_valid,
        "balance_proof_blockers": (
            ([ROLLBACK_CONTAMINATED] if contains_rollback else [])
            + ([RESOLVER_MISMATCH] if resolver_errors else [])
        ),
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
            normalized = normalize_release_day(day, value)
            passed = normalized is not None and normalized >= value
            detail = f"day={day} (normalized={normalized})"
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


def build_report(
    release_slug: str,
    capture_filter: str | None,
    *,
    allow_rollback: bool = False,
    config: dict[str, Any] | None = None,
) -> tuple[str, bool]:
    targets = load_balance_targets(
        ROOT / "main-game" / "draft" / "releases" / "planning" / "balance" / "balance_targets.yaml"
    )
    mapping = {row["run_id"]: row for row in targets.get("matrix_execution_mapping", [])}
    cap_dir = capture_dir()
    run_ids = [capture_filter] if capture_filter else list(MATRIX_RUN_IDS)

    lines = [
        "# Runtime vs model comparison",
        "",
        f"**Release:** `{release_slug}`",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Capture dir:** `{_rel(cap_dir)}`",
        f"**Rollback policy:** {'informational only' if allow_rollback else 'rollback-contaminated captures invalid for balance proof'}",
        "",
        "## Summary",
        "",
        "| Run | Capture | Structure | Assertions | Rollback | Balance proof | Notes |",
        "|---|---|---|---|---|---|---|",
    ]

    assertion_rows: list[dict] = []
    missing: list[str] = []
    has_failure = False

    for run_id in run_ids:
        path = cap_dir / f"{run_id}.jsonl"
        if not path.exists():
            lines.append(f"| `{run_id}` | missing | — | — | — | — | No JSONL file |")
            missing.append(run_id)
            continue
        events = load_events(path)
        summary = summarize_capture(run_id, events, config=config)
        spec = mapping.get(run_id, {})
        assertions = spec.get("assertions", [])
        if assertions:
            results = evaluate_assertions(run_id, events, assertions)
            assertion_rows.extend(results)
            assertion_pass = all(r["passed"] for r in results) if results else False
        else:
            assertion_pass = False

        structure = summary["structure_ok"] and summary["has_choice_or_gate"]
        balance_proof = summary["balance_proof_valid"] or allow_rollback
        if not balance_proof or (assertions and not assertion_pass):
            has_failure = True

        notes = []
        if summary["endings"]:
            notes.append("ending=" + summary["endings"][-1])
        if not summary["has_choice_or_gate"]:
            notes.append("no choice/gate events")
        if summary["balanced_effect_count"]:
            notes.append(f"balanced_effect={summary['balanced_effect_count']}")
        if summary["contains_rollback"] and not allow_rollback:
            notes.append(ROLLBACK_CONTAMINATED)
        if summary["resolver_errors"]:
            notes.append(f"{RESOLVER_MISMATCH}={len(summary['resolver_errors'])}")

        proof_label = "PASS" if balance_proof else "FAIL"
        lines.append(
            f"| `{run_id}` | present | {'PASS' if structure else 'INCOMPLETE'} | "
            f"{'PASS' if assertion_pass else 'FAIL' if assertions else 'n/a'} | "
            f"{'yes' if summary['contains_rollback'] else 'no'} | "
            f"{proof_label} | "
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

    resolver_rows: list[tuple[str, str]] = []
    for run_id in run_ids:
        path = cap_dir / f"{run_id}.jsonl"
        if not path.exists():
            continue
        summary = summarize_capture(run_id, load_events(path), config=config)
        for error in summary["resolver_errors"]:
            resolver_rows.append((run_id, error))

    if resolver_rows:
        lines.extend(["", "## Semantic profile resolver mismatches", ""])
        for run_id, error in resolver_rows:
            lines.append(f"- `{run_id}`: {error}")

    if missing:
        lines.extend(["", "## Missing captures", ""])
        for run_id in missing:
            lines.append(
                f"- `{run_id}.jsonl` — play non-prod with `jump debug_capture_start` "
                f"after setting `_capture_run_id`"
            )

    lines.extend(
        [
            "",
            "## Limits",
            "",
            "- Compares final snapshots and ending labels only; does not replay rollback vectors yet.",
            "- Captures containing `rollback_event` are rejected for balance proof unless `--allow-rollback`.",
            "- `balanced_effect` events are re-resolved against `effect_profiles.yaml` at compare time.",
            "- Abstract simulator (`simulate_balance.py`) may disagree until P1–P7 captures exist.",
            "",
        ]
    )
    return "\n".join(lines), has_failure


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare JSONL runtime captures to balance matrix.")
    parser.add_argument("--release", default=DEFAULT_RELEASE)
    parser.add_argument("--capture", help="Single run_id (e.g. P1_corruption_forward)")
    parser.add_argument(
        "--allow-rollback",
        action="store_true",
        help="Treat rollback-contaminated captures as valid for balance proof (informational only)",
    )
    parser.add_argument(
        "--output",
        help="Markdown output path (default: pipeline releases qa folder)",
    )
    args = parser.parse_args()

    report, has_failure = build_report(
        args.release,
        args.capture,
        allow_rollback=args.allow_rollback,
    )
    out = (
        Path(args.output)
        if args.output
        else ROOT / "main-game" / "pipeline" / "releases" / args.release / "qa" / "runtime_model_comparison.md"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"Wrote {_rel(out)}")

    if not has_failure:
        return 0

    if args.capture is None:
        any_present = any((capture_dir() / f"{run_id}.jsonl").exists() for run_id in MATRIX_RUN_IDS)
        if not any_present:
            return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
