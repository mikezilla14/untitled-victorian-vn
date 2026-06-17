# Rewrite Narrative

Use this skill when the user requests a **full rewrite** of an existing narrative file, a specific day, a time period, or a story chain event (e.g., "Rewrite day 104 afternoon choice path", "Rewrite Vance story chain from scratch"). It executes the full writers' room workflow: divergent brainstorming pool, convergent synthesis, and sequential specialist gates.

## What to do

1. Load [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md) and run pipeline **`rewrite-narrative`**.
2. Stage 1: [`.agents/rules/writers_room.md`](../../rules/writers_room.md) — Workflow **A** (Full divergent pool → convergent synthesis → sequential gates).
3. Stage 2: [`.agents/rules/non_prod_code_agent.md`](../../rules/non_prod_code_agent.md) — Technical wrap with verbatim creative prose (if target is a script).
4. Stage 3: [`.agents/rules/chief_architect.md`](../../rules/chief_architect.md) — Sandbox validation.

## Required context files

- Target file or description of the story chain / time period to rewrite
- `narrative/draft/releases/planning/story_board.md` (relevant rows)
- `narrative/draft/releases/planning/continuity_handoff.md` (affected day sections only)
- Relevant character profiles under `narrative/draft/bible/`

## Outputs

- Updated promotion draft (e.g., `dayrdd_non_canon.rpy` or `shared/story_chains_non_canon.rpy`)
- Convergent report `dayrdd_convergent_report.md`
- Gate verdicts: Narrative (`dayrdd_gate_lead_narrative.md`), Psychology (`dayrdd_gate_forensic_psychology.md`), and Victorian (`dayrdd_gate_victorian.md`)

## Next-step helper

```powershell
py scripts/agent_next_step.py --pipeline rewrite-narrative --stage 1 --day <dd> --release "<release>"
```

## Validate

```powershell
py scripts/validate.py --profile changed --agent writers_room --files "<paths>"
```
