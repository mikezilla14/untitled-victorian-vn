# Spec: Art prompt workflow documentation

## Purpose

Create a single, repo-owned prompt workflow for visual novel art production so concept prompts, image references, asset manifest entries, VNCCS sprite outputs, background cleanup notes, and Ren'Py-ready asset names are no longer scattered across chats.

This spec is intended for an agentic IDE/code assistant to implement documentation and lightweight repository structure. It does **not** ask the agent to generate art. It asks the agent to document the repeatable workflow and create the files/templates needed to run art production consistently.

## Problem statement

Current art production material is distributed across chats and ad hoc files. That was useful for avoiding image-generation context pollution, but it creates production friction:

- prompts are hard to find and compare;
- concepts are not consistently linked to manifest entries;
- approved assets are not clearly separated from raw generations;
- sprite/background prompt templates are repeated and drift over time;
- reusable hotel background layering rules are not yet documented as a production system;
- VNCCS sprite-sheet outputs need a documented naming and slicing pipeline;
- future paper-doll/sprite-layering backlog requirements need to be preserved without blocking MVP delivery.

## Product goal

Implement a documentation-driven art prompt workflow that supports the MVP art sprint and future layered sprite backlog.

The workflow should make it easy to:

1. create an asset card from the asset manifest;
2. choose a prompt template;
3. generate concept art from text or an existing image;
4. store raw and approved outputs in predictable folders;
5. promote approved concepts to VNCCS/background cleanup;
6. export Ren'Py-ready assets;
7. preserve source prompts and raw crops for future paper-doll work.

## Scope

### In scope

Create documentation and templates for:

- global visual style bible;
- character sprite prompt templates;
- image-to-sprite conversion prompt templates;
- background prompt templates;
- image-to-background conversion prompt templates;
- expression/pose variant generation prompts;
- UI/HUD prompt handling;
- CG/story illustration prompt handling;
- asset cards;
- source/approved/final asset folder conventions;
- naming conventions;
- VNCCS sheet slicing workflow;
- modular hotel background layering workflow;
- MVP vs backlog distinctions.

### Out of scope

Do not:

- generate images;
- change story content;
- modify existing `.rpy` scene scripts;
- implement the future paper-doll runtime system;
- add large binary art assets;
- move existing assets unless explicitly requested;
- alter the Ren'Py asset manifest unless a later implementation task explicitly asks for it.

## Repository context

This repo uses documentation-driven agent orchestration. Keep this workflow compatible with the existing agent style: markdown docs, clear contracts, explicit file paths, and validation-friendly structure.

## Files to create or update

Create the following documentation files:

```text
docs/art/README.md
docs/art/STYLE_BIBLE.md
docs/art/PROMPT_LIBRARY.md
docs/art/ASSET_CARD_SCHEMA.md
docs/art/ASSET_NAMING.md
docs/art/VNCCS_SPRITE_SHEETS.md
docs/art/BACKGROUND_LAYERING.md
docs/art/PRODUCTION_WORKFLOW.md
docs/art/examples/character_card_cora.md
docs/art/examples/location_card_servants_corridor.md
```

Optional, only if useful:

```text
assets_source/README.md
assets_source/prompts/README.md
assets_source/character_cards/README.md
assets_source/location_cards/README.md
assets_source/vnccs_sheets/README.md
assets_source/generated_concepts/README.md
assets_source/approved_assets/README.md
```

Do not add heavy binary images in this task.

## Required documentation content

### `docs/art/README.md`

Purpose: top-level entry point for the art workflow.

Must include:

- what the art workflow is for;
- quick-start steps;
- file map linking to the docs below;
- MVP rule: generate concepts fast, put roughs in Ren'Py quickly, polish only approved/high-frequency assets;
- backlog rule: preserve source sheets, prompts, and raw crops for future paper-doll extraction.

### `docs/art/STYLE_BIBLE.md`

Purpose: canonical visual language for all prompt templates.

Must include these style anchors:

- refined Victorian period-drama visual novel style;
- soft Violet Evergarden-adjacent anime elegance;
- slight western-animation-adjacent facial structure;
- expressive but grounded faces;
- clean confident linework;
- soft painterly cel-shading;
- restrained luminous eyes, not huge glossy doll eyes;
- delicate period-drama polish;
- neutral gray sprite background for sprite generation;
- painterly but readable backgrounds that sit behind dialogue/sprites;
- avoid photorealism, 3D-render look, plastic skin, chibi proportions, generic modern anime, modern clothing, harsh comic-book outlines, and noisy detail.

Include separate blocks for:

- master sprite style;
- master background style;
- UI/HUD style;
- historical-costume notes for 1890s London.

