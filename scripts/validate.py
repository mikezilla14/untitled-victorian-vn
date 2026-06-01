#!/usr/bin/env python3
"""Standard validation entry point for CI and agents."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from writers_room_pipeline import validate_day_pipeline  # noqa: E402


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
        norm = file.replace("//", "/")
        name = Path(norm).name
        if norm.startswith("narrative/draft/") and (
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


def run_writers_room_pipeline_check(
    file_str: str,
    *,
    require_gates: bool,
    partial_gates: bool,
    require_json_contracts: bool = True,
) -> int:
    failures, messages = validate_day_pipeline(
        file_str,
        require_gates=require_gates,
        partial_gates=partial_gates,
        require_json_contracts=require_json_contracts,
    )
    if not messages:
        return 0
    for line in messages:
        print(line)
    return 1 if failures else 0


def run_step_chunked(name, base_command, files, file_arg_name="--files", joiner=join_files, use_list=False):
    if not files:
        return 0
    chunk = []
    current_len = sum(len(str(x)) for x in base_command) + len(name) + 100
    exit_code = 0
    
    for file in files:
        file_len = len(file) + 1
        if current_len + file_len > 7000 and chunk:
            if use_list:
                cmd = base_command + chunk
            else:
                cmd = base_command + [file_arg_name, joiner(chunk)]
            res = run_step(f"{name} (chunk)", cmd)
            if res:
                exit_code = res
            chunk = []
            current_len = sum(len(str(x)) for x in base_command) + len(name) + 100
        chunk.append(file)
        current_len += file_len
        
    if chunk:
        if use_list:
            cmd = base_command + chunk
        else:
            cmd = base_command + [file_arg_name, joiner(chunk)]
        res = run_step(name, cmd)
        if res:
            exit_code = res
            
    return exit_code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        choices=["changed", "code", "narrative", "full"],
        default="changed",
    )
    parser.add_argument("--files", default="", help="Comma-separated changed file paths.")
    parser.add_argument("--agent", default="human", help="Agent name for domain gatekeeping.")
    parser.add_argument(
        "--skip-gate-checks",
        action="store_true",
        help="Skip gate verdict file checks (WIP drafts only).",
    )
    parser.add_argument(
        "--strict-gates",
        action="store_true",
        help="Require all three gate files even if none exist yet (pre-promotion).",
    )
    parser.add_argument(
        "--skip-json-contracts",
        action="store_true",
        help="Skip JSON sidecar validation for gate/brief handoffs.",
    )
    args = parser.parse_args()
    require_gates = not args.skip_gate_checks
    partial_gates = not args.strict_gates
    require_json_contracts = not args.skip_json_contracts

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
        failures |= run_step_chunked(
            "Domain gatekeeper",
            [py, "scripts/gatekeeper.py", "--agent", args.agent],
            target_files,
            file_arg_name="--files"
        )

    if args.profile in {"changed", "code", "full"}:
        target_files = files or all_files_under(
            ROOT / "renpy_project" / "game",
            lambda path: path.suffix == ".rpy",
        )
        failures |= run_step_chunked(
            "Engineering compliance",
            [py, "scripts/engineering_compliance.py"],
            target_files,
            file_arg_name="--files"
        )
        failures |= run_step_chunked(
            "Ren'Py contract lint",
            [py, "scripts/renpy_contract_linter.py"],
            target_files,
            file_arg_name="--files"
        )
        failures |= run_step(
            "Asset manifest sync audit",
            [py, "scripts/check_assets.py"]
        )


    if args.profile in {"changed", "narrative", "full"}:
        target_files = narrative_files(files)
        if args.profile == "full":
            target_files = all_files_under(
                ROOT / "narrative" / "draft",
                lambda path: path.name.endswith("_non_canon.rpy") or path.suffix == ".md",
            )

        for file in target_files:
            failures |= run_step(
                f"Historical lint: {file}",
                [py, "scripts/historical_linter.py", "--file", file],
            )

        non_canon_rpy = [file for file in target_files if file.replace("//", "/").endswith("_non_canon.rpy")]
        if non_canon_rpy:
            # Scene direction runs (logically) before formatting: it generates the
            # `[asset auto]` staging lines that the formatter then marks.
            failures |= run_step_chunked(
                "Scene direction check",
                [py, "scripts/scene_direction.py", "--check"],
                non_canon_rpy,
                file_arg_name="--files"
            )
            failures |= run_step_chunked(
                "Non-canon formatting check",
                [py, "scripts/format_non_canon.py", "--check"],
                non_canon_rpy,
                use_list=True
            )
            for file in non_canon_rpy:
                failures |= run_writers_room_pipeline_check(
                    file,
                    require_gates=require_gates,
                    partial_gates=partial_gates,
                    require_json_contracts=require_json_contracts,
                )

    if failures:
        return 1

    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
