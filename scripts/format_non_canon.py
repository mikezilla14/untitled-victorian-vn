#!/usr/bin/env python3
"""Standardize formatting for dayrxx_non_canon.md narrative scripts.

Rules:
- Normalize marker comments to `# [TAG] ...`
- Add a format legend once per file (after top title block)
- Add a blank line after marker blocks when prose/dialogue starts
- Add lightweight inferred markers for common Ren'Py-like commands
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable


LEGEND_LINES = [
    "# FORMAT LEGEND:",
    "# [ASSET]  -> backgrounds, sprites, transitions, CG/UI callouts",
    "# [STATE]  -> variable changes, effects, conditions, jumps",
    "# [CHOICE] -> menu blocks and inflection points",
    "# [BEAT]   -> narrative intent / scene intent notes",
]

CANONICAL_TAGS = {"ASSET", "STATE", "CHOICE", "BEAT"}
DAYRXX_NON_CANON_RE = re.compile(r"^day([1-9]\d*)(0[1-9]|[1-9]\d)_non_canon\.md$")


def is_dialogue_or_narration(stripped: str) -> bool:
    if not stripped:
        return False
    if stripped.startswith('"'):
        return True
    # Typical Ren'Py dialogue: `name "text"`
    return bool(re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*\s+\"", stripped))


def normalize_marker_line(line: str) -> str:
    stripped = line.strip()
    indent = line[: len(line) - len(line.lstrip(" "))]

    marker_match = re.match(r"^#\s*\[([A-Za-z]+)\]\s*(.*)$", stripped)
    if marker_match:
        tag = marker_match.group(1).upper()
        payload = marker_match.group(2).strip()
        if tag in CANONICAL_TAGS:
            payload = payload.rstrip(".")
            return f"{indent}# [{tag}] {payload}".rstrip()

    inflection = re.match(r"^#\s*INFLECTION POINT\s*(.*)$", stripped, re.IGNORECASE)
    if inflection:
        payload = ("INFLECTION POINT " + inflection.group(1).strip()).rstrip(": ").strip()
        return f"{indent}# [CHOICE] {payload}"

    if re.match(r"^#\s*UI\s*CALL", stripped, re.IGNORECASE):
        payload = re.sub(r"^#\s*", "", stripped).rstrip(".")
        return f"{indent}# [ASSET] {payload}"

    if re.match(r"^#\s*CG\s*:", stripped, re.IGNORECASE):
        payload = re.sub(r"^#\s*CG\s*:\s*", "Show CG: ", stripped, flags=re.IGNORECASE).rstrip(".")
        return f"{indent}# [ASSET] {payload}"

    return line.rstrip("\n")


def line_indent(line: str) -> str:
    return line[: len(line) - len(line.lstrip(" "))]


def is_command_line(stripped: str) -> bool:
    return stripped.startswith(("scene ", "show ", "hide ", "with ", "$ ", "jump ", "menu:"))


def needs_marker_before(lines: list[str], idx: int) -> str | None:
    line = lines[idx]
    stripped = line.strip()
    if not stripped:
        return None
    indent = line_indent(line)

    prev_non_empty = ""
    j = idx - 1
    while j >= 0:
        candidate = lines[j].strip()
        if candidate:
            prev_non_empty = candidate
            break
        j -= 1

    if prev_non_empty.startswith("# ["):
        return None
    if is_command_line(prev_non_empty):
        return None

    if stripped.startswith("menu:"):
        return f"{indent}# [CHOICE] Decision point"
    if stripped.startswith(("scene ", "show ", "hide ", "with ")):
        return f"{indent}# [ASSET] Visual/staging command"
    if stripped.startswith(("$ ", "jump ")):
        return f"{indent}# [STATE] State/progression update"

    return None


def add_legend(lines: list[str]) -> list[str]:
    if any(l.strip() == "# FORMAT LEGEND:" for l in lines):
        return lines

    # Insert after initial 3-line title banner if present.
    if len(lines) >= 3 and lines[0].startswith("# ===") and lines[2].startswith("# ==="):
        insert_at = 3
        out = lines[:insert_at] + LEGEND_LINES + [""] + lines[insert_at:]
        return out

    return LEGEND_LINES + [""] + lines


def format_lines(raw_lines: Iterable[str]) -> list[str]:
    lines = [l.rstrip("\n") for l in raw_lines]
    lines = add_legend(lines)

    # First pass: normalize marker lines.
    lines = [normalize_marker_line(line) for line in lines]

    # Second pass: infer missing markers before known commands.
    out: list[str] = []
    for idx, line in enumerate(lines):
        marker = needs_marker_before(lines, idx)
        if marker:
            if out and out[-1].strip():
                out.append("")
            out.append(marker)
        out.append(line)

    # Third pass: ensure blank line after marker block when narration/dialogue starts.
    final: list[str] = []
    for i, line in enumerate(out):
        final.append(line)
        if not line.strip().startswith("# ["):
            continue

        # marker block can span consecutive marker lines
        if i + 1 >= len(out):
            continue

        nxt = out[i + 1].strip()
        if not nxt.startswith("# [") and is_dialogue_or_narration(nxt):
            if i + 1 > 0 and out[i + 1 - 1].strip() != "":
                final.append("")

    # Fourth pass: align marker indentation with nearby code blocks.
    aligned: list[str] = []
    for i, line in enumerate(final):
        stripped = line.strip()
        if not stripped.startswith("# ["):
            aligned.append(line)
            continue

        next_indent = None
        k = i + 1
        while k < len(final):
            nxt = final[k].strip()
            if not nxt:
                k += 1
                continue
            if nxt.startswith("# ["):
                k += 1
                continue
            next_indent = line_indent(final[k])
            break
        if next_indent is None:
            aligned.append(line)
        else:
            aligned.append(f"{next_indent}{stripped}")

    # Compact triple+ blank lines to at most double blank lines.
    compact: list[str] = []
    blank_run = 0
    for line in aligned:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= 2:
                compact.append(line)
        else:
            blank_run = 0
            compact.append(line)

    return compact


def process_file(path: Path, write: bool) -> bool:
    original = path.read_text(encoding="utf-8").splitlines()
    formatted = format_lines(original)
    changed = formatted != original
    if changed and write:
        path.write_text("\n".join(formatted) + "\n", encoding="utf-8")
    return changed


def resolve_targets(root: Path, paths: list[str]) -> list[Path]:
    if paths:
        return [Path(p).resolve() for p in paths]
    candidates = root.glob("narrative/writers_room/releases/**/day*_non_canon.md")
    return sorted(p for p in candidates if DAYRXX_NON_CANON_RE.fullmatch(p.name))


def main() -> None:
    parser = argparse.ArgumentParser(description="Format dayrxx_non_canon.md files.")
    parser.add_argument("paths", nargs="*", help="Optional files to format")
    parser.add_argument("--check", action="store_true", help="Check only; do not write")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    targets = resolve_targets(root, args.paths)
    if not targets:
        raise SystemExit("No target files found.")

    changed_files = []
    for target in targets:
        if process_file(target, write=not args.check):
            changed_files.append(target)

    mode = "would change" if args.check else "changed"
    print(f"{len(changed_files)} file(s) {mode}.")
    for f in changed_files:
        print(f"- {f}")

    if args.check and changed_files:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
