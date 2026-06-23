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
- Prose lives in `book1_block_*` labels in per-day Book1 files.
- Day scripts own fuel checks, manuscript completion, stat changes, routing, and post-writing flow.
- Book1 prose labels should not mutate `story`, `player`, `time_manager`, or persistent state.
- Image changes are explicitly supported through `book1_set_page_image(...)`.

This architecture is sound and should be preserved.

The main MVP correction is pagination ownership. `book1_nvl_write_line(...)` should remain as the low-level reveal primitive, but the MVP should not rely on a hardcoded rendered-line counter such as `_book1_page_line_limit = 4` as the primary pagination mechanism. Rendered line count changes with font, localization, text size, and layout width. Page flow should instead be controlled through authored page beats via `book1_write_beat(..., page_break=True)`.

`_book1_page_line_limit` may remain as a defensive fallback or debug guard, but it should not be treated as the source of truth for final page composition.

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

The MVP should not require separate premium tableau and plate art for every payoff. The approved tableau should be the source image. The default plate should be a runtime presentation mode using monochrome/sepia treatment, paper texture, hatch overlay, border, and Ren'Py-rendered caption. Hand-finished `plate_book_*` assets are reserved for tentpole rewards, not required for every MVP beat.

### Existing screen architecture

The current Book1 NVL screen has:

- left manuscript text area;
- right penny dreadful title/cover area;
- framed illustration image;
- price/publisher footer;
- lower player stats HUD showing portrait, inkwell, corruption, and anxiety.

The revised MVP direction should remove the player stats HUD from the Book1 writing screen. The book should feel like Cora's escape from the hotel pressure loop, not another pressure dashboard.

The screen still needs to make the hotel-to-book connection legible. That connection should be communicated through prose framing, chapter subtitles, author thought, plate captions, and masthead language rather than exposed numeric stats.

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

Stats, state flags, and route buckets may still drive routing behind the scenes. They should not dominate the writing presentation.

### 4. The payload must not become a black box

Book1 should not expose numeric stats, but the player must understand why the current chapter, tone, image, or plate emerged from the preceding hotel day.

The solution is prose-level provenance, not a dashboard.

Use subtle narrative tells:

- chapter subtitles;
- masthead variants;
- opening author thought;
- plate captions;
- publisher/footer flavour;
- route-specific border or ornament variants later.

Every major Book1 payoff should include at least one visible route-provenance cue within the first screen.

Examples:

```text
CHAPTER THE SECOND
— Derived from a Night of Contraband —
```

```text
CHAPTER THE THIRD
— Written Under the Pressure of Watching Eyes —
```

```text
CHAPTER THE FOURTH
— After an Afternoon of Silk, Service, and Humiliation —
```

### 5. Modular enhancement over hard rewrites

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

## MVP Player Experience

### Flow

A writing event should follow this general sequence:

1. Hotel gameplay creates narrative material.
2. The day script calls `book1_write_chapter(...)`.
3. The screen shifts away from hotel UI into Book1 presentation.
4. The chapter title and route-provenance subtitle appear.
5. Manuscript prose reveals word by word through `book1_write_beat(...)`.
6. Sparse author-thought fragments appear alongside the prose they comment on.
7. The page image changes at explicit visual beats.
8. A staged original-style tableau appears.
9. The current tableau transitions into runtime Victorian plate mode, or into a hand-finished plate asset for tentpole scenes.
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
- a lore codex;
- an arbitrary scene selected by hidden mechanics.

## Module Overview

Book1 should be treated as a modular payload system with these major modules:

1. **Prose Router** - resolves chapter key and route bucket to prose label.
2. **Prose Renderer / Narrative Beat API** - renders manuscript prose and unifies prose, optional author thought, and intentional page breaks through `book1_write_beat(...)`.
3. **Author Thought Renderer** - shows sparse Cora composition-thought fragments.
4. **Visual Controller** - handles cover/tableau/plate/detail image modes and captions.
5. **Page Modes** - defines cover/tableau/plate/detail/blank presentation behaviour.
6. **Transition Layer** - centralises visual transitions and future animation hooks.
7. **Caption System** - renders dynamic plate and image captions.
8. **Screen Presenter** - renders the writing screen, manuscript page, image area, and captions.
9. **Payload Reflection Bridge** - makes hotel-to-book causality legible without showing stats.
10. **Asset Registry** - manages approved Book1 images, runtime plate overlays, and fallbacks.
11. **Import/Export Interface** - future tooling layer for external prose editing.
12. **Gallery/Unlock Stub** - optional future layer for unlocked plates.

