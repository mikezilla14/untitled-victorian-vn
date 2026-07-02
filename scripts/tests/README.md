# Script tests

Pytest suite for repository tooling (validation, balance, standup, scene direction, Ren'Py SDK helpers).

## Run

From the repository root:

```powershell
py -m pytest scripts/tests/
py -m pytest scripts/tests/test_daily_standup.py
py -m pytest scripts/tests/test_compare_runtime_capture.py
```

## Scope

| Module | Covers |
|--------|--------|
| `test_balance_profile_lint.py` | Semantic balance profile lint |
| `test_balance_catalogue.py` | Choice catalogue import/build |
| `test_balance_resolver.py` | Balance resolver semantics |
| `test_compare_runtime_capture.py` | Runtime vs model comparison |
| `test_daily_standup.py` | Daily standup script |
| `test_renpy_sdk.py` | Ren'Py SDK path helpers |
| `test_scene_direction.py` | Scene direction post-processor |
| `test_validation_path_support.py` | Path resolution for validation |

CI and local pre-PR checks may run a subset; see [`scripts/README.md`](../README.md) and [`.github/workflows/gatekeeper.yml`](../../.github/workflows/gatekeeper.yml).
