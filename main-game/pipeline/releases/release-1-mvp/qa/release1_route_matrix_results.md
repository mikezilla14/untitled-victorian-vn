# Release 1 route matrix results

**Release:** `release-1-mvp`  
**Purpose:** Human-readable playtest matrix record (complements `runtime_model_comparison.md` and JSONL captures).  
**Capture dir:** `main-game/non-prod-game/debug_captures/`

Regenerate machine checks:

```powershell
py main-game/pipeline/tools/compare_runtime_to_model.py --release release-1-mvp
```

## Matrix

| Run | Expected | Actual | Pass/fail | Rollback? | Notes |
|---|---|---|---|---|---|
| P1 | Day 105 MVP ending; `manuscript_progress` ≥ 5 | `day105_7_release_one_ending`; MS **5** (Corr L9, Insp 50/50, Anxiety 70) | **PASS** | no | Validated 2026-06-20 after Day 2 mandatory write fix. Capture: `P1_corruption_forward.jsonl` (260 events). Book1 ladder: day1+day2 same night (D102), then day3–day5. |
| P2 | Cautious completion / weak path; reach Day 105 | — | pending | — | Abstract sim: stops day 104. Needs runtime capture. |
| P3 | Rejection / soft fail (`bad_ending_rejection`) | — | pending | — | Abstract sim: deadline-1 mismatch. Needs runtime capture. |
| P4 | `game_over_deadline_1` | — | pending | — | Abstract sim: PASS. Good next thin capture. |
| P5 | `game_over_deadline_2` | — | pending | — | Abstract sim: PASS. |
| P6 | `game_over_dismissed` | — | pending | — | Abstract sim: PASS. |
| P7 | Confrontation / penance paths | — | pending | — | Abstract sim: INCOMPLETE (needs graph walk). |

## P1 evidence

| Item | Value |
|------|--------|
| Run ID | `P1_corruption_forward` |
| JSONL | `main-game/non-prod-game/debug_captures/P1_corruption_forward.jsonl` |
| Comparison | `main-game/pipeline/releases/release-1-mvp/qa/runtime_model_comparison.md` |
| Assertions | `assert_ending: day105_7_release_one_ending` ✓; `assert_stat_floor: manuscript_progress 5` ✓ |
| Structure | `run_start` → grains/choices/gates → `ending` → `run_end` |

## Status

- **Runtime captures:** 1 / 7 (P1 only)
- **Blockers:** none for P1
- **Next recommended:** P4 (fail path), then P2 or P3 (sim gaps)
