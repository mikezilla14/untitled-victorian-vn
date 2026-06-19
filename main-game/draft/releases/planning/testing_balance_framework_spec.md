# Testing and Balance Framework Spec

> **Owner:** Technical / systems
> **Target tree:** `main-game/non-prod-game/`
> **Support tooling:** `main-game/pipeline/tools/`, `main-game/pipeline/releases/release-1-mvp/graph/`
> **Design references:** `story_board.md`, `continuity_handoff.md`, `mvp_systems_integration_checklist.md`, Release 1 graph artifacts
> **Purpose:** Turn Release 1 MVP testing and economy balance from manual route guessing into a repeatable agentic workflow using static grain extraction, Ren'Py runtime capture, Python simulation, and human review.

---

## 1. Executive summary

This framework exists to answer four questions with evidence:

1. **Can the spine complete?**
   - A player can move from `label start` through Day 100 to Day 105 without debug harnesses.

2. **Can intended fail states fire cleanly?**
   - Deadline fails, rejection, anxiety dismissal, and penance/confrontation routes are reachable and non-crashing.

3. **Does the economy support the intended player archetypes?**
   - Corruption-forward, cautious, passive, reckless, recovery, deadline-fail, and anxiety-fail routes produce distinct, intended outcomes.

4. **Does the implemented Ren'Py route match the static model?**
   - Static grain/DAG model, Python balance simulator, and runtime capture should broadly agree. Mismatches become implementation or model defects.

The framework must not become a second storyboard. It must remain a practical test and balance layer.

---

## 2. Non-goals

Do **not** build:

- A full Ren'Py interpreter in Python.
- A prose analysis engine.
- A complete combinatorial route explorer for every possible line-level branch.
- A replacement for human playtesting.
- A new gameplay system.
- A second source of truth for narrative structure.

The framework tests and balances the existing release structure. It does not design the game for the writer.

---

## 3. Core concept: grain-based testing

A **grain** is the smallest useful test/balance unit.

A grain is not every line of script. A grain is a block with:

- one entry point,
- one balancing or routing purpose,
- one expected outcome or handoff,
- measurable start/end state.

Examples:

- Day/time-period start
- menu choice group
- writing gate
- deadline gate
- consequence window
- optional chain window
- penance/confrontation gate
- ending/reckoning label
- Book 1 chapter write event

### 3.1 Grain hierarchy

Use three levels:

| Level | Name | Example | Purpose |
|---|---|---|---|
| L1 | Time period grain | `day103/night` | spreadsheet overview |
| L2 | Label grain | `day103_3_bedroom_final_write` | runtime location |
| L3 | Balance grain | `day103_ch3_write_gate` | test/balance proof |

The debug overlay and runtime capture should display all three when possible.

---

## 4. Metadata contract

Use a hybrid approach:

1. infer obvious structure from Ren'Py syntax;
2. use DAG tags for choices and gates;
3. add one explicit `DAG_GRAIN` tag only where a spreadsheet/runtime capture boundary matters.

### 4.1 `DAG_GRAIN`

Add `DAG_GRAIN` beside balance-critical labels or blocks.

```renpy
# DAG_GRAIN id=day103_ch3_write_gate type=write_gate day=103 period=night capture=start_end_stats
label day103_3_bedroom_final_write:
```

Required fields:

| Field | Required | Notes |
|---|---:|---|
| `id` | yes | stable ID used by manifest, overlay, runtime capture, simulator |
| `type` | yes | `spine`, `choice`, `write_gate`, `deadline_gate`, `consequence_window`, `optional_chain`, `penance`, `ending`, `book1` |
| `day` | recommended | use 100-105 for Release 1 |
| `period` | recommended | `prologue`, `morning`, `afternoon`, `evening`, `night`, `manuscript`, `ending` |
| `capture` | optional | `start_stats`, `start_end_stats`, `gate_result`, `choice_path` |

