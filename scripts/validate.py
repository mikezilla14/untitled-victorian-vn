#!/usr/bin/env python3
"""Standard validation entry point for CI and agents."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_step(name, command):
    print(f"\n== {name} ==")
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode:
        print(f"{name} failed with exit code {result.returncode}.")
    return result.returncode


def split_files(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def join_files(files):
    return ",".join(files)


def narrative_files(files):
    targets = []
    for file in files:
        norm = file.replace("\\", "/")
        name = Path(norm).name
        if norm.startswith("narrative/writers_room/") and (
            name.endswith("_non_canon.rpy") or name.endswith(".md")
        ):
            targets.append(file)
    return targets


def all_files_under(path, predicate):
    return [
        item.relative_to(ROOT).as_posix()
        for item in path.rglob("*")
        if item.is_file() and predicate(item)
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        choices=["changed", "code", "narrative", "full"],
        default="changed",
    )
    parser.add_argument("--files", default="", help="Comma-separated changed file paths.")
    parser.add_argument("--agent", default="human", help="Agent name for domain gatekeeping.")
    args = parser.parse_args()

    files = split_files(args.files)
    if args.profile in {"changed", "code", "narrative"} and not files:
        print("No files provided. Nothing to validate.")
        return 0

    py = sys.executable
    failures = 0

    if args.profile in {"changed", "full"}:
        target_files = files or all_files_under(
            ROOT,
            lambda path: ".git" not in path.parts and "__pycache__" not in path.parts,
        )
        failures |= run_step(
            "Domain gatekeeper",
            [py, "scripts/gatekeeper.py", "--agent", args.agent, "--files", join_files(target_files)],
        )

    if args.profile in {"changed", "code", "full"}:
        target_files = files or all_files_under(
            ROOT / "renpy_project" / "game",
            lambda path: path.suffix == ".rpy",
        )
        failures |= run_step(
            "Engineering compliance",
            [py, "scripts/engineering_compliance.py", "--files", join_files(target_files)],
        )
        failures |= run_step(
            "Ren'Py contract lint",
            [py, "scripts/renpy_contract_linter.py", "--files", join_files(target_files)],
        )

    if args.profile in {"changed", "narrative", "full"}:
        target_files = narrative_files(files)
        if args.profile == "full":
            target_files = all_files_under(
                ROOT / "narrative" / "writers_room",
                lambda path: path.name.endswith("_non_canon.rpy") or path.suffix == ".md",
            )

        for file in target_files:
            failures |= run_step(
                f"Historical lint: {file}",
                [py, "scripts/historical_linter.py", "--file", file],
            )

        non_canon_rpy = [file for file in target_files if file.replace("\\", "/").endswith("_non_canon.rpy")]
        if non_canon_rpy:
            failures |= run_step(
                "Non-canon formatting check",
                [py, "scripts/format_non_canon.py", "--check", *non_canon_rpy],
            )

    if failures:
        return 1

    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
