#!/usr/bin/env python3
"""Canonical semantic balance profile resolver for lint, CSV checks, and tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILES_PATH = (
    ROOT / "main-game" / "draft" / "releases" / "planning" / "balance" / "effect_profiles.yaml"
)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


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
        "schema_version": data.get("schema_version", 1),
        "valid_witnesses": tuple(data["valid_witnesses"]),
        "active_intensities": tuple(data.get("active_intensities", ())),
        "migration_mode": data.get("migration_mode", {}),
        "profiles": dict(data["profiles"]),
    }


def resolve_balanced_effect(
    profile: str,
    intensity_override: str | float | None = "standard",
    witness: str | None = None,
    base_witness: bool = False,
    *,
    config: dict[str, Any] | None = None,
    allow_inactive: bool = False,
) -> dict[str, int]:
    """Translate a semantic profile into concrete apply_effects kwargs."""
    cfg = config or load_profiles()
    profiles = cfg.get("profiles", {})
    valid_witnesses = cfg.get("valid_witnesses", ())
    schema_version = cfg.get("schema_version", 1)

    if schema_version != 2:
        raise ValueError(f"Unsupported schema version: {schema_version}. Expected version 2.")

    if profile not in profiles:
        raise ValueError(f"Unknown balance profile: {profile}")

    prof_data = profiles[profile]
    if not allow_inactive and not prof_data.get("active", False):
        raise ValueError(f"Profile '{profile}' is inactive.")

    intensity = intensity_override if intensity_override is not None else "standard"

    if _is_number(intensity):
        raise ValueError(f"Numeric intensity override not supported in schema v2: {intensity}")

    active_intensities = cfg.get("active_intensities", ())
    if intensity not in active_intensities:
        raise ValueError(f"Inactive or unknown intensity: {intensity}")

    if base_witness and prof_data.get("active", False):
        raise ValueError("base_witness=True is not allowed for active profiles during this migration pass.")

    # Get deltas block
    deltas = prof_data.get("deltas", {}).get(intensity, {})
    
    kwargs: dict[str, int] = {}
    if deltas.get("insp", 0) != 0:
        kwargs["insp"] = deltas["insp"]
    if deltas.get("corr", 0) != 0:
        kwargs["corr"] = deltas["corr"]

    witness_susp = deltas.get("witness_susp", 0)
    if witness_susp != 0:
        if witness is None:
            raise ValueError(f"Profile '{profile}' requires a named witness parameter.")
        if witness not in valid_witnesses:
            raise ValueError(f"Unknown witness '{witness}'. Must be one of: {', '.join(valid_witnesses)}")
        key = f"{witness}_base" if base_witness else f"{witness}_susp"
        kwargs[key] = witness_susp

    return kwargs
