# Produce Day

Use when the user wants to **draft a new day on the technical path** (starts at `writers_room`, not Writer's Desk). For plain-language authoring, use [`writer_write_scene`](../writer_write_scene/SKILL.md) → `writer-author` instead.

## What to do

1. Load [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md) and run pipeline **`produce-day`**.
2. Stage 1: [`.agents/rules/writers_room.md`](../../rules/writers_room.md) — workflow **A** + sequential gates.
3. **Post-gates:** [`scene_direction`](../scene_direction/SKILL.md) if the draft has staged scenes.
4. Stage 2: [`.agents/rules/non_prod_code_agent.md`](../../rules/non_prod_code_agent.md) — verbatim prose.
5. Stage 3: [`.agents/rules/chief_architect.md`](../../rules/chief_architect.md).

Catalogue: [`SKILL_CATALOG.md`](../../../docs/agents/SKILL_CATALOG.md)

## Required context files

- `narrative/draft/releases/planning/story_board.md`
- `narrative/draft/releases/planning/continuity_handoff.md` (current day section only)

## Outputs

- `narrative/draft/releases/<release>/non_prod_renpy_project/game/days/dayrdd_non_canon.rpy`
- `narrative/pipeline/releases/<release>/days/dayrdd/synthesis/dayrdd_convergent_report.md`
- Gate verdicts: `dayrdd_gate_lead_narrative.md`, `dayrdd_gate_forensic_psychology.md`, `dayrdd_gate_victorian.md` (+ `.json` sidecars)

## Validate

```powershell
py scripts/agent_next_step.py --pipeline produce-day --stage 1 --day <dd> --release release-1-mvp
py scripts/validate.py --profile changed --agent writers_room --files "narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/dayrdd_non_canon.rpy"
py scripts/contract_validate.py --day dayrdd --release release-1-mvp
```
