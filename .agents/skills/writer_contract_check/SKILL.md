# Writer: Contract Check

Runs the **full-fidelity, advisory** contract pre-check on the Writer's draft before it goes to the
binding gates — so she resolves conflicts in conversation instead of hitting a downstream `REJECT`.
Use when she asks "Is this okay historically / in character?" or before any handoff.

## What to do

1. Load [`.agents/rules/writers_desk.md`](../../rules/writers_desk.md).
2. Run all three families (thoroughness over speed):
   | Family | Source of truth | Check |
   |--------|-----------------|-------|
   | Prose / structure | `book_writing_contract.md`, writers_room structure & psychological/dialogue gap contracts, voice guides | scaled-down [`lead_narrative_editor`](../../rules/lead_narrative_editor.md) on affected labels |
   | Historical | `main-game/canon/historical_guardrails.md` | real `py scripts/historical_linter.py "<draft>"` |
   | Psychological | character / forensic profiles | scaled-down [`forensic_psychology_consultant`](../../rules/forensic_psychology_consultant.md) on affected labels |
3. For each finding, return one of:
   - **PASS** — continue.
   - **SUGGESTION** — present the conflict in plain language **with concrete compliant options**;
     she picks or revises.
   - **EXCEPTION** — she declines all options → route to [`writer_log_exception`](../writer_log_exception/SKILL.md).
4. Record results in the Authoring Intent `contract_precheck` block.

This pre-check **never blocks**. The binding gates remain authoritative in fixed order:
`lead_narrative_editor → forensic_psychology_consultant → victorian_consultant`.

## Validate

```powershell
py scripts/historical_linter.py "<changed *_non_canon.rpy>"
```