### `docs/art/PROMPT_LIBRARY.md`

Purpose: reusable copy/paste prompt templates.

Must include templates for:

1. character sprite from text;
2. character sprite from existing image;
3. background from text;
4. background from existing image;
5. expression/pose variant generation;
6. UI/HUD asset generation;
7. CG/story illustration generation;
8. optional intimate CG/story CG prompt pattern, framed as story CG production and requiring clearly adult characters.

Each template should have labeled placeholders, for example:

```text
[CHARACTER DESCRIPTION]
[OUTFIT DESCRIPTION]
[MOOD]
[LOCATION DESCRIPTION]
[LIGHTING]
[REFERENCE IMAGE NOTES]
```

Important: keep templates compact enough to reuse, but explicit enough to prevent style drift.

### `docs/art/ASSET_CARD_SCHEMA.md`

Purpose: define one card per generated asset.

Must include schemas for:

#### Character asset card

```yaml
asset_id:
asset_type: sprite
character:
role:
scene_use:
canonical: false
source_mode: text-to-image | image-to-image | vnccs-variant | manual-cleanup
pose_family:
head_angle:
expression:
outfit:
mood:
style_reference:
prompt_template:
prompt:
negative_prompt_notes:
source_reference:
source_sheet:
selected_cell:
status: todo | rough | in_engine | needs_revision | approved | final | cut
renpy_image_name:
renpy_target_path:
source_output_path:
approved_output_path:
final_output_path:
notes:
```

#### Background asset card

```yaml
asset_id:
asset_type: background
location:
scene_use:
source_mode: text-to-image | image-to-image | manual-cleanup | overlay
base_or_overlay: base | lighting_overlay | detail_overlay | prop_overlay | mood_overlay
mood:
lighting:
time_of_day:
palette:
reusability_notes:
removable_details:
layer_group:
prompt_template:
prompt:
source_reference:
status: todo | rough | in_engine | needs_revision | approved | final | cut
renpy_image_name:
renpy_target_path:
source_output_path:
approved_output_path:
final_output_path:
notes:
```

#### UI asset card

```yaml
asset_id:
asset_type: ui
purpose:
blend_mode_expectation:
transparent_or_black_background:
prompt_template:
prompt:
status:
renpy_image_name:
renpy_target_path:
notes:
```

### `docs/art/ASSET_NAMING.md`

Purpose: define boring, stable names.

Must include:

- lowercase snake_case;
- no spaces;
- no `final_final_2` names;
- raw/generated/approved/final separation;
- Ren'Py display names vs source filenames;
- future paper-doll compatible sprite naming.

Character sprite source naming:

```text
{character}_{pose_family}_{expression}_{outfit}_v###.png
```

Examples:

```text
cora_standing_front_guarded_maid_v001.png
cora_writing_down_focused_maid_v001.png
gideon_standing_front_amused_suit_v001.png
stern_standing_front_commanding_housekeeper_v001.png
```

Ren'Py-friendly aliases may stay simpler:

```renpy
image cora_sprite guarded = "images/sprites/cora/cora_standing_front_guarded_maid_v001.webp"
```

Background naming:

```text
bg_{location}_{base_or_state}_v###.png
overlay_{location}_{function}_{variant}_v###.png
```

Examples:

```text
bg_servants_corridor_base_v001.png
overlay_servants_corridor_light_morning_v001.png
overlay_servants_corridor_door_number_12_v001.png
```

### `docs/art/VNCCS_SPRITE_SHEETS.md`

Purpose: document sprite-sheet production and slicing.

Must include:

- VNCCS sheet outputs can create 12 candidate sprites per render cycle;
- current MVP uses pre-rendered full sprites;
- future backlog may use layered/paper-doll sprites;
- therefore keep source sheets and raw crops;
- group sheets by pose/head-angle families, not random expression soup;
- expression reuse only works reliably within compatible pose/head-angle families;
- source sheets may already have transparent backgrounds, so alpha-component detection can be preferable to chroma key;
- final exports must be placed on a consistent transparent canvas to avoid Ren'Py sprite jumping;
- preserve metadata: source sheet, cell/order, prompt, character version, pose family, expression, outfit.

Recommended folders:

```text
assets_source/vnccs_sheets/{character}/
assets_source/sliced/{character}/{pose_family}/raw_crops/
assets_source/sliced/{character}/{pose_family}/final/
game/images/sprites/{character}/
```

### `docs/art/BACKGROUND_LAYERING.md`

Purpose: document reusable hotel background strategy.

Must include:

