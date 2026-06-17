# Narrative workspace

All story authoring lives under `narrative/`. **Episodic canon** (what ships in the game) is only in `renpy_project/game/dayrdd.rpy` — not here.

## Layout

| Path | Canon? | Purpose |
|------|--------|---------|
| [`canon/`](canon/) | **Yes** (static lore) | Characters, locations, mechanics, voice guides — promoted truth |
| [`draft/`](draft/) | **No** | Promotion-bound non-canon scripts (`dayrdd_non_canon.rpy`), release planning, sandbox `.rpy` |
| [`pipeline/`](pipeline/) | **No** | Pre-draft exploration: spec scripts, persona ideas, gates, handoffs — **context-firewalled** |

## Release slug

Use kebab-case folder names, e.g. `release-1-mvp` (not `release 1 - mvp`). JSON handoffs use the same slug in the `release` field.

## Per-day structure (MVP)

```
narrative/draft/releases/
  planning/          story_board.md, continuity_handoff.md (shared across releases)
  release-1-mvp/
    shared/            cross-day sandbox .rpy
    days/day105/
      day105_non_canon.rpy
      briefs/          narrative change briefs (optional)

narrative/pipeline/releases/release-1-mvp/days/day105/
  specs/             divergent persona spec scripts
  ideas/             persona brainstorming logs (do not load for new assignments)
  synthesis/         convergent decision reports (do not load for new assignments)
  gates/             lead narrative / forensic / Victorian verdicts
  handoffs/          profile_delta, promotion_handoff JSON
```

## Prose ownership rules

- Prose edits go in `draft/` unless the change is explicitly a runtime patch.
- If you fix prose directly in `renpy_project/game/dayNNN.rpy`, mirror that change back to the matching `_non_canon.rpy` draft, or note the change in the promotion handoff JSON.
- When `draft/` and `renpy_project/game/` diverge on prose, `draft/` is source of truth for future promotion.

## Context firewall (agents)

| Load by default | Do **not** load for new day assignments |
|-----------------|----------------------------------------|
| `canon/`, `draft/bible/`, current `planning/` section | `pipeline/**/ideas/`, `pipeline/**/synthesis/` |
| Current day `specs/` (convergent only) | Other days' `specs/` |
| Current `dayrdd_non_canon.rpy` | Prior days' drafts (use `continuity_handoff.md` instead) |

See [`pipeline/README.md`](pipeline/README.md) and [`.agents/rules/writers_room.md`](../.agents/rules/writers_room.md).

## Path helpers (CI)

`scripts/narrative_paths.py` is the single source of truth for layout paths used by `validate.py` and contract checks.
