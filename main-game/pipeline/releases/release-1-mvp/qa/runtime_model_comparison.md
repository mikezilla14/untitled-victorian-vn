# Runtime vs model comparison

**Release:** `release-1-mvp`
**Generated:** 2026-06-20 12:39 UTC
**Capture dir:** `main-game/non-prod-game/debug_captures`
**Rollback policy:** rollback-contaminated captures invalid for balance proof

## Summary

| Run | Capture | Structure | Assertions | Rollback | Balance proof | Notes |
|---|---|---|---|---|---|---|
| `P1_corruption_forward` | present | PASS | PASS | no | PASS | ending=day105_7_release_one_ending |

## Assertion detail

| Run | Assertion | Expected | Pass | Detail |
|---|---|---|---|---|
| `P1_corruption_forward` | `assert_ending` | `"day105_7_release_one_ending"` | yes | endings=['day105_7_release_one_ending'] |
| `P1_corruption_forward` | `assert_stat_floor` | `{"manuscript_progress": 5}` | yes | stats={'anxiety': 45, 'corruption_level': 8, 'corruption_xp': 5, 'inspiration': 50, 'inspiration_cap': 50, 'manuscript_progress': 5} |

## Limits

- Compares final snapshots and ending labels only; does not replay rollback vectors yet.
- Captures containing `rollback_event` are rejected for balance proof unless `--allow-rollback`.
- `balanced_effect` events are re-resolved against `effect_profiles.yaml` at compare time.
- Abstract simulator (`simulate_balance.py`) may disagree until P1–P7 captures exist.
