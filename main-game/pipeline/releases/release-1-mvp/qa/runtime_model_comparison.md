# Runtime vs model comparison

**Release:** `release-1-mvp`
**Generated:** 2026-06-19 22:58 UTC
**Capture dir:** `main-game/non-prod-game/debug_captures`

## Summary

| Run | Capture | Structure | Assertions | Rollback | Notes |
|---|---|---|---|---|---|
| `P1_corruption_forward` | missing | — | — | — | No JSONL file |
| `P2_cautious` | missing | — | — | — | No JSONL file |
| `P3_low_corruption` | missing | — | — | — | No JSONL file |
| `P4_deadline_1` | missing | — | — | — | No JSONL file |
| `P5_deadline_2` | missing | — | — | — | No JSONL file |
| `P6_anxiety_collapse` | missing | — | — | — | No JSONL file |
| `P7_penance` | missing | — | — | — | No JSONL file |

## Assertion detail

_No capture files with assertions to evaluate._

## Missing captures

- `P1_corruption_forward.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`
- `P2_cautious.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`
- `P3_low_corruption.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`
- `P4_deadline_1.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`
- `P5_deadline_2.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`
- `P6_anxiety_collapse.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`
- `P7_penance.jsonl` — play non-prod with `jump debug_capture_start` after setting `_capture_run_id`

## Limits

- Compares final snapshots and ending labels only; does not replay rollback vectors yet.
- Abstract simulator (`simulate_balance.py`) may disagree until P1–P7 captures exist.