Each module should have a narrow API and avoid hidden coupling.

## Module A: Prose Router

### Existing component

```renpy
label book1_write_chapter(chapter_key="day1_chapter", current_day=101, word_delay=0.04, include_debug=False):
```

### Responsibility

- Clear NVL at start and end.
- Initialise Book1 runtime display state.
- Resolve the route bucket.
- Resolve route-provenance copy for the masthead/subtitle.
- Call the appropriate `book1_block_*` label.
- Preserve existing call signature where possible.

### Required MVP changes

Extend initialisation to include presentation state:

```renpy
$ store._book1_word_delay = word_delay
$ store._book1_page_line_count = 0
$ store._book1_page_line_limit = 4 # defensive fallback only, not primary pagination
$ store.book1_page_image = "ui_book_cover"
$ store.book1_page_mode = "cover"
$ store.book1_plate_caption = ""
$ store.book1_chapter_title = ""
$ store.book1_chapter_subtitle = ""
$ store.book1_author_thought = ""
$ store.book1_author_thought_id = 0
$ store.book1_route_provenance = ""
$ store.book1_show_stats = False
```

The exact names can change, but the separation is important:

- `book1_page_image` = what image is displayed;
- `book1_page_mode` = how the image is framed/interpreted;
- `book1_plate_caption` = dynamic caption text;
- `book1_chapter_title` = dynamic chapter/masthead text;
- `book1_chapter_subtitle` = route-provenance subtitle;
- `book1_author_thought` = sparse composition-thought text;
- `book1_author_thought_id` = increments when thought changes, allowing fade/replay logic;
- `book1_route_provenance` = human-readable source cue for the payload;
- `book1_show_stats` = should remain false for the revised MVP screen.

### State isolation rule

Book1 reads resolved hotel state. It does not mutate hotel state.

Allowed:

```renpy
if story.day2_contraband_state == "stolen_wearing":
    call book1_write_beat(
        "The ribbon still remembered the shape of a dishonest hand.",
        thought="No one saw. That is not the same as innocence."
    )
```

Forbidden:

```renpy
$ story.day2_contraband_state = "book_processed"
$ player.anxiety += 1
$ time_manager.advance_slot()
```

Day scripts own gameplay state. Book1 owns presentation and manuscript rendering.

## Module B: Prose Renderer

### Existing component

```renpy
label book1_nvl_write_line(line, word_delay=0.04):
```

### Responsibility

- Apply word-by-word reveal.
- Display manuscript prose.
- Preserve existing prose label compatibility.
- Avoid gameplay state mutation.

### MVP correction

Keep `book1_nvl_write_line(...)`, but treat it as a low-level text reveal primitive.

Do not rely on `_book1_page_line_limit = 4` as the primary pagination system. A fixed rendered-line counter will break when:

- text localises longer than expected;
- font size changes;
- the paper frame changes;
- Ren'Py wrapping changes;
- a paragraph wraps into more visual lines than the author expected.

The MVP should use intentional `page_break` beats instead of pretending the engine can reliably infer page layout from line count.

### New preferred wrapper

```renpy
label book1_write_beat(text, thought=None, word_delay=None, page_break=False, clear_thought=False):
    if page_break:
        nvl clear
        $ store._book1_page_line_count = 0

    if word_delay is None:
        $ word_delay = store._book1_word_delay

    if thought is not None:
        $ store.book1_author_thought = thought
        $ store.book1_author_thought_id += 1

    call book1_nvl_write_line(text, word_delay=word_delay)

    if clear_thought:
        $ store.book1_author_thought = ""

    return
```

### Usage rule

Most Book1 prose should use `book1_write_beat(...)`, not raw `book1_nvl_write_line(...)`.

Preferred:

```renpy
call book1_write_beat(
    "The tea service steams; every cup rings as if the house itself were counting who shall be ruined before the cakes grow cold.",
    thought="Not listened. Witnessed."
)
```

Allowed for compatibility or simple legacy prose:

```renpy
call book1_nvl_write_line("The tea service steams...", word_delay=_book1_word_delay)
```

### Page break rule

Page breaks should be explicit authoring decisions:

```renpy
call book1_write_beat(
    "Chapter the Second opens upon a lady's hatbox, sealed like a coffin for silk and scandal.",
    thought="Too neat. She would not remember it so cleanly.",
    page_break=True
)
```

