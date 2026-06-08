# Writer's Desk Agent & Skill Framework Spec

Status: **partial** — agent rule, skills, schema, and pipelines scaffolded and registered; workflow
not yet exercised end-to-end with the Writer.

This spec designs a prose-first agent and skill layer that lets a non-technical writing
partner author, rewrite, and extend the visual novel entirely in plain language. It produces
well-formed Ren'Py to project standards, wires state through the existing class layer, keeps the
DAG and asset manifests in sync, and runs an interactive contract check that surfaces — rather
than silently enforces — prose, historical, and psychological constraints. The writer keeps final
editorial control; deviations are logged as human-overridden exceptions with impact notes.

## 1. Purpose And Target User

**Target user:** the writing partner ("the Writer") — a creative author who should never have to
read or type Ren'Py, Python, label routing, state setters, DAG tags, or manifest entries.

**Goal:** expose a small vocabulary of plain-language skills so the Writer can:

- write and rewrite prose freely (hotel layer and Book1 manuscript layer);
- introduce a **new state flag** without touching `classes.rpy` — boolean by default, and when it
  is not boolean the framework **prompts her for the allowed values** and builds the whitelist;
- introduce a **new stat delta** (inspiration / corruption / two-tier suspicion / anxiety);
- introduce a **new branching path** (menu, choice arm, optional chain, consequence);
- update the **Book1 manuscript** prose.

The framework then **shapes** her intent into proper Ren'Py syntax and project structure: it adds
the `[ASSET] / [STATE] / [CHOICE] / [BEAT] / [DAG_*]` tags where she did not, refreshes the DAG
graph, and updates the asset manifest where her changes introduce new backgrounds, sprites, or
audio. When work is sent for review, an **interactive contract check** helps her land the change
without breaking historical accuracy, story continuity, or immersion. Where her writing falls
outside the prose, historical, or psychological contracts, the framework **puts the conflict to
her with concrete suggestions to comply** — and if she chooses to keep it, records a documented
**exception with human override and a stated impact**.

This layer does **not** replace the Writers' Room, the code agents, the Chief Architect, or the
gates. It is a **concierge** in front of them: it translates prose intent into the existing named
pipelines and shields the Writer from every technical surface.

## 2. Current Implementation Status

| Component | Status |
|-----------|--------|
| Writer's Desk agent rule (`.agents/rules/writers_desk.md`) | **scaffolded** |
| Writer-facing skills (`.agents/skills/writer_*`) | **scaffolded** (9 `SKILL.md` wrappers) |
| Authoring Intent schema (`docs/contracts/authoring_intent.schema.json`) | **scaffolded** |
| Pipeline registration (`writer-author`, `flag-wiring-only` in `agent_next_step.py`) | **scaffolded** |
| Guardrails (`writer_experience` domain + `writers_desk` agent in `.guardrails.yml`) | **scaffolded** |
| Interactive contract-check protocol | designed; relies on existing linter/gate agents (no new tooling) |
| Contract exception ledger | designed; first ledger written on first override (no separate schema file yet) |
| Underlying machinery (writers_room, code agents, gates, DAG tool, manifests) | **implemented** — reused as-is |

"Scaffolded" means the rule/skill/schema/pipeline files exist and are registered; the workflow has
not yet been exercised end-to-end with the Writer. This spec adds an authoring **front door** — all
gate logic, state contracts, the DAG extractor
(`narrative/pipeline/tools/build_story_graph_manifest.py`), and the asset manifest workflow already
exist and are reused unchanged.

## 3. Design Principles

1. **Prose in, Ren'Py out.** The Writer speaks in scenes, characters, choices, and consequences.
   Every `.rpy` token, `$` line, setter, tag, and manifest entry is produced *for* her, never *by*
   her.
2. **Reuse, don't reinvent.** The Desk routes to existing pipelines (`produce-day`,
   `rewrite-narrative`, `revise-narrative`, `dag-tag-update`, `storyboard-sync`, `promote-day`) and
   existing agents. It introduces exactly one new artifact type (Authoring Intent) and one new
   ledger (exceptions).
