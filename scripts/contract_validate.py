#!/usr/bin/env python3
"""
Validate agent handoff JSON contracts for a release day.

Usage:
  py scripts/contract_validate.py --day day105 --release "release 1 - mvp"
  py scripts/contract_validate.py --file path/to/day105_gate_lead_narrative.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from contract_schemas import (  # noqa: E402
    GATE_VERDICTS,
    check_gate_json_sidecar,
    load_json_file,
    validate_book_writing_context,
    validate_gate_verdict,
    validate_narrative_change_brief,
    validate_profile_delta,
    validate_promotion_handoff,
)
from narrative_paths import DayContext, draft_day_dir, pipeline_gates_dir, pipeline_handoffs_dir  # noqa: E402
from writers_room_pipeline import (  # noqa: E402
    check_narrative_change_brief,
    validate_day_pipeline,
)

ROOT = Path(__file__).resolve().parents[1]


def validate_day(day_id: str, release: str) -> int:
    ctx = DayContext(day_id=day_id, release_slug=release)
    failures = 0
    gates = pipeline_gates_dir(ctx)

    print(f"Validating contracts for {day_id} ({release})\n")

    for gate_slug in GATE_VERDICTS:
        md = gates / f"{day_id}_gate_{gate_slug}.md"
        if not md.exists():
            continue
        errs = check_gate_json_sidecar(gates, day_id, release, gate_slug, md)
        if errs:
            failures += len(errs)
            for e in errs:
                print(f"  [ERROR] {e}")
        else:
            print(f"  [OK] gate {gate_slug} (md + json)")

    brief_errs = check_narrative_change_brief(ctx)
    if brief_errs:
        failures += len(brief_errs)
        for e in brief_errs:
            print(f"  [ERROR] {e}")
    elif (draft_day_dir(ctx) / "briefs" / f"{day_id}_narrative_change_brief.md").exists():
        print("  [OK] narrative change brief")

    handoffs = pipeline_handoffs_dir(ctx)
    profile_json = handoffs / f"{day_id}_profile_delta.json"
    if profile_json.exists():
        data, load_errs = load_json_file(profile_json)
        errs = list(load_errs)
        if data is not None:
            errs.extend(validate_profile_delta(data))
        if errs:
            failures += len(errs)
            for e in errs:
                print(f"  [ERROR] {e}")
        else:
            print("  [OK] profile delta")

    promo = handoffs / f"{day_id}_promotion_handoff.json"
    if promo.exists():
        data, load_errs = load_json_file(promo)
        errs = list(load_errs)
        if data is not None:
            errs.extend(validate_promotion_handoff(data))
        if errs:
            failures += len(errs)
            for e in errs:
                print(f"  [ERROR] {e}")
        else:
            print("  [OK] promotion handoff")

    non_canon = (draft_day_dir(ctx) / f"{day_id}_non_canon.rpy").relative_to(ROOT).as_posix()
    if (ROOT / non_canon).exists():
        count, messages = validate_day_pipeline(
            non_canon,
            require_gates=True,
            partial_gates=False,
            require_json_contracts=True,
        )
        for line in messages:
            print(line)
        failures += count

    if failures:
        print(f"\n{failures} contract error(s).")
        return 1
    print("\nAll contracts valid.")
    return 0


def validate_single_file(path_str: str) -> int:
    path = ROOT / path_str
    name = path.name
    data, errs = load_json_file(path)
    if data is None:
        for e in errs:
            print(f"[ERROR] {e}")
        return 1

    if "_gate_" in name and name.endswith(".json"):
        errs = validate_gate_verdict(data)
    elif "narrative_change_brief" in name:
        errs = validate_narrative_change_brief(data)
    elif "profile_delta" in name:
        errs = validate_profile_delta(data)
    elif "promotion_handoff" in name:
        errs = validate_promotion_handoff(data)
    elif "book_writing_context" in name or data.get("kind") in (
        "book_writing_context",
        "book_import_header",
    ):
        errs = validate_book_writing_context(data)
    else:
        print(f"Unknown contract file type: {name}")
        return 1

    if errs:
        for e in errs:
            print(f"[ERROR] {e}")
        return 1
    print(f"[OK] {path.relative_to(ROOT).as_posix()}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate agent handoff JSON contracts.")
    parser.add_argument("--day", help="Day id e.g. day105")
    parser.add_argument("--release", default="release-1-mvp", help="Release slug or display name")
    parser.add_argument("--file", help="Single JSON contract file path")
    args = parser.parse_args()

    if args.file:
        return validate_single_file(args.file.replace("//", "/"))
    if not args.day:
        parser.error("Provide --day or --file")
    return validate_day(args.day, args.release)


if __name__ == "__main__":
    sys.exit(main())
