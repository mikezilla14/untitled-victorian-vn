# Spec: Book1 MVP Payload System

## Purpose

Define Book1 as the primary MVP payoff vehicle for the Victorian VN.

The hotel loop creates stress, suspicion, temptation, class pressure, erotic curiosity, and narrative material. The Book1 writing engine converts that material into Cora Hartley's fictional manuscript: a sensational Holywell Street penny dreadful written through her authorial persona, Coralie Vale.

The MVP test is:

> Can the player's hotel choices create enough tension and narrative investment that the writing event feels like a grounded, satisfying, adult payoff?

Book1 is therefore not a side flavour feature. It is the MVP payload layer: the place where hotel pressure becomes authored gothic fantasy, manuscript prose, and illustrated plate reward.

This spec keeps the existing prose and image architecture, then defines the modular components required to support the new payload direction without making future enhancements brittle.

---

## Current Architecture Summary

### Existing prose architecture

Book1 currently uses a label-based Ren'Py architecture.

Existing core pieces:

- `book1.CHAPTER_BLOCKS` maps chapter keys and state buckets to prose labels.
- `book1_write_chapter(...)` is the public entry point called by day scripts and harness tests.
- `book1_nvl_write_line(...)` renders manuscript prose with word-by-word reveal.
- Pagination is centrally controlled through `_book1_page_line_limit`.
- Prose lives in `book1_block_*` labels in per-day Book1 files.
- Day scripts own fuel checks, manuscript completion, stat changes, routing, and post-writing flow.
- Book1 prose labels should not mutate `story`, `player`, `time_manager`, or persistent state.
- Image changes are explicitly supported through `book1_set_page_image(...)`.

This architecture is sound and should be preserved.

### Existing image architecture

Book1 currently has a simple right-frame illustration primitive:

```renpy
call book1_set_page_image("image_name")
```

This updates:

```renpy
store.book1_page_image
```

The Book1/NVL screen displays `book1_page_image` in the right-side framed illustration slot.

This is the correct low-level primitive, but it is not expressive enough for the MVP payload concept on its own. The new system should add a higher-level visual controller while keeping `book1_set_page_image(...)` as a compatibility wrapper.

### Existing screen architecture

The current Book1 NVL screen has:

- left manuscript text area;
- right penny dreadful title/cover area;
- framed illustration image;
- price/publisher footer;
- lower player stats HUD showing portrait, inkwell, corruption, and anxiety.

The revised MVP direction should remove the player stats HUD from the Book1 writing screen. The book should feel like Cora's escape from the hotel pressure loop, not another pressure dashboard.

---

## Design Pillars

### 1. The book is the payoff

The hotel loop earns the writing event. The writing event must reward the player with:

- transformed prose;
- visible consequence of earlier choices;
- erotic/gothic escalation;
- authorial identity;
- staged image payoff;
- Victorian plate reveal;
- a collectible sense that the hotel day became a chapter.

### 2. Cora transforms experience into fiction

Book1 is not literal hotel recap.

The manuscript should transform hotel events through:

- exaggeration;
- gothic abstraction;
- erotic intensification;
- symbolic substitution;
- class revenge;
- self-mythologising;
- concealment, distortion, and selective confession.

The dramatic point is not only what happened. It is what Cora chooses to make of it.

### 3. The writing screen is emotional escape

The hotel UI represents pressure, management, suspicion, and consequence.

The Book1 UI should feel like release:

- no visible anxiety meter;
- no corruption meter;
- no suspicion UI;
- no player stats HUD;
- minimal mechanical reminders;
- focus on page, prose, image, caption, and authorial transformation.

Stats may still drive routing behind the scenes. They should not dominate the writing presentation.

### 4. Modular enhancement over hard rewrites

Each subsystem should be independently replaceable.

The engine should allow later upgrades such as:

