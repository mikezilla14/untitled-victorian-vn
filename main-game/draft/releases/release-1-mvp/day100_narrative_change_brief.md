# Narrative Change Brief — day100
# Invoked by: lead_narrative_editor
# Scale: M
# Status: CLOSED

## Trigger

Human-approved **Option B hybrid merge** after lead narrative review of the dark-romance rewrite experiment (`narrative/draft/releases/release-1-mvp/planning/day100_non_canon_draft rewrite.rpy`).

**Keep:** Sir John dismissal exit, Savoy reference as master’s leverage, all three prologue flags, label spine, archetype seed menu, Waterloo handoff.

**Change:** Inciting scandal from Sir John / George (master–stableman) to **Lady Eleanor Wiltshire + an under-housemaid** (illicit sapphic encounter). Sir John **expels Cora at his wife’s behest** after Cora is caught trespassing with knowledge of the Lady’s ruin.

**Marketing mandate:** The live discovery beat (parlour or letters branch) must carry **elevated AO spice (~3.0–3.2)** — hotter than the prior ~2.8 daydream-only model — while remaining voyeur/reader POV, not a playable sex scene.

## Affected scope

### Labels (rewrite prose; preserve names and jumps)

| Label | Change |
|-------|--------|
| `day100_main` | Retain kinetic Wiltshire night opening. Add **Irish linguistic erasure** inner beats (Cork lilt vs flat English maid mask). Threat source: Lady may have confiscated pages, not only Sir John. |
| `day100_1_afternoon_boredom` | Reframe room as **Lady Eleanor’s private study / withdrawing room** (still use `bg_country_estate_study`). Menu copy: search bureau vs parlour for confiscated manuscript pages. **Keep** `apply_balanced_effect` profiles (`curious` / `transgressive`). |
| `day100_2_parlour_branch` | **Replace** Sir John / George overheard beat with **Lady Eleanor + under-housemaid** encounter (see Spice floor). Cora eavesdrops or glimpses through door crack / keyhole. |
| `day100_2_desk_branch` | **Replace** Sir John’s love letters with **Lady Eleanor’s scandalous letters to the under-housemaid** (or locked journal packet). **Preserve** Savoy lockbox / Strand solicitor mystery hook — thread via mixed household correspondence (Lady’s fear of husband discovering *or* Sir John’s separate London letter slipped among her papers). |
| `day100_2_reconvergence` | **Replace** Sir John–alone caught beat with **Lady-first confrontation → Sir John performs dismissal at wife’s demand**. Restore full two-menu structure. |
| `day100_3_night_daydream` | Branch-conditioned daydream reflects **Lady + housemaid** discovery (not Sir John / George). Optional **interior** False-Dawn seed (secrets as potential currency) — **no** blackmail victory, no sovereigns demanded. Posture-conditioned Holywell writing tempo blocks **must remain**. |
| `day100_3_arrival` | Retain manuscript spill at Waterloo. Accent performance beat (English country mask holds). |

### Flags / setters (unchanged values — MUST all fire)

| Setter | Values | Notes |
|--------|--------|-------|
| `story.set_prologue_found` | `"read_letters"` / `"overheard"` | Same enum; new scandal content only. |
| `story.set_prologue_holywell_posture` | `"careful"` / `"eager"` / `"desperate"` | Menu group `day100_1_afternoon_boredom_menu_2` — how Cora answers **Sir John** when caught (Lie / Deflect / Submit). |
| `story.set_prologue_why_write` | `"money_home"` / `"cataloguer"` / `"scandal_hungry"` | Menu group `day100_2_evening_flashback_menu_1` — **MUST NOT BE OMITTED**. |
| `story.set_run_archetype_seed` | `"ghost"` / `"prey"` / `"predator"` | Unchanged train menu. |

### Balance / implementation

- Use **`apply_balanced_effect(profile, intensity=...)`** on all choice stat lines — do **not** revert to raw `apply_effects(insp=..., corr=...)` except where graph already locks numeric deltas via balance profiles.
- Choice catalogue rows in `main-game/draft/releases/planning/balance/choice_catalogue.csv` and `release1_choices.csv` must remain valid after edit (regenerate graph if menu text changes but stat profiles unchanged).

### story_board rows

- Global State Tracking: `prologue_found`, `prologue_why_write`, `prologue_holywell_posture`
- Scene Ledger: Day 100 (Prologue / Tutorial) — update descriptive bullet only after gates pass (human/orchestrator)
- Spine sequence step 0: `day100_main` → Day 101 handoff

### Canon citations (non-negotiable)