3. **Creative/technical separation is preserved.** The Desk owns the *conversation* and the
   *prose*. It never edits `classes.rpy`/`classes_non_canon.rpy` itself; it emits a structured
   request and **delegates wiring to `non_prod_code_agent`** (per the existing rule that the code
   agent wires flags into the class file). Prose is always copied verbatim downstream.
4. **Soft gates before hard gates.** Contract checks first run *interactively and advisorily* with
   the Writer. The formal narrative → psychology → historical gates remain the binding authority,
   in their fixed order, run by the Writers' Room.
5. **The Writer has the final word.** No contract can block her. A contract conflict she declines
   to resolve becomes a logged exception with a human-override marker and an impact statement — it
   does not silently disappear and it does not silently ship.
6. **Everything stays in the sandbox.** All Desk output lands under `narrative/draft/**` and
   `narrative/pipeline/**`. Promotion to `renpy_project/` remains the `prod_code_agent` path behind
   the Chief Architect gate.

## 4. Architecture Overview

```text
        ┌─────────────────────────────────────────────────────────────┐
        │                        THE WRITER                            │
        │            (plain language: scenes, choices, flags)          │
        └───────────────────────────────┬─────────────────────────────┘
                                         │
                          ┌──────────────▼───────────────┐
                          │      WRITER'S DESK AGENT      │   .agents/rules/writers_desk.md
                          │  prose-first concierge/router │
                          │  • parses intent              │
                          │  • runs interactive contract  │
                          │    pre-check (advisory)       │
                          │  • emits Authoring Intent      │
                          │  • logs exceptions / overrides │
                          └───┬───────────┬───────────┬───┘
        writer-facing skills  │           │           │
   write-scene / rewrite-scene│  add-flag │ add-effect │ add-branch / write-book
                              │  (prompts │            │  contract-check / log-exception
                              │  for values)           │
                              ▼           ▼           ▼
              ┌───────────────────────────────────────────────────────┐
              │            EXISTING MACHINERY (unchanged)              │
              │                                                       │
              │  writers_room ──► divergent/convergent ──► GATES:     │
              │      lead_narrative ► forensic_psychology ► victorian │
              │                                                       │
              │  non_prod_code_agent  ── wires flags/effects into     │
              │      classes_non_canon.rpy + notes; shapes .rpy;      │
              │      adds [ASSET]/[STATE]/[CHOICE]/[BEAT] tags        │
              │                                                       │
              │  dag_tag_update  ── refresh DAG tags + graph sync     │
              │      (build_story_graph_manifest.py)                  │
              │  check_assets    ── assets_manifest fallback entries  │
              │  scene_direction ── sprite placement tags             │
              │                                                       │
              │  chief_architect ──► prod_code_agent ──► renpy_project│
              └───────────────────────────────────────────────────────┘
```

The Desk is a **thin orchestration persona**. Its leverage is the *interview* (turning vague
prose intent into a precise, contract-aware Authoring Intent) and the *routing* (choosing the
right existing pipeline and scale).

## 5. The Writer's Desk Agent

New rule file: `.agents/rules/writers_desk.md`.

**Domain / write boundary:** read `narrative/canon/`, `docs/canon/`, `docs/contracts/`, voice
guides; write only `narrative/draft/**` and `narrative/pipeline/**`. Never writes
`renpy_project/`, `docs/canon/`, `classes*.rpy`, `scripts/**`, `.agents/**`.

**Responsibilities:**

- **Intake interview.** Convert a plain-language request into a structured **Authoring Intent**
  (§7). Ask only the questions a non-technical author can answer (who/where/when, what changes,
  what the choice means) — never ask about syntax.
- **Prose capture.** Take dictated/edited prose verbatim. The Desk may lightly format paragraphs
  but never invents or rewrites story content on its own initiative — substantive prose generation
  routes to the Writers' Room.
- **Type elicitation for flags/effects/branches** (§8–§10), including the **allowed-values prompt**
  for non-boolean flags.
- **Interactive contract pre-check** (§11) before any handoff.
- **Routing** to the correct existing pipeline + scale (S/M/L).
- **Exception logging** with human override and impact (§12).

**Hard rules (mirroring the existing role contracts):**

1. Never edit production files or the class files directly. Flag/effect wiring is **delegated to
   `non_prod_code_agent`**; framework changes escalate to `chief_architect`.
