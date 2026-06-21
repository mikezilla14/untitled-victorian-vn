#!/usr/bin/env python3
"""Check executable Ren'Py contracts promised by the Chief Architect rules."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROD_GAME_DIR = ROOT / "main-game" / "prod-game" / "game"
NON_PROD_GAME_DIR = ROOT / "main-game" / "non-prod-game" / "game"
GAME_DIRS = (PROD_GAME_DIR, NON_PROD_GAME_DIR)

ENGINE_SYMBOLS = {
    "abs",
    "bool",
    "dict",
    "False",
    "float",
    "format",
    "getattr",
    "hasattr",
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
    "setattr",
    "str",
    "sum",
    "True",
    "tuple",
    "TypeError",
    "ValueError",
}

ENGINE_SPEAKERS = {"nvl_narrator"}

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

# Ren'Py block types whose indented bodies are not dialogue script.
SCREEN_LANGUAGE_BLOCKS = frozenset({"screen", "transform", "style"})
NON_DIALOGUE_BLOCKS = SCREEN_LANGUAGE_BLOCKS | frozenset({"python", "image"})

BLOCK_START_PATTERNS = (
    ("screen", re.compile(r"^screen\s+")),
    ("transform", re.compile(r"^transform\s+")),
    ("style", re.compile(r"^style\s+")),
    ("label", re.compile(r"^label\s+")),
    ("python", re.compile(r"^(?:init\b.*\s+)?python\s*:")),
    ("image", re.compile(r"^image\s+")),
)


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
        if path.suffix != ".rpy":
            continue
        game_dir = game_dir_for(path)
        if game_dir is None:
            continue
        relative = path.resolve().relative_to(game_dir.resolve())
        if relative.parts and relative.parts[0] in {"AEditor", "gui", "tl"}:
            continue
        targets.append(path)
    return [path for path in targets if path.exists()]


def game_dir_for(path):
    resolved = path.resolve()
    for game_dir in GAME_DIRS:
        try:
            resolved.relative_to(game_dir.resolve())
            return game_dir
        except ValueError:
            continue
    return None


def definition_files(game_dir):
    if game_dir == NON_PROD_GAME_DIR:
        return [
            game_dir / "shared" / "classes_non_canon.rpy",
            game_dir / "shared" / "functions_non_canon.rpy",
            game_dir / "variables.rpy",
            game_dir / "shared" / "characters.rpy",
        ]
    return [
        game_dir / "classes.rpy",
        game_dir / "functions.rpy",
        game_dir / "variables.rpy",
        game_dir / "characters.rpy",
    ]


def load_defined_speakers(game_dir):
    speakers = set()
    for path in definition_files(game_dir):
        if not path.exists():
            continue
        speakers.update(
            re.findall(
                r"^\s*define\s+([A-Za-z_]\w*)\s*=\s*Character\s*\(",
                read_text(path),
                re.MULTILINE,
            )
        )
    return speakers


def symbols_defined_in(path):
    if not path.exists():
        return set()
    text = read_text(path)
    symbols = set(re.findall(r"^\s*class\s+([A-Za-z_]\w*)\s*\(", text, re.MULTILINE))
    symbols.update(re.findall(r"^\s*def\s+([A-Za-z_]\w*)\s*\(", text, re.MULTILINE))
    symbols.update(re.findall(r"^\s*default\s+([A-Za-z_]\w*)\s*=", text, re.MULTILINE))
    symbols.update(re.findall(r"^\s*define\s+([A-Za-z_]\w*)\s*=", text, re.MULTILINE))
    return symbols


def load_defined_symbols(game_dir):
    symbols = set(ENGINE_SYMBOLS)

    for path in definition_files(game_dir):
        symbols.update(symbols_defined_in(path))

    return symbols


def _image_block_opens(stripped):
    """True when an image statement continues on following indented lines."""
    if "(" not in stripped:
        return False
    tail = stripped.rstrip()
    return not tail.endswith(")")


def compute_block_contexts(lines):
    """Return active Ren'Py block types for each line (index matches ``lines``)."""
    contexts = []
    stack = []

    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if stripped and not stripped.startswith("#"):
            while stack and indent <= stack[-1][1]:
                stack.pop()

            for block_type, pattern in BLOCK_START_PATTERNS:
                if not pattern.match(stripped):
                    continue
                if block_type == "image" and not _image_block_opens(stripped):
                    break
                stack.append((block_type, indent))
                break

        contexts.append(frozenset(name for name, _ in stack))

    return contexts


