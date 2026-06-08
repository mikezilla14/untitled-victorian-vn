# Writer: Log Exception

Records a **human-overridden contract exception** when the Writer chooses to keep prose that a
contract objected to. This is how her final editorial control is made auditable. She may **self-sign**
— but only after she has been made aware of the impact and it is documented.

## What to do

1. Load [`.agents/rules/writers_desk.md`](../../rules/writers_desk.md).
2. **Before signing**, present the **possible impact** in plain language (immersion / continuity /
   accuracy). She may amend it.
3. Capture her acknowledgement **in her own words**, then write the entry to
   `narrative/draft/releases/<release>/exceptions/contract_exceptions.md` (+ `.json`):

```markdown
## EX-<release>-<dd>-<n>
- Date: <YYYY-MM-DD>
- Contract: historical | prose | psychological
- Source rule: <file#anchor>
- Location: <label / book1_block>
- Contested text (anchor): "<the exact passage the finding objected to, verbatim>"
- Fingerprint: <stable hash of the normalized contested text>
- Finding: <plain language>
- Suggestions offered: <options she declined>
- Writer decision: KEEP AS WRITTEN
- Rationale (Writer's words): "..."
- Possible impact: <Desk-assessed consequence>
- Impact acknowledged by Writer: yes — "<her words>"
- Override signature: <Writer> (self-sign permitted once impact acknowledged)
- Status: PROPOSED | ACCEPTED | REVISITED
```

## Rules

- Do **not** record `ACCEPTED` until the impact-acknowledgement line is filled in her words; until
  then it is `PROPOSED`.
- A `PROPOSED` exception **blocks promotion**; an `ACCEPTED` one does not.
- **Content-anchored expiry.** Capture the contested passage verbatim plus a `Fingerprint` hash.
  The exception blesses *that text*, not the whole label. On a later pass: if the contested text is
  unchanged, the exception persists silently; if it changed, set `REVISITED` and re-run the relevant
  contract check (the old blessing does not carry to new words). Unrelated edits in the same label
  do not re-prompt.
- Link the exception id back into the Authoring Intent `exception_ids` / `contract_precheck`.
