#!/usr/bin/env python3
"""Validate agent handoff JSON contracts (stdlib only)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CONTRACT_VERSION = "1"

GATE_VERDICTS: dict[str, tuple[str, ...]] = {
    "lead_narrative": ("PASS", "REJECT"),
    "forensic_psychology": (
        "PSYCHOLOGICALLY_CONSISTENT",
        "PROFILE_UPDATE_REQUIRED",
        "PSYCHOLOGICAL_DRIFT",
        "PSYCHOLOGY_PRESERVED",
        "PSYCHOLOGY_REGRESSION",
    ),
    "victorian": (
        "HISTORICALLY_SOUND",
        "MINOR_ANACHRONISM",
        "MAJOR_VIOLATION",
    ),
}

BLOCKING_VERDICTS = frozenset(
    {
        "REJECT",
        "PSYCHOLOGICAL_DRIFT",
        "PSYCHOLOGY_REGRESSION",
        "MAJOR_VIOLATION",
    }
)

DAY_ID_RE = re.compile(r"^day[0-9]{3}$")


def _err(path: str, message: str) -> str:
    return f"{path}: {message}"


def _require_str(data: dict, key: str, errors: list[str], path: str = "") -> str | None:
    prefix = f"{path}.{key}" if path else key
    if key not in data:
        errors.append(_err(prefix, "required"))
        return None
    val = data[key]
    if not isinstance(val, str) or not val.strip():
        errors.append(_err(prefix, "must be a non-empty string"))
        return None
    return val


def _verdict_in_markdown(md_content: str, verdict: str) -> bool:
    """Match JSON verdict (underscores) to markdown ## Verdict (often spaces)."""
    if "## Verdict" not in md_content:
        return False
    section = md_content.split("## Verdict", 1)[1].upper()
    spaced = verdict.replace("_", " ")
    return verdict.upper() in section or spaced.upper() in section


def normalize_verdict_for_json(gate: str, md_verdict_line: str) -> str | None:
    """Best-effort map from markdown bold verdict to JSON enum."""
    upper = md_verdict_line.upper()
    for candidate in GATE_VERDICTS.get(gate, ()):
        if candidate.replace("_", " ") in upper or candidate in upper:
            return candidate
    return None


def validate_gate_verdict(data: Any, *, path: str = "gate") -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return [_err(path, "must be a JSON object")]

    version = _require_str(data, "contract_version", errors, path)
    if version and version != CONTRACT_VERSION:
        errors.append(_err(f"{path}.contract_version", f"must be {CONTRACT_VERSION!r}"))

    day_id = _require_str(data, "day_id", errors, path)
    if day_id and not DAY_ID_RE.match(day_id):
        errors.append(_err(f"{path}.day_id", "must match dayNNN"))

    _require_str(data, "release", errors, path)
    gate = _require_str(data, "gate", errors, path)
    verdict = _require_str(data, "verdict", errors, path)

    if gate and gate not in GATE_VERDICTS:
        errors.append(_err(f"{path}.gate", f"must be one of {list(GATE_VERDICTS)}"))
    if gate and verdict and verdict not in GATE_VERDICTS[gate]:
        errors.append(
            _err(
                f"{path}.verdict",
                f"for gate {gate!r} must be one of {GATE_VERDICTS[gate]}",
            )
        )

    if "blocking" not in data:
        errors.append(_err(f"{path}.blocking", "required"))
    elif not isinstance(data["blocking"], bool):
        errors.append(_err(f"{path}.blocking", "must be boolean"))
    elif verdict and data["blocking"] != (verdict in BLOCKING_VERDICTS):
        errors.append(
            _err(
                f"{path}.blocking",
                f"must be {verdict in BLOCKING_VERDICTS} for verdict {verdict!r}",
            )
        )

    files = data.get("reviewed_files")
    if not isinstance(files, list) or not files:
        errors.append(_err(f"{path}.reviewed_files", "must be a non-empty array"))
    elif not all(isinstance(f, str) and f.strip() for f in files):
        errors.append(_err(f"{path}.reviewed_files", "must contain non-empty strings"))

    follow = data.get("follow_up")
    if follow is not None and not isinstance(follow, dict):
        errors.append(_err(f"{path}.follow_up", "must be an object"))

    return errors


def validate_narrative_change_brief(data: Any, *, path: str = "brief") -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return [_err(path, "must be a JSON object")]

    version = _require_str(data, "contract_version", errors, path)
    if version and version != CONTRACT_VERSION:
        errors.append(_err(f"{path}.contract_version", f"must be {CONTRACT_VERSION!r}"))

    day_id = _require_str(data, "day_id", errors, path)
    if day_id and not DAY_ID_RE.match(day_id):
        errors.append(_err(f"{path}.day_id", "must match dayNNN"))

    _require_str(data, "release", errors, path)

    status = _require_str(data, "status", errors, path)
    if status and status not in ("OPEN", "IN_WRITERS_ROOM", "GATED", "CLOSED"):
        errors.append(_err(f"{path}.status", "invalid enum"))

    scale = _require_str(data, "scale", errors, path)
    if scale and scale not in ("S", "M", "L"):
        errors.append(_err(f"{path}.scale", "must be S, M, or L"))

    invoked = _require_str(data, "invoked_by", errors, path)
    allowed_invokers = (
        "non_prod_code_agent",
        "lead_narrative_editor",
        "forensic_psychology_consultant",
        "chief_architect",
        "human",
    )
    if invoked and invoked not in allowed_invokers:
        errors.append(_err(f"{path}.invoked_by", f"must be one of {allowed_invokers}"))

    labels = data.get("affected_labels")
    if not isinstance(labels, list):
        errors.append(_err(f"{path}.affected_labels", "must be an array"))
    elif scale == "S" and not labels:
        pass  # S may target inline edits; empty allowed with note in md
    elif scale in ("M", "L") and not labels:
        errors.append(_err(f"{path}.affected_labels", "required non-empty for scale M/L"))

    personas = data.get("personas", [])
    if personas:
        valid = {"thematic", "humour", "tension", "erotic", "mystery", "class"}
        bad = [p for p in personas if p not in valid]
        if bad:
            errors.append(_err(f"{path}.personas", f"invalid: {bad}"))

    return errors


