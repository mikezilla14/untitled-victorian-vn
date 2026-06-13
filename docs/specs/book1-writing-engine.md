# Spec: Book1 Label-Based Writing Engine

## Purpose

Define the MVP Book1 writing artifact for Cora's manuscript scenes. Book1 renders NVL manuscript prose from gameplay state while keeping the authoring surface readable for writers.

The active MVP architecture is label-based:

- Ren'Py labels are the unit of prose variation.
- `book1.CHAPTER_BLOCKS` maps chapter keys and state buckets to prose labels.
- `book1_write_chapter(...)` owns routing, word reveal, and pagination.
- prose labels render text only and return cleanly.

The older inline macro/payload direction is retired and removed from the active non-prod Book1 engine. New Book1 work must not add prose to `BOOK1_PAYLOADS` or depend on curly-brace prose macros.

Book/chapter writing prompt calls should enter through `writer_write_book` or the `book_writing_engine` skill. Those flows request a Book Writing Context Packet from `non_prod_code_agent`, then route prose through the Writers' Room and gates before the code agent wraps approved prose into `book1_block_*` labels.

## Target Scope

- Engine/runtime file: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/book1_non_canon.rpy`
- Per-day prose files:
  - `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/book1_day101_non_canon.rpy`
  - `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/book1_day102_non_canon.rpy`
  - `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/book1_day103_non_canon.rpy`
  - `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/book1_day104_non_canon.rpy`
  - `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/book1_day105_non_canon.rpy`
- Gameplay call sites: `day101_non_canon.rpy` through `day105_non_canon.rpy`
- Direct harness: `test_day2_writing_non_canon.rpy`

Production promotion is out of scope until Chief Architect approval.

The runtime is split into a small shared engine file plus per-day Book1 prose files. That split preserves the public interfaces below.

## Implemented MVP Behavior

- Writing events call `book1_write_chapter(chapter_key=..., current_day=...)`.
- Active chapter keys route through `book1.CHAPTER_BLOCKS`:
  - `day1_slop_chapter`
  - `day1_chapter`
  - `day2_chapter`
  - `day3_chapter`
  - `day4_triumphant_chapter`
  - `day5_reckoning_chapter`
- Day 1, Day 2, Day 3, Day 4, and Day 5 manuscript prose is authored as `book1_block_*` labels in the matching `book1_day10N_non_canon.rpy` file.
- `book1_nvl_write_line(...)` applies word-by-word reveal and clears the NVL page after 4 rendered lines.
- `book1_set_page_image(...)` updates the current manuscript right-frame image.
- `book1_debug_chapter_route(...)` shows the chapter key, state bucket, and resolved prose label.
- The test harness includes direct render entries for the active Book1 chapter events.

## Authoring Rules

Writers edit prose labels, not route or state code.

Allowed inside prose labels:

- `call book1_nvl_write_line("...", word_delay=_book1_word_delay)`
- ordinary Ren'Py `if` / `elif` / `else` checks against `story` or `player`
- `call book1_block_...` for reusable optional beats
- `return`

Not allowed inside prose labels:

- mutating `story`, `player`, or persistent state
- applying stats or fuel costs
- calling `end_slot`
- adding prose to `BOOK1_PAYLOADS`
- using curly-brace macro syntax for new prose
- hiding CG/image triggers inside prose text

Day scripts remain responsible for fuel checks, manuscript completion, stat changes, and routing after the writing event.

## Interfaces

### `label book1_write_chapter(chapter_key="day1_chapter", current_day=101, word_delay=0.04, include_debug=False)`

Public entry label for day scripts and harness tests.

- Clears NVL at start and end.
- Initializes page counters.
- Resolves the chapter route using gameplay state.
- Calls the resolved prose label.
- Keeps the existing call signature for compatibility.

### `label book1_nvl_write_line(line, word_delay=0.04)`

Shared manuscript line renderer.

- Applies word-by-word reveal with `book1_word_reveal_text(...)`.
- Paginates after 4 NVL lines to preserve bottom whitespace.
- Does not mutate gameplay state.

### `label book1_set_page_image(image_name="ui_book_cover")`

Optional helper for manuscript CG/illustration changes.

- Sets `book1_page_image` for the current Book1/NVL screen.
- Is called explicitly before the affected prose beat.
- Does not mutate story progress, stats, or route state.
- Uses approved asset names or manifest fallbacks.

### `book1.CHAPTER_BLOCKS`

Immutable routing table under `init python in book1`.

Add new top-level variants here only when a new chapter bucket is genuinely needed. Routine prose changes belong in labels.

## Presentation Decision

For MVP, Book1 uses the current NVL screen and the shared 4-line pagination limit. Full manuscript-page visual treatment, page-turn feedback, inkwell UI, or Editor's Desk interaction remains polish/backlog unless promoted separately.

Reference styling work remains in `docs/specs/book-writing-styling.md`.

## Test Plan

- Run non-canon formatter on changed `.rpy` files.
- Run scoped validation:
  `py scripts/validate.py --profile changed --agent non_prod_code_agent --files "<changed files>"`
- In Ren'Py, launch the non-prod project and test:
  - Day 1 chapter
  - Day 2 predator, ghost, and prey
  - Day 3 chapter
  - Day 4 triumphant chapter
  - Day 5 reckoning chapter
- Confirm:
  - no parse errors;
  - no missing labels;
  - pages clear before text reaches the bottom of the NVL screen;
  - words appear one at a time at normal text speed.

## Remaining MVP Work

Track remaining work in `docs/backlog/book1-writing-feature-mvp.md`.
