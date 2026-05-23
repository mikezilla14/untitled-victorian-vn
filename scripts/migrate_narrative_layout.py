#!/usr/bin/env python3
"""
One-time migration: writers_room + speculative -> narrative/draft + narrative/pipeline.

Run from repo root:
  py scripts/migrate_narrative_layout.py --dry-run
  py scripts/migrate_narrative_layout.py
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

from narrative_paths import (
    DEFAULT_RELEASE_NAME,
    DEFAULT_RELEASE_SLUG,
    DayContext,
    ROOT,
    draft_release_root,
    pipeline_day_dir,
    pipeline_gates_dir,
    pipeline_handoffs_dir,
    pipeline_ideas_dir,
    pipeline_release_root,
    pipeline_specs_dir,
    pipeline_synthesis_dir,
)

OLD_RELEASE = DEFAULT_RELEASE_NAME
NEW_SLUG = DEFAULT_RELEASE_SLUG

WRITERS_ROOM = ROOT / "narrative" / "writers_room"
SPECULATIVE = ROOT / "speculative"
OLD_ARCHIVE = SPECULATIVE / "idea_archive" / "releases" / OLD_RELEASE
OLD_SPECS = SPECULATIVE / "spec_scripts" / "releases" / OLD_RELEASE
OLD_WR_RELEASE = WRITERS_ROOM / "releases" / OLD_RELEASE

DAY_FILE_RE = re.compile(r"^(day[0-9]{3})")


def ensure_dir(path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    path.mkdir(parents=True, exist_ok=True)


def move_file(src: Path, dst: Path, dry_run: bool) -> None:
    if not src.exists():
        return
    ensure_dir(dst.parent, dry_run)
    print(f"  {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
    if dry_run:
        return
    if dst.exists():
        dst.unlink()
    shutil.move(str(src), str(dst))


def ctx_for(day_id: str) -> DayContext:
    return DayContext(day_id=day_id, release_slug=NEW_SLUG)


def migrate_pipeline_artifacts(dry_run: bool) -> None:
    print("\n== Pipeline artifacts ==")
    if not OLD_ARCHIVE.exists() and not OLD_SPECS.exists():
        print("  (no legacy speculative release folder)")
        return

    for path in sorted(OLD_ARCHIVE.glob("*")) if OLD_ARCHIVE.exists() else []:
        name = path.name
        m = DAY_FILE_RE.match(name)
        if not m:
            print(f"  SKIP unscoped: {path.name}")
            continue
        day_id = m.group(1)
        ctx = ctx_for(day_id)

        if name.endswith("_ideas.md"):
            move_file(path, pipeline_ideas_dir(ctx) / name, dry_run)
        elif name.endswith("_convergent_report.md"):
            move_file(path, pipeline_synthesis_dir(ctx) / name, dry_run)
        elif "_gate_" in name:
            move_file(path, pipeline_gates_dir(ctx) / name, dry_run)
        elif name.endswith("_profile_delta.json") or name.endswith("_promotion_handoff.json"):
            move_file(path, pipeline_handoffs_dir(ctx) / name, dry_run)
        elif name.endswith("_forensic_psychology_profile_report.md"):
            move_file(path, pipeline_handoffs_dir(ctx) / name, dry_run)
        else:
            print(f"  SKIP unknown: {name}")

    if OLD_SPECS.exists():
        for path in sorted(OLD_SPECS.glob("day*_spec.rpy")):
            day_id = path.name.split("_")[0]
            move_file(path, pipeline_specs_dir(ctx_for(day_id)) / path.name, dry_run)

    experiments = SPECULATIVE / "writing_experiments"
    new_experiments = ROOT / "narrative" / "pipeline" / "experiments"
    if experiments.exists():
        ensure_dir(new_experiments, dry_run)
        for item in experiments.iterdir():
            move_file(item, new_experiments / item.name, dry_run)


def migrate_draft(dry_run: bool) -> None:
    print("\n== Draft (non-canon) ==")
    draft_root = draft_release_root(NEW_SLUG)
    planning = draft_root / "planning"
    shared = draft_root / "shared"
    bible = ROOT / "narrative" / "draft" / "bible"

    for name in ("story_board.md", "continuity_handoff.md"):
        src = OLD_WR_RELEASE / name
        move_file(src, planning / name, dry_run)

    if OLD_WR_RELEASE.exists():
        for path in OLD_WR_RELEASE.iterdir():
            if path.name.startswith("day") and path.name.endswith("_non_canon.rpy"):
                day_id = path.name.replace("_non_canon.rpy", "")
                move_file(path, draft_root / "days" / day_id / path.name, dry_run)
            elif path.suffix == ".rpy" or path.name.endswith("_notes.md"):
                move_file(path, shared / path.name, dry_run)

    for name in (
        "characters_non_canon.md",
        "locations_non_canon.md",
        "cora_character_non_canon.md",
    ):
        src = WRITERS_ROOM / name
        move_file(src, bible / name, dry_run)

    templates = ROOT / "narrative" / "templates" / "Voice_Guides"
    canon_vg = ROOT / "narrative" / "canon" / "voice_guides"
    if templates.exists():
        ensure_dir(canon_vg, dry_run)
        for path in templates.glob("*.md"):
            dst = canon_vg / path.name
            if dst.exists():
                print(f"  SKIP duplicate voice guide: {path.name}")
                continue
            move_file(path, dst, dry_run)


def prune_empty(dry_run: bool) -> None:
    if dry_run:
        return
    for folder in (
        OLD_ARCHIVE,
        OLD_SPECS,
        OLD_WR_RELEASE,
        WRITERS_ROOM / "releases",
        SPECULATIVE / "idea_archive" / "releases",
        SPECULATIVE / "spec_scripts" / "releases",
        SPECULATIVE,
        WRITERS_ROOM,
        ROOT / "narrative" / "templates",
    ):
        if folder.exists() and folder.is_dir():
            try:
                folder.rmdir()
            except OSError:
                pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"Migrating release {OLD_RELEASE!r} -> slug {NEW_SLUG!r}")
    migrate_pipeline_artifacts(args.dry_run)
    migrate_draft(args.dry_run)
    prune_empty(args.dry_run)
    print("\nDone. Update JSON `release` fields to use slug or display name consistently.")
    print("Run: py scripts/validate.py --profile full (after updating path references)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