Manual `nvl clear` calls should be avoided inside prose labels except inside central helpers. This keeps page behaviour testable and replaceable later.

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

### Required helpers

Standalone helpers may remain available:

```renpy
label book1_author_thought(text, linger=True):
    $ store.book1_author_thought = text
    $ store.book1_author_thought_id += 1
    return
```

```renpy
label book1_clear_author_thought():
    $ store.book1_author_thought = ""
    return
```

But the preferred MVP usage is through `book1_write_beat(...)`:

```renpy
call book1_write_beat(
    "The hallway was quiet enough to hear the silver settle.",
    thought="No. Quiet is not innocence. Quiet is opportunity."
)
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
- sparse and controlled;
- alpha fade-in when changed.

Example display text:

```text
No. Too merciful. Make the room complicit.
```

### Timing rule

Author thought should normally appear alongside the paragraph it comments on, not as a separate click beat.

Bad default:

```renpy
call book1_author_thought("Too clean. The page wants teeth.")
call book1_nvl_write_line("The tea service steams...")
```

Preferred:

```renpy
call book1_write_beat(
    "The tea service steams...",
    thought="Too clean. The page wants teeth."
)
```

This prevents the thought from appearing too early, being skipped too quickly, or distracting from the word-by-word reveal.

### Usage rules

Use 2-5 author thoughts per writing event.

Good uses:

```renpy
call book1_write_beat(
    "The door had not opened; the house had merely decided to confess.",
    thought="Not listened. Listening is a servant's crime. Witnessing is a writer's privilege."
)
```

```renpy
call book1_write_beat(
    "The room was too clean to be innocent.",
    thought="Too clean. The page wants teeth."
)
```

```renpy
call book1_write_beat(
    "Her lie was fitted as neatly as a glove.",
    thought="There. Let the lie wear gloves."
)
```

Do not let author thoughts become a second full prose track.

### State rule

Author thoughts may branch based on existing state, but must not create new route-critical state.

Allowed:

```renpy
if story.day2_contraband_state == "stolen_wearing":
    call book1_write_beat(
        "The lace kept its counsel.",
        thought="No one saw. That is not the same as innocence."
    )
```

Forbidden:

```renpy
$ story.book1_author_thought_seen = True
```

### Screen rule

The screen should render `book1_author_thought`. It should not mutate state or run timing logic. All state changes should happen in labels/helpers.

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

### Chapter title helper

```renpy
label book1_set_chapter_title(title="", subtitle=""):
    $ store.book1_chapter_title = title
    $ store.book1_chapter_subtitle = subtitle
    return
```

Use `subtitle` for route-provenance copy.

Example:

```renpy
call book1_set_chapter_title(
    title="CHAPTER THE SECOND",
    subtitle="Derived from a Night of Contraband"
)
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
label book1_show_plate(image_name=None, caption=""):
    if image_name is None:
        $ image_name = store.book1_page_image
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

### Plate asset rule

`book1_show_plate(...)` should work with either:

1. the current tableau image, treated as a plate by the screen; or
2. a hand-finished `plate_book_*` image passed explicitly.

MVP default:

```renpy
call book1_show_tableau("cg_book_d2_hatbox_tableau")
call book1_show_plate(caption="Plate II - The Hatbox Curse")
```

Tentpole override:

```renpy
call book1_show_tableau("cg_book_d2_hatbox_tableau")
call book1_show_plate("plate_book_d2_hatbox_curse", caption="Plate II - The Hatbox Curse")
```

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
- ground the scene in recognisable VN character art;
- act as the source of truth for plate treatment.

#### `plate`

Victorian illustrated plate presentation.

Purpose:

- final payoff artifact;
- printed Holywell Street illustration;
- captioned, collectible, authored transformation;
- avoid requiring duplicate premium art for every MVP payoff.

MVP default:

- reuse the current tableau image;
- apply runtime sepia/monochrome treatment;
- add paper texture overlay;
- add hatch/noise overlay;
- add ornamental border;
- render caption dynamically.

Tentpole option:

- use a hand-finished `plate_book_*` asset when the scene is important enough to justify cleanup.

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
plate_transform_stub
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

`page_turn_stub`, `ink_spread_stub`, and `plate_transform_stub` are named placeholders for later animation upgrades.

### Plate transition rule

The tableau-to-plate moment should be implemented as a mode change first, not a mandatory asset swap.

MVP:

```renpy
call book1_show_tableau("cg_book_d2_hatbox_tableau")
call book1_write_beat("Coralie lifts the lace as though innocence were a thing one could hold by two fingers.")
call book1_show_plate(caption="Plate II - The Hatbox Curse")
```

