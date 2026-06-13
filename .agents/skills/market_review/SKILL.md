# Market Review (F95 / adult VN)

Use only when the user **explicitly** requests **market** or F95 viability (read-only). To **change** erotic intensity levels, use [`spiciness_tuner`](../spiciness_tuner/SKILL.md) instead.

## What to do

1. Load [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md) — pipeline **`market-review`**.
2. [`.agents/rules/adult_market_reviewer.md`](../../rules/adult_market_reviewer.md) — **read-only**; no file edits.

Modes: `assess-prod`, `assess-draft`, `compare-prod-draft`, `deep-dive`.

If the user says only "assess prod" without a lens, ask one clarifying question before proceeding.
