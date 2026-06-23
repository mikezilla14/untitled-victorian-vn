#!/usr/bin/env python3
"""Export balance profiles and their resolved stat deltas to CSV."""

from __future__ import annotations

import argparse
import ast
import csv
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_RPY_PATH = (
    ROOT / "main-game" / "non-prod-game" / "game" / "shared" / "balance_profiles_non_canon.rpy"
)
DEFAULT_OUTPUT_CSV = (
    ROOT / "main-game" / "draft" / "releases" / "planning" / "balance" / "balance_profile_deltas.csv"
)


def parse_rpy_profiles(rpy_path: Path) -> dict[str, Any]:
    """Parse the balance resolver parameters directly from the .rpy file using AST."""
    if not rpy_path.exists():
        raise FileNotFoundError(f"Source file not found: {rpy_path}")

    lines = []
    in_python_block = False
    with open(rpy_path, "r", encoding="utf-8") as f:
        for line in f:
            if "init -1 python in balance_resolver:" in line:
                in_python_block = True
                continue
            if in_python_block:
                lines.append(line)

    python_lines = []
    for line in lines:
        if line.strip() == "":
            python_lines.append("")
        elif line.startswith("    "):
            python_lines.append(line[4:])
        else:
            break

    python_code = "\n".join(python_lines)
    tree = ast.parse(python_code)

    extracted: dict[str, Any] = {}
    target_vars = {
        "BALANCE_STAT_UNITS",
        "BALANCE_INTENSITIES",
        "BALANCE_PROFILES",
        "BALANCE_VALID_WITNESSES",
    }

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in target_vars:
                    extracted[target.id] = ast.literal_eval(node.value)

    missing = target_vars - extracted.keys()
    if missing:
        raise ValueError(
            f"Failed to extract variables {', '.join(missing)} from {rpy_path}"
        )

    return extracted


def _clean_scale(value: Any) -> float:
    return round(float(value), 6)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _resolve_balance_amount(
    stat_key: str,
    intensity_key: Any,
    scale_modifier: float,
    stat_units: dict[str, int],
    intensities: dict[str, float],
) -> int:
    if intensity_key is None:
        return 0

    if stat_key not in stat_units:
        raise ValueError(f"Unknown balance stat unit: {stat_key}")

    scale_modifier = _clean_scale(scale_modifier)
    base_unit = stat_units[stat_key]

    if _is_number(intensity_key):
        base_multiplier = _clean_scale(intensity_key)
    else:
        if intensity_key not in intensities:
            raise ValueError(f"Unknown balance intensity constant: {intensity_key}")
        base_multiplier = _clean_scale(intensities[intensity_key])

    return int(round(base_unit * base_multiplier * scale_modifier))


def _resolve_intensity_scale_modifier(
    intensity_override: Any,
    intensities: dict[str, float],
) -> float:
    if intensity_override is None or intensity_override == "standard":
        return 1.0

    if _is_number(intensity_override):
        return _clean_scale(intensity_override)

    if intensity_override not in intensities:
        raise ValueError(f"Unknown balance intensity override: {intensity_override}")

    standard = intensities["standard"]
    if standard == 0:
        raise ValueError("BALANCE_INTENSITIES['standard'] cannot be zero.")

    return _clean_scale(intensities[intensity_override] / standard)


def generate_csv_rows(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate resolved rows for each profile and each defined intensity."""
    stat_units = config["BALANCE_STAT_UNITS"]
    intensities = config["BALANCE_INTENSITIES"]
    profiles = config["BALANCE_PROFILES"]

    rows = []
    # Order of intensities we want to display
    intensity_keys = ["trace", "minor", "standard", "major", "severe"]

    # In case there are custom/other intensities in the file not in the list:
    for key in intensities:
        if key not in intensity_keys:
            intensity_keys.append(key)

    for profile_name, spec in sorted(profiles.items()):
        for intensity in intensity_keys:
            scale_mod = _resolve_intensity_scale_modifier(intensity, intensities)
            
            insp_val = 0
            corr_val = 0
            witness_susp_val = 0
            
            if "insp" in spec:
                insp_val = _resolve_balance_amount("insp", spec["insp"], scale_mod, stat_units, intensities)
            if "corr" in spec:
                corr_val = _resolve_balance_amount("corr", spec["corr"], scale_mod, stat_units, intensities)
            if "witness_susp" in spec:
                witness_susp_val = _resolve_balance_amount("susp", spec["witness_susp"], scale_mod, stat_units, intensities)

            rows.append({
                "profile": profile_name,
                "intensity": intensity,
                "insp": insp_val,
                "corr": corr_val,
                "witness_susp": witness_susp_val,
            })
            
    return rows


def build_csv_content(rows: list[dict[str, Any]]) -> str:
    """Generate CSV string from rows."""
    import io
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["profile", "intensity", "insp", "corr", "witness_susp"],
        lineterminator="\n"
    )
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return output.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export balance profiles and resolved values to CSV."
    )
    parser.add_argument(
        "--rpy",
        type=Path,
        default=DEFAULT_RPY_PATH,
        help="Path to balance_profiles_non_canon.rpy",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_CSV,
        help="Path to output CSV file",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if the existing CSV is up to date without writing",
    )
    args = parser.parse_args()

    rpy_path = args.rpy if args.rpy.is_absolute() else ROOT / args.rpy
    output_path = args.output if args.output.is_absolute() else ROOT / args.output

    try:
        config = parse_rpy_profiles(rpy_path)
        rows = generate_csv_rows(config)
        csv_content = build_csv_content(rows)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if not output_path.exists():
            print(f"Check failed: {output_path} does not exist.", file=sys.stderr)
            return 1
        
        try:
            existing_content = output_path.read_text(encoding="utf-8").replace("\r\n", "\n")
        except Exception as exc:
            print(f"ERROR reading existing CSV: {exc}", file=sys.stderr)
            return 1

        if existing_content != csv_content:
            print(f"Check failed: {output_path} is out of sync with {rpy_path}.", file=sys.stderr)
            print("Run: py scripts/export_balance_csv.py", file=sys.stderr)
            return 1
        
        print(f"OK: {output_path} is in sync.")
        return 0

    # Write output
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(csv_content, encoding="utf-8")
        try:
            rel_out = output_path.relative_to(ROOT).as_posix()
        except ValueError:
            rel_out = output_path.as_posix()
        print(f"Successfully exported balance profile deltas to {rel_out}")
    except Exception as exc:
        print(f"ERROR writing CSV: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
