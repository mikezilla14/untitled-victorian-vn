#!/usr/bin/env python3
"""Seed choice_catalogue.csv from Release 1 graph extraction outputs."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RELEASE = "release-1-mvp"

CATALOGUE_FIELDS = [
    "grain_id",
    "choice_group",
    "choice_id",
    "next_grain",
    "insp_delta",
    "corr_xp_delta",
    "corr_level_delta",
    "anxiety_delta",
    "stern_susp_delta",
    "missy_susp_delta",
    "vance_susp_delta",
    "gideon_susp_delta",
    "manuscript_delta",
    "sets_flag",
    "unique_unlock",
    "risk_tier",
    "design_note",
]


def _int_or_blank(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    try:
        return str(int(float(value)))
    except ValueError:
        return ""


def _risk_tier(insp: int, corr: int, susp_total: int) -> str:
    if corr >= 15 or susp_total >= 30:
        return "high"
    if corr >= 5 or susp_total >= 15:
        return "medium"
    if insp > 0 or corr > 0:
        return "low"
    return "safe"


def _parse_effects_mapped(raw: str) -> dict[str, int]:
    if not raw:
        return {}
    try:
        data = json.loads(raw.replace("'", '"'))
    except json.JSONDecodeError:
        return {}
    result: dict[str, int] = {}
    for key, value in data.items():
        try:
            result[key] = int(value)
        except (TypeError, ValueError):
            continue
    return result


def load_effects_by_option(effects_path: Path) -> dict[tuple[str, str], dict[str, int]]:
    lookup: dict[tuple[str, str], dict[str, int]] = {}
    if not effects_path.exists():
        return lookup
    with effects_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (row.get("label", ""), row.get("branch_option", ""))
            mapped = {
                "inspiration_delta": _int_or_blank(row.get("inspiration_delta", "")),
                "corruption_delta": _int_or_blank(row.get("corruption_delta", "")),
                "stern_acute_susp_delta": _int_or_blank(row.get("stern_acute_susp_delta", "")),
                "vance_acute_susp_delta": _int_or_blank(row.get("vance_acute_susp_delta", "")),
                "missy_acute_susp_delta": _int_or_blank(row.get("missy_acute_susp_delta", "")),
                "gideon_acute_susp_delta": _int_or_blank(row.get("gideon_acute_susp_delta", "")),
            }
            for field, value in mapped.items():
                if value:
                    mapped[field] = int(value)
                else:
                    mapped[field] = 0
            if row.get("effects_mapped"):
                mapped.update(_parse_effects_mapped(row["effects_mapped"]))
            lookup[key] = mapped
    return lookup


def build_rows(choices_path: Path, effects_lookup: dict[tuple[str, str], dict[str, int]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with choices_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            label = row.get("label", "")
            option_key = row.get("option_key", "")
            effects = effects_lookup.get((label, option_key), _parse_effects_mapped(row.get("effects_mapped", "")))
            insp = int(effects.get("inspiration_delta", 0) or 0)
            corr = int(effects.get("corruption_delta", 0) or 0)
            stern = int(effects.get("stern_acute_susp_delta", 0) or 0)
            vance = int(effects.get("vance_acute_susp_delta", 0) or 0)
            missy = int(effects.get("missy_acute_susp_delta", 0) or 0)
            gideon = int(effects.get("gideon_acute_susp_delta", 0) or 0)
            susp_total = abs(stern) + abs(vance) + abs(missy) + abs(gideon)
            choice_group = row.get("choice_group", "")
            rows.append(
                {
                    "grain_id": choice_group,
                    "choice_group": choice_group,
                    "choice_id": option_key or row.get("choice_id", ""),
                    "next_grain": row.get("jump_to", ""),
                    "insp_delta": str(insp) if insp else "",
                    "corr_xp_delta": str(corr) if corr else "",
                    "corr_level_delta": "",
                    "anxiety_delta": "",
                    "stern_susp_delta": str(stern) if stern else "",
                    "missy_susp_delta": str(missy) if missy else "",
                    "vance_susp_delta": str(vance) if vance else "",
                    "gideon_susp_delta": str(gideon) if gideon else "",
                    "manuscript_delta": "",
                    "sets_flag": row.get("sets_state", ""),
                    "unique_unlock": "",
                    "risk_tier": _risk_tier(insp, corr, susp_total),
                    "design_note": f"Imported from graph choices ({row.get('source_file', '')}:{row.get('line_number', '')})",
                }
            )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Build choice_catalogue.csv from graph extraction outputs.")
    parser.add_argument("--release", default=DEFAULT_RELEASE)
    parser.add_argument(
        "--graph-dir",
        default=f"main-game/pipeline/releases/{DEFAULT_RELEASE}/graph",
    )
    parser.add_argument(
        "--out",
        default="main-game/draft/releases/planning/balance/choice_catalogue.csv",
    )
    args = parser.parse_args()

    graph_dir = Path(args.graph_dir)
    out_path = Path(args.out)
    if not graph_dir.is_absolute():
        graph_dir = ROOT / graph_dir
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    choices_path = graph_dir / "release1_choices.csv"
    effects_path = graph_dir / "release1_effects.csv"
    if not choices_path.exists():
        print(f"Missing graph choices file: {choices_path}", file=sys.stderr)
        return 1

    rows = build_rows(choices_path, load_effects_by_option(effects_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CATALOGUE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} choice rows to {out_path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
