# Writer: Status

Gives the Writer a plain-language answer to "What's left before this is safe to ship?" by reading
gate verdicts and the exception ledger. No syntax, no jargon.

## What to do

1. Load [`.agents/rules/writers_desk.md`](../../rules/writers_desk.md).
2. Read, for the current day/release:
   - gate verdicts: `dayrdd_gate_lead_narrative.md`, `dayrdd_gate_forensic_psychology.md`,
     `dayrdd_gate_victorian.md`;
   - the Authoring Intent status;
   - `narrative/draft/releases/<release>/exceptions/contract_exceptions.md`.
3. Summarize in plain language:
   - which gates have passed / are pending / rejected;
   - any **PROPOSED** exceptions (impact not yet acknowledged) — these **block promotion**;
   - any **ACCEPTED** exceptions — accepted deviations, do not block;
   - any **ACCEPTED** exception whose `Fingerprint` no longer matches the current contested text —
     flag it `REVISITED` (the blessed words changed; re-run that contract check);
   - any flags placed in the draft but **not yet wired** into `classes_non_canon.rpy` (run the
     `flag-wiring-only` pass before promotion);
   - the single next action she should take.

## Outputs

- A short, jargon-free status readout. No file edits.