Later, `plate_transform_stub` can become a real ink-spread or print-registration animation without changing prose labels.

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
- route-provenance subtitle;
- dynamic caption;
- publisher/footer flavour;
- paper and ink atmosphere.

### Proposed right-side layout

Approximate 1920x1080 layout:

```text
Right panel: x 960-1920

40-125      Masthead / chapter title
125-165     Route-provenance subtitle
190-780     Illustration frame
800-850     Plate caption / image caption
870-980     Publisher footer / price badge / decorative rule
```

The removed HUD space should be given back to the image and caption.

### Dynamic mode styling

The screen should branch based on `book1_page_mode`.

#### `cover`

- show masthead;
- show chapter subtitle if present;
- show default cover;
- hide or minimise caption.

#### `tableau`

- show original-style CG;
- use clean frame;
- caption optional.

#### `plate`

- show current image with runtime plate treatment, unless the image itself is already a hand-finished plate;
- show dynamic plate caption;
- use stronger print framing;
- show paper texture, hatch/noise overlay, and ornamental border.

Screen-side sketch:

```renpy
if book1_page_mode == "plate":
    add book1_page_image at book1_plate_treatment
    add "ui_book_plate_paper_overlay"
    add "ui_book_plate_hatch_overlay"
    add "ui_illustration_border_plate"
else:
    add book1_page_image
```

Transform sketch:

```renpy
transform book1_plate_treatment:
    matrixcolor SepiaMatrix("#ead7a4") * ContrastMatrix(1.12)
```

Do not depend on runtime filtering to fix bad posing, anatomy, facial acting, or composition. The source tableau must already work.

#### `detail`

- show crop/detail image;
- caption optional.

#### `blank`

- show paper, ink, or decorative placeholder.

### Author thought display

Author thought should render in a dedicated marginalia container.

Suggested behaviour:

- visible only when `book1_author_thought` is non-empty;
- small, italic, pencilled, visually separate from manuscript prose;
- fade in when `book1_author_thought_id` changes;
- no gameplay state mutation inside the screen.

The helper label controls state. The screen only renders it.

## Module I: Payload Reflection Bridge

### Purpose

Make the hotel-to-book conversion legible without restoring a stats HUD.

The player should understand why this chapter, tone, image, or plate happened, but should not see a dashboard inside the book.

### Core rule

Book1 never mutates hotel state. It reads resolved state, route buckets, and flags, then translates them into manuscript presentation.

The translation should be visible through:

- chapter subtitle;
- masthead wording;
- opening author thought;
- plate caption;
- publisher/footer flavour;
- route-specific ornamentation later.

### Required MVP cue

Every major Book1 payoff must include at least one route-provenance cue within the first screen.

Examples:

```renpy
call book1_set_chapter_title(
    title="CHAPTER THE SECOND",
    subtitle="Derived from a Night of Contraband"
)
```

```renpy
call book1_set_chapter_title(
    title="CHAPTER THE THIRD",
    subtitle="Written Under the Pressure of Watching Eyes"
)
```

```renpy
call book1_write_beat(
    "The corridor in Coralie's book is narrower than the one she remembers.",
    thought="Because the real one had room to escape. This one should not."
)
```

### Good feedback style

Good:

```text
— Derived from a Night of Contraband —
```

Good:

```text
Plate III - The Door That Listened
```

Good:

```text
Printed for those who know the value of a closed mouth.
```

Bad:

```text
Risk Route: 72%
Suspicion: High
Desire Flag: True
```

### Debug exception

Debug or harness builds may show route labels, state buckets, and validation notes. Player-facing builds should not.

## Module J: Asset Registry

### Purpose

Book1 payoff assets need consistent naming, approval, fallback behaviour, and a cheap runtime plate path.

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
- `ui_illustration_border_plate`
- `ui_price_badge`
- `ui_book_page_bg`
- `ui_book_plate_paper_overlay`
- `ui_book_plate_hatch_overlay`
- optional: `ui_book_caption_rule`
- optional: `ui_book_page_shadow`

#### CG assets

MVP required:

- original-style staged tableau images.

MVP optional:

- hand-finished Victorian plate versions;
- cheap detail crops.

Do not require both a tableau and a separate premium plate for every payoff.

#### Runtime plate treatment

Every approved tableau should be compatible with runtime plate treatment.

Runtime plate treatment consists of:

