#!/usr/bin/env python3
"""Build choice_catalogue.csv from graph choices + non-prod script effect extraction."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from balance_catalogue import (  # noqa: E402
    ExtractedEffect,
    effect_to_catalogue_columns,
    extract_effect_near_line,
)
from balance_resolver import load_profiles  # noqa: E402

DEFAULT_RELEASE = "release-1-mvp"

CATALOGUE_FIELDS = [
    "grain_id",
    "choice_group",
    "choice_id",
    "next_grain",
    "effect_profile",
    "effect_intensity",
    "effect_witness",
    "effect_base_witness",
    "effect_resolved_from_profile",
    "insp_delta",
    "corr_xp_delta",
    "corr_level_delta",
    "anxiety_delta",
    "stern_susp_delta",
    "missy_susp_delta",
    "vance_susp_delta",
    "gideon_susp_delta",
    "stern_base_delta",
    "vance_base_delta",
    "missy_base_delta",
    "gideon_base_delta",
    "manuscript_delta",
    "sets_flag",
    "unique_unlock",
    "risk_tier",
    "design_note",
]


def _risk_tier(insp: int, corr: int, susp_total: int) -> str:
    if corr >= 15 or susp_total >= 30:
        return "high"
    if corr >= 5 or susp_total >= 15:
        return "medium"
    if insp > 0 or corr > 0:
        return "low"
    return "safe"


def _int_field(row: dict[str, str], field: str) -> int:
    value = (row.get(field) or "").strip()
    if not value:
        return 0
    return int(float(value))


def build_rows(choices_path: Path, *, config) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    file_cache: dict[Path, list[str]] = {}

    with choices_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            source_file = (row.get("source_file") or "").strip()
            line_number = int(row.get("line_number") or 0)
            choice_group = row.get("choice_group", "")

            effect = ExtractedEffect(kind="none")
            if source_file and line_number:
                src_path = Path(source_file)
                if not src_path.is_absolute():
                    src_path = ROOT / src_path
                if src_path.exists():
                    if src_path not in file_cache:
                        file_cache[src_path] = src_path.read_text(encoding="utf-8").splitlines()
                    effect = extract_effect_near_line(file_cache[src_path], line_number)

            effect_cols = effect_to_catalogue_columns(effect, config=config)

            insp = _int_field(effect_cols, "insp_delta")
            corr = _int_field(effect_cols, "corr_xp_delta")
            susp_total = sum(
                abs(_int_field(effect_cols, field))
                for field in (
                    "stern_susp_delta",
                    "missy_susp_delta",
                    "vance_susp_delta",
                    "gideon_susp_delta",
                    "stern_base_delta",
                    "vance_base_delta",
                    "missy_base_delta",
                    "gideon_base_delta",
                )
            )

            rows.append(
                {
                    "grain_id": choice_group,
                    "choice_group": choice_group,
                    "choice_id": row.get("option_key") or row.get("choice_id", ""),
                    "next_grain": row.get("jump_to", ""),
                    **effect_cols,
                    "corr_level_delta": "",
                    "anxiety_delta": "",
                    "manuscript_delta": "",
                    "sets_flag": row.get("sets_state", ""),
                    "unique_unlock": "",
                    "risk_tier": _risk_tier(insp, corr, susp_total),
                    "design_note": (
                        f"Imported from graph choices ({source_file}:{line_number})"
                        if source_file
                        else "Imported from graph choices"
                    ),
                }
            )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Build choice_catalogue.csv from graph + script scan.")
    parser.add_argument("--release", default=DEFAULT_RELEASE)
    parser.add_argument(
        "--graph-dir",
        default=f"main-game/pipeline/releases/{DEFAULT_RELEASE}/graph",
    )
    parser.add_argument(
        "--out",
        default="main-game/draft/releases/planning/balance/choice_catalogue.csv",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate existing catalogue profile rows against balance_resolver",
    )
    args = parser.parse_args()

    graph_dir = Path(args.graph_dir)
    out_path = Path(args.out)
    if not graph_dir.is_absolute():
        graph_dir = ROOT / graph_dir
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    config = load_profiles()

    if args.check:
        from balance_catalogue import validate_choice_catalogue

        errors = validate_choice_catalogue(out_path, config=config)
        if errors:
            for error in errors[:20]:
                print(error, file=sys.stderr)
            if len(errors) > 20:
                print(f"... and {len(errors) - 20} more", file=sys.stderr)
            return 1
        print(f"OK — {out_path.relative_to(ROOT).as_posix()} profile rows match resolver")
        return 0

    choices_path = graph_dir / "release1_choices.csv"
    if not choices_path.exists():
        print(f"Missing graph choices file: {choices_path}", file=sys.stderr)
        return 1

    rows = build_rows(choices_path, config=config)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CATALOGUE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    profile_rows = sum(1 for row in rows if row.get("effect_profile"))
    bespoke_rows = sum(
        1 for row in rows if row.get("effect_resolved_from_profile") == "false" and not row.get("effect_profile")
    )
    print(
        f"Wrote {len(rows)} choice rows to {out_path.relative_to(ROOT).as_posix()} "
        f"({profile_rows} profile, {bespoke_rows} bespoke deltas)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
