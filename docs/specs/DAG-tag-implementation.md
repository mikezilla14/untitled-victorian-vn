I reviewed the repo. The spec should be adjusted quite a bit.

The important repo reality is this:

1. The project is **documentation-driven prompt chaining**, not an in-repo autonomous pipeline. `AGENTS.md` says there is no in-repo LLM runtime; agents are markdown rule files and the orchestrator routes work by prompt chaining.
2. The existing narrative workflow says the playable product is `renpy_project/`, and non-canon day scripts in `narrative/draft/` are supporting design/implementation input, “not a parser pipeline.”
3. The actual draft day path is already standardised as `narrative/draft/releases/<release>/non_prod_renpy_project/game/days/dayrdd_non_canon.rpy`.
4. `scripts/**`, `.agents/**`, and repo workflow docs are **not** Non-Prod Code Agent territory under guardrails; they sit under repo operations / documentation ownership. Non-prod can write `narrative/draft/**` and `narrative/pipeline/**`.
5. The draft `.rpy` files already have a real marker system: `[ASSET]`, `[STATE]`, `[CHOICE]`, `[BEAT]`, plus scene-direction tags.
6. The runtime already has useful machine-readable truth: `apply_effects()` has concrete params for `insp`, `corr`, acute suspicion like `stern_susp`, and base suspicion like `stern_base`; generic `susp` is deprecated.
7. Router outcomes already live in `StoryState.SLOT_EXIT_ROUTES`, and penance routes live in `POST_PENANCE_ROUTES`.
8. Existing draft scripts already expose lots of graph-relevant structure through labels, menus, `apply_effects()`, setters, `check_confrontations`, `end_slot()`, and `advance_after_confrontation`.

So the new spec should **not** create a grand new architecture. It should add a repo-realistic graph extractor under `narrative/pipeline/`, plus a lightweight tag contract that existing create/rewrite/implement flows can follow.

# Spec: Release 1 Graph Manifest Extractor — Repo-Realistic Phase 1

## 1. Purpose

Create a lightweight graph-manifest extractor for Release 1 MVP that reads the existing non-canon Ren’Py-shaped draft scripts and emits spreadsheet-friendly graph data for balancing.

The extractor must reflect the actual repository workflow:

* `.rpy` draft scripts are the best structural source.
* `story_board.md` remains a planning/review document, not the sole graph source.
* Existing tags `[ASSET]`, `[STATE]`, `[CHOICE]`, `[BEAT]` must remain valid.
* New DAG tags are optional semantic hints maintained by day creation/rewrite workflows.
* The graph manifest tool consumes scripts and reports gaps; it does not edit `.rpy` files.

The immediate goal is to answer:

```text
What nodes, choices, branches, gates, router exits, effects, chain events, and balancing gaps exist right now?
```

This is not a simulator yet.

---

## 2. Correct Source Model

Use this source hierarchy for Phase 1:

```text
1. Non-canon .rpy draft scripts
   Primary source for labels, menus, jumps, calls, effects, state setters, and slot exits.

2. Existing repo runtime helpers
   Read-only source for apply_effects argument names and StoryState router maps.

3. Optional thin DAG tags
   Semantic hints added by create/rewrite/implement day workflows.

4. story_board.md
   Planning and audit context, not the primary extraction source.

5. Generated graph manifest and CSVs
   Machine-readable balancing skeleton.
```

Do not build `story_board.md → DAG` as the primary path.

Do not regenerate `story_board.md` in Phase 1.

---

## 3. Ownership and Guardrail Reality

This task spans two ownership zones.

### Non-Prod Code Agent may implement

The extractor itself may be created under:

```text
narrative/pipeline/tools/build_story_graph_manifest.py
```

or:

```text
narrative/pipeline/graph/build_story_graph_manifest.py
```

because `narrative/pipeline/**` is mutable by the Non-Prod Code Agent.

### Chief Architect / Human must own repo-operation changes

Do not ask the Non-Prod Code Agent to edit these directly:

```text
scripts/**
.agents/**
docs/**
.guardrails.yml
```

Changes to orchestrator skills, validation scripts, or global documentation must be handled by Chief Architect, Documentation Steward, or Human according to repo guardrails.

Therefore, Phase 1 should not require changes to `scripts/validate.py`, `.agents/skills/*`, or `.agents/rules/*`.

---

## 4. Input Paths

