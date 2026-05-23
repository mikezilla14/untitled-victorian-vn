#!/usr/bin/env python3
"""Rewrite legacy narrative path strings after layout refactor."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {".git", ".claude", "__pycache__", "node_modules"}
TEXT_SUFFIXES = {".md", ".mdc", ".py", ".yml", ".json", ".rpy"}

BASE_REPLACEMENTS: list[tuple[str, str]] = [
    (
        "narrative/writers_room/releases/release 1 - mvp/",
        "narrative/draft/releases/release-1-mvp/",
    ),
    ("narrative/writers_room/", "narrative/draft/"),
    ("speculative/idea_archive/releases/release 1 - mvp/", "narrative/pipeline/releases/release-1-mvp/"),
    ("speculative/spec_scripts/releases/release 1 - mvp/", "narrative/pipeline/releases/release-1-mvp/"),
    ("speculative/idea_archive/", "narrative/pipeline/"),
    ("speculative/spec_scripts/", "narrative/pipeline/"),
    ("speculative/writing_experiments/", "narrative/pipeline/experiments/"),
    ("speculative/", "narrative/pipeline/"),
    ("narrative/templates/Voice_Guides/", "narrative/canon/voice_guides/"),
]

REGEX_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    # Draft day scripts -> per-day folders
    (
        re.compile(
            r"narrative/draft/releases/([^/]+)/day([0-9]{3})_non_canon\.rpy"
        ),
        r"narrative/draft/releases/\1/days/day\2/day\2_non_canon.rpy",
    ),
    # Pipeline artifacts -> typed subfolders
    (
        re.compile(
            r"narrative/pipeline/releases/([^/]+)/day([0-9]{3})_gate_"
        ),
        r"narrative/pipeline/releases/\1/days/day\2/gates/day\2_gate_",
    ),
    (
        re.compile(
            r"narrative/pipeline/releases/([^/]+)/day([0-9]{3})_convergent_report"
        ),
        r"narrative/pipeline/releases/\1/days/day\2/synthesis/day\2_convergent_report",
    ),
    (
        re.compile(
            r"narrative/pipeline/releases/([^/]+)/day([0-9]{3})_([a-z]+)_ideas"
        ),
        r"narrative/pipeline/releases/\1/days/day\2/ideas/day\2_\3_ideas",
    ),
    (
        re.compile(
            r"narrative/pipeline/releases/([^/]+)/day([0-9]{3})_([a-z]+)_spec\.rpy"
        ),
        r"narrative/pipeline/releases/\1/days/day\2/specs/day\2_\3_spec.rpy",
    ),
    (
        re.compile(
            r"narrative/pipeline/releases/([^/]+)/day([0-9]{3})_profile_delta\.json"
        ),
        r"narrative/pipeline/releases/\1/days/day\2/handoffs/day\2_profile_delta.json",
    ),
    (
        re.compile(
            r"narrative/pipeline/releases/([^/]+)/day([0-9]{3})_promotion_handoff\.json"
        ),
        r"narrative/pipeline/releases/\1/days/day\2/handoffs/day\2_promotion_handoff.json",
    ),
    (
        re.compile(
            r"narrative/pipeline/releases/([^/]+)/day([0-9]{3})_forensic_psychology_profile_report"
        ),
        r"narrative/pipeline/releases/\1/days/day\2/handoffs/day\2_forensic_psychology_profile_report",
    ),
    # Release slug in JSON
    (
        re.compile(r'"release": "release 1 - mvp"'),
        '"release": "release-1-mvp"',
    ),
    # Planning docs
    (
        re.compile(
            r"narrative/draft/releases/([^/]+)/story_board\.md"
        ),
        r"narrative/draft/releases/\1/planning/story_board.md",
    ),
    (
        re.compile(
            r"narrative/draft/releases/([^/]+)/continuity_handoff\.md"
        ),
        r"narrative/draft/releases/\1/planning/continuity_handoff.md",
    ),
]


def transform(text: str, *, normalize_slashes: bool = True) -> str:
    updated = text.replace("\\", "/") if normalize_slashes else text
    for old, new in BASE_REPLACEMENTS:
        updated = updated.replace(old, new)
    for pattern, repl in REGEX_REPLACEMENTS:
        updated = pattern.sub(repl, updated)
    return updated


def patch_file(path: Path) -> bool:
    if path.name in {"update_path_references.py", "migrate_narrative_layout.py"}:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    updated = transform(text, normalize_slashes=path.suffix != ".py")
    if updated == text:
        return False
    if path.suffix == ".json":
        try:
            updated = json.dumps(json.loads(updated), indent=2) + "\n"
        except json.JSONDecodeError:
            pass
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if patch_file(path):
            print(path.relative_to(ROOT))
            changed += 1
    print(f"\nUpdated {changed} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
