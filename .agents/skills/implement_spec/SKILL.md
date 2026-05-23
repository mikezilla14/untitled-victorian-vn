# Implement Spec

Use when drafting sandbox Ren'Py / Python scaffolding for an approved non-canon script.

## What to do

1. Load [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md) — pipeline **`implement-spec`**.
2. [`.agents/rules/non_prod_code_agent.md`](../../rules/non_prod_code_agent.md) — **verbatim** creative prose.
3. [`.agents/rules/chief_architect.md`](../../rules/chief_architect.md) — validation.

If blocked on missing dialogue, stop and route to **`revise-narrative`** (do not invent prose).

```powershell
py scripts/agent_next_step.py --pipeline implement-spec --stage 1
```
