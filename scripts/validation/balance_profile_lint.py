#!/usr/bin/env python3
"""Semantic balance profile lint for non-prod scripts."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import balance_resolver
from balance_catalogue import (  # noqa: E402
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
    if not full_path.name.endswith("_non_canon.rpy") and not full_path.name.endswith("story_chains_non_canon.rpy"):
        return False
    norm = full_path.as_posix().replace("\\", "/")
    return "/non-prod-game/game/days/" in norm or "/non-prod-game/game/shared/story_chains_non_canon.rpy" in norm


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _is_comment(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith("#") or not stripped


def _has_intensity_exception_marker(lines: list[str], line_index: int) -> bool:
    INTENSITY_EXCEPTION_RE = re.compile(r"#\s*\[BALANCE\s+intensity-exception:\s*[^\]]+\]", re.IGNORECASE)
    start = max(0, line_index - 3)
    for idx in range(start, line_index):
        if INTENSITY_EXCEPTION_RE.search(lines[idx]):
            return True
    return False


def _get_bespoke_reason(lines: list[str], line_index: int) -> str | None:
    BESPOKE_STRICT_COMMENT_RE = re.compile(r"#\s*\[STATE bespoke:\s*([a-zA-Z_]+)\]", re.IGNORECASE)
    start = max(0, line_index - BESPOKE_LOOKBACK)
    for idx in range(line_index - 1, start - 1, -1):
        match = BESPOKE_STRICT_COMMENT_RE.search(lines[idx])
        if match:
            return match.group(1)
    return None


def load_bespoke_allowlist() -> dict[str, Any]:
    allowlist_path = ROOT / "main-game" / "draft" / "releases" / "planning" / "balance" / "bespoke_effect_allowlist.yaml"
    if not allowlist_path.exists():
        return {}
    if yaml is None:
        return {}
    try:
        data = yaml.safe_load(allowlist_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _validate_balanced_call(
    effect,
    *,
    config: dict[str, Any],
    rel_file: str,
    line_no: int,
    lines: list[str],
    line_index: int,
) -> list[str]:
    import balance_resolver

    failures: list[str] = []
    profiles = config.get("profiles", {})
    if effect.profile not in profiles:
        failures.append(f"{rel_file}:{line_no} unknown balance profile '{effect.profile}'")
        return failures

    spec = profiles[effect.profile]
    if not spec.get("active", False):
        failures.append(f"{rel_file}:{line_no} inactive balance profile '{effect.profile}'")
        return failures

    intensity = effect.intensity
    if isinstance(intensity, (int, float)):
        failures.append(f"{rel_file}:{line_no} numeric intensity override '{intensity}' is forbidden in schema v2")
        return failures

    if intensity not in config.get("active_intensities", ()):
        failures.append(
            f"{rel_file}:{line_no} unknown or inactive balance intensity '{intensity}' "
            f"for profile '{effect.profile}'"
        )
        return failures

    # Check allowed story intensities (migration mode standard only unless annotated)
    allowed_intensities = config.get("migration_mode", {}).get("allowed_story_intensities", ())
    if intensity not in allowed_intensities:
        if not _has_intensity_exception_marker(lines, line_index):
            failures.append(
                f"{rel_file}:{line_no} intensity '{intensity}' blocked during migration pass "
                f"without explicit '# [BALANCE intensity-exception: ...]' annotation"
            )

    # Check witness suspension profiles
    standard_deltas = spec.get("deltas", {}).get("standard", {})
    is_risky = standard_deltas.get("witness_susp", 0) > 0
    if is_risky and not effect.witness:
        failures.append(
            f"{rel_file}:{line_no} risky profile '{effect.profile}' requires a witness parameter"
        )

    if effect.witness and effect.witness not in config["valid_witnesses"]:
        failures.append(
            f"{rel_file}:{line_no} unknown witness '{effect.witness}' "
            f"(valid: {', '.join(config['valid_witnesses'])})"
        )

    if effect.base_witness:
        failures.append(f"{rel_file}:{line_no} base_witness=True is forbidden for active profiles")

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


def _validate_bespoke_call(
    reason: str,
    kwargs: dict[str, int],
    allowlist: dict[str, Any],
    rel_file: str,
    line_no: int,
    label: str | None,
) -> list[str]:
    failures = []
    allowed_categories = {
        "negative_suspicion",
        "write_spend",
        "fixed_manuscript_reward",
        "gate_failure_penalty",
        "legacy_exception",
    }
    if reason not in allowed_categories:
        failures.append(f"{rel_file}:{line_no} invalid bespoke reason '{reason}'")
        return failures

    kwargs = {str(k): int(v) for k, v in kwargs.items()}

    if reason == "negative_suspicion":
        allowed_keys = {"stern_susp", "vance_susp", "missy_susp", "gideon_susp"}
        for k, v in kwargs.items():
            if k not in allowed_keys:
                failures.append(f"{rel_file}:{line_no} negative_suspicion cannot modify '{k}'")
            elif v >= 0:
                failures.append(f"{rel_file}:{line_no} negative_suspicion value for '{k}' must be negative (got {v})")
    elif reason == "write_spend":
        allowed_keys = {"insp"}
        for k, v in kwargs.items():
            if k not in allowed_keys:
                failures.append(f"{rel_file}:{line_no} write_spend cannot modify '{k}'")
            elif v >= 0:
                failures.append(f"{rel_file}:{line_no} write_spend value for '{k}' must be negative (got {v})")
    else:
        matched = False
        allowed_entries = allowlist.get("allowed_bespoke_effects", {})
        for entry_name, entry in allowed_entries.items():
            entry_file = entry.get("file", "").replace("\\", "/")
            norm_rel_file = rel_file.replace("\\", "/")
            if entry_file != norm_rel_file:
                continue
            if "label" in entry and entry["label"] != label:
                continue
            entry_kwargs = {str(k): int(v) for k, v in entry.get("allowed_kwargs", {}).items()}
            if entry_kwargs == kwargs:
                matched = True
                break

        if not matched:
            failures.append(
                f"{rel_file}:{line_no} mixed bespoke call with reason '{reason}' and kwargs {kwargs} "
                f"is not allowlisted in bespoke_effect_allowlist.yaml (current label: {label})"
            )
    return failures


def lint_file(
    path: Path,
    *,
    config: dict[str, Any] | None = None,
    root: Path | None = None,
    allowlist: dict[str, Any] | None = None,
) -> BalanceProfileLintResult:
    import balance_resolver

    cfg = config or balance_resolver.load_profiles()
    repo_root = root or Path(__file__).resolve().parents[2]
    rel_file = _rel(path.resolve(), repo_root)
    result = BalanceProfileLintResult()
    
    awlist = allowlist or load_bespoke_allowlist()

    lines = path.read_text(encoding="utf-8").splitlines()
    current_label = None

    for idx, line in enumerate(lines, start=1):
        label_match = re.match(r"^\s*label\s+([a-zA-Z0-9_]+)\s*:", line)
        if label_match:
            current_label = label_match.group(1)

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
                _validate_balanced_call(
                    balanced,
                    config=cfg,
                    rel_file=rel_file,
                    line_no=idx,
                    lines=lines,
                    line_index=idx - 1,
                )
            )
            continue

        if parse_apply_effects_line(line):
            reason = _get_bespoke_reason(lines, idx - 1)
            if reason:
                result.bespoke_calls += 1
                kwargs = parse_apply_effects_line(line).kwargs or {}
                result.failures.extend(
                    _validate_bespoke_call(
                        reason=reason,
                        kwargs=kwargs,
                        allowlist=awlist,
                        rel_file=rel_file,
                        line_no=idx,
                        label=current_label,
                    )
                )
            else:
                result.unmarked_apply_effects += 1
                result.failures.append(
                    f"{rel_file}:{idx} raw `apply_effects(...)` without strict `# [STATE bespoke: <reason>]` marker"
                )

    return result


def finalize_unmarked_severity(result: BalanceProfileLintResult) -> None:
    """No-op in schema v2 where unmarked apply_effects always fail immediately."""
    pass


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
    cfg = config or balance_resolver.load_profiles()
    awlist = load_bespoke_allowlist()

    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = repo_root / path
        if not path.exists():
            merged.failures.append(f"{raw}: file not found")
            continue
        if not is_balance_lint_target(path):
            continue
        merge_results(merged, lint_file(path, config=cfg, root=repo_root, allowlist=awlist))

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
    # Add story chains non-canon
    chains = non_prod_game_dir() / "game" / "shared" / "story_chains_non_canon.rpy"
    if chains.exists():
        paths.append(chains)
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
    evidence_prefix: str = "non-prod scripts",
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
                "No direct player stat mutations in scoped scripts",
                evidence_prefix,
            )
        )

    profile_failures = [
        item
        for item in result.failures
        if "unknown balance profile" in item
        or "inactive balance profile" in item
        or "intensity" in item
        or "requires a witness" in item
        or "unknown witness" in item
        or "base_witness" in item
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
        checks.append(
            CheckResult(
                Severity.FAIL,
                f"Unmarked raw apply_effects ({result.unmarked_apply_effects})",
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

    if result.warnings:
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
                "No economy effect calls found in scoped scripts",
                evidence_prefix,
            )
        )

    return checks
