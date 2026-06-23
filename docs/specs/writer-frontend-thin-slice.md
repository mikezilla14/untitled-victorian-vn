# Spec: Writer Frontend Thin Slice

## Purpose

Define a separate thin-slice writer frontend for prose authoring and review.

The immediate problem is not story direction. It is authoring friction. Ren'Py script files are a poor working surface for a writing partner who wants to help with prose rewrites but does not want to navigate scene direction, asset calls, stat mutations, label structure, and validation rules.

This feature creates a simple frontend that exposes the prose layer in a writer-friendly format while preserving Ren'Py as the runtime source of truth.

The goal is to reduce prose workload from the main backlog by allowing a writing partner to edit dialogue, narration, menus, and Book1 prose without touching raw `.rpy` structure unless necessary.

This feature is separate from `book1-mvp-payload-system.md`, but depends on it for the Book1 prose package and visual beat model.

---

## Dependency

### Hard dependency

- `docs/specs/book1-mvp-payload-system.md`

The writer frontend should not invent a second Book1 API.

For Book1 content, it must use the Book1 package model:

- prose beats;
- thought beats;
- visual beats;
- captions;
- route buckets;
- target labels;
- metadata headers;
- importer/compiler workflow.

### Related existing architecture

The feature should align with:

- label-based Book1 routing;
- current `writer_write_book` / book writing export conventions;
- current day-writing agent/skill patterns;
- Ren'Py `.rpy` day files;
- scene direction tags and asset comments;
- validation scripts.

---

## Core Design Statement

The writer frontend is not a Ren'Py IDE.

It is a prose workbench.

It should hide implementation noise, expose semantic context, and allow safe edits that can either be written back to `.rpy` files or exported as a structured change package for an agent to implement.

The main value is giving prose collaborators a low-friction authoring surface while protecting the game code from malformed edits.

---

## MVP User Experience

A writer opens the frontend and selects a day file or Book1 chapter.

The app shows two main panes:

1. **Writer Window** - editable prose-oriented view.
2. **Presentation Window** - readable Ink-style flow preview of dialogue, narration, menus, and writing beats.

The writer window strips or collapses scene direction and exposes semantic state effects in plain language.

The presentation window shows the playable conversation flow in an Ink/Inky-like format so the writer can understand how text will feel without launching Ren'Py.

The writer can then:

- edit dialogue;
- edit narration;
- edit Cora inner monologue;
- edit Book1 manuscript prose;
- edit Book1 author-thought beats;
- inspect menus;
- inspect semantic stat/flag effects;
- save back to `.rpy` where safe;
- or export a structured change package for agent implementation.

---

## Non-Goals

The thin slice should not attempt to be a full game editor.

Out of scope for MVP:

- full Ren'Py execution;
- rendering sprites/backgrounds;
- visual timeline editing;
- asset browser beyond approved image names;
- live gameplay simulation;
- full variable/state interpreter;
- full Ink compiler compatibility;
- drag-and-drop branching editor;
- full Git GUI;
- rich WYSIWYG book page preview;
- automated prose generation.

The MVP is an editing and review surface, not a replacement for Ren'Py.

---

## High-Level Architecture

```text
Ren'Py .rpy files
      -> parser/extractor
Writer Package / Day Package
      -> frontend editor
Edited Package
      -> importer/compiler
Ren'Py .rpy patch or direct save
      -> validation
```

The app should support two modes:

1. **Direct file mode** - open, edit, and save `.rpy` files where the transformation is safe.
2. **Package mode** - export edits as structured JSON/YAML for an agent or compiler to implement.

Direct file mode is useful for controlled edits.

Package mode is safer for complex branching or when the parser cannot guarantee a clean round-trip.

---

## Main Modules

### 1. File Loader

Responsible for loading source files.

Supported MVP inputs:

- day `.rpy` files;
- Book1 prose `.rpy` files;
- future exported day packages;
- future exported Book1 packages.

Examples:

