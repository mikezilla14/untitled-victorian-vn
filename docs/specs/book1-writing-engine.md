# Spec: Book1 Writing Engine (NVL Artifact)

## Purpose

Define a maintainable, schema-driven writing engine that generates `book1` NVL chapter prose from gameplay state, with explicit branch scoping, creative direction per payload, and predictable extensibility for future spice variants.

This document is both:

- the **feature requirement spec** for continued development; and
- the **implementation ledger** of what has already landed in non-prod draft.

Target runtime scope for this spec:

- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/book1_non_canon.rpy`
- related call sites in `day101_non_canon.rpy` through `day105_non_canon.rpy`
- test harness in `test_day2_writing_non_canon.rpy`

---

## Product goals

1. Writing events call into an NVL artifact (`book1`) instead of hardcoding long branch prose in day scripts.
2. Output should be routed by:
   - theme (`ghost` / `predator` / `prey`)
   - flavor bucket
   - branch decisions
   - inflection beats from significant flagged events
3. Authors can scope and estimate branch load via payload IDs, not by reading runtime logic.
4. Creative quality improves over time by replacing payload prose in a controlled schema, not by restructuring logic each pass.
5. Day progression logic remains stable; writing-engine work should avoid breaking `end_slot` routing and deadline gates.

---

## Current implementation status (as of this spec)

## Implemented

- **Schema-driven `book1` core** in `book1_non_canon.rpy`:
  - `BOOK1_SCHEMA`: chapter structure (`base_id`, decision groups, beats)
  - `BOOK1_PAYLOADS`: payload prose + creative direction + beat checks
  - `book1_resolve_payload_ids(chapter_key)`: dynamic payload resolution from current flags
  - `build_book1_chapter_packet(...)`: assembled chapter lines from resolved payload IDs
  - `book1_word_reveal_text(...)`: word-by-word reveal formatting for NVL pacing
  - `label book1_write_chapter(...)`: callable render label for writing events
  - `label book1_debug_schema(...)`: inspection label showing active payloads and directions

- **Integration in day flow**:
  - Day writing labels call `book1_write_chapter(...)` for chapter moments.
  - Day 1 includes intentional low-corruption “slop” output path.

- **Testing support**:
  - `test_day2_writing_non_canon.rpy` includes setup labels for seeded state.
  - Schema/debug labels available for payload routing inspection.

## Partially implemented

- Branching breadth exists, but prose depth remains generic in many payloads.
- Beat coverage is structurally present, but first two days lack enough high-signal narrative flags to make variants feel sharply distinct.

## Not implemented yet

- Full authored prose pass for all payloads in `BOOK1_PAYLOADS`.
- Two-tier flag system (narrative-input vs progression-gating flags).
- Systematic spice-variant matrix (e.g., prey beat at 3 spice levels).
- Automated content expansion pipeline for spice variants.

---

## Problem diagnosis

The current output feels underpowered mostly because early-day state carries limited narrative texture:

- many route-relevant flags are coarse;
- few event flags encode nuanced interpersonal consequences in Day 1/2;
- available flags skew toward progression mechanics rather than prose-driving detail.

Result: routing works, but payload selection often resolves to similar prose bands.

---

## Requirements

### R1. Stable schema contract

Keep chapter assembly controlled by `BOOK1_SCHEMA` and `BOOK1_PAYLOADS` only.

No new ad hoc prose branching should be added directly in day labels.

### R2. Two-tier flag model

Introduce explicit separation:

1. **Narrative input flags** (for prose flavor/beat selection):
   - nuanced social/emotional context
   - witness/debt/intimacy posture
   - inferred framing stance
2. **True progression flags** (for gameplay gates):
   - chapter completion/deadline states
   - route unlocks
   - fail-state prerequisites

Narrative flags may be richer and more numerous; progression flags should remain minimal and robust.

### R3. Early-day texture uplift

Add meaningful Day 1/2 narrative-input flags so early chapter payloads branch into substantially different texture.

### R4. Spiciness layering model

Support cheap branch multiplication by decoupling **plot routing** from **spice rendering**:

- keep one canonical semantic payload per branch;
- derive level variants (e.g., L1/L2/L3) via controlled rewrite passes;
- do not explode core logic dictionaries per spice level.

### R5. Authorability and scoping

For any chapter key, developers/authors must be able to answer:

- which payload IDs can fire;
- which flags decide each branch;
- where to edit prose and creative direction;
- approximate payload count by chapter before writing.

### R6. Testability

Must support direct render tests that bypass day routing fail states for author iteration.

### R7. Inline Prose Macro System

Support a custom micro-DSL syntax within prose strings to allow low-friction authoring of variations and conditional segments:
- **Syntax**: `{ "literal text" default; variable_name if condition; }`
- **Options**: Support both double-quoted string literals and unquoted variable names (representing strings or lists/tuples of strings).
- **Compound Conditions**: Support logical `and` and `or` logical operations inside condition expressions.
- **Evaluation Order**: Deterministic "first match wins" (evaluated top-to-bottom, stopping at the first positive condition or falling back to `default`).
- **Ren'Py Compatibility**: Ignore standard Ren'Py styling/formatting curly tags by specifically matching macro brackets containing valid text/variable options.

---

## Proposed architecture (next phase)

### 1) Flag taxonomy

Add a structured mapping in `book1_non_canon.rpy`:

- `BOOK1_FLAG_TIERS = { "narrative_input": (...), "progression_gate": (...) }`

And an optional metadata map:

- `BOOK1_FLAG_NOTES = { flag_name: "intent + producer labels" }`

### 2) Narrative input aggregator

Create a lightweight resolver function that maps raw state into normalized writing-engine tags:

- `book1_resolve_narrative_inputs() -> set[str]`

Example tags:

- `tone.witness_complicit`
- `debt.missy_high`
- `power.stern_public_discipline`
- `heat.ultimatum_refusal`

Then route many payload checks by these normalized tags instead of scattered raw flags.

### 3) Payload model extension

Extend payload metadata:

- `direction` (already present)
- `intent` (one-line objective)
- `depends_on` (tags/flags)
- `spice_profile` (allowed levels)

Optional:

- `rewrite_source_id` for derived variants.

### 4) Spice variant strategy

For each eligible payload, store semantic base at level 2 and optionally generated variants:

- `lines_l2` required
- `lines_l1`, `lines_l3` optional (generated or hand-tuned)

Fallback policy:

- request level N
- if missing, derive from nearest existing level
- never block rendering due to missing variant.

### 5) Chapter build pipeline

Formalize assembly stages:

1. resolve theme/flavor
2. resolve normalized narrative-input tags
3. resolve payload IDs from schema
4. select spice variant per payload
5. render NVL lines

### 6) Inline Prose Macro Parser

Implement a custom micro-DSL parsing and evaluation engine:
- **Scanner**: A regex matcher looking for `/{/s*(?:"|[_a-zA-Z]).*?/}` to extract macro blocks without colliding with Ren'Py's formatting tags (e.g., `{b}`).
- **Splitter**: Splits options within a block by semicolon `;` (handling quotes/semicolons correctly).
- **Resolver**: If an option value is a variable reference (identifier), resolves it against `BOOK1_COMMON_FRAGMENTS` or globals.
- **Evaluator**: Parses and evaluates conditions. Handles logical `and` / `or` operations with standard precedence (`and` binds tighter than `or`), checking attributes on the singletons `story` and `player`.
- **NVL Expansion**: If a macro constitutes the entire line and resolves to a list of strings, the engine inserts them as multiple paragraphs (lines) in the NVL packet.

---

## Implementation plan

## Phase A — Flag foundation (Day 1/2 uplift)

1. Inventory current Day 1/2 flags and classify into two tiers.
2. Add 6-12 narrative-input tags that encode interesting writing context without breaking progression.
3. Seed tags in existing day labels at high-signal moments (e.g., Stern/Missy confrontation dynamics, deception posture, complicity cost, observed vs acted desire).
4. Add debug label to print resolved narrative-input tags for current state.

Acceptance:

- Day 2 debug runs show distinct tag sets across predator/prey/ghost harness presets.

## Phase B — Payload schema deepening

1. Add payload metadata fields (`intent`, `depends_on`, `spice_profile`).
2. Replace remaining generic prose placeholders for Day 1/2 payloads.
3. Add coverage checklist comment/table mapping chapter -> payload IDs -> prose status.

Acceptance:

- Every active Day 1/2 payload has non-placeholder prose and explicit direction/intent.

## Phase C — Spiciness layering

1. Add chapter-level spice parameter to `book1_write_chapter(...)`.
2. Implement variant selection fallback.
3. Define first pilot set:
   - prey branch decision payloads
   - key beats with 3 spice levels.
4. Use spiciness agent workflow to generate variant candidates from level-2 canonical prose.

Acceptance:

- Same chapter/flags rendered at 3 spice levels with stable semantics and controlled intensity shift.

## Phase D — Validation + workflow docs

1. Add a compact author guide section in this spec (or linked doc) for “add new payload” workflow.
2. Ensure test harness has at least:
   - one direct render per theme
   - one debug schema/tag route per theme
3. Optionally add script checks for missing payload prose keys when referenced by schema.

Acceptance:

- New payload addition is possible without touching day script routing logic.

## Phase E — Inline Prose Macro Engine

1. Implement custom regex scanner, option splitter, variable lookup, and compound condition evaluator in `book1_non_canon.rpy`.
2. Restructure `book1_non_canon.rpy` to organize parsing logic at the top and payload blocks below.
3. Hook macro resolution into the rendering pipeline (`_book1_render_line` and `_book1_payload_lines`).
4. Add comprehensive unit tests verifying literals, variables, and compound log-based evaluation in `test_day2_writing_non_canon.rpy`.

Acceptance:

- Test harness successfully verifies macro syntax, logical compound conditions, multi-paragraph variable expansion, and formatting tag safety.

---

## What to edit for future work

- Routing + schema: `book1_non_canon.rpy`
- Trigger points in gameplay flow: `day101_non_canon.rpy` .. `day105_non_canon.rpy`
- Rapid iteration harness: `test_day2_writing_non_canon.rpy`

---

## Open decisions

1. Where should narrative-input tags live long term?
   - in `StoryState` (persistent), or
   - transiently computed each chapter call from canonical flags.
2. Should spice level be:
   - global per run,
   - chapter-specific,
   - or branch-specific with fallback?
3. How much generated spice prose is acceptable before mandatory human pass?
4. Do we cap beat count per chapter render to prevent overlong NVL blocks?

---

## Risks and mitigations

- **Risk:** branch explosion makes authoring unmanageable.
  - **Mitigation:** keep semantic branches compact; multiply by spice level via derivation, not duplicated core routing.
- **Risk:** early flags stay too shallow.
  - **Mitigation:** add narrative-input tag layer before writing large prose payloads.
- **Risk:** test harness misleads due to day routing fail states.
  - **Mitigation:** keep direct-render tests as the default author workflow.

---

## Acceptance criteria for “feature mature enough for broad prose pass”

- `book1_debug_schema(...)` shows predictable payload IDs for all Day 1/2/3 key presets.
- Narrative-input tags materially alter payload resolution in first two chapters.
- The inline macro system parses compound conditions, variable lookups, and multi-paragraph lists correctly.
- At least one full chapter has:
  - authored prose for all active payloads,
  - three spice variants on selected prey branch + beats,
  - no progression regression in day flow.
- Authors can estimate payload count and writing scope per chapter from schema alone.
