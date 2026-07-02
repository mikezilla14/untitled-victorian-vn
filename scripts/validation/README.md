# Validation internals

Implementation modules behind stable root-level validation commands. Agents and CI should call the root wrappers in [`scripts/`](../README.md), not import from here directly unless extending the validation stack.

## Modules

| File | Role |
|------|------|
| `balance_profile_lint.py` | Lint semantic balance profiles against catalogue rules. |
| `balance_report_impl.py` | Shared logic for static balance report generation. |

## Stable entrypoints

| Command | Wrapper |
|---------|---------|
| `py scripts/balance_report.py --release release-1-mvp` | [`scripts/balance_report.py`](../balance_report.py) |
| `py scripts/balance_profile_lint.py` | Root wrapper (if present) or direct module per skill docs |
| `py scripts/validate.py --profile changed --files "<paths>"` | [`scripts/validate.py`](../validate.py) |

When moving or renaming modules here, update [`docs/architecture/scripts_refactor_map.md`](../../docs/architecture/scripts_refactor_map.md) and preserve root CLI compatibility.
