# ActionEditor

This folder contains Ren'Py ActionEditor/dev tooling for in-engine animation or staging support.

## Status

- **Feature lifecycle:** `optional-dev`.
- **Player path:** not part of the normal player-facing story path.
- **Agent default:** do not edit unless the task explicitly targets ActionEditor behaviour.

## Rules

- Keep ActionEditor changes separate from prose, story routing, asset manifest, and promotion PRs.
- Do not treat files here as project-authored narrative or runtime systems.
- If ActionEditor stops being useful, mark it as `remove-candidate` in `docs/architecture/feature_lifecycle_registry.md` before removing it.
