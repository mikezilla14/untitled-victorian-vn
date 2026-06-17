# MVP Compliance Checklist

Use this checklist for PR review by Prod Code Agent + Chief Architect.
Mark each item `pass` or `fail`.

Automated subset in CI: `scripts/engineering_compliance.py` (PR pipeline).
Local orchestration: Run `py scripts/orchestrate_review.py --files <path/to/files>` to automatically check compliance.
Agent pipeline: See [`AGENTS.md`](../AGENTS.md). Use `.agents/rules/orchestrator.md` as your system prompt and invoke the `implement-spec` or `produce-day` pipeline (non-prod drafting/wrapping) followed by the `promote-day` pipeline (production merging and linting).
Manual-only items remain reviewer responsibilities.

## A) Scope and flow

- [ ] Change supports the 5-day MVP narrative path (no unrelated feature expansion).
- [ ] No new mandatory pipeline/tooling added outside MVP scope.
- [ ] Day flow and ending routes remain coherent.

## B) State architecture

- [ ] Core state remains class-backed in `main-game/prod-game/game/classes.rpy` (`TimeManager`, `PlayerStats`, `StoryState`); no raw globals for game state in day scripts.
- [ ] No new global `default` declarations outside `main-game/prod-game/game/variables.rpy`.
- [ ] Stat/flag mutations are traceable and consistent with existing patterns; binary flags use `bool` + setters; mutually exclusive outcomes use a **single** string + whitelist in Python + a single setter, not several booleans.
- [ ] Direct field edits are avoided when a mutation method exists. In game scripts, **do not** assign whitelisted string fields (e.g. `story.day1_corridor_state = ...`) or `story.has_*` booleans; use setters (e.g. `story.set_corridor_state("predator")`, `story.set_has_written_first_chapter(True)`).
- [ ] `scripts/engineering_compliance.py` includes checks for disallowed `story.day1_corridor_state` assignment and unqualified `set_corridor_state(` in `main-game/prod-game/game/`.

## C) Mechanics integrity

- [ ] Inspiration, Corruption, and Suspicion behavior remain internally consistent.
- [ ] Suspicion fail-state ordering is safe (check before passive decay where expected).
- [ ] Writing gate behavior still aligns with intended progression pressure.
- [ ] Endings trigger conditions remain valid and testable.

## D) Code hygiene

- [ ] `script.rpy` remains thin (entry + guard labels; no heavy logic).
- [ ] Repeated mechanics are consolidated or explicitly queued for `functions.rpy`.
- [ ] **Asset manifest updated:** every new `scene`, `show <sprite>`, and audio alias introduced by the promoted file has a matching `declare_image_with_fallback` or `register_audio` entry in `main-game/prod-game/game/assets_manifest.rpy`. Undeclared assets are not caught by `renpy lint` — they silently render as solid-colour placeholders at runtime. PR diff must include `assets_manifest.rpy` if any new asset is referenced.
- [ ] **Bracket interpolation audit:** grep each promoted `.rpy` file for `/[[A-Z][a-zA-Z]+/]`; any match in a string that is not a defined runtime variable must be escaped to `[[Word]]` before promotion. Unescaped brackets cause a `NameError` at the first player interaction with that menu.
- [ ] `renpy lint` passes with zero errors.

## E) Narrative and historical constraints

- [ ] Any changed writers-room narrative draft (`*_non_canon.rpy`) or markdown docs pass historical linter checks.
- [ ] Dialogue/tone remains consistent with established voice and class context.
- [ ] Forensic psychology gate passed: player choices, character decisions, branch outcomes, and profile/voice-guide traits remain psychologically consistent.
- [ ] Any character profile or voice-guide psychology updates include a short forensic psychology report describing what changed, why, and future writing implications.
- [ ] **Strict Creative Handoff Enforced:** Checked that neither the non-prod nor prod code agent edited or rewrote character dialogue or narrator prose from the approved Writers' Room draft. All creative text remains exactly verbatim. (Reject immediately on creative drift).

## Optional reviewer notes

- Risks:
- Follow-up tasks:
- Deferred improvements:
