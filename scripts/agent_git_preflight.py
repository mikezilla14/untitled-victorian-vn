#!/usr/bin/env python3
"""Check Git branch/worktree hygiene before agent edits."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class CheckResult:
    failures: list[str]
    warnings: list[str]


def git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def require_git(args: list[str]) -> str:
    result = git(args)
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip()
        print(f"ERROR: git {' '.join(args)} failed: {message}", file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


def current_branch() -> str:
    branch = require_git(["branch", "--show-current"])
    return branch or "(detached HEAD)"


def short_head() -> str:
    return require_git(["rev-parse", "--short", "HEAD"])


def status_lines() -> list[str]:
    output = require_git(["status", "--short"])
    return [line for line in output.splitlines() if line.strip()]


def worktree_paths() -> list[str]:
    output = require_git(["worktree", "list", "--porcelain"])
    return [
        line.removeprefix("worktree ").strip()
        for line in output.splitlines()
        if line.startswith("worktree ")
    ]


def is_feature_branch(branch: str, allowed_prefixes: tuple[str, ...]) -> bool:
    if branch in {"main", "master", "(detached HEAD)"}:
        return False
    return branch.startswith(allowed_prefixes)


def run_checks(args: argparse.Namespace) -> CheckResult:
    failures: list[str] = []
    warnings: list[str] = []
    branch = current_branch()
    dirty = status_lines()
    worktrees = worktree_paths()
    prefixes = tuple(args.feature_prefix)

    if args.require_feature_branch and not is_feature_branch(branch, prefixes):
        failures.append(
            f"current branch '{branch}' is not an allowed feature/fix branch "
            f"(allowed prefixes: {', '.join(prefixes)})"
        )
    elif branch in {"main", "master"}:
        warnings.append(f"current branch is '{branch}'; normal agent edits should use a feature branch")

    if args.fail_if_dirty and dirty:
        failures.append(f"working tree has {len(dirty)} dirty path(s)")
    elif dirty:
        warnings.append(f"working tree has {len(dirty)} dirty path(s)")

    extra_worktrees = [path for path in worktrees if Path(path).resolve() != ROOT]
    if args.fail_if_extra_worktrees and extra_worktrees:
        failures.append(f"{len(extra_worktrees)} extra worktree(s) are registered")
    elif extra_worktrees:
        warnings.append(f"{len(extra_worktrees)} extra worktree(s) are registered")

    return CheckResult(failures=failures, warnings=warnings)


def print_report(args: argparse.Namespace, result: CheckResult) -> None:
    branch = current_branch()
    dirty = status_lines()
    worktrees = worktree_paths()

    print("Agent Git preflight")
    print(f"- Repo: {ROOT}")
    print(f"- Branch: {branch}")
    print(f"- HEAD: {short_head()}")
    print(f"- Working tree: {'dirty' if dirty else 'clean'}")
    print(f"- Registered worktrees: {len(worktrees)}")

    if dirty and args.show_dirty:
        print("\nDirty paths:")
        for line in dirty:
            print(f"  {line}")

    extra_worktrees = [path for path in worktrees if Path(path).resolve() != ROOT]
    if extra_worktrees:
        print("\nExtra worktrees:")
        for path in extra_worktrees:
            print(f"  {path}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"- {warning}")

    if result.failures:
        print("\nFailures:")
        for failure in result.failures:
            print(f"- {failure}")
        print("\nPreflight failed. Stop before editing unless the human explicitly approves.")
    else:
        print("\nPreflight passed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-feature-branch",
        action="store_true",
        help="Fail unless the current branch uses an allowed feature/fix/docs prefix.",
    )
    parser.add_argument(
        "--feature-prefix",
        action="append",
        default=["feature/", "fix/", "docs/", "chore/", "codex/"],
        help="Allowed branch prefix. May be passed more than once.",
    )
    parser.add_argument(
        "--fail-if-dirty",
        action="store_true",
        help="Fail when staged or unstaged changes exist.",
    )
    parser.add_argument(
        "--fail-if-extra-worktrees",
        action="store_true",
        help="Fail when more than the main worktree is registered.",
    )
    parser.add_argument(
        "--show-dirty",
        action="store_true",
        default=True,
        help="Show dirty paths in the report.",
    )
    args = parser.parse_args()

    result = run_checks(args)
    print_report(args, result)
    return 1 if result.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
