#!/usr/bin/env python3
"""CLI for semantic balance profile lint (non-prod day scripts)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from narrative_paths import DEFAULT_RELEASE_SLUG, normalize_release_slug  # noqa: E402
from validation.balance_profile_lint import lint_paths, lint_release_day_scripts  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint semantic balance profiles in non-prod day scripts."
    )
    parser.add_argument(
        "--files",
        default="",
        help="Comma-separated non-prod day script paths (default: MVP day scripts)",
    )
    parser.add_argument(
        "--release",
        default=DEFAULT_RELEASE_SLUG,
        help=f"Release slug when scanning default day scripts (default: {DEFAULT_RELEASE_SLUG})",
    )
    args = parser.parse_args(argv)

    if args.files.strip():
        paths = [item.strip() for item in args.files.split(",") if item.strip()]
        result = lint_paths(paths, root=ROOT)
    else:
        release = normalize_release_slug(args.release)
        result = lint_release_day_scripts(release)

    if result.profile_calls or result.bespoke_calls or result.unmarked_apply_effects:
        print(
            "Economy calls: "
            f"{result.profile_calls} profile, "
            f"{result.bespoke_calls} bespoke, "
            f"{result.unmarked_apply_effects} unmarked "
            f"(migration {result.migration_ratio:.0%})"
        )

    for warning in result.warnings:
        print(f"WARN: {warning}")
    for failure in result.failures:
        print(f"FAIL: {failure}")

    if result.failures:
        print(f"\nBalance profile lint failed ({len(result.failures)} issue(s)).")
        return 1

    if result.warnings:
        print(f"\nBalance profile lint passed with {len(result.warnings)} warning(s).")
    else:
        print("\nBalance profile lint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
