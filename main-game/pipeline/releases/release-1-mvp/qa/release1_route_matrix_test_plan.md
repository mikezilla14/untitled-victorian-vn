# Release 1 Route Matrix — Detailed Test Plan

**Release:** `release-1-mvp`  
**Engine:** `main-game/non-prod-game/` (capture sandbox)  
**Assertion source:** `main-game/draft/releases/planning/balance/balance_targets.yaml`  
**Quick checklist:** [`release1_balance_playtest_checklist.md`](release1_balance_playtest_checklist.md)  
**Results log:** [`release1_route_matrix_results.md`](release1_route_matrix_results.md)  
**Machine compare:** `py main-game/pipeline/tools/compare_runtime_to_model.py --release release-1-mvp`

---

## 1. Purpose

This document defines **what each matrix run must exercise** in the playable story: choice posture, writing behaviour, expected endings, stat floors, and evidence to record. It is the human test specification; the checklist is the tick-box companion.

The matrix proves:

1. The **MVP spine** completes under a corruption-forward policy (P1).
2. A **cautious** player can still reach Day 105 (P2).
3. **Soft fail** and **hard fail** endings fire on schedule (P3–P6).
4. **Penance / confrontation** machinery surfaces at runtime (P7).

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Project | Ren'Py launcher → `main-game/non-prod-game/` |
| Overlay | **F10** balance capture overlay visible |
| Cheats | **Do not** use debug stat cheats |
| Rollback | Forward-only preferred; rollbacks allowed but mark capture if used |
| Saves | Save/load smoke is **out of scope** per run (separate smoke pass) |
| Prologue | All runs start at `label start` → Day 100 prologue → Savoy arc |
| Writing rule | **Ch2 before Ch3:** any run that writes past Day 102 night must complete `day2_chapter` before Day 103 morning deadline gate |

### Start a capture

**Overlay:** press **P1**–**P7** (restarts from `label start` with run id preset).

**Console:**

```renpy
$ _capture_run_id = "P5_deadline_2"
jump debug_capture_start
```

### End a capture

- Reach the expected ending (or fail label).
- Overlay **Stop** or `jump debug_capture_stop` so `run_end` is logged.
- Verify JSONL: `main-game/non-prod-game/debug_captures/<run_id>.jsonl`

### Validate

```powershell
py main-game/pipeline/tools/compare_runtime_to_model.py --release release-1-mvp --capture <run_id>
```

Update [`release1_route_matrix_results.md`](release1_route_matrix_results.md).

---

## 3. Day and numbering reference

| File id | `TimeManager.current_day` | Story slot |
|---------|---------------------------|------------|
| day100 | (prologue) | Wiltshire prequel |
| day101 | 1 | Savoy Day 1 |
| day102 | 2 | Savoy Day 2 |
| day103 | 3 | Savoy Day 3 |
| day104 | 4 | Savoy Day 4 |
| day105 | 5 | Savoy Day 5 |

Capture assertions may use file id **105**; runtime snapshots store slot **5**. The compare tool normalizes slot → file id.

---

## 4. Matrix runs (detailed)

### P1 — `P1_corruption_forward` ✓ recorded

| Field | Value |
|-------|--------|
| **Policy** | `corruption_forward` |
| **Length** | Long (~45–90 min) |
| **Intent** | Stress-test the **happy path**: high corruption, manuscript ladder complete, MVP ending |

#### What this run must cover

- **Prologue (day100):** transgressive / scandal-hungry posture; archetype seed toward predator or corruption-forward tone.
- **Day 101:** predator or corruption-leaning corridor path; complete **Chapter 1** (or defer to 102 catch-up per design); visit Missy or write at night.
- **Day 102:** contraband **stolen_wearing** or **planted**; corruption chore focus; **predator** or high-corruption tea path; **write Ch2 same night** (mandatory before day103).
- **Day 103:** brush test; Gideon tea; write Ch3 if gates allow; survive Stern suspicion beat.
- **Day 104:** lockbox / escape branch; retain photograph if possible; **triumphant chapter** write (Ch4).
- **Day 105:** full reckoning; Gideon marks Cora; **`day105_7_release_one_ending`**.

#### Choice posture (summary)

| Day | Lean toward |
|-----|-------------|
| 100 | Scandal-hungry / predator seed |
| 101 | Predator corridor; corruption ledger; write or visit Missy |
| 102 | Take contraband; corruption chore; predator tea; **write at night** |
| 103 | Corruption corridor chain; exposure brush; frantic write if needed |
| 104 | Bold escape; keep evidence; finish manuscript |
| 105 | Predator/muse dynamic; complete reckoning chapter |

#### Do not

- Skip all writing (that is P4).
- Play purely ghost/safe (that is P2/P3).

#### Pass criteria (automated)

