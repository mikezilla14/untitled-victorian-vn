# Game workspace (`main-game/`)

All story authoring and both Ren'Py projects live here. **Episodic canon** (what ships) is only in `prod-game/game/dayrdd.rpy`.

## Layout

| Path | Canon? | Purpose |
|------|--------|---------|
| [`canon/`](canon/) | **Yes** (static lore) | Characters, locations, mechanics, voice guides, historical guardrails |
| [`draft/`](draft/) | **No** | Release planning, bible databases, writer intents/exceptions |
| [`pipeline/`](pipeline/) | **No** | Pre-draft exploration: spec scripts, persona ideas, gates, handoffs |
| [`non-prod-game/`](non-prod-game/) | **No** | Sandbox Ren'Py project — `dayrdd_non_canon.rpy` drafts + full asset set |
| [`prod-game/`](prod-game/) | **Yes** (runtime) | Production Ren'Py project — promoted `dayrdd.rpy` |

## Release slug

Use kebab-case folder names under `pipeline/releases/`, e.g. `release-1-mvp`. JSON handoffs use the same slug in the `release` field.

## Per-day structure (MVP)

```
main-game/
  draft/releases/
    planning/              story_board.md, continuity_handoff.md (shared across releases)
    <release>/             intents/, exceptions/ (optional)
  non-prod-game/game/
    days/day105_non_canon.rpy
    shared/                cross-day sandbox .rpy
  pipeline/releases/release-1-mvp/days/day105/
    specs/                 divergent persona spec scripts
    ideas/                 persona brainstorming (do not load for new assignments)
    synthesis/             convergent reports (do not load for new assignments)
    gates/                 lead narrative / forensic / Victorian verdicts
    handoffs/              profile_delta, promotion_handoff JSON
  prod-game/game/
    day105.rpy             promoted runtime script
```

## Prose ownership rules

- Prose edits go in `non-prod-game/game/days/` unless the change is explicitly a runtime patch.
- If you fix prose directly in `prod-game/game/dayNNN.rpy`, mirror that change back to the matching `_non_canon.rpy` draft, or note the change in the promotion handoff JSON.
- When `non-prod-game/` and `prod-game/` diverge on prose, the non-prod draft is source of truth for future promotion.

## Context firewall (agents)

| Load by default | Do **not** load for new day assignments |
|-----------------|----------------------------------------|
| `canon/`, `draft/bible/`, `draft/releases/planning/` | `pipeline/**/ideas/`, `pipeline/**/synthesis/` |
| Current day `specs/` (convergent only) | Other days' `specs/` |
| Current `dayrdd_non_canon.rpy` | Prior days' drafts (use `continuity_handoff.md` instead) |

See [`pipeline/README.md`](pipeline/README.md) and [`.agents/rules/writers_room.md`](../.agents/rules/writers_room.md).

## Path helpers (CI)

`scripts/narrative_paths.py` is the single source of truth for layout paths used by `validate.py` and contract checks.
