# Produce Day

Use when the user wants to **draft a new day**: divergent personas, convergent synthesis, gates, and non-prod Ren'Py wrap.

## What to do

1. Load [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md) and run pipeline **`produce-day`**.
2. Stage 1: [`.agents/rules/writers_room.md`](../../rules/writers_room.md) — workflow **A**.
3. Stage 2: [`.agents/rules/non_prod_code_agent.md`](../../rules/non_prod_code_agent.md) after all gates pass.
4. Stage 3: [`.agents/rules/chief_architect.md`](../../rules/chief_architect.md).

## Required context files

- `narrative/draft/releases/<release>/planning/story_board.md`
- `narrative/draft/releases/<release>/planning/continuity_handoff.md` (current day section only)

## Outputs

- `narrative/draft/releases/<release>/dayrdd_non_canon.rpy`
- `narrative/pipeline/releases/<release>/dayrdd_convergent_report.md`
- Gate verdicts: `dayrdd_gate_lead_narrative.md`, `dayrdd_gate_forensic_psychology.md`, `dayrdd_gate_victorian.md`

## Validate

```powershell
py scripts/validate.py --profile changed --agent writers_room --files "<paths>"
```