| Assertion | Expected |
|-----------|----------|
| `assert_ending` | `day105_7_release_one_ending` |
| `assert_stat_floor` | `manuscript_progress` ≥ **5** |

#### Record manually

- Final corruption level, inspiration, anxiety.
- Whether Book1 tableau/plate CGs appeared on Ch1/Ch2 writes.
- Any penance labels consumed (informational).

---

### P2 — `P2_cautious` ✓ recorded

| Field | Value |
|-------|--------|
| **Policy** | `cautious` |
| **Length** | Long |
| **Intent** | Low-risk player still reaches **Day 105**; weaker manuscript quality acceptable |

#### What this run must cover

- Inspiration-first and ghost/prey choices where safe.
- Write when `has_story_fuel` allows — **do not** skip Ch2 before Day 103.
- Spread suspicion; avoid reckless corruption spikes.
- Accept weaker slop chapter or quality feedback if corruption stays low.

#### Choice posture (summary)

| Day | Lean toward |
|-----|-------------|
| 101 | Prey/ghost corridor; meek interview; inspiration ledger |
| 102 | Deceive Missy or planted contraband; inspiration chore; prey/ghost tea |
| 103 | Inspiration corridor chain; craftsman brush answer |
| 104 | Fireplace or cautious escape; atonement twilight if offered |
| 105 | Witness/ghost motivation; complete ending spine |

#### Do not

- Max corruption for gate fuel unless required to pass a write gate.
- Skip Ch2 night write before Day 103.

#### Pass criteria (automated)

| Assertion | Expected |
|-----------|----------|
| `assert_reaches_day_at_least` | **105** (runtime slot **5** normalized) |

#### Record manually

- Final MS count (may be &lt; 5).
- Whether ending was “weak” vs corruption-forward.
- Abstract sim note: sim may stop day **104** — runtime may still reach 105.

---

### P3 — `P3_low_corruption` — pending

| Field | Value |
|-------|--------|
| **Policy** | `passive` |
| **Length** | Long |
| **Intent** | Player avoids corruption; manuscript quality fails publisher bar |

#### What this run must cover

- Consistently **low corruption** choices (safe, inspiration, ghost, meek).
- Minimal transgressive writing; slop chapter path on Day 101 if corruption ≤ 2.
- Reach Day 105 reckoning with **insufficient corruption / life-experience** subtext.
- Trigger **`bad_ending_rejection`** (respectable-writer soft fail).

#### Choice posture (summary)

| Day | Lean toward |
|-----|-------------|
| 100–105 | Avoid corruption menus; prefer inspiration/safe options |
| 101 | Ghost/prey; write slop or thin Ch1 |
| 102–104 | Write only when mandatory for spine progress; avoid indulge |
| 105 | Low-corruption motivation branches |

#### Do not

- Grind corruption for write gates.
- Use predator-forward paths.

#### Pass criteria (automated)

| Assertion | Expected |
|-----------|----------|
| `assert_ending_one_of` | `bad_ending_rejection` |

#### Record manually

- Rejection feedback text (quality vs corruption).
- Final corruption level (expect low).

---

### P4 — `P4_deadline_1` ✓ recorded

| Field | Value |
|-------|--------|
| **Policy** | `deadline_skip` |
| **Length** | Short (~15–25 min) |
| **Intent** | **No manuscript** by Day 3 morning |

#### What this run must cover

- Day 100–102: always choose **non-write** nights (visit Missy, indulge, reflect, chains only).
- Never complete `day1_chapter` or book1 write blocks.
- Advance time to **Day 103 morning** with `manuscript_progress == 0`.

#### Choice posture

- Any time a menu offers **Write…** / manuscript progress → choose the alternative.
- Chains and story content otherwise OK.

#### Pass criteria (automated)

| Assertion | Expected |
|-----------|----------|
| `assert_ending` | `game_over_deadline_1` |

#### Record manually

- Confirm MS **0** in final snapshot.

---

### P5 — `P5_deadline_2` — pending

| Field | Value |
|-------|--------|
| **Policy** | `ch1_only` |
| **Length** | Medium (~25–40 min) |
| **Intent** | **Ch1 only**, then stop writing; fail by Day 4 deadline |

#### What this run must cover

- Write **Chapter 1 only** on Day 101 night **or** Day 102 catch-up.
- After `manuscript_progress` ≥ 1, **no** further completed chapters (`day2_chapter`, etc.).
- Play story days through Day 4 close; hit **`game_over_deadline_2`**.

#### Choice posture

| Phase | Behaviour |
|-------|-----------|
| Day 101–102 | Write Ch1 once |
| Day 102+ | Non-write nights; avoid book1 completion menus |
| Day 103–104 | Story choices OK; do not finish Ch2–Ch4 |

#### Do not

- Complete Ch2 on Day 102 night (would invalidate deadline-2).