def validate_profile_delta(data: Any, *, path: str = "profile_delta") -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return [_err(path, "must be a JSON object")]

    version = _require_str(data, "contract_version", errors, path)
    if version and version != CONTRACT_VERSION:
        errors.append(_err(f"{path}.contract_version", f"must be {CONTRACT_VERSION!r}"))

    _require_str(data, "character_id", errors, path)
    day_id = _require_str(data, "day_id", errors, path)
    if day_id and not DAY_ID_RE.match(day_id):
        errors.append(_err(f"{path}.day_id", "must match dayNNN"))

    _require_str(data, "release", errors, path)
    verdict = _require_str(data, "verdict", errors, path)
    if verdict and verdict not in ("PROFILE_DOCUMENTED", "PROFILE_UPDATE_REQUIRED", "NO_CHANGE"):
        errors.append(_err(f"{path}.verdict", "invalid enum"))

    edits = data.get("edits")
    if not isinstance(edits, list):
        errors.append(_err(f"{path}.edits", "must be an array"))
    elif verdict == "PROFILE_UPDATE_REQUIRED" and not edits:
        errors.append(_err(f"{path}.edits", "required when verdict is PROFILE_UPDATE_REQUIRED"))
    elif verdict == "NO_CHANGE" and edits:
        errors.append(_err(f"{path}.edits", "must be empty when verdict is NO_CHANGE"))

    for i, edit in enumerate(edits if isinstance(edits, list) else []):
        if not isinstance(edit, dict):
            errors.append(_err(f"{path}.edits[{i}]", "must be an object"))
            continue
        _require_str(edit, "file", errors, f"{path}.edits[{i}]")
        _require_str(edit, "change_type", errors, f"{path}.edits[{i}]")
        _require_str(edit, "summary", errors, f"{path}.edits[{i}]")
        ct = edit.get("change_type")
        if ct and ct not in ("add", "refine", "remove", "flag_contradiction"):
            errors.append(_err(f"{path}.edits[{i}].change_type", "invalid enum"))

    return errors


def validate_promotion_handoff(data: Any, *, path: str = "promotion") -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return [_err(path, "must be a JSON object")]

    version = _require_str(data, "contract_version", errors, path)
    if version and version != CONTRACT_VERSION:
        errors.append(_err(f"{path}.contract_version", f"must be {CONTRACT_VERSION!r}"))

    day_id = _require_str(data, "day_id", errors, path)
    if day_id and not DAY_ID_RE.match(day_id):
        errors.append(_err(f"{path}.day_id", "must match dayNNN"))

    _require_str(data, "release", errors, path)
    _require_str(data, "source_non_canon", errors, path)
    _require_str(data, "target_prod", errors, path)

    if "creative_text_preserved" not in data:
        errors.append(_err(f"{path}.creative_text_preserved", "required"))
    elif not isinstance(data["creative_text_preserved"], bool):
        errors.append(_err(f"{path}.creative_text_preserved", "must be boolean"))
    elif data["creative_text_preserved"] is False:
        errors.append(_err(f"{path}.creative_text_preserved", "must be true for promotion"))

    return errors


def load_json_file(path: Path) -> tuple[Any | None, list[str]]:
    if not path.exists():
        return None, [f"Missing JSON: {path.relative_to(ROOT).as_posix()}"]
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as exc:
        return None, [f"Invalid JSON {path.relative_to(ROOT).as_posix()}: {exc}"]


def gate_json_path(archive_dir: Path, day_id: str, gate_slug: str) -> Path:
    return archive_dir / f"{day_id}_gate_{gate_slug}.json"


def check_gate_json_sidecar(
    archive_dir: Path,
    day_id: str,
    release: str,
    gate_slug: str,
    md_path: Path,
) -> list[str]:
    """Validate JSON sidecar exists and matches markdown gate."""
    errors: list[str] = []
    json_path = gate_json_path(archive_dir, day_id, gate_slug)
    data, load_errors = load_json_file(json_path)
    errors.extend(load_errors)
    if data is None:
        return errors

    errors.extend(validate_gate_verdict(data, path=json_path.name))

    if data.get("day_id") != day_id:
        errors.append(_err(json_path.name, f"day_id must be {day_id!r}"))
    release_val = data.get("release")
    if release_val != release:
        from narrative_paths import normalize_release_slug, release_display_name

        slug = normalize_release_slug(release)
        allowed = {release, slug, release_display_name(slug)}
        if release_val not in allowed:
            errors.append(
                _err(json_path.name, f"release must match {release!r} (or slug {slug!r})")
            )
    if data.get("gate") != gate_slug:
        errors.append(_err(json_path.name, f"gate must be {gate_slug!r}"))

    if md_path.exists():
        md = md_path.read_text(encoding="utf-8")
        verdict = data.get("verdict")
        if isinstance(verdict, str) and not _verdict_in_markdown(md, verdict):
            errors.append(
                _err(
                    json_path.name,
                    f"verdict {verdict!r} not found in {md_path.name} ## Verdict section",
                )
            )

    return errors
