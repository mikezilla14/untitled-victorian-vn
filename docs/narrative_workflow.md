# Narrative workflow (MVP)

The product is a **playable Ren'Py MVP** in `renpy_project/`. Non-canon day scripts in `narrative/writers_room/` are supporting design/implementation input, not a parser pipeline.

## Your loop

1. **Write a non-canon day draft** in Ren'Py-shaped form under `narrative/writers_room/` using `dayrdd_non_canon.rpy` naming. These drafts can include implementation notes, but should stay promotion-ready for runtime `.rpy`.
2. **Historical pass** — run `scripts/historical_linter.py` on the draft file (CI runs it when those files change). Fix or justify flagged anachronisms; align with `narrative/templates/Voice_Guides/*_voice_guide.md` where relevant.
3. **Implementation** — hand the non-canon draft to the **coding agent** and iterate until behavior exists in `renpy_project/game/dayrdd.rpy`.
4. **Architecture** — the **chief architect** reviews Ren'Py changes for methodology (class-backed `StoryState` / stats, whitelisted setters for exclusive branches, no direct field assignment in scripts, no leaky globals, lint), not prose formatting preferences.

## Day file naming contract

- **Non-canon draft scripts** must be named `dayrdd_non_canon.rpy`.
- **Ren'Py episodic runtime files** must be named `dayrdd.rpy`.
- `r` is the release number, and `dd` is the 2-digit day slot (`00`-`99`).
- Example: release 1 prologue/day 00 -> `day100_non_canon.rpy`; release 1 day 1 -> `day101_non_canon.rpy` and `day101.rpy`.
- This contract is enforced in CI via `scripts/engineering_compliance.py`.

## What is *not* in scope for MVP

- No required JSON beat payloads, no markdown→JSON→Ren’Py automation.
- Deferred ideas live in **`docs/backlog/`** (see `docs/backlog/narrative-json-beat-pipeline.md`).

## Optional non-canon draft conventions

These are suggestions, not rules:

- **Labels:** `label day2_morning:` as a line you intend to become a Ren’Py label.
- **Menus:** sketch branches with intent, e.g. `menu: # risky vs safe`.
- **State:** `$ player.raise_suspicion(10)` or plain English: “after choice: +Susp, flag read_letters”.
- **Characters:** `cora "..."` / `gideon "..."` matching how you expect sprites to be defined in the game.

The coding agent promotes this into runtime Ren'Py that matches `classes.rpy` / `variables.rpy` patterns.

## Supporting narrative databases

- **Main characters (non-canon):** `narrative/writers_room/<name>_character_non_canon.md`
- **Minor characters (non-canon):** `narrative/writers_room/characters_non_canon.md`
- **Locations (non-canon):** `narrative/writers_room/locations_non_canon.md`
- **Voice guides:** `narrative/templates/Voice_Guides/*_voice_guide.md`
- Canon mirrors should live in `narrative/canon/` using `_canon.md` equivalents.
