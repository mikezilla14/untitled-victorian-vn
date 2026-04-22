# Narrative workflow (MVP)

The product is a **playable Ren’Py MVP** in `renpy_project/`. Narrative design in markdown is **supporting material**, not a parser pipeline.

## Your loop

1. **Write a pseudo-script** for Ren’Py in markdown under `narrative/writers_room/` (one file can cover several days). Use whatever structure helps you think: headings, scene beats, `menu:` / `label:` sketches, `$ player...` notes, flags, dialogue blocks. It does **not** need to be valid Ren’Py yet.
2. **Historical pass** — run `scripts/historical_linter.py` on the markdown (CI runs it when those files change). Fix or justify flagged anachronisms; align with `narrative/templates/voice_guide.md` where relevant.
3. **Implementation** — hand the pseudo-script to the **coding agent** and iterate until the behavior exists in `renpy_project/game/*.rpy`.
4. **Architecture** — the **chief architect** reviews Ren’Py changes for methodology (state, structure, no leaky globals, lint), not for markdown format.

## Day file naming contract

- **Non-canon markdown drafts** must be named `dayrxx_non_canon.md`.
- **Ren'Py episodic files** must be named `dayrxx.rpy`.
- `r` is the release number, and `xx` is the 2-digit day number (`01`-`99`).
- Example: release 1 day 1 -> `day101_non_canon.md` and `day101.rpy`.
- This contract is enforced in CI via `scripts/engineering_compliance.py`.

## What is *not* in scope for MVP

- No required JSON beat payloads, no markdown→JSON→Ren’Py automation.
- Deferred ideas live in **`docs/backlog/`** (see `docs/backlog/narrative-json-beat-pipeline.md`).

## Optional pseudo-script conventions

These are suggestions, not rules:

- **Labels:** `label day2_morning:` as a line you intend to become a Ren’Py label.
- **Menus:** sketch branches with intent, e.g. `menu: # risky vs safe`.
- **State:** `$ player.raise_suspicion(10)` or plain English: “after choice: +Susp, flag read_letters”.
- **Characters:** `cora "..."` / `gideon "..."` matching how you expect sprites to be defined in the game.

The coding agent turns this into real Ren’Py that matches `classes.rpy` / `variables.rpy` patterns.