Default release:

```text
release-1-mvp
```

Primary script sources:

```text
narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/*.rpy
narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/*.rpy
```

Read-only helper sources:

```text
renpy_project/game/functions.rpy
renpy_project/game/classes.rpy
```

Optional audit source:

```text
narrative/draft/releases/release-1-mvp/planning/story_board.md
```

The extractor should default to the canonical release paths already used by `scripts/narrative_paths.py`.

---

## 5. Command

Create:

```text
narrative/pipeline/tools/build_story_graph_manifest.py
```

Recommended command:

```powershell
py narrative/pipeline/tools/build_story_graph_manifest.py `
  --release release-1-mvp `
  --out-dir narrative/pipeline/releases/release-1-mvp/graph `
  --storyboard narrative/draft/releases/release-1-mvp/planning/story_board.md
```

Optional flags:

```text
--script-dir
--shared-dir
--no-storyboard-audit
--write-mermaid
```

---

## 6. Required Outputs

Write generated outputs under:

```text
narrative/pipeline/releases/release-1-mvp/graph/
```

Required files:

```text
release1_graph_manifest.json
release1_nodes.csv
release1_edges.csv
release1_choices.csv
release1_gates.csv
release1_effects.csv
release1_router_outcomes.csv
release1_graph_gaps.md
release1_graph_audit.md
release1_graph_mermaid.mmd
```

Do not write generated graph outputs into `renpy_project/`.

Do not write generated graph outputs into `docs/`.

---

## 7. What to Extract

The extractor must statically parse `.rpy` files for:

```text
label declarations
menu blocks
menu options
jump targets
jump expression targets
call targets
call end_slot(outcome="...")
call check_confrontations
call book1_write_chapter(...)
call advance_after_confrontation
if / elif / else blocks with jump/call outcomes
story.set_* calls
story.complete_chain_beat(...)
story.chain_available(...)
story.resolve_chain_label(...)
apply_effects(...)
existing marker comments: [STATE], [CHOICE], [BEAT], [ASSET]
optional DAG comments if present
```

No Ren’Py execution.

No LLM calls.

Line-based parsing is acceptable for Phase 1.

Uncertainty must become a gap, not a guess.

---

## 8. Effect Mapping

Parse `apply_effects(...)` using the current runtime contract.

Map:

```text
insp          -> inspiration_delta
corr          -> corruption_delta
stern_susp    -> stern_acute_susp_delta
vance_susp    -> vance_acute_susp_delta
missy_susp    -> missy_acute_susp_delta
gideon_susp   -> gideon_acute_susp_delta
stern_base    -> stern_base_susp_delta
vance_base    -> vance_base_susp_delta
missy_base    -> missy_base_susp_delta
gideon_base   -> gideon_base_susp_delta
```

Flag:

```text
susp
```

as deprecated / invalid, because generic suspicion is deprecated in the current runtime helper.

If an `apply_effects()` call uses unknown fields, preserve the raw call and report `unmapped_effect_fields`.

---

## 9. Router Extraction

Extract router outcomes from two sources:

### 9.1 Script call sites

Parse:

```renpy
call end_slot(outcome="d1_write_ch1")
```

### 9.2 `StoryState.SLOT_EXIT_ROUTES`

Read `renpy_project/game/classes.rpy` and parse the `SLOT_EXIT_ROUTES` dictionary.

This is allowed as read-only source extraction.

Do not perform full runtime state auditing.

Only extract router maps and penance route maps.

Also parse:

```text
POST_PENANCE_ROUTES
get_post_penance_target
get_slot_exit_target
```

as lightweight route context.

---

## 10. Penance Extraction

Phase 1 should only produce a penance summary, not a full simulator.

Extract:

```text
label check_confrontations
player.anxiety >= 100
player.is_confrontation_ready("stern")
player.is_confrontation_ready("vance")
player.is_confrontation_ready("missy")
jump confrontation_*
label advance_after_confrontation
story.get_post_penance_target(...)
story.consume_penance()
jump expression _target[2]
```

Output a summary such as:

```json
{
  "interrupt_id": "check_confrontations",
  "trigger": "anxiety >= 100 or individual character confrontation threshold",
  "confrontation_targets": ["stern", "vance", "missy"],
  "hard_fail_target": "game_over_dismissed",
  "post_penance_router": "advance_after_confrontation",
  "confidence": "medium"
}
```

If Gideon is not checked in the current `check_confrontations` label, do not invent it. Report it as a design question if storyboard/mechanics imply Gideon should participate.

---

## 11. Optional Chain Extraction

Extract optional chains from shared script labels:

```text
stern_chain_1
stern_chain_2
stern_chain_3
missy_chain_1
missy_chain_2
missy_chain_3
vance_chain_1
vance_chain_2
vance_chain_3
```

For each chain label, extract:

```text
chain_character
chain_level
menu options
apply_effects calls
story.complete_chain_beat(character)
jump advance_after_confrontation
```

Report gaps when:

```text
chain label has no complete_chain_beat
chain label has no apply_effects
chain label has ambiguous safe/progress branch
chain label has no explicit slot availability/window
chain reaches level 3 but route quality consequence is not documented
```

Do not invent appointment windows.

---

## 12. Existing Marker Comments

Current draft scripts use:

```text
[ASSET]
[STATE]
[CHOICE]
[BEAT]
```

Treat these as useful context.

Example extraction rules:

* `[CHOICE]` near `menu:` increases confidence that the menu is balancing-relevant.
* `[STATE]` near `apply_effects`, setters, jumps, or calls increases confidence that the line is graph-relevant.
* `[BEAT]` should not be parsed as mechanics unless paired with state/effect calls.
* `[ASSET]` is ignored for graph purposes.

Do not remove or rewrite existing markers.

---

## 13. Optional DAG Tags

DAG tags are allowed but not required for Phase 1.

They should be maintained by create/rewrite/implement day workflows, not by the manifest extractor.

Recommended format:

```renpy
# [DAG_NODE id=day102_3_coras_choice type=choice day=102 period=Evening slot=WORK]
# [DAG_CHOICE group=day2_tea_choice sets=story.day2_tea_choice]
# [DAG_BRANCH option=predator sets=story.day2_tea_choice:predator]
# [DAG_GATE id=day102_ch2_gate type=writing_fuel condition="has_story_fuel(30)" pass=day102_4_cora_writes_a_chapter fail=day102_4_sneaks_a_feel]
# [DAG_ROUTE outcome=d2_write_night to=day103_morning]
# [DAG_CHECK type=confrontation]
# [DAG_GAP type=missing_stat_deltas owner=BalancingPass note="Confirm final branch deltas."]
```

Placement rule:

DAG tags should sit beside existing structural markers, not replace them.

Preferred:

```renpy
# [CHOICE] Decision point
# [DAG_CHOICE group=day2_tea_choice sets=story.day2_tea_choice]
menu:
```

Preferred:

```renpy
# [STATE] Charged path
# [DAG_BRANCH option=predator sets=story.day2_tea_choice:predator]
$ apply_effects(insp=5, corr=15, missy_susp=10)
```

Avoid adding a `DAG_*` tag as the only marker immediately before a `menu:`, `scene`, `show`, `$`, or `jump` line, because the current formatter treats any `# [` line as a marker block.

