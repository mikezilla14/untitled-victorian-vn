<!--
  FILE: day2_non_canon.md
  STATUS: Writers' Room Draft
-->

# Day 2 — "Missing Articles"

## Morning — Scene 2-01: The Dry Pen

**Setup**

`[bg]` `interior/coras_room_morning`

`[mus]` `themes/melancholy`

> *Cora sits at her desk, staring at a blank page. The events of the previous evening swirl in her mind—Missy's flushed face, the intimate glimpse of Sir Gideon's undeniable authority—yet the ink remains trapped in the pen. She is missing the narrative thread that elevates common smut into something Mr. Holywell will purchase.*

```json
{
  "beat_id": "2-01",
  "location": "interior/coras_room_morning",
  "setup": "Cora struggles to find the inciting spark for her manuscript, reflecting on the events that brought her to the Savoy.",
  "choices": [
    {
      "choice_text": "Lean into the memory of Missy's innocent fascination.",
      "consequence": "Cora finds herself intrigued by the corruption of the pure, drawing dark inspiration.",
      "stat_changes": {
        "Insp": 10,
        "Susp": 0,
        "Corr": 10
      }
    },
    {
      "choice_text": "Focus on the raw power dynamic witnessed in the upper suite.",
      "consequence": "Cora channels the memory of absolute authority into a sharper, more dominant prose style.",
      "stat_changes": {
        "Insp": 15,
        "Susp": 0,
        "Corr": 5
      }
    }
  ],
  "end_state": "The writing session is abruptly interrupted by a sharp knock at the door."
}
```

---

**[choice] — "Where does her mind wander?"**

- **Option A — "Missy's fascination."**
  → Cora's thoughts drift to the younger girl's trembling hands. The idea of molding such naivety is intoxicating.
  → `[+10 Corr, +10 Insp]`

- **Option B — "The power of the master suite."**
  → Cora recalls Gideon's low, commanding tone. That level of absolute assurance is a potent muse.
  → `[+5 Corr, +15 Insp]`

`[renpy.block_rollback()]`

## Morning — Scene 2-02: The Accusation

**Setup**

`[sfx]` `loud_knocking`

> *A sharp rapping at the door breaks Cora from her reverie. She opens it to find Ms. Stern, her face flushed with uncharacteristic color. Behind her stands Missy, trembling on the verge of tears.*

```
STERN "Miss Hartley. You and Missy were the only staff operating in the upper corridor last evening. You will accompany me to the master suite at once."
```

`[bg]` `interior/master_suite_morning`

> *Inside the suite, Ms. Vance is incandescent with rage, though curiously vague about the specifics of her grievance.*

```
VANCE "I will not tolerate thieves! The item was placed precisely here last night. It is gone. I demand you search them both this instant!"

STERN "Madam, if you would simply describe the missing item, my staff could attempt to locate it. Perhaps it was sent down with the morning linens in error."

VANCE "It was not sent down with the linens! It is... a personal garment of significant worth!"
```

> *Before the shouting can escalate, the inner door opens. Sir Gideon steps into the room, impeccably dressed. His presence instantly lowers the temperature of the air.*

```
GIDEON "Enough."
```

> *He does not raise his voice. He does not need to.*

```
GIDEON "My dear, you are evidently mistaken. You must have misplaced it yourself. We will speak no more of this triviality. Ms. Stern, I apologize for the disruption. You are dismissed."
```

> *Vance's face is a portrait of wounded pride, but she remains entirely silent. Stern nods stiffly, though she is visibly displeased with Vance's bullying, and signals her staff to leave.*

## Morning — Scene 2-03: The Revelation

**Setup**

`[bg]` `interior/servants_corridor_morning`

`[mus]` `ambient/servants_corridor`

> *Safely out of earshot, Cora turns to Missy with a conspiratorial glance.*

```
CORA "Did you truly take them, then? After I expressly told you to leave them be?"

MISSY "No! I swear it, Cora! I dropped them the moment you spoke. I would never—oh, what if they dismiss us?"

CORA "Hush. I believe you. Return to your duties before Ms. Stern's temper flares anew."
```

> *Cora returns briefly to her own quarters. She reaches into the deep pocket of her apron, and her fingers brush against fine silk and lace.*
> *She had slipped them away while Missy was recoiling in embarrassment. A necessary souvenir.*

```
CORA (internal) "I suppose I am a thief. How very scandalous."
```

## Afternoon — Scene 2-04: The Volunteer

**Setup**

`[bg]` `interior/servants_laundry_afternoon`

> *Cora is sorting the heavy linens when Ms. Stern appears in the doorway.*

```
STERN "The lady in the master suite requires assistance tracing a misplaced article. Frankly, I will not subject Missy to another tirade. Will you attend to it, Miss Hartley, or shall I send Ellen?"
```