- page-turn transitions;
- ink-spread transformations;
- gallery unlocks;
- alternate captions;
- close-up crops;
- audio stingers;
- better text pacing;
- different page templates;
- multiple books;
- route-specific mastheads;
- external authoring/import tools;

without forcing a rewrite of prose routing.

---

## MVP Player Experience

### Flow

A writing event should follow this general sequence:

1. Hotel gameplay creates narrative material.
2. The day script calls `book1_write_chapter(...)`.
3. The screen shifts away from hotel UI into Book1 presentation.
4. The chapter title appears.
5. Manuscript prose reveals word by word.
6. Sparse author-thought fragments may appear as Cora composes.
7. The page image changes at explicit beats.
8. A staged original-style tableau may appear.
9. The final tableau transitions into a Victorian illustrated plate.
10. The chapter closes.
11. The player returns to the hotel loop or night conclusion.
12. Optional: the plate is marked as unlocked for gallery use.

### Emotional rhythm

The writing event should feel like:

- first breath after pressure;
- private authorship;
- transmutation of fear into control;
- erotic/gothic imagination taking command;
- a reward proportional to the hotel investment.

It should not feel like:

- a normal dialogue scene with a decorative image;
- a stats menu;
- an exposition dump;
- a disconnected adult CG viewer;
- a lore codex.

---

## Module Overview

Book1 should be treated as a modular payload system with these major modules:

1. **Prose Router** - resolves chapter key and route bucket to prose label.
2. **Prose Renderer** - renders manuscript prose with word reveal and pagination.
3. **Author Thought Renderer** - shows sparse Cora composition-thought fragments.
4. **Visual Controller** - handles cover/tableau/plate/detail image modes and captions.
5. **Screen Presenter** - renders the writing screen, manuscript page, image area, and captions.
6. **Asset Registry** - manages approved Book1 images and fallbacks.
7. **Import/Export Interface** - future tooling layer for external prose editing.
8. **Gallery/Unlock Stub** - optional future layer for unlocked plates.

Each module should have a narrow API and avoid hidden coupling.

---

## Module A: Prose Router

### Existing component

```renpy
label book1_write_chapter(chapter_key="day1_chapter", current_day=101, word_delay=0.04, include_debug=False):
```

### Responsibility

- Clear NVL at start and end.
- Initialise Book1 runtime display state.
- Resolve the route bucket.
- Call the appropriate `book1_block_*` label.
- Preserve existing call signature where possible.

### Required MVP changes

Extend initialisation to include presentation state:

```renpy
$ store._book1_word_delay = word_delay
$ store._book1_page_line_count = 0
$ store._book1_page_line_limit = 4
$ store.book1_page_image = "ui_book_cover"
$ store.book1_page_mode = "cover"
$ store.book1_plate_caption = ""
$ store.book1_chapter_title = ""
$ store.book1_author_thought = ""
$ store.book1_show_stats = False
```

The exact names can change, but the separation is important:

- `book1_page_image` = what image is displayed;
- `book1_page_mode` = how the image is framed/interpreted;
- `book1_plate_caption` = dynamic caption text;
- `book1_chapter_title` = dynamic chapter/masthead text;
- `book1_author_thought` = sparse composition-thought text;
- `book1_show_stats` = should remain false for the revised MVP screen.

---

## Module B: Prose Renderer

### Existing component

```renpy
label book1_nvl_write_line(line, word_delay=0.04):
```

### Responsibility

- Apply word-by-word reveal.
- Display manuscript prose.
- Track line count.
- Clear page after configured line limit.

### MVP recommendation

Keep this helper stable. It is already doing the correct job.

Possible future wrapper:

```renpy
label book1_write_paragraph(line, word_delay=0.04, emphasis=None):
```

Do not rename or replace the current renderer unless necessary. Existing Book1 labels depend on it.

---

## Module C: Author Thought Renderer

### Purpose

Add a sparse thought stream showing Cora composing, revising, intensifying, censoring, or transforming the hotel material into fiction.

This should make the writing process feel authored rather than merely displayed.

