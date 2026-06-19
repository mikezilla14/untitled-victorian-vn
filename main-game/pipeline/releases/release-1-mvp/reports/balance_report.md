# Testing and balance report

**Release:** `release-1-mvp`
**Generated:** 2026-06-19 21:31 UTC

## Verdict

**INCOMPLETE**

> Static structure checks only. Route simulation, runtime capture, and
> policy fuzz are not part of this first pass.

## Checked files

- `main-game/non-prod-game/game/days/book1_non_canon.rpy`
- `main-game/non-prod-game/game/days/day101_non_canon.rpy`
- `main-game/non-prod-game/game/days/day102_non_canon.rpy`
- `main-game/non-prod-game/game/days/day103_non_canon.rpy`
- `main-game/non-prod-game/game/days/day104_non_canon.rpy`
- `main-game/non-prod-game/game/days/day105_non_canon.rpy`
- `main-game/non-prod-game/game/shared/endings.rpy`
- `main-game/non-prod-game/game/shared/functions_non_canon.rpy`

## Route/balance assumptions

- Corruption Rank 1 is the starting state; prologue should leave the player able to reach Level 2 before Day 2 book writing.
- Level 2 is required for Day 101/102 Chapter 1 gates (`WRITE_GATE_CH1` corruption floor = 2).
- Level 3 is required for Chapter 2+ gates and is the soft-fail floor at Day 5 reckoning (`WRITE_GATE_CH2` corruption floor = 3).
- Level 4 is the intended optimized-path milestone by end of Day 4 (not yet statically provable without simulation).
- Cautious players may reach Day 2 but write weaker chapters (Day 101 slop path when `corruption_level <= WRITE_SLOP_MAX_CORRUPTION_LEVEL`).
- Passive/low-corruption play should route to `bad_ending_rejection` (respectable-writer soft fail), not a silent hard lock.
- Risky paths may reach MVP ending (`day105_7_release_one_ending`) but can trigger hard fails (`game_over_*`).
- Writing gates use AND semantics: both inspiration and corruption_level must clear (`has_story_fuel`).

## Manuscript gate checks

- ✓ **PASS** — WRITE_GATE_CH1 = (15, 2) (inspiration, corruption_level) (`main-game/non-prod-game/game/shared/functions_non_canon.rpy`)
- ✓ **PASS** — WRITE_GATE_CH2 = (30, 3) (inspiration, corruption_level) (`main-game/non-prod-game/game/shared/functions_non_canon.rpy`)
- ✓ **PASS** — WRITE_GATE_CH3 = (45, 3) (inspiration, corruption_level) (`main-game/non-prod-game/game/shared/functions_non_canon.rpy`)
- ✓ **PASS** — `WRITE_SLOP_MAX_CORRUPTION_LEVEL` present in functions (`main-game/non-prod-game/game/shared/functions_non_canon.rpy`)
- ✓ **PASS** — `ANXIETY_WRITE_PARALYSIS` present in functions (`main-game/non-prod-game/game/shared/functions_non_canon.rpy`)
- ✓ **PASS** — `has_story_fuel` present in functions (`main-game/non-prod-game/game/shared/functions_non_canon.rpy`)
- ✓ **PASS** — `attempt_write` present in functions (`main-game/non-prod-game/game/shared/functions_non_canon.rpy`)
- ✓ **PASS** — Day 101 night write menu uses `has_story_fuel(*WRITE_GATE_CH1)` (`main-game/non-prod-game/game/days/day101_non_canon.rpy`)
- ✓ **PASS** — Day 102 Ch1 catch-up uses `has_story_fuel(*WRITE_GATE_CH1)` (`main-game/non-prod-game/game/days/day102_non_canon.rpy`)
- ✓ **PASS** — Day 102 Ch2 write uses `has_story_fuel(*WRITE_GATE_CH2)` (`main-game/non-prod-game/game/days/day102_non_canon.rpy`)
- ✓ **PASS** — Day 103 Ch3 write uses `has_story_fuel(*WRITE_GATE_CH3)` (`main-game/non-prod-game/game/days/day103_non_canon.rpy`)
- ✓ **PASS** — `label book1_write_chapter` found in book1_non_canon.rpy (`main-game/non-prod-game/game/days/book1_non_canon.rpy`)
- ✓ **PASS** — `call book1_write_chapter` found in day101_non_canon.rpy (`main-game/non-prod-game/game/days/day101_non_canon.rpy`)
- ✓ **PASS** — `call book1_write_chapter` found in day102_non_canon.rpy (`main-game/non-prod-game/game/days/day102_non_canon.rpy`)
- ✓ **PASS** — `call book1_write_chapter` found in day103_non_canon.rpy (`main-game/non-prod-game/game/days/day103_non_canon.rpy`)
- ✓ **PASS** — `call book1_write_chapter` found in day104_non_canon.rpy (`main-game/non-prod-game/game/days/day104_non_canon.rpy`)
- ✓ **PASS** — `call book1_write_chapter` found in day105_non_canon.rpy (`main-game/non-prod-game/game/days/day105_non_canon.rpy`)
- ✓ **PASS** — Manuscript progress hook for `day1_chapter` present (`main-game/non-prod-game/game/days/day101_non_canon.rpy`)
- ✓ **PASS** — Manuscript progress hook for `day2_chapter` present (`main-game/non-prod-game/game/days/day102_non_canon.rpy`)
- ✓ **PASS** — Manuscript progress hook for `day3_chapter` present (`main-game/non-prod-game/game/days/day103_non_canon.rpy`)
- ✓ **PASS** — Manuscript progress hook for `day4_triumphant_chapter` present (`main-game/non-prod-game/game/days/day104_non_canon.rpy`)
- ✓ **PASS** — Manuscript progress hook for `day5_reckoning_chapter` present (`main-game/non-prod-game/game/days/day105_non_canon.rpy`)