```json
{
  "beat_id": "2-04",
  "location": "interior/servants_laundry_afternoon",
  "setup": "Ms. Stern asks for a volunteer to face Ms. Vance's lingering wrath. Cora secretly holds the missing item.",
  "choices": [
    {
      "choice_text": "Volunteer to attend to Ms. Vance.",
      "consequence": "Cora puts herself in the center of the conflict, bringing the stolen item with her.",
      "stat_changes": {
        "Insp": 10,
        "Susp": 10,
        "Corr": 5
      }
    },
    {
      "choice_text": "Allow Ellen to face the wrath.",
      "consequence": "Cora remains safely in the laundry, missing a crucial encounter but lowering her risk.",
      "stat_changes": {
        "Insp": 0,
        "Susp": -5,
        "Corr": 0
      }
    }
  ],
  "end_state": "The path branches based on whether Cora enters the suite or avoids it."
}
```

---

**[choice] — "Does Cora step into the fire?"**

- **Option A — "Volunteer."**
  → Cora nods dutifully. *"I will handle it, Ms. Stern. Do not worry."*
  → `[+5 Corr, +10 Insp, +10 Susp]`
  → `[flag]` `volunteered_for_vance = True`
  → *Transitions to Scene 2-05.*

- **Option B — "Send Ellen."**
  → Cora keeps her head down. She has the article; producing it now might be far too perilous.
  → `[+0 Corr, +0 Insp, -5 Susp]`
  → `[flag]` `volunteered_for_vance = False`
  → *Transitions directly to Scene 2-06.*

`[renpy.block_rollback()]`

## Afternoon — Scene 2-05: The Discovery (If Volunteered)

**Setup**

`[bg]` `interior/master_suite_afternoon`

`[mus]` `ambient/upper_corridor_tension`

> *Cora enters the suite. Vance spins around, her eyes narrowing as she recognizes Cora from the morning's humiliation.*

```
VANCE "You. You were the one pawing through my quarters yesterday. I know you hide it to mock me."
```

> *The item is in Cora's possession. She can resolve this, but the method carries immense risk.*

```json
{
  "beat_id": "2-05",
  "location": "interior/master_suite_afternoon",
  "setup": "Cora must decide how to 'find' the missing knickers without fully exposing her own theft.",
  "choices": [
    {
      "choice_text": "Produce it from her own person, feigning innocence.",
      "consequence": "Vance recognizes the impossibility and becomes enraged, but Cora maintains the facade.",
      "stat_changes": {
        "Insp": 5,
        "Susp": 20,
        "Corr": 15
      }
    },
    {
      "choice_text": "'Discover' it hidden in the back of the wardrobe.",
      "consequence": "Cora pretends it was misplaced by another maid, humiliating Vance further.",
      "stat_changes": {
        "Insp": 15,
        "Susp": 5,
        "Corr": 10
      }
    }
  ],
  "end_state": "Sir Gideon intervenes to silence Vance's outburst."
}
```

---

**[choice] — "How does Cora produce the missing article?"**

- **Option A — "From her own pocket."**
  → Cora calmly reaches into her apron and holds it out. *"Is this the item you seek, Madam? It appears it was inadvertently mixed with my dusting cloths."* Vance turns entirely pale; she knows she checked Cora's person earlier. The sheer brazenness leaves her sputtering.
  → `[+15 Corr, +5 Insp, +20 Susp]`

- **Option B — "From the wardrobe."**
  → Cora opens the wardrobe and swiftly drops the silk into a dark corner, only to pull it out a second later. *"Madam, it seems to have slipped behind your travel trunks."* Vance explodes, insisting it had no right to be there.
  → `[+10 Corr, +15 Insp, +5 Susp]`

`[renpy.block_rollback()]`

> *Before Vance can strike her, Gideon appears from the dressing room.*

```
GIDEON "You will cease this unbecoming display immediately."
```

> *His voice is like a whip cracking in the quiet room. Vance freezes, instantly brought to heel. The venom drains from her posture, replaced by a rigid, terrified obedience.*

```
GIDEON "Miss Hartley. You have done quite enough. You are dismissed."
```

> *Cora bows and steps out into the corridor. As she closes the door, she hears the distinct sound of a sharp slap, followed by Vance's muffled whimper. The discipline has begun.*

```
CORA (internal) "He commands her completely. What an extraordinarily dangerous man."
```

## Evening — Scene 2-06: Stern's Warning (Conditional Gate)

**Setup**

`[bg]` `interior/coras_room_evening`

> *If Cora's Suspicion is dangerously high after the day's events, she receives a visitor.*

*Note: This scene only plays if [Suspicion > 30]. Otherwise, skip to Scene 2-07.*

```
STERN "You walk a very fine line, Miss Hartley. There have been disruptions since your arrival. I run a respectable establishment. Further irregularities will simply not be tolerated."
```

> *Cora apologizes formally. The warning is clear: she must temper her curiosity, or risk losing her position entirely.*

## Evening — Scene 2-07: The First Chapter

**Setup**

`[bg]` `interior/coras_room_evening`

`[mus]` `themes/temptation_understated`

> *The day's events have provided exactly the fuel Cora required. The arrogance of the consort. The absolute dominion of the master. The trembling fear of the innocent.*

> *She draws her pen to the paper. This time, the ink flows like wine. She writes of power, of surrender, of the thrill of being entirely undone by a superior will. The first chapter of her manuscript is finally taking shape.*

```
CORA (internal) "It is finished. Tomorrow, I must find a way to submit this to Mr. Holywell. My new life truly begins."
```

> **End of Day 2**