### Design intent

Author thoughts are not ordinary inner monologue. They are writer-brain fragments.

They should express:

- correction;
- selection;
- denial;
- intensification;
- shame;
- appetite;
- craft;
- self-mythologising;
- memory being altered;
- moral laundering;
- revenge through phrasing.

### Required helper

```renpy
label book1_author_thought(text, linger=True):
    $ store.book1_author_thought = text
    return
```

Optional clear helper:

```renpy
label book1_clear_author_thought():
    $ store.book1_author_thought = ""
    return
```

### Presentation

Author thoughts should not appear as normal manuscript text.

They should render as marginalia or pencilled composition notes:

- smaller than body prose;
- italic or handwritten-style if available;
- warm grey/brown ink;
- visually separate from manuscript prose;
- no speaker name;
- no quotation marks;
- sparse and controlled.

Example display text:

```text
No. Too merciful. Make the room complicit.
```

### Usage rules

Use 2-5 author thoughts per writing event.

Good uses:

```renpy
call book1_author_thought("Not listened. Listening is a servant's crime. Witnessing is a writer's privilege.")
```

```renpy
call book1_author_thought("Too clean. The page wants teeth.")
```

```renpy
call book1_author_thought("There. Let the lie wear gloves.")
```

Do not let author thoughts become a second full prose track.

### State rule

Author thoughts may branch based on existing state, but must not create new route-critical state.

Allowed:

```renpy
if story.day2_contraband_state == "stolen_wearing":
    call book1_author_thought("No one saw. That is not the same as innocence.")
```

Forbidden:

```renpy
$ story.book1_author_thought_seen = True
```

---

## Module D: Visual Controller

### Existing component

```renpy
label book1_set_page_image(image_name="ui_book_cover"):
```

### Required direction

Keep `book1_set_page_image(...)` as a compatibility wrapper, but add a higher-level visual API.

### New preferred helper

```renpy
label book1_set_visual(image_name="ui_book_cover", mode="cover", caption="", transition="dissolve"):
    $ store.book1_page_image = image_name
    $ store.book1_page_mode = mode
    $ store.book1_plate_caption = caption
    call book1_apply_visual_transition(transition)
    return
```

Compatibility wrapper:

```renpy
label book1_set_page_image(image_name="ui_book_cover"):
    call book1_set_visual(image_name=image_name, mode="cover", caption="", transition="none")
    return
```

### Convenience helpers

```renpy
label book1_show_cover():
    call book1_set_visual("ui_book_cover", mode="cover", caption="", transition="dissolve")
    return
```

```renpy
label book1_show_tableau(image_name, caption=""):
    call book1_set_visual(image_name=image_name, mode="tableau", caption=caption, transition="dissolve")
    return
```

```renpy
label book1_show_plate(image_name, caption=""):
    call book1_set_visual(image_name=image_name, mode="plate", caption=caption, transition="fade")
    return
```

```renpy
label book1_show_detail(image_name, caption=""):
    call book1_set_visual(image_name=image_name, mode="detail", caption=caption, transition="dissolve")
    return
```

```renpy
label book1_show_blank(caption=""):
    call book1_set_visual(image_name="ui_book_blank", mode="blank", caption=caption, transition="dissolve")
    return
```

---

## Module E: Page Modes

### Purpose

`book1_page_mode` tells the screen how to interpret and frame the current visual.

### Required MVP modes

```text
cover
tableau
plate
detail
blank
```

### Mode definitions

#### `cover`

Default state.

Used at chapter start or when no specific illustration is active.

#### `tableau`

Original VN/CG style image.

Purpose:

- preserve character fidelity;
- show emotional acting clearly;
- ground the scene in recognisable VN character art.

#### `plate`

Victorian illustrated plate version of the tableau.

Purpose:

- final payoff artifact;
- printed Holywell Street illustration;
- captioned, collectible, authored transformation.

#### `detail`

Optional crop or close-up.

