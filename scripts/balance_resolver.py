#!/usr/bin/env python3
"""Canonical semantic balance profile resolver for lint, CSV checks, and tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

SCALE_PRECISION = 6

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILES_PATH = (
    ROOT / "main-game" / "draft" / "releases" / "planning" / "balance" / "effect_profiles.yaml"
)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _clean_scale(value: Any) -> float:
    return round(float(value), SCALE_PRECISION)


def load_profiles(path: Path | None = None) -> dict[str, Any]:
    """Load balance profile configuration from YAML."""
    profile_path = path or DEFAULT_PROFILES_PATH
    if yaml is None:
        raise RuntimeError("PyYAML is required to load effect_profiles.yaml")
    if not profile_path.exists():
        raise FileNotFoundError(f"Balance profile source missing: {profile_path}")
    data = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid balance profile YAML: {profile_path}")
    return {
        "stat_units": dict(data["stat_units"]),
        "intensities": dict(data["intensities"]),
        "valid_witnesses": tuple(data["valid_witnesses"]),
        "profiles": dict(data["profiles"]),
    }


def _resolve_balance_amount(
    stat_key: str,
    intensity_key: Any,
    scale_modifier: float,
    config: dict[str, Any],
) -> int:
    if intensity_key is None:
        return 0

    stat_units = config["stat_units"]
    intensities = config["intensities"]

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


def _resolve_intensity_scale_modifier(intensity_override: Any, config: dict[str, Any]) -> float:
    intensities = config["intensities"]

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


def resolve_balanced_effect(
    profile: str,
    intensity_override: str | float | None = None,
    witness: str | None = None,
    base_witness: bool = False,
    *,
    config: dict[str, Any] | None = None,
) -> dict[str, int]:
    """Translate a semantic profile into concrete apply_effects kwargs."""
    cfg = config or load_profiles()
    profiles = cfg["profiles"]
    valid_witnesses = cfg["valid_witnesses"]

    if profile not in profiles:
        raise ValueError(f"Unknown balance profile: {profile}")

    if witness is not None and witness not in valid_witnesses:
        raise ValueError(
            f"Unknown witness '{witness}'. Must be one of: {', '.join(valid_witnesses)}"
        )

    spec = profiles[profile]
    kwargs: dict[str, int] = {}
    scale_mod = _resolve_intensity_scale_modifier(intensity_override, cfg)

    if "insp" in spec:
        kwargs["insp"] = _resolve_balance_amount("insp", spec["insp"], scale_mod, cfg)

    if "corr" in spec:
        kwargs["corr"] = _resolve_balance_amount("corr", spec["corr"], scale_mod, cfg)

    if "witness_susp" in spec:
        if witness is None:
            raise ValueError(f"Profile '{profile}' requires a named witness parameter.")

        amount = _resolve_balance_amount("susp", spec["witness_susp"], scale_mod, cfg)
        key = f"{witness}_base" if base_witness else f"{witness}_susp"
        kwargs[key] = amount

    return kwargs
