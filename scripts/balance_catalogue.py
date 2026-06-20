#!/usr/bin/env python3
"""Choice catalogue helpers: script effect extraction, profile resolution, validation."""

from __future__ import annotations

import ast
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

APPLY_EFFECTS_RE = re.compile(r"apply_effects\s*\((.*)\)\s*$")
BALANCED_RE = re.compile(r'apply_balanced_effect\s*\(\s*"([^"]+)"\s*(?:,\s*(.*))?\)\s*$')
BESPOKE_COMMENT_RE = re.compile(r"#\s*\[STATE bespoke\]", re.IGNORECASE)
MENU_OPTION_RE = re.compile(r'^(?P<indent>\s*)"(?P<text>[^"]+)"(?:\s+if\s+(?P<condition>[^:]+))?:\s*$')

CATALOGUE_DELTA_FIELDS = (
    "insp_delta",
    "corr_xp_delta",
    "stern_susp_delta",
    "missy_susp_delta",
    "vance_susp_delta",
    "gideon_susp_delta",
    "stern_base_delta",
    "vance_base_delta",
    "missy_base_delta",
    "gideon_base_delta",
)

KWARG_TO_DELTA = {
    "insp": "insp_delta",
    "corr": "corr_xp_delta",
    "stern_susp": "stern_susp_delta",
    "vance_susp": "vance_susp_delta",
    "missy_susp": "missy_susp_delta",
    "gideon_susp": "gideon_susp_delta",
    "stern_base": "stern_base_delta",
    "vance_base": "vance_base_delta",
    "missy_base": "missy_base_delta",
    "gideon_base": "gideon_base_delta",
}


@dataclass
class ExtractedEffect:
    kind: str  # profile | bespoke | none
    profile: str = ""
    intensity: str | float = "standard"
    witness: str = ""
    base_witness: bool = False
    raw_call: str = ""
    kwargs: dict[str, int] | None = None