Useful for cheap enhancement:

- hands;
- face;
- notebook;
- lace;
- keyhole;
- letter;
- glass;
- glove;
- ink;
- candle.

#### `blank`

Writing-only mode.

Used when the prose needs quiet focus without image distraction.

---

## Module F: Transition Layer

### Purpose

Transitions should be centralised so the visual language can improve later without rewriting prose labels.

### MVP transition types

```text
none
dissolve
fade
page_turn_stub
ink_spread_stub
```

### Helper

```renpy
label book1_apply_visual_transition(transition="dissolve"):
    if transition == "fade":
        with fade
    elif transition == "dissolve":
        with dissolve
    else:
        pass
    return
```

MVP may implement only `fade`, `dissolve`, and `none`.

`page_turn_stub` and `ink_spread_stub` are named placeholders for later animation upgrades.

---

## Module G: Caption System

### Purpose

Plates need dynamic captions.

Examples:

```text
Plate I - The Conservatory Lever
Plate II - The Hatbox Curse
Plate III - The Lady at the Door
Plate IV - The Fragile Lord
Plate V - A Mask Fixed Forever
```

### Rules

- Captions should be rendered by Ren'Py where possible.
- Do not bake every caption into the image unless required by art direction.
- Captions should be optional.
- Captions should be controlled by Book1 visual state, not prose text parsing.

Required state:

```renpy
default book1_plate_caption = ""
```

---

## Module H: Screen Presenter

### Current state

The current NVL screen already provides the manuscript/page split and framed image slot.

### Required MVP refactor

Remove the lower player stats HUD from the Book1 writing screen.

The Book1 screen should not display:

- anxiety meter;
- corruption meter;
- suspicion breakdown;
- Cora stat portrait;
- player stat bars;
- manuscript progress boxes.

These remain in the hotel HUD/ledger systems.

The book is not a status dashboard. It is the fantasy/artifact space.

### Revised screen priorities

The screen should prioritise:

- manuscript page;
- author thought/marginalia;
- illustration/plate;
- chapter title;
- dynamic caption;
- publisher/footer flavour;
- paper and ink atmosphere.

### Proposed right-side layout

Approximate 1920x1080 layout:

```text
Right panel: x 960-1920

40-160      Masthead / chapter title
190-780     Illustration frame
800-850     Plate caption / image caption
870-980     Publisher footer / price badge / decorative rule
```

The removed HUD space should be given back to the image and caption.

### Dynamic mode styling

The screen should branch based on `book1_page_mode`.

#### `cover`

- show masthead;
- show default cover;
- hide or minimise caption.

#### `tableau`

- show original-style CG;
- use clean frame;
- caption optional.

#### `plate`

- show Victorian plate CG;
- show dynamic plate caption;
- use stronger print framing.

#### `detail`

- show crop/detail image;
- caption optional.

#### `blank`

- show paper, ink, or decorative placeholder.

---

## Module I: Asset Registry

### Purpose

Book1 payoff assets need consistent naming, approval, and fallback behaviour.

### Naming convention

```text
cg_book_d{day}_{beat}_tableau
plate_book_d{day}_{beat}
detail_book_d{day}_{beat}_{detail}
ui_book_{component}
```

Examples:

```text
cg_book_d2_hatbox_tableau
plate_book_d2_hatbox_curse
detail_book_d2_lace_hand
cg_book_d3_brush_tableau
plate_book_d3_master_shadow
```

### Required asset categories

#### UI assets

- `ui_book_writing_paper`
- `ui_book_cover`
- `ui_book_blank`
- `ui_illustration_border`
- `ui_price_badge`
- `ui_book_page_bg`
- optional: `ui_book_caption_rule`
- optional: `ui_book_page_shadow`

#### CG assets

- original-style staged tableau images;
- Victorian plate versions;
- optional detail crops.

#### Fallback assets

Every planned Book1 asset should have a manifest fallback so missing art does not break the build.

---