| Source | Requirement |
|--------|-------------|
| `main-game/canon/cora_character_canon.md` § Breaking Point | Prologue ends in **absolute dismissal** after impropriety proximity — Cora does **not** blackmail her way out, does **not** leave triumphant. |
| `main-game/canon/cora_character_canon.md` § Voice | Speech/thought Gap; Irish erasure; ≤8 words spoken to superiors; no contractions in service register. |
| `main-game/canon/cora_character_canon.md` § False Dawn | Interior foreshadow only — she may *think* secrets have price; she does **not** collect payment in prologue. |
| `main-game/draft/releases/planning/continuity_handoff.md` § Handoff → Day 101 | Exit state must still read: dismissed, manuscript + forged references, performed maid vs inner author — update sensory callbacks after merge. |

## Narrative requirements (MUST)

### 1. Inciting scandal — Lady + housemaid

- **Lady Eleanor Wiltshire** (Lady of the house) is the compromised figure. Pair her with a **named under-housemaid** (writers pick a period-plausible name; she is a one-scene Wiltshire NPC, not a recurring cast member).
- **`overheard` branch:** Cora witnesses or overhears a **live**, high-tension intimate encounter (sapphic, transgressive, class-coded). POV stays Cora’s voyeur lens.
- **`read_letters` branch:** Cora reads Lady Eleanor’s explicit correspondence to the same housemaid (or journal pages). Letters must feel as hot as the overheard branch in different medium.
- **Remove** Sir John / George sexual scandal entirely from both branches.

### 2. Spice floor (marketing)

| Zone | Target | Rules |
|------|--------|-------|
| Live discovery (`day100_2_parlour_branch`, `day100_2_desk_branch`) | **3.0–3.2** | Sensory, power, hypocrisy, breath/skin/fabric; Cora’s arousal + tactical observation. **No** step-by-step anatomical porn; **no** player-controlled participation. |
| Train daydream (`day100_3_night_daydream`) | **2.8–3.0** | Echo branch choice; posture-conditioned Holywell tempo lines preserved. |
| Reconvergence (`day100_2_reconvergence`) | **≤2.5 live** | Tension and class geometry; Sir John may show disarray but not a second explicit sex beat. |

Reference donor prose for heat and Irish erasure: `narrative/draft/releases/release-1-mvp/planning/day100_non_canon_draft rewrite.rpy` (do **not** import blackmail exit, Eleanor/George stableman, or long spoken demands).

### 3. Reconvergence beat — Lady’s behest, Lord’s dismissal

Required dramatic sequence (adjust staging, not outcome):

1. Cora is caught trespassing with **her confiscated manuscript pages** in play (Lady may hold them, or Sir John enters with them).
2. **Lady Eleanor** reacts first: terror, class venom, optional **Irish slur** (“guttersnipe” / equivalent period insult) triggering Cora’s **linguistic vigilance** inner beat — she must not slip into Cork register in spoken reply.
3. Lady insists Cora be removed **immediately** — social death if the maid breathes a word; Lady’s ruin stakes (children, name, exile) visible in her panic.
4. **Sir John** enters or speaks with cold authority: validates wife’s judgment, performs **master’s dismissal** — not Cora’s victory. Example shape (not verbatim lock): *“My wife is correct. Pack your trunk. You leave on the morning train.”*
5. Sir John offers **Savoy reference under threat** (blacken name / gutter) — same leverage geometry as current promoted draft.
6. Cora’s spoken lines to Sir John: **≤8 words**, no contractions (`cora_voice_guide.md` Day 0 band).

### 4. Menus — full restoration

**Menu A — Caught posture** (`day100_1_afternoon_boredom_menu_2`):

| Choice | Posture | Balance profile (keep existing) |
|--------|---------|----------------------------------|
| Lie — draft / innocent search | `careful` | none on flag-only arm |
| Deflect — pages are mine | `eager` | `observant` minor |
| Submit — mercy | `desperate` | `obedient` minor |

**Menu B — Why write** (`day100_2_evening_flashback_menu_1`) — **mandatory**:

| Choice | Flag | Balance profile |
|--------|------|-----------------|
| For the shillings home | `money_home` | `safe` minor |
| To catalogue what power hides | `cataloguer` | `curious` minor |
| Because scandal tastes better than porridge | `scandal_hungry` | `transgressive` standard |

Sir John (or Lady, then Sir John) must pose the “why this filth?” challenge so Menu B lands naturally.

### 5. Donor material to merge

From dark-romance rewrite experiment — **interior only** unless voice-checked:

- Cork lilt vs English maid mask (`day100_main`, reconvergence, Waterloo).
- Lady’s **gendered ruin** stakes (inner observation: a Lady’s reputation is total; a Lord’s is manageable — foreshadows False Dawn without prologue triumph).
- Darker sensory diction in discovery branches (within spice floor).
- Posture-conditioned daydream lines (already in promoted draft — re-tune imagery to new scandal).

### 6. Mystery hook — preserve

