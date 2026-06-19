#!/usr/bin/env python3
"""Static testing and balance report for Release 1 MVP (non-prod sandbox).

This is a narrow first pass: file presence, gate evidence, fail-state wiring,
deprecated-router guards, and documented balance assumptions. It does not
simulate full route execution or replace the storyboard.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Iterable

import sys

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from narrative_paths import (  # noqa: E402
    DayContext,
    DEFAULT_RELEASE_SLUG,
    draft_day_dir,
    draft_non_canon_path,
    draft_shared_dir,
    non_prod_game_dir,
    normalize_release_slug,
    pipeline_release_root,
    planning_dir,
)


class Severity(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    INCOMPLETE = "INCOMPLETE"


@dataclass
class CheckResult:
    severity: Severity
    message: str
    evidence: str = ""

    def icon(self) -> str:
        return {
            Severity.PASS: "✓",
            Severity.WARN: "⚠",
            Severity.FAIL: "✗",
            Severity.INCOMPLETE: "…",
        }[self.severity]


@dataclass
class BalanceReport:
    release_slug: str
    day_filter: str | None
    generated_at: str
    checked_files: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    required_files: list[CheckResult] = field(default_factory=list)
    manuscript_gates: list[CheckResult] = field(default_factory=list)
    corruption_progression: list[CheckResult] = field(default_factory=list)
    fail_states: list[CheckResult] = field(default_factory=list)
    soft_fail: list[CheckResult] = field(default_factory=list)
    deprecated_routers: list[CheckResult] = field(default_factory=list)
    framework_artifacts: list[CheckResult] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    recommended_next: list[str] = field(default_factory=list)

    def verdict(self) -> Severity:
        all_checks = (
            self.required_files
            + self.manuscript_gates
            + self.corruption_progression
            + self.fail_states
            + self.soft_fail
            + self.deprecated_routers
            + self.framework_artifacts
        )
        if any(c.severity == Severity.FAIL for c in all_checks):
            return Severity.FAIL
        if any(c.severity == Severity.INCOMPLETE for c in all_checks):
            return Severity.INCOMPLETE
        if any(c.severity == Severity.WARN for c in all_checks):
            return Severity.WARN
        return Severity.PASS

    def to_markdown(self) -> str:
        lines: list[str] = [
            "# Testing and balance report",
            "",
            f"**Release:** `{self.release_slug}`",
            f"**Generated:** {self.generated_at}",
        ]
        if self.day_filter:
            lines.append(f"**Scope:** `{self.day_filter}` only (+ shared dependencies)")
        lines.extend(
            [
                "",
                "## Verdict",
                "",
                f"**{self.verdict().value}**",
                "",
                "> Static structure checks only. Route simulation, runtime capture, and",
                "> policy fuzz are not part of this first pass.",
                "",
                "## Checked files",
                "",
            ]
        )
        if self.checked_files:
            for path in self.checked_files:
                lines.append(f"- `{path}`")
        else:
            lines.append("- _(none)_")

        lines.extend(["", "## Route/balance assumptions", ""])
        for item in self.assumptions:
            lines.append(f"- {item}")

        for title, checks in (
            ("Manuscript gate checks", self.manuscript_gates),
            ("Corruption/inspiration progression checks", self.corruption_progression),
            ("Fail-state checks", self.fail_states),
            ("Soft-fail checks", self.soft_fail),
            ("Deprecated-router checks", self.deprecated_routers),
            ("Grain manifest and balance model checks", self.framework_artifacts),
        ):
            lines.extend(["", f"## {title}", ""])
            if checks:
                for check in checks:
                    line = f"- {check.icon()} **{check.severity.value}** — {check.message}"
                    if check.evidence:
                        line += f" (`{check.evidence}`)"
                    lines.append(line)
            else:
                lines.append("- _(no checks in scope)_")

        lines.extend(["", "## Required day files", ""])
        for check in self.required_files:
            line = f"- {check.icon()} **{check.severity.value}** — {check.message}"
            if check.evidence:
                line += f" (`{check.evidence}`)"
            lines.append(line)

        lines.extend(["", "## Missing evidence", ""])
        if self.missing_evidence:
            for item in self.missing_evidence:
                lines.append(f"- {item}")
        else:
            lines.append("- None flagged by static checks.")

        lines.extend(["", "## Recommended next tests", ""])
        for item in self.recommended_next:
            lines.append(f"- {item}")

        lines.append("")
        return "\n".join(lines)


# Design targets documented when no machine-readable catalogue exists yet.
BALANCE_ASSUMPTIONS = [
    "Corruption Rank 1 is the starting state; prologue should leave the player able to reach Level 2 before Day 2 book writing.",
    "Level 2 is required for Day 101/102 Chapter 1 gates (`WRITE_GATE_CH1` corruption floor = 2).",
    "Level 3 is required for Chapter 2+ gates and is the soft-fail floor at Day 5 reckoning (`WRITE_GATE_CH2` corruption floor = 3).",
    "Level 4 is the intended optimized-path milestone by end of Day 4 (not yet statically provable without simulation).",
    "Cautious players may reach Day 2 but write weaker chapters (Day 101 slop path when `corruption_level <= WRITE_SLOP_MAX_CORRUPTION_LEVEL`).",
    "Passive/low-corruption play should route to `bad_ending_rejection` (respectable-writer soft fail), not a silent hard lock.",
    "Risky paths may reach MVP ending (`day105_7_release_one_ending`) but can trigger hard fails (`game_over_*`).",
    "Writing gates use AND semantics: both inspiration and corruption_level must clear (`has_story_fuel`).",
]

REQUIRED_DAY_IDS = ("day101", "day102", "day103", "day104", "day105")

WRITE_GATE_PATTERN = re.compile(
    r"WRITE_GATE_CH(?P<ch>[123])\s*=\s*\(\s*(?P<insp>\d+)\s*,\s*(?P<corr>\d+)\s*\)"
)
LABEL_PATTERN = re.compile(r"^label\s+([a-zA-Z0-9_]+)\s*:", re.MULTILINE)

DEPRECATED_JUMP_PATTERNS = (
    re.compile(r"^\s*jump\s+end_slot\s*$", re.MULTILINE),
    re.compile(r"^\s*jump\s+advance_after_confrontation\s*$", re.MULTILINE),
)

GATE_SLOT_EXPECTATIONS: tuple[tuple[str, str, str], ...] = (
    ("day101_non_canon.rpy", "WRITE_GATE_CH1", "Day 101 night write menu"),
    ("day102_non_canon.rpy", "WRITE_GATE_CH1", "Day 102 Ch1 catch-up"),
    ("day102_non_canon.rpy", "WRITE_GATE_CH2", "Day 102 Ch2 write"),
    ("day103_non_canon.rpy", "WRITE_GATE_CH3", "Day 103 Ch3 write"),
)

FAIL_LABELS: tuple[tuple[str, str, str], ...] = (
    ("game_over_dismissed", "endings.rpy", "Anxiety ≥ 100 dismissal"),
    ("game_over_deadline_1", "day103_non_canon.rpy", "No Ch1 by Day 3 morning"),
    ("game_over_deadline_2", "day104_non_canon.rpy", "manuscript_progress < 2 by Day 4 close"),
    ("bad_ending_rejection", "day105_non_canon.rpy", "corruption_level < 3 at reckoning"),
)

BOOK1_ARTIFACTS: tuple[tuple[str, str], ...] = (
    ("book1_non_canon.rpy", "label book1_write_chapter"),
    ("day101_non_canon.rpy", "call book1_write_chapter"),
    ("day102_non_canon.rpy", "call book1_write_chapter"),
    ("day103_non_canon.rpy", "call book1_write_chapter"),
    ("day104_non_canon.rpy", "call book1_write_chapter"),
    ("day105_non_canon.rpy", "call book1_write_chapter"),
)

MANUSCRIPT_CHAPTERS: tuple[tuple[str, str], ...] = (
    ("day101_non_canon.rpy", "day1_chapter"),
    ("day102_non_canon.rpy", "day2_chapter"),
    ("day103_non_canon.rpy", "day3_chapter"),
    ("day104_non_canon.rpy", "day4_triumphant_chapter"),
    ("day105_non_canon.rpy", "day5_reckoning_chapter"),
)

BALANCE_MODEL_FILES: tuple[tuple[str, str], ...] = (
    ("balance/gate_catalogue.csv", "gate_catalogue"),
    ("balance/run_policies.csv", "run_policies"),
    ("balance/balance_targets.yaml", "balance_targets"),
    ("balance/choice_catalogue.csv", "choice_catalogue"),
)

SIMULATION_OUTPUTS: tuple[tuple[str, str], ...] = (
    ("balance/simulation_report.md", "simulation_report"),
    ("balance/policy_results.csv", "policy_results"),
    ("balance/gate_results.csv", "gate_results"),
)

EXPECTED_CATALOGUE_GATES = (
    "ch1_write_gate",
    "ch2_write_gate",
    "ch3_write_gate",
    "deadline_ch1",
    "deadline_ch2",
    "soft_fail_rejection",
    "anxiety_dismissal",
)

EXPECTED_GRAIN_TYPES = (
    "write_gate",
    "deadline_gate",
    "ending",
    "book1",
)


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _day_ids_in_scope(day_filter: str | None) -> tuple[str, ...]:
    if day_filter:
        return (day_filter,)
    return REQUIRED_DAY_IDS


def _collect_scan_files(
    release_slug: str,
    day_filter: str | None,
) -> tuple[list[Path], Path, Path]:
    days_dir = draft_day_dir(DayContext("day101", release_slug))
    shared_dir = draft_shared_dir()
    functions_path = shared_dir / "functions_non_canon.rpy"
    endings_path = shared_dir / "endings.rpy"
    book1_path = days_dir / "book1_non_canon.rpy"

    files: list[Path] = []
    for day_id in _day_ids_in_scope(day_filter):
        ctx = DayContext(day_id, release_slug)
        files.append(draft_non_canon_path(ctx))

    if day_filter is None:
        files.append(book1_path)

    for extra in (functions_path, endings_path):
        if extra not in files:
            files.append(extra)

    return files, functions_path, endings_path


def _parse_write_gates(functions_text: str) -> dict[str, tuple[int, int]]:
    gates: dict[str, tuple[int, int]] = {}
    for match in WRITE_GATE_PATTERN.finditer(functions_text):
        key = f"WRITE_GATE_CH{match.group('ch')}"
        gates[key] = (int(match.group("insp")), int(match.group("corr")))
    return gates


def _labels_in(text: str) -> set[str]:
    return set(LABEL_PATTERN.findall(text))


def _contains_jump_to(text: str, label: str) -> bool:
    return bool(re.search(rf"^\s*jump\s+{re.escape(label)}\s*$", text, re.MULTILINE))


def _scan_deprecated_jumps(paths: Iterable[Path], root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    offenders: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        text = _read(path)
        for pattern in DEPRECATED_JUMP_PATTERNS:
            if pattern.search(text):
                offenders.append(_rel(path, root))
    if offenders:
        results.append(
            CheckResult(
                Severity.FAIL,
                "Deprecated router jump found in active sandbox scripts",
                ", ".join(sorted(set(offenders))),
            )
        )
    else:
        results.append(
            CheckResult(
                Severity.PASS,
                "No new `jump end_slot` or `jump advance_after_confrontation` in scanned files",
            )
        )
    return results


def _check_framework_artifacts(release_slug: str, root: Path) -> tuple[list[CheckResult], list[str], list[str]]:
    """Return checks, updated missing evidence, and recommended next tests."""
    checks: list[CheckResult] = []
    missing: list[str] = []
    next_tests: list[str] = []

    grain_dir = pipeline_release_root(release_slug) / "grain"
    manifest_path = grain_dir / "release1_grain_manifest.json"
    gaps_path = grain_dir / "release1_grain_gaps.md"
    balance_dir = planning_dir() / "balance"

    if manifest_path.exists():
        data = json.loads(_read(manifest_path))
        rel = _rel(manifest_path, root)
        grain_count = data.get("grain_count", 0)
        gap_count = data.get("gap_count", 0)
        by_type = data.get("counts", {}).get("by_type", {})
        checks.append(
            CheckResult(
                Severity.PASS,
                f"Grain manifest present ({grain_count} grains, {gap_count} gaps)",
                rel,
            )
        )
        for grain_type in EXPECTED_GRAIN_TYPES:
            count = by_type.get(grain_type, 0)
            if count:
                checks.append(
                    CheckResult(
                        Severity.PASS,
                        f"Grain type `{grain_type}` inferred ({count} grains)",
                        rel,
                    )
                )
            else:
                checks.append(
                    CheckResult(
                        Severity.WARN,
                        f"Grain type `{grain_type}` not found in manifest",
                        rel,
                    )
                )
        if gaps_path.exists():
            gaps_text = _read(gaps_path)
            blockers_block = ""
            if "## Blockers" in gaps_text:
                blockers_block = gaps_text.split("## Blockers", 1)[1].split("## Major", 1)[0]
            if "### grain_gap_" in blockers_block:
                checks.append(
                    CheckResult(
                        Severity.FAIL,
                        "Grain gap report lists blocker findings",
                        _rel(gaps_path, root),
                    )
                )
            elif "### grain_gap_" in gaps_text:
                checks.append(
                    CheckResult(
                        Severity.WARN,
                        "Grain gap report lists major/warning findings (untagged gates expected for now)",
                        _rel(gaps_path, root),
                    )
                )
            else:
                checks.append(
                    CheckResult(
                        Severity.PASS,
                        "Grain gap report has no blocker findings",
                        _rel(gaps_path, root),
                    )
                )
    else:
        checks.append(
            CheckResult(
                Severity.WARN,
                "Grain manifest missing — run `py main-game/pipeline/tools/build_grain_manifest.py`",
                _rel(grain_dir, root),
            )
        )
        missing.append("Grain manifest not generated — run build_grain_manifest before promotion prep.")
        next_tests.append("Run `py main-game/pipeline/tools/build_grain_manifest.py --release release-1-mvp`.")

    for rel_path, label in BALANCE_MODEL_FILES:
        path = balance_dir / rel_path.split("/", 1)[1]
        rel = _rel(path, root)
        if path.exists():
            checks.append(CheckResult(Severity.PASS, f"Balance model file present: {label}", rel))
        else:
            checks.append(CheckResult(Severity.WARN, f"Balance model file missing: {label}", rel))

    gate_catalogue = balance_dir / "gate_catalogue.csv"
    if gate_catalogue.exists():
        with gate_catalogue.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        gate_ids = {row["gate_id"] for row in rows if row.get("gate_id")}
        rel = _rel(gate_catalogue, root)
        for gate_id in EXPECTED_CATALOGUE_GATES:
            if gate_id in gate_ids:
                checks.append(
                    CheckResult(Severity.PASS, f"Gate catalogue row present: `{gate_id}`", rel)
                )
            else:
                checks.append(
                    CheckResult(Severity.WARN, f"Gate catalogue missing row: `{gate_id}`", rel)
                )

    choice_catalogue = balance_dir / "choice_catalogue.csv"
    if choice_catalogue.exists():
        with choice_catalogue.open(encoding="utf-8", newline="") as handle:
            choice_count = sum(1 for _ in csv.DictReader(handle))
        checks.append(
            CheckResult(
                Severity.PASS,
                f"Choice catalogue present ({choice_count} rows)",
                _rel(choice_catalogue, root),
            )
        )
    else:
        checks.append(
            CheckResult(
                Severity.INCOMPLETE,
                "Choice catalogue not yet authored (`choice_catalogue.csv`)",
                _rel(balance_dir, root),
            )
        )
        missing.append("Choice catalogue CSV not yet authored — run build_choice_catalogue.py.")

    pipeline_balance = pipeline_release_root(release_slug) / "balance"
    for rel_path, label in SIMULATION_OUTPUTS:
        path = pipeline_balance / rel_path.split("/", 1)[1]
        rel = _rel(path, root)
        if path.exists():
            checks.append(CheckResult(Severity.PASS, f"Simulation output present: {label}", rel))
        else:
            checks.append(
                CheckResult(
                    Severity.INCOMPLETE,
                    f"Simulation output missing: {label} — run simulate_balance.py",
                    rel,
                )
            )

    missing.extend(
        [
            "No Python route simulator yet — cannot prove optimized/cautious/passive paths reach intended stats.",
            "No runtime JSONL captures — cannot verify gate pass/fail at play time.",
            "Corruption Level 4 milestone by Day 4 end is design intent only until simulation exists.",
        ]
    )
    next_tests.extend(
        [
            "Review `main-game/pipeline/releases/release-1-mvp/balance/simulation_report.md` matrix gaps before tuning numbers.",
            "Run P1/P2 runtime captures when JSONL harness lands; compare to abstract sim.",
            "Implement graph-walk simulator or expand catalogue coverage for P1/P2/P3 precision.",
        ]
    )
    return checks, missing, next_tests


def build_balance_report(
    release: str = DEFAULT_RELEASE_SLUG,
    day_filter: str | None = None,
) -> BalanceReport:
    release_slug = normalize_release_slug(release)
    root = non_prod_game_dir().parents[1]
    days_dir = draft_day_dir(DayContext("day101", release_slug))
    scan_files, functions_path, endings_path = _collect_scan_files(release_slug, day_filter)

    report = BalanceReport(
        release_slug=release_slug,
        day_filter=day_filter,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        assumptions=list(BALANCE_ASSUMPTIONS),
    )

    artifact_checks, missing_evidence, recommended_next = _check_framework_artifacts(release_slug, root)
    if day_filter is None:
        report.framework_artifacts = artifact_checks
    report.missing_evidence = missing_evidence
    report.recommended_next = recommended_next + [
        "Smoke-test hard fails: skip all writing → `game_over_deadline_1`; Ch1 only → `game_over_deadline_2`; anxiety 100 → `game_over_dismissed`.",
        "Verify cautious Day 101 slop path still advances spine without bricking deadline gates.",
    ]

    report.checked_files = sorted(
        _rel(p, root) for p in scan_files if p.exists()
    )

    # --- Required day files ---
    if day_filter is None:
        for day_id in REQUIRED_DAY_IDS:
            ctx = DayContext(day_id, release_slug)
            path = draft_non_canon_path(ctx)
            rel = _rel(path, root)
            if path.exists():
                report.required_files.append(
                    CheckResult(Severity.PASS, f"Required sandbox day file present: {day_id}", rel)
                )
            else:
                report.required_files.append(
                    CheckResult(Severity.FAIL, f"Missing required sandbox day file: {day_id}", rel)
                )
    else:
        ctx = DayContext(day_filter, release_slug)
        path = draft_non_canon_path(ctx)
        rel = _rel(path, root)
        if path.exists():
            report.required_files.append(
                CheckResult(Severity.PASS, f"Scoped day file present: {day_filter}", rel)
            )
        else:
            report.required_files.append(
                CheckResult(Severity.FAIL, f"Scoped day file missing: {day_filter}", rel)
            )

    # --- Functions / gate constants ---
    if not functions_path.exists():
        report.manuscript_gates.append(
            CheckResult(Severity.FAIL, "Missing `functions_non_canon.rpy`", _rel(functions_path, root))
        )
        return report

    functions_text = _read(functions_path)
    gates = _parse_write_gates(functions_text)

    expected_gates = {
        "WRITE_GATE_CH1": (15, 2),
        "WRITE_GATE_CH2": (30, 3),
        "WRITE_GATE_CH3": (45, 3),
    }
    for gate_name, expected in expected_gates.items():
        actual = gates.get(gate_name)
        rel = _rel(functions_path, root)
        if actual == expected:
            report.manuscript_gates.append(
                CheckResult(
                    Severity.PASS,
                    f"{gate_name} = {expected} (inspiration, corruption_level)",
                    rel,
                )
            )
        elif actual is None:
            report.manuscript_gates.append(
                CheckResult(Severity.FAIL, f"{gate_name} constant not found", rel)
            )
        else:
            report.manuscript_gates.append(
                CheckResult(
                    Severity.WARN,
                    f"{gate_name} = {actual}, checklist expects {expected}",
                    rel,
                )
            )

    for const_name in ("WRITE_SLOP_MAX_CORRUPTION_LEVEL", "ANXIETY_WRITE_PARALYSIS", "has_story_fuel", "attempt_write"):
        if const_name in functions_text:
            report.manuscript_gates.append(
                CheckResult(Severity.PASS, f"`{const_name}` present in functions", _rel(functions_path, root))
            )
        else:
            report.manuscript_gates.append(
                CheckResult(Severity.FAIL, f"`{const_name}` missing from functions", _rel(functions_path, root))
            )

    # Gate usage in day files (full release or scoped day)
    for filename, gate_name, slot_desc in GATE_SLOT_EXPECTATIONS:
        day_id = filename.replace("_non_canon.rpy", "")
        if day_filter and day_id != day_filter:
            continue
        path = days_dir / filename
        rel = _rel(path, root)
        if not path.exists():
            report.manuscript_gates.append(
                CheckResult(Severity.FAIL, f"{slot_desc}: file missing", rel)
            )
            continue
        text = _read(path)
        if f"has_story_fuel(*{gate_name})" in text:
            report.manuscript_gates.append(
                CheckResult(Severity.PASS, f"{slot_desc} uses `has_story_fuel(*{gate_name})`", rel)
            )
        else:
            report.manuscript_gates.append(
                CheckResult(
                    Severity.WARN,
                    f"{slot_desc}: expected `has_story_fuel(*{gate_name})` not found",
                    rel,
                )
            )

    # Book1 + manuscript progress (release-wide)
    if day_filter is None:
        for filename, needle in BOOK1_ARTIFACTS:
            path = days_dir / filename
            rel = _rel(path, root)
            if not path.exists():
                report.manuscript_gates.append(
                    CheckResult(Severity.FAIL, f"Book1 artifact file missing: {filename}", rel)
                )
                continue
            if needle in _read(path):
                report.manuscript_gates.append(
                    CheckResult(Severity.PASS, f"`{needle}` found in {filename}", rel)
                )
            else:
                report.manuscript_gates.append(
                    CheckResult(Severity.WARN, f"`{needle}` not found in {filename}", rel)
                )

        for filename, chapter_id in MANUSCRIPT_CHAPTERS:
            path = days_dir / filename
            rel = _rel(path, root)
            if not path.exists():
                continue
            text = _read(path)
            if f'complete_manuscript_chapter("{chapter_id}")' in text:
                report.manuscript_gates.append(
                    CheckResult(
                        Severity.PASS,
                        f"Manuscript progress hook for `{chapter_id}` present",
                        rel,
                    )
                )
            else:
                report.manuscript_gates.append(
                    CheckResult(
                        Severity.WARN,
                        f"`complete_manuscript_chapter(\"{chapter_id}\")` not found",
                        rel,
                    )
                )

    # --- Corruption progression (static alignment only) ---
    ch1_corr = gates.get("WRITE_GATE_CH1", (None, None))[1]
    ch2_corr = gates.get("WRITE_GATE_CH2", (None, None))[1]
    if ch1_corr == 2:
        report.corruption_progression.append(
            CheckResult(
                Severity.PASS,
                "CH1 gate corruption floor (2) matches Day 2 write readiness intent",
                _rel(functions_path, root),
            )
        )
    if ch2_corr == 3:
        report.corruption_progression.append(
            CheckResult(
                Severity.PASS,
                "CH2/CH3 gate corruption floor (3) matches Level 3 milestone / soft-fail floor",
                _rel(functions_path, root),
            )
        )
    report.corruption_progression.append(
        CheckResult(
            Severity.INCOMPLETE,
            "Cannot verify optimized path reaches corruption Level 4 by Day 4 without route simulation",
        )
    )
    report.corruption_progression.append(
        CheckResult(
            Severity.INCOMPLETE,
            "Cannot verify cautious/passive/risky archetype outcomes without policy simulator or playtest matrix",
        )
    )

    # --- Fail states ---
    endings_text = _read(endings_path) if endings_path.exists() else ""
    ending_labels = _labels_in(endings_text)

    for label, expected_file, description in FAIL_LABELS:
        if day_filter:
            day_from_file = expected_file.replace("_non_canon.rpy", "")
            if expected_file != "endings.rpy" and day_from_file != day_filter:
                continue

        inline_path = days_dir / expected_file if expected_file != "endings.rpy" else endings_path
        inline_labels: set[str] = _labels_in(_read(inline_path)) if inline_path.exists() else set()
        defined_in = ending_labels | inline_labels

        if label not in defined_in:
            report.fail_states.append(
                CheckResult(
                    Severity.FAIL,
                    f"Hard/soft fail label `{label}` not defined ({description})",
                    expected_file,
                )
            )
            continue

        define_evidence = expected_file if label in inline_labels else "endings.rpy"
        report.fail_states.append(
            CheckResult(
                Severity.PASS,
                f"Fail label `{label}` defined ({description})",
                define_evidence,
            )
        )

        # Reference check: jumps/calls to fail labels
        ref_found = False
        search_paths = [endings_path]
        for day_id in _day_ids_in_scope(day_filter):
            search_paths.append(draft_non_canon_path(DayContext(day_id, release_slug)))
        if endings_path.exists():
            search_paths.append(draft_shared_dir() / "story_chains_non_canon.rpy")
            search_paths.append(draft_shared_dir() / "script.rpy")

        for path in search_paths:
            if not path.exists():
                continue
            text = _read(path)
            if _contains_jump_to(text, label) or f"call {label}" in text:
                ref_found = True
                report.fail_states.append(
                    CheckResult(
                        Severity.PASS,
                        f"`{label}` referenced from script",
                        _rel(path, root),
                    )
                )
                break
        if not ref_found and label != "game_over_dismissed":
            # dismissed may route via check_suspicion / chains — warn not fail
            sev = Severity.WARN if label == "game_over_dismissed" else Severity.WARN
            report.fail_states.append(
                CheckResult(
                    sev,
                    f"No direct `jump {label}` found in scanned spine (may route indirectly)",
                )
            )

    # game_over_dismissed via story chains
    chains_path = draft_shared_dir() / "story_chains_non_canon.rpy"
    if chains_path.exists() and _contains_jump_to(_read(chains_path), "game_over_dismissed"):
        report.fail_states.append(
            CheckResult(
                Severity.PASS,
                "`game_over_dismissed` referenced from story chains",
                _rel(chains_path, root),
            )
        )

    # MVP success ending
    if day_filter is None or day_filter == "day105":
        d105 = days_dir / "day105_non_canon.rpy"
        if d105.exists():
            text = _read(d105)
            if "label day105_7_release_one_ending" in text:
                report.fail_states.append(
                    CheckResult(
                        Severity.PASS,
                        "MVP success label `day105_7_release_one_ending` present",
                        _rel(d105, root),
                    )
                )
            else:
                report.fail_states.append(
                    CheckResult(
                        Severity.FAIL,
                        "MVP success label `day105_7_release_one_ending` missing",
                        _rel(d105, root),
                    )
                )

    # --- Soft fail ---
    d101 = days_dir / "day101_non_canon.rpy"
    if d101.exists() and (day_filter is None or day_filter == "day101"):
        text = _read(d101)
        if "day1_slop_chapter" in text:
            report.soft_fail.append(
                CheckResult(
                    Severity.PASS,
                    "Day 101 slop chapter path present for low-corruption cautious play",
                    _rel(d101, root),
                )
            )
        else:
            report.soft_fail.append(
                CheckResult(Severity.WARN, "Day 101 slop chapter path not found", _rel(d101, root))
            )

    d105 = days_dir / "day105_non_canon.rpy"
    if d105.exists() and (day_filter is None or day_filter == "day105"):
        text = _read(d105)
        if "bad_ending_rejection" in text and "WRITE_GATE_CH2" in text:
            report.soft_fail.append(
                CheckResult(
                    Severity.PASS,
                    "Day 105 reckoning wires soft fail via `WRITE_GATE_CH2` corruption floor",
                    _rel(d105, root),
                )
            )
        else:
            report.soft_fail.append(
                CheckResult(
                    Severity.WARN,
                    "Day 105 soft-fail wiring to `bad_ending_rejection` incomplete",
                    _rel(d105, root),
                )
            )

    report.soft_fail.append(
        CheckResult(
            Severity.INCOMPLETE,
            "Cannot confirm passive players receive clear life-experience feedback before soft fail without playtest",
        )
    )

    # --- Deprecated routers ---
    scan_paths = [p for p in scan_files if p.exists()]
    scan_paths.extend(draft_shared_dir().glob("*.rpy"))
    report.deprecated_routers = _scan_deprecated_jumps(scan_paths, root)

    # Retained compatibility labels are OK if not jumped to
    if (draft_shared_dir() / "story_chains_non_canon.rpy").exists():
        chains_text = _read(draft_shared_dir() / "story_chains_non_canon.rpy")
        if "label advance_after_confrontation" in chains_text:
            report.deprecated_routers.append(
                CheckResult(
                    Severity.PASS,
                    "Compatibility label `advance_after_confrontation` retained but not jumped from active work",
                    _rel(draft_shared_dir() / "story_chains_non_canon.rpy", root),
                )
            )

    return report


def default_report_path(release_slug: str) -> Path:
    return pipeline_release_root(release_slug) / "reports" / "balance_report.md"


def write_balance_report(
    report: BalanceReport,
    output_path: Path,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report.to_markdown(), encoding="utf-8")
    return output_path
