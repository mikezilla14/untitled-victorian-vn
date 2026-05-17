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

* **Orchestrator**: Decomposes a production task into an ordered agent pipeline and manages handoffs. Entry point for cross-IDE use — paste `.agents/rules/orchestrator.md` as system prompt, state your task. Pipelines: `produce-day`, `review-scene`, `implement-spec`, `historical-check`, `canon-update`.
* **Code agent**: Promotes non-canon `.rpy` drafts into runtime `.rpy` under guardrails.
* **Chief architect**: Enforces Ren’Py methodology and reviews code PRs.
* **Writers’ room / you**: Produce non-canon `.rpy` drafts and design intent.
* **Victorian consultant / historical linter**: Era-appropriate language checks on writers’ room narrative drafts in CI.

## Narrative → game workflow (MVP)

**Automated (recommended):** Paste `.agents/rules/orchestrator.md` as your system prompt in any IDE or Claude Code, then: `"Produce day N: [brief]"`. The orchestrator runs the full pipeline below.

**Manual:**
1. Write a **non-canon Ren'Py draft script** (`dayrdd_non_canon.rpy`) in `narrative/writers_room/`.
2. CI runs **`scripts/historical_linter.py`** on changed writers-room narrative drafts (`*_non_canon.rpy`, plus narrative markdown docs).
3. Work with the **coding agent** to land behavior in **`renpy_project/game/`**.
4. Run local orchestration with **`py scripts/orchestrate_review.py --files <path_to_draft>,<path_to_runtime>`** (or `python ...` on non-Windows) to automatically verify all Agent Contracts and generate AI remediation prompts.
5. **Chief architect** validates structure and practice on code changes.

Details: **`docs/narrative_workflow.md`**.

## CI

GitHub Actions (`.github/workflows/gatekeeper.yml`): standard changed-file validation via `scripts/validate.py`. No JSON beat validation.

---

## Development philosophy & scoping

* **Agentic context**: Clear folders so assistants load the right docs.
* **Consistency > Quality** for art pipeline where applicable.
* **Rule of 3 scope cap**: 3 primary characters, 6 backgrounds, 5 polished CGs per module guideline.
