# Backlog: JSON beat pipeline (deferred)

This repository previously explored a **markdown → JSON beat schema → Ren’Py** path (`validate_beats`, `sync_beats`, `narrative/beats`, etc.). That work is **deferred** so effort stays on **shipping the MVP** in `renpy_project/`.

## What was removed from the active toolchain

- Automated beat JSON validation in CI
- Beat catalog audit and sync/extract scripts
- `narrative/beats` as a required artifact

## Preserved for future reference

- **`beat_schema.json`** in this folder — optional contract if the JSON approach is revived later.

## Current MVP narrative path

See **`docs/narrative_workflow.md`**: pseudo-Ren’Py script in markdown → coding agent implements in `.rpy` → chief architect reviews methodology; historical accuracy via `scripts/historical_linter.py` (and Victorian Consultant role where used).