## Module J: Import/Export Interface

### Purpose

Book1 should expose a prose package API modelled on the existing book writing export feature, with a future import API for a simple frontend that can author branching book text without hand-editing `.rpy` files.

The runtime format remains Ren'Py labels.

The authoring format should be structured data.

Conceptual flow:

```text
book package JSON/YAML
        -> importer/compiler
book1_day10N_non_canon.rpy labels
        -> runtime
Ren'Py Book1 engine
```

### Export API

Purpose:

> Give me the current Book1 prose structure in a frontend-editable format.

The export should include:

- `book_id`
- `chapter_key`
- `target_file`
- route buckets
- target labels
- prose beats
- author thought beats
- visual beats
- captions
- branch conditions
- approved assets
- validation notes
- metadata compatible with existing Book Engine Import Header conventions.

Example conceptual package:

```json
{
  "schema_version": "book_payload_v1",
  "book_id": "book1",
  "chapter_key": "day2_chapter",
  "target_file": "main-game/non-prod-game/game/days/book1_day102_non_canon.rpy",
  "routes": [
    {
      "bucket": "predator",
      "target_label": "book1_block_day2_predator_core",
      "style_lens": "Carmilla",
      "beats": [
        {
          "type": "prose",
          "text": "Chapter the Second opens upon a lady's hatbox, sealed like a coffin for silk and scandal."
        },
        {
          "type": "thought",
          "text": "Too neat. She would not remember it so cleanly."
        },
        {
          "type": "visual",
          "mode": "tableau",
          "image": "cg_book_d2_hatbox_tableau",
          "caption": ""
        },
        {
          "type": "visual",
          "mode": "plate",
          "image": "plate_book_d2_hatbox_curse",
          "caption": "Plate II - The Hatbox Curse"
        }
      ]
    }
  ]
}
```

### Import API

Purpose:

> Take a validated package and generate/replace the Ren'Py prose labels safely.

The importer should:

- validate schema;
- validate target file;
- validate target label;
- validate known route bucket;
- validate beat types;
- validate approved asset names or fallbacks;
- escape quotes correctly;
- generate valid `call book1_nvl_write_line(...)` calls;
- generate valid `call book1_author_thought(...)` calls;
- generate valid visual helper calls;
- refuse gameplay state mutation;
- preserve or regenerate metadata headers;
- produce a diff or patch before writing.

The frontend should not directly write `.rpy`. It should produce a package. The importer/compiler should compile the package into Ren'Py.

### Beat model

The external authoring unit should be `BookBeat`, not raw paragraph text.

Required beat types:

```text
prose
thought
visual
page_break
branch
note
```

#### `prose`

Compiles to:

```renpy
call book1_nvl_write_line("...", word_delay=_book1_word_delay)
```

#### `thought`

Compiles to:

```renpy
call book1_author_thought("...")
```

#### `visual`

Compiles to one of:

```renpy
call book1_show_cover()
call book1_show_tableau("image_name", caption="...")
call book1_show_plate("image_name", caption="...")
call book1_show_detail("image_name", caption="...")
call book1_show_blank(caption="...")
```

#### `page_break`

MVP should avoid manual page breaks where possible because central pagination already exists. If supported later, it should compile to a central helper, not raw `nvl clear` inside arbitrary prose.

#### `branch`

Represents conditional content based on existing `story` or `player` fields.

Import compiler must generate valid Ren'Py `if` / `elif` / `else` blocks.

#### `note`

Authoring-only note. Does not compile into runtime output.

---

## Narrative Payload Model

### Hotel trigger

Each Book1 payoff should be grounded in a prior hotel event.

Examples:

- witnessed intimacy;
- stolen object;
- suspicion spike;
- class humiliation;
- private conversation;
- near discovery;
- physical service task;
- moral compromise;
- betrayal or protection of Missy;
- Gideon/Vance/Stern pressure beat.

No Book1 payoff should exist as a random adult scene.

