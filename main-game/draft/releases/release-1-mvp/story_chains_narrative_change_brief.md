# Narrative Change Brief — story_chains (cross-cutting, Days 101–104)

# Invoked by: lead_narrative_editor
# Scale: M
# Status: CLOSED

## Trigger

Lead narrative editor prose audit (2026-06-28) of Release 1 main spine vs. optional story chains and penance confrontations. **Verdict:** Main five-day spine is coherent and branch-memory-strong; optional chains are mechanically wired but **prose tiers lack differentiation**. All three character chains (Stern, Missy, Vance) reuse an identical scene template (safe vs. charged menu → `complete_chain_beat` on both arms → tier-3 gated climax). Menu copy promises `[[Shed Suspicion / Break Chain]]` but safe paths still advance chain level. Penance confrontations share a single debuff template. Chains do not emit spine-readable flags, so mandatory plot never acknowledges chain depth.

**Human note:** Confirmed user observation — story chain tiers need distinct dramatic jobs, not only spice-gradient escalation.

## API pass complete (2026-06-28)

`non_prod_code_agent` landed in non-prod:

- `StoryState.abandon_chain_beat`, extended `complete_chain_beat(character, path=...)`, outcome fields/setters, `*_chain_closed` flags.
- `story_chains_non_canon.rpy` — safe arms → `abandon_chain_beat`; charged T1–T2 → `path="safe_progress"`; charged T3 → `path="climax"`; menu tag `Close Track` on safe arms.
- Spine callbacks: `day103_4_room_stern_suspicion`, `day103_2_suite_gideon_beat`, `day102_3` corridor aftermath; penance `cora_inner` hooks on chain outcome.
- Notes: `story_chains_non_canon_notes.md` §5.

**Writers' room still required:** ~~tier dramatic-job prose rewrite~~ **Done (code-revision-1).** Pending: formal gate chain + prod promotion.

## Lead narrative gate (2026-06-28)

**PASS** — `main-game/pipeline/releases/release-1-mvp/shared/gates/story_chains_gate_lead_narrative.md`

## Victorian gate (2026-06-28)

**HISTORICALLY_SOUND** — `main-game/pipeline/releases/release-1-mvp/shared/gates/story_chains_gate_victorian.md`

**Brief closed.** Next: `implement-spec` / prod promotion (`classes.rpy`, `story_chains.rpy`).

## Forensic psychology gate (2026-06-28)

**PSYCHOLOGICALLY_CONSISTENT** — `main-game/pipeline/releases/release-1-mvp/shared/gates/story_chains_gate_forensic_psychology.md`

## Contract anchor

`day_id` in JSON sidecar is **`day102`** (first full afternoon story-window integration). **Deliverable file** is shared module, not a day script.

## Affected scope

### Primary merge target

| File | Action |
|------|--------|
| `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy` | **Rewrite** chain beats + penance labels per this brief |
| `main-game/prod-game/game/story_chains.rpy` | Promote after gates + `implement-spec` (verbatim creative text) |

### Labels (rewrite in place — preserve names, DAG tags, jumps/returns)

| Label | Tier / role |
|-------|-------------|
| `stern_chain_1` | Stern T1 — posture / linen audit |
| `stern_chain_2` | Stern T2 — notebook extraction |
| `stern_chain_3` | Stern T3 — vacant-room corrective / climax |
| `missy_chain_1` | Missy T1 — French seam / solidarity pact |
| `missy_chain_2` | Missy T2 — broom-closet shared secret |
| `missy_chain_3` | Missy T3 — manuscript page / intimacy climax |
| `vance_chain_1` | Vance T1 — dropped handkerchief / witnessed humiliation |
| `vance_chain_2` | Vance T2 — staircase grief / power reversal |
| `vance_chain_3` | Vance T3 — desk blackmail / collusion climax |
| `confrontation_stern` | Penance — Stern-specific punishment |
| `confrontation_missy` | Penance — Missy betrayal labour |
| `confrontation_vance` | Penance — Vance-class insult labour |
| `anxiety_breakdown_downtime` | **Preserve** — voice is distinct; light polish only if needed |
| `watch_suspicion` | **Preserve** routing; no prose change unless lock-text copy edit |
| `story_window_penance_gate` | **Preserve** behaviour |

