# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An AI-accelerated adult pseudo-sandbox RPG visual novel set at the Savoy Hotel, London (Winter 1891). Built with **Ren'Py 8.x** as the playable deliverable, plus an **agentic narrative production pipeline** using specialist AI roles. MVP is Release 1: five episodic days (`day101`–`day105`) fully scripted with branching choices, stat tracking, and three ending states.

## Commands

### Validation (run before PRs or AI handoffs)
```bash
# Validate specific changed files (CI entry point)
python scripts/validate.py --profile changed --files "renpy_project/game/day106.rpy,narrative/draft/day106_non_canon.rpy"

# Validate only code files
python scripts/validate.py --profile code --files "renpy_project/game/day106.rpy"

# Validate only narrative drafts
python scripts/validate.py --profile narrative --files "narrative/draft/day106_non_canon.rpy"

# Full repository audit
python scripts/validate.py --profile full
```

### Local AI orchestration review
```bash
# Run Code Agent + Chief Architect checks and generate AI remediation prompts
python scripts/orchestrate_review.py --files narrative/draft/day106_non_canon.rpy,renpy_project/game/day106.rpy
```

### Ren'Py lint (requires Ren'Py SDK on PATH)
```bash
renpy lint renpy_project/
```

### Historical linter (standalone)
```bash
python scripts/historical_linter.py narrative/draft/day106_non_canon.rpy
```

### Run the game
Launch via the Ren'Py SDK launcher (GUI) pointing at `renpy_project/`, or via the `renpy` CLI. There is no `npm`/`pip install` step — Ren'Py is a standalone runtime.

## Repository Architecture

```
/
├── renpy_project/game/     # Playable game — the core MVP deliverable
├── narrative/
│   ├── writers_room/       # Non-canon drafts (Writers' Room + Lead Editor)
│   └── canon/              # Locked truth (Lead Narrative Editor only)
├── docs/                   # Mechanics bible, narrative workflow, compliance
├── scripts/                # CI validation tooling
├── .agents/rules/          # AI agent system prompts (six specialist roles)
└── .guardrails.yml         # Domain boundary enforcement
```

### Game source structure (`renpy_project/game/`)

| File | Role |
|------|------|
| `classes.rpy` | All Python class definitions: `TimeManager`, `PlayerStats`, `StoryState` |
| `variables.rpy` | Singleton instantiation only — one `default` declaration per class |
| `functions.rpy` | Shared game logic helpers called from narrative scripts |
| `script.rpy` | Thin entry point; jumps to `day101_main` |
| `characters.rpy` | Character sprite definitions (`define speaker = Character(...)`) |
| `assets_manifest.rpy` | Centralized asset declarations with fallback placeholders |
| `screens.rpy` | HUD overlay, ledger screen, UI templates |
| `gui.rpy` / `options.rpy` | Ren'Py UI config — touch only with Chief Architect role |
| `day101.rpy` – `day105.rpy` | Episodic narrative scripts (owned by Code Agent) |
| `endings.rpy` | Hard fail, soft fail, and success ending labels |

## State Architecture

All game state is **class-backed** — no raw Ren'Py globals. Three persistent objects (declared in `variables.rpy`, defined in `classes.rpy`):

- **`time_manager`** (`TimeManager`): Day number and time-of-day period. Valid periods: `"Early Morning"`, `"Morning"`, `"Afternoon"`, `"Evening"`, `"Night"`, `"Late Night"`.
- **`player`** (`PlayerStats`): `inspiration` (writing resource, capped at `20 + corruption_level × 10`), `corruption_xp`/`corruption_level`, and `suspicion` (0–100; 100 = game over).
- **`story`** (`StoryState`): ~50 narrative flags — binary booleans and mutually exclusive string branches.

### Mutation rules (enforced by CI)

```renpy
# ✓ CORRECT — use setters and helpers
$ story.set_corridor_state("predator")        # string branch
$ story.set_has_witnessed_voyeur_scene(True)  # boolean flag
$ player.gain_inspiration(10)
$ player.raise_suspicion(5)
$ apply_effects(insp=15, corr=5, susp=10)    # combined stat delta

# ✗ FORBIDDEN — direct assignment on state objects
$ story.day1_corridor_state = "predator"     # bypasses whitelist validation
$ player.inspiration = 50                    # bypasses bounds enforcement
```

Reading state directly in `if` conditions is always allowed.

### Key functions (`functions.rpy`)

