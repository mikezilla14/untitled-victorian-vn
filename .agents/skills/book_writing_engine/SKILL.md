# Book Writing Engine

Use when drafting or rewriting chapters for Cora's manuscript (`book1`) using the label-based Book1 prose engine and the Holywell Street penny dreadful creative style.

## What to do

1. **Context Packet**: Invoke [`.agents/rules/non_prod_code_agent.md`](../../rules/non_prod_code_agent.md) to compile the Book Writing Context Packet for the target chapter/day:
   - available story flags, string states, and player stats up to the chapter;
   - short real-life Savoy story-so-far summary;
   - target chapter key, route bucket, and existing `book1_block_*` labels;
   - approved manuscript CG/image names.
2. **Drafting (Writers' Room)**: Invoke [`.agents/rules/writers_room.md`](../../rules/writers_room.md) to orchestrate divergent specs and convergent synthesis.
   * Write in the style of a salacious **Holywell Street penny dreadful**.
   * Transpose Cora's IRL events at the Savoy Hotel into the fictional Ravenshade Conservatory setting.
   * Target the relevant route buckets, usually `prey`, `predator`, and `ghost` for days 1-4 and day-specific buckets where the route table defines them.
   * Produce prose and branch notes suitable for `book1_block_*` labels, ordinary Ren'Py `if` / `elif` / `else`, and reusable `book1_block_*` beat labels.
   * Put manuscript image changes in explicit cue notes so the code agent can implement `call book1_set_page_image("image_name")`.
   * **LLM Guardrails**: If there is a risk of triggering safety filters for suggestive content, create a Safe for Work (SFW) summary and clearly tag it as `[HUMAN WRITE: SFW summary of suggestive scene details]`.
3. **Structure Compliance**: Ensure the output adheres to the [Book Writing Contract](../../../docs/contracts/book_writing_contract.md): no curly-brace macros, no `BOOK1_PAYLOADS`, no state mutation inside prose labels, and all manuscript paragraphs routed through `book1_nvl_write_line(...)`.
4. **Non-Prod Wrap**: Route approved prose to `non_prod_code_agent` for the label wrapper in the non-prod Book1 runtime file(s). The code agent preserves prose verbatim.
   - Engine/routing/helper code lives in `book1_non_canon.rpy`.
   - Prose blocks live in `book1_day101_non_canon.rpy` through `book1_day105_non_canon.rpy`.
5. **Validation**: Validate the final draft using `scripts/validate.py` via the Chief Architect review path.

```powershell
py scripts/validate.py --profile changed --agent human --files "main-game/non-prod-game/game/days/book1_non_canon.rpy" "main-game/non-prod-game/game/days/book1_day101_non_canon.rpy" "main-game/non-prod-game/game/days/book1_day102_non_canon.rpy" "main-game/non-prod-game/game/days/book1_day103_non_canon.rpy" "main-game/non-prod-game/game/days/book1_day104_non_canon.rpy" "main-game/non-prod-game/game/days/book1_day105_non_canon.rpy"
```