### 4.2 `DAG_CHOICE`

Use for player-facing route axes and menu groups.

```renpy
# DAG_CHOICE id=day3_ultimatum axis=day3_ultimatum values=defied,bargained,surrendered grain=day103_gideon_ultimatum
menu:
```

Required/expected fields:

| Field | Required | Notes |
|---|---:|---|
| `id` | yes | choice group ID |
| `axis` | yes | story-state axis affected |
| `values` | recommended | valid branch values |
| `grain` | recommended | parent grain ID |

### 4.3 `DAG_GATE`

Use for balancing-relevant `if` conditions.

```renpy
# DAG_GATE id=ch2_write_gate grain=day102_night_write_slot type=write_gate requires="insp>=30,corr>=3"
if has_story_fuel(*WRITE_GATE_CH2):
```

Required/expected fields:

| Field | Required | Notes |
|---|---:|---|
| `id` | yes | stable gate ID |
| `grain` | recommended | parent grain ID |
| `type` | yes | `write_gate`, `deadline_gate`, `anxiety_gate`, `chain_gate`, `ending_gate` |
| `requires` | recommended | human-readable requirement |

---

## 5. Source of truth boundaries

| Layer | Source of truth | Notes |
|---|---|---|
| Narrative design | `story_board.md`, day scripts | What should happen dramatically |
| Structural graph | generated graph manifest | What static extraction sees |
| Runtime truth | Ren'Py capture logs | What actually happened in play |
| Balance intent | spreadsheet/CSV archetype definitions | What outcomes are desired |
| Balance proof | Python simulator report | Whether the numbers support the intent |
| Feel/pacing | human playtest notes | Whether it feels fair, hot, tense, readable |

No single layer is enough by itself.

---

## 6. Phased implementation plan

## Phase 0 — Freeze scope and protect routing

**Goal:** Prevent balance/testing work from moving underfoot.

### Tasks

- [ ] Freeze label names for Day 100-105 spine labels.
- [ ] Freeze menu branch counts and jump/call targets unless a test defect requires change.
- [ ] Freeze state mutation APIs:
  - `apply_effects(...)`
  - `story.set_*`
  - `complete_manuscript_chapter(...)`
  - chain/confrontation helpers
- [ ] Confirm non-prod target remains `main-game/non-prod-game/`.
- [ ] Confirm test harnesses remain excluded from official route captures.

### Acceptance

- A partner prose rewrite can change wording inside labels, but cannot change branch structure without explicit technical review.

---

## Phase 1 — Grain tagging and static extraction

**Goal:** Produce a grain manifest that identifies testable segments.

### New/updated files

- `main-game/pipeline/tools/build_grain_manifest.py`
- `main-game/pipeline/releases/release-1-mvp/grain/release1_grain_manifest.json`
- `main-game/pipeline/releases/release-1-mvp/grain/release1_grains.csv`
- `main-game/pipeline/releases/release-1-mvp/grain/release1_grain_gaps.md`

### Extraction inputs

Scan:

- `main-game/non-prod-game/game/days/*.rpy`
- `main-game/non-prod-game/game/shared/*.rpy`

### Inference rules

Infer grain candidates from:

| Syntax/pattern | Grain candidate |
|---|---|
| `label day103_morning:` | label/time-period grain |
| `menu:` | choice grain |
| `if has_story_fuel`, `WRITE_GATE`, `attempt_write` | write gate |
| `manuscript_progress == 0`, `< 2` | deadline gate |
| `book1_write_chapter` | Book 1 grain |
| `complete_manuscript_chapter` | manuscript progress mutation |
| `watch_suspicion` | consequence window |
| `story_window_penance_gate` | optional chain/penance gate |
| `consume_pending_penance` | penance consumption |
| `jump game_over_*`, `jump bad_ending_*` | fail/ending grain |

### Tag override rules

