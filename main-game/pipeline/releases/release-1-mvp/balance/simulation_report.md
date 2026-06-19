# Release 1 balance simulation report

**Release:** `release-1-mvp`
**Generated:** 2026-06-19 21:51 UTC
**Model:** abstract day-budget simulator (not full Ren'Py route walk)

## Verdict

**INCOMPLETE** — abstract model diverges from targets or lacks coverage.

## Policy results

| Policy | Ending | Insp | Corr | MS | Anxiety | Notes |
|--------|--------|-----:|-----:|---:|--------:|-------|
| corruption_forward | day105_7_release_one_ending | 30 | 10 | 5 | 43 | Prologue baseline: insp=20, corr=2; Wrote ch1; manuscript_progress=1; Wrote ch2; manuscript_progress=2 |
| cautious | game_over_deadline_2 | 40 | 3 | 1 | 9 | Prologue baseline: insp=20, corr=2; Day 101 slop path — no manuscript_progress; Wrote ch1; manuscript_progress=1 |
| passive | game_over_deadline_1 | 30 | 1 | 0 | 5 | Prologue baseline: insp=15, corr=1; Failed ch1_write_gate: insp=30, corr=1; Failed ch1_write_gate: insp=30, corr=1 |
| reckless | game_over_dismissed | 60 | 9 | 3 | 100 | Prologue baseline: insp=15, corr=2; Wrote ch1; manuscript_progress=1; Wrote ch2; manuscript_progress=2 |
| recovery | game_over_deadline_2 | 40 | 3 | 1 | 7 | Prologue baseline: insp=15, corr=2; Day 101 slop path — no manuscript_progress; Wrote ch1; manuscript_progress=1 |
| deadline_skip | game_over_deadline_1 | 30 | 1 | 0 | 0 | Prologue baseline: insp=10, corr=1; Skipped write for ch1 per policy; Skipped write for ch1 per policy |
| ch1_only | game_over_deadline_2 | 40 | 2 | 1 | 7 | Prologue baseline: insp=15, corr=2; Day 101 slop path — no manuscript_progress; Wrote ch1; manuscript_progress=1 |
| anxiety_push | game_over_dismissed | 50 | 6 | 0 | 100 | Prologue baseline: insp=10, corr=1; Anxiety hit 100 on day 101 |
| penance_force | day105_7_release_one_ending | 20 | 8 | 4 | 65 | Prologue baseline: insp=15, corr=2; Wrote ch1; manuscript_progress=1; Wrote ch2; manuscript_progress=2 |

## Matrix assertions

| Run | Assertion | Pass | Actual |
|-----|-----------|------|--------|
| P1_corruption_forward | assert_ending:day105_7_release_one_ending | yes | day105_7_release_one_ending |
| P1_corruption_forward | assert_stat_floor:{'manuscript_progress': 5} | yes | manuscript_progress=5 |
| P2_cautious | assert_reaches_day_at_least:105 | no | 104 |
| P3_low_corruption | assert_ending_one_of:bad_ending_rejection | no | game_over_deadline_1 |
| P4_deadline_1 | assert_ending:game_over_deadline_1 | yes | game_over_deadline_1 |
| P5_deadline_2 | assert_ending:game_over_deadline_2 | yes | game_over_deadline_2 |
| P6_anxiety_collapse | assert_ending:game_over_dismissed | yes | game_over_dismissed |
| P7_penance | assert_event_seen:confrontation | no | INCOMPLETE — requires runtime capture or graph walk |

## Fuzz distribution (100 runs)

| Ending | Count | % |
|--------|------:|--:|
| game_over_deadline_2 | 46 | 46.0 |
| game_over_dismissed | 26 | 26.0 |
| game_over_deadline_1 | 16 | 16.0 |
| day105_7_release_one_ending | 12 | 12.0 |

## Limitations

- Does not walk label-level branches; uses per-day economy budgets from choice catalogue.
- Penance/confrontation assertions require runtime capture (marked INCOMPLETE).
- Anxiety model is simplified from acute suspicion totals.
