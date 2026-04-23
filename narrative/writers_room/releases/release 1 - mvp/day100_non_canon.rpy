# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes

<!--
  FILE: day100_non_canon.rpy
  STATUS: Writers' Room Draft
-->

# Prologue

## Scene P-01: The Train Journey

**Setup**

`[bg]` `interior/train_carriage_day` — Cora is seated by the window, the rolling green countryside slowly yielding to the sprawling grey smog of London.

> *The rhythm of the train lulls her into a restless slumber, memories of the countryside estate pulling her back to the day her entire world unraveled.*

## Scene P-02: The Discovery (Flashback)

**Setup**

`[bg]` `interior/country_estate_study`

`[mus]` `themes/melancholy`

> *She stands in the study of her previous benefactor, the man who had inexplicably permitted her to learn to read. A strange noise drifts from the adjoining parlour, breaking the quiet. At the very same moment, her eyes fall upon the master's desk, which lies open before her, papers scattered about in need of ordering.*

---

**[choice] — "A curious sound from the parlour, or the duty of the desk?"**

- **Option A — "Investigate the parlour."**
  → Cora presses her ear to the heavy oak door. She overhears her employer and his partner detailing their deepest, most improper desires in vivid clarity.
  → `[+15 Corr, +0 Insp]` — She experiences the reality of their lust firsthand, coloring her worldview.
  → `[flag]` `prologue_found = overheard`

- **Option B — "Continue with her duties at the desk."**
  → Cora's eyes trace the elegant, scandalous handwriting on the letters left carelessly exposed. She reads them, completely absorbed in the illicit fiction.
  → `[+10 Corr, +15 Insp]` — She discovers the power of the written word to evoke desire, drawing dark inspiration from it.
  → `[flag]` `prologue_found = read_letters`

> *In both instances, the illusion shatters. A shadow falls over her as her benefactor returns. The harsh admonishment of betrayal quickly follows, and her dismissal from the estate is absolute.*

`[renpy.block_rollback()]`

## Scene P-03: Awakening

**Setup**

`[bg]` `interior/train_carriage_day`

> *Cora jolts awake as the train whistle shrieks. The carriage rattles over the iron tracks, carrying her into the smoke.*

`[sfx]` `train_whistle`

> *Pages have spilled from her satchel onto the floorboards. She scrambles to gather them up in a panic. It is a half-written manuscript of a highly improper nature, accompanied by forged references. If anyone were to examine them, she would be ruined before she even stepped out of the station.*

```
CORA (internal) "I must be mindful. The city will afford no second chances to a chambermaid with such secrets."
```

> *She tucks the papers safely away as the brooding skyline of London looms through the soot-stained window. Her new position at the Savoy awaits, but she brings her inclinations with her.*