2. Never silently rewrite the Writer's prose; never silently discard a contract conflict.
3. Always keep prose, dialogue, menu meaning, and stat intent verbatim through the technical
   shaping step.
4. Default flags to boolean; for one-of-N outcomes, **stop and prompt for the allowed values**, and
   record them as a whitelist request — never model a fork with multiple booleans.
5. All output stays in the sandbox; promotion is out of scope for the Desk.

## 6. Writer-Facing Skill Set

New skills under `.agents/skills/`, each a thin `SKILL.md` wrapper (matching the existing skill
format) that loads `writers_desk.md` and routes onward. Names are deliberately plain-language.

| Skill | Writer says… | Routes to |
|-------|--------------|-----------|
| `writer_write_scene` | "Write the Day 3 corridor scene where Cora hides the letters." | Authoring Intent → `produce-day` / `revise-narrative` (Workflow A/B by scale) → gates |
| `writer_rewrite_scene` | "Rewrite Day 4 afternoon — make Missy colder." | Authoring Intent → `rewrite-narrative` → gates |
| `writer_add_flag` | "Track whether Cora kept the stolen brooch." | Type interview (§8) → Authoring Intent → `non_prod_code_agent` wiring |
| `writer_add_effect` | "Refusing the money should sting her inspiration." | Effect interview (§9) → Authoring Intent → `non_prod_code_agent` |
| `writer_add_branch` | "Add a choice to warn Missy or stay silent." | Branch interview (§10) → Authoring Intent → writers_room + code agent |
| `writer_write_book` | "Write Coralie's Chapter 2 the prey way." | Book1 protocol (§ book_writing_contract) → `book_writing_engine` skill |
| `writer_shape` | (implicit) "Make it real." | `non_prod_code_agent` shape + `dag_tag_update` + `check_assets` + `scene_direction` |
| `writer_contract_check` | "Is this okay historically / in character?" | Interactive contract pre-check (§11) |
| `writer_log_exception` | "Keep it anyway — I accept the risk." | Exception ledger write + human override (§12) |
| `writer_status` | "What's left before this is safe to ship?" | Reads gate verdicts + exception ledger; plain-language summary |

Most sessions touch only `write-scene`, `rewrite-scene`, `add-flag`, `add-branch`, and
`write-book`; the rest run automatically inside those flows. Each new skill is registered in
`AGENTS.md` and `.agents/README.md` and picked up by `scripts/documentation_audit.py` per the
existing skill-maintenance contract.

## 7. The Authoring Intent Artifact

The single new contract between the prose-first layer and the technical layer. It is what the Desk
emits and what `non_prod_code_agent` / `writers_room` consume. It is the writer-initiated, prose-first
sibling of the existing `narrative_change_brief`.

Path: `narrative/draft/releases/<release>/intents/dayrdd_authoring_intent.md` (+ `.json` sidecar).

```markdown
# Authoring Intent — day[R][dd]
# Author: writer | Captured-by: writers_desk
# Scale: S | M | L          (Desk proposes; writers_room may re-grade)
# Status: DRAFT | CONTRACT_CHECKED | IN_PIPELINE | GATED | CLOSED

## Intent (plain language)
- What the Writer wants, in her words.

## Target
- Release / day / time period / label or window (Desk fills technical target).
- Layer: hotel | book1_manuscript

## Prose (verbatim)
- Paragraphs / dialogue exactly as authored. [HUMAN WRITE: ...] safety tags preserved.

## Requested flags
- name (plain): "kept the stolen brooch"
  type: boolean | one_of
  allowed_values: ["none","kept","returned","sold"]   # required iff one_of
  default: "none"

## Requested effects
- trigger: choice/label
  deltas: insp=+10, corr=+5, stern_acute_susp=+5, anxiety=-2

## Requested branches
- menu at: <window/label>
  arms:
    - text: "Warn Missy."        meaning: prey/protective    sets: ...   effects: ...
    - text: "Say nothing."       meaning: ghost              sets: ...   effects: ...

## Contract pre-check result
- prose | historical | psychological: PASS | SUGGESTION | EXCEPTION (ids)

## Routing
- pipeline: produce-day | revise-narrative | rewrite-narrative | flag-wiring-only
- next agent: writers_room | non_prod_code_agent
```