Desk branch must retain a path to **Savoy locked box / Strand solicitor** clue (current promoted line or equivalent). May sit in Sir John’s letter among Lady’s papers or in household ledger stack — writers choose least contrived placement.

### 7. Artifact hygiene

- Deliver clean `.rpy` to `main-game/non-prod-game/game/days/day100_non_canon.rpy` — no markdown wrapper, no editorial `<details>`, no non-English typos in player text.
- Preserve `[DAG_*]`, `[STATE]`, `[CHOICE]`, `[BEAT]`, `[ASSET]` markers.

## Out of scope

- Changing dismissal outcome to blackmail, sovereign payment, or Cora-led negotiation.
- Replacing Sir John as the speaking authority who dismisses and threatens reference.
- Adding new StoryState flags or labels beyond the existing Day 100 spine.
- Canon file edits (`main-game/canon/**`) — if Lady Eleanor requires canon entry, flag `NEEDS HUMAN CONFIRMATION` in convergent report; do not write to canon.
- Day 101+ prose changes (continuity handoff update only after Day 100 gates pass).
- Promoting to `main-game/prod-game/` (separate `promote-day` step after gates).

## Personas (M)

Run **partial divergent pool**, then convergent merge:

| Persona | Focus |
|---------|-------|
| **erotic** | Lady + housemaid discovery branches; spice floor 3.0–3.2; daydream echo |
| **class** | Lady’s behest vs Sir John’s performed authority; dismissal threat; maid mask speech |
| **tension** | Night crawl, caught sequence, Waterloo spill |
| **thematic** | Hypocrisy sermon vs secret appetite; Irish erasure; False Dawn interior seed |
| **mystery** | Savoy lockbox / Strand thread in desk branch |

Skip humour persona.

## Scene architecture sketch (writers’ starting point)

```
day100_main (night crawl, pages missing, Irish vigilance)
  → day100_1_afternoon_boredom (search Lady's rooms)
       ├─ bureau → day100_2_desk_branch (Lady's letters + mystery hook)
       └─ parlour → day100_2_parlour_branch (overheard Lady + housemaid, spice 3.0+)
  → day100_2_reconvergence
       Lady terror → demands expulsion
       Sir John → posture menu → why-write menu → dismissal + Savoy threat
  → day100_3_night_daydream (archetype seed + branch daydream)
  → day100_3_arrival (Waterloo spill, accent mask, jump day101_main)
```

## MUST FIX checklist (gate resubmission)

1. Lady + housemaid scandal in **both** `prologue_found` branches; Sir John / George sex scandal **removed**.
2. Reconvergence ends in **Sir John dismissal at Lady’s behest** — not blackmail (`cora_character_canon.md`).
3. **`prologue_why_write` menu present** with all three arms and setters.
4. Spoken `cora` lines to Sir John: **≤8 words**, no contractions.
5. Live discovery spice **≥3.0** marketing floor; bounded voyeur/reader POV.
6. **`apply_balanced_effect`** on stat choices; no orphan raw stat lines.
7. Savoy / Strand mystery hook **present** in desk branch.
8. Irish erasure beats in crawl, reconvergence, and/or Waterloo.
9. Clean `.rpy` artifact; no wrapper prose or encoding errors.

## Return to

- **Agent:** `writers_room` (Workflow D — scale M → partial pool → convergent → gates 5–7)
- **Pipeline:** `revise-narrative` → on narrative/psychology/historical **PASS** → `non_prod_code_agent` (`implement-spec`) wraps verbatim into non-prod if needed → `lead_narrative_editor` re-review → `promote-day` when human requests prod sync

## Post-gate housekeeping (orchestrator / convergent)

1. Update `main-game/pipeline/releases/release-1-mvp/days/day100/synthesis/day100_convergent_report.md` (`Pass: editor-revision-1`).
2. Update `continuity_handoff.md` § Handoff → Day 101 exit imagery (Lady scandal, dismissal at wife’s behest, Irish mask).
3. Invalidate prior gate verdicts (`day100_gate_*.md`) — re-run full gate chain.
4. Set brief `Status: CLOSED` when prod/non-prod aligned and gates pass.

## Reference files

| File | Use |
|------|-----|
| `main-game/non-prod-game/game/days/day100_non_canon.rpy` | Current promoted baseline |
| `narrative/draft/releases/release-1-mvp/planning/day100_non_canon_draft rewrite.rpy` | Donor (interior heat, Irish erasure — not structure) |
| `main-game/pipeline/releases/release-1-mvp/days/day100/specs/day100_*_spec.rpy` | Persona seeds — **rewrite specs** for new scandal geometry |
| `main-game/canon/cora_character_canon.md` | Exit + voice lock |
| `main-game/draft/releases/planning/story_board.md` | Flag spine |
