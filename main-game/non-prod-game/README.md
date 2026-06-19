# Non-production Ren'Py sandbox

This is the playable sandbox Ren'Py project for the MVP. It is where non-canon day drafts, shared sandbox systems, UI, assets, and development-only tools can run before promotion to `main-game/prod-game/`.

For repo-level workflow rules, start at [`../../AGENTS.md`](../../AGENTS.md). For the source-of-truth path contract, see [`../../scripts/narrative_paths.py`](../../scripts/narrative_paths.py) and [`../README.md`](../README.md).

## Human contributor quickstarts

- Prose/editorial contributors: `docs/onboarding/prose_editor_quickstart.md`
- Agent workflow contributors: `AGENTS.md`
- Current MVP checklist: `main-game/draft/releases/planning/mvp_systems_integration_checklist.md`

## Source-of-truth status

This folder is **not production canon**.

| Area | Status | Notes |
|------|--------|-------|
| `game/days/` | Active sandbox day drafts | Use `dayNNN_non_canon.rpy`; these are the source drafts for future promotion. |
| `game/shared/` | Active sandbox support code | Shared non-prod classes, functions, story chains, and support labels. |
| `game/images/`, `game/audio/`, `game/gui/` | Sandbox runtime assets | May contain missing/fallback assets while MVP content is still being assembled. |
| `game/AEditor/` | Optional dev tooling | Development-only. Not part of the player path. |
| `../prod-game/` | Production runtime | Only promotion agents should copy approved content there. |

## Current narrative shape

The MVP is a five-day Ren'Py visual novel arc about Cora, a chambermaid at an 1891 London hotel, trying to survive staff scrutiny while gathering enough experience and manuscript material for Holywell Street.

The active non-prod day-file naming contract is:

```text
main-game/non-prod-game/game/days/dayNNN_non_canon.rpy
```

For release 1, current day identifiers normally follow:

| Day | Sandbox draft path | Production promotion target |
|-----|--------------------|-----------------------------|
| Day 1 | `game/days/day101_non_canon.rpy` | `main-game/prod-game/game/day101.rpy` |
| Day 2 | `game/days/day102_non_canon.rpy` | `main-game/prod-game/game/day102.rpy` |
| Day 3 | `game/days/day103_non_canon.rpy` | `main-game/prod-game/game/day103.rpy` |
| Day 4 | `game/days/day104_non_canon.rpy` | `main-game/prod-game/game/day104.rpy` |
| Day 5 | `game/days/day105_non_canon.rpy` | `main-game/prod-game/game/day105.rpy` |

## Core systems in scope

The sandbox currently supports or is expected to support these MVP systems:

- manuscript fuel gates and chapter progress;
- corruption/inspiration progression;
- suspicion/anxiety and character-specific pressure;
- story chains and consequence windows;
- penance/confrontation routing;
- Book1 manuscript writing blocks;
- fail states and soft-fail/rejection ending routes;
- structural asset manifest checks and fallback visibility.

For lifecycle status, use [`../../docs/architecture/feature_lifecycle_registry.md`](../../docs/architecture/feature_lifecycle_registry.md).

## Repository structure

```text
main-game/non-prod-game/
├── README.md
├── game/
│   ├── README.md
│   ├── AEditor/              # Optional ActionEditor/dev tooling
│   ├── audio/                # Sandbox audio assets
│   ├── days/                 # Non-canon day drafts and Book1 writing labels
│   ├── gui/                  # Ren'Py GUI assets/config support
│   ├── images/               # Backgrounds, sprites, UI images
│   ├── shared/               # Shared non-prod classes/functions/story chains
│   ├── saves/                # Local save files; should remain git-ignored
│   ├── gui.rpy               # Ren'Py UI configuration
│   ├── options.rpy           # Ren'Py project configuration
│   ├── screens.rpy           # Sandbox screens/HUD/UI definitions
│   └── script.rpy            # Sandbox entry point
└── utilities/                # Local development utilities, if present
```

## Agent rules

- Prose changes normally target `game/days/*_non_canon.rpy` through Writer's Desk, Writers' Room, or the approved narrative pipelines.
- Shared mechanics belong in `game/shared/` or the relevant sandbox support file, not directly in promoted prod files.
- Do not write production files from this folder except through `promote-day` or `promote-framework`.
- Do not route normal work through `game/AEditor/` unless the task explicitly targets ActionEditor tooling.
- Do not revive old root-level day paths such as `game/day101.rpy`; use `game/days/day101_non_canon.rpy` instead.

## Common validation

Run commands from the repository root:

```powershell
py scripts/validate.py --profile changed --agent human --files "main-game/non-prod-game/game/days/day105_non_canon.rpy"
py scripts/scene_direction.py --check --files "main-game/non-prod-game/game/days/day105_non_canon.rpy"
py scripts/documentation_audit.py --check
```

## Running the game

Open the project in the Ren'Py launcher and point it at `main-game/non-prod-game/`. Requires Ren'Py 7.x or 8.x.