- `DAG_GRAIN` overrides inferred grain type/day/period.
- `DAG_CHOICE` attaches menu to route axis.
- `DAG_GATE` attaches condition to gate metadata.

### Gap report rules

Flag:

- untagged menus affecting route state;
- untagged balancing-relevant gates;
- duplicate grain IDs;
- grain IDs missing from runtime instrumentation;
- dynamic call sites without declared possible outcomes;
- labels with multiple write/deadline gates but no sub-grain tags.

### Acceptance

- Manifest generated without duplicate IDs.
- All write gates, deadline gates, consequence windows, optional chain windows, and ending gates have stable grain IDs.
- Gap report separates blockers from warnings.

---

## Phase 2 — Debug overlay and runtime capture

**Goal:** Ren'Py records real playtest paths automatically.

### New/updated files

- `main-game/non-prod-game/game/shared/debug_grain_overlay.rpy`
- `main-game/non-prod-game/game/shared/debug_run_capture.rpy`
- output directory: `main-game/non-prod-game/debug_captures/`

### Runtime events

Log these event types:

| Event | Required data |
|---|---|
| `run_start` | run ID, timestamp |
| `grain_enter` | grain ID, label, day, period, grain type, start stats |
| `choice` | choice group, choice made, current grain |
| `gate` | gate ID, pass/fail, requirements, actual stats |
| `flag` | flag/state mutation where useful |
| `grain_exit` | result, next label, end stats |
| `ending` | ending ID, final stats |
| `run_end` | completion note |

### Captured state snapshot

Every event should include:

```json
{
  "stats": {
    "inspiration": 0,
    "inspiration_cap": 50,
    "corruption_level": 1,
    "corruption_xp": 0,
    "anxiety": 0,
    "manuscript_progress": 0
  },
  "suspicion": {
    "stern": 0,
    "missy": 0,
    "vance": 0,
    "gideon": 0
  }
}
```

Add route flags where useful:

- `day1_corridor_state`
- `day1_ledger_focus`
- `day2_contraband_state`
- `day2_tea_choice`
- `day3_brush_choice`
- `day3_ultimatum`
- `day4_escape_state`
- `day5_dynamic`
- `day5_money_choice`
- chain levels
- pending penance window/character if applicable

### Output format

Use JSONL:

```text
main-game/non-prod-game/debug_captures/P1_corruption_forward.jsonl
```

One event per line.

### Rollback policy

Official capture runs are forward-only.

Rules:

- do not use rollback during official capture;
- do not skip backward;
- start each test path from a fresh run ID;
- if rollback is used, discard the capture file and rerun.

### Acceptance

- A P1 test run creates a JSONL file.
- File contains `run_start`, multiple `grain_enter`, at least one `choice`, at least one `gate`, and either `ending` or `run_end`.
- Debug overlay can be toggled without affecting route logic.
- Capture tooling is clearly non-prod and excluded from public build profile.

---

## Phase 3 — Route test matrix execution

**Goal:** Prove the spine and fail states at runtime before deep balancing.

### Required run IDs

| Run ID | Route type | Expected result |
|---|---|---|
| `P1_corruption_forward` | risk/corruption-forward | reaches Day 105 MVP ending |
| `P2_cautious` | low-risk/inspiration/safety | reaches weak completion or recoverable warning path |
| `P3_low_corruption` | avoids corruption | rejection/soft fail or explicitly designed replacement |
| `P4_deadline_1` | skips all Ch1 paths | `game_over_deadline_1` |
| `P5_deadline_2` | completes Ch1 only | `game_over_deadline_2` |
| `P6_anxiety_collapse` | maximizes exposure/suspicion | `game_over_dismissed` |
| `P7_penance` | forces confrontations | Stern/Missy/Vance confrontation paths across runs |

### Runtime capture checklist

For each run:

- [ ] starts from `label start`;
- [ ] no test harness;
- [ ] no debug stat cheats;
- [ ] no rollback;
- [ ] JSONL capture saved;
- [ ] ending/result matches expected route intent;
- [ ] save/load smoke-tested separately for day boundary and Book 1 screen.