JSON sidecar schema lives at `docs/contracts/authoring_intent.schema.json` (new), modeled on the
existing `narrative_change_brief.schema.json`. Fields mirror the markdown headers so CI and
`agent_next_step.py` can route on them.

## 8. New State Flag Protocol (Boolean Default, Prompt For Values)

When the Writer asks to track something:

1. **Name it in plain language** ("did Cora keep the brooch?"). The Desk proposes a snake_case
   field + typed setter name; the Writer never sees or types these unless she wants to.
2. **Type decision (the required prompt).** The Desk asks one plain question:
   *"Is this a simple yes/no, or is it one of several outcomes?"*
   - **Yes/no →** boolean. Wiring request: `bool` attribute + `set_<name>(value)` setter.
   - **One of several →** the Desk **prompts for the allowed values** (e.g. `kept`, `returned`,
     `sold`), always prepends the `none` default sentinel, and records a whitelist request:
     `VALID_<NAME>_STATES = ("none", ...)` + `set_<name>(value)` driven by `_set_string_state`.
     This is mandatory — a one-of-N fork is never modeled as multiple booleans (matches the
     existing `StoryState` whitelist convention, e.g. `VALID_CORRIDOR_STATES`).
3. **Placement.** The Desk places the *usage* (the `$ story.set_...` note and any `if` reads) in
   the draft `.rpy` via the shaping step, in plain story terms.
4. **Wiring delegated and batched (proceed + queue — resolved decision).** Placement happens now;
   the Writer keeps writing. The Authoring Intent's `requested_flags` block is handed to
   `non_prod_code_agent` (pipeline `flag-wiring-only`) in a **later, batched** pass, which adds the
   attribute, whitelist, and setter to `classes_non_canon.rpy` and documents it in
   `classes_non_canon_notes.md` for the Chief Architect. The Writer is told, in plain language,
   "this choice is now remembered."
   - **Accepted trade-off:** between placing usage and running the wiring pass, `orchestrate_review`
     reports the setter as an unresolved symbol. This is expected and **not** enforced as a hard
     stop (no gate-blocking check). The Authoring Intent is the durable to-do list; the wiring pass
     must run before gates/promotion so no queued flag is forgotten — `writer_status` lists any
     placed-but-unwired flags.

## 9. New Stat Delta Protocol

The Writer expresses consequences emotionally ("this should drain her, but feed the corruption").
The Desk maps to the **existing** effect vocabulary — it never invents counters:

- `insp` (inspiration, capped), `corr` (corruption_xp), `anxiety`;
- two-tier per-character suspicion: `<char>_acute_susp` (temporary heat) and `<char>_base_susp`
  (permanent), for `stern` / `vance` / `gideon` / `missy`. Generic `susp` is deprecated and the
  Desk will steer the Writer to acute/base instead.

It emits `apply_effects(...)`-shaped deltas in the Authoring Intent and lets the code agent place
them. If the Writer requests a genuinely new stat or mechanic, the Desk **stops and escalates to
Chief Architect** (new mechanics are framework changes) rather than fabricating one.

## 10. New Branching Path Protocol

The Writer describes a fork by its *meaning*, not its syntax. The Desk captures, per arm: the
player-facing text, the **psychological mode** it expresses (Observer / Predator / Prey / Ghost —
cosmetic-only menus are forbidden per the psychological contract), the flag it sets, and the
effects it applies. Structural placement follows the routing refactor contract:

- fixed/core forks live in time-period spine labels;
- optional content lives in a **named dynamic window** that is *called* and *returns*;
- queued consequences land only in authored consequence windows.

The Desk never asks the Writer to choose `jump` vs `call` or to name labels; it derives the
structure and routes prose generation (if new dialogue is needed) through the Writers' Room and
structure through `non_prod_code_agent`.

## 11. Interactive Contract Check (Advisory Pre-Gate)

Before any handoff, the Desk runs a lightweight, conversational pre-check against the three
contract families. This is **advisory** — it helps the Writer comply early; it does not replace the
binding gates.

