# Spiciness Tuner Skill

Use this skill when the user asks to tune erotic intensity, specify a spice level from 1-5, make a passage hotter or milder, generate spice variants, or run the writers room with a requested spice level.

Load `.agents/rules/spiciness_tuning_agent.md` as the primary rule. For file or draft changes, also load `.agents/rules/writers_room.md`; for collaborator checks, load `.agents/rules/lead_narrative_editor.md`, `.agents/rules/forensic_psychology_consultant.md`, and `.agents/rules/victorian_consultant.md`.

Level summary:

- Level 1: erotic fantasy first; Victorian accuracy retrofitted afterward.
- Level 2: erotic payoff leads, with plausible cover.
- Level 3: dramatic middle ground; mostly correct Victorian rules with heightened adult VN moments.
- Level 4: restrained heat; plausibility leads but tension is actively shaped.
- Level 5: project default; historical fidelity first, spice only where it preserves immersion.

If the user requests multiple levels or "all 5", keep outputs as variants in `speculative/writing_experiments/` until the human selects one. Only a selected variant should become `dayrdd_non_canon.rpy` and enter normal gate review.