```text
main-game/non-prod-game/game/days/day102_non_canon.rpy
main-game/non-prod-game/game/days/book1_day102_non_canon.rpy
```

### 2. Ren'Py Prose Extractor

Responsible for parsing `.rpy` files into editable prose units.

The extractor does not need to understand all Ren'Py syntax. It needs to identify and preserve enough structure to safely expose prose.

MVP extracted units:

- labels;
- narration lines;
- character dialogue lines;
- `cora_inner` lines;
- menu prompts;
- menu options;
- Book1 `book1_nvl_write_line(...)` calls;
- Book1 `book1_author_thought(...)` calls;
- Book1 visual helper calls;
- state mutation lines;
- asset/staging lines;
- jump/call flow lines.

### 3. Scene Direction Stripper

Responsible for hiding implementation noise from the writer window.

It should collapse, hide, or mark:

- `scene` commands;
- `show` commands;
- `hide` commands;
- `with` transitions;
- `[ASSET]` comments;
- sprite direction comments;
- auto-placement tags;
- background/camera/staging calls;
- non-prose technical comments.

The stripped data must not be discarded. It must remain attached to the source structure for round-trip or patch generation.

### 4. Semantic State Translator

Responsible for showing state changes in human-readable terms.

Raw code such as:

```renpy
$ apply_effects(stern_susp=-5, insp=15, corr=0)
```

should display as something like:

```text
Effect: Stern suspicion decreases. Inspiration increases. No corruption change.
```

Raw code such as:

```renpy
$ story.set_day2_contraband_state("stolen_wearing")
```

should display as:

```text
Flag: Day 2 contraband state = Cora stole and wore the lace.
```

The translator is read-only for MVP unless a later implementation explicitly supports state editing.

### 5. Writer Window

The writer window is the main editable surface.

It should show prose in a clean, script-like layout:

```text
Label: day102_1_missy_finds_a_thing

Narration:
There is a soft clatter behind me.

Missy:
Cora?

Cora:
What is it?

Cora inner:
The room seems to narrow around the thing.

Effect:
Flag: day2_contraband_state = stolen_wearing
```

It should clearly separate:

- editable prose;
- read-only semantic effects;
- collapsed implementation blocks;
- menus;
- Book1 visual beats;
- comments/notes.

### 6. Presentation Window

The presentation window provides an Ink/Inky-style read-through.

It should show:

- dialogue in sequence;
- narration in sequence;
- menus as branching options;
- calls/jumps as flow links;
- Book1 prose as manuscript blocks;
- Book1 visual beats as lightweight stage cards.

Example:

```text
=== day102_2_day2_chore_time ===

Cora inner: We escape the suite with the linen cart...

Missy: You are quiet.

Cora: I am working.

* Work fast. Catalogue the room, the people, the risk. [Observant focus]
  -> day102_2_day2_insp_choice

* Linger near the danger. Let the secret sharpen itself. [Reckless linger]
  -> day102_2_day2_corr_choice
```

For Book1:

```text
=== book1_block_day2_predator_core ===

[Cover]
Chapter the Second opens upon a lady's hatbox...

[Author thought]
Too neat. She would not remember it so cleanly.

[Tableau: cg_book_d2_hatbox_tableau]
Coralie lifts the lace...

[Plate: plate_book_d2_hatbox_curse]
Caption: Plate II - The Hatbox Curse
```

This is not a perfect runtime preview. It is a readable prose-flow preview.

### 7. Package Exporter

Responsible for exporting edited content as a structured package.

Two package types are needed:

- Day Writing Package;
- Book1 Writing Package.

The Book1 package must align with `book1-mvp-payload-system.md`.

The Day package should be derived from the current day-writing skill conventions.

### 8. Importer / Patch Generator

Responsible for converting edited packages into implementation-ready changes.

MVP output options:

1. Write directly to `.rpy` where safe.
2. Export a patch/change package for an agent.
3. Export markdown review notes for manual implementation.