| Function | Purpose |
|----------|---------|
| `apply_effects(insp=0, corr=0, susp=0)` | Combined stat delta. Positive `insp` = gain; negative = spend (returns bool). Corruption never decreases. |
| `attempt_write(required_insp=30, cost=20)` | Writing-gate check + spend. Returns `True` if passed. |
| `has_story_fuel(required_total=15)` | Read-only fuel check (inspiration + corruption_xp). |
| `resolve_turn()` | Calls `check_suspicion` label then `update_stats()` — always in this order. |
| `set_time_period(period)` | Advances time via `TimeManager` with validation. |
| `show_ledger_ui()` | Pauses narrative and shows the HUD ledger screen. |

## Key Code Conventions

### Mutually exclusive branches

Use a single string field with a whitelist rather than multiple booleans. Every `StoryState` exclusive branch has a `VALID_*` tuple and a typed setter. For example:

```python
VALID_CORRIDOR_STATES = ("none", "ghost", "predator", "prey")
def set_corridor_state(self, value): ...
```

Default is always `"none"`. Never represent the same fork with multiple booleans.

### Bracket interpolation in Ren'Py strings

```renpy
# ✓ CORRECT — double brackets escape to literal text
menu:
    "Gain [[Inspiration]] and [[Corruption]].":

# ✗ WRONG — single brackets evaluate as Python variables at runtime
menu:
    "Gain [Inspiration] and [Corruption].":
```

### Asset fallbacks

`assets_manifest.rpy` registers placeholder solid-color images for all missing backgrounds/sprites. Missing audio is guarded before play (`if audio_name: renpy.play(...)`). Never assume an asset file exists — declare it in the manifest.

### New mechanics go in `functions.rpy`

Keep day scripts free of inline Python logic. If a mechanic is used more than once or is complex, add a function to `functions.rpy` and call it with `$` from the narrative.

## File Naming Contract

Enforced by `scripts/engineering_compliance.py` in CI:

- **Non-canon drafts:** `narrative/draft/releases/<release>/dayrdd_non_canon.rpy`
- **Runtime episodic scripts:** `renpy_project/game/dayrdd.rpy`

Where `r` = release number, `dd` = zero-padded day slot. Example: Release 1, Day 6 → `day106_non_canon.rpy` and `day106.rpy`.

## Narrative → Implementation Workflow

1. **Non-canon draft** — write `dayrdd_non_canon.rpy` in `narrative/draft/`. Use Ren'Py-shaped pseudo-code; state notes like `$ player.raise_suspicion(10)` or plain English descriptions are both fine.
2. **Historical pass** — CI runs `scripts/historical_linter.py` on changed `*_non_canon.rpy` files. Fix flagged anachronisms.
3. **Implementation** — Code Agent promotes the draft to `renpy_project/game/dayrdd.rpy`, using class-backed state and setter APIs.
4. **Architecture review** — Chief Architect checks methodology: class-backed state, whitelisted setters, no raw globals, `renpy lint` passes.

Use the **Orchestrator** for automated pipelines: paste `.agents/rules/orchestrator.md` as system prompt and state the task (e.g., `"Produce day 106: [brief]"`).

## Domain Boundaries (`.guardrails.yml`)

| Domain | Paths | Mutable By |
|--------|-------|-----------|
| `framework_code` | `classes.rpy`, `screens.rpy`, `characters.rpy`, `gui.rpy`, `options.rpy`, mechanics bible | `chief_architect`, `human` |
| `episodic_code` | `day*.rpy`, `endings.rpy`, `functions.rpy`, `script.rpy` | `code_agent`, `chief_architect`, `human` |
| `production_narrative` | `narrative/draft/**` | `writers_room`, `lead_narrative_editor`, `human` |
| `canon_lore` | `docs/canon/**`, `narrative/canon/**` | `lead_narrative_editor`, `victorian_consultant`, `human` |
| `repo_operations` | `scripts/**`, `.agents/**`, `docs/*.md`, `.github/**` | `chief_architect`, `gatekeeper_orchestrator`, `human` |
| `speculative_sandbox` | `narrative/pipeline/**` | `writers_room`, `code_agent`, `human` — no gatekeeping |

## CI

GitHub Actions (`.github/workflows/gatekeeper.yml`) runs on every PR to `develop` or `main`. It collects changed files and calls `python scripts/validate.py --profile changed --agent human --files <list>`. Checks: domain gatekeeper, engineering compliance (naming, no raw globals, setter usage), Ren'Py contract linter (speaker definitions, symbol resolution, asset existence), and historical linter on narrative drafts.

## Narrative Reference

- **Voice guides:** `narrative/canon/voice_guides/<name>_voice_guide.md` — consult for dialogue tone per character.
- **Character databases:** `narrative/draft/*_character_non_canon.md` (drafts) and `narrative/canon/characters_canon.md` (locked truth).
- **Locations:** `narrative/draft/locations_non_canon.md` and `narrative/canon/locations_canon.md`.
- **Mechanics:** `docs/game_mechanics_bible.md` — distinguishes active MVP mechanics from deferred post-MVP features.