- sepia/desaturation matrix;
- contrast adjustment;
- paper texture overlay;
- hatch/noise overlay;
- ornamental border;
- dynamic caption.

This gives the scene a printed artifact feel without doubling premium art production.

#### Fallback assets

Every planned Book1 asset should have a manifest fallback so missing art does not break the build.

Fallback examples:

```text
cg_book_missing_tableau -> ui_book_blank
plate_book_missing      -> current tableau in runtime plate mode
detail_book_missing     -> ui_book_blank
```

### Promotion rule

Only promote a runtime plate into a hand-finished `plate_book_*` asset when:

- the scene is a tentpole reward;
- the runtime filter damages facial readability;
- the hatch overlay muddies the image;
- the plate is intended for gallery/marketing use;
- the MVP test proves the payoff is worth extra cleanup.

## Module K: Import/Export Interface

### Purpose

Book1 should eventually expose a prose package API modelled on the existing book writing export feature, with a future import API for a simple frontend that can author branching book text without hand-editing `.rpy` files.

This is no longer an MVP implementation dependency.

For the first MVP payload set, write the 4-5 major Book1 chapters directly in native Ren'Py labels using the runtime APIs. Validate the core loop before building a compiler.

The runtime format remains Ren'Py labels.

The future authoring format should be structured data.

Conceptual flow:

```text
book package JSON/YAML
        -> importer/compiler
book1_day10N_non_canon.rpy labels
        -> runtime
Ren'Py Book1 engine
```

### MVP stance

Do now:

- design labels around `book1_write_beat(...)`;
- keep visual beats explicit;
- keep page breaks explicit;
- keep prose labels easy to export later;
- document the package shape as a future contract.

Do not do now:

- build a full CLI compiler;
- build a frontend;
- spend days parsing five handwritten labels;
- make automation a blocker for content validation.

### Export API

Future purpose:

> Give me the current Book1 prose structure in a frontend-editable format.

The export should include:

- `book_id`
- `chapter_key`
- `target_file`
- route buckets
- target labels
- prose beats
- thought fields attached to prose beats
- visual beats
- captions
- route-provenance text
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
      "provenance": "Derived from a Night of Contraband",
      "beats": [
        {
          "type": "title",
          "title": "CHAPTER THE SECOND",
          "subtitle": "Derived from a Night of Contraband"
        },
        {
          "type": "prose",
          "text": "Chapter the Second opens upon a lady's hatbox, sealed like a coffin for silk and scandal.",
          "thought": "Too neat. She would not remember it so cleanly.",
          "page_break": true
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
          "image": null,
          "caption": "Plate II - The Hatbox Curse"
        }
      ]
    }
  ]
}
```

### Import API

Future purpose:

> Take a validated package and generate/replace the Ren'Py prose labels safely.

The importer should:

- validate schema;
- validate target file;
- validate target label;
- validate known route bucket;
- validate beat types;
- validate approved asset names or fallbacks;
- escape quotes correctly;
- generate valid `call book1_write_beat(...)` calls;
- generate valid visual helper calls;
- generate valid `call book1_set_chapter_title(...)` calls;
- refuse gameplay state mutation;
- preserve or regenerate metadata headers;
- produce a diff or patch before writing.

The frontend should not directly write `.rpy`. It should produce a package. The importer/compiler should compile the package into Ren'Py.

### Beat model

The external authoring unit should be `BookBeat`, not raw paragraph text.

Required future beat types:

```text
title
prose
visual
page_break
branch
note
```

#### `title`

Compiles to:

```renpy
call book1_set_chapter_title(title="...", subtitle="...")
```

#### `prose`

Compiles to:

```renpy
call book1_write_beat("...", thought="...", page_break=False, clear_thought=False)
```

A separate `thought` beat should be avoided for normal prose flow. Author thought belongs beside the paragraph it comments on.

#### `visual`

Compiles to one of:

```renpy
call book1_show_cover()
call book1_show_tableau("image_name", caption="...")
call book1_show_plate(caption="...")
call book1_show_plate("plate_image_name", caption="...")
call book1_show_detail("image_name", caption="...")
call book1_show_blank(caption="...")
```

#### `page_break`

Avoid standalone page-break beats where possible. Prefer `page_break: true` on the prose beat that begins the new page.

If supported later, it should compile to a central helper, not raw `nvl clear` inside arbitrary prose.

#### `branch`

Represents conditional content based on existing `story` or `player` fields.

Import compiler must generate valid Ren'Py `if` / `elif` / `else` blocks.

#### `note`

Authoring-only note. Does not compile into runtime output.

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

### Payload reflection

Book1 does not mechanically mutate the hotel loop. It converts existing hotel state into authored fiction.

For every major payoff, define:

```text
hotel trigger -> emotional conversion -> prose lens -> visual motif -> route-provenance cue
```

Example:

```text
Cora steals/wears contraband lace
-> Risk + Desire
-> Carmilla-like intimate contamination
-> hatbox, lace, gloved lie
-> "Derived from a Night of Contraband"
```

Example:

```text
Cora is nearly discovered eavesdropping
-> Discovery + Risk
-> house-as-witness gothic dread
-> keyhole, floorboards, watching door
-> "Written Under the Pressure of Watching Eyes"
```

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

## Art Direction Requirements

### Original-style tableau

Purpose:

- preserve character fidelity;
- show emotional acting clearly;
- ground the scene in recognisable VN character art;
- provide the visual source of truth for runtime plate treatment.

Style:

- current house sprite/CG style;
- character-faithful;
- readable poses;
- clear expressions;
- strong 2-second read.

### Runtime Victorian plate treatment

Purpose:

- transform the tableau into a forbidden publication artifact;
- create the adult/penny dreadful payoff;
- make the scene feel authored, printed, collectible;
- avoid doubling premium art for every payoff.

Style:

- faux Victorian illustrated plate;
- warm paper;
- dark sepia/charcoal ink;
- controlled hatch/noise overlay;
- ornamental border or printed frame;
- dynamic caption;
- faces kept readable.

Runtime treatment should not be expected to create true hand-drawn crosshatching. It is a presentation layer, not an art replacement.

### Hand-finished Victorian plate version

Purpose:

- premium tentpole reward;
- gallery-worthy final artifact;
- marketing/screenshot asset;
- cleanup when runtime filtering harms the image.

Style:

- faux Victorian illustrated plate;
- warm paper;
- dark sepia/charcoal ink;
- controlled crosshatching;
- ornamental border or printed frame;
- dynamic or baked caption depending on art needs;
- faces kept cleaner than clothes/backgrounds;
- print treatment, not full identity-destroying redraw.

### Relationship between tableau and plate

The tableau is the source of truth.

The plate is the printed transformation.

MVP pipeline:

```text
storyboard -> pose render -> assembled tableau -> runtime plate treatment -> Ren'Py presentation
```

Tentpole pipeline:

```text
storyboard -> pose render -> assembled tableau -> plate treatment -> cleanup -> Ren'Py asset registration
```

Do not rely on the plate pass to solve pose, anatomy, expression, or character identity.

### Production rule

For MVP, every major payoff needs one strong tableau.

A separate hand-finished `plate_book_*` asset is optional. Use it selectively where it materially improves the reward.

## MVP Content Scope

Recommended MVP target:

```text
4-5 major Book1 payoff events
```

Each event should include:

- one hotel trigger;
- one visible route-provenance cue;
- one route-aware prose block;
- 2-5 author thought fragments attached to prose beats;
- one original-style staged tableau;
- one runtime Victorian plate reveal;
- one dynamic plate caption;
- optional hand-finished plate for tentpole scenes;
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
- mandatory separate tableau and plate assets for every payoff;
- 3-4 unique CGs per writing session;
- bespoke transitions per event;
- fully animated page turns;
- complex gallery UI;
- heavy branching image variants for every state;
- full JSON/YAML compiler before the first 4-5 scenes are tested.

Rendering many pose concepts is fine if rendering is cheap. Only promote the strongest into final assembled CGs and optional hand-finished plate assets.

## Authoring Rules

### Writers can request image cues

Allowed:

```renpy
call book1_show_tableau("cg_book_d2_hatbox_tableau")
call book1_show_plate(caption="Plate II - The Hatbox Curse")
call book1_show_plate("plate_book_d2_hatbox_curse", caption="Plate II - The Hatbox Curse")
```

### Writers should use prose beats

Preferred:

```renpy
call book1_write_beat(
    "The tea service steams; every cup rings as if the house itself were counting who shall be ruined before the cakes grow cold.",
    thought="Too clean. The page wants teeth."
)
```

Allowed for compatibility:

```renpy
call book1_nvl_write_line("The tea service steams...", word_delay=_book1_word_delay)
```

### Writers can request author thought beats

Preferred:

```renpy
call book1_write_beat(
    "The door had not opened; the house had merely decided to confess.",
    thought="Not listened. Listening is a servant's crime. Witnessing is a writer's privilege."
)
```

Standalone author thought is allowed only when the thought is meant to linger across multiple prose beats:

```renpy
call book1_author_thought("No. Too clean. The page wants teeth.")
```

### Writers should set route-provenance titles

Allowed:

```renpy
call book1_set_chapter_title(
    title="CHAPTER THE SECOND",
    subtitle="Derived from a Night of Contraband"
)
```

Every major payoff should include at least one early route-provenance cue.

### Writers must not hide image triggers in prose

Forbidden:

```text
[SHOW CG HERE]
{plate:hatbox}
<image=...>
```

Image changes must remain explicit Ren'Py calls or structured visual beats in the future import/export package.

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

## Example Runtime Sequence

```renpy
label book1_block_day2_predator_core:

    call book1_show_cover()

    call book1_set_chapter_title(
        title="CHAPTER THE SECOND",
        subtitle="Derived from a Night of Contraband"
    )

    call book1_write_beat(
        "Chapter the Second opens upon a lady's hatbox, sealed like a coffin for silk and scandal.",
        thought="Too neat. She would not remember it so cleanly.",
        page_break=True
    )

    call book1_write_beat(
        "The tea service steams; every cup rings as if the house itself were counting who shall be ruined before the cakes grow cold.",
        thought="Not listened. Witnessed."
    )

    call book1_show_tableau("cg_book_d2_hatbox_tableau")

    call book1_write_beat(
        "Coralie lifts the lace as though innocence were a thing one could hold by two fingers."
    )

    # MVP default: same tableau, rendered through plate mode by the screen.
    call book1_show_plate(caption="Plate II - The Hatbox Curse")

    call book1_write_beat(
        "The reader is meant to blush - and then turn the page anyway.",
        thought="There. Let the lie wear gloves.",
        clear_thought=True
    )

    return