The importer must preserve non-prose code and scene direction unless an explicit edit target covers it.

### 9. Validation Runner

Optional but valuable in MVP.

Should expose buttons or CLI commands for:

```powershell
py scripts/format_non_canon.py <changed .rpy files>
py scripts/validate.py --profile changed --agent non_prod_code_agent --files "<changed files>"
```

For Book1 imports, include the relevant Book1 validation flow.

---

## Data Model

### Editable Unit

A parsed prose item should become an editable unit.

```json
{
  "id": "day102_1_missy_finds_a_thing:line_012",
  "source_file": "main-game/non-prod-game/game/days/day102_non_canon.rpy",
  "label": "day102_1_missy_finds_a_thing",
  "kind": "dialogue",
  "speaker": "missy",
  "text": "Cora?",
  "line_start": 110,
  "line_end": 110,
  "editable": true
}
```

Supported `kind` values:

```text
narration
dialogue
inner
menu_prompt
menu_option
book_prose
book_thought
book_visual
state_effect
asset_direction
flow_control
comment
unknown
```

### Semantic Effect Unit

```json
{
  "id": "day102_2_day2_insp_choice:effect_001",
  "kind": "state_effect",
  "raw": "$ apply_effects(stern_susp=-5, insp=15, corr=0)",
  "summary": "Stern suspicion decreases. Inspiration increases. No corruption change.",
  "editable": false
}
```

### Menu Unit

```json
{
  "id": "day102_2_day2_chore_time:menu_001",
  "kind": "menu",
  "prompt": "How do I carry the morning?",
  "options": [
    {
      "text": "Work fast. Catalogue the room, the people, the risk. [[Observant focus]]",
      "target": "day102_2_day2_insp_choice"
    },
    {
      "text": "Linger near the danger. Let the secret sharpen itself. [[Reckless linger]]",
      "target": "day102_2_day2_corr_choice"
    }
  ]
}
```

### Book Beat Unit

The Book1 beat model should match the Book1 payload spec.

```json
{
  "type": "visual",
  "mode": "plate",
  "image": "plate_book_d2_hatbox_curse",
  "caption": "Plate II - The Hatbox Curse"
}
```

---

## Day Writing API

### Purpose

The app needs a Day Writing API derived from the current write-day skill and Ren'Py day file structure.

This API should expose day prose without forcing the writer to interact with implementation details.

### Exported day package shape

```json
{
  "schema_version": "day_writing_v1",
  "day": 102,
  "source_file": "main-game/non-prod-game/game/days/day102_non_canon.rpy",
  "labels": [
    {
      "label": "day102_1_missy_finds_a_thing",
      "title": "Missy Finds A Thing",
      "units": [
        {
          "kind": "narration",
          "text": "There is a soft clatter behind me.",
          "editable": true
        },
        {
          "kind": "dialogue",
          "speaker": "missy",
          "text": "Cora?",
          "editable": true
        },
        {
          "kind": "state_effect",
          "summary": "Flag: day2_contraband_state = stolen_wearing",
          "editable": false
        }
      ]
    }
  ]
}
```

### Import behaviour

The importer should:

- update only editable text units;
- preserve indentation;
- preserve labels;
- preserve jumps/calls;
- preserve scene direction;
- preserve state mutations;
- escape quotes safely;
- reject edits that change unsupported structures;
- produce a diff before writing.

---

## Book Writing API

### Purpose

The app needs a Book Writing API that directly uses the Book1 payload package model.

### Exported book package shape