| Family | Source of truth | Lightweight check | Binding gate (later) |
|--------|-----------------|-------------------|----------------------|
| **Prose / structure** | `book_writing_contract.md`, Writers' Room Day Script Structure Contract, voice guides, Psychological & Dialogue Gap Contract | Voice/POV drift, the Cora "mask vs. inner voice" gap, NVL pagination, cosmetic-menu detection, structural placement | `lead_narrative_editor` |
| **Historical** | `docs/canon/historical_guardrails.md` | `scripts/historical_linter.py` on the draft → anachronism hints | `victorian_consultant` |
| **Psychological** | character profiles, forensic profiles | Choice-mode coverage, unearned reversals, NPC-integrity rules (Stern's shield, Gideon's pacing cycle, Vance's projection) | `forensic_psychology_consultant` |

**Interaction model — three outcomes per finding:**

1. **PASS** — no conflict; continue.
2. **SUGGESTION** — the Desk presents the conflict in plain language *with one or more concrete
   compliant rewrites/options* and asks the Writer to pick or revise. (This is the
   `AskUserQuestion`-style choice surface.) On accept, the Intent is updated.
3. **EXCEPTION** — the Writer declines all suggestions and chooses to keep her version. The Desk
   does **not** block; it routes to §12.

**Fidelity decision (resolved): full-fidelity pre-check.** The pre-check is intentionally thorough
rather than heuristic, because catching a conflict in conversation is far cheaper than a downstream
gate `REJECT` and rework. The historical family runs the real `historical_linter.py`; the prose and
psychology families run **scaled-down invocations of the actual gate agents**
(`lead_narrative_editor`, `forensic_psychology_consultant`) against the affected labels only —
same rules and source-of-truth files as the binding gates, narrower scope. This makes the pre-check
slower, which is an accepted trade: the goal is that a draft reaching the formal gates rarely
surfaces a new objection. The pre-check is still advisory — it never blocks — but its findings
should closely match what the binding gates will say.

## 12. Exception Ledger And Human Override

When the Writer overrides a contract finding, the Desk records it — this is how "final editorial
control" is made auditable rather than invisible.

**Override authority (resolved): the Writer self-signs.** She does not need a second human to sign.
The override is valid on two conditions, both enforced by the Desk before the exception can move to
`ACCEPTED`:

1. **Informed.** The Desk has presented the **possible impact** in plain language and the Writer
   has explicitly acknowledged it (the acknowledgement, in her words, is captured).
2. **Documented.** Both the override decision and the stated impact are written to the ledger entry.

A self-signed, informed, documented exception is `ACCEPTED` and does **not** block promotion. An
exception missing the impact acknowledgement stays `PROPOSED` and blocks promotion — so the gate is
not "who signs" but "was she made aware and is it on the record."

Path: `narrative/draft/releases/<release>/exceptions/contract_exceptions.md` (+ `.json`).

```markdown
## EX-<release>-<dd>-<n>
- Date: 2026-06-08
- Contract: historical | prose | psychological
- Source rule: docs/canon/historical_guardrails.md#<anchor>
- Location: day103_evening / book1_block_day3_core
- Contested text (anchor): "<the exact passage the finding objected to, verbatim>"
- Fingerprint: <stable hash of the normalized contested text>
- Finding: <what the contract objected to, plain language>
- Suggestions offered: <the compliant options the Writer declined>
- Writer decision: KEEP AS WRITTEN
- Rationale (Writer's words): "..."
- Possible impact: <immersion / continuity / accuracy consequence, Desk-assessed>
- Impact acknowledged by Writer: yes — "<her words confirming she understood the impact>"
- Override signature: <Writer> (self-sign permitted once impact is acknowledged)
- Status: PROPOSED | ACCEPTED | REVISITED
```

Rules:

- **Content-anchored expiry (resolved decision).** An exception blesses the *contested text*, not the
  whole label. The entry stores the contested passage verbatim plus a `Fingerprint` hash. On any
  later pass over that location the Desk recomputes the fingerprint: if the contested text is
  **unchanged**, the `ACCEPTED` exception persists silently — edits elsewhere in the same label do
  **not** re-prompt. If the contested text **changed**, the exception flips to `REVISITED` and the
  relevant contract check re-runs; the old blessing never carries to new words. This keeps the audit
  precise without nagging on unrelated edits, and closes the stale-blessing risk where a rewritten
  line could otherwise ship under an old override.

- An exception is **PROPOSED** until the Writer has both **acknowledged the stated impact** and
  **signed**. She may self-sign — no second human is required — but the Desk must not record
  `ACCEPTED` until the impact acknowledgement line is filled in her words. The binding gates still
  *see* the exception and may comment, but a signed-and-acknowledged exception is recorded as an
  accepted deviation rather than an open `REJECT`.
- Every exception names a **possible impact**. The Desk drafts it and must present it to the Writer
  *before* offering to sign; she may amend it.
- The ledger is surfaced by `writer_status` so the Writer always knows her standing deviations.
- Promotion (`prod_code_agent` / Chief Architect) reads the ledger; **PROPOSED** exceptions (impact
  not yet acknowledged/signed) block promotion, **ACCEPTED** ones do not.

## 13. End-To-End Worked Example

> Writer: *"On Day 3, add a moment where Cora can pocket Lady Vance's brooch. If she takes it,
> remember it, give her a jolt of inspiration but make Vance edgier. Write it tense."*

1. `writer_write_scene` loads `writers_desk.md`.
2. **Interview:** target = Day 103, evening, hotel layer. New flag "kept the brooch" → Desk asks
   "yes/no or several outcomes?" Writer: *"she keeps it, returns it, or it gets planted on her."* →
   `one_of`, values `("none","kept","returned","planted")`, default `none`. Effects: `insp=+10`,
   `vance_acute_susp=+8`. New branch with Predator/Prey/Ghost arms.
3. **Prose capture:** verbatim into the Authoring Intent.
4. **Contract pre-check:** historical linter clean; psychology flags that a "Ghost" arm needs a
   non-cosmetic consequence → SUGGESTION; Writer accepts a tweak. Prose voice check passes.
5. **Authoring Intent** emitted (scale **M**), routed to `revise-narrative` (partial pool for the
   new branch arms) → gates.
6. **Shape:** `non_prod_code_agent` wires `VALID_BROOCH_STATES` + `set_brooch_state` into
   `classes_non_canon.rpy`, places the dynamic window + `apply_effects`, copies prose verbatim,
   adds `[CHOICE]/[STATE]/[BEAT]` tags; `dag_tag_update` refreshes DAG tags + runs graph sync;
   `check_assets` confirms the brooch close-up CG has a manifest fallback (adds one if missing).
7. **Status:** `writer_status` reports gates green, zero open exceptions → "safe to hand to
   promotion."

The Writer typed no Ren'Py, named no label, and chose no `jump`/`call`.

## 14. Source-Of-Truth Files

- **New:** `.agents/rules/writers_desk.md`; `.agents/skills/writer_*/SKILL.md`;
  `docs/contracts/authoring_intent.schema.json`; exception ledger schema.
- **Reused (read/route):** `.agents/rules/writers_room.md`, `non_prod_code_agent.md`,
  `prod_code_agent.md`, `chief_architect.md`, `orchestrator.md`.
- **Contracts enforced:** `docs/contracts/book_writing_contract.md`,
  `docs/canon/historical_guardrails.md`, the Psychological & Dialogue Gap Contract (in
  `writers_room.md`), voice guides under `narrative/canon/voice_guides/`.
- **Tooling reused:** `narrative/pipeline/tools/build_story_graph_manifest.py`,
  `scripts/historical_linter.py`, `scripts/orchestrate_review.py`, `scripts/validate.py`,
  `renpy_project/game/assets_manifest.rpy`, `scripts/scene_direction.py`.
- **State model:** `narrative/draft/.../shared/classes_non_canon.rpy` (+ notes).

## 15. Validation / Review Path

```powershell
# After the Desk emits an Authoring Intent and the code agent shapes the draft:
py scripts/orchestrate_review.py --files "<changed non_prod .rpy paths>"
py scripts/validate.py --profile changed --agent non_prod_code_agent --skip-gate-checks --files "<paths>"
py scripts/historical_linter.py "<changed *_non_canon.rpy>"
py narrative/pipeline/tools/build_story_graph_manifest.py --release release-1-mvp `
   --out-dir narrative/pipeline/releases/release-1-mvp/graph `
   --storyboard narrative/draft/releases/release-1-mvp/planning/story_board.md
```

Binding review order is unchanged: convergent → `lead_narrative_editor` →
`forensic_psychology_consultant` → `victorian_consultant`, then `chief_architect` →
`prod_code_agent` for promotion. The Desk only adds the advisory pre-check and the exception
ledger; it cannot bypass these gates.

## 16. Rollout Phases

- **Phase 1 — Conversation only.** Ship `writers_desk.md` + `writer_write_scene` /
  `writer_rewrite_scene` + the Authoring Intent artifact. No new automation; the Desk routes to
  existing pipelines. Validates the interview model.
- **Phase 2 — State authoring.** Add `writer_add_flag` / `writer_add_effect` / `writer_add_branch`
  with the boolean-default / allowed-values prompt and `non_prod_code_agent` wiring handoff.
- **Phase 3 — Interactive contract check + exceptions.** Add `writer_contract_check`,
  `writer_log_exception`, the exception ledger + schema, and the historical-linter pre-check wiring.
- **Phase 4 — Book layer + status.** Add `writer_write_book` (Book1) and `writer_status` summarizer
  over gate verdicts + ledger.

Each phase is independently useful and leaves the existing pipeline fully functional.

## 17. Resolved Decisions

- **Override authority — RESOLVED.** The Writer may self-sign her own overrides; no second human is
  required. Validity is conditional on the Desk having presented the possible impact, the Writer
  acknowledging it in her own words, and both the override and the impact being documented in the
  ledger (§12). Promotion is gated on that acknowledgement being on record, not on who signs.
- **Pre-check fidelity — RESOLVED.** Favor thoroughness over speed. The pre-check runs the real
  `historical_linter.py` plus scaled-down, same-rules invocations of the actual narrative and
  psychology gate agents on the affected labels (§11). Slower is accepted because it means less
  downstream rework.
- **Desk ownership zone — RESOLVED (new `writer_experience` lane).** A `writer_experience` domain is
  added to `.guardrails.yml` covering writer-facing skill **copy** (`.agents/skills/writer_*/**`)
  plus the Desk's `intents/` and `exceptions/` artifacts, mutable by `writers_desk`, `human`, and
  `documentation_steward`. Copy/wording changes are owned by the writing side and do **not** require
  Chief Architect review; the Desk's routing logic and its rule file
  (`.agents/rules/writers_desk.md`) stay `repo_operations`. **Precedence caveat:** `gatekeeper.py`
  grants on *any* matching domain, so `chief_architect` retains access via `repo_operations` /
  `documentation` — the lane is an additive grant plus an ownership convention, not a hard exclusion
  (a true exclusion would require reworking gatekeeper precedence to most-specific-wins; deferred).
- **Flag wiring latency — RESOLVED (proceed + queue, no enforcement).** `writer_add_flag` places the
  usage and keeps the Writer moving; class wiring is batched via `flag-wiring-only` (§8). The
  unresolved-symbol window is accepted and not gate-blocked; `writer_status` lists placed-but-unwired
  flags so the wiring pass runs before promotion.
- **Exception expiry — RESOLVED (content-anchored fingerprint).** Each exception stores the contested
  passage verbatim plus a fingerprint hash and blesses *that text*, not the whole label. Unrelated
  edits do not re-prompt; a change to the contested text flips the exception to `REVISITED` and
  re-runs the check (§12).

## 18. Future Considerations

- **Gatekeeper precedence.** If the `writer_experience` lane should ever *exclude* Chief Architect
  rather than merely add the writing side, `gatekeeper.py` needs most-specific-match precedence
  instead of its current any-match union. Deferred until there's a concrete need.
- **Fingerprint tooling.** The content-anchored expiry currently relies on the Desk recomputing and
  comparing the stored hash by hand. A small helper (or a `validate.py` check) could compute and
  diff fingerprints automatically; deferred until the ledger sees real use.
- **Authoring Intent JSON validation.** `authoring_intent.schema.json` is the reference artifact;
  wiring it into `scripts/contract_schemas.py` for programmatic CI validation is a later phase, like
  the sprite layout policy.
```
