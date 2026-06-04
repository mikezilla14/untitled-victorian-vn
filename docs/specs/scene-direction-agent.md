# Spec: Ren'Py Scene Direction Agent

## Purpose

Add a **deterministic sprite-placement post-processor** to the production pipeline. After the
Writers' Room produces or rewrites prose, the Scene Direction Agent reads the resulting `.rpy`
script and adds / updates / preserves `show ... at <slot>` sprite-direction lines according to a
fixed layout policy. It keeps the Writers' Room creative and the placement mechanical.

The behavioural contract is defined in full by the source brief
(`Ren'Py Sprite Scene Direction Agent Spec`, v1). This document is the **implementation plan**: it
maps that brief onto this repo's actual conventions, names the concrete files to create, and wires
the agent into the existing orchestrator pipelines, guardrails, contracts, and skills.

This is a code/automation task. The deterministic logic lives in a Python script; the agent rule and
skill are thin wrappers that invoke it. **No freeform LLM rewriting of scripts** (per §16 of the brief).

---

## Critical reconciliation findings (read before implementing)

The source brief's examples assume a grammar that does **not** match this project. The implementation
must use the project's real conventions, not the brief's literal examples.

| Brief assumes | This repo actually uses | Resolution |
|---------------|--------------------------|------------|
| `show cora neutral at left_bust` | `show cora_sprite base_travel at left_bust` (`_sprite` suffix on the image tag) | Agent maps **speaker name → sprite tag** via a registry (`cora` → `cora_sprite`). See [characters.rpy](../../narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/characters.rpy) and existing `show` lines. |
| Single-line `show` statements only | Some `show` lines are **block form** with a trailing `:` and an indented ATL block (e.g. [day101_non_canon.rpy:263](../../narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day101_non_canon.rpy)) | Block-form `show` is treated as **implicitly locked** (never rewritten); only single-line `show` lines are candidates for `[asset auto]` management. |
| `left_bust4`, `centre_left_bust4`, `centre_right_bust4`, `right_bust4` slots exist | Only `left_bust`, `centre_bust`, `right_bust` are defined in [asset_transforms.rpy](../../narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/asset_transforms.rpy) | **Prerequisite step:** define the four 4-character transforms (+ the two aliases) before the agent can emit 4-up layouts. |
| Expression token always present | Many lines omit expression (`show gideon_sprite at right_bust`) | Expression preservation must tolerate a missing expression and fall back to a per-character safe default (§12). |

