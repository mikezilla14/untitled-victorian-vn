# Convergent Decision Report — day103
# Release: Release 1 - MVP
# Pass: initial (Writers' Room synthesis)
# Personas considered: thematic, erotic, tension
# Draft output: narrative/draft/releases/release-1-mvp/days/day103/day103_non_canon.rpy
# Spec inputs: narrative/pipeline/releases/release-1-mvp/days/day103/specs/day103_*_spec.rpy
# Prose baseline: renpy_project/game/day103.rpy (promoted)
# Target spice level: 3.5ish (Dramatic Middle Ground + Restrained Heat)

## 1. Considered (inventory)
| Persona | Spec file | Labels / beats reviewed | Notes |
|---------|-----------|-------------------------|-------|
| thematic | day103_thematic_spec.rpy | servants_corridor, suite_gideon_tea, gideon_beat, night_tea, final_write | Cora's performer self; manuscript as survival; ink vs copper |
| erotic | day103_erotic_spec.rpy | suite_gideon_tea, gideon_beat, night_tea, final_write | Silk & French powder texture; mirror meetings; uniform tightness; explicit retelling |
| tension | day103_tension_spec.rpy | servants_corridor, suite_gideon_tea, gideon_beat, stern_suspicion, night_tea | Exposure anxiety; keyhole-risk; lockbox-threat; raw kneeling frame |

## 2. Included (merged into draft)
| Persona | Source (spec label) | Target (draft label) | What changed (1 line) |
|---------|---------------------|----------------------|-----------------------|
| thematic | servants_corridor | `day103_1_servants_corridor` | Performing self / resetting gears metaphor |
| thematic | suite_gideon_tea | `day103_2_suite_cora_vs_gideon` | Description of vanity bones and craft description |
| thematic | night_tea | `day103_2_night_defy_gideon` | Sentence on defiance tasting like ink and copper |
| erotic | suite_gideon_tea | `day103_2_suite_gideon_tea` | Tactile scent of warm silk and hairbrush sliding tension |
| erotic | suite_gideon_tea | `day103_2_suite_cora_vs_gideon` | Proximity and meeting eyes in mirror glass |
| erotic | gideon_beat | `day103_2_suite_gideon_beat` | Tactile threat: Gideon's low voice and temple proximity |
| erotic | night_tea | `day103_2_night_surrender_gideon` | Gideon undone collar; corset pulse; corset/skirt heat |
| erotic | final_write | `day103_3_bedroom_final_write` | Sensual/eroticized manuscript retelling with unbuttoning |
| tension | servants_corridor | `day103_1_servants_corridor` | Stern inspection shadow and floorboard creaks |
| tension | suite_gideon_tea | `day103_2_cora_vs_gideon_ghost` | Detailed kneeling frame, boot-heels, skirt catch |
| tension | stern_suspicion | `day103_4_room_stern_suspicion` | Play stupid "innocence you cannot afford" beat |
| tension | night_tea | `day103_2_suite_night_tea` | Keyhole exposure weight and lockbox keys threat |

## 3. Cut (not in draft)
| Persona | Idea / beat | Rationale | Disposition |
|---------|-------------|-----------|-------------|
| thematic | Direct essay on autopsies | Too modern and academic; slows down parlor pacing | Rejected |
| erotic | Explicitness in real-life suite | Violates Victorian constraint for IRL layer; moves to manuscript | Shifted to book layer |
| tension | Stern screaming at door | Contradicts Stern's quiet, cynical discipline style | Rejected |

## 4. Structural & canon decisions
- **Spine preserved:** Entry label is restructured as `day103_morning` (with deadline check) before jumping to `day103_1_servants_corridor` so it compiles without error and routes properly from Day 102.
- **De-deprecated variables:** All legacy `susp` references are mapped to target suspicions (`stern_susp` or `vance_susp`) to prevent `ValueError` at runtime.
- **API calls synchronized:** Evaluated and mapped `player.has_story_fuel` to `has_story_fuel` matching baseline architecture.
- **Story chains:** Optional morning chain menu jumps correctly to `day103_1_optional_character_chain` as designed for non-canon.

## 5. Downstream gate notes
- **Lead Narrative Editor:** The performing self vs Cora's Irish identity is sharply delineated. Dialect slips in writing are appropriate.
- **Forensic Psychology:** Gideon's dominant framing and Cora's panic/pleasure reaction in "Surrender" represent a highly-consistent Level 3.5 tension.
- **Victorian Consultant:** Savoy electric lighting, lavender scents, and class distance are maintained with absolute precision.
