# Runtime vs model comparison

**Release:** `release-1-mvp`
**Generated:** 2026-06-21 13:24 UTC
**Capture dir:** `main-game/non-prod-game/debug_captures`
**Rollback policy:** rollback-contaminated captures invalid for balance proof

## Summary

| Run | Capture | Structure | Assertions | Rollback | Balance proof | Notes |
|---|---|---|---|---|---|---|
| `P1_corruption_forward` | present | PASS | PASS | no | PASS | ending=day105_7_release_one_ending |
| `P2_cautious` | present | PASS | FAIL | no | PASS | ending=day105_7_release_one_ending |
| `P3_low_corruption` | missing | — | — | — | — | No JSONL file |
| `P4_deadline_1` | present | PASS | PASS | no | PASS | ending=game_over_deadline_1 |
| `P5_deadline_2` | missing | — | — | — | — | No JSONL file |
| `P6_anxiety_collapse` | missing | — | — | — | — | No JSONL file |
| `P7_penance` | missing | — | — | — | — | No JSONL file |

## Assertion detail

| Run | Assertion | Expected | Pass | Detail |
|---|---|---|---|---|
| `P1_corruption_forward` | `assert_ending` | `"day105_7_release_one_ending"` | yes | endings=['day105_7_release_one_ending'] |
| `P1_corruption_forward` | `assert_stat_floor` | `{"manuscript_progress": 5}` | yes | stats={'anxiety': 45, 'corruption_level': 8, 'corruption_xp': 5, 'inspiration': 50, 'inspiration_cap': 50, 'manuscript_progress': 5} |
| `P2_cautious` | `assert_reaches_day_at_least` | `105` | no | day=5 |
| `P4_deadline_1` | `assert_ending` | `"game_over_deadline_1"` | yes | endings=['game_over_deadline_1'] |

## Missing captures

- `P3_low_corruption.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`
- `P5_deadline_2.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`
- `P6_anxiety_collapse.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`
- `P7_penance.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`

## Limits

- Compares final snapshots and ending labels only; does not replay rollback vectors yet.
- Captures containing `rollback_event` are rejected for balance proof unless `--allow-rollback`.
- `balanced_effect` events are re-resolved against `effect_profiles.yaml` at compare time.
- Abstract simulator (`simulate_balance.py`) may disagree until P1–P7 captures exist.
