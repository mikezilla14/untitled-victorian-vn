# Writer: Add Flag

Lets the Writer **track something the story should remember** without touching `classes.rpy` (e.g.
"Remember whether Cora kept the stolen brooch"). Boolean by default; otherwise the Desk **prompts
for the allowed values**.

## What to do

1. Load [`.agents/rules/writers_desk.md`](../../rules/writers_desk.md).
2. **Name it in plain language.** Propose the snake_case field + `set_<name>` setter internally;
   the Writer never types them.
3. **Ask the one required question:** *"Is this a simple yes/no, or one of several outcomes?"*
   - **Yes/no →** `bool` + `set_<name>(value)`.
   - **One of several →** **prompt for the allowed values**, prepend `none`, record a whitelist:
     `VALID_<NAME>_STATES = ("none", ...)` + `set_<name>(value)` via `_set_string_state`. Never use
     multiple booleans for one fork (matches existing `StoryState` whitelists).
4. Record the flag + its in-story usage in the **Authoring Intent** (`requested_flags` block).
   **Proceed — do not block her writing.** Place the usage now and keep going; the class wiring is
   batched, not synchronous. (Trade-off: `orchestrate_review` will report the setter as unresolved
   until the wiring pass runs — this is expected. The Authoring Intent is the durable to-do; run the
   wiring before gates/promotion so no queued flag is forgotten.)
5. **Delegate wiring (batched)** → pipeline **`flag-wiring-only`**
   ([`.agents/rules/non_prod_code_agent.md`](../../rules/non_prod_code_agent.md) → chief_architect):
   it adds the attribute, whitelist, and setter to `classes_non_canon.rpy` and documents it in
   `classes_non_canon_notes.md` for the Chief Architect.

```powershell
py scripts/agent_next_step.py --pipeline flag-wiring-only --stage 1
```

## Outputs

- Updated Authoring Intent; flag wiring in `classes_non_canon.rpy` + notes (via code agent).

## Validate

```powershell
py scripts/orchestrate_review.py --files "<changed non_prod .rpy + classes_non_canon notes>"
```