def split_args(raw: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for part in re.split(r",(?![^\(]*\))", raw):
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, value = part.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def _parse_literal(value: str) -> str | float | int | bool:
    value = value.strip()
    try:
        parsed = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        return value
    return parsed


def parse_apply_effects_kwargs(raw: str) -> dict[str, int]:
    kwargs: dict[str, int] = {}
    for key, value in split_args(raw).items():
        parsed = _parse_literal(value)
        if isinstance(parsed, bool):
            continue
        if isinstance(parsed, (int, float)):
            kwargs[key] = int(parsed)
    return kwargs


def parse_balanced_effect_line(line: str) -> ExtractedEffect | None:
    stripped = line.strip()
    match = BALANCED_RE.search(stripped)
    if not match:
        return None

    profile = match.group(1)
    arg_tail = (match.group(2) or "").strip()
    args = split_args(arg_tail) if arg_tail else {}

    intensity: str | float = "standard"
    if "intensity" in args:
        parsed = _parse_literal(args["intensity"])
        if isinstance(parsed, (int, float)):
            intensity = float(parsed)
        elif isinstance(parsed, str):
            intensity = parsed

    witness = ""
    if "witness" in args:
        parsed = _parse_literal(args["witness"])
        witness = str(parsed) if parsed is not None else ""

    base_witness = False
    if "base_witness" in args:
        parsed = _parse_literal(args["base_witness"])
        base_witness = bool(parsed)

    return ExtractedEffect(
        kind="profile",
        profile=profile,
        intensity=intensity,
        witness=witness,
        base_witness=base_witness,
        raw_call=stripped,
    )


def parse_apply_effects_line(line: str) -> ExtractedEffect | None:
    stripped = line.strip()
    match = APPLY_EFFECTS_RE.search(stripped)
    if not match:
        return None
    kwargs = parse_apply_effects_kwargs(match.group(1))
    return ExtractedEffect(kind="bespoke", raw_call=stripped, kwargs=kwargs)


def extract_effect_near_line(
    lines: list[str],
    line_number: int,
    *,
    window: int = 30,
) -> ExtractedEffect:
    """Scan forward from a 1-based menu line for the first economy effect call."""
    start = max(0, line_number - 1)
    end = min(len(lines), start + window)
    bespoke_pending = False

    option_match = MENU_OPTION_RE.match(lines[start]) if start < len(lines) else None
    option_indent = option_match.group("indent") if option_match else None

    for idx in range(start, end):
        if idx > start and option_indent is not None:
            sibling = MENU_OPTION_RE.match(lines[idx])
            if sibling and sibling.group("indent") == option_indent:
                break

        line = lines[idx]
        if BESPOKE_COMMENT_RE.search(line):
            bespoke_pending = True
        if balanced := parse_balanced_effect_line(line):
            return balanced
        if effects := parse_apply_effects_line(line):
            effects.kind = "bespoke" if bespoke_pending else "bespoke"
            return effects

    return ExtractedEffect(kind="none")


def resolve_profile_kwargs(
    effect: ExtractedEffect,
    *,
    config: dict[str, Any] | None = None,
) -> dict[str, int]:
    import balance_resolver

    cfg = config or balance_resolver.load_profiles()
    intensity_override = effect.intensity if effect.intensity != "standard" else "standard"
    witness = effect.witness or None
    return balance_resolver.resolve_balanced_effect(
        effect.profile,
        intensity_override=intensity_override,
        witness=witness,
        base_witness=effect.base_witness,
        config=cfg,
    )


def kwargs_to_delta_columns(kwargs: dict[str, int]) -> dict[str, str]:
    row: dict[str, str] = {field: "" for field in CATALOGUE_DELTA_FIELDS}
    for key, value in kwargs.items():
        column = KWARG_TO_DELTA.get(key)
        if column and value != 0:
            row[column] = str(value)
    return row


def effect_to_catalogue_columns(
    effect: ExtractedEffect,
    *,
    config: dict[str, Any] | None = None,
) -> dict[str, str]:
    columns = {
        "effect_profile": "",
        "effect_intensity": "",
        "effect_witness": "",
        "effect_base_witness": "",
        "effect_resolved_from_profile": "",
        **{field: "" for field in CATALOGUE_DELTA_FIELDS},
    }

    if effect.kind == "none":
        return columns

    if effect.kind == "profile":
        columns["effect_profile"] = effect.profile
        columns["effect_intensity"] = str(effect.intensity)
        columns["effect_witness"] = effect.witness
        columns["effect_base_witness"] = "true" if effect.base_witness else "false"
        columns["effect_resolved_from_profile"] = "true"
        kwargs = resolve_profile_kwargs(effect, config=config)
        columns.update(kwargs_to_delta_columns(kwargs))
        return columns

    columns["effect_resolved_from_profile"] = "false"
    if effect.kwargs:
        columns.update(kwargs_to_delta_columns(effect.kwargs))
    return columns


def _int_field(row: dict[str, str], field: str) -> int:
    value = (row.get(field) or "").strip()
    if not value:
        return 0
    return int(float(value))


def validate_catalogue_row(row: dict[str, str], *, config: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    choice_id = row.get("choice_id") or row.get("grain_id") or "?"
    profile = (row.get("effect_profile") or "").strip()
    resolved_flag = (row.get("effect_resolved_from_profile") or "").strip().lower()

    if profile:
        if resolved_flag not in {"true", "1", "yes"}:
            errors.append(f"{choice_id}: effect_profile set but effect_resolved_from_profile is not true")
            return errors

        intensity_raw = (row.get("effect_intensity") or "standard").strip()
        witness = (row.get("effect_witness") or "").strip() or None
        base_witness = (row.get("effect_base_witness") or "").strip().lower() in {"true", "1", "yes"}

        if intensity_raw.replace(".", "", 1).isdigit():
            intensity: str | float = float(intensity_raw)
        else:
            intensity = intensity_raw or "standard"

        import balance_resolver

        cfg = config or balance_resolver.load_profiles()
        try:
            expected = balance_resolver.resolve_balanced_effect(
                profile,
                intensity_override=intensity,
                witness=witness,
                base_witness=base_witness,
                config=cfg,
            )
        except ValueError as exc:
            errors.append(f"{choice_id}: {exc}")
            return errors

        expected_cols = kwargs_to_delta_columns(expected)
        for field in CATALOGUE_DELTA_FIELDS:
            if _int_field(row, field) != _int_field(expected_cols, field):
                errors.append(
                    f"{choice_id}: {field} mismatch (catalogue={row.get(field)!r}, resolved={expected_cols.get(field)!r})"
                )
        return errors

    if resolved_flag in {"true", "1", "yes"}:
        errors.append(f"{choice_id}: effect_resolved_from_profile=true without effect_profile")

    return errors


def validate_choice_catalogue(path: Path, *, config: dict[str, Any] | None = None) -> list[str]:
    if not path.exists():
        return [f"Missing choice catalogue: {path}"]
    errors: list[str] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            errors.extend(validate_catalogue_row(row, config=config))
    return errors


def profile_usage_summary(path: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not path.exists():
        return counts
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            profile = (row.get("effect_profile") or "").strip()
            if not profile:
                continue
            intensity = (row.get("effect_intensity") or "standard").strip() or "standard"
            key = f"{profile}_{intensity}"
            counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))