def check_speakers(files):
    violations = []
    dialogue = re.compile(r'^\s*([A-Za-z_]\w*)\s+"')

    for path in files:
        lines = read_text(path).splitlines()
        contexts = compute_block_contexts(lines)
        defined = load_defined_speakers(game_dir_for(path)) | ENGINE_SPEAKERS
        for idx, line in enumerate(lines, start=1):
            if contexts[idx - 1] & NON_DIALOGUE_BLOCKS:
                continue
            match = dialogue.match(line)
            if not match:
                continue
            speaker = match.group(1)
            if speaker in RENPY_KEYWORDS:
                continue
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
    violations = []
    bare_call = re.compile(r"(?<![\.\w])([A-Za-z_]\w*)\s*\(")

    for path in files:
        lines = read_text(path).splitlines()
        contexts = compute_block_contexts(lines)
        defined = load_defined_symbols(game_dir_for(path)) | symbols_defined_in(path)
        for idx, line in enumerate(lines, start=1):
            expr = extract_expression(line)
            if not expr:
                continue
            stripped = line.strip()
            if (
                contexts[idx - 1] & SCREEN_LANGUAGE_BLOCKS
                and stripped.startswith(("if ", "elif ", "while "))
            ):
                continue
            for symbol in bare_call.findall(expr):
                if symbol in RENPY_KEYWORDS or symbol in defined:
                    continue
                violations.append(
                    f"{repo_path(path)}:{idx} unresolved callable `{symbol}`; define it in canonical runtime code or qualify it"
                )

    return violations


def check_bracket_interpolation(files):
    violations = []
    quoted_string = re.compile(r'"(?:\\.|[^"\\])*"')
    interpolation = re.compile(r"(?<!\[)\[([A-Z][A-Za-z0-9_]*)\](?!\])")

    for path in files:
        defined = load_defined_symbols(game_dir_for(path))
        for idx, line in enumerate(read_text(path).splitlines(), start=1):
            for string in quoted_string.findall(line):
                for symbol in interpolation.findall(string):
                    if symbol in defined:
                        continue
                    violations.append(
                        f"{repo_path(path)}:{idx} unescaped bracket label `[{symbol}]`; "
                        f"use `[[{symbol}]]` or define the runtime interpolation symbol"
                    )

    return violations


def check_label_naming(files):
    violations = []
    label = re.compile(r"^\s*label\s+(day\d{3}(?:_[A-Za-z0-9_]+)?)\s*(?:\([^)]*\))?\s*:")
    allowed_structural = re.compile(
        r"^day\d{3}(?:|_main|_(?:morning|afternoon|evening|night)"
        r"(?:_(?:story|consequence)_window)?)$"
    )
    major_scene = re.compile(r"^day\d{3}_[1-9]_[a-z0-9]+(?:_[a-z0-9]+)*$")

    for path in files:
        for idx, line in enumerate(read_text(path).splitlines(), start=1):
            match = label.match(line)
            if not match:
                continue
            name = match.group(1)
            if allowed_structural.fullmatch(name) or major_scene.fullmatch(name):
                continue
            violations.append(
                f"{repo_path(path)}:{idx} label `{name}` does not follow "
                "`dayRdd_p_location_description` or an approved structural day label"
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
    violations.extend(check_bracket_interpolation(targets))
    violations.extend(check_label_naming(targets))

    if violations:
        print("REN'PY CONTRACT VIOLATIONS:")
        for violation in violations:
            print(f" - {violation}")
        return 1

    print("Ren'Py contract checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