### Day spine — minimal callback hooks (1–2 lines each, conditional)

Writers add **only** when corresponding chain outcome flag is set (see Implementation contract). Do not restructure day labels.

| Label | Callback when |
|-------|----------------|
| `day103_4_room_stern_suspicion` | `story.stern_chain_outcome` in `("marked", "climax")` |
| `day103_2_suite_gideon_beat` | `story.vance_chain_outcome` in `("collusion", "climax")` |
| `day104_4_twilight_ledger_false_dawn` | any `*_chain_outcome` climax + `story.day4_escape_state` (penance vs. voluntary atonement echo) |
| `day102_3_coras_choice` aftermath corridor | optional Missy line if `story.missy_chain_outcome == "abandoned"` |

### Flags / setters (new — requires `non_prod_code_agent` before or parallel to prose)

| Setter / helper | Values / behaviour |
|-----------------|-------------------|
| `story.abandon_chain_beat(character)` | **NEW.** Safe "break chain" path at T1–T2: does **not** increment `*_chain_level`; sets `*_chain_outcome` to `"abandoned"`; applies existing safe-path stat deltas. Track remains closed (`chain_available` → False via level cap or explicit `*_chain_closed` boolean — implementer chooses minimal diff). |
| `story.complete_chain_beat(character, path=...)` | **EXTEND** optional `path`: `"safe_progress"` (T1–T2 charged that still advances), `"climax"` (T3 one-time). Emits outcome flag. |
| `story.set_stern_chain_outcome` | `"none"` / `"abandoned"` / `"cautious"` / `"marked"` / `"climax"` |
| `story.set_missy_chain_outcome` | `"none"` / `"abandoned"` / `"pact"` / `"entangled"` / `"climax"` |
| `story.set_vance_chain_outcome` | `"none"` / `"abandoned"` / `"voyeur"` / `"collusion"` / `"climax"` |

Default for all outcomes: `"none"`. Whitelist + typed setters in `StoryState` per `chief_architect` / `classes_non_canon.rpy` convention.

**Menu contract after implementation:**

| Tier | Safe arm | Charged arm |
|------|----------|-------------|
| 1–2 | `abandon_chain_beat` — **closes track** | `complete_chain_beat(path="safe_progress")` — advances to next tier |
| 3 | `abandon_chain_beat` or safe copy — **permanent climax loss** (existing copy) | Gated climax — `complete_chain_beat(path="climax")` |

Remove `[[Break Chain]]` from menu text on arms that still call `complete_chain_beat`.

### Balance / implementation

- Preserve existing `apply_effects(...)` kwargs on each arm unless balance report explicitly flags a tier; do not rebalance economy in this brief.
- Preserve tier-3 gates: `player.anxiety < 75` and `player.get_total_suspicion("<character>") < 80`.
- Preserve `[DAG_NODE]`, `[DAG_CHOICE]`, `[STATE]`, `[CHOICE]`, `[BEAT]`, `[ASSET]` markers; run `dag_tag_update` if menus change.
- IRL chain spice: tier 1 ≤ **2.0**, tier 2 ≤ **2.2**, tier 3 climax ≤ **2.2** (hotel layer). Reserve higher heat for manuscript retelling per `story_board.md` Adult Payoff Structure.
- Diegetic lock lines (`[player.anxiety]` / suspicion) — keep; polish for Victorian register only.

### story_board rows

- Global State Tracking — `stern_chain_level`, `missy_chain_level`, `vance_chain_level`, `penance_triggered`
- Two-Step Slot Integration — optional story windows (`day101_night_story_window`, `day102_afternoon_story_window`, `day103_1_optional_character_chain`)
- `check_confrontations` entry points — penance consumption unchanged
- Adult Payoff Structure — IRL chains restrained; climax is inspection/intimacy, not full explicit H-scene

### Canon citations (non-negotiable)