Use the schema from `book1-mvp-payload-system.md`:

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
          "text": "Chapter the Second opens upon a lady's hatbox..."
        },
        {
          "type": "thought",
          "text": "Too neat. She would not remember it so cleanly."
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

### Import behaviour

The importer should compile package beats into:

```renpy
call book1_nvl_write_line("...", word_delay=_book1_word_delay)
call book1_author_thought("...")
call book1_show_plate("image_name", caption="...")
```

It must reject hidden image triggers inside prose text.

---

## Frontend Layout

### MVP layout

Use a simple two-pane layout.

```text
+---------------------------------------------------------------+
| File / Chapter Selector                                       |
+-------------------------------+-------------------------------+
| Writer Window                 | Presentation Window           |
|                               |                               |
| Editable prose units          | Ink-style read-through         |
| Collapsed implementation      | Dialogue flow                  |
| Semantic effects              | Menu branches                  |
| Book beats                    | Book visual beat cards         |
|                               |                               |
+-------------------------------+-------------------------------+
| Save | Export Package | Export Agent Patch | Validate        |
+---------------------------------------------------------------+
```

### Writer Window rules

Show:

- label name;
- optional scene title;
- editable prose;
- speaker name;
- prose type;
- semantic effect summaries;
- collapsed scene direction markers;
- warnings.

Hide or collapse:

- sprite placement;
- background staging;
- transitions;
- comments not relevant to prose;
- raw state code by default.

### Presentation Window rules

Show:

- dialogue/narration in order;
- menu options in Ink-style layout;
- branch targets;
- Book1 prose and visual beat cards;
- lightweight flow links.

Do not attempt exact Ren'Py visual fidelity.

---

## Save and Export Modes

### Mode A: Direct Save

Directly update `.rpy` files.

Allowed only when:

- all edits are simple text replacements;
- line mapping is stable;
- no unsupported structure changed;
- validation passes or can be run immediately after.

### Mode B: Export Change Package

Export a JSON/YAML package containing edits.

Use when:

- complex branching is involved;
- line mapping is uncertain;
- an agent should implement the changes;
- the writer does not need direct repo write access.

### Mode C: Export Agent Patch Brief

Export a markdown brief that can be handed to an agent.

Should include:

- source file;
- labels touched;
- before/after prose;
- semantic notes;
- implementation warnings;
- validation commands.

---

## Thin Slice Implementation Strategy

### Phase 1: Read-only parser and preview

Goal: prove that `.rpy` can be turned into a writer-friendly view.

Required:

- load one day file;
- parse labels;
- extract dialogue/narration/inner lines;
- collapse scene direction;
- show presentation window;
- show semantic state summaries for common patterns.

No saving yet.

### Phase 2: Simple text editing

Goal: support safe prose edits.

Required:

- edit narration/dialogue/inner lines;
- preserve speaker and line structure;
- save back to `.rpy` for simple replacements;
- export diff;
- run/print validation command.

### Phase 3: Menu support

Goal: make branching readable.

Required:

- parse menu prompts and options;
- show Ink-style options;
- allow editing option text;
- preserve jump/call targets.

### Phase 4: Book1 package support

Goal: support the Book1 MVP payload workflow.

Required:

- load Book1 prose labels;
- parse `book1_nvl_write_line` calls;
- parse `book1_author_thought` calls;
- parse visual helper calls;
- show beats in writer window;
- export/import `book_payload_v1`.

Depends on Book1 payload runtime helpers.

### Phase 5: Agent handoff mode

Goal: make the tool useful even before direct-save is robust.

Required:

- export edited package;
- export markdown patch brief;
- include validation commands;
- include unsupported edit warnings.

---

## Semantic Translation Rules

### MVP supported patterns

#### `apply_effects(...)`

Example raw:

```renpy
$ apply_effects(stern_susp=-5, insp=15, corr=0)
```

Display:

```text
Effect: Stern suspicion decreases. Inspiration increases. No corruption change.
```

#### `apply_balanced_effect(...)`

Example raw:

```renpy
$ apply_balanced_effect("reckless", intensity="minor", witness="vance")
```

Display:

```text
Effect profile: reckless, minor intensity. Witness: Vance.
```

#### `story.set_*` calls

Example raw:

```renpy
$ story.set_day2_contraband_state("stolen_wearing")
```

Display:

```text
Flag: Day 2 contraband state = stolen/wearing.
```

#### `jump`

Display:

```text
Flow: jumps to day102_2_day2_chore_time.
```

#### `call expression _chain_label`

Display:

```text
Dynamic flow: calls resolved story-chain label.
```

### Translation dictionary

The frontend should use a configurable dictionary for known flags and stat names.

Example:

```json
{
  "insp": "Inspiration",
  "corr": "Corruption",
  "stern_susp": "Stern suspicion",
  "vance_susp": "Vance suspicion",
  "day2_contraband_state.stolen_wearing": "Cora stole and wore the lace",
  "day2_contraband_state.planted_in_trunk": "Cora planted the lace in Locke's trunk"
}
```

Do not hardcode every meaning into the parser.

---

## Technical Recommendation

### Preferred MVP stack

A lightweight local web app is probably the best fit.

Suggested stack:

- Python backend;
- FastAPI or Flask;
- simple file API;
- parser/extractor module;
- package exporter/importer module;
- browser frontend with plain HTML/JS or a small framework.

Avoid overbuilding.

A Streamlit prototype is acceptable for proof-of-concept, but may become limiting for structured editing and diff workflows.

### Suggested directory

```text
tools/writer_frontend/
```

Possible structure:

```text
tools/writer_frontend/
  app.py
  parser.py
  semantic_translate.py
  package_export.py
  package_import.py
  templates/
  static/
```

If implemented as CLI first:

```text
scripts/writer_frontend_export.py
scripts/writer_frontend_import.py
```

---

## Validation and Safety

### Must preserve

- labels;
- indentation;
- state mutation lines;
- asset direction lines;
- jumps/calls;
- comments needed by agents;
- DAG tags;
- sprite direction tags.

### Must reject or warn on

- changed label names;
- changed indentation structure;
- edited state code;
- edited jump targets;
- removed return statements;
- unsupported Python blocks;
- unknown multiline constructs;
- hidden image triggers in prose;
- malformed quotes.

### Required validation commands

After direct save, surface:

```powershell
py scripts/format_non_canon.py <changed .rpy files>
py scripts/validate.py --profile changed --agent non_prod_code_agent --files "<changed files>"
```

For Book1 package import, also run or display the relevant Book1 harness/validation instructions.

---

## Acceptance Criteria

The thin slice is successful when:

1. A writing partner can open a day `.rpy` file without seeing raw scene-direction noise.
2. Dialogue, narration, and Cora inner monologue appear in a clean writer window.
3. Menus appear in an Ink/Inky-style presentation layout.
4. Common stat deltas and flag setters are shown as semantic summaries.
5. Scene direction is preserved but hidden/collapsed.
6. Simple prose edits can be saved back safely or exported as an agent package.
7. Book1 prose can be represented using the Book1 payload beat model.
8. Book1 visual/thought/prose beats can be exported in `book_payload_v1` shape.
9. The app never requires the writing partner to understand Ren'Py syntax for routine prose rewrites.
10. The tool reduces prose-editing friction enough to move prose work out of the main technical backlog.

---

## Delivery Recommendation

This will affect the deadline, but it is likely worth it if prose collaboration is currently stalled.

The thin slice should be scoped ruthlessly:

- first read-only preview;
- then simple text replacement;
- then export package;
- then Book1 beats;
- only then direct import for complex branches.

The highest-value first milestone is not a perfect editor. It is a tool that lets a writing partner read the day flow, understand the choices, edit text, and hand back structured changes without fighting Ren'Py.

---

## Final Design Statement

The writer frontend exists to separate prose work from implementation work.

Ren'Py remains the runtime. Agents and validation remain the safety net. The frontend becomes the low-friction authoring surface.

For day writing, it exposes dialogue, narration, menus, and semantic state effects.

For Book1 writing, it uses the Book1 MVP payload API: prose beats, author-thought beats, visual beats, captions, and route buckets.

The result should let prose collaborators work inside the story instead of inside the engine.
