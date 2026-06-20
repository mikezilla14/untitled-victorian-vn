# Narrative Change Brief — day101
# Invoked by: lead_narrative_editor
# Scale: M
# Status: CLOSED

## Trigger

Lead narrative review of the dark-romance rewrite experiment (`narrative/draft/releases/release-1-mvp/planning/day101_non_canon_draft_rewrite.rpy`) against the passed sandbox baseline (`main-game/non-prod-game/game/days/day101_non_canon.rpy`).

**Verdict:** REJECT as wholesale replacement. **Approve selective merge** of atmosphere, Irish precarity, Stern inspection prose, Missy/Hindon identity trap, and ledger reflection upgrades — while **preserving** the live spine (dressing room, stairwell, ghost wall path, Gideon naming, full `day1_vance_relation` tree, restrained IRL corridor layer).

**Human note:** Experiment still references Lady Eleanor blackmail economics; Day 100 canon is Sir John dismissal + conditional Savoy reference. All Wiltshire backstory in merged prose must align with promoted `day100_non_canon.rpy`.

## Affected scope

### Labels (merge into live sandbox — preserve names, jumps, and graph)

| Label | Action |
|-------|--------|
| `day101_main` | **Replace opener** with experiment donor: Savoy consumption metaphor, Cork lilt suppression, Holywell/workhouse ruin geometry, Wiltshire parson's-daughter mask. **No** Eleanor blackmail / sovereign payment. |
| `day101_1_cora_waiting` | **Enhance** interior: reference in pocket as Sir John's conditional leash (post-dismissal), not "Lady Eleanor signed with a trembling hand." Keep clock / enter beat. |
| `day101_1_morning_interview` | **Enhance** Stern physical inspection (carbolic soap, collar/throat diagnostic touch). **Fix** Stern reference line to Sir John / Wiltshire household. **Keep** live competent-path split (`"Exact?"` / short reply). **Do not** import long single-block competent dialogue from experiment. |
| `day101_1_vance_throws_toy` | **Keep live spine** (scent-bottle → Gideon `"Vance."` → Cora naming). Optional: borrow *tone* of Vance-over-Missy cruelty from experiment as **future** alt beat only — **out of scope for this brief** unless human requests corridor cold-open swap. |
| `day101_1_vance_dressing_room` | **PRESERVE UNCHANGED** (structure + menus + setters). |
| `day101_1_vance_stairwell_encounter` | **PRESERVE UNCHANGED** (structure + menus + setters). |
| `day101_2_missy_meets_cora` | **Insert** Hindon / East Knoyle / Mr. Harrison curate trap from experiment. Retain live Missy warmth, spoon salvage, corridor-rules wisdom. |
| `day101_2_coras_path_choice` | **Keep live corridor logic** (predator / prey / ghost). Ghost arm = pull Missy away + wall rhythm — **not** experiment's bold-knock full-view. IRL layer = sound, fragment, silhouette; **no** bare buttocks / crop on vanity in hotel corridor. Optional: borrow sharper slap/gasp *audio* from experiment at ≤2.5 live spice. |
| `day101_3_taking_stock_day1` | **Cherry-pick** ledger reflection lines from experiment where they improve accounting prose; keep live branch `if story.day1_corridor_state` structure. |
| `day101_night_story_window` | **Optional polish** on rest/reflection sub-menu prose from experiment. Preserve chain routing (`story.resolve_chain_label`). |
| `day101_4_write_the_chapter` | **Enhance** corruption/inspiration framing inner monologue from experiment. Explicit corridor imagery belongs **here** (manuscript layer), scaled to writing minigame / book1 retelling rules — not IRL corridor. |

### Labels explicitly out of merge

- Do **not** delete or bypass: `day101_1_vance_dressing_room`, `day101_1_vance_stairwell_encounter`.
- Do **not** replace ghost path with experiment knock-and-enter beat.

### Flags / setters (unchanged enums — MUST all fire)

| Setter | Values | Notes |
|--------|--------|-------|
| `story.set_day1_interview_state` | `"meek"` / `"competent"` | Unchanged menus. |
| `story.set_day1_stern_relation` | `"subservient"` / `"resistant"` / `"complicit"` | Unchanged. |
| `story.set_day1_stern_secret_bound` | `"fearful"` / `"loyal"` / `"exploitative"` | Unchanged. |
| `story.set_day1_vance_relation` | Full `VALID_VANCE_RELATIONS` tree via dressing room + stairwell | **Must remain** — experiment's subservient/defiant/ghostly-only corridor menu is insufficient. |
| `story.set_corridor_state` | `"predator"` / `"prey"` / `"ghost"` | Semantic lock: ghost = unseen / wall / walk-on. |
| `story.set_day1_ledger_focus` | `"inspiration"` / `"corruption"` | Unchanged. |
| `story.set_day1_night_action` | `"write"` (write path) | Unchanged. |
| `story.set_missy_day1_trust_state` | `"unsettled"` / `"warned_cora"` / `"shared_caution"` / `"soothed"` | **ADD** explicit setter calls on corridor outcomes + Hindon beat where prose implies trust shift (currently missing in live draft). |