| Source | Requirement |
|--------|-------------|
| `main-game/canon/voice_guides/cora_voice_guide.md` | Speech/thought gap; public deference under pressure; sovereignty narrows in private chain beats only. |
| `main-game/canon/voice_guides/stern_voice_guide.md` | Iron discipline; keys as authority; improper touch framed as correction, not confession. |
| `main-game/canon/voice_guides/missy_voice_guide.md` | Sin/shame vocabulary as shield; trust earned; yield is conscious when it happens. |
| `main-game/canon/voice_guides/vance_voice_guide.md` | Petulant class rage; performance for audience; Gideon shadow on tier 3. |
| `main-game/canon/historical_guardrails.md` §10 | No modern feminism, casual class-mixing, or anachronistic address. |
| `main-game/draft/releases/planning/story_board.md` | Chain windows return to spine; penance consumes slot; confrontation at suspicion ≥ 50. |
| `main-game/non-prod-game/game/shared/story_chains_non_canon_notes.md` | Acute vs. base suspicion routing — do not break `apply_effects(stern_susp=...)` semantics. |

---

## Narrative requirements (MUST)

### 1. Per-character tier dramatic job (not spice-gradient clones)

Each tier must change **relationship state**, not only touch intensity. Writers deliver distinct scene purpose per cell:

#### Miss Stern — "The Sovereign Disciplines"

| Tier | Dramatic job | Safe arm (abandon) | Charged arm (advance) |
|------|--------------|--------------------|------------------------|
| **T1** | Posture audit — who controls the body in service | Country fool; Stern dismisses as beneath notice (`outcome: abandoned`) | Geometry answer; Stern marks the neck with keys (`outcome: cautious` → sets up T2) |
| **T2** | Knowledge extraction — notebook as confessional | Spelling exercise; notebook survives, heat cools (`abandoned`) | Scandalous passage read aloud; pulse check under apron (`cautious` → T3) |
| **T3** | Public vs. private discipline — kneeling as spectacle risk | Blind servant; fire extinguished forever (`abandoned`) | Kneeling audit; Stern's trembling improper inspection (`marked` / `climax`) |

**Differentiation rule:** T1 = external correction; T2 = intellectual theft accusation; T3 = body inventory under guise of housekeeping. Each tier's charged path must reference the previous tier's residue (e.g. T3 Stern mentions the notebook line from T2 if `stern_chain_level >= 2`).

#### Missy — "The Laundry Quarters Erotics"

| Tier | Dramatic job | Safe arm | Charged arm |
|------|--------------|----------|-------------|
| **T1** | Mutual protection pact | Silent stitch; friendship without entanglement (`abandoned`) | Cheek stroke; trust without romance (`pact`) |
| **T2** | Shared secret — valet case | "Forget you saw it" (`abandoned`) | Chest-to-chest in dark; chosen proximity (`entangled`) |
| **T3** | Authorship betrayal — page in hand | Tear page; trust dead (`abandoned`) | Defend writing + silk chemise; mutual kiss (`climax`) |

**Differentiation rule:** T1 = labour solidarity; T2 = danger-bonding; T3 = **Cora's crime is using Missy as material** — strongest existing beat; T1–T2 must foreshadow the manuscript moral wound.

#### Miss Vance — "The Blackmail Collusion"

| Tier | Dramatic job | Safe arm | Charged arm |
|------|--------------|----------|-------------|
| **T1** | Witnessed humiliation — Gideon shadow | Perfect bow; forgettable (`abandoned`) | Steal handkerchief; study petulant panic (`voyeur`) — **expand to full exchange (currently underwritten)** |
| **T2** | Grief witnessed — class mask slips | Slip past in shadow (`abandoned`) | Thumb on tear; dominance reversal (`voyeur` deepens) |
| **T3** | Shared crime — key as collusion | Potato maid performance (`abandoned`) | Vanity corner; collar marks; brass key transfer (`collusion` / `climax`) |

**Differentiation rule:** T1 charged path MUST reach Stern/Missy exchange length. Reference Gideon's correction from Day 102 tea crisis where possible (`story.day2_tea_choice` flavour line, not branch gate).

### 2. Menu copy tier-specific