## Corruption/inspiration progression checks

- ✓ **PASS** — CH1 gate corruption floor (2) matches Day 2 write readiness intent (`main-game/non-prod-game/game/shared/functions_non_canon.rpy`)
- ✓ **PASS** — CH2/CH3 gate corruption floor (3) matches Level 3 milestone / soft-fail floor (`main-game/non-prod-game/game/shared/functions_non_canon.rpy`)
- … **INCOMPLETE** — Cannot verify optimized path reaches corruption Level 4 by Day 4 without route simulation
- … **INCOMPLETE** — Cannot verify cautious/passive/risky archetype outcomes without policy simulator or playtest matrix

## Fail-state checks

- ✓ **PASS** — Fail label `game_over_dismissed` defined (Anxiety ≥ 100 dismissal) (`endings.rpy`)
- ✓ **PASS** — `game_over_dismissed` referenced from script (`main-game/non-prod-game/game/shared/story_chains_non_canon.rpy`)
- ✓ **PASS** — Fail label `game_over_deadline_1` defined (No Ch1 by Day 3 morning) (`endings.rpy`)
- ✓ **PASS** — `game_over_deadline_1` referenced from script (`main-game/non-prod-game/game/days/day103_non_canon.rpy`)
- ✓ **PASS** — Fail label `game_over_deadline_2` defined (manuscript_progress < 2 by Day 4 close) (`endings.rpy`)
- ✓ **PASS** — `game_over_deadline_2` referenced from script (`main-game/non-prod-game/game/days/day104_non_canon.rpy`)
- ✓ **PASS** — Fail label `bad_ending_rejection` defined (corruption_level < 3 at reckoning) (`endings.rpy`)
- ✓ **PASS** — `bad_ending_rejection` referenced from script (`main-game/non-prod-game/game/days/day105_non_canon.rpy`)
- ✓ **PASS** — `game_over_dismissed` referenced from story chains (`main-game/non-prod-game/game/shared/story_chains_non_canon.rpy`)
- ✓ **PASS** — MVP success label `day105_7_release_one_ending` present (`main-game/non-prod-game/game/days/day105_non_canon.rpy`)

## Soft-fail checks

- ✓ **PASS** — Day 101 slop chapter path present for low-corruption cautious play (`main-game/non-prod-game/game/days/day101_non_canon.rpy`)
- ✓ **PASS** — Day 105 reckoning wires soft fail via `WRITE_GATE_CH2` corruption floor (`main-game/non-prod-game/game/days/day105_non_canon.rpy`)
- … **INCOMPLETE** — Cannot confirm passive players receive clear life-experience feedback before soft fail without playtest

## Deprecated-router checks

- ✓ **PASS** — No new `jump end_slot` or `jump advance_after_confrontation` in scanned files
- ✓ **PASS** — Compatibility label `advance_after_confrontation` retained but not jumped from active work (`main-game/non-prod-game/game/shared/story_chains_non_canon.rpy`)

## Required day files

- ✓ **PASS** — Required sandbox day file present: day101 (`main-game/non-prod-game/game/days/day101_non_canon.rpy`)
- ✓ **PASS** — Required sandbox day file present: day102 (`main-game/non-prod-game/game/days/day102_non_canon.rpy`)
- ✓ **PASS** — Required sandbox day file present: day103 (`main-game/non-prod-game/game/days/day103_non_canon.rpy`)
- ✓ **PASS** — Required sandbox day file present: day104 (`main-game/non-prod-game/game/days/day104_non_canon.rpy`)
- ✓ **PASS** — Required sandbox day file present: day105 (`main-game/non-prod-game/game/days/day105_non_canon.rpy`)

## Missing evidence

- No Python route simulator or choice catalogue yet — cannot prove optimized/cautious/passive paths reach intended stats.
- No runtime JSONL captures — cannot verify gate pass/fail at play time.
- No grain manifest or gate catalogue CSV — normalized condition extraction not wired.
- Corruption Level 4 milestone by Day 4 end is design intent only until simulation exists.

## Recommended next tests

- Run P1 corruption-forward and P2 cautious playthroughs; save JSONL when capture harness lands.
- Build `choice_catalogue.csv` / `gate_catalogue.csv` and deterministic policy simulator (Phase 2/5 of spec).
- Add grain manifest builder to cross-check DAG tags against write/deadline gates.
- Smoke-test hard fails: skip all writing → `game_over_deadline_1`; Ch1 only → `game_over_deadline_2`; anxiety 100 → `game_over_dismissed`.
- Verify cautious Day 101 slop path still advances spine without bricking deadline gates.
