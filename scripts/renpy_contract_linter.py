#!/usr/bin/env python3
"""Check executable Ren'Py contracts promised by the Chief Architect rules."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "main-game" / "prod-game" / "game"

ENGINE_SYMBOLS = {
    "abs",
    "bool",
    "dict",
    "False",
    "float",
    "format",
    "int",
    "isinstance",
    "len",
    "list",
    "max",
    "min",
    "None",
    "print",
    "range",
    "renpy",
    "set",
    "str",
    "sum",
    "True",
    "tuple",
    "TypeError",
    "ValueError",
}

RENPY_KEYWORDS = {
    "call",
    "elif",
    "else",
    "if",
    "init",
    "jump",
    "label",
    "menu",
    "python",
    "return",
    "scene",
    "show",
    "with",
}


def read_text(path):
    return path.read_text(encoding="utf-8")


def repo_path(path):
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_file(path):
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def changed_game_scripts(files):
    targets = []
    for file in files:
        path = resolve_file(file)
        norm = repo_path(path)
        name = path.name
        if norm.startswith("main-game/prod-game/game/") and name.endswith(".rpy"):
            if name.startswith("day") or name in {"endings.rpy", "script.rpy"}:
                targets.append(path)
    return [path for path in targets if path.exists()]


def load_defined_speakers():
    characters = GAME_DIR / "characters.rpy"
    if not characters.exists():
        return set()
    return set(
        re.findall(
            r"^\s*define\s+([A-Za-z_]\w*)\s*=\s*Character\s*\(",
            read_text(characters),
            re.MULTILINE,
        )
    )


def load_defined_symbols():
    symbols = set(ENGINE_SYMBOLS)

    for path in [
        GAME_DIR / "classes.rpy",
        GAME_DIR / "functions.rpy",
        GAME_DIR / "variables.rpy",
        GAME_DIR / "characters.rpy",
    ]:
        if not path.exists():
            continue
        text = read_text(path)
        symbols.update(re.findall(r"^\s*class\s+([A-Za-z_]\w*)\s*\(", text, re.MULTILINE))
        symbols.update(re.findall(r"^\s*def\s+([A-Za-z_]\w*)\s*\(", text, re.MULTILINE))
        symbols.update(re.findall(r"^\s*default\s+([A-Za-z_]\w*)\s*=", text, re.MULTILINE))
        symbols.update(re.findall(r"^\s*define\s+([A-Za-z_]\w*)\s*=", text, re.MULTILINE))

    return symbols


def check_speakers(files):
    defined = load_defined_speakers()
    violations = []
    dialogue = re.compile(r'^\s*([A-Za-z_]\w*)\s+"')

    for path in files:
        for idx, line in enumerate(read_text(path).splitlines(), start=1):
            match = dialogue.match(line)
            if not match:
                continue
            speaker = match.group(1)
            if speaker not in defined:
                violations.append(
                    f"{repo_path(path)}:{idx} undefined dialogue speaker `{speaker}`; define it in characters.rpy"
                )

    return violations


def check_story_flag_assignments(files):
    violations = []
    direct_flag = re.compile(r"story\.has_[A-Za-z_]\w*\s*=(?!=)")

    for path in files:
        for idx, line in enumerate(read_text(path).splitlines(), start=1):
            if direct_flag.search(line):
                violations.append(
                    f"{repo_path(path)}:{idx} direct `story.has_*` assignment; use the typed StoryState setter"
                )

    return violations


def extract_expression(line):
    stripped = line.strip()
    if stripped.startswith("$"):
        return stripped[1:].strip()
    if stripped.startswith(("if ", "elif ", "while ")):
        parts = stripped.split(None, 1)
        if len(parts) < 2:
            return None
        return parts[1].rstrip(":").strip()
    return None


def check_callable_symbols(files):
    defined = load_defined_symbols()
    violations = []
    bare_call = re.compile(r"(?<![\.\w])([A-Za-z_]\w*)\s*\(")

    for path in files:
        for idx, line in enumerate(read_text(path).splitlines(), start=1):
            expr = extract_expression(line)
            if not expr:
                continue
            for symbol in bare_call.findall(expr):
                if symbol in RENPY_KEYWORDS or symbol in defined:
                    continue
                violations.append(
                    f"{repo_path(path)}:{idx} unresolved callable `{symbol}`; define it in canonical runtime code or qualify it"
                )

    return violations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", required=True, help="Comma-separated changed file paths.")
    args = parser.parse_args()

    files = [file.strip() for file in args.files.split(",") if file.strip()]
    targets = changed_game_scripts(files)
    if not targets:
        print("No Ren'Py game scripts provided. Skipping Ren'Py contract lint.")
        return 0

    violations = []
    violations.extend(check_speakers(targets))
    violations.extend(check_story_flag_assignments(targets))
    violations.extend(check_callable_symbols(targets))

    if violations:
        print("REN'PY CONTRACT VIOLATIONS:")
        for violation in violations:
            print(f" - {violation}")
        return 1

    print("Ren'Py contract checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
