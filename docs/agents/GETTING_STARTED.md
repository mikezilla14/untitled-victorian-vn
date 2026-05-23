# Getting started with the agent system

This guide assumes you have never used this repo's agents before.

## What you are doing

You are **chaining AI sessions** (or one long session) where each step uses a different "role" defined in markdown. The **Production Orchestrator** is the only role that plans the sequence; everyone else executes one slice of work.

You are **not** running a local agent server. Cursor/Claude does the inference; this repo supplies the instructions.

## Step 1 — Pick your entry

| Goal | Load this as system prompt |
|------|----------------------------|
| Any production task (recommended) | [`.agents/rules/orchestrator.md`](../../.agents/rules/orchestrator.md) |
| Write or revise story only | [`.agents/rules/writers_room.md`](../../.agents/rules/writers_room.md) |
| One historical question | [`.agents/rules/victorian_consultant.md`](../../.agents/rules/victorian_consultant.md) |

In Cursor you can also enable the project rule **"Victorian VN — use orchestrator"** (`.cursor/rules/00-orchestrator.mdc`) or pick a skill from `.agents/skills/`.

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
| Promotion draft | `narrative/draft/releases/<release>/dayrdd_non_canon.rpy` |
| Gate verdicts | `narrative/pipeline/releases/<release>/dayrdd_gate_*.md` |
| Production day | `renpy_project/game/dayrdd.rpy` |

Naming: `r` = release number, `dd` = two-digit day (`00`–`99`).

## Step 5 — Use the pipeline helper (optional)

While chaining agents manually:

```powershell
py scripts/agent_next_step.py --pipeline produce-day --stage 1 --day 105 --release "release 1 - mvp"
py scripts/agent_next_step.py --list-pipelines
```

## Step 6 — JSON contracts (when gates or briefs exist)

Agents write **markdown + JSON** for gates, change briefs, profile deltas, and promotion handoffs. See [`docs/contracts/README.md`](../contracts/README.md).

```powershell
py scripts/contract_validate.py --day day105 --release "release 1 - mvp"
```

## Step 7 — Validate before you PR

```powershell
py scripts/orchestrate_review.py --files "narrative/draft/releases/release-1-mvp/days/day105/day105_non_canon.rpy"
```

For promotion pairs:

```powershell
py scripts/orchestrate_review.py --files "narrative/draft/releases/release-1-mvp/days/day105/day105_non_canon.rpy,renpy_project/game/day105.rpy"
```

Before promotion, require all gate files:

```powershell
py scripts/validate.py --profile changed --agent human --strict-gates --files "narrative/draft/releases/release-1-mvp/days/day105/day105_non_canon.rpy"
```

While drafting (gates not written yet):

```powershell
py scripts/validate.py --profile changed --agent writers_room --skip-gate-checks --files "..."
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
