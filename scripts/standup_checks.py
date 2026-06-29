#!/usr/bin/env python3
"""Automated checks run by the daily standup (live validation only — no stale artifacts)."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from renpy_sdk import build_lint_command, find_renpy_executable, lint_fix_hint

ROOT = Path(__file__).resolve().parents[1]
NON_PROD_PROJECT_DIR = ROOT / "main-game" / "non-prod-game"
NON_PROD_GAME_DIR = NON_PROD_PROJECT_DIR / "game"
PROD_GAME_DIR = ROOT / "main-game" / "prod-game" / "game"
BIBLE_DIR = ROOT / "main-game" / "draft" / "bible"


@dataclass
class CheckResult:
    check_id: str
    name: str
    status: str  # pass | fail | skip
    summary: str
    details: list[str] = field(default_factory=list)
    fix_command: str | None = None

    @property
    def passed(self) -> bool:
        return self.status == "pass"

    @property
    def failed(self) -> bool:
        return self.status == "fail"


def collect_non_prod_rpy_paths() -> list[str]:
    paths = sorted(NON_PROD_GAME_DIR.rglob("*.rpy"))
    return [p.relative_to(ROOT).as_posix() for p in paths]


def collect_non_canon_rpy_paths() -> list[str]:
    paths = sorted(NON_PROD_GAME_DIR.rglob("*_non_canon.rpy"))
    return [p.relative_to(ROOT).as_posix() for p in paths]


def collect_bible_paths() -> list[str]:
    if not BIBLE_DIR.exists():
        return []
    return [p.relative_to(ROOT).as_posix() for p in sorted(BIBLE_DIR.glob("*.md"))]


def _run_subprocess(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", cwd=ROOT)


def run_renpy_contract_check(rpy_paths: list[str]) -> CheckResult:
    if not rpy_paths:
        return CheckResult(
            "renpy_contract",
            "Ren'Py contract lint (non-prod)",
            "skip",
            "No non-prod .rpy files found.",
        )
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "renpy_contract_linter.py"),
        "--files",
        ",".join(rpy_paths),
    ]
    res = _run_subprocess(cmd)
    if res.returncode == 0:
        return CheckResult(
            "renpy_contract",
            "Ren'Py contract lint (non-prod)",
            "pass",
            f"{len(rpy_paths)} script(s) checked.",
        )
    details = [line for line in (res.stdout + res.stderr).splitlines() if line.strip()]
    return CheckResult(
        "renpy_contract",
        "Ren'Py contract lint (non-prod)",
        "fail",
        f"{len(details)} violation(s).",
        details=details[:10],
        fix_command=(
            f'py scripts/renpy_contract_linter.py --files "{",".join(rpy_paths[:5])}"'
            + (" ..." if len(rpy_paths) > 5 else "")
        ),
    )


def run_engineering_compliance(rpy_paths: list[str]) -> CheckResult:
    if not rpy_paths:
        return CheckResult(
            "engineering_compliance",
            "Engineering compliance (non-prod)",
            "skip",
            "No non-prod .rpy files found.",
        )
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "engineering_compliance.py"),
        "--files",
        ",".join(rpy_paths),
    ]
    res = _run_subprocess(cmd)
    if res.returncode == 0:
        return CheckResult(
            "engineering_compliance",
            "Engineering compliance (non-prod)",
            "pass",
            f"{len(rpy_paths)} script(s) checked.",
        )
    details = [line for line in (res.stdout + res.stderr).splitlines() if line.strip()]
    return CheckResult(
        "engineering_compliance",
        "Engineering compliance (non-prod)",
        "fail",
        f"{len(details)} violation(s).",
        details=details[:10],
        fix_command=(
            f'py scripts/engineering_compliance.py --files "{",".join(rpy_paths[:5])}"'
            + (" ..." if len(rpy_paths) > 5 else "")
        ),
    )


def run_scene_direction_check(rpy_paths: list[str]) -> CheckResult:
    if not rpy_paths:
        return CheckResult(
            "scene_direction",
            "Scene direction ([asset auto])",
            "skip",
            "No *_non_canon.rpy files found.",
        )
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "scene_direction.py"),
        "--files",
        ",".join(rpy_paths),
        "--check",
    ]
    res = _run_subprocess(cmd)
    if res.returncode == 0:
        return CheckResult(
            "scene_direction",
            "Scene direction ([asset auto])",
            "pass",
            f"{len(rpy_paths)} draft script(s) checked.",
        )
    details = []
    for line in res.stdout.splitlines():
        if line.strip().startswith("-"):
            details.append(line.strip().strip("- ").strip())
    return CheckResult(
        "scene_direction",
        "Scene direction ([asset auto])",
        "fail",
        f"{len(details)} file(s) out of date.",
        details=details,
        fix_command='py scripts/scene_direction.py --files "<path>"',
    )


def run_formatting_check(rpy_paths: list[str]) -> CheckResult:
    if not rpy_paths:
        return CheckResult(
            "format_non_canon",
            "Non-canon prose formatting",
            "skip",
            "No *_non_canon.rpy files found.",
        )
    cmd = [sys.executable, str(ROOT / "scripts" / "format_non_canon.py"), "--check"] + rpy_paths
    res = _run_subprocess(cmd)
    if res.returncode == 0:
        return CheckResult(
            "format_non_canon",
            "Non-canon prose formatting",
            "pass",
            f"{len(rpy_paths)} draft script(s) checked.",
        )
    details = []
    for line in res.stdout.splitlines():
        if line.strip().startswith("-"):
            details.append(line.strip().strip("- ").strip())
    return CheckResult(
        "format_non_canon",
        "Non-canon prose formatting",
        "fail",
        f"{len(details)} file(s) need formatting.",
        details=details,
        fix_command='py scripts/format_non_canon.py "<path>"',
    )


def run_historical_check(files: list[str]) -> CheckResult:
    if not files:
        return CheckResult(
            "historical_linter",
            "Historical linter (drafts + bible)",
            "skip",
            "No narrative draft or bible files found.",
        )
    failed: list[str] = []
    for f in files:
        cmd = [sys.executable, str(ROOT / "scripts" / "historical_linter.py"), "--file", f]
        res = _run_subprocess(cmd)
        if res.returncode != 0:
            failed.append(f)
    if not failed:
        return CheckResult(
            "historical_linter",
            "Historical linter (drafts + bible)",
            "pass",
            f"{len(files)} file(s) checked.",
        )
    return CheckResult(
        "historical_linter",
        "Historical linter (drafts + bible)",
        "fail",
        f"{len(failed)} file(s) with anachronisms.",
        details=failed,
        fix_command='py scripts/historical_linter.py --file "<path>"',
    )


def audit_non_prod_assets_on_disk() -> CheckResult:
    """Declared manifest entries must exist on non-prod or prod disk."""
    manifest_path = NON_PROD_GAME_DIR / "assets_manifest.rpy"
    if not manifest_path.exists():
        manifest_path = NON_PROD_GAME_DIR / "shared" / "assets_manifest.rpy"
    if not manifest_path.exists():
        return CheckResult(
            "asset_disk",
            "Asset manifest disk sync (non-prod)",
            "skip",
            "No non-prod assets_manifest.rpy found.",
        )

    import re

    text = manifest_path.read_text(encoding="utf-8")
    image_pattern = re.compile(
        r'declare_image_with_fallback\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']'
    )
    audio_pattern = re.compile(
        r'(?:audio_[a-zA-Z0-9_]+\s*=\s*)?register_audio\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']'
    )

    missing: list[str] = []
    for img_id, rel_path in image_pattern.findall(text):
        if not (NON_PROD_GAME_DIR / rel_path).exists() and not (PROD_GAME_DIR / rel_path).exists():
            missing.append(f"Image '{img_id}' → {rel_path}")
    for alias, rel_path in audio_pattern.findall(text):
        if not (NON_PROD_GAME_DIR / rel_path).exists() and not (PROD_GAME_DIR / rel_path).exists():
            missing.append(f"Audio '{alias}' → {rel_path}")

    if not missing:
        return CheckResult(
            "asset_disk",
            "Asset manifest disk sync (non-prod)",
            "pass",
            "All declared assets exist on disk (non-prod or prod pool).",
        )
    return CheckResult(
        "asset_disk",
        "Asset manifest disk sync (non-prod)",
        "fail",
        f"{len(missing)} declared asset(s) missing from both engines.",
        details=missing[:10],
        fix_command="py scripts/daily_asset_manifest.py",
    )


def run_renpy_lint_optional() -> CheckResult:
    """Live renpy lint when an SDK is on PATH or under Documents/Renpy."""
    cmd = build_lint_command(NON_PROD_PROJECT_DIR)
    if not cmd:
        return CheckResult(
            "renpy_lint",
            "renpy lint (non-prod project)",
            "skip",
            "Ren'Py SDK not found (PATH, RENPY_SDK, or Documents/Renpy).",
            fix_command=lint_fix_hint(NON_PROD_PROJECT_DIR),
        )
    sdk_note = ""
    sdk_root = find_renpy_executable()
    if sdk_root is not None:
        sdk_note = f" via {sdk_root.parent.name}"
    res = _run_subprocess(cmd)
    if res.returncode == 0:
        return CheckResult(
            "renpy_lint",
            "renpy lint (non-prod project)",
            "pass",
            f"Zero Ren'Py engine lint errors{sdk_note}.",
        )
    details = [line for line in (res.stdout + res.stderr).splitlines() if line.strip()]
    return CheckResult(
        "renpy_lint",
        "renpy lint (non-prod project)",
        "fail",
        "Ren'Py engine reported script errors.",
        details=details[:15],
        fix_command=" ".join(cmd),
    )


def run_all_daily_checks() -> list[CheckResult]:
    """Execute every automated check the daily standup is allowed to report."""
    non_prod_rpy = collect_non_prod_rpy_paths()
    non_canon_rpy = collect_non_canon_rpy_paths()
    bible_paths = collect_bible_paths()
    historical_targets = non_canon_rpy + bible_paths

    return [
        run_renpy_contract_check(non_prod_rpy),
        run_engineering_compliance(non_prod_rpy),
        run_scene_direction_check(non_canon_rpy),
        run_formatting_check(non_canon_rpy),
        run_historical_check(historical_targets),
        audit_non_prod_assets_on_disk(),
        run_renpy_lint_optional(),
    ]
