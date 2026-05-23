# Revise Narrative

Use when prose must change because code, structure, or a gate filed `dayrdd_narrative_change_brief.md` (scale S / M / L).

## What to do

1. Confirm `narrative/draft/releases/<release>/dayrdd_narrative_change_brief.md` exists with `Status: OPEN`.
2. Load [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md) and run **`revise-narrative`**.
3. [`.agents/rules/writers_room.md`](../../rules/writers_room.md) — workflow **B** (S), partial divergent pool (M), or **A** (L).
4. Run gates in order: lead narrative → forensic psychology → Victorian.

## Next-step helper

```powershell
py scripts/agent_next_step.py --pipeline revise-narrative --stage 1 --day <dd> --release "<release>"
```
