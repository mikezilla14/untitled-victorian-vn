# MVP Compliance Checklist

Use this checklist for PR review by Code Agent + Chief Architect.
Mark each item `pass` or `fail`.

Automated subset in CI: `scripts/engineering_compliance.py` (PR pipeline).
Manual-only items remain reviewer responsibilities.

## A) Scope and flow

- [ ] Change supports the 5-day MVP narrative path (no unrelated feature expansion).
- [ ] No new mandatory pipeline/tooling added outside MVP scope.
- [ ] Day flow and ending routes remain coherent.

## B) State architecture

- [ ] Core state remains class-backed in `renpy_project/game/classes.rpy`.
- [ ] No new global `default` declarations outside `renpy_project/game/variables.rpy`.
- [ ] Stat/flag mutations are traceable and consistent with existing patterns.
- [ ] Direct field edits are avoided when a mutation method exists.

## C) Mechanics integrity

- [ ] Inspiration, Corruption, and Suspicion behavior remain internally consistent.
- [ ] Suspicion fail-state ordering is safe (check before passive decay where expected).
- [ ] Writing gate behavior still aligns with intended progression pressure.
- [ ] Endings trigger conditions remain valid and testable.

## D) Code hygiene

- [ ] `script.rpy` remains thin (entry + guard labels; no heavy logic).
- [ ] Repeated mechanics are consolidated or explicitly queued for `functions.rpy`.
- [ ] `renpy lint` passes with zero errors.

## E) Narrative and historical constraints

- [ ] Any changed writers-room markdown passes historical linter checks.
- [ ] Dialogue/tone remains consistent with established voice and class context.

## Optional reviewer notes

- Risks:
- Follow-up tasks:
- Deferred improvements:
