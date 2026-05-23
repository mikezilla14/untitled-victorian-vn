# Promote Day

Use when the user wants to move an **approved non-canon day** into `renpy_project/game/dayrdd.rpy`.

## What to do

1. Load [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md) and run pipeline **`promote-day`**.
2. Confirm gates already passed on `dayrdd_non_canon.rpy`. If prose drift or gaps exist, run **`revise-narrative`** first.
3. Follow stages: `chief_architect` → `forensic_psychology_consultant` (pre) → `prod_code_agent` → `forensic_psychology_consultant` (post) → `chief_architect`.

## Rule files

- [`.agents/rules/chief_architect.md`](../../rules/chief_architect.md)
- [`.agents/rules/forensic_psychology_consultant.md`](../../rules/forensic_psychology_consultant.md)
- [`.agents/rules/prod_code_agent.md`](../../rules/prod_code_agent.md)

## Critical contract

Creative dialogue and narrator prose must copy **verbatim** from the writers' room draft. Reject on any creative drift.

## Validate

```powershell
py scripts/orchestrate_review.py --files "narrative/draft/releases/<release>/dayrdd_non_canon.rpy,renpy_project/game/dayrdd.rpy"
```
