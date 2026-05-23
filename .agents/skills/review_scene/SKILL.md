# Review Scene

Use when the user wants **canon, psychological, and historical review** of existing content (not F95 market audit).

## What to do

1. Load [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md) and run pipeline **`review-scene`**.
2. Invoke these agents **in parallel** on the target file(s):
   - [`.agents/rules/lead_narrative_editor.md`](../../rules/lead_narrative_editor.md)
   - [`.agents/rules/forensic_psychology_consultant.md`](../../rules/forensic_psychology_consultant.md)
   - [`.agents/rules/victorian_consultant.md`](../../rules/victorian_consultant.md)
3. Consolidate verdicts for the human.

## Not this skill

- F95 / market / spice viability → use **`market-review`** and `adult_market_reviewer.md`
- Code architecture / lint → `chief_architect.md`
- New day drafting → **`produce-day`**

## Optional automation

```powershell
py scripts/historical_linter.py <path_to_non_canon.rpy>
py scripts/orchestrate_review.py --files "<paths>"
```