#### Pass criteria (automated)

| Assertion | Expected |
|-----------|----------|
| `assert_ending` | `game_over_deadline_2` |

#### Record manually

- Final MS **1** only (`day1_chapter` in ladder).

---

### P6 — `P6_anxiety_collapse` — pending

| Field | Value |
|-------|--------|
| **Policy** | `anxiety_push` |
| **Length** | Medium–long |
| **Intent** | Anxiety reaches cap → dismissal |

#### What this run must cover

- High **acute suspicion** on multiple characters.
- Defiant / visible / complicit choices.
- Defer writing when it reduces pressure (optional).
- Accept penance and confrontation heat.
- End at **`game_over_dismissed`** (anxiety ≥ 100).

#### Choice posture

| Day | Lean toward |
|-----|-------------|
| 101 | Prey corridor (high vance susp) or predator visibility |
| 102 | Stolen wearing + vance crisis; confess or frame |
| 103 | Ghost brush retreat; Stern suspicion peak |
| 104 | Bold lie escape; Stern pressure |

#### Pass criteria (automated)

| Assertion | Expected |
|-----------|----------|
| `assert_ending` | `game_over_dismissed` |

#### Record manually

- Final anxiety (expect ~100).
- Which character drove the last suspicion spike.

---

### P7 — `P7_penance` — pending

| Field | Value |
|-------|--------|
| **Policy** | `penance_force` |
| **Length** | Medium per character; may need **multiple captures** |
| **Intent** | Prove confrontation / penance labels execute |

#### What this run must cover

- Push **one** tracked character (Stern, Missy, or Vance) to confrontation threshold (**50** total suspicion).
- Pass through a **consequence window** that calls `consume_pending_penance`.
- Execute a `confrontation_*` label.

#### Per-character hints

| Character | How to spike |
|-----------|----------------|
| **Stern** | Meek interview fail; contraband; confession; missed standards |
| **Missy** | Frame Missy; trust break; use as cover |
| **Vance** | Predator corridor; stolen wearing; visible lies |

#### Pass criteria (automated)

| Assertion | Expected |
|-----------|----------|
| `assert_event_seen` | `confrontation` (flag or `confrontation_*` label in JSONL) |

#### Partial coverage

One capture may only prove **one** character. Mark matrix row **PARTIAL** and note which character fired.

Optional extra local files: `P7_penance_stern.jsonl` etc. (document in matrix Notes; compare tool uses single `P7_penance` id by default).

---

## 5. Recommended execution order

| Order | Run | Rationale |
|-------|-----|-----------|
| 1 | P4 | Short fail; validates deadline-1 wiring |
| 2 | P5 | Short fail; validates Ch1-only deadline |
| 3 | P6 | Medium fail; anxiety wiring |
| 4 | P3 | Long; soft fail ending |
| 5 | P7 | May require rerolls per character |
| — | P1, P2 | Already recorded; re-run only if story changes |

---

## 6. JSONL structure expectations

Each valid capture should contain:

| Event | Required |
|-------|----------|
| `run_start` | yes |
| `grain_enter` | yes (labels through spine) |
| `choice` / `gate` | at least one |
| `ending` or terminal label | yes |
| `run_end` | yes |

**Balance proof invalid if:** `rollback_event` present (unless `--allow-rollback`).

---

## 7. Sign-off gate (Release 1 balance framework)

From [`testing_balance_framework_spec.md`](../../../../draft/releases/planning/testing_balance_framework_spec.md):

- [ ] **P1–P7** JSONL captures exist (P7 at least once).
- [ ] `runtime_model_comparison.md` — no blocker assertion failures.
- [ ] `release1_route_matrix_results.md` — all rows filled PASS/PARTIAL with notes.
- [ ] Ch2-before-Ch3 verified on any write-past-102 run.
- [ ] No crashes, soft locks, or missing fail labels on recorded paths.

---

## 8. Failure handling

1. **Keep** failed JSONL files.
2. Log **expected vs actual** ending in the matrix.
3. File prose bugs separately from balance tuning.
4. Re-run **only** the affected run id after a fix.

---

## 9. Quick reference

| Run ID | JSONL | Primary ending / signal |
|--------|-------|-------------------------|
| P1 | `P1_corruption_forward.jsonl` | `day105_7_release_one_ending` |
| P2 | `P2_cautious.jsonl` | reach day 105 |
| P3 | `P3_low_corruption.jsonl` | `bad_ending_rejection` |
| P4 | `P4_deadline_1.jsonl` | `game_over_deadline_1` |
| P5 | `P5_deadline_2.jsonl` | `game_over_deadline_2` |
| P6 | `P6_anxiety_collapse.jsonl` | `game_over_dismissed` |
| P7 | `P7_penance.jsonl` | confrontation event |
