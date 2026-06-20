# Convergent Decision Report — day101
# Release: Release 1 - MVP
# Pass: editor-revision-1
# Prior pass: revision-1
# Personas considered (editor-revision-1): tension, class, thematic, erotic (selective merge per day101_narrative_change_brief.md)
# Draft output: main-game/non-prod-game/game/days/day101_non_canon.rpy
# Spec inputs: narrative/draft/releases/release-1-mvp/planning/day101_non_canon_draft_rewrite.rpy (donor); live sandbox baseline

## 1. Considered (inventory)
| Persona | Spec file | Labels / beats reviewed | Notes |
|---------|-----------|-------------------------|-------|
| thematic | day101_thematic_spec.rpy | `day101_1_morning_interview`, `day101_2_missy_meets_cora` | Stressed class distances and sensory smoke of London's Savoy. |
| tension | day101_tension_spec.rpy | `day101_2_coras_path_choice`, `day101_3_taking_stock_day1` | Built high-tension corridor eavesdropping pacing and panic. |
| class | day101_class_spec.rpy | `day101_1_morning_interview`, `day101_1_vance_throws_toy` | Highlighted class distance and Stern's hyper-surveillance metrics. |
| mystery | day101_mystery_spec.rpy | `day101_4_write_the_chapter` | Integrated the lockbox hook and Locke's secret portfolio clue. |
| erotic | day101_erotic_spec.rpy | `day101_2_coras_path_choice`, `day101_4_visit_missy` | Added close somatic detail, skin friction, and voyeuristic shame. |

## 2. Included (merged into draft)
| Persona | Source (spec label / line) | Target (draft label) | What changed (1 line) |
|---------|---------------------------|----------------------|------------------------|
| class | day101_class_spec:15 | `day101_1_morning_interview` | Expanded Miss Stern's rigorous, measuring inspection of Cora. |
| thematic | day101_thematic_spec:33 | `day101_1_morning_interview` | Contraction-free and short-sentenced Cora Day 1 voice constraints. |
| tension | day101_tension_spec:45 | `day101_1_vance_throws_toy` | High-anxiety reaction to Mr. Locke's cold footsteps in the corridor. |
| erotic | day101_erotic_spec:52 | `day101_2_coras_path_choice` | Sensual/ voyeuristic tension in Vance kneeling before Gideon Locke. |
| mystery | day101_mystery_spec:70 | `day101_3_taking_stock_day1` | Locked journal entry detailing command, witness, and consequence. |
| erotic | day101_erotic_spec:110 | `day101_4_visit_missy` | Warm, intimate physical closeness between Cora and Missy on the bed. |

## 3. Cut (not in draft)
| Persona | Idea / beat | Rationale | Disposition (parked / rejected) |
|---------|-------------|-----------|----------------------------------|
| thematic | Prolonged country house flashback during interview | Slowed down the tense pacing of Stern's immediate interrogation. | Rejected |
| mystery | Details on Mr. Locke's background portfolio | Too early to reveal; keep focus on immediate sensory voyeurism in Day 1. | Parked |
| tension | Footman actively intercepting Cora in the hallway | False threat that distracts from the core tension of the corridor choice. | Rejected |

## 4. Structural & canon decisions
- **Spine preserved / altered:** Spine fully preserved. All slot endings (desk retreat, write chapter, visit Missy) successfully updated to call the centralized `end_slot` router label.
- **Branching / flags touched:** Set `day1_interview_state` (`"meek"` / `"competent"`), `day1_corridor_state` (`"predator"` / `"prey"` / `"ghost"`), `day1_ledger_focus` (`"inspiration"` / `"corruption"`), `day1_night_action` (`"write"` / `"visit_missy"`), and `missy_day1_trust_state` using whitelisted setters in `classes_non_canon.rpy`.
- **`# CANON FLAG` items:** None.

## 5. Downstream gate notes
- **Lead Narrative Editor:** Strict Day 1 voice locks applied to all of Cora's dialogue with superiors: sentences are <= 8 words and contain no contractions.
- **Victorian Consultant:** Formal register and historical framing preserved. Cora utilizes formal titles (Ma'am, Sir, Miss) when addressing superiors.

---

## 6. Editor-revision-1 (2026-06-21) — dark-romance selective merge

**Trigger:** `day101_narrative_change_brief.md` (lead_narrative_editor, scale M).

| Donor beat | Target label | Disposition |
|------------|--------------|-------------|
| Opening precarity (Cork lilt, Holywell, Savoy consumption) | `day101_main` | **Merged** |
| Sir John reference leash (not Eleanor blackmail) | `day101_1_cora_waiting`, `day101_1_morning_interview` | **Merged** |
| Stern clinical inspection (carbolic, boots, throat trace) | `day101_1_morning_interview` | **Merged** |
| Missy Hindon / East Knoyle identity trap | `day101_2_missy_meets_cora` | **Merged** |
| `set_missy_day1_trust_state` on corridor branches | `day101_2_coras_path_choice` | **Merged** (`unsettled` / `shared_caution` / `soothed`) |
| Ledger + write-chapter reflection polish | `day101_3_taking_stock_day1`, `day101_4_write_the_chapter` | **Partial merge** |
| Vance-Missy corridor cold open | `day101_1_vance_throws_toy` | **Rejected** — preserves Gideon naming + dressing room spine |
| Ghost knock-and-enter | `day101_2_coras_path_choice` | **Rejected** — live walk-on/wall path retained |
| IRL explicit corridor anatomy | corridor branches | **Rejected** — manuscript layer only |

**Spine preserved:** `day101_1_vance_dressing_room`, `day101_1_vance_stairwell_encounter`, full `day1_vance_relation` tree, all menu/setter contracts unchanged.