---

## 14. Human-Locked DAG Tags

Human-authored DAG tags are allowed and must be preservable.

Use the `manual` flag to mark a tag as human-managed:

```renpy
# [DAG_NODE id=day102_3_coras_choice type=choice day=102 period=Evening slot=WORK manual]
# [DAG_CHOICE group=day2_tea_choice sets=story.day2_tea_choice manual]
# [DAG_BRANCH option=predator sets=story.day2_tea_choice:predator manual]
# [DAG_GATE id=day102_ch2_gate type=writing_fuel condition="has_story_fuel(30)" manual]
# [DAG_ROUTE outcome=d2_write_night to=day103_morning manual]
```

Default agent behavior:

```text
Preserve manual DAG tags.
Skip edits to any DAG tag carrying `manual`.
Report skipped manual tags in the implementation report.
Do not rewrite nearby prose, routing, stats, staging, or non-DAG markers.
```

Explicit overwrite behavior:

```text
Manual DAG tags may only be overwritten when the human explicitly asks for it.
```

Recommended command flag for a future tag updater:

```powershell
py narrative/pipeline/tools/update_dag_tags.py `
  --files "path/to/day102_non_canon.rpy" `
  --overwrite-manual-dag-tags
```

Without that explicit flag/request, manual DAG tags are authoritative.