```

Tentpole variant using a hand-finished plate:

```renpy
call book1_show_tableau("cg_book_d2_hatbox_tableau")
call book1_show_plate("plate_book_d2_hatbox_curse", caption="Plate II - The Hatbox Curse")
```

## Required Engine State

Add or confirm:

```renpy
default book1_page_image = "ui_book_cover"
default book1_page_mode = "cover"
default book1_plate_caption = ""
default book1_chapter_title = ""
default book1_chapter_subtitle = ""
default book1_author_thought = ""
default book1_author_thought_id = 0
default book1_route_provenance = ""
default book1_show_stats = False
default _book1_word_delay = 0.04
default _book1_page_line_count = 0
default _book1_page_line_limit = 4 # defensive fallback only
```

Optional future state:

```renpy
default book1_current_plate_id = None
default book1_unlocked_plates = []
default book1_transition_mode = "dissolve"
default book1_current_book = "book1"
default book1_runtime_plate_enabled = True
```

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
label book1_write_beat(text, thought=None, word_delay=None, page_break=False, clear_thought=False):
```

```renpy
label book1_set_chapter_title(title="", subtitle=""):
```

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
label book1_show_plate(image_name=None, caption=""):
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

## Implementation Phases

### Phase 1: Runtime helpers

Add:

- `book1_page_mode`
- `book1_plate_caption`
- `book1_chapter_title`
- `book1_chapter_subtitle`
- `book1_route_provenance`
- `book1_author_thought`
- `book1_author_thought_id`
- `book1_write_beat(...)`
- `book1_set_chapter_title(...)`
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
- add route-provenance subtitle region;
- add author thought/marginalia display;
- add runtime plate styling for `book1_page_mode == "plate"`;
- branch display based on `book1_page_mode`;
- preserve existing text rendering.

### Phase 3: One vertical slice

Build one complete writing payoff directly in native Ren'Py labels:

- hotel trigger;
- route-aware prose;
- route-provenance subtitle;
- author thoughts attached through `book1_write_beat(...)`;
- tableau image;
- runtime plate reveal;
- caption;
- transition;
- return flow.

This proves the pipeline before scaling content.

### Phase 4: MVP payload set

Produce 4-5 selected writing payoff events.

Each gets:

- route-aware prose;
- visible route-provenance cue;
- sparse author thoughts;
- one tableau;
- runtime plate reveal;
- one caption;
- fallback assets.

Optional:

- hand-finished plate for the strongest scenes;
- detail crop where cheap and useful.

### Phase 5: Package schema notes

Define the external authoring package format as a future contract.

Do not build the frontend yet.

Do not build the compiler yet unless the Ren'Py-authored vertical slice proves the core loop is worth scaling.

