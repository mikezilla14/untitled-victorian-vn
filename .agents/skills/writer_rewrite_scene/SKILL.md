# Writer: Rewrite Scene

Prose-first front door for **rewriting or revising** existing content (e.g. "Rewrite Day 4
afternoon — make Missy colder", "Soften Cora's inner voice in the corridor"). The Writer stays in
plain language.

## What to do

1. Load [`.agents/rules/writers_desk.md`](../../rules/writers_desk.md).
2. Interview for intent and scope; derive the affected labels/window yourself.
3. Capture the new/edited prose **verbatim** into an **Authoring Intent**.
4. Run the **full-fidelity contract pre-check**; resolve findings (PASS / SUGGESTION / EXCEPTION).
5. **Route** by scale → [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md):
   - Localized copy / single branch / flavour line → **`revise-narrative`** (Workflow B).
   - Full rewrite of a file / day / time period / story chain → **`rewrite-narrative`** (Workflow A).

## Required context

- Target description; affected `dayrdd_non_canon.rpy` labels (scoped); `story_board.md` rows;
  `continuity_handoff.md` (affected day sections).

## Outputs

- Authoring Intent; updated promotion draft; convergent report; gate verdicts.

## Validate

```powershell
py scripts/validate.py --profile changed --agent writers_room --files "<paths>"
```
