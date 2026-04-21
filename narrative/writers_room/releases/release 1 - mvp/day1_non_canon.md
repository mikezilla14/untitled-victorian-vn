<!--
  FILE: day1_non_canon.md
  STATUS: Writers' Room Draft
-->

# Day 1 — "The Savoy"

## Morning — Scene 1-01: The Interview

**Setup**

`[bg]` `interior/savoy_corridor_morning`

`[mus]` `themes/threshold`

> *Cora waits outside Ms. Stern’s office. Her traveling clothes still carry the faint scent of coal smoke from the train, a stark contrast to the gleaming mahogany and polished brass of the Savoy. She rehearses her fabricated references in her head.*

---

**[choice] — "How to present herself to the exacting Ms. Stern?"**

- **Option A — "An earnest desire to learn."**
  → Cora sits perfectly straight, explaining her ambition to understand proper hotel duty.
  → `[+5 Insp, +5 Susp]`
  → `[flag]` `stern_first_impression = diligent`

- **Option B — "The invisible chambermaid."**
  → Cora keeps her eyes downcast, assuring Ms. Stern she is simply there to clean and be unseen.
  → `[+5 Corr, +0 Susp]`
  → `[flag]` `stern_first_impression = meek`

`[renpy.block_rollback()]`

## Morning — Scene 1-02: A Proper Dressing Down

**Setup**

`[bg]` `interior/savoy_lobby_stairs`

> *Cora exits the office, feeling a momentary flush of relief, only to nearly collide with a woman sweeping down the stairs. It is Ms. Vance, Sir Gideon's consort, practically vibrating with indignation.*

```
VANCE "You there! Are we expected to wait for our rooms to draw our own baths? Impertinent girl."
```

> *Before Cora can stammer an apology, Ms. Stern materializes.*

```
STERN "The staff rotate at the half-hour, Madam. Miss Hartley is not yet assigned. Your attendance will arrive presently."
```

> *Vance's fiery bravado falters momentarily. But more curious is what follows—as Sir Gideon himself descends the stairs behind her, Vance instinctively steps back, taking up a submissive, almost deferential posture, her hostility melting into compliance.*

```
CORA (internal) "Curious. She breathes fire at the staff, yet folds like paper in his shadow."
```

## Afternoon — Scene 1-03: The Laundry

**Setup**

`[bg]` `interior/servants_laundry_afternoon`

`[mus]` `ambient/servants_corridor`

> *Following Stern’s orders, Cora takes her traveling clothes to the laundry. The sharp smell of starch and hot iron cuts through the damp air. She overhears a departing maid complaining about the exacting guests.*

> *As the older maid leaves, Cora turns to find a younger girl struggling with a heavy basket. This is Missy. She is bright-eyed, undeniably attractive, and possessing a naivety that seems entirely unsuited for the city.*

```
MISSY "Oh, pardon me! You must be the new girl. I am Missy. This place... it is quite overwhelming, is it not?"
```

## Afternoon — Scene 1-04: The Corridor Tease

**Setup**

> *Cora and Missy leave the laundry together, navigating the narrow servant's corridor that runs behind the magnificent guest suites. As they pass a janitorial access door adjoining the master suite, they hear a sharp voice.*

```
GIDEON (muffled) "You will wait until you are told to rise. Is that understood?"
```

> *Cora stops. She sees Missy's face flush deep red as the younger girl instinctively gravitates toward the door, listening intently.*

---

**[choice 1] — "Where does her attention linger?" (Seeds `dom_sub_flag`)**

- **Option A — "Watch Missy listening."**
  → Cora finds her own pulse quickening as she watches Missy's breath hitch. She is captivated by the girl's vulnerability.
  → `[+5 Insp, +10 Corr]`
  → `[flag]` `dom_sub_flag = submissive`

- **Option B — "Sneak a peek into the suite."**
  → Cora risks a look through the grate. She sees Vance kneeling with Gideon's heavy hand resting on her cheek, commanding total obedience. Cora shifts, her dress brushing the doorframe and making a noise. Gideon's head turns slightly.
  → `[+15 Insp, +15 Corr, +10 Susp]`
  → `[flag]` `dom_sub_flag = dominant`

`[renpy.block_rollback()]`

**[choice 2] — "How to handle Missy?" (Seeds `missy_flag`)**

- **Option A — "Draw her away, she must be protected."**
  → Cora gently pulls Missy back from the door, a sudden maternal instinct rising. *She is too soft for this.*
  → `[+10 Insp, +0 Corr, +0 Susp]`
  → `[flag]` `missy_flag = protect`

- **Option B — "Note her fascination. A useful trait to groom."**
  → Cora smiles, realizing Missy is highly suggestible. *She could be molded into a very compliant accomplice.*
  → `[+0 Insp, +10 Corr, +0 Susp]`
  → `[flag]` `missy_flag = corrupt`

`[renpy.block_rollback()]`

## Evening — Scene 1-05: The Nightly Ink

**Setup**

`[bg]` `interior/coras_room_evening`

`[mus]` `themes/melancholy`

> *Cora sits at her small desk, pen in hand. But the ink will not flow. The pages of the scandalous manuscript she brought with her demand a continuation, yet she struggles to capture the precise heat of the day's events.*

```
CORA (internal) "I lack the necessary detail. It feels entirely inadequate."
```

## Evening — Scene 1-06: The Snooping Errand

**Setup**

`[bg]` `interior/servants_corridor_night`

> *Restless, Cora ventures into the corridor. She encounters Missy, who is nervously wringing her hands near the laundry drop.*

---

**[choice] — "How to convince Missy to enter the suite?"**

- **Option A — "Deception." (Available if Corr > 15)**
  → Cora speaks with feigned authority, claiming Ms. Stern demanded a secondary inspection of the linens. Missy immediately complies out of dutiful fear.
  → `[+15 Corr, +5 Susp, +5 Insp]`

- **Option B — "Persuasion." (Available if Insp > 15)**
  → Cora drops her voice to a conspiratorial whisper, coaxing Missy into a thrilling, improper adventure.
  → `[+15 Insp, +10 Susp, +5 Corr]`

`[renpy.block_rollback()]`

**Resolution**

`[bg]` `interior/master_suite_night`

`[mus]` `themes/temptation_understated`

> *Inside the suite, Missy's hands tremble as she sifts through the discarded clothing. She holds up an article of women's undergarments—scandalous, French-made, and hastily abandoned.*

```
CORA "I would suggest you return those precisely as you found them. Ms. Vance's musky underthings are hardly suitable for your delicate hands."
```

> *Missy gasps, her face burning, and drops them back into the pile. She did not fully comprehend what they were until Cora named them. But the damage is done; her scent, her hesitation—if anything were to go missing, the guilt would inevitably drift her way.*

```
CORA (internal) "I have what I needed. The detail. The atmosphere."
```

`[flag]` `knickers_flag_planted = True`

> **End of Day 1**
