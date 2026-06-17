# Convergent Decision Report — day104
# Release: Release 1 - MVP
# Pass: initial (Writers' Room synthesis)
# Personas considered: thematic, erotic, tension
# Draft output: main-game/non-prod-game/game/days/day104_non_canon.rpy
# Spec inputs: main-game/pipeline/releases/release-1-mvp/days/day104/specs/day104_*_spec.rpy
# Prose baseline: main-game/prod-game/game/day104.rpy (promoted)
# Target spice level: 3.5ish (Dramatic Middle Ground + Restrained Heat)

## 1. Considered (inventory)
| Persona | Spec file | Labels / beats reviewed | Notes |
|---------|-----------|-------------------------|-------|
| thematic | day104_thematic_spec.rpy | false_dawn_suite_window, lockbox_evidence, return_early, stern_pressure, twilight_ledger_false_dawn, triumphant_chapter, false_dawn_ending | Cora's performer self; manuscript ending as knife; false dawn reset metaphor |
| erotic | day104_erotic_spec.rpy | false_dawn_suite_window, lockbox_evidence, return_early, stern_pressure, twilight_ledger_false_dawn, triumphant_chapter, false_dawn_ending | Shaving soap & leather scents; photographic paper corner scratch on chest; hearth unlacing heat |
| tension | day104_tension_spec.rpy | false_dawn_suite_window, lockbox_evidence, return_early, stern_pressure, twilight_ledger_false_dawn, triumphant_chapter, false_dawn_ending | Floorboard creaks; hairpin bending under slick sweat; mouse in a cage framing; loose board paranoia |

## 2. Included (merged into draft)
| Persona | Source (spec label) | Target (draft label) | What changed (1 line) |
|---------|---------------------|----------------------|-----------------------|
| thematic | false_dawn_suite_window | `day104_1_false_dawn_suite_window` | Resetting expensive rooms metaphor |
| thematic | lockbox_evidence | `day104_1_lockbox_evidence` | Description of manuscript ending as knife |
| thematic | return_early | `day104_2_return_early` | False dawn springing trap and letting sun in first metaphor |
| erotic | false_dawn_suite_window | `day104_1_false_dawn_suite_window` | Bodice tightness and scent of shaving soap and leather |
| erotic | lockbox_evidence | `day104_1_lockbox_evidence` | Photographic paper scratching bodice skin like a second pulse |
| erotic | return_early | `day104_2_escape_fireplace` | Crawling into unlit hearth with photo against bare chest |
| erotic | triumphant_chapter | `day104_5_triumphant_chapter` | Single candle writing by shift; shift loose over shoulders |
| tension | lockbox_evidence | `day104_1_lockbox_evidence` | Slick hands and hairpin bending before lock gives way |
| tension | return_early | `day104_2_return_early` | Trapped mouse in a gilded cage escape pressure |
| tension | stern_pressure | `day104_3_stern_pressure` | Guilt smelling like laundry quarters mildew |
| tension | twilight_ledger_false_dawn | `day104_4_twilight_ledger_false_dawn` | Loose board under bed paranoia and checking grates |

## 3. Cut (not in draft)
| Persona | Idea / beat | Rationale | Disposition |
|---------|-------------|-----------|-------------|
| thematic | Extended dialogue on autopsies | Slows down pacing of tense bedroom escape | Rejected |
| erotic | Intimate fireplace unlacing with Gideon present | Gideon doesn't check the hearth; unrealistic for day-layer | Rejected |
| tension | Stern breaking door down | Stern relies on cynicism and observation, not violent outbursts | Rejected |

## 4. Structural & canon decisions
- **Spine preserved:** Draft starts with `day104_1_false_dawn_suite_window` which aligns seamlessly with `day103_non_canon.rpy`'s exit routing.
- **Two-tiered suspicion alignment:** Resolved the fireplace escape to correctly modify permanent acute `stern_susp` by `35` to reflect soot on uniform. Fireplace atonement correctly modifies `stern_susp` by `-30`.
- **Missy alibi integrity:** Retained the optional `missy_susp` adjustments during the Missy cover branch to ensure non-canon sandbox choices carry mechanical weight.

## 5. Downstream gate notes
- **Lead Narrative Editor:** The double-life distinction (maid mask by day, writer self by night) is masterfully written.
- **Forensic Psychology:** Cora's panic vs calculated survival choices (Observer, Predator, Prey, Ghost) are extremely consistent with the bible.
- **Victorian Consultant:** Savoy West End matinees, leather lockboxes, and lye soap are historically authentic.