Accepted aliases may be added later (`human`, `lock`), but Phase 1 should standardize on `manual`.

---

## 15. DAG Tag Update Workflow

Add a dedicated workflow/skill variant:

```text
dag-tag-update
```

Purpose:

```text
Update or recreate `[DAG_*]` comments only, without touching prose, routing, stats, staging, or existing non-DAG markers.
```

Normal placement:

```text
rewrite-narrative / revise-narrative / manual rewrite
  -> scene_direction if cast/staging changed
  -> dag-tag-update
  -> graph manifest extraction
  -> storyboard drift audit
  -> storyboard_sync when documentation is stale
```

Rules:

```text
Default update preserves manual DAG tags.
Default recreate preserves manual DAG tags.
Full recreate may overwrite manual tags only with an explicit human request.
Any DAG tag update or recreate must rerun downstream graph files and references.
```

Downstream files to regenerate after a DAG tag update:

```text
release1_graph_manifest.json
release1_nodes.csv
release1_edges.csv
release1_choices.csv
release1_gates.csv
release1_effects.csv
release1_router_outcomes.csv
release1_graph_gaps.md
release1_graph_audit.md
release1_graph_mermaid.mmd
release1_graph_implementation_report.md
```

The gap report should include:

```text
Manual DAG Tags Preserved
```

Each preserved manual tag row should include:

```text
source_file
line_number
tag_type
tag_id_or_group
reason_skipped
overwrite_command
```

---

## 16. Manifest Tool Must Not Insert Tags

The extractor must never edit `.rpy` scripts.

It may report:

```text
missing_dag_node_tag
missing_dag_choice_tag
missing_dag_branch_tag
missing_dag_gate_tag
missing_dag_route_tag
```

But tag insertion belongs to the day creation/rewrite/implement workflows.

---

## 17. Nodes CSV

Columns:

```text
node_id
label
node_type
day
period
slot
source_file
line_number
has_dag_node_tag
has_menu
has_check_confrontations
has_end_slot
has_apply_effects
confidence
```

Node type may be inferred from:

```text
label name
DAG_NODE tag
menu presence
end_slot call
check_confrontations call
book1_write_chapter call
story_chain label pattern
```

Allowed values:

```text
work
choice
reflect
write
chain
penance_check
router
hard_fail
unknown
```

---

## 18. Edges CSV

Columns:

```text
edge_id
from_label
to_label
edge_type
condition
branch_option
router_outcome
source_file
line_number
confidence
```

Edge types:

```text
jump
jump_expression
menu_branch
gate_pass
gate_fail
router
penance
chain_return
unknown
```

For `jump expression _chain_label`, report as:

```text
edge_type = jump_expression
to_label = dynamic:story.resolve_chain_label(character)
```

---

## 19. Choices CSV

Columns:

```text
choice_id
label
choice_group
option_key
menu_text
sets_state
apply_effects_raw
effects_mapped
jump_to
source_file
line_number
has_dag_choice_tag
has_dag_branch_tag
stat_effects_known
confidence
```

For current scripts, derive option keys from:

1. `DAG_BRANCH option=...` if present.
2. Setter call inside branch, e.g. `story.set_corridor_state("predator")`.
3. Menu text bracket hint, e.g. `[[Predator path...]]`.
4. Fallback: generated option index.

Do not edit menu text.

---

## 20. Gates CSV

Columns:

```text
gate_id
label
gate_type
condition
pass_to
fail_to
source_file
line_number
has_dag_gate_tag
confidence
```

Gate candidates include:

```text
if player.anxiety >= 100
if player.anxiety >= 85
if has_story_fuel(...)
if story.manuscript_progress ...
if player.inspiration ...
if story.chain_available(...)
if player.is_confrontation_ready(...)
```

Only create gate rows for conditions that affect story flow, writing progression, chain availability, penance, or fail states.

---

## 21. Effects CSV

Columns:

```text
effect_id
label
branch_option
raw_call
inspiration_delta
corruption_delta
stern_acute_susp_delta
stern_base_susp_delta
vance_acute_susp_delta
vance_base_susp_delta
missy_acute_susp_delta
missy_base_susp_delta
gideon_acute_susp_delta
gideon_base_susp_delta
unmapped_fields
source_file
line_number
confidence
```

This file is important because it becomes the first balancing spreadsheet seed.

---

## 22. Router Outcomes CSV

Columns:

```text
outcome
target_day
target_period
target_label
source
call_sites
confidence
```

Sources:

```text
StoryState.SLOT_EXIT_ROUTES
call end_slot(outcome="...")
DAG_ROUTE tags if present
```

If `end_slot()` calls an outcome not present in `SLOT_EXIT_ROUTES`, report a gap.

If `SLOT_EXIT_ROUTES` defines an outcome with no call site, report a warning, not an error.

---

## 23. Gap Report

Create:

```text
release1_graph_gaps.md
```

Required sections:

```text
Missing DAG Tags
Ambiguous Choice Groups
Missing / Incomplete apply_effects
Deprecated Generic Suspicion Usage
Unmapped Effect Fields
Router Outcome Mismatches
Dynamic Jump Targets
Gate Pass/Fail Ambiguity
Optional Chain Window Gaps
Penance / Opportunity Cost Gaps
Storyboard Drift Notes
Manual DAG Tags Preserved
```

Each gap must include:

```text
gap_id
gap_type
source_file
line_number
label
description
recommended_owner
recommended_next_action
```

Recommended owners:

```text
Create/Rewrite Day Workflow
Non-Prod Code Agent
Chief Architect
Human Designer
Balancing Pass
Writers Room
```

Ownership rules:

```text
missing DAG tag -> Create/Rewrite Day Workflow
missing stat/effect deltas -> Balancing Pass / Human Designer
router mismatch -> Chief Architect / Non-Prod Code Agent
missing player-facing branch content -> Writers Room / Human Designer
formatter or validator changes -> Chief Architect
```

---

## 24. Storyboard Audit

If `--storyboard` is supplied, compare the extracted graph against `story_board.md`.

Do not use the storyboard to build the graph.

Audit only:

```text
storyboard label missing from scripts
script label missing from storyboard
storyboard router outcome missing from runtime routes
runtime route missing from storyboard
storyboard gate missing from script extraction
script gate missing from storyboard
```

Write these findings to:

```text
release1_graph_gaps.md
```

under:

```text
Storyboard Drift Notes
```

Do not rewrite `story_board.md` in Phase 1.

---

## 25. Audit Report

Create:

```text
release1_graph_audit.md
```

Include:

```text
files scanned
labels found
menus found
branches extracted
apply_effects calls parsed
router outcomes found
gates found
chain labels found
check_confrontations calls found
DAG tags found by type
gaps found by type
readiness assessment
```

Readiness values:

```text
Not ready — extraction failed
Partial — graph skeleton usable, balancing inputs incomplete
Ready for first balancing spreadsheet skeleton
```

Expected first result:

```text
Partial — graph skeleton usable, balancing inputs incomplete
```

---

## 26. Mermaid Output

Create:

```text
release1_graph_mermaid.mmd
```

Show:

```text
major day labels
menus / choice labels
router exits
writing gates
penance/confrontation node
optional chain labels
hard fail nodes
```

Keep readable. Do not dump every local jump.

---

## 27. Validation Command

After implementation, run:

```powershell
py scripts/validate.py --profile changed --agent non_prod_code_agent --files "narrative/pipeline/tools/build_story_graph_manifest.py"
```

Then run the tool itself:

```powershell
py narrative/pipeline/tools/build_story_graph_manifest.py `
  --release release-1-mvp `
  --out-dir narrative/pipeline/releases/release-1-mvp/graph `
  --storyboard narrative/draft/releases/release-1-mvp/planning/story_board.md
```

Then validate generated files if practical:

```powershell
py scripts/validate.py --profile changed --agent non_prod_code_agent --files "narrative/pipeline/releases/release-1-mvp/graph/release1_graph_audit.md,narrative/pipeline/releases/release-1-mvp/graph/release1_graph_gaps.md"
```

Do not require changes to CI in Phase 1.

---

## 28. Implementation Report

Create:

```text
narrative/pipeline/releases/release-1-mvp/graph/release1_graph_implementation_report.md
```

Include:

```text
files created
files scanned
commands run
validation result
extraction counts
top graph gaps
whether storyboard audit was run
recommended next owner
```

---

## 29. Storyboard Sync Workflow

Add a dedicated workflow/skill:

```text
storyboard-sync
```

Purpose:

```text
Update `story_board.md` after manual or agent-authored `.rpy` changes so the planning document reflects current script structure, without treating the storyboard as the source of truth.
```

Use after:

```text
human rewrites `.rpy` labels, menus, choices, gates, routes, or major beats
rewrite-narrative changes structure
revise-narrative changes structure
dag-tag-update or graph extraction reports storyboard drift
manual continuity edits affect the spine or scene ledger
```

Allowed primary write:

```text
narrative/draft/releases/release-1-mvp/planning/story_board.md
```

Rules:

```text
`.rpy` files are source of truth.
Do not edit `.rpy` files.
Do not invent structure absent from scripts.
Preserve the storyboard lineage header.
Update affected sections only where practical.
If script intent is ambiguous, add a drift note or open question rather than guessing.
```

Suggested pipeline placement after manual rewrites:

```text
human edits `.rpy`
  -> manual rewrite review framework
  -> dag-tag-update if structure changed
  -> graph manifest regeneration
  -> storyboard-sync
  -> continuity sync in a future feature