### Phase 6: Export/import CLI

Build scripts only after the MVP payload set validates the loop:

```powershell
python scripts/book1_export.py --chapter day2_chapter
python scripts/book1_import.py path/to/book_package.json
```

The import script should validate and generate Ren'Py label code.

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
- simple frontend for branch authoring;
- hand-finished plates for proven tentpole scenes.

## Testing Requirements

### Engine tests

For each chapter:

- route resolves to a valid label;
- no missing labels;
- no parse errors;
- authored page breaks work;
- defensive page overflow guard catches excessive prose;
- word reveal works;
- `book1_write_beat(...)` correctly updates prose, optional thought, and optional page break;
- visual helper calls do not break NVL rendering;
- fallback image appears if asset missing;
- runtime plate mode works with a tableau image;
- author thought helper does not mutate gameplay state.

### Presentation tests

For each page mode:

- `cover` displays correctly;
- `tableau` displays correctly;
- `plate` displays correctly using runtime treatment;
- optional hand-finished `plate_book_*` images display correctly;
- `detail` displays correctly;
- `blank` displays correctly;
- caption appears only when expected;
- route-provenance subtitle appears when expected;
- author thought appears in the intended marginalia position;
- author thought does not distract from the word reveal;
- text remains readable;
- image is large enough to feel rewarding;
- no player stats HUD appears during Book1 writing mode.

### Import/export tests

For future package tooling:

- export current labels to valid package format;
- import package into valid Ren'Py label code;
- reject unknown beat types;
- reject unknown assets without fallback;
- reject gameplay state mutation;
- escape quotes correctly;
- preserve metadata headers;
- produce a diff before writing;
- generate `book1_write_beat(...)`, not separate thought/prose calls unless explicitly required.

### MVP loop tests

For each major writing event:

- prior hotel choice is reflected;
- route-provenance cue appears early;
- prose transformation is legible;
- author thought clarifies Cora's transformation process;
- adult payoff feels earned;
- plate caption matches scene;
- runtime plate treatment feels intentional, not like a cheap filter;
- image does not feel random;
- return to hotel loop is clean.

## Acceptance Criteria

Book1 is MVP-ready when:

1. The hotel loop clearly feeds the writing event.
2. The writing event visibly transforms player choices into manuscript content.
3. The writing UI feels like a dedicated authorship space, not a stats screen.
4. At least 4 major writing payoffs include prose and image payload.
5. At least 3 payoffs include final Victorian plate reveals, using runtime plate treatment or hand-finished plates.
6. Sparse author thoughts make Cora's composition process feel present without crowding the prose.
7. Author thoughts appear alongside the prose they comment on, not as awkward standalone interruptions.
8. Plate images are large enough and well-framed enough to feel like rewards.
9. Every major payoff includes an early route-provenance cue so the player understands why this payload came from this hotel day.
10. All prose routes render without parse errors.
11. All image calls have manifest fallbacks.
12. The runtime API can add more plates later without changing core routing.
13. The prose package schema can represent prose beats with attached thoughts, visual beats, page breaks, and route-provenance text.
14. Book1 prose labels do not mutate gameplay state.
15. The player can understand why this adult payoff came from this hotel day.

## Final Design Statement

Book1 should be treated as the MVP's core payload layer: a modular manuscript engine where hotel pressure is transformed into erotic gothic authorship.

The system should preserve its existing strengths:

- label-based routing;
- explicit prose blocks;
- central word reveal;
- explicit visual calls;
- compatibility with current Book1 labels.

The MVP upgrade is a presentation and authoring promotion:

- remove the stats HUD from the writing screen;
- centre the book as an escape space;
- expand the visual plate area;
- add page modes and captions;
- add route-provenance subtitles so the payload does not feel arbitrary;
- add sparse Cora author-thought marginalia attached to prose beats;
- use explicit page breaks through `book1_write_beat(...)` rather than fragile hard line-count pagination;
- formalise tableau-to-runtime-plate reveals;
- reserve hand-finished plates for tentpole rewards;
- define an import/export package model for future frontend editing;
- keep all modules independently replaceable.

The target experience is:

> The hotel creates the wound.  
> The book turns it into art.  
> The plate makes it feel forbidden, authored, and worth the trouble.

The architectural rule is:

> Book1 reads hotel state, translates it into authored fiction, and presents the result through prose, marginalia, masthead, tableau, and plate treatment. It does not mutate gameplay state, expose numeric stats, or require duplicate premium art for every payoff.