Replace repeated `[[Shed Suspicion / Break Chain]]` / `[[Progress Chain]]` with tier-unique stakes. Examples (not verbatim lock):

| Character | T1 safe | T1 charged |
|-----------|---------|------------|
| Stern | "Play the stupid country girl and vanish." | "Answer her geometry and let her mark you." |
| Missy | "Stitch in silence and owe her nothing." | "Comfort her with touch she didn't ask for." |
| Vance | "Return the silk and be furniture." | "Steal the handkerchief and study her panic." |

Tier-3 safe must retain **permanent climax loss** language already present.

### 3. Time-of-day variants must alter stakes

Current `if time_manager.time_of_day` blocks are wallpaper. Each tier must add **one** conditional line or menu consequence:

- Morning = witness risk (footsteps, shift change)
- Afternoon = heat / visibility
- Evening or Night = reduced witnesses but higher intimacy violation

Not a full branch tree — one diegetic stake shift per tier.

### 4. Penance confrontations — character-specific punishment

Preserve stat effects (`*_susp=-35`, slot loss, no writing). Rewrite prose so each confrontation is **that person's** punishment logic:

| Label | Punishment identity | Must reference |
|-------|---------------------|----------------|
| `confrontation_stern` | Visible humiliation — grand stairs, witnesses, kneeling scrub | Last `stern_chain_outcome` if not `"none"`; keys / marble / character reference |
| `confrontation_vance` | Feminine class insult — cold silk, lavender, bleeding knuckles | Gideon as unseen audience; handkerchief or collar echo from chain |
| `confrontation_missy` | Social exile — betrayal labour, "don't speak to me again" | `missy_day2_trust_break` or chain climax betrayal; strongest emotional specificity of the three |

Shared closing beat ("night lost, manuscript untouched") may remain **one sentence**; the middle must not be interchangeable.

### 5. Distinguish voluntary atonement vs. assigned penance (Day 104)

When `story.day4_twilight_action == "atonement"`, interior copy should read as **Cora choosing** visible submission. When `confrontation_*` fires, copy should read as **assignment**. Optional cross-line in `day104_4_atonement` if `story.has_pending_penance()` was recently consumed — out of scope unless trivial.

### 6. Voice pass

- Cora spoken to superiors: short, class-appropriate; contractions only in `cora_inner` or private chain beats.
- Stern: no softening into romance confession at T3 — dread + invitation duality only.
- Missy: shame vocabulary on safe/abandon paths; charged paths show shield lowering deliberately.
- Vance: petulance, not villain monologue; T3 Gideon shadow mandatory.

### 7. Artifact hygiene

- Clean `.rpy` only in deliverable paths
- No `[BEAT]` notes in player-facing strings
- No internal spice labels in final menu captions (`2.2 Spice` → move to dev comment only)

---

## Tier differentiation matrix (acceptance test)

Gate resubmission fails if any row sounds interchangeable with another character's same tier:

| Test | Pass criterion |
|------|----------------|
| Blind read T2 | Reader can identify Stern vs. Missy vs. Vance without names |
| Safe T1 | Player understands track is **closed**, not merely cooled |
| Charged ladder | T3 charged prose impossible to understand without T1–T2 emotional setup |
| Penance | Three confrontations differ in verb choices (scrub / wash / boil) **and** emotional wound |
| Spine echo | At least one spine label reacts to `*_chain_outcome` |

---

## Out of scope

- New chain characters (Gideon chain deferred post-MVP)
- Fourth chain tier or Release 2 chain extension
- Economy rebalance / `apply_effects` number changes (unless gatekeeper flags regression)
- Manuscript retelling minigame CG prose
- Canon file edits (`main-game/canon/**`)
- Wholesale rewrite of Day 101–105 spine WORK blocks
- `advance_after_confrontation` router removal (already deprecated)
- Promoting to prod without gate chain pass

---

## Personas (M)

Run **partial divergent pool** (one spec per character chain), then convergent merge into `story_chains_non_canon.rpy`:

| Persona | Focus |
|---------|-------|
| **tension** | Stern T1–T2; Vance T1–T2; penance Stern |
| **class** | Vance full ladder; Stern T3 public humiliation; penance Vance |
| **erotic** | Missy T2–T3; Stern T3; Vance T3 — hotel-layer cap 2.2 |
| **thematic** | Missy T1–T3 manuscript betrayal arc; anxiety breakdown polish |
| **mystery** | Vance key collusion; optional spine callback seeds |

Skip humour persona.

---

## Implementation order (orchestrator)

1. **`non_prod_code_agent`** — `abandon_chain_beat`, outcome setters, `complete_chain_beat` path arg; update `story_chains_non_canon_notes.md` one paragraph.
2. **`writers_room`** — `revise-narrative` scale M per this brief.
3. **`scene_direction_agent`** — sprite lines if staging changes materially.
4. **Gates** — lead narrative → forensic psychology → Victorian (order fixed).
5. **`non_prod_code_agent`** — spine callback lines in day files if not done by convergent.
6. **`implement-spec` / promote** — `story_chains.rpy` + any day spine touch files.

---

## MUST FIX checklist (gate resubmission)

1. Safe arms at T1–T2 call `abandon_chain_beat` — **do not** increment chain level.
2. Charged arms at T1–T2 call `complete_chain_beat` and advance level.
3. Each tier sets distinct `*_chain_outcome` per whitelist.
4. Menu text no longer claims "Break Chain" on arms that advance the ladder.
5. Stern / Missy / Vance T1–T3 each satisfy dramatic-job table above.
6. Vance T1 charged path expanded to full dialogue exchange (parity with Stern T1).
7. Time-of-day block in each tier alters stakes (one conditional line minimum).
8. Three `confrontation_*` labels are prose-distinct; reference chain outcome when not `"none"`.
9. `anxiety_breakdown_downtime` preserved unless Victorian pass flags idiom only.
10. Voice guides cited — no anachronistic diction in player-facing text.
11. IRL spice caps respected; no explicit anatomy beyond current tier-3 ceiling.
12. At least **one** spine callback line wired to `*_chain_outcome` (table above).
13. DAG tags intact; `py scripts/validate.py --profile changed --files "main-game/non-prod-game/game/shared/story_chains_non_canon.rpy"` passes.
14. Clean `.rpy` artifact — no planning markdown in script files.

---

## Return to

- **Agent:** `non_prod_code_agent` (API first) → `writers_room` (Workflow D — scale M → partial pool → convergent → gates 5–7)
- **Pipeline:** `revise-narrative` → on **PASS** → `implement-spec` for spine callbacks → `lead_narrative_editor` re-review
- **Gate artifacts:** `main-game/pipeline/releases/release-1-mvp/shared/gates/story_chains_gate_lead_narrative.md` (+ `.json`) — create on first gate run; psychology and Victorian gates similarly under `shared/gates/` or per-day if orchestrator prefers `day102` folder

---

## Post-gate housekeeping

1. Update `main-game/pipeline/releases/release-1-mvp/shared/synthesis/story_chains_convergent_report.md` (create if missing).
2. Sync `story_board.md` Scene Ledger — add `*_chain_outcome` flags to Global State Tracking (documentation steward or convergent).
3. Re-run route matrix path **P7** (`penance_force`) after prose land.
4. Set brief `Status: CLOSED` when sandbox + gates pass.

---

## Reference files

| File | Use |
|------|-----|
| `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy` | **Merge target** |
| `main-game/prod-game/game/story_chains.rpy` | Promotion parity check |
| `main-game/non-prod-game/game/shared/classes_non_canon.rpy` | Chain level / penance queue API |
| `main-game/non-prod-game/game/shared/story_chains_non_canon_notes.md` | Suspicion routing |
| `main-game/draft/releases/planning/story_board.md` | Window routing + adult payoff |
| `main-game/draft/releases/planning/mvp_full_review_2026-06-28.md` | Audit source |
| `main-game/pipeline/releases/release-1-mvp/qa/release1_route_matrix_test_plan.md` | P7 penance verification |
| `main-game/canon/voice_guides/*_voice_guide.md` | Voice lock |
| `.agents/rules/lead_narrative_editor.md` | Brief authority |
