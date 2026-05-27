# Convergent Decision Report — day100
# Release: Release 1 - MVP
# Pass: initial
# Personas considered: thematic, tension, class, mystery, erotic
# Draft output: narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day100_non_canon.rpy
# Spec inputs: narrative/pipeline/releases/release-1-mvp/day100_*_spec.rpy

## 1. Considered (inventory)
| Persona | Spec file | Labels / beats reviewed | Notes |
|---------|-----------|-------------------------|-------|
| thematic | day100_thematic_spec.rpy | `day100_main`, `day100_2_discovery_flashback`, `day100_3_awakening` | Provided literary Wiltshire vs London smog contrasts. |
| tension | day100_tension_spec.rpy | `day100_2_parlour_branch`, `day100_3_awakening` | Enhanced the sensory adrenaline of the hallway eavesdropping and satchel panic. |
| class | day100_class_spec.rpy | `day100_2_discovery_flashback` | Added the social distance of Sir John and the dismissal scene's threat dynamics. |
| mystery | day100_mystery_spec.rpy | `day100_2_desk_branch` | Elaborated the elegant letters' content and hidden lockbox hooks. |
| erotic | day100_erotic_spec.rpy | `day100_main`, `day100_2_parlour_branch`, `day100_2_desk_branch` | Injected sensory, physical awareness, illicit intimacy, and master shame. |

## 2. Included (merged into draft)
| Persona | Source (spec label / line) | Target (draft label) | What changed (1 line) |
|---------|---------------------------|----------------------|------------------------|
| thematic | day100_thematic_spec:12 | `day100_main` | Wiltshire green fields vs London soot aesthetic. |
| class | day100_class_spec:28 | `day100_2_discovery_flashback` | Rationale of Sir John allowing a housemaid to read and treating her as walking furniture. |
| tension | day100_tension_spec:42 | `day100_2_parlour_branch` | Raw, panting sensory pacing of George and Sir John's voices. |
| mystery | day100_mystery_spec:51 | `day100_2_desk_branch` | Content of Sir John's forbidden love letter and its Strand / Savoy lockbox clue hook. |
| tension | day100_tension_spec:82 | `day100_3_awakening` | Panic of gathering the manuscript pages and forged reference on the floor under the passenger's gaze. |
| erotic | day100_erotic_spec:10 | `day100_main` | Close, humid third-class atmosphere and physical confinement. |
| erotic | day100_erotic_spec:47 | `day100_2_parlour_branch` | George's physical intimacy dialogue and Cora's physiological reaction. |
| erotic | day100_erotic_spec:57 | `day100_2_desk_branch` | Sensory, skin-focused desire in Sir John's open letter. |
| erotic | day100_erotic_spec:67 | `day100_2_reconvergence` | Sir John's physical state of disarray (loose collar, grey breathing, shame). |

## 3. Cut (not in draft)
| Persona | Idea / beat | Rationale | Disposition (parked / rejected) |
|---------|-------------|-----------|----------------------------------|
| thematic | Prolonged country estate history | Slowed down the prologue pace; need to get to the Savoy quickly. | Rejected |
| class | Dialogue with fellow Wiltshire maid | Added extra characters that distract from Cora's internal isolation. | Rejected |
| tension | Conductor inspecting her ticket | Created false urgency about ticket-loss when the true anxiety is the manuscript. | Rejected |
| mystery | Cryptic lock code in the letter | Too early to establish mechanical lockbox lock codes; keep focus on illicit desires. | Parked |

## 4. Structural & canon decisions
- **Spine preserved / altered:** Spine fully preserved as defined in `story_board.md` for Day 100 Prologue.
- **Branching / flags touched:** Added `prologue_found` flag set (`"overheard"` / `"read_letters"`), correctly integrated with `StoryState` in `classes_non_canon.rpy`.
- **`# CANON FLAG` items:** None.

## 5. Downstream gate notes
- **Lead Narrative Editor:** The script contains wide contrast between dialogue and internal monologue. Need review of the Wiltshire transition.
- **Victorian Consultant:** The language is formal and avoids contractions to superiors ("I am" instead of "I'm"). The letter contains Victorian epistolary registers.