These are the main open decisions — see [Open decisions](#open-decisions) at the end.

---

## Where it runs in the pipeline

Per §1 of the brief, the agent runs after: new scene generation, scene rewrite, script rewrite,
dialogue expansion, scene restructuring. In this repo those map to existing
[orchestrator](../../.agents/rules/orchestrator.md) pipelines. The agent slots in as a **new stage
between the gated Writers' Room draft and `non_prod_code_agent`**, so the code agent receives a script
that already has correct, idempotent sprite direction.

| Pipeline | Insertion point |
|----------|-----------------|
| `produce-day` | New **Stage 1.5**: after gates pass (Stage 1), before `non_prod_code_agent` (Stage 2). |
| `rewrite-narrative` | New **Stage 1.5**: same position. |
| `revise-narrative` | New **Stage 5.5**: after brief closes / gates clear, before resuming the requester. Scoped to the touched labels only. |
| `spice-tune` | After the selected variant clears its three gates, before any implement step. |

It does **not** run inside `promote-day`/`promote-framework` (production sprite direction is copied
verbatim by `prod_code_agent`; the draft is already directed). It is **read-mostly** elsewhere.

Rationale for "after gates, before code": the agent must never touch dialogue, and dialogue is frozen
once gates pass — so running it post-gate guarantees it only ever inserts/edits `[asset auto]` lines
around already-approved prose.

**Ordering with the non-canon formatter.** `scripts/format_non_canon.py` inserts a
`# [ASSET] Visual/staging command` marker before each staging block, so the Scene Direction pass must
run **before** the formatter. The two reach a stable fixpoint: `scene_direction` → `format_non_canon`
→ both `--check` pass and stay passing on re-run. Always run them in that order; never run the
formatter between two scene-direction passes.

---

## Files to create / change

### 1. Deterministic engine — `scripts/scene_direction.py` (new)

The heart of the feature. A pure-Python, idempotent transformer. Mirror the structure of the existing
linters ([renpy_contract_linter.py](../../scripts/renpy_contract_linter.py),
[check_assets.py](../../scripts/check_assets.py)): `argparse`, `repo_path`/`resolve_file` helpers,
`--files` comma-separated input.

CLI:

```powershell
py scripts/scene_direction.py --files "<path1>,<path2>" [--check] [--agent scene_direction]
```

- default: rewrite files in place (only `[asset auto]` lines change).
- `--check`: report-only / non-zero exit if the file is not already in canonical form (for CI + the
  gatekeeper). Idempotence is verified by: run → run again → second run produces zero diffs.

Algorithm (from §10) implemented as discrete, testable functions:

1. `split_scene_blocks(lines)` — split on `^scene/s+` (§2). Respect `# [asset lock:scene]` before/after the `scene` line → skip block (§3.1).
2. `parse_block(block)` — walk lines, tracking `visible_cast` ordered list. Recognise `# [enter:X]`, `# [exit:X]` (§4), infer enter from a dialogue speaker not yet visible (§4.1), **never** infer exit (§4.2).
3. `resolve_layout(visible_cast, pins)` — apply the rule-priority resolver (§7): scene lock → line keep → explicit pin → hard relationship rules → strong character prefs → default ordering. Uses the policy YAML (below) as data, not hardcoded.
4. `render_show_lines(...)` — emit `show <tag> <expr> at <slot> <transition> # [asset auto]` (§11),
   preserving existing expression where the character already had one (§12), else per-character default.
   **Transitions:** a *newly appearing* character uses a directional entrance — `with moveinleft` when
   placed in a left-of-centre slot, `with moveinright` for centre/right slots; an *already-visible*
   character that changes slot uses `with move`. (Resolves brief §11's open `with move` question.)
5. `apply()` — replace only existing `[asset auto]` lines for the same layout event; never duplicate (§13 idempotence); leave `[asset keep]` and block-form `show` untouched.
6. Overflow: >4 visible → emit `# [asset warning: ...]` and leave layout for manual review (§14).

**Speaker→sprite-tag registry:** **derived from
[characters.rpy](../../narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/characters.rpy)**
at runtime (parse the `define <name> = Character(...)` declarations and the corresponding sprite image
tags) so `cora` → `cora_sprite`. The policy YAML carries no hardcoded tag map; if a derived tag has no
declared image, the speaker is skipped with a warning rather than guessed.

The policy (slots, aliases, hard rules, character preferences, canonical layouts, overflow) is **not**
hardcoded — it is read from the contract file below so it can be tuned without code changes.

### 2. Policy contract — `docs/contracts/sprite_layout_policy.yaml` + `.schema.json` (new)

Lift §15's `sprite_scene_direction_agent` YAML verbatim as the canonical policy, plus add a
`sprite_tags:` section for the speaker→image-tag map and a `default_expressions:` section. Add a JSON
Schema alongside it (matching the `docs/contracts/*.schema.json` pattern). This makes the layout policy
a first-class, validated handoff artifact like the other contracts in
[docs/contracts/README.md](../../docs/contracts/README.md).

Register it in `docs/contracts/README.md` (new row in the schemas table) and have
`scripts/contract_validate.py` validate it when present.

### 3. Ren'Py transform prerequisite — `asset_transforms.rpy` (edit)

Add the four 4-character slot transforms and route the two aliases. This is a **non-prod draft** edit
(the file lives under `non_prod_renpy_project/`), so it is in-domain for `non_prod_code_agent`; the
matching production change is later carried by `promote-framework`. Target slots (interpolating the
existing `vp_x` fractions in [asset_transforms.rpy](../../narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/asset_transforms.rpy)):

```renpy
transform left_bust4:          # ~vp_x(0.12)
transform centre_left_bust4:   # ~vp_x(0.38)   (alias: left_centre_bust4)
transform centre_right_bust4:  # ~vp_x(0.62)   (alias: right_centre_bust4)
transform right_bust4:         # ~vp_x(0.88)
```

Exact fractions to be tuned visually; the agent only emits the canonical names.

### 4. Agent rule — `.agents/rules/scene_direction_agent.md` (new)

Follow the header convention of the other rule files (Role / Domain / Write / Gate). Domain: read
draft `.rpy` scripts; write only `[asset auto]` lines within them. Immutable rules restated from the
brief: never touch dialogue, backgrounds, names, locked/keep lines, or block-form `show`; always run
the deterministic script rather than hand-editing; must be idempotent. The rule file instructs the
agent to **invoke `scripts/scene_direction.py`**, not to reason out placements freeform.

Add it to the agent registry table in [.agents/README.md](../../.agents/README.md) and to
[AGENTS.md](../../AGENTS.md).

### 5. Skill — `.agents/skills/scene_direction/SKILL.md` (new)

Thin wrapper in the style of [check_assets/SKILL.md](../../.agents/skills/check_assets/SKILL.md):
"When to use" (after writers-room prose lands; before non-prod implement; as a regression check),
"What to do" (run the script, resolve any `[asset warning]` for >4 cast manually), "Compliance
contract" (CI runs `--check`).

### 6. Orchestrator + pipeline wiring (edit)

- [.agents/rules/orchestrator.md](../../.agents/rules/orchestrator.md): add the Stage 1.5 / 5.5 rows
  to `produce-day`, `rewrite-narrative`, `revise-narrative`, `spice-tune`; add a routing-table row and
  a classification step.
- [docs/agents/PIPELINE_REFERENCE.md](../../docs/agents/PIPELINE_REFERENCE.md): mirror the stage
  additions and add the agent to the flowchart.

### 7. Guardrails — `.guardrails.yml` (edit)

Add `scene_direction` to the `agents:` list. It needs write access to `draft_narrative` (it edits
draft `.rpy`). It should **not** be granted `framework_code` / `episodic_code`. Note: the new
`art_agent` / `art_production` are themselves not yet in `.guardrails.yml` — flag separately; this
spec only adds `scene_direction`.

### 8. Validation integration

- Add a `scene_direction.py --check` pass to [validate.py](../../scripts/validate.py) and/or
  [orchestrate_review.py](../../scripts/orchestrate_review.py) for any changed day `.rpy`, so CI fails
  if a draft has stale/duplicated `[asset auto]` lines or a >4 overflow without a warning comment.
- The gatekeeper ([gatekeeper.py](../../scripts/gatekeeper.py)) enforces the `scene_direction` domain
  when `--agent scene_direction` is passed.

---

## Relationship to the Art Production Agent

The Scene Direction Agent (placement / `at <slot>`) is **distinct** from the
[Art Production Agent](../../.agents/rules/art_agent.md) (asset fidelity, cards, naming, the
[art_fidelity_contract](../../docs/contracts/art_fidelity_contract.json)). Division of labour:

- **Art agent** guarantees the sprite *image* exists, is on-style, and is correctly named/manifested.
- **Scene Direction agent** guarantees the sprite is *placed* in the right slot for the visible cast.

They share no files. Scene Direction depends on Art only in that the sprite tag it emits
(`cora_sprite`) must be a declared image — already enforced by the
[check_assets](../../.agents/skills/check_assets/SKILL.md) skill, so no new coupling is needed.

---

## Phased rollout

1. **Phase 0 — transforms + policy.** Add the four 4-up transforms to `asset_transforms.rpy`; commit
   `sprite_layout_policy.yaml` + schema. Nothing reads them yet.
2. **Phase 1 — engine.** Build `scripts/scene_direction.py` with unit tests (see below). Run `--check`
   only (no in-place writes) against existing day files to measure churn and surface surprises.
3. **Phase 2 — agent + skill + guardrails.** Add the rule, skill, guardrail entry, registry rows.
4. **Phase 3 — pipeline wiring.** Insert the Stage 1.5/5.5 steps and the validation hook. Enable
   in-place mode.
5. **Phase 4 — backfill.** Run once across the in-scope day files — **`day102`, `day103`, `day104`,
   `day105` only; `day100_non_canon.rpy` and `day101_non_canon.rpy` are excluded** (hand-directed,
   left as-is). The `shared/*.rpy` framework files are out of scope (no scenes). Review the diff
   manually (expect block-form and `[asset keep]` lines untouched).

---

## Tests (ship with Phase 1)

Mirror any existing script tests; if none, add `scripts/tests/test_scene_direction.py`. Cover:

- **Idempotence:** run twice → second run is a no-op (the §13 requirement).
- **Lock/keep preservation:** `# [asset lock:scene]` skips the block; `# [asset keep]` and block-form
  `show ... :` lines are byte-for-byte unchanged.
- **Canonical layouts:** every named layout in §8–§9 of the brief (Cora+Missy, Vance+Gideon, the three
  4-up canonical sets, etc.) resolves exactly.
- **Hard rules:** Vance never right of Gideon; Cora+Missy-alone fixed positions.
- **Alias folding:** `left_centre_bust4` → `centre_left_bust4` on output.
- **Enter/infer/exit:** infer-enter on speak; never auto-exit on silence.
- **Overflow:** 5 visible → warning comment, no silent drop.
- **Grammar:** emits `cora_sprite` not `cora`; preserves existing expression; falls back to default
  when absent.

---

## Resolved decisions

1. **Sprite-tag source of truth.** **Derive** the speaker→`*_sprite` map from `characters.rpy` at
   runtime. No hardcoded tag map in the policy YAML.
2. **Transitions.** Use directional **`moveinleft` / `moveinright`** for newly appearing characters
   (by slot side) and **`with move`** for repositioning an already-visible character.
3. **4-up slot fractions.** Create the four transforms now with **logical placeholder `vp_x` values**
   (left≈0.12, centre-left≈0.38, centre-right≈0.62, right≈0.88); these will be tuned visually later.
   The agent only ever emits the canonical slot names, so tuning the transforms does not require
   re-running the agent.
4. **Backfill scope.** Apply to **all non-canon day files except `day100_non_canon.rpy` and
   `day101_non_canon.rpy`** — i.e. `day102`–`day105`. `shared/*.rpy` is out of scope.

---

## Acceptance criteria

- `py scripts/scene_direction.py --files <day> --check` passes on a freshly directed file and fails on
  a stale/duplicated one.
- Running the engine twice yields no diff on the second run.
- A `produce-day` / `rewrite-narrative` run produces draft `.rpy` with correct `[asset auto]` direction
  and untouched dialogue, locks, keeps, and block-form shows.
- All §8/§9 canonical layouts are reproduced by the test suite.
- `scene_direction` is a recognised agent in `.guardrails.yml`, the orchestrator routing table, the
  pipeline reference, and the agent registry.