- hotel setting is chosen to support asset reuse;
- base architecture should be clean and reusable;
- remove or avoid baked-in text, room numbers, unique paintings, signage, and overly specific props;
- create layered replacements for details;
- use overlays for time-of-day, mood, candle/fire/gaslight, shadows, and room identity;
- keep dialogue readability in mind.

Recommended background layer groups:

```text
base architecture
lighting overlay
mood/shadow overlay
door number/signage overlay
painting/detail overlay
prop overlay
special event overlay
```

Example:

```text
bg_servants_corridor_base.webp
overlay_servants_corridor_light_morning.webp
overlay_servants_corridor_door_number_12.webp
overlay_servants_corridor_lamp_glow.webp
```

### `docs/art/PRODUCTION_WORKFLOW.md`

Purpose: day-to-day sprint workflow.

Must include:

1. create/update asset card;
2. choose prompt template;
3. generate first-pass concept;
4. save source prompt and output;
5. drop rough into Ren'Py immediately if it fills a manifest gap;
6. mark status;
7. promote approved sprite to VNCCS or approved background cleanup;
8. slice/export final sprite/background;
9. update manifest if needed;
10. run asset validation/check workflow where applicable.

Must include MVP priorities:

- rough art in-engine beats polished art in folders;
- polish high-frequency assets first;
- generate generously but ship selectively;
- cut weak assets;
- keep H/CG scope small and high-impact;
- do not build paper-doll runtime before MVP.

## Example cards

### `docs/art/examples/character_card_cora.md`

Use Cora as the example:

- 22-year-old Victorian chambermaid;
- dark Black Irish hair pulled back neatly;
- deep dark piercing eyes;
- pale porcelain skin;
- intelligent, reserved, analytical expression;
- charcoal gray Victorian chambermaid dress;
- stiff white starched collar;
- white maid cap;
- starched white apron;
- neutral gray background;
- canonical sprite concept.

Include 3 example expression rows:

- base/composed;
- guarded;
- focused.

### `docs/art/examples/location_card_servants_corridor.md`

Use servant corridor as the example:

- reusable Savoy Hotel servant corridor, 1891;
- moody transitional/dialogue background;
- dark wood trim, patterned wallpaper, brass lamps, repeated doors;
- removable details: door numbers, signage, paintings, lamp glows;
- layering target: base architecture + morning/dim/night overlays.

## Existing material to preserve

The prompt library should incorporate the existing character and UI prompt material from prior notes, including:

- Cora Hartley sprite setup;
- Sir Gideon Locke sprite setup;
- Missy sprite setup;
- Vance sprite setup;
- Ms. Stern sprite setup;
- UI cameo, suspicion vignette, and inkwell prompts.

When migrating this material, edit for consistency and remove duplicated style blocks, but do not discard character-specific details.

## Acceptance criteria

The task is complete when:

- all required docs under `docs/art/` exist;
- `docs/art/README.md` links to each art workflow document;
- `PROMPT_LIBRARY.md` includes reusable prompt templates for text/image sprites and text/image backgrounds;
- `ASSET_CARD_SCHEMA.md` includes character, background, and UI schemas;
- `ASSET_NAMING.md` defines source, approved, final, and Ren'Py naming conventions;
- `VNCCS_SPRITE_SHEETS.md` documents sheet slicing and future paper-doll preservation rules;
- `BACKGROUND_LAYERING.md` documents base/overlay strategy for reusable hotel backgrounds;
- `PRODUCTION_WORKFLOW.md` gives a practical step-by-step MVP workflow;
- example Cora and servant-corridor asset cards exist;
- docs are markdown-only and do not introduce binary art assets;
- no production `.rpy` scene content is changed;
- any validation/check command recommended by the repo passes or any failures are documented.

## Suggested agent instructions

Use the repository's existing documentation-driven style. Keep docs concise but operational. Prefer clear headings, examples, and copy/paste templates over essay prose.

Do not invent new character canon beyond the provided art prompt notes. If a character detail is unclear, leave a placeholder or mark it as TBD.

Do not overbuild. This is a production support workflow for a 3-week art sprint, not a full digital asset management system.

## Suggested validation

After implementing, run the repository's normal validation for changed docs if available. At minimum, check that all markdown links between the new docs resolve.

Suggested manual review checklist:

- Can a new asset be generated by reading only `docs/art/README.md`, `STYLE_BIBLE.md`, and `PROMPT_LIBRARY.md`?
- Can a sprite generated from VNCCS be named and archived using only `VNCCS_SPRITE_SHEETS.md` and `ASSET_NAMING.md`?
- Can a background be cleaned/layered using only `BACKGROUND_LAYERING.md`?
- Can the workflow distinguish MVP pre-rendered sprites from future paper-doll backlog assets?
