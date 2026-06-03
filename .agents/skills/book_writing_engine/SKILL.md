# Book Writing Engine

Use when drafting or rewriting chapters for Cora's manuscript (`book1`) using inline prose macros and the Holywell Street penny dreadful creative style.

## What to do

1. **Flag Check**: Invoke [`.agents/rules/non_prod_code_agent.md`](../../rules/non_prod_code_agent.md) to compile a list of all active story flags up to the current chapter.
2. **Drafting (Writers' Room)**: Invoke [`.agents/rules/writers_room.md`](../../rules/writers_room.md) to orchestrate divergent specs and convergent synthesis.
   * Write in the style of a salacious **Holywell Street penny dreadful**.
   * Transpose Cora's IRL events at the Savoy Hotel into the fictional Ravenshade Conservatory setting.
   * Target the 3 main branches: `prey`, `predator`, and `ghost`.
   * Embed all choices, decisions, and beats directly within the prose using curly-brace inline macros matching the compiled flags until it catches up to the IRL story.
   * **LLM Guardrails**: If there is a risk of triggering safety filters for suggestive content, create a Safe for Work (SFW) summary and clearly tag it as `[HUMAN WRITE: SFW summary of suggestive scene details]`.
3. **Syntax Compliance**: Ensure all macro syntax adheres to the [Book Writing Contract](../../../docs/contracts/book_writing_contract.md).
4. **Validation**: Validate the final draft using `scripts/validate.py` via the Chief Architect review path.

```powershell
py scripts/validate.py --profile changed --agent human --files "narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/book1_non_canon.rpy"
```
