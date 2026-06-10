# Narrative Gate — Lead Narrative Editor
# dayrdd: day100
# Release: release 1 - mvp
# Draft: narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day100_non_canon.rpy
# Reviewed: 2026-06-10
# Reference: day100_convergent_report.md, story_board.md

## Verdict

**PASS**

The rewritten promotion draft of the Day 100 Prologue is structurally excellent and fully matches the new creative specifications. The transition to a leaner, more immediate opening starts in motion with high tension and avoids dry lore dumps. The script successfully sets all required global StoryState variables and meets Cora's early-game voice lock requirements.

## Canon cross-reference

| Check | Result |
|-------|--------|
| Story board spine (labels, menus, flags) | OK — All eight labels (`day100_main` through `day100_3_arrival`) are correctly preserved and correctly jump to `day101_main`. |
| Performed Self backstory / references | OK — Cora's Wiltshire domestic service background is properly woven into her interior dialogue and the confrontation with Sir John. |
| Sir John's role and tone | OK — Sir John is presented as a quiet, authoritative figure whose social power does not need to raise its voice. |
| Choice-state integration | OK — Correctly sets `prologue_found`, `prologue_why_write`, and `prologue_holywell_posture`. |

## Stat-story alignment

- Search choices correctly apply inspiration, corruption, and suspicion stats:
  - walnut bureau search: `$ apply_effects(insp=15, corr=10)`
  - parlour entrance search: `$ apply_effects(corr=15)`
- Why Write choices correctly distribute stat effects:
  - money_home: `$ apply_effects(insp=5)`
  - cataloguer: `$ apply_effects(insp=5, corr=5)`
  - scandal_hungry: `$ apply_effects(corr=10)`
- Caught reaction choices correctly map to posture flags:
  - Lie: `careful`
  - Deflect: `eager` (`$ apply_effects(insp=5)`)
  - Submit: `desperate` (`$ apply_effects(corr=5)`)

## Implementation alignment

- **Centralized Exit Routing**: The script exits via `jump day101_main` after setting the day to 1 and time to "Morning" via the `time_manager` API, complying with the exit router contract.
- **State Management**: Uses only approved whitelisted StoryState setters (`set_prologue_found`, `set_prologue_why_write`, `set_prologue_holywell_posture`).

## Voice check

| Character | Assessment |
|-----------|------------|
| Cora (Wiltshire maid mask) | **Strict Voice Lock**. Cora's spoken lines to Sir John (`cora "I was only seeking ink, sir."`, `cora "They are my pages, sir."`, `cora "Forgive me, sir."`, `cora "I understand, sir."`) strictly respect the cap of <= 8 words per line and contain zero contractions. The gap between her hyper-literate, sensory thoughts and her simple spoken mask is beautifully executed. |
| Sir John | Sir John speaks with cold, quiet authority ("Come out, Vale."). His dialogue conveys absolute power without shouting. |

## Editorial notes (non-blocking)

1. **Adrenaline flow**:
   The transition from the tense cupboard hiding beat to the quiet caught moment works exceptionally well to establish the social geometry of the house.
2. **Spice integration**:
   The 2.8 spice rating is achieved perfectly through Cora's sensory daydream in the train carriage, reflecting the branch choices in a highly responsive manner.

## Resubmission gate

N/A — Approved for the forensic psychology gate.