### Acceptance

- At least P1, P2, and one fail path complete before balance tuning begins.
- All seven required paths complete before Release 1 promotion.

---

## Phase 4 — Balance model inputs

**Goal:** Create machine-readable economy data for Python simulation.

### New files

- `main-game/draft/releases/planning/balance/choice_catalogue.csv`
- `main-game/draft/releases/planning/balance/gate_catalogue.csv`
- `main-game/draft/releases/planning/balance/run_policies.csv`
- `main-game/draft/releases/planning/balance/balance_targets.yaml`

### `choice_catalogue.csv`

Columns:

```csv
grain_id,choice_group,choice_id,next_grain,insp_delta,corr_xp_delta,corr_level_delta,anxiety_delta,stern_susp_delta,missy_susp_delta,vance_susp_delta,gideon_susp_delta,manuscript_delta,sets_flag,risk_tier,design_note
```

Notes:

- Keep this as the designer-editable control panel.
- Do not include prose.
- Do not include sprite/background data.

### `gate_catalogue.csv`

Columns:

```csv
gate_id,grain_id,gate_type,required_insp,required_corr_level,required_manuscript_progress,required_anxiety_max,required_anxiety_min,on_pass,on_fail,design_note
```

### `run_policies.csv`

Columns:

```csv
policy_id,description,choice_rule,write_rule,risk_rule,expected_result
```

Example policies:

| Policy | Rule |
|---|---|
| `corruption_forward` | maximize corruption while writing when possible |
| `cautious` | minimize suspicion/anxiety, prefer inspiration |
| `passive` | minimize corruption and avoid risky writes |
| `reckless` | maximize corruption regardless of suspicion |
| `recovery` | cautious Day 1-2, risky Day 3 |
| `deadline_skip` | skip writing |
| `anxiety_push` | maximize suspicion/anxiety |

### `balance_targets.yaml`

Example:

```yaml
release: release-1-mvp
must_pass:
  - policy: corruption_forward
    reaches: day105_7_release_one_ending
  - policy: cautious
    reaches_day_at_least: 105
  - policy: passive
    reaches_one_of:
      - bad_ending_rejection
      - respectable_writer_soft_fail
  - policy: deadline_skip
    reaches: game_over_deadline_1
  - policy: anxiety_push
    reaches: game_over_dismissed
thresholds:
  ch1_gate:
    intended_pass:
      - corruption_forward
    intended_maybe_fail:
      - cautious
      - passive
  ch2_gate:
    intended_pass:
      - corruption_forward
      - recovery
  ch3_gate:
    intended_pass:
      - corruption_forward
      - reckless
    intended_recoverable_fail:
      - cautious
```

### Acceptance

- Python can load all input files without manual cleanup.
- Each choice group in the grain manifest has matching rows in `choice_catalogue.csv`, or is explicitly marked non-balance.
- Each balancing gate has a row in `gate_catalogue.csv`.

---

## Phase 5 — Python balance simulator

**Goal:** Model route economy and detect impossible goals, cliffs, and dominant choices.

### New files

- `main-game/pipeline/tools/simulate_balance.py`
- `main-game/pipeline/tools/balance_model.py`
- `main-game/pipeline/releases/release-1-mvp/balance/balance_report.md`
- `main-game/pipeline/releases/release-1-mvp/balance/policy_results.csv`
- `main-game/pipeline/releases/release-1-mvp/balance/gate_results.csv`
- `main-game/pipeline/releases/release-1-mvp/balance/choice_dominance_report.csv`
- `main-game/pipeline/releases/release-1-mvp/balance/cliff_report.csv`

### Simulator state

Track at minimum:

```python
state = {
    "day": 100,
    "period": "prologue",
    "grain_id": "start",
    "inspiration": 0,
    "inspiration_cap": 50,
    "corruption_level": 1,
    "corruption_xp": 0,
    "anxiety": 0,
    "manuscript_progress": 0,
    "suspicion": {
        "stern": 0,
        "missy": 0,
        "vance": 0,
        "gideon": 0,
    },
    "flags": {},
    "chain_levels": {
        "stern": 0,
        "missy": 0,
        "vance": 0,
    }
}
```

### Required simulation reports

#### 5.1 Policy pass/fail report

For each policy:

- final result;
- ending reached;
- last grain;
- manuscript progress;
- final corruption;
- final inspiration;
- max anxiety;
- gates passed/failed;
- route notes.

#### 5.2 Gate range report

For each gate:

- minimum possible relevant stats;
- maximum possible relevant stats;
- value by policy;
- intended pass/fail;
- actual pass/fail;
- warning if mismatch.

#### 5.3 Dominant choice report

Flag choices that are strictly worse than another option in the same group unless protected by design note.

Potential rule:

- A choice is dominated when another option gives equal or better inspiration/corruption and equal or lower anxiety/suspicion, with no unique flag/unlock.

#### 5.4 Cliff report

Flag when a small choice difference causes a major result shift.

Examples:

- one choice changes outcome from Day 105 completion to deadline fail;
- one missing inspiration point blocks a required chapter;
- one suspicion hit jumps from safe to dismissal;
- penance relief trivializes all anxiety pressure.

#### 5.5 Random/fuzz route report

Generate N random policy-weighted runs.

Default:

```text
N = 10000
```

Report ending distribution:

| Ending/result | Count | Percentage |
|---|---:|---:|
| MVP ending | | |
| weak completion | | |
| rejection | | |
| deadline 1 | | |
| deadline 2 | | |
| dismissed | | |
| unexpected stop | | |

### Acceptance

- `simulate_balance.py` runs from command line.
- Reports generated without manual intervention.
- Must-pass targets clearly PASS/FAIL.
- At least one deterministic policy and random fuzz run are supported.

---

## Phase 6 — Runtime vs simulator comparison

**Goal:** Compare real Ren'Py captures against model predictions.

### New files

- `main-game/pipeline/tools/compare_runtime_to_model.py`
- `main-game/pipeline/releases/release-1-mvp/balance/runtime_model_comparison.md`
- `main-game/pipeline/releases/release-1-mvp/balance/runtime_model_mismatches.csv`

### Inputs

- JSONL runtime captures from `main-game/non-prod-game/debug_captures/`
- grain manifest
- policy simulation results
- gate catalogue

### Compare

For each runtime capture:

| Check | Mismatch meaning |
|---|---|
| runtime grain missing from manifest | untagged or stale grain |
| manifest grain never reached | untested or impossible route |
| runtime gate result differs from simulator | model or implementation bug |
| runtime stat deltas differ from catalogue | spreadsheet/model stale |
| runtime ending differs from target | balance or implementation issue |
| runtime unknown branch flag | missing catalogue entry |

### Mismatch classes

| Class | Meaning |
|---|---|
| `MODEL_STALE` | Python/spreadsheet does not match implemented Ren'Py |
| `IMPLEMENTATION_BUG` | Ren'Py route/state behavior contradicts intended model |
| `TAG_DRIFT` | grain/DAG tags are missing or stale |
| `TEST_DEVIATION` | human route did not follow declared policy |
| `DESIGN_DECISION_REQUIRED` | model and runtime agree, but outcome conflicts with design target |

### Acceptance

- P1 and P2 runtime captures can be compared to simulated policies.
- Mismatches are written to CSV with grain/gate IDs.
- No blocker mismatches remain before promotion.

---

## Phase 7 — Agentic workflow integration

**Goal:** Make the testing framework usable by agents without letting agents rewrite the game accidentally.

### Agent roles