```

---

## 30. Future Phase 2

Phase 2 may add:

```text
DAG tag coverage enforcement
formatter support for DAG tags
optional validation check for malformed DAG tags
orchestrator skill updates
state contract audit
runtime setter/enum reconciliation
graph manifest consumed by balancing simulator
manual rewrite review framework
continuity tracker sync workflow
```

Do not build Phase 2 in this task.

## Changes I’d make to `story_board.md`

Do **not** convert `story_board.md` into a fully generated artifact yet. The repo currently treats it as required planning context for produce/rewrite workflows, and the narrative workflow explicitly lists it as a required context file for new day drafting.

Make smaller changes:

1. Add a lineage header at the very top:

```markdown
# Story Board Lineage & Ownership

This storyboard is a human-readable planning, review, and continuity artifact derived from the Release 1 non-canon `.rpy` draft scripts.

The `.rpy` files are the structural source of truth for graph extraction:

`narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/*.rpy`
`narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/*.rpy`

This file must not be treated as the primary machine-readable source for routing, DAG tags, menu structure, gates, stat effects, or graph manifests. Those are extracted from `.rpy` scripts plus optional `[DAG_*]` comments.
```

2. Add a section near the top:

```markdown
## Graph Extraction Note

The balancing graph is generated from non-canon `.rpy` draft scripts plus optional DAG tags.

This storyboard remains the human planning and review document. It is used as context by the writers-room and rewrite workflows, but it is not the sole machine-readable graph source.

Generated graph outputs live under:

`narrative/pipeline/releases/release-1-mvp/graph/`
```

3. In “Coding, Class, and Style Conventions,” add a fifth convention:

```markdown
5. **Graph Annotation:** Structural `.rpy` labels, menus, gates, and router exits may include thin `[DAG_*]` comments. These comments are non-player-facing technical metadata used by the graph manifest extractor. They must not replace `[STATE]`, `[CHOICE]`, `[BEAT]`, or `[ASSET]` markers. Human-authored DAG comments may be marked `manual`; tag-update agents must skip those unless explicitly instructed to overwrite manual DAG tags.
```

4. Add a “Graph Audit Links” section near the router section:

```markdown
## Graph Audit Links

Latest generated graph manifest:

`narrative/pipeline/releases/release-1-mvp/graph/release1_graph_manifest.json`

Latest graph gaps:

`narrative/pipeline/releases/release-1-mvp/graph/release1_graph_gaps.md`

Latest audit:

`narrative/pipeline/releases/release-1-mvp/graph/release1_graph_audit.md`

Manual `.rpy` rewrites should be followed by `storyboard_sync`, which updates this file from the current scripts and graph audit outputs. This keeps the storyboard current as documentation while preserving the rule that `.rpy` scripts remain the structural source of truth.
```

5. Update any language that implies `story_board.md` is the parser source of truth. Its current “Passage-Level Design” note says non-canon drafts hold narrative structure, dialogue, and flow, then are parsed into canon scripts. That is broadly consistent with script-first graph extraction, but it should say the graph extractor reads the `.rpy` drafts directly rather than reverse-engineering the storyboard.

## One blunt recommendation

Do **not** put this in `scripts/` for the first pass. In this repo, `scripts/**` is repo-operations territory, while `narrative/pipeline/**` is already writable by the Non-Prod Code Agent. Build it in `narrative/pipeline/tools/` first. Promote or mirror it into `scripts/` later only after Chief Architect signs off.
