#!/usr/bin/env python3
"""Canonical narrative layout paths — single source of truth for CI and agents."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Release folder slug (paths) vs display name (JSON contracts)
DEFAULT_RELEASE_SLUG = "release-1-mvp"
DEFAULT_RELEASE_NAME = "release 1 - mvp"

RELEASE_SLUG_ALIASES: dict[str, str] = {
    "release 1 - mvp": DEFAULT_RELEASE_SLUG,
    DEFAULT_RELEASE_SLUG: DEFAULT_RELEASE_SLUG,
}

DAY_ID_RE = re.compile(r"^(day[0-9]{3})")


def normalize_release_slug(release: str) -> str:
    return RELEASE_SLUG_ALIASES.get(release.strip(), release.strip())


def release_display_name(release_slug: str) -> str:
    for display, slug in RELEASE_SLUG_ALIASES.items():
        if slug == release_slug and display != slug:
            return display
    return release_slug


class DayContext:
    __slots__ = ("day_id", "release_slug")

    def __init__(self, day_id: str, release_slug: str) -> None:
        self.day_id = day_id
        self.release_slug = normalize_release_slug(release_slug)

    @property
    def release_name(self) -> str:
        """Display name for JSON handoff contracts."""
        return release_display_name(self.release_slug)


def parse_day_id(filename: str) -> str | None:
    match = DAY_ID_RE.match(filename)
    return match.group(1) if match else None


def draft_release_root(release_slug: str) -> Path:
    return ROOT / "narrative" / "draft" / "releases" / normalize_release_slug(release_slug)


def draft_day_dir(ctx: DayContext) -> Path:
    return draft_release_root(ctx.release_slug) / "non_prod_renpy_project" / "game" / "days"


def draft_non_canon_path(ctx: DayContext) -> Path:
    return draft_day_dir(ctx) / f"{ctx.day_id}_non_canon.rpy"


def pipeline_release_root(release_slug: str) -> Path:
    return ROOT / "narrative" / "pipeline" / "releases" / normalize_release_slug(release_slug)


def pipeline_day_dir(ctx: DayContext) -> Path:
    return pipeline_release_root(ctx.release_slug) / "days" / ctx.day_id


def pipeline_specs_dir(ctx: DayContext) -> Path:
    return pipeline_day_dir(ctx) / "specs"


def pipeline_ideas_dir(ctx: DayContext) -> Path:
    return pipeline_day_dir(ctx) / "ideas"


def pipeline_synthesis_dir(ctx: DayContext) -> Path:
    return pipeline_day_dir(ctx) / "synthesis"


def pipeline_gates_dir(ctx: DayContext) -> Path:
    return pipeline_day_dir(ctx) / "gates"


def pipeline_handoffs_dir(ctx: DayContext) -> Path:
    return pipeline_day_dir(ctx) / "handoffs"


def parse_non_canon_path(file_path: Path) -> DayContext | None:
    """Parse narrative/draft/releases/<slug>/non_prod_renpy_project/game/days/dayNNN_non_canon.rpy."""
    try:
        rel = file_path.relative_to(ROOT / "narrative" / "draft" / "releases")
    except ValueError:
        return None
    parts = rel.parts
    if len(parts) < 5 or parts[1] != "non_prod_renpy_project" or parts[2] != "game" or parts[3] != "days":
        return None
    filename = parts[-1]
    if not filename.endswith("_non_canon.rpy"):
        return None
    day_id = filename.replace("_non_canon.rpy", "")
    if not DAY_ID_RE.match(day_id):
        return None
    return DayContext(day_id=day_id, release_slug=parts[0])


# Legacy path detection (pre-refactor) for helpful error messages
LEGACY_WRITERS_ROOM_PREFIX = "narrative/draft/"
LEGACY_SPECULATIVE_PREFIX = "narrative/pipeline/"
