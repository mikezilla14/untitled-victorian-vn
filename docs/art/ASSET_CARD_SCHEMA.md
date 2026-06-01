# Asset Card YAML Schema Specification

Every generated visual asset must possess a corresponding asset tracking card (`*.md`) located under `assets_source/character_cards/` or `assets_source/location_cards/`. These files must declare metadata using standardized YAML frontmatter schemas.

---

## 👥 Character Sprite Card Schema

```yaml
asset_id: ""                  # Unique lowercase snake_case ID (e.g. cora_maid)
asset_type: "sprite"          # Hardcoded 'sprite'
character: ""                 # Character name (Cora / Gideon / Stern / Vance / Missy)
role: ""                      # In-game role (e.g. chambermaid, VIP guest)
canonical: false              # Set to true if this matches locked character profiles
source_mode: ""               # text-to-image | image-to-image | vnccs-variant | manual-cleanup
pose_family: ""               # Pose designation (e.g. standing_front, writing_side)
head_angle: ""                # front | three-quarters | profile
expression: ""                # target state: neutral | guarded | dominant | submissive | shocked
outfit: ""                    # Outfit description (e.g. domestic_maid, premium_suit)
mood: ""                      # Psychological tone (e.g. composed, alert, cowed)
style_reference: ""           # Style bible version or base image URL reference
prompt_template: ""           # Reference prompt template ID from PROMPT_LIBRARY.md
prompt: ""                    # Exact generated text prompt used
negative_prompt_notes: ""     # What was avoided in generation
source_sheet: ""              # Filename of original VNCCS sheet in assets_source/vnccs_sheets/
selected_cell: ""             # Cell coordinates (e.g. Row 2, Col 3) if extracted from a grid
status: ""                    # todo | rough | in_engine | needs_revision | approved | final | cut
renpy_image_name: ""          # Image alias used in Ren'Py manifest (e.g. cora_sprite guarded)
renpy_target_path: ""         # Engine target path (e.g. images/sprites/cora/guarded.webp)
source_output_path: ""        # Raw crop location (e.g. assets_source/generated_concepts/cora_guarded_crop.png)
approved_output_path: ""      # Cleaned asset path (e.g. assets_source/approved_assets/cora_guarded.webp)
notes: ""                     # Arbitrary layout or rendering notes
```

---

## 🏢 Background Card Schema

```yaml
asset_id: ""                  # Unique lowercase snake_case ID (e.g. servants_corridor_dim)
asset_type: "background"      # Hardcoded 'background'
location: ""                  # environment name (e.g. service_corridors, laundry)
scene_use: ""                 # Intended narrative scenario use
source_mode: ""               # text-to-image | image-to-image | manual-cleanup | overlay
base_or_overlay: ""           # base | lighting_overlay | detail_overlay | prop_overlay | mood_overlay
mood: ""                      # Environmental tone (e.g. dusty, tense, luxurious)
lighting: ""                  # Ambient lights (e.g. high_window_morning, flickering_gaslight)
time_of_day: ""               # morning | day | dusk | night | tea
palette: ""                   # Dominant colors (e.g. desaturated_mahogany, warm_amber)
reusability_notes: ""         # Notes on reusing architecture or overlays
removable_details: []         # Array of baked details to slice off (e.g. [door_numbers, paintings])
layer_group: ""               # Base architecture, lighting_overlay, prop_overlay
prompt_template: ""           # Reference prompt template ID from PROMPT_LIBRARY.md
prompt: ""                    # Exact text prompt used
source_reference: ""          # URL or plate ID of raw plate
status: ""                    # todo | rough | in_engine | needs_revision | approved | final | cut
renpy_image_name: ""          # Manifest alias name (e.g. bg_servants_corridor_dim)
renpy_target_path: ""         # Engine location (e.g. images/backgrounds/bg_servants_corridor_dim.webp)
source_output_path: ""        # Concept location (e.g. assets_source/generated_concepts/corridor_dim.png)
approved_output_path: ""      # Final output path (e.g. assets_source/approved_assets/bg_servants_corridor_dim.webp)
notes: ""                     # Arbitrary visual notes
```

---

## 🎛️ UI Card Schema

```yaml
asset_id: ""                  # Unique lowercase snake_case ID (e.g. ui_inkwell_empty)
asset_type: "ui"              # Hardcoded 'ui'
purpose: ""                   # Core functionality (e.g. persistent stats HUD, writing desk mask)
blend_mode_expectation: ""    # normal | alpha_blend | additive_vignette
transparent_or_black_background: "" # transparent | black_bleed
prompt_template: ""           # Prompter text
prompt: ""                    # Raw string
status: ""                    # todo | rough | in_engine | approved | final
renpy_image_name: ""          # Manifest display alias
renpy_target_path: ""         # Engine path
notes: ""                     # Functional notes
```
