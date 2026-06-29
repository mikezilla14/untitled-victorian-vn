# Release 1 route matrix results

**Release:** `release-1-mvp`  
**Purpose:** Human-readable playtest matrix record (complements `runtime_model_comparison.md` and JSONL captures).  
**Detailed test plan:** [`release1_route_matrix_test_plan.md`](release1_route_matrix_test_plan.md)  
**Capture dir:** `main-game/non-prod-game/debug_captures/`  
**Last synced:** 2026-06-29

Regenerate machine checks:

```powershell
py main-game/pipeline/tools/compare_runtime_to_model.py --release release-1-mvp
```

## Matrix

| Run | Expected | Actual | Pass/fail | Rollback? | Notes |
|---|---|---|---|---|---|
| P1 | Day 105 MVP ending; `manuscript_progress` ≥ 5 | `day105_7_release_one_ending`; MS **5** | **PASS** | no | Capture: `P1_corruption_forward.jsonl`. Assertions: ending + manuscript floor. |
| P2 | Cautious path; reach Day 105 | `day105_7_release_one_ending`; runtime `current_day` **5** (slot index) | **PASS** | no | Capture: `P2_cautious.jsonl`. Day assertion normalized 5→105 in compare tool (2026-06-29). |
| P3 | Rejection / soft fail (`bad_ending_rejection`) | — | pending | — | Needs runtime capture. |
| P4 | `game_over_deadline_1` | `game_over_deadline_1` on Day 3 morning | **PASS** | no | Capture: `P4_deadline_1.jsonl`. |
| P5 | `game_over_deadline_2` | — | pending | — | Abstract sim: PASS. Needs runtime capture. |
| P6 | `game_over_dismissed` | — | pending | — | Abstract sim: PASS. Needs runtime capture. |
| P7 | Confrontation / penance paths | — | pending | — | Abstract sim: INCOMPLETE. Needs runtime capture. |

## P1 evidence

| Item | Value |
|------|--------|
| Run ID | `P1_corruption_forward` |
| JSONL | `main-game/non-prod-game/debug_captures/P1_corruption_forward.jsonl` |
| Comparison | `main-game/pipeline/releases/release-1-mvp/qa/runtime_model_comparison.md` |
| Assertions | `assert_ending: day105_7_release_one_ending` ✓; `assert_stat_floor: manuscript_progress 5` ✓ |

## P2 evidence

| Item | Value |
|------|--------|
| Run ID | `P2_cautious` |
| JSONL | `main-game/non-prod-game/debug_captures/P2_cautious.jsonl` |
| Ending | `day105_7_release_one_ending` |
| Assertions | `assert_reaches_day_at_least: 105` ✓ (runtime slot `5` normalized to file id `105`) |

## P4 evidence

| Item | Value |
|------|--------|
| Run ID | `P4_deadline_1` |
| JSONL | `main-game/non-prod-game/debug_captures/P4_deadline_1.jsonl` |
| Assertions | `assert_ending: game_over_deadline_1` ✓ |

## Status

- **Runtime captures:** 3 / 7 (P1, P2, P4)
- **Blockers:** none for recorded paths
- **Next recommended:** P5 (deadline-2 fail), then P3 / P6 / P7