### Emotional conversion categories

Each writing event should convert the hotel trigger into one primary emotional payload.

#### Discovery

Cora sees something forbidden.

Book expression:

- keyholes;
- curtains;
- thresholds;
- half-open doors;
- staged voyeurism;
- plate titles like `The Discovery` or `The House Confesses`.

#### Power

Cora is controlled, tested, or chooses control.

Book expression:

- hand at chin;
- glove on wrist;
- desk confrontation;
- command/submission language;
- formal posture under erotic pressure.

#### Risk

Cora almost gets caught.

Book expression:

- shadow;
- footsteps;
- hidden figure;
- breath held behind a door;
- suspicion as gothic dread.

#### Desire

Cora is fascinated by beauty, intimacy, luxury, or transgression.

Book expression:

- dressing room;
- mirror;
- loosened gown;
- perfume;
- lamplight;
- tactile detail.

#### Class revenge

Cora transforms service humiliation into gothic punishment or pulp spectacle.

Book expression:

- Sweeney-like machinery;
- Ripper-like social dissection;
- Jekyll/Hyde masks;
- Frankenstein stitching;
- Dracula-like possession;
- Carmilla-like intimate feeding.

### Gothic seed layer

The public domain story seeds should be used as symbolic lenses, not straight adaptation.

The player should feel:

> This has Sweeney Todd energy.

Not:

> This is just Sweeney Todd with new names.

Recommended usage:

- emotional/thematic abstraction: default;
- recognisable motifs: occasional;
- direct plot imitation: rare.

---

## Art Direction Requirements

### Original-style tableau

Purpose:

- preserve character fidelity;
- show emotional acting clearly;
- ground the scene in recognisable VN character art.

Style:

- current house sprite/CG style;
- character-faithful;
- readable poses;
- clear expressions;
- strong 2-second read.

### Victorian plate version

Purpose:

- transform the tableau into a forbidden publication artifact;
- create the adult/penny dreadful payoff;
- make the scene feel authored, printed, collectible.

Style:

- faux Victorian illustrated plate;
- warm paper;
- dark sepia/charcoal ink;
- controlled crosshatching;
- ornamental border or printed frame;
- dynamic caption;
- faces kept cleaner than clothes/backgrounds;
- print treatment, not full identity-destroying redraw.

### Relationship between tableau and plate

The tableau is the source of truth.

The plate is the printed transformation.

Pipeline:

```text
storyboard -> pose render -> assembled tableau -> plate treatment -> cleanup -> Ren'Py asset registration
```

Do not rely on the plate pass to solve pose, anatomy, expression, or character identity.

---

## MVP Content Scope

Recommended MVP target:

```text
4-5 major Book1 payoff events
```

Each event should include:

- one hotel trigger;
- one route-aware prose block;
- 2-5 author thought fragments;
- one original-style staged tableau;
- one Victorian plate version;
- one dynamic plate caption;
- optional cheap detail crop;
- optional gallery unlock stub.

### Minimum viable payload

```text
3 Book1 payoff events
```

This is enough to test whether the system works, but may feel thin if Book1 is the main adult payload.

### Strong MVP payload

```text
5 Book1 payoff events
```

This better tests the value proposition.

### Avoid for first MVP

- 15-20 fully finished plate scenes;
- 3-4 unique CGs per writing session;
- bespoke transitions per event;
- fully animated page turns;
- complex gallery UI;
- heavy branching image variants for every state.

Rendering many pose concepts is fine if rendering is cheap. Only promote the strongest into final assembled CGs and plate assets.

---

## Authoring Rules

### Writers can request image cues

Allowed:

```renpy
call book1_show_tableau("cg_book_d2_hatbox_tableau")
call book1_show_plate("plate_book_d2_hatbox_curse", caption="Plate II - The Hatbox Curse")
```

### Writers can request author thought beats

Allowed:

```renpy
call book1_author_thought("No. Too clean. The page wants teeth.")
```

