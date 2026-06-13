# Getting started with the agent system

This guide assumes you have never used this repo's agents before.

## What you are doing

You are **chaining AI sessions** (or one long session) where each step uses a different "role" defined in markdown. The **Production Orchestrator** plans technical production sequences; **Writer's Desk** and **Documentation steward** are alternate entry lanes for prose-first and docs work.

You are **not** running a local agent server. Cursor/Claude does the inference; this repo supplies the instructions.

## Step 1 — Pick your entry

| Goal | Load this as system prompt | Skill picker |
|------|----------------------------|--------------|
| Technical production (days, code, promotion) | [`.agents/rules/orchestrator.md`](../../.agents/rules/orchestrator.md) | `orchestrator` |
| Prose-first authoring (plain language) | [`.agents/rules/writers_desk.md`](../../.agents/rules/writers_desk.md) | `writer_write_scene`, `writer_rewrite_scene`, … |
| Documentation / catalogue hygiene | [`.agents/rules/documentation_steward.md`](../../.agents/rules/documentation_steward.md) | `documentation_audit` |
| One historical question only | [`.agents/rules/victorian_consultant.md`](../../.agents/rules/victorian_consultant.md) | `historical_check` |

Full skill index: [`SKILL_CATALOG.md`](SKILL_CATALOG.md). In Cursor, enable project rule **"Victorian VN — use orchestrator"** (`.cursor/rules/00-orchestrator.mdc`) or pick a skill from `.agents/skills/`.

## Step 2 — State your task clearly

Good prompts include **what**, **where**, and **scope**:

- "Produce **day 106** for release 1: afternoon, Cora confronts Stern about the ledger."
- "Promote **day 105** non-canon to `renpy_project`."
- "Review **`day103_non_canon.rpy`** for canon, psychology, and 1891 accuracy."
- "Tune the parlour scene in **day 103** to **spice level 3**."

Avoid ambiguous phrases unless you mean them:

- "Assess prod" → orchestrator will ask: code, canon, market, or drift?
- "Review changes" → same clarification.

## Step 3 — Follow the orchestrator's stages

When the orchestrator names a stage (e.g. `writers_room`), start a **new** message or session with:

1. The full content of that agent's `.md` file from [`.agents/rules/`](../../.agents/rules/).
2. File paths and prior verdicts the orchestrator listed.

Do not improvise gate order. On new promotion drafts the order is always:

**lead narrative editor → forensic psychology → Victorian consultant**

## Step 4 — Know where files go

| Artifact | Location |
|----------|----------|
| Divergent spec scripts | `narrative/pipeline/releases/<release>/dayrdd_<persona>_spec.rpy` |
| Idea sidecars (not assignment context) | `narrative/pipeline/releases/<release>/dayrdd_<persona>_ideas.md` |
| Convergent report | `narrative/pipeline/releases/<release>/dayrdd_convergent_report.md` |
| Promotion draft (MVP sandbox) | `narrative/draft/releases/<release>/non_prod_renpy_project/game/days/dayrdd_non_canon.rpy` |
| Gate verdicts | `narrative/pipeline/releases/<release>/dayrdd_gate_*.md` |
| Production day | `renpy_project/game/dayrdd.rpy` |

Naming: `r` = release number, `dd` = two-digit day (`00`–`99`).

## Step 5 — Use the pipeline helper (optional)

While chaining agents manually:

```powershell
py scripts/agent_next_step.py --pipeline produce-day --stage 1 --day 105 --release release-1-mvp
py scripts/agent_next_step.py --list-pipelines
```

## Step 6 — JSON contracts (when gates or briefs exist)

Agents write **markdown + JSON** for gates, change briefs, profile deltas, and promotion handoffs. See [`docs/contracts/README.md`](../contracts/README.md).

Documentation maintenance uses the same documentation-driven pattern. For stale README files,
feature specs, or catalogue refreshes, route `documentation-audit` and run:

```powershell
py scripts/documentation_audit.py --write
py scripts/documentation_audit.py --check
```

```powershell
py scripts/contract_validate.py --day day105 --release release-1-mvp
```

## Step 7 — Validate before you PR

Pick the mode that matches where you are in the pipeline:

| You are... | Use this flag | Typical agent |
|------------|--------------|---------------|
| Drafting / exploring, gates not written yet | `--skip-gate-checks` | `writers_room` |
| Preparing for promotion, all gates must pass | `--strict-gates` | `human` |

**While drafting:**

```powershell
py scripts/validate.py --profile changed --agent writers_room --skip-gate-checks --files "..."
```

**Before promotion** (requires all gate files):

```powershell
py scripts/validate.py --profile changed --agent human --strict-gates --files "narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day105_non_canon.rpy"
```

**Full orchestrated review:**

```powershell
py scripts/orchestrate_review.py --files "narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day105_non_canon.rpy"
```

For promotion pairs:

```powershell
py scripts/orchestrate_review.py --files "narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day105_non_canon.rpy,renpy_project/game/day105.rpy"
```

CI runs `scripts/validate.py` on changed paths (see [`.github/workflows/gatekeeper.yml`](../../.github/workflows/gatekeeper.yml)).

## Common workflows

### New day (full pipeline)

Orchestrator → `produce-day` → writers' room (divergent → convergent → 3 gates) → non-prod code → chief architect.

### Fix prose after code added a branch

File or request `dayrdd_narrative_change_brief.md` → orchestrator → `revise-narrative` → resume implement/promote.

### Ship to playable game

Gates passed on non-canon → orchestrator → `promote-day` → prod code agent (verbatim prose) → chief architect.

## When to stop and ask a human

- Canon file changes (`canon-update` pipeline stops for approval).
- Same gate **REJECT** twice on the same issue (orchestrator escalates).
- Two specialists disagree (orchestrator surfaces both sides).

## Next reads

- [Pipeline reference](PIPELINE_REFERENCE.md) — triggers and stage tables
- [Contracts](CONTRACTS.md) — handoffs and guardrails
- [Narrative workflow](../narrative_workflow.md) — MVP loop in prose
