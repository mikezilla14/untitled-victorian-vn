# Spiciness Tuner Skill

Use this skill when the user asks to tune erotic intensity, specify a spice level from 1-5, make a passage hotter or milder, generate spice variants, or run the writers room with a requested spice level.

## What to do

1. Load [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md) and run pipeline **`spice-tune`** (or load tuning agent directly for diagnosis-only).
2. Primary rule: [`.agents/rules/spiciness_tuning_agent.md`](../../rules/spiciness_tuning_agent.md).
3. If prose must change: [`.agents/rules/writers_room.md`](../../rules/writers_room.md), then three gates in order.

Human index: [AGENTS.md](../../../AGENTS.md).

Level summary:

- Level 1: erotic fantasy first; Victorian accuracy retrofitted afterward.
- Level 2: erotic payoff leads, with plausible cover.
- Level 3: dramatic middle ground; mostly correct Victorian rules with heightened adult VN moments.
- Level 4: restrained heat; plausibility leads but tension is actively shaped.
- Level 5: project default; historical fidelity first, spice only where it preserves immersion.

If the user requests multiple levels or "all 5", keep outputs as variants in `narrative/pipeline/experiments/` until the human selects one. Only a selected variant should become `dayrdd_non_canon.rpy` and enter normal gate review.