### Writers must not hide image triggers in prose

Forbidden:

```text
[SHOW CG HERE]
{plate:hatbox}
<image=...>
```

Image changes must remain explicit Ren'Py calls or structured visual beats in the import/export package.

### Prose labels must not mutate gameplay state

Still forbidden inside Book1 prose:

- changing `story`;
- changing `player`;
- changing `time_manager`;
- spending fuel;
- completing chapters;
- ending time slots;
- routing day progression.

Day scripts own gameplay state.

Book1 owns presentation and manuscript rendering.

---

## Example Runtime Sequence

```renpy
label book1_block_day2_predator_core:

    call book1_show_cover()
    call book1_nvl_write_line("Chapter the Second opens upon a lady's hatbox, sealed like a coffin for silk and scandal.", word_delay=_book1_word_delay)

    call book1_author_thought("Too neat. She would not remember it so cleanly.")
    call book1_nvl_write_line("The tea service steams; every cup rings as if the house itself were counting who shall be ruined before the cakes grow cold.", word_delay=_book1_word_delay)

    call book1_show_tableau("cg_book_d2_hatbox_tableau")
    call book1_nvl_write_line("Coralie lifts the lace as though innocence were a thing one could hold by two fingers.", word_delay=_book1_word_delay)

    call book1_author_thought("There. Let the lie wear gloves.")
    call book1_show_plate("plate_book_d2_hatbox_curse", caption="Plate II - The Hatbox Curse")
    call book1_nvl_write_line("The reader is meant to blush - and then turn the page anyway.", word_delay=_book1_word_delay)

    call book1_clear_author_thought()
    return
```

---

## Required Engine State

Add or confirm:

```renpy
default book1_page_image = "ui_book_cover"
default book1_page_mode = "cover"
default book1_plate_caption = ""
default book1_chapter_title = ""
default book1_author_thought = ""
default book1_show_stats = False
default _book1_word_delay = 0.04
default _book1_page_line_count = 0
default _book1_page_line_limit = 4
```

Optional future state:

```renpy
default book1_current_plate_id = None
default book1_unlocked_plates = []
default book1_transition_mode = "dissolve"
default book1_current_book = "book1"
```

---

## Required Labels / API

### Existing, retained

```renpy
label book1_write_chapter(chapter_key="day1_chapter", current_day=101, word_delay=0.04, include_debug=False):
```

```renpy
label book1_nvl_write_line(line, word_delay=0.04):
```

```renpy
label book1_set_page_image(image_name="ui_book_cover"):
```

### New preferred runtime API

```renpy
label book1_set_visual(image_name="ui_book_cover", mode="cover", caption="", transition="dissolve"):
```

```renpy
label book1_show_cover():
```

```renpy
label book1_show_tableau(image_name, caption=""):
```

```renpy
label book1_show_plate(image_name, caption=""):
```

```renpy
label book1_show_detail(image_name, caption=""):
```

```renpy
label book1_show_blank(caption=""):
```

```renpy
label book1_author_thought(text, linger=True):
```

```renpy
label book1_clear_author_thought():
```

Optional:

```renpy
label book1_unlock_plate(plate_id):
```

```renpy
label book1_apply_visual_transition(transition="dissolve"):
```

---

## Implementation Phases

### Phase 1: Runtime helpers

Add:

- `book1_page_mode`
- `book1_plate_caption`
- `book1_chapter_title`
- `book1_author_thought`
- `book1_set_visual(...)`
- `book1_show_cover(...)`
- `book1_show_tableau(...)`
- `book1_show_plate(...)`
- `book1_show_detail(...)`
- `book1_author_thought(...)`
- `book1_clear_author_thought(...)`

Keep `book1_set_page_image(...)` as compatibility wrapper.

### Phase 2: Screen refactor

Modify the Book1 NVL screen:

- remove lower stats HUD;
- enlarge illustration area;
- add caption region;
- add author thought/marginalia display;
- branch display based on `book1_page_mode`;
- preserve existing text rendering.

