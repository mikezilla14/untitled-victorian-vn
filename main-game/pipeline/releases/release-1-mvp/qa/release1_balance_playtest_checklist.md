# Release 1 balance playtest checklist

Use this to finish **P2–P7** runtime captures and close the end-to-end balancing loop.

**Already done:** P1 (`P1_corruption_forward.jsonl`) — PASS, MS 5, MVP ending.

**Record results in:** [`release1_route_matrix_results.md`](release1_route_matrix_results.md)

---

## Before you start (once per session)

- [ ] Open Ren'Py launcher → project **`main-game/non-prod-game/`**
- [ ] Start game → press **F10** (balance debug overlay)
- [ ] Confirm overlay shows label / stats; **do not** use debug stat cheats
- [ ] Optional: delete old capture if re-running same ID  
  `main-game/non-prod-game/debug_captures/<run_id>.jsonl`

### Start any matrix run

```renpy
$ _capture_run_id = "P4_deadline_1"
jump debug_capture_start
```

Or use overlay **P1** button only for P1; for P2–P7 set `_capture_run_id` in console first.

### After each run

```powershell
py main-game/pipeline/tools/compare_runtime_to_model.py --release release-1-mvp --capture <run_id>
```

- [ ] JSONL exists under `main-game/non-prod-game/debug_captures/`
- [ ] Comparison report shows **Structure PASS**
- [ ] Assertions **PASS** (or note intentional design exception)
- [ ] Update row in `release1_route_matrix_results.md`
- [ ] Overlay **Stop** (or `jump debug_capture_stop`) so `run_end` is logged

**Rules:** forward-only play preferred; rollbacks are OK (marked in report). One official attempt per run ID unless redoing a bad capture.

---

## Recommended order

Fail paths first (quick, validates deadlines), then sim-gap routes, then P7 last.

| Order | Run | Why |
|-------|-----|-----|
| 1 | P4 | Short; abstract sim already PASS |
| 2 | P5 | Short fail path |
| 3 | P6 | Short fail path |
| 4 | P2 | Long; sim says may stop day 104 — validate cautious MVP/weak path |
| 5 | P3 | Long; sim says soft-fail intent — validate `bad_ending_rejection` |
| 6 | P7 | May need **multiple captures** (Stern / Missy / Vance confrontations) |

---

## P4 — deadline fail 1

| | |
|---|---|
| **Run ID** | `P4_deadline_1` |
| **Intent** | Skip **all** manuscript writing through Day 2 |
| **Expected** | `game_over_deadline_1` (no Ch1 by Day 3 morning) |

### Play hints

- [ ] Take non-write night options every day (chains, reflect, indulge, barricade, etc.)
- [ ] Never choose “Write…” / manuscript progress menus
- [ ] Do **not** need to reach Day 105

### Pass criteria

- [ ] Ending label `game_over_deadline_1` in JSONL
- [ ] `manuscript_progress` stays **0** at ending snapshot
- [ ] Matrix row → **PASS**

---

## P5 — deadline fail 2

| | |
|---|---|
| **Run ID** | `P5_deadline_2` |
| **Intent** | Complete **Ch1 only**, then stop writing |
| **Expected** | `game_over_deadline_2` (draft incomplete by Day 4 close) |

### Play hints

- [ ] Write Ch1 on Day 101 **or** Day 102 catch-up only
- [ ] After Ch1 (`manuscript_progress` ≥ 1), avoid further completed chapters
- [ ] Still play story days normally; reach Day 4 ending gate

### Pass criteria

- [ ] Ending `game_over_deadline_2`
- [ ] Final MS **1** (only `day1_chapter` in ladder — no day2+ book1 blocks)
- [ ] Matrix row → **PASS**

---

## P6 — anxiety collapse

| | |
|---|---|
| **Run ID** | `P6_anxiety_collapse` |
| **Intent** | Maximize exposure / suspicion / anxiety |
| **Expected** | `game_over_dismissed` (anxiety hits cap) |

### Play hints

- [ ] Prefer high-suspicion, high-anxiety choices (defiant, complicit, risky corridor/tea paths)
- [ ] Defer or skip writing when it lowers pressure
- [ ] Accept penance/confrontation heat if it spikes anxiety

### Pass criteria

- [ ] Ending `game_over_dismissed`
- [ ] High anxiety in final snapshot (near **100**)
- [ ] Matrix row → **PASS**

---

## P2 — cautious

| | |
|---|---|
| **Run ID** | `P2_cautious` |
| **Intent** | Low-risk / inspiration-first; write when gates allow |
| **Expected** | Reach **Day 105** (weak completion or recoverable MVP path OK) |

### Play hints

