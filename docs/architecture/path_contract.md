# Active path contract

This document records the current active repo paths that agents should use. It exists to stop old generated or migrated path fragments from becoming instructions.

The implementation source of truth remains [`../../scripts/narrative_paths.py`](../../scripts/narrative_paths.py). This document is the human-readable companion.

## Active MVP paths

| Purpose | Active path |
|---------|-------------|
| Main game workspace | `main-game/` |
| Static promoted lore | `main-game/canon/` |
| Planning, bible, intents, exceptions | `main-game/draft/` |
| Pre-draft exploration | `main-game/pipeline/` |
| Sandbox Ren'Py project | `main-game/non-prod-game/` |
| Production Ren'Py project | `main-game/prod-game/` |
| Sandbox game folder | `main-game/non-prod-game/game/` |
| Sandbox day drafts | `main-game/non-prod-game/game/days/dayNNN_non_canon.rpy` |
| Sandbox shared support | `main-game/non-prod-game/game/shared/` |
| Production day files | `main-game/prod-game/game/dayNNN.rpy` |
| Release planning docs | `main-game/draft/releases/planning/` |
| Current release pipeline | `main-game/pipeline/releases/release-1-mvp/` |

## Legacy / stale path patterns

Do not add new docs or code that point at these patterns:

| Stale pattern | Replacement |
|---------------|-------------|
| `main-game/draft/releases/<release>/non_prod_main-game/prod-game/game/days/...` | `main-game/non-prod-game/game/days/dayNNN_non_canon.rpy` |
| `non_prod_main-game/prod-game/` | `main-game/non-prod-game/` or `main-game/prod-game/`, depending on context |
| `narrative/draft/` | `main-game/draft/` |
| `narrative/pipeline/` | `main-game/pipeline/` |
| `renpy_project/` | `main-game/prod-game/` or `main-game/non-prod-game/`, depending on context |
| `main-game/non-prod-game/game/day101.rpy` | `main-game/non-prod-game/game/days/day101_non_canon.rpy` |
| `main-game/non-prod-game/game/characters.rpy` | Check current asset/character declarations; do not assume this file exists. |

## Agent rules

- Use `scripts/narrative_paths.py` when building, validating, or promoting paths programmatically.
- Use `dayNNN_non_canon.rpy` in sandbox day docs and handoffs.
- Use `dayNNN.rpy` only for promoted production day files.
- Do not invent mixed paths by combining draft release paths with Ren'Py project paths.
- If a generated catalogue still contains stale paths, regenerate it locally after source docs are fixed.

## Related docs

- [`docs/agents/PIPELINE_REFERENCE.md`](../agents/PIPELINE_REFERENCE.md) — pipeline index; sandbox day path matches this contract.
