# Pipeline tools

Release-scoped analysis and balance tooling for the non-prod sandbox. Nothing here ships in the playable game; outputs land under `main-game/pipeline/releases/<release>/`.

## Commands

Run from the repository root.

| Script | Purpose |
|--------|---------|
| `py main-game/pipeline/tools/build_grain_manifest.py --release release-1-mvp` | Extract balance grains and gap report from sandbox `.rpy` files. |
| `py main-game/pipeline/tools/build_choice_catalogue.py --release release-1-mvp` | Import graph choices/effects into `choice_catalogue.csv`. |
| `py main-game/pipeline/tools/simulate_balance.py --release release-1-mvp` | Abstract policy/gate simulation and fuzz distribution report. |
| `py main-game/pipeline/tools/compare_runtime_to_model.py --release release-1-mvp` | Compare JSONL playtest captures to balance targets. |
| `py main-game/pipeline/tools/build_story_graph_manifest.py --release release-1-mvp` | Build DAG/story graph manifest from `[DAG_*]` tags. |

## Related docs

- [`main-game/pipeline/README.md`](../README.md) — pipeline folder layout
- [`scripts/balance_report.py`](../../../scripts/balance_report.py) — stable wrapper for static balance reports
- [`docs/architecture/feature_lifecycle_registry.md`](../../../docs/architecture/feature_lifecycle_registry.md) — testing and balance framework row

## Validation

- `py scripts/balance_report.py --release release-1-mvp`
- `py -m pytest scripts/tests/test_compare_runtime_capture.py scripts/tests/test_balance_catalogue.py`
