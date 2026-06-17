#!/usr/bin/env python3
"""Writers' room pipeline artifact checks (convergent report, spec scripts, gate verdicts)."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from narrative_paths import (  # noqa: E402
    DayContext,
    draft_day_dir,
    draft_release_root,
    parse_non_canon_path,
    pipeline_gates_dir,
    pipeline_handoffs_dir,
    pipeline_specs_dir,
    pipeline_synthesis_dir,
)

ROOT = Path(__file__).resolve().parents[1]

GATE_SPECS = (
    {
        "slug": "lead_narrative",
        "filename": "{day_id}_gate_lead_narrative.md",
        "verdicts": ("PASS", "REJECT"),
    },
    {
        "slug": "forensic_psychology",
        "filename": "{day_id}_gate_forensic_psychology.md",
        "verdicts": (
            "PSYCHOLOGICALLY CONSISTENT",
            "PROFILE UPDATE REQUIRED",
            "PSYCHOLOGICAL DRIFT",
            "PSYCHOLOGY PRESERVED",
            "PSYCHOLOGY REGRESSION",
        ),
    },
    {
        "slug": "victorian",
        "filename": "{day_id}_gate_victorian.md",
        "verdicts": (
            "HISTORICALLY SOUND",
            "MINOR ANACHRONISM",
            "MAJOR VIOLATION",
        ),
    },
)


def writers_room_release_dir(ctx: DayContext) -> Path:
    return draft_release_root(ctx.release_slug)


def check_convergent_report(ctx: DayContext) -> list[str]:
    errors: list[str] = []
    report_path = pipeline_synthesis_dir(ctx) / f"{ctx.day_id}_convergent_report.md"
    rel = report_path.relative_to(ROOT).as_posix()
    if not report_path.exists():
        errors.append(f"Missing convergent report: {rel}")
    elif _is_placeholder(report_path.read_text(encoding="utf-8")):
        errors.append(f"Convergent report empty or placeholder: {rel}")
    return errors


def check_spec_scripts(ctx: DayContext) -> list[str]:
    errors: list[str] = []
    spec_dir = pipeline_specs_dir(ctx)
    rel_dir = spec_dir.relative_to(ROOT).as_posix()
    if not spec_dir.exists():
        errors.append(f"Spec scripts directory missing: {rel_dir}")
        return errors
    specs = list(spec_dir.glob(f"{ctx.day_id}_*_spec.rpy"))
    if not specs:
        errors.append(f"No spec scripts in {rel_dir} for {ctx.day_id}")
    return errors


def _is_placeholder(content: str) -> bool:
    stripped = content.strip()
    if len(stripped) < 50:
        return True
    lower = stripped.lower()
    if "todo" in lower or "tbd" in lower:
        return True
    if re.search(r"(?<![/w-])/bplaceholder/b(?![/w-])", lower):
        if not re.search(r"asset placeholders?", lower):
            return True
    return False


def _has_verdict(content: str, verdicts: tuple[str, ...]) -> bool:
    if "## Verdict" not in content:
        return False
    after = content.split("## Verdict", 1)[1]
    upper = after.upper()
    return any(v in upper for v in verdicts)


def check_gate_file(ctx: DayContext, spec: dict, *, require_json: bool = True) -> list[str]:
    errors: list[str] = []
    path = pipeline_gates_dir(ctx) / spec["filename"].format(day_id=ctx.day_id)
    rel = path.relative_to(ROOT).as_posix()
    if not path.exists():
        errors.append(f"Missing gate file: {rel}")
        return errors
    content = path.read_text(encoding="utf-8")
    if _is_placeholder(content):
        errors.append(f"Gate file empty or placeholder: {rel}")
    elif not _has_verdict(content, spec["verdicts"]):
        errors.append(
            f"Gate file missing ## Verdict with expected label: {rel} "
            f"(expected one of: {', '.join(spec['verdicts'])})"
        )

    if require_json:
        try:
            from contract_schemas import check_gate_json_sidecar

            errors.extend(
                check_gate_json_sidecar(
                    pipeline_gates_dir(ctx),
                    ctx.day_id,
                    ctx.release_name,
                    spec["slug"],
                    path,
                )
            )
        except ImportError:
            pass

    return errors


def check_gates(
    ctx: DayContext,
    *,
    partial_ok: bool = True,
    require_json: bool = True,
) -> list[str]:
    gates = pipeline_gates_dir(ctx)
    existing = [
        spec
        for spec in GATE_SPECS
        if (gates / spec["filename"].format(day_id=ctx.day_id)).exists()
    ]
    if partial_ok and not existing:
        return []
    if len(existing) not in (0, 3):
        missing = [
            spec["filename"].format(day_id=ctx.day_id)
            for spec in GATE_SPECS
            if not (gates / spec["filename"].format(day_id=ctx.day_id)).exists()
        ]
        return [
            f"Incomplete gate set for {ctx.day_id}: found {len(existing)}/3. "
            f"Missing: {', '.join(missing)}"
        ]
    errors: list[str] = []
    for spec in GATE_SPECS:
        errors.extend(check_gate_file(ctx, spec, require_json=require_json))
    return errors


def check_narrative_change_brief(ctx: DayContext) -> list[str]:
    brief_md = draft_day_dir(ctx) / "briefs" / f"{ctx.day_id}_narrative_change_brief.md"
    if not brief_md.exists():
        return []

    errors: list[str] = []
    brief_json = draft_day_dir(ctx) / "briefs" / f"{ctx.day_id}_narrative_change_brief.json"
    try:
        from contract_schemas import load_json_file, validate_narrative_change_brief

        data, load_errors = load_json_file(brief_json)
        errors.extend(load_errors)
        if data is not None:
            errors.extend(validate_narrative_change_brief(data))
            if data.get("day_id") != ctx.day_id:
                errors.append(f"{brief_json.name}: day_id must be {ctx.day_id!r}")
            release = data.get("release")
            if release not in (ctx.release_name, ctx.release_slug):
                errors.append(
                    f"{brief_json.name}: release must be {ctx.release_name!r} "
                    f"or {ctx.release_slug!r}"
                )
    except ImportError:
        pass
    return errors


def validate_day_pipeline(
    file_str: str,
    *,
    require_gates: bool = True,
    partial_gates: bool = True,
    require_json_contracts: bool = True,
) -> tuple[int, list[str]]:
    file_path = ROOT / file_str
    ctx = parse_non_canon_path(file_path)
    if ctx is None:
        return 0, []

    messages: list[str] = []
    failures = 0

    messages.append(
        f"== Writers' Room Pipeline: {ctx.day_id} ({ctx.release_slug}) =="
    )

    for check_fn, label in (
        (check_convergent_report, "convergent report"),
        (check_spec_scripts, "spec scripts"),
    ):
        errs = check_fn(ctx)
        if errs:
            failures += len(errs)
            for err in errs:
                messages.append(f"  [ERROR] {err}")
        else:
            messages.append(f"  [OK] {label}")

    if require_gates:
        gate_errs = check_gates(
            ctx,
            partial_ok=partial_gates,
            require_json=require_json_contracts,
        )
        if gate_errs:
            failures += len(gate_errs)
            for err in gate_errs:
                messages.append(f"  [ERROR] {err}")
        elif partial_gates and not any(
            (pipeline_gates_dir(ctx) / s["filename"].format(day_id=ctx.day_id)).exists()
            for s in GATE_SPECS
        ):
            messages.append(
                "  [WARN] No gate verdict files yet — required before promotion "
                f"(see main-game/pipeline/releases/{ctx.release_slug}/days/"
                f"{ctx.day_id}/gates/)"
            )
        else:
            messages.append("  [OK] all three gate verdicts (markdown + JSON)")

    brief_errs = check_narrative_change_brief(ctx)
    if brief_errs:
        failures += len(brief_errs)
        for err in brief_errs:
            messages.append(f"  [ERROR] {err}")
    elif (draft_day_dir(ctx) / "briefs" / f"{ctx.day_id}_narrative_change_brief.md").exists():
        messages.append("  [OK] narrative change brief JSON")

    return failures, messages


# Re-export for contract_validate.py
def archive_dir(ctx: DayContext) -> Path:
    """Gate JSON sidecars live alongside gate markdown in pipeline/gates/."""
    return pipeline_gates_dir(ctx)


def spec_scripts_dir(ctx: DayContext) -> Path:
    return pipeline_specs_dir(ctx)
