# Convergent Decision Report — day102
# Release: Release 1 - MVP
# Pass: initial
# Personas considered: thematic, humour, tension, erotic, mystery, class
# Draft output: narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy
# Spec inputs: narrative/pipeline/releases/release-1-mvp/day102_*_spec.rpy
# Prose baseline: renpy_project/game/day102.rpy (promoted)

## 1. Considered (inventory)
| Persona | Spec file | Labels / beats reviewed | Notes |
|---------|-----------|-------------------------|-------|
| thematic | day102_thematic_spec.rpy | 021 morning, 022 chore, 023 gideon, 024 night | Evidence/proper survival; ledger vs page |
| humour | day102_humour_spec.rpy | 021 find, 023 vance, 023 pretend | Deadpan class comedy; Stern mouth |
| tension | day102_tension_spec.rpy | 021 take, 022 corr, 023 stern/confess | Clock interval; pulse vs mouth |
| erotic | day102_erotic_spec.rpy | 021 find, 022 corridor, 024 indulge | Lace charge; mirror disagreement |
| mystery | day102_mystery_spec.rpy | 021 deceive, 023 pretend/gideon | Trunk-as-question; ribbon misdirection; note kept |
| class | day102_class_spec.rpy | 021 deceive, 023 vance/ghost/gideon | Rank logic; management not justice |

## 2. Included (merged into draft)
| Persona | Source (spec label / line) | Target (draft label) | What changed (1 line) |
|---------|---------------------------|----------------------|------------------------|
| thematic | day102_1 spec | `day102_1_cora_missy_first_shift` | Added proof/loud-living lines after suite opening |
| thematic | day102_1_missy spec | `day102_1_missy_finds_a_thing` | Intimate vs respectability beat |
| thematic | day102_3_gideon spec | `day102_3_gideon_interrupts_controls_vance` | Reputation upholstery; prey "filed" |
| thematic | day102_4 spec | `day102_4_night` | Ledger/page appetite split |
| humour | day102_1_missy spec | `day102_1_missy_finds_a_thing` | Cora deadpan on lady who owns lace |
| humour | day102_3_vance spec | `day102_3_vance_goes_incandescent` | Private wearing wrong shoes |
| humour | day102_3_pretend spec | `day102_3_cora_pretends_to_find_it` | Stern Savoy-laughter beat |
| tension | day102_1_take spec | `day102_1_cora_takes_the_thing` | Wager breath; obedient exterior |
| tension | day102_2_corr spec | `day102_2_day2_corr_choice` | Genre-shift glance line |
| tension | day102_3_stern spec | `day102_3_stern_fetches_cora` | Clock between discovery and punishment |
| tension | day102_3_confess spec | `day102_3_cora_confesses` | Pulse vs mouth |
| erotic | day102_1 spec | `day102_1_missy_finds_a_thing` | Lace lightness line |
| erotic | day102_2 spec | `day102_2_day2_chore_time` | Heat/fear shared pulse (wearing) |
| erotic | day102_4 spec | `day102_4_cora_sneaks_a_feel` | Mirror maid vs skin; heat without ink |
| mystery | day102_1_deceive spec | `day102_1_cora_deceives_missy` | Trunk as question to Locke |
| mystery | day102_3_pretend spec | `day102_3_cora_pretends_to_find_it` | Ribbon teaches wrong lesson |
| mystery | day102_3_gideon spec | `day102_3_gideon_interrupts_controls_vance` | Story chosen; ghost keeps note |
| class | day102_1_deceive spec | `day102_1_cora_deceives_missy` | (merged with promoted trunk logic) |
| class | day102_3_vance spec | `day102_3_vance_goes_incandescent` | Truth unheard from below stairs |
| class | day102_3_frames spec | `day102_3_cora_frames_missy` | Ivory-handled knives |
| class | day102_3_gideon spec | `day102_3_gideon_interrupts_controls_vance` | Miss Vance privately |

## 3. Cut (not in draft)
| Persona | Idea / beat | Rationale | Disposition |
|---------|-------------|-----------|-------------|
| humour | Hatbox size joke before crisis | Undercuts Vance incandescent tone | Rejected |
| tension | Door slam before Gideon | Contradicts silent entrance | Rejected |
| mystery | Extra witness maid | New fact not in spine | Rejected |
| thematic | Feminism sermon in tea room | Victorian gate risk | Rejected |

## 4. Structural & canon decisions
- **Spine preserved:** All labels and branches match `story_board.md` and promoted `day102.rpy`.
- **Router:** Afternoon chains + desk retreat → `end_slot(d2_reflect_done)`; night → `end_slot(d2_write_night)`; `day103_morning` deadline stub retained.
- **CHECK slots:** `check_confrontations` + `show_ledger_ui` at `day102_2_day2_chore_time` and `day102_4_night`.
- **Stats:** `apply_effects` values aligned with promoted `day102.rpy` (`susp`/`insp`/`corr`); legacy `susp` maps to Stern per `functions_non_canon.rpy`.
- **APIs:** `has_story_fuel`, `set_time_period`, `time_manager.set_current_day(2)`, whitelisted `story.set_*` only.
- **`# CANON FLAG` items:** None.

## 5. Downstream gate notes
- **Lead Narrative Editor:** Day 2 voice — thought sharper, speech formal; verify Cora line lengths to superiors where added.
- **Victorian Consultant:** "Miss Vance privately"; servant/deadpan register; no modern psych jargon.