- [ ] Prefer safe / inspiration choices; spread suspicion; avoid reckless corruption spikes
- [ ] Write at gates when fuel allows — **Ch2 on Day 102 night is mandatory** before Ch3
- [ ] Ch1 may be deferred to Day 102 (same as P1); ensure **day2 book1 block** appears before day3
- [ ] Accept weaker manuscript quality feedback if offered

### Pass criteria

- [ ] Reaches day **105** (`assert_reaches_day_at_least: 105`) — MVP ending **or** weak but complete path
- [ ] Note final MS, corruption level, and whether feedback felt clear for cautious players
- [ ] Compare to abstract sim (expected gap: sim stopped day 104)
- [ ] Matrix row → **PASS** or **FAIL** with notes for tuning

---

## P3 — passive / low corruption

| | |
|---|---|
| **Run ID** | `P3_low_corruption` |
| **Intent** | Avoid corruption; minimal risky writing |
| **Expected** | `bad_ending_rejection` (soft fail / respectable writer) |

### Play hints

- [ ] Prefer low-corruption, “safe” choices; skip corruption-forward options
- [ ] You may write cautiously, but keep corruption low through Day 5 reckoning
- [ ] Do **not** grind corruption for gates if avoidable

### Pass criteria

- [ ] Ending `bad_ending_rejection`
- [ ] Feedback points to life-experience / quality cause (subjective — note in matrix)
- [ ] Matrix row → **PASS**

---

## P7 — penance / confrontations

| | |
|---|---|
| **Run ID** | `P7_penance` |
| **Intent** | Force confrontation windows across the spine |
| **Expected** | At least one `confrontation_*` label or confrontation `flag` event |

### Play hints

- [ ] Push suspicion on **Stern**, **Missy**, and **Vance** across separate runs if needed
- [ ] Accept penance when queued; use story-chain windows
- [ ] Labels to watch: `confrontation_stern`, `confrontation_missy`, `confrontation_vance`
- [ ] One capture may not hit all three — document partial coverage honestly

### Pass criteria (per capture)

- [ ] JSONL contains confrontation evidence (`assert_event_seen: confrontation`)
- [ ] Matrix row → **PASS** / **PARTIAL** (note which character)

Optional extra captures (same checklist, new JSONL suffix or overwrite with notes):

- [ ] `P7_penance` — Stern-focused run
- [ ] `P7_penance_stern` / manual note — if you split files locally
- [ ] Missy-focused run
- [ ] Vance-focused run

---

## End-of-session framework commands

Run from repo root after captures:

```powershell
# Compare all captures vs balance_targets.yaml
py main-game/pipeline/tools/compare_runtime_to_model.py --release release-1-mvp

# Static + artefact cross-check (grain, catalogues, sim, harness)
py scripts/balance_report.py --release release-1-mvp

# Abstract policy matrix (sanity-check vs runtime)
py main-game/pipeline/tools/simulate_balance.py --release release-1-mvp

# Optional deep fuzz (slow)
py main-game/pipeline/tools/simulate_balance.py --release release-1-mvp --deep
```

### Review outputs

- [ ] `main-game/pipeline/releases/release-1-mvp/qa/runtime_model_comparison.md`
- [ ] `main-game/pipeline/releases/release-1-mvp/qa/release1_route_matrix_results.md` — **7/7 rows filled**
- [ ] `main-game/pipeline/releases/release-1-mvp/reports/balance_report.md`
- [ ] `main-game/pipeline/releases/release-1-mvp/balance/simulation_report.md`

---

## Sign-off (MVP balance framework)

From [`testing_balance_framework_spec.md`](../../../../draft/releases/planning/testing_balance_framework_spec.md) — tick when true:

- [ ] **P1–P7** runtime JSONL captures exist (P7 confrontation at least once)
- [ ] No unknown runtime endings in any capture
- [ ] Runtime vs `balance_targets.yaml` assertions documented (PASS/FAIL/exceptions)
- [ ] P2/P3/P7 sim-vs-runtime deltas noted in matrix Notes column
- [ ] No **blocker** mismatches (crashes, soft locks, impossible P1, missing fail labels)
- [ ] Ch2-before-Ch3 manuscript rule verified on any run that writes past Day 102

---

## Quick reference — run IDs

| ID | JSONL filename |
|----|----------------|
| P1 | `P1_corruption_forward.jsonl` ✓ |
| P2 | `P2_cautious.jsonl` |
| P3 | `P3_low_corruption.jsonl` |
| P4 | `P4_deadline_1.jsonl` |
| P5 | `P5_deadline_2.jsonl` |
| P6 | `P6_anxiety_collapse.jsonl` |
| P7 | `P7_penance.jsonl` |

---

## If something fails

1. Keep the JSONL — failed captures are useful.
2. Note **expected vs actual** ending in the matrix.
3. Do **not** fix prose in the same session unless it is a clear blocker; log as tuning follow-up.
4. Re-run only the failed run ID after a fix.

Good night — start with **P4** when you’re back.
