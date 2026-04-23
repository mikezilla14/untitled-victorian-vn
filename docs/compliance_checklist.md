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

- [ ] Core state remains class-backed in `renpy_project/game/classes.rpy` (`TimeManager`, `PlayerStats`, `StoryState`); no raw globals for game state in day scripts.
- [ ] No new global `default` declarations outside `renpy_project/game/variables.rpy`.
- [ ] Stat/flag mutations are traceable and consistent with existing patterns; binary flags use `bool` + setters; mutually exclusive outcomes use a **single** string + whitelist in Python + a single setter, not several booleans.
- [ ] Direct field edits are avoided when a mutation method exists. In game scripts, **do not** assign whitelisted string fields (e.g. `story.day1_corridor_state = ...`) or `story.has_*` booleans; use setters (e.g. `story.set_corridor_state("predator")`, `story.set_has_written_first_chapter(True)`).
- [ ] `scripts/engineering_compliance.py` includes checks for disallowed `story.day1_corridor_state` assignment and unqualified `set_corridor_state(` in `renpy_project/game/`.

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

- [ ] Any changed writers-room narrative draft (`*_non_canon.rpy`) or markdown docs pass historical linter checks.
- [ ] Dialogue/tone remains consistent with established voice and class context.

## Optional reviewer notes

- Risks:
- Follow-up tasks:
- Deferred improvements:
