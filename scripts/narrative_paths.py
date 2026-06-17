#!/usr/bin/env python3
"""Canonical game workspace paths — single source of truth for CI and agents."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_GAME = ROOT / "main-game"

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
        return release_display_name(self.release_slug)


def parse_day_id(filename: str) -> str | None:
    match = DAY_ID_RE.match(filename)
    return match.group(1) if match else None


def canon_root() -> Path:
    return MAIN_GAME / "canon"


def draft_root() -> Path:
    return MAIN_GAME / "draft"


def planning_dir() -> Path:
    return draft_root() / "releases" / "planning"


def draft_release_root(release_slug: str) -> Path:
    return draft_root() / "releases" / normalize_release_slug(release_slug)


def non_prod_game_dir() -> Path:
    return MAIN_GAME / "non-prod-game"


def prod_game_dir() -> Path:
    return MAIN_GAME / "prod-game"


def draft_day_dir(ctx: DayContext) -> Path:
    return non_prod_game_dir() / "game" / "days"


def draft_shared_dir() -> Path:
    return non_prod_game_dir() / "game" / "shared"


def draft_non_canon_path(ctx: DayContext) -> Path:
    return draft_day_dir(ctx) / f"{ctx.day_id}_non_canon.rpy"


def prod_day_path(ctx: DayContext) -> Path:
    return prod_game_dir() / "game" / f"{ctx.day_id}.rpy"


def pipeline_root() -> Path:
    return MAIN_GAME / "pipeline"


def pipeline_release_root(release_slug: str) -> Path:
    return pipeline_root() / "releases" / normalize_release_slug(release_slug)


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
    """Parse main-game/non-prod-game/game/days/dayNNN_non_canon.rpy."""
    path = file_path.resolve()
    try:
        rel = path.relative_to(non_prod_game_dir() / "game" / "days")
    except ValueError:
        return _parse_legacy_non_canon_path(path)
    filename = rel.parts[-1] if rel.parts else rel.name
    if not filename.endswith("_non_canon.rpy"):
        return None
    day_id = filename.replace("_non_canon.rpy", "")
    if not DAY_ID_RE.match(day_id):
        return None
    return DayContext(day_id=day_id, release_slug=DEFAULT_RELEASE_SLUG)


def _parse_legacy_non_canon_path(file_path: Path) -> DayContext | None:
    legacy_root = ROOT / "narrative" / "draft" / "releases"
    try:
        rel = file_path.relative_to(legacy_root)
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


LEGACY_WRITERS_ROOM_PREFIX = "narrative/draft/"
LEGACY_SPECULATIVE_PREFIX = "narrative/pipeline/"
LEGACY_PROD_PREFIX = "renpy_project/"
