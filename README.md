# Project Name: [Pending Title]

An AI-accelerated, adult pseudo-sandbox RPG visual novel set in a Victorian hotel. This project explores themes of dark gothic corruption, voyeurism, and the loss of purity, utilizing a dynamic "paper doll" visual state system.

## Repository architecture (monorepo)

* **`/docs`**: Studio and mechanics docs. **`docs/narrative_workflow.md`** describes the MVP narrative loop (non-canon Ren'Py draft `.rpy` -> promoted runtime `.rpy` in `renpy_project/`).
* **`/docs/backlog`**: Deferred tooling (e.g. optional JSON beat schema), not required for MVP.
* **`/narrative/writers_room`**: Draft non-canon scripts, storyboards, and `dayrdd_non_canon.rpy` supporting material (`r` = release, `dd` = 2-digit day slot `00`-`99`), plus character/location databases (`*_character_non_canon.md`, `characters_non_canon.md`, `locations_non_canon.md`).
* **`/narrative/templates/Voice_Guides`**: Per-character voice bibles used to enforce consistent dialogue and narration tone.
* **`/narrative/canon`**: Promoted truth (Lead Narrative Editor), when used.
* **`/scripts`**: Tooling and validation scripts.
  * **`validate.py`**: CI workflow entry point for domain checks, engineering compliance, and linting.
  * **`orchestrate_review.py`**: Local orchestration tool to run Agent Contracts (historical, engineering, Ren'Py) against your files. Generates AI-ready remediation prompts. Use `py scripts/orchestrate_review.py --files <paths>` before PRs or AI handoffs.
* **`/.agents`**: AI role rules.
* **`/art_pipeline`**: Asset tooling (when present).
* **`/renpy_project`**: The playable game — **core MVP deliverable**.

## Tech stack

* **Game engine**: Ren'Py (v8+)
* **Version control**: Git / GitHub

## AI roles (short)

* **Orchestrator**: Decomposes a production task into ordered agent pipelines (`produce-day`, `review-scene`, `implement-spec`, `promote-day`, `promote-framework`, etc.).
* **Prod code agent**: Promotes non-canon drafts and framework designs into production (`renpy_project/` and `docs/canon/`) while preserving creative text verbatim.
* **Non-prod code agent**: Focuses on sandbox/draft implementations strictly in `narrative/writers_room/` preserving dialogue and prose verbatim.
* **Chief architect**: Enforces Ren’Py methodology, reviews code changes, and checks creative-technical boundaries.
* **Writers’ room (orchestration)**: Runs divergent spec scripts → convergent synthesis → `dayrdd_non_canon.rpy`; owns 100% of creative prose/dialogue in the promotion draft. Brainstorm archive: `speculative/idea_archive/` (not loaded for new assignments).
* **Spiciness tuner**: Interactive 1-5 erotic intensity dial for whole-story, day, scene, passage, branch, and visual-brief variants. Level 5 is the default historical-fidelity-first project setting; lower levels progressively prioritize erotic fantasy.
* **Victorian consultant / historical linter**: Era-appropriate language checks on writers’ room narrative drafts in CI.

## Narrative → game workflow (MVP)

**Automated (recommended):** Paste `.agents/rules/orchestrator.md` as your system prompt in any IDE or Claude Code, then state your task (e.g. `"Produce day N: [brief]"` or `"Promote day N"`).

**Manual:**
1. Write a **non-canon Ren'Py draft script** (`dayrdd_non_canon.rpy`) in `narrative/writers_room/`.
2. CI runs **`scripts/historical_linter.py`** on changed writers-room narrative drafts (`*_non_canon.rpy`).
3. Work with the **non-prod code agent** to implement technical wrapping and python logic inside the non-canon draft files under `narrative/writers_room/`.
4. Work with the **prod code agent** to promote validated drafts to the production **`renpy_project/game/`** folder.
5. Run local orchestration with **`py scripts/orchestrate_review.py --files <path_to_draft>,<path_to_runtime>`** to automatically verify all Agent Contracts.
6. **Chief architect** validates structure, state contracts, lint, and strict creative-technical preservation on code changes.

Details: **`docs/narrative_workflow.md`**.

## CI

GitHub Actions (`.github/workflows/gatekeeper.yml`): standard changed-file validation via `scripts/validate.py`. No JSON beat validation.

---

## Development philosophy & scoping

* **Agentic context**: Clear folders so assistants load the right docs.
* **Consistency > Quality** for art pipeline where applicable.
* **Rule of 3 scope cap**: 3 primary characters, 6 backgrounds, 5 polished CGs per module guideline.
