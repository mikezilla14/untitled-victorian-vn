# STUDIO DEVELOPMENT BIBLE

**Project:** [Pending Title]  
**Version:** 1.1  
**Scope:** Studio execution, release discipline, and Ren'Py engineering contracts.

This document is split into two parts:
- **MVP Contract (enforced now)**: rules that current code and workflow must follow.
- **Deferred Roadmap (not enforced now)**: planned systems after MVP.

---

## I. MVP Contract (Enforced)

### 1) Product Focus
- The deliverable is a **playable 5-day Ren'Py MVP** in `renpy_project/`.
- Narrative markdown is design input. Runtime truth is `.rpy` behavior.
- Any process/tooling that slows completion of the 5-day narrative and asset manifest is out of scope.

### 2) Scope Guardrails
- Standard release module cap remains:
  - max 3 primary characters,
  - max 6 primary backgrounds,
  - max 5 polished event CGs.
- New mechanics require explicit approval before implementation.

### 3) Ways of Work
- Writing/design happens in markdown pseudo-scripts (`narrative/writers_room/`).
- Historical checks run through `scripts/historical_linter.py`.
- Code implementation happens in `renpy_project/game/*.rpy`.
- Chief Architect enforces code methodology and consistency.

### 4) MVP Technical Architecture Contract

#### File responsibilities
- `script.rpy`: entry point and global guard labels only.
- `classes.rpy`: state class definitions.
- `variables.rpy`: state object instantiation via `default`.
- `functions.rpy`: shared Python helper logic (migrate repeated mechanics here as needed).
- `day*.rpy`, `endings.rpy`: narrative flow and branch content.

#### State discipline
- Core logic uses class-backed state (`TimeManager`, `PlayerStats`, `StoryState`).
- No ad hoc global `default` variables outside `variables.rpy`.
- Prefer mutation methods (`gain_*`, `raise_*`, `spend_*`) over direct field edits.

#### Failure and branch safety
- Suspicion fail checks must run in a deterministic order.
- Branch flags and stat changes must be traceable in scripts.

### 5) Release Cadence (Operational Target)
- Week 1: script lock (pseudo-script + implementation intent).
- Week 2: art generation from approved narrative/asset checklist.
- Week 3: Ren'Py assembly + branch wiring.
- Week 4: QA and fixes.
- Week 5: release and marketing.

---

## II. Deferred Roadmap (Not Enforced During MVP)

These items are valid future directions but are not current compliance targets:
- Full pseudo-sandbox hub navigation via clickmaps/screens.
- Dynamic paperdoll/layeredimage assembly as a full production system.
- Extended content pipeline automation beyond current MVP workflow.
- Optional structured narrative formats (kept in backlog docs).

---

## III. Cost Tracking Protocol (Studio)

Track effort and compute costs using:
- `CapEx_Infrastructure`
- `OpEx_Production`
- `Writing_Design`
- `Marketing_Admin`

Cloud GPU allocation:
- Base systems/training -> `CapEx_Infrastructure`
- Episode-specific outputs -> `OpEx_Production`