### Phase 3: Package schema

Define the external authoring package format.

Do not build the frontend yet. Define the schema and compiler expectations first.

### Phase 4: Export/import CLI

Build scripts before any UI frontend:

```powershell
python scripts/book1_export.py --chapter day2_chapter
python scripts/book1_import.py path/to/book_package.json
```

The import script should validate and generate Ren'Py label code.

### Phase 5: One vertical slice

Build one complete writing payoff:

- hotel trigger;
- route-aware prose;
- author thoughts;
- tableau image;
- plate image;
- caption;
- transition;
- return flow.

This proves the pipeline before scaling content.

### Phase 6: MVP payload set

Produce 4-5 selected writing payoff events.

Each gets:

- route-aware prose;
- sparse author thoughts;
- one tableau;
- one plate;
- one caption;
- fallback assets.

### Phase 7: Polish/backlog

Add later:

- real page-turn animation;
- ink-spread transformation;
- audio stingers;
- gallery;
- plate unlock notifications;
- detail crops;
- alternate captions;
- multi-book support;
- simple frontend for branch authoring.

---

## Testing Requirements

### Engine tests

For each chapter:

- route resolves to a valid label;
- no missing labels;
- no parse errors;
- no page overflow;
- word reveal works;
- visual helper calls do not break NVL rendering;
- fallback image appears if asset missing;
- author thought helper does not mutate gameplay state.

### Presentation tests

For each page mode:

- `cover` displays correctly;
- `tableau` displays correctly;
- `plate` displays correctly;
- `detail` displays correctly;
- `blank` displays correctly;
- caption appears only when expected;
- author thought appears in the intended marginalia position;
- text remains readable;
- image is large enough to feel rewarding;
- no player stats HUD appears during Book1 writing mode.

### Import/export tests

For package tooling:

- export current labels to valid package format;
- import package into valid Ren'Py label code;
- reject unknown beat types;
- reject unknown assets without fallback;
- reject gameplay state mutation;
- escape quotes correctly;
- preserve metadata headers;
- produce a diff before writing.

### MVP loop tests

For each major writing event:

- prior hotel choice is reflected;
- prose transformation is legible;
- author thought clarifies Cora's transformation process;
- adult payoff feels earned;
- plate caption matches scene;
- image does not feel random;
- return to hotel loop is clean.

---

## Acceptance Criteria

Book1 is MVP-ready when:

1. The hotel loop clearly feeds the writing event.
2. The writing event visibly transforms player choices into manuscript content.
3. The writing UI feels like a dedicated authorship space, not a stats screen.
4. At least 4 major writing payoffs include prose and image payload.
5. At least 3 payoffs include final Victorian plate reveals.
6. Sparse author thoughts make Cora's composition process feel present without crowding the prose.
7. Plate images are large enough and well-framed enough to feel like rewards.
8. All prose routes render without parse errors.
9. All image calls have manifest fallbacks.
10. The runtime API can add more plates later without changing core routing.
11. The prose package schema can represent prose, thought, and visual beats.
12. The player can understand why this adult payoff came from this hotel day.

---

## Final Design Statement

Book1 should be treated as the MVP's core payload layer: a modular manuscript engine where hotel pressure is transformed into erotic gothic authorship.

The system should preserve its existing strengths:

- label-based routing;
- explicit prose blocks;
- central word reveal;
- central pagination;
- explicit image calls.

The MVP upgrade is a presentation and authoring promotion:

- remove the stats HUD from the writing screen;
- centre the book as an escape space;
- expand the visual plate area;
- add page modes and captions;
- add sparse Cora author-thought marginalia;
- formalise tableau-to-plate reveals;
- define an import/export package model for future frontend editing;
- keep all modules independently replaceable.

The target experience is:

> The hotel creates the wound.  
> The book turns it into art.  
> The plate makes it feel forbidden, authored, and worth the trouble.
