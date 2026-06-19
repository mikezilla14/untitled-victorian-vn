# Architecture documentation

This folder holds repo-level architecture and process documents that sit above individual agent, narrative, contract, and runtime docs.

## Index

| Document | Purpose |
|----------|---------|
| [`active_processes.md`](active_processes.md) | Everyday process menu: which lane to use, who owns it, and what not to bypass. |
| [`feature_lifecycle_registry.md`](feature_lifecycle_registry.md) | Feature status, ownership, validation, deprecation, and removal decisions. |
| [`scripts_refactor_map.md`](scripts_refactor_map.md) | Safe migration contract for reorganising `scripts/` without breaking agent commands. |

## Rules

- Keep process-level decisions here when they affect more than one agent, folder, or pipeline.
- Keep implementation details in the owning spec, README, or contract file.
- Backlog ideas belong under `docs/backlog/` or `main-game/pipeline/` as appropriate.
