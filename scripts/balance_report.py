#!/usr/bin/env python3
"""Generate static testing and balance report for Release 1 MVP."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from narrative_paths import DEFAULT_RELEASE_SLUG, normalize_release_slug  # noqa: E402
from validation.balance_report_impl import (  # noqa: E402
    Severity,
    build_balance_report,
    default_report_path,
    write_balance_report,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Static testing and balance report for non-prod sandbox (Release 1 MVP)."
    )
    parser.add_argument(
        "--release",
        default=DEFAULT_RELEASE_SLUG,
        help=f"Release slug (default: {DEFAULT_RELEASE_SLUG})",
    )
    parser.add_argument(
        "--day",
        default=None,
        help="Optional day scope, e.g. day105 (default: all MVP days 101-105)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Markdown output path (default: pipeline release reports/balance_report.md)",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print report to stdout instead of writing a file",
    )
    args = parser.parse_args(argv)

    release_slug = normalize_release_slug(args.release)
    day_filter = args.day.strip() if args.day else None
    if day_filter and not day_filter.startswith("day"):
        print(f"ERROR: --day must look like day101, got {day_filter!r}", file=sys.stderr)
        return 2

    report = build_balance_report(release=release_slug, day_filter=day_filter)
    markdown = report.to_markdown()

    if args.stdout:
        print(markdown)
    else:
        output = Path(args.output) if args.output else default_report_path(release_slug)
        if not output.is_absolute():
            output = ROOT / output
        written = write_balance_report(report, output)
        print(f"Wrote balance report: {written.relative_to(ROOT).as_posix()}")
        print(f"Verdict: {report.verdict().value}")

    verdict = report.verdict()
    if verdict == Severity.FAIL:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
