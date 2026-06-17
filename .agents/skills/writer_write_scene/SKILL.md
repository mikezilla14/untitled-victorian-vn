# Writer: Write Scene

Prose-first front door for authoring a **new scene or day**. Use when the Writer describes a scene
in plain language (e.g. "Write the Day 3 corridor scene where Cora hides the letters"). She never
touches Ren'Py or Python.

## What to do

1. Load [`.agents/rules/writers_desk.md`](../../rules/writers_desk.md).
2. **Interview** in plain language (who / where / when / what changes / what choices mean). Derive
   the technical target yourself.
3. Capture prose **verbatim** and emit an **Authoring Intent**:
   `main-game/draft/releases/<release>/intents/dayrdd_authoring_intent.md` (+ `.json`, schema
   [`docs/contracts/authoring_intent.schema.json`](../../../docs/contracts/authoring_intent.schema.json)).
4. Run the **full-fidelity contract pre-check** (prose / historical / psychological). Resolve each
   finding as PASS / SUGGESTION / EXCEPTION (see `writer_log_exception`).
5. **Route** by scale → [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md) pipeline
   **`produce-day`** (writers_room → gates → `non_prod_code_agent` shape → `chief_architect`).

## Required context

- The Writer's description; `story_board.md` rows; `continuity_handoff.md` (current day section).
- Canon, voice guides, character bible.

## Outputs

- Authoring Intent (`.md` + `.json`); gated `dayrdd_non_canon.rpy`; convergent report; gate verdicts.

## Validate

```powershell
py scripts/orchestrate_review.py --files "<changed non_prod .rpy paths>"
```