| Agent role | Allowed actions | Forbidden actions |
|---|---|---|
| Grain Tagger | add/update `DAG_GRAIN`, `DAG_CHOICE`, `DAG_GATE` comments | rewrite prose, change route logic |
| Manifest Builder | run extraction, produce gap reports | edit scripts directly |
| Runtime Instrumenter | add debug capture calls at grain boundaries | alter player-facing copy or branch outcomes |
| Balance Modeler | update CSV/YAML model files | change `.rpy` scripts |
| Balance Analyst | run simulator, summarize failures/cliffs | tune numbers without explicit task |
| Runtime QA Agent | inspect capture logs and compare to model | infer feel/pacing without human notes |
| Human Designer | approve tuning changes and design exceptions | none |

### Agent task sequence

1. **Grain extraction pass**
   - Run manifest builder.
   - Produce gap report.

2. **Tagging pass**
   - Add missing `DAG_GRAIN` / `DAG_CHOICE` / `DAG_GATE` only where required.
   - Do not change routing.

3. **Instrumentation pass**
   - Add `debug_enter_grain`, `debug_choice`, `debug_gate`, `debug_exit_grain`, `debug_ending` calls.
   - Do not change player-facing content.

4. **Model build pass**
   - Populate choice/gate catalogues.
   - Define policy targets.

5. **Simulation pass**
   - Run deterministic policies.
   - Run random fuzz.
   - Generate reports.

6. **Runtime QA pass**
   - Execute required route captures manually or with Ren'Py automation where possible.
   - Compare logs to model.

7. **Tuning proposal pass**
   - Agent proposes numeric changes only.
   - Human approves.

8. **Retest pass**
   - Re-run simulator.
   - Re-run impacted runtime captures.

### PR/review contract

Every testing-framework PR must declare:

- files changed;
- whether routing changed;
- whether prose changed;
- whether stat deltas changed;
- commands run;
- generated report paths;
- remaining blockers.

---

## Phase 8 — Balance tuning workflow

**Goal:** Adjust economy numbers safely.

### Tuning loop

1. Change numbers in `choice_catalogue.csv`, `gate_catalogue.csv`, or approved `.rpy` stat effects.
2. Run simulator.
3. Review:
   - policy pass/fail;
   - gate ranges;
   - cliffs;
   - dominant choices;
   - ending distribution.
4. Apply minimal tuning change.
5. Re-run simulator.
6. Run impacted runtime capture.
7. Compare runtime to model.
8. Update notes.

### Tuning principles

- Fix cliffs before polishing averages.
- Do not make corruption-forward strictly optimal.
- Cautious should be viable but weaker, not silently bricked.
- Passive should receive clear warning and route toward soft fail/rejection, not accidental hard fail unless deliberately chosen.
- Reckless should buy heat and manuscript power while increasing confrontation/anxiety pressure.
- Penance should relieve pressure but not erase consequences.
- Writing gates should be legible through feedback before they punish the player.

### Numeric review checklist

For each gate:

- [ ] intended pass policies pass;
- [ ] intended fail policies fail clearly;
- [ ] recovery path is possible if designed;
- [ ] one-point misses are intentional or smoothed;
- [ ] no dominant choice invalidates the menu;
- [ ] suspicion/anxiety pressure matters.

---

## Phase 9 — Promotion evidence package

**Goal:** Produce the testing proof needed before MVP promotion.

### Required output files

- `release1_grain_manifest.json`
- `release1_grain_gaps.md`
- `balance_report.md`
- `policy_results.csv`
- `gate_results.csv`
- `cliff_report.csv`
- `choice_dominance_report.csv`
- `runtime_model_comparison.md`
- captured JSONL files for P1-P7
- final route matrix summary

### Final route matrix summary

Create:

```text
main-game/pipeline/releases/release-1-mvp/qa/release1_route_matrix_results.md
```

Include:

| Run | Expected | Actual | Pass/fail | Notes |
|---|---|---|---|---|
| P1 | Day 105 MVP ending | | | |
| P2 | cautious completion/weak path | | | |
| P3 | rejection/soft fail | | | |
| P4 | deadline fail 1 | | | |
| P5 | deadline fail 2 | | | |
| P6 | anxiety dismissal | | | |
| P7 | confrontations/penance | | | |

### Acceptance

- No unknown runtime endings.
- No unresolved blocker mismatches.
- Full route matrix recorded.
- Simulator and runtime broadly agree on gate outcomes.
- Remaining mismatches are documented as accepted design exceptions or non-blocking tool limitations.

---

## Phase 10 — Packaging safeguards

**Goal:** Ensure debug/test tooling does not leak into public build.

### Public build exclusions

Exclude:

- `debug_grain_overlay.rpy`
- `debug_run_capture.rpy`
- `debug_captures/`
- test harness labels from player-accessible routes
- generated QA logs unless intentionally packaged as dev notes
- local saves/cache/logs/tracebacks

### Acceptance

- Clean packaged candidate does not show debug overlay.
- Public build cannot start capture controls.
- Packaged build is separately smoke-tested after exclusions.

---

## 7. Command design

Suggested command names:

```powershell
py main-game/pipeline/tools/build_grain_manifest.py --release release-1-mvp
py main-game/pipeline/tools/simulate_balance.py --release release-1-mvp
py main-game/pipeline/tools/compare_runtime_to_model.py --release release-1-mvp
```

Optional all-in-one command:

```powershell
py main-game/pipeline/tools/run_release1_balance_check.py
```

This should run:

1. grain manifest build;
2. grain gap report;
3. balance simulation;
4. runtime/model comparison if capture logs exist;
5. final summary.

---

## 8. Data quality rules

### IDs

- IDs must be stable and lowercase snake case.
- Do not include prose snippets in IDs.
- Do not rename IDs once runtime captures exist unless migration is intentional.

### CSV/YAML

- No blank required fields.
- No duplicate choice IDs within a choice group.
- No duplicate gate IDs.
- Every gate ID in runtime logs must exist in `gate_catalogue.csv`.
- Every balance-critical choice group must exist in `choice_catalogue.csv`.

### Runtime logs

- One run ID per official attempt.
- Official runs are forward-only.
- Failed/abandoned captures are retained but marked invalid.

---

## 9. Severity model

| Severity | Meaning | Examples |
|---|---|---|
| Blocker | prevents promotion/testing proof | crash, soft lock, impossible P1, missing ending, unknown runtime route |
| Major | breaks intended economy | cautious always hard-fails, reckless never punished, corruption choice dominates all |
| Medium | confusing or brittle | one-point gate miss with poor feedback, unclear rejection cause |
| Minor | polish/tooling | missing note, non-blocking tag drift, report formatting |

---

## 10. Framework completion definition

The testing/balance framework is complete for Release 1 MVP when:

- [ ] grain manifest exists and covers all balancing-critical labels;
- [ ] debug overlay and runtime capture work in non-prod;
- [ ] route captures exist for P1-P7;
- [ ] Python simulator runs deterministic policies;
- [ ] random fuzz report exists;
- [ ] runtime/model comparison report exists;
- [ ] balance report lists pass/fail against explicit design targets;
- [ ] no blocker issues remain;
- [ ] debug tooling is excluded from public packaging.

---

## 11. Recommended build order

Implement in this order:

1. `DAG_GRAIN` convention and grain manifest builder.
2. Minimal debug overlay.
3. Runtime JSONL capture.
4. P1/P2/P4 thin route captures.
5. Choice/gate catalogue CSVs.
6. Deterministic policy simulator.
7. Gate range and cliff reports.
8. Runtime/model comparison.
9. Random fuzz runs.
10. Full P1-P7 capture matrix.
11. Promotion evidence package.
12. Public build exclusion profile.

This order prevents overbuilding the simulator before the game can prove basic runtime completion.
