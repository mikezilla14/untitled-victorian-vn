# Convergent Decision Report — day100
# Release: Release 1 - MVP
# Pass: rewrite-narrative-synthesis
# Personas considered: thematic, tension, class, mystery, erotic
# Draft output: main-game/non-prod-game/game/days/day100_non_canon.rpy
# Spec inputs: main-game/pipeline/releases/release-1-mvp/days/day100/specs/day100_*_spec.rpy

## 1. Considered (inventory)
| Persona | Spec file | Labels / beats reviewed | Notes |
|---------|-----------|-------------------------|-------|
| thematic | day100_thematic_spec.rpy | `day100_main`, `day100_1_afternoon_boredom`, `day100_2_reconvergence` | Metaphors of country house stone, soot-stained carriage, and stolen currency of ink. |
| tension | day100_tension_spec.rpy | `day100_main`, `day100_2_reconvergence`, `day100_3_night_daydream` | Suspense of crawling the corridor, hiding behind folding screen, and Waterloo arrival. |
| class | day100_class_spec.rpy | `day100_main`, `day100_2_reconvergence`, `day100_3_night_daydream` | Master-servant geometry, Sir John's absolute social weight, and threat of the gutter. |
| mystery | day100_mystery_spec.rpy | `day100_2_desk_mystery`, `day100_2_parlour_mystery` | Savoy lockbox clue, Strand solicitor, and forged reference liability. |
| erotic | day100_erotic_spec.rpy | `day100_2_desk_erotic`, `day100_2_parlour_erotic`, `day100_2_reconvergence_erotic`, `day100_3_night_daydream` | Sensory details of letters, parlour sounds, Sir John's undone collar, and 2.8 spice train daydream. |

## 2. Included (merged into draft)
| Persona | Source (spec label / line) | Target (draft label) | What changed (1 line) |
|---------|---------------------------|----------------------|------------------------|
| tension | day100_tension_spec:5 | `day100_main` | Opening in motion with candle and three pages. |
| class | day100_class_spec:10 | `day100_main` | Cora's interiority of country maid training and trespass. |
| thematic | day100_thematic_spec:25 | `day100_1_afternoon_boredom` | Description of study, smell of dried roses, and master desk. |
| erotic | day100_erotic_spec:45 | `day100_2_parlour_branch` | Rhythmic damp gasp and buckle release heard through parlour door. |
| erotic | day100_erotic_spec:55 | `day100_2_desk_branch` | Erotic, wild handwriting in Sir John's letter to George. |
| mystery | day100_mystery_spec:45 | `day100_2_desk_branch` / `day100_2_parlour_branch` | lockbox key at Strand / Savoy hotel hooks. |
| tension | day100_tension_spec:45 | `day100_2_reconvergence` | Step-by-step hiding behind folding screen and caught moment. |
| class | day100_class_spec:60 | `day100_2_reconvergence` | Defining choices: Lie/Deflect/Submit and Why Write. |
| erotic | day100_erotic_spec:65 | `day100_2_reconvergence` | Sir John's state of disarray (loose collar, breathing). |
| tension | day100_tension_spec:80 | `day100_3_night_daydream` | Coal smoke, damp wool train atmosphere, and satchel spill at Waterloo. |
| erotic | day100_erotic_spec:75 | `day100_3_night_daydream` | Daydream details (parlour breath vs letters' ink) reflecting 2.8 spice rating. |

## 3. Cut (not in draft)
| Persona | Idea / beat | Rationale | Disposition (parked / rejected) |
|---------|-------------|-----------|----------------------------------|
| thematic | Extended description of carriage passenger | Distracted from the immediate tension of the satchel spill. | Rejected |
| mystery | Detailed name of solicitor on the Strand | Too much detail for a prologue; can be resolved in Day 101/102. | Parked |

## 4. Structural & canon decisions
- **Spine preserved / altered:** Labels fully preserved to match Twine-mapped spine and downstream files.
- **Branching / flags touched:** Maps to `prologue_found` (`"read_letters"` / `"overheard"`), `prologue_why_write` (`"money_home"` / `"cataloguer"` / `"scandal_hungry"`), and `prologue_holywell_posture` (`"careful"` / `"eager"` / `"desperate"`).
- **`# CANON FLAG` items:** None.

## 5. Downstream gate notes
- **Lead Narrative Editor:** Check Cora's speech lock in the dialogue with Sir John (strict cap of <= 8 words, no contractions).
- **Forensic Psychology Gate:** Verify the psychological consistency of the three confrontation postures (Lie, Deflect, Submit) with early-game Cora.
- **Victorian Consultant:** Verify period terms (walnut bureau, grandfather clock, third-class train carriage, Strand solicitor, lye, coal smoke).
