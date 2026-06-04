# Scripts

This folder contains local and CI helper scripts for validation, migration, catalogue refreshes, and
deterministic post-processing. Scripts are meant to be run from the repository root.

## Common commands

| Command | Purpose |
|---------|---------|
| `py scripts/validate.py --profile changed --agent human --files "<paths>"` | Standard changed-file validation entry. |
| `py scripts/orchestrate_review.py --files "<paths>"` | Pre-PR narrative contract bundle. |
| `py scripts/contract_validate.py --day day105 --release release-1-mvp` | Validate per-day JSON/markdown handoffs. |
| `py scripts/scene_direction.py --check --files "<day_non_canon.rpy>"` | Check deterministic sprite placement lines. |
| `py scripts/documentation_audit.py --write` | Refresh documentation catalogue and audit artifacts. |
| `py scripts/documentation_audit.py --check` | Fail when generated documentation catalogue artifacts are stale. |

## Maintenance

When adding a script, document its role here if it becomes part of normal agent, CI, or human
workflow. One-off migrations should live under `scripts/archive/one_off_migrations/`.