Suggested corridor mapping (writers may adjust copy, not semantics):

| Corridor branch | Suggested `missy_day1_trust_state` |
|-----------------|-------------------------------------|
| Predator (used Missy as shield) | `"unsettled"` or `"warned_cora"` |
| Prey (Cora dragged Missy into risk) | `"shared_caution"` |
| Ghost (Cora pulled Missy away) | `"soothed"` |

### Balance / implementation

- Preserve existing `apply_balanced_effect(profile, intensity=..., witness=...)` on all choice stat lines.
- Ghost path bespoke: `$ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5, insp=10, corr=0)` — **keep as-is**.
- Prey path: `$ apply_balanced_effect("reckless", intensity=1.4, witness="vance")` — **keep as-is**.
- Do **not** introduce raw stat lines except where graph already locks bespoke deltas.
- Preserve `[DAG_*]`, `[STATE]`, `[CHOICE]`, `[BEAT]`, `[ASSET]` markers; run `dag_tag_update` if label prose changes materially.

### story_board rows

- Global State Tracking: `day1_interview_state`, `day1_corridor_state`, `day1_ledger_focus`, `missy_day1_trust_state`
- Scene Ledger: Day 101 — update descriptive bullets after gates pass (Hindon trap, opener precarity)
- Adult Payoff Structure: IRL corridor restrained; manuscript retelling carries explicit heat
- Spine sequence steps 1–4: `day101_main` through `day101_night_story_window`

### Canon citations (non-negotiable)

| Source | Requirement |
|--------|-------------|
| `main-game/canon/cora_character_canon.md` § Origins / Breaking Point | Irish erasure + performed English country girl; prologue ended in **absolute dismissal** — reference is survival tool, not blackmail triumph. |
| `main-game/canon/characters_minor_canon.md` § Sir John Wiltshire | Savoy reference spoken/threatened by **Sir John** after Lady Eleanor demands expulsion — Stern cites Sir John or "the Wiltshire household," not Lady Eleanor as reference author. |
| `main-game/canon/characters_minor_canon.md` § Lady Eleanor | Prologue only; **no** Day 101 blackmail payment, trembling signature, or sovereign economics. |
| `main-game/draft/releases/planning/story_board.md` § Adult Payoff | IRL hotel layer restrained; explicit H-scene payoff in manuscript / writing minigame. |
| `main-game/draft/releases/planning/story_board.md` § `day1_corridor_state` | Ghost = predator/prey/ghost archetype seed; ghost branch semantics preserved for Day 102+ contraband logic. |
| Prior gate `day101_gate_lead_narrative.md` | Voice lock Day 1: Cora spoken ≤8 words, no contractions to superiors; thought/speech Gap. |

## Narrative requirements (MUST)

### 1. Wiltshire backstory — Sir John reference geometry

Replace all experiment blackmail residue:

| Remove | Replace with |
|--------|--------------|
| "Lady Eleanor signed with a trembling hand" | Sir John's reference — conditional, cold, post-dismissal |
| "five gold sovereigns and her private dignity" | Dismissal at Lady's behest + Sir John's threat (gutter / blackened name) — interior echo only |
| Stern: "The Lady Eleanor speaks highly..." | Stern: Sir John / Wiltshire household speaks to discretion — period address |

**Example shapes (not verbatim lock):**

- Inner: *Sir John's reference sits in my pocket like a blade with his name on the handle.*
- Stern: *"Sir John's reference speaks to your quiet nature, Vale."*

Cross-check against live `day100_non_canon.rpy` reconvergence exit before finalizing Stern's spoken reference line.

### 2. Opening precarity (donor merge)

From experiment `day101_main` + waiting beat:

- Savoy as consumption / erasure of identity
- Cork lilt forced below the floorboards
- Holywell Street + workhouse as layered ruin (Irishness, papers, manuscript)
- Forged **performance** of Wiltshire identity — papers support mask; Savoy reference is Sir John's leash

### 3. Missy / Hindon identity trap (new beat)

Insert in `day101_2_missy_meets_cora` after papers/Wiltshire exchange:

- Missy from **Hindon** (~3 miles from Cora's claimed **East Knoyle** fiction)
- Local colour test: old oak by mill, curate Mr. Harrison — Cora evades without blowing cover
- Inner: Missy as "the real thing" Cora pretends to be; "two halves of a lie"
- Cora spoken evasion: **≤8 words per line**, no contractions

Do **not** resolve Hindon test in Day 101 — seed recurring exposure for Day 102+.

### 4. Stern interview enhancement

Merge experiment's clinical dominance (boots, carbolic, throat/collar diagnostic touch) into live interview **after** first menu, before second menu.

**Keep** live lines that gate passed:

- Competent path split across Stern's *"Exact?"*
- Complicit gaze branch hot/deliberate touch — compatible with dark romance
- Third secret menu exploitative slip

**Voice pass required** on any merged Cora spoken lines.

### 5. Corridor — semantic lock + spice zoning

| Branch | IRL live spice (≤2.5) | Manuscript layer (write beat) |
|--------|----------------------|-------------------------------|
| Predator | Missy opens door; **fragments** only (hand, shoe, stick) — live draft model | Fuller tableau in `day101_4_write_the_chapter` / book1 retelling |
| Prey | Vent/board creak; chin grip; near-discovery | Invitation/fear blur in corruption framing |
| Ghost | Wall rhythm; walk-on; **no direct view** | Precision-from-ignorance in inspiration framing |

**Do not import** experiment predator/ghost explicit anatomy (bare buttocks, chemise, crop on vanity) into IRL corridor.

### 6. Preserve dark-romance spine scenes

These are **load-bearing** for Release 1 Vance intimacy and `day1_vance_relation` values beyond subservient/defiant/ghostly:

- `day101_1_vance_dressing_room` — collar intimacy (`protected` / `intimate` / `observed`)
- `day101_1_vance_stairwell_encounter` — (`loyal_witness` / `accomplice` / `silent_observer`)

No prose merge from experiment may delete, bypass, or shorten these labels.

### 7. Gideon seed

Live draft's `"Your name, girl?"` / `"Cora, Sir."` / discretion collar beat in `day101_1_vance_throws_toy` **must remain**. Experiment removes this — do not drop.

### 8. `missy_day1_trust_state` wiring

Add `story.set_missy_day1_trust_state(...)` at end of corridor branches (and optionally after Hindon evasion if writers add a micro-trust beat). Document chosen mapping in convergent report.

### 9. Artifact hygiene

- Deliver clean `.rpy` to `main-game/non-prod-game/game/days/day101_non_canon.rpy`
- No markdown wrapper, `<details>`, or planning prose
- Fix typos if any donor lines imported ("transitonal", "slowly sliding", "teeth grit")

## Donor material map (experiment → live)

| Experiment source | Live target | Import? |
|-------------------|-------------|---------|
| L93–97 opening inner monologue | `day101_main` | **Yes** (canon-fix references) |
| L128–129 waiting pocket beat | `day101_1_cora_waiting` | **Yes** (Sir John reference) |
| L217–219 Stern inspection prose | `day101_1_morning_interview` | **Yes** |
| L167–169 Stern Eleanor reference | `day101_1_morning_interview` | **Rewrite** to Sir John |
| L339–437 Vance-Missy corridor cold open | `day101_1_vance_throws_toy` | **No** (this brief) |
| L541–559 Hindon trap | `day101_2_missy_meets_cora` | **Yes** |
| L586–682 corridor explicit IRL | `day101_2_coras_path_choice` | **No** — tone/audio only |
| L658–682 ghost knock-enter | `day101_2_coras_path_choice` | **No** |
| L717–737 ledger reflection | `day101_3_taking_stock_day1` | **Partial** |
| L791–824 rest/reflection + write framing | night window / write chapter | **Partial** |
| Dressing room / stairwell | — | **N/A — keep live** |

## Out of scope

- Wholesale replacement of live `day101_non_canon.rpy` with experiment file.
- Removing `day101_1_vance_dressing_room` or `day101_1_vance_stairwell_encounter`.
- Ghost path knock-and-enter redesign.
- IRL explicit BDSM visibility in corridor (reserve for manuscript layer).
- New StoryState flags or label renames beyond trust-state wiring.
- Canon file edits (`main-game/canon/**`).
- Promoting to `main-game/prod-game/` (separate `promote-day`).
- Replacing scent-bottle corridor with Vance-Missy abuse beat (flag for human if desired later).

## Personas (M)

Run **partial divergent pool**, then convergent merge into live sandbox:

| Persona | Focus |
|---------|-------|
| **tension** | Opening precarity, Stern inspection, corridor near-discovery |
| **class** | Sir John reference vs performed Wiltshire maid; Stern house law |
| **thematic** | Irish erasure, Hindon trap, ghost-as-unseen observer |
| **erotic** | Manuscript/write-beat heat only; dressing room/stairwell preservation check |
| **humour** | Skip |

Skip mystery persona (no new clue geometry).

## Scene architecture (post-merge — unchanged spine)

```
day101_main (enhanced opener)
  → day101_1_cora_waiting (Sir John reference beat)
  → day101_1_morning_interview (enhanced Stern inspection)
  → day101_1_vance_throws_toy (UNCHANGED live)
  → day101_1_vance_dressing_room (UNCHANGED live)
  → day101_1_vance_stairwell_encounter (UNCHANGED live)
  → day101_2_missy_meets_cora (+ Hindon trap)
  → day101_2_coras_path_choice (live branches + trust setters)
  → day101_3_taking_stock_day1 (+ ledger polish)
  → day101_evening_consequence_window
  → day101_night_story_window / day101_4_write_the_chapter
  → day102_1_cora_missy_first_shift
```

## MUST FIX checklist (gate resubmission)

1. **No** Lady Eleanor blackmail, sovereign payment, or trembling-signature reference prose (`characters_minor_canon.md`, `cora_character_canon.md`).
2. Stern / waiting beats cite **Sir John** or Wiltshire household reference geometry aligned with `day100_non_canon.rpy`.
3. **Hindon / East Knoyle** trap present in `day101_2_missy_meets_cora`.
4. **Ghost corridor path** = walk-on / wall — **not** knock-and-enter full view.
5. **IRL corridor** ≤2.5 spice; no explicit anatomy/props — manuscript layer carries heat.
6. **`day101_1_vance_dressing_room`** and **`day101_1_vance_stairwell_encounter`** preserved intact.
7. Gideon **naming/discretion** beat preserved in `day101_1_vance_throws_toy`.
8. **`set_missy_day1_trust_state`** wired on corridor outcomes.
9. Cora spoken lines to superiors: **≤8 words**, no contractions (Day 1 voice lock).
10. **`apply_balanced_effect`** preserved on stat choices; graph markers intact.
11. Clean `.rpy` artifact at `main-game/non-prod-game/game/days/day101_non_canon.rpy`.

## Return to

- **Agent:** `writers_room` (Workflow D — scale M → partial pool → convergent → gates 5–7)
- **Pipeline:** `revise-narrative` → on narrative / psychology / historical **PASS** → `non_prod_code_agent` if wrap needed → `lead_narrative_editor` re-review → invalidate prior `day101_gate_*` verdicts

## Post-gate housekeeping (orchestrator / convergent)

1. Update `main-game/pipeline/releases/release-1-mvp/days/day101/synthesis/day101_convergent_report.md` (`Pass: editor-revision-1` or equivalent).
2. Update `continuity_handoff.md` § Handoff Day 101 → Day 102 (Hindon exposure vector, Sir John reference, trust states).
3. Re-run full gate chain: lead narrative → forensic psychology → Victorian.
4. Run `py scripts/validate.py --profile changed --files "main-game/non-prod-game/game/days/day101_non_canon.rpy"`.
5. Set brief `Status: CLOSED` when sandbox aligned and gates pass.

## Closure (2026-06-21)

- All three gates **PASS** / **PSYCHOLOGICALLY CONSISTENT** / **HISTORICALLY SOUND** (editor-revision-1).
- Victorian review corrected **East Knoyle → Fovant** for Hindon parish distance (~3 mi).
- Strict validation: `py scripts/validate.py --profile changed --agent human --strict-gates --files "main-game/non-prod-game/game/days/day101_non_canon.rpy"` — **passed**.

## Reference files

| File | Use |
|------|-----|
| `main-game/non-prod-game/game/days/day101_non_canon.rpy` | **Merge target** (passed baseline) |
| `narrative/draft/releases/release-1-mvp/planning/day101_non_canon_draft_rewrite.rpy` | Donor (atmosphere, Hindon, Stern — not structure) |
| `main-game/non-prod-game/game/days/day100_non_canon.rpy` | Sir John reference / dismissal exit cross-check |
| `main-game/canon/cora_character_canon.md` | Voice + backstory lock |
| `main-game/canon/characters_minor_canon.md` | Sir John / Lady Eleanor scope |
| `main-game/draft/releases/planning/story_board.md` | Flag spine + adult payoff rules |
| `main-game/pipeline/releases/release-1-mvp/days/day101/gates/day101_gate_lead_narrative.md` | Prior PASS criteria |
