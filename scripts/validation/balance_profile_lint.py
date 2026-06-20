#!/usr/bin/env python3
"""Semantic balance profile lint for non-prod day scripts."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from balance_catalogue import (  # noqa: E402
    BESPOKE_COMMENT_RE,
    parse_apply_effects_line,
    parse_balanced_effect_line,
)
from narrative_paths import (  # noqa: E402
    DayContext,
    draft_non_canon_path,
    non_prod_game_dir,
    normalize_release_slug,
)

REQUIRED_DAY_IDS = ("day101", "day102", "day103", "day104", "day105")

BESPOKE_LOOKBACK = 5
MIGRATION_FAIL_THRESHOLD = 0.80

DIRECT_PLAYER_WRITE_RE = re.compile(
    r"^\s*\$\s*player\.(?:"
    r"inspiration|anxiety|suspicion|corruption_xp|corruption_level|"
    r"stern_acute_susp|stern_base_susp|vance_acute_susp|vance_base_susp|"
    r"missy_acute_susp|missy_base_susp|gideon_acute_susp|gideon_base_susp"
    r")\s*[-+*/]?="
)

EXCLUDED_LINT_NAMES = frozenset(
    {
        "functions_non_canon.rpy",
        "balance_profiles_non_canon.rpy",
        "debug_run_capture.rpy",
        "classes_non_canon.rpy",
    }
)


@dataclass
class BalanceProfileLintResult:
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    profile_calls: int = 0
    bespoke_calls: int = 0
    unmarked_apply_effects: int = 0
    direct_mutations: int = 0

    @property
    def economy_calls(self) -> int:
        return self.profile_calls + self.bespoke_calls + self.unmarked_apply_effects

    @property
    def migration_ratio(self) -> float:
        if self.economy_calls == 0:
            return 1.0
        return self.profile_calls / self.economy_calls

    def ok(self) -> bool:
        return not self.failures


def is_balance_lint_target(path: Path | str) -> bool:
    """Return True for non-prod day economy scripts in Phase 2 migration scope."""
    full_path = Path(path)
    if full_path.name in EXCLUDED_LINT_NAMES:
        return False
    if not full_path.name.endswith("_non_canon.rpy"):
        return False
    norm = full_path.as_posix().replace("\\", "/")
    return "/non-prod-game/game/days/" in norm


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _is_comment(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith("#") or not stripped


def _has_bespoke_marker(lines: list[str], line_index: int) -> bool:
    start = max(0, line_index - BESPOKE_LOOKBACK)
    for idx in range(start, line_index):
        if BESPOKE_COMMENT_RE.search(lines[idx]):
            return True
    return False


def _validate_balanced_call(
    effect,
    *,
    config: dict[str, Any],
    rel_file: str,
    line_no: int,
) -> list[str]:
    import balance_resolver

    failures: list[str] = []
    profiles = config["profiles"]
    if effect.profile not in profiles:
        failures.append(f"{rel_file}:{line_no} unknown balance profile '{effect.profile}'")
        return failures

    intensity = effect.intensity
    if isinstance(intensity, str) and intensity not in ("standard",) and intensity not in config["intensities"]:
        if not str(intensity).replace(".", "", 1).isdigit():
            failures.append(
                f"{rel_file}:{line_no} unknown balance intensity '{intensity}' "
                f"for profile '{effect.profile}'"
            )
            return failures

    spec = profiles[effect.profile]
    if "witness_susp" in spec and not effect.witness:
        failures.append(
            f"{rel_file}:{line_no} profile '{effect.profile}' requires a witness parameter"
        )

    if effect.witness and effect.witness not in config["valid_witnesses"]:
        failures.append(
            f"{rel_file}:{line_no} unknown witness '{effect.witness}' "
            f"(valid: {', '.join(config['valid_witnesses'])})"
        )

    try:
        balance_resolver.resolve_balanced_effect(
            effect.profile,
            intensity_override=effect.intensity,
            witness=effect.witness or None,
            base_witness=effect.base_witness,
            config=config,
        )
    except ValueError as exc:
        failures.append(f"{rel_file}:{line_no} {exc}")

    return failures


def lint_file(path: Path, *, config: dict[str, Any] | None = None, root: Path | None = None) -> BalanceProfileLintResult:
    import balance_resolver

    cfg = config or balance_resolver.load_profiles()
    repo_root = root or Path(__file__).resolve().parents[2]
    rel_file = _rel(path.resolve(), repo_root)
    result = BalanceProfileLintResult()

    lines = path.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines, start=1):
        if _is_comment(line):
            continue

        if DIRECT_PLAYER_WRITE_RE.search(line):
            result.direct_mutations += 1
            result.failures.append(
                f"{rel_file}:{idx} direct `player.<stat>` assignment; use apply_effects / mutation methods"
            )
            continue

        if balanced := parse_balanced_effect_line(line):
            result.profile_calls += 1
            result.failures.extend(
                _validate_balanced_call(balanced, config=cfg, rel_file=rel_file, line_no=idx)
            )
            continue

        if parse_apply_effects_line(line):
            if _has_bespoke_marker(lines, idx - 1):
                result.bespoke_calls += 1
            else:
                result.unmarked_apply_effects += 1
                result.warnings.append(
                    f"{rel_file}:{idx} raw `apply_effects(...)` without `# [STATE bespoke]` marker"
                )

    return result


def finalize_unmarked_severity(result: BalanceProfileLintResult) -> None:
    """Promote unmarked apply_effects warnings to failures once migration threshold is met."""
    if not result.unmarked_apply_effects:
        return
    unmarked_messages = [
        item
        for item in result.warnings
        if "raw `apply_effects(...)` without `# [STATE bespoke]` marker" in item
    ]
    if not unmarked_messages:
        return
    if result.migration_ratio >= MIGRATION_FAIL_THRESHOLD:
        result.warnings = [item for item in result.warnings if item not in unmarked_messages]
        result.failures.extend(unmarked_messages)


def merge_results(target: BalanceProfileLintResult, incoming: BalanceProfileLintResult) -> None:
    target.failures.extend(incoming.failures)
    target.warnings.extend(incoming.warnings)
    target.profile_calls += incoming.profile_calls
    target.bespoke_calls += incoming.bespoke_calls
    target.unmarked_apply_effects += incoming.unmarked_apply_effects
    target.direct_mutations += incoming.direct_mutations


def lint_paths(
    paths: list[Path | str],
    *,
    config: dict[str, Any] | None = None,
    root: Path | None = None,
) -> BalanceProfileLintResult:
    merged = BalanceProfileLintResult()
    repo_root = root or Path(__file__).resolve().parents[2]

    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = repo_root / path
        if not path.exists():
            merged.failures.append(f"{raw}: file not found")
            continue
        if not is_balance_lint_target(path):
            continue
        merge_results(merged, lint_file(path, config=config, root=repo_root))

    finalize_unmarked_severity(merged)
    return merged


def default_day_script_paths(release_slug: str = "release-1-mvp") -> list[Path]:
    release = normalize_release_slug(release_slug)
    paths: list[Path] = []
    for day_id in REQUIRED_DAY_IDS:
        ctx = DayContext(day_id, release)
        path = draft_non_canon_path(ctx)
        if path.exists():
            paths.append(path)
    day100 = non_prod_game_dir() / "game" / "days" / "day100_non_canon.rpy"
    if day100.exists():
        paths.insert(0, day100)
    return paths


def lint_release_day_scripts(
    release_slug: str = "release-1-mvp",
    *,
    config: dict[str, Any] | None = None,
) -> BalanceProfileLintResult:
    return lint_paths(default_day_script_paths(release_slug), config=config)


def lint_to_check_results(
    result: BalanceProfileLintResult,
    *,
    root: Path,
    evidence_prefix: str = "non-prod day scripts",
) -> list:
    from validation.balance_report_impl import CheckResult, Severity

    checks: list[CheckResult] = []

    if result.direct_mutations:
        checks.append(
            CheckResult(
                Severity.FAIL,
                f"Direct player stat mutations found ({result.direct_mutations})",
                evidence_prefix,
            )
        )
    else:
        checks.append(
            CheckResult(
                Severity.PASS,
                "No direct player stat mutations in scoped day scripts",
                evidence_prefix,
            )
        )

    profile_failures = [
        item
        for item in result.failures
        if "unknown balance profile" in item
        or "unknown balance intensity" in item
        or "requires a witness" in item
        or "unknown witness" in item
    ]
    if profile_failures:
        checks.append(
            CheckResult(
                Severity.FAIL,
                f"Invalid semantic profile calls ({len(profile_failures)})",
                evidence_prefix,
            )
        )
    elif result.profile_calls:
        checks.append(
            CheckResult(
                Severity.PASS,
                f"Semantic profile calls valid ({result.profile_calls} call(s))",
                evidence_prefix,
            )
        )

    if result.unmarked_apply_effects:
        severity = (
            Severity.FAIL
            if result.migration_ratio >= MIGRATION_FAIL_THRESHOLD
            else Severity.WARN
        )
        checks.append(
            CheckResult(
                severity,
                f"Unmarked raw apply_effects ({result.unmarked_apply_effects}); "
                f"migration {result.migration_ratio:.0%} "
                f"(FAIL threshold {MIGRATION_FAIL_THRESHOLD:.0%})",
                evidence_prefix,
            )
        )
    elif result.bespoke_calls or result.profile_calls:
        checks.append(
            CheckResult(
                Severity.PASS,
                f"Bespoke apply_effects marked ({result.bespoke_calls} call(s))",
                evidence_prefix,
            )
        )

    other_failures = [
        item
        for item in result.failures
        if item not in profile_failures
        and "direct `player." not in item
        and "raw `apply_effects" not in item
    ]
    if other_failures:
        checks.append(
            CheckResult(
                Severity.FAIL,
                f"Balance profile lint failures ({len(other_failures)})",
                evidence_prefix,
            )
        )

    if result.warnings and not result.unmarked_apply_effects:
        checks.append(
            CheckResult(
                Severity.WARN,
                f"Balance profile lint warnings ({len(result.warnings)})",
                evidence_prefix,
            )
        )

    if (
        not result.failures
        and not result.warnings
        and result.profile_calls == 0
        and result.bespoke_calls == 0
    ):
        checks.append(
            CheckResult(
                Severity.WARN,
                "No economy effect calls found in scoped day scripts",
                evidence_prefix,
            )
        )

    return checks
