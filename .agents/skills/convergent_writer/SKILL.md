# Convergent Writer

Use after divergent spec scripts exist for the current day.

## What to do

1. Load [`.agents/rules/convergent_writer.md`](../../rules/convergent_writer.md).
2. Read only **this day's** spec scripts under `main-game/pipeline/releases/<release>/`.
3. Deliver:
   - `main-game/draft/releases/<release>/dayrdd_non_canon.rpy`
   - `main-game/pipeline/releases/<release>/dayrdd_convergent_report.md`
4. Then run gates in order (or return to writers' room orchestration).

Validate:

```powershell
py scripts/validate.py --profile changed --agent writers_room --files "<dayrdd_non_canon.rpy path>"
```
