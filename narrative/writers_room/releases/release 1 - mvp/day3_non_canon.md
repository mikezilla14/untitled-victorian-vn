<!--
  FILE: day3_non_canon.md
  STATUS: Writers' Room Draft — awaiting Lead Narrative Editor review
  BEAT SCHEMA: Setup → Player Choice → Consequence → Stat Delta
  CANON CONFLICTS: None detected. Day 2 Evening resolved Gideon/consort suspicion arc and Cora's first deadline.
  SEEDED FLAGS CONSUMED: dom_sub_flag (Day 1 tease corridor), missy_flag (protect/corrupt), knickers_flag (in Cora's possession)
  SEEDED FLAGS PRODUCED: manuscript_submitted (bool), gideon_trust_flag (low/medium/high), missy_bond_flag (elevated post-confrontation)
  AUTHOR NOTE: The explicit "chapter tease" payoff lives in the Evening beat.
-->

# Day 3 — "The Ink Dries"

---

## Morning — Scene 3-01: "The Weight of What Was Written"

**Setup**

`[bg]` `interior/coras_room_morning` — grey London light through thin curtains. Cora's writing desk is a ruin of crumpled pages and one candle stub burned to the brass. She sits at the edge of the bed in her shift, staring at a sealed envelope on the desk.

`[mus]` `themes/quiet_dread`

> *The chapter is finished. She can feel it the way you feel a tooth just pulled — the strange hollow relief that is also just a new kind of ache. She has written one true thing. Whether it is a magnificent or a ruinous thing she cannot yet say.*

---

**Scene 3-01a — "The Envelope"**

```
CORA (internal) "Four pages. Four pages of the most ungodly accurate
               description of power and want that I have ever—"

               [She stops herself.]

CORA (internal) "Professional. Detached. It is commerce, nothing more."

               [She is lying, of course.]
```

> *The deadline for the first submission to Mr. Holywell is this afternoon. She had agreed to a drop-box at the back of Sweetings on Cheapside — discreet, impersonal, the kind of arrangement a lady disappears into and surfaces from without explanation.*

---

**[choice] — Does Cora read it back before sealing it?**

> `[sfx]` gentle rustle of paper

- **Option A — "She reads it."**
  → Cora opens the envelope and reads her own work aloud (internal monologue, restrained but vivid).
  → `[flag]` `manuscript_reread = True`
  → `[+10 Corruption, +8 Insp]` — she lingers on the corridor scene. The prose is good. She knows it.
  → Transition: Scene 3-01b (Missy knocks while Cora is mid-sentence)

- **Option B — "She seals it without looking."**
  → Cold discipline. She is not a woman who second-guesses herself before breakfast.
  → `[flag]` `manuscript_reread = False`
  → `[+5 Insp, -5 Corruption]` — professional remove.
  → Transition: Scene 3-01b

`[renpy.block_rollback()]`

---

**Scene 3-01b — "Missy at the Door"**

| Element | Value |
|---------|-------|
| `[bg]` | `interior/coras_room_morning` |
| `[char]` | Cora, Missy (doorway, apron slightly crooked, worried eyes) |
| `[mus]` | `themes/quiet_dread` fades to `ambient/servants_corridor` |

> *Missy is terrible at keeping things to herself. It is written all over her face from the moment Cora opens the door.*

```
MISSY  "Cora— I need to— I have to tell you something before we go downstairs."

CORA   "Good morning to you as well."

MISSY  "I'm— yes, sorry— good morning. But Cora, she knows. Ms. Vance.
       Ellen told me — Ms. Vance told Ms. Stern that she wants it to be
       us specifically who turns down her room today. Specifically us."
```

> *Cora feels the envelope in her apron pocket like a live coal.*

```
CORA (internal) "She wants us in that room. Which means she either knows,
               or suspects, or—"

               [She looks at Missy properly for the first time this morning.]

CORA (internal) "—or she simply wants an audience for whatever she's
               planning."
```

---

**[choice] — How does Cora handle Missy?**

*Branched by `missy_flag` from Day 1.*

**If `missy_flag = protect`:**

- **Option A — "Keep her out of it." (soft lock if Corruption > 60)**
  → Cora tells Missy to volunteer for laundry and claim a headache. Warm, protective, borderline maternal.
  → `[+10 Insp, +5 Susp]` — Stern will notice the avoidance.
  → `[flag]` `missy_in_room_day3 = False`

- **Option B — "Tell her the truth — that she probably did take them."**
  → Honest, not cruel. Missy's fingermarks aren't exactly reassuring evidence.
  → `[+8 Insp, +10 Susp]` — Missy, rattled, reads as guilty around Stern.
  → `[flag]` `missy_in_room_day3 = True` (Missy insists on coming to prove innocence)

**If `missy_flag = corrupt`:**

- **Option A — "Use her." (unlocked)**
  → Cora suggests they go together; if anything goes sideways, Missy should look confused. She's very good at that, after all. A thin smile. Missy stiffens — not entirely sure whether she's being flattered or handled.
  → `[+15 Corruption, +5 Insp]`
  → `[flag]` `missy_in_room_day3 = True`

- **Option B — "Send her away."**
  → No liability needed.
  → No stat delta.
  → `[flag]` `missy_in_room_day3 = False`

`[renpy.block_rollback()]`

---

## Morning — Scene 3-02: "The Vance Room (Again)"

**Setup**

`[bg]` `interior/master_suite_morning` — Vance at the vanity in a heavy peignoir, appraising Cora in the mirror rather than turning to face her.

`[mus]` `ambient/upper_corridor_tension`

> *The room still smells faintly of Gideon's tobacco and something warmer underneath. Cora has been in this room three times. Each time it gives up something new.*

---

**Scene 3-02a — "The Vance Audit"**

```
VANCE  [via mirror, not turning]
       "You're the one who found it."

       [Silence.]

CORA   "Ma'am?"

VANCE  "The item. Yesterday. You produced it from thin air while I was
       ready to have the lot of you dismissed. I find that very interesting.
       Sir Gideon asked me to leave it as it lay. And yet."
```

---

**[choice] — How does Cora respond?**

*Influenced by `dom_sub_flag`.*

- **Option A — "Deflect with deference."**
  → *"I simply thought it may have fallen, ma'am."*
  → `[+5 Susp, +5 Insp]` — neutral. Vance files it.

- **Option B — "Hold her gaze in the mirror." (Unlocked: `dom_sub_flag = dominant`)**
  → Cora doesn't look away. Doesn't say anything confrontational. Just doesn't flinch. Vance is first to return to her wrists.
  → `[+10 Insp, +10 Corruption, +15 Susp]`
  → `[flag]` `vance_noticed_cora = True`

- **Option C — "Sympathise." (Unlocked: `dom_sub_flag = submissive`)**
  → *"It must have been a frightful morning, ma'am."* Genuine. Unexpected. Vance's eyes flicker with something that isn't contempt.
  → `[-10 Susp, +8 Insp]`
  → `[flag]` `vance_thaw = True`

`[renpy.block_rollback()]`

---

**Scene 3-02b — "Gideon Enters"**

| Element | Value |
|---------|-------|
| `[char]` | Gideon (morning dress, unhurried, cataloguing look) |
| `[sfx]` | door latch, footsteps on carpet |

> *He is the kind of man who walks into a room without changing his pace to acknowledge its current inhabitants. The room simply adjusts.*

```
GIDEON [to Vance, barely]
       "We have a luncheon at two."

       [He glances at Cora. Not unfriendly. Not warm. A cataloguing look.]

GIDEON "Have you been properly settled in, Miss—?"

CORA   "Hartley, sir. Yes, thank you."

GIDEON "Good."

       [He picks up yesterday's newspaper. He has clearly already read it.
       He is not reading it now either.]
```

---

**[choice] — Does Cora take the opportunity?**

- **Option A — "Keep her head down."**
  → Finishes work, excuses herself. Clean. Safe.
  → `[-5 Susp]` — unremarkable.

- **Option B — "Ask after Sir Gideon's requirements for the room."**
  → Framed as professional diligence. His answer: terse, precise, revealing.
  → `[+5 Susp, +10 Insp]`
  → `[flag]` `gideon_spoken_to = True` (expands Gideon dialogue tree, Day 4+)

`[renpy.block_rollback()]`

---

## Afternoon — Scene 3-03: "The Drop"

**Setup**

`[bg]` `exterior/cheapside_alley` — narrow, smelling of fish and industry. A lacquered postbox on the wall of Sweetings, partially obscured by a delivery crate.

`[mus]` `themes/threshold`

> *This is the part she did not think about while writing it. The actual giving of it over. The manuscript was hers alone until this moment. Now she is about to hand it to the city and the city is not particularly kind to women who write certain kinds of things.*

---

**[choice] — "Does Cora hesitate?"**

- **Option A — "She posts it without ceremony."**
  → The envelope drops. She does not watch it fall.
  → `[+15 Insp]`
  → `[flag]` `manuscript_submitted = True`
  → `[renpy.block_rollback()]`

- **Option B — "She reads the first line one more time."**
  → Opens it. Just the first line. Then seals and posts it.
  → `[+20 Insp, +10 Corruption]` — she is no longer pretending this is commerce.
  → `[flag]` `manuscript_submitted = True`
  → `[renpy.block_rollback()]`

> *The slot clicks shut. London continues, entirely indifferent.*

```
CORA (internal) "Right, then."
```

---

## Afternoon — Scene 3-04: "Stern's Ledger"

**Setup**

`[bg]` `interior/sterns_office` — spare, immaculate, lavender water and ink.

```
STERN  [not looking up]
       "You left the premises during your afternoon rest hour."

CORA   "I had an errand, Ms. Stern."

STERN  "I am aware you had an errand, Miss Hartley. I am asking whether
       you intend to make a habit of it."
```

---

**[choice] — How does Cora handle Stern?**

*Gated by current Suspicion level.*

- **Option A — "Transparency." (Gated: Susp < 40)**
  → Posted a letter, family matter, won't repeat without prior arrangement.
  → `[-10 Susp, +5 Insp]`
  → `[flag]` `stern_trust_medium = True`

- **Option B — "Flattery." (Always available)**
  → Admires aloud that Stern always knows where everyone is. Then defers on the errand.
  → `[+5 Susp, -5 Insp]` — Stern is not flattered. She is observed.

- **Option C — "Weather it." (Gated: Susp > 60)**
  → Can't afford to give Stern more material. One apology. Let her dismiss.
  → `[+5 Susp]` — the passivity reads as guilt.

`[renpy.block_rollback()]`

```
STERN  [finally looking up]
       "I have had word from Sir Gideon's secretary. The party will be
       extending their stay by four additional days. You'll be working
       the upper floor assignment through the week."
```

> *It is not a reward. It is not a punishment. With Ms. Stern, Cora is learning, the two are occasionally identical.*

---

## Evening — Scene 3-05: "The Reply" *(Writing Mechanic Payoff Gate)*

**Setup**

`[bg]` `interior/coras_room_evening`

`[mus]` `themes/temptation_understated`

> *A small sealed card. No return. No salutation.*

```
CORA (internal) [reading, barely audible]
               "Your material shows promise. The restraint is elegant
                but costs you in heat. The publisher's market has a
                particular appetite this season. One more chapter,
                twelve days. Shock me."
```

---

**⚙️ MECHANIC — WRITING GATE CHECK**

| Resource | Required |
|----------|----------|
| Inspiration | ≥ 40 |
| Corruption | ≥ 30 |

→ **Both met:** unlock Scene 3-05a (Chapter 2 draft)
→ **Either unmet:** lock to Scene 3-05b (the dry spell)

---

**Scene 3-05a — "Chapter Two" (Gate Open)**

| Element | Value |
|---------|-------|
| `[char]` | Cora (nightgown, dishevelled, flush layer active) |
| `[mus]` | `themes/temptation_understated` — build |

> *She writes using names she does not own and perhaps a room she has stood in and a hand she caught only at the corner of her vision. The character she has written — she didn't plan for her. She arrived as an afterthought and wouldn't leave. She has Missy's wide eyes and Vance's arrogance and some quality Cora is carefully not naming yet.*

---

**[choice] — Which scene does Cora write?**

*Seeded by `dom_sub_flag`.*

**If `dom_sub_flag = dominant`:**
- **Option A — "The instructor."** A scene of careful, deliberate instruction. A woman who knows exactly what she wants and the exact, patient way she intends to take it.
  → `[+25 Corruption, +20 Insp]`
  → `[flag]` `manuscript_tone = dominant`

**If `dom_sub_flag = submissive` OR free choice:**
- **Option B — "The penitent."** A scene of surrender that is entirely voluntary — someone walking into a room knowing what is going to happen and going anyway.
  → `[+20 Corruption, +25 Insp]`
  → `[flag]` `manuscript_tone = submissive`

`[renpy.block_rollback()]`

> *She seals the new pages without reading them back. She learned that lesson this morning.*

```
CORA (internal) "Twelve days."

               [The candle gutters.]

CORA (internal) "Right, then."
```

`[mus]` `themes/temptation_understated` — resolve. Fade to black.

---

**Scene 3-05b — "The Dry Spell" (Gate Closed)**

> *She sits for an hour. The page stays white. She knows what she saw. She knows what she felt. But knowing a thing and being able to write it are separate problems entirely.*

```
CORA (internal) "Tomorrow."
```

`[mus]` `ambient/room_at_night`

> **📌 PLAYER NOTE:** The writing gate is not cleared. Revisit Day 3 choices or reload to gather more Inspiration/Corruption before attempting again. Eleven days until deadline.

`[flag]` `chapter2_deferred = True`

---

## Day 3 — Flags & Stat Summary

| Flag | Set By | Effect Forward |
|------|--------|---------------|
| `manuscript_submitted` | Scene 3-03 | Unlocks Holywell contact chain, Day 4+ |
| `manuscript_reread` | Scene 3-01a | Mild corruption flavour in Day 4 |
| `missy_in_room_day3` | Scene 3-01b | Determines Missy's Vance encounter, Day 4 |
| `vance_noticed_cora` | Scene 3-02a Option B | Unlocks Vance private encounter, Day 5+ |
| `vance_thaw` | Scene 3-02a Option C | Unlocks gentler Vance arc |
| `gideon_spoken_to` | Scene 3-02b Option B | Expands Gideon dialogue tree |
| `stern_trust_medium` | Scene 3-04 Option A | Unlocks Stern intel/protection event |
| `manuscript_tone` | Scene 3-05a | Seeds Chapter 3 framing |
| `chapter2_deferred` | Scene 3-05b | Forces Day 4 re-attempt gate |

### Stat Deltas (Maximum possible)

| Stat | Max Gain | Max Loss |
|------|----------|----------|
| Inspiration | +91 | -5 |
| Corruption | +75 | -5 |
| Suspicion | +45 | -25 |

---

## Assets Checklist — Day 3

### Backgrounds
- [ ] `interior/coras_room_morning` (variant: desk_closeup)
- [ ] `exterior/cheapside_alley`
- [ ] `interior/sterns_office`
- [ ] `interior/coras_room_evening` (variant: desk_lamp)

### Music
- [ ] `themes/quiet_dread`
- [ ] `themes/threshold`
- [ ] `themes/temptation_understated`
- [ ] `ambient/servants_corridor`
- [ ] `ambient/upper_corridor_tension`
- [ ] `ambient/office_quiet`
- [ ] `ambient/room_at_night`

### Character Sprites (new states required)
- [ ] Cora — shift/tired, nightgown/flush, outdoor dress
- [ ] Missy — doorway/worried
- [ ] Vance — peignoir/back-to-camera (mirror reflection variant)
- [ ] Gideon — morning dress/cataloguing
- [ ] Stern — at desk/ledger; looking up variant
