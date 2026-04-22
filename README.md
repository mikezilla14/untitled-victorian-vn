# Project Name: [Pending Title]

An AI-accelerated, adult pseudo-sandbox RPG visual novel set in a Victorian hotel. This project explores themes of dark gothic corruption, voyeurism, and the loss of purity, utilizing a dynamic "paper doll" visual state system.

## Repository architecture (monorepo)

* **`/docs`**: Studio and mechanics docs. **`docs/narrative_workflow.md`** describes the MVP narrative loop (pseudo-Ren’Py in markdown → implement in `renpy_project/`).
* **`/docs/backlog`**: Deferred tooling (e.g. optional JSON beat schema), not required for MVP.
* **`/narrative/writers_room`**: Draft pseudo-scripts, storyboards, and `dayrxx_non_canon.md` supporting material (`r` = release, `xx` = 2-digit day).
* **`/narrative/canon`**: Promoted truth (Lead Narrative Editor), when used.
* **`/scripts`**: **`historical_linter.py`** (retained) and **`gatekeeper.py`** (domain checks). No beat-JSON pipeline in MVP.
* **`/.agents`**: AI role rules.
* **`/art_pipeline`**: Asset tooling (when present).
* **`/renpy_project`**: The playable game — **core MVP deliverable**.

## Tech stack

* **Game engine**: Ren'Py (v8+)
* **Version control**: Git / GitHub

## AI roles (short)

* **Code agent**: Implements pseudo-scripts as real `.rpy` under guardrails.
* **Chief architect**: Enforces Ren’Py methodology and reviews code PRs.
* **Writers' room / you**: Produce markdown pseudo-scripts and design intent.
* **Victorian consultant / historical linter**: Era-appropriate language checks on writers’ room markdown in CI.

## Narrative → game workflow (MVP)

1. Write a **pseudo Ren’Py script** in markdown (`narrative/writers_room/`).
2. CI runs **`scripts/historical_linter.py`** on changed `narrative/writers_room/*.md`.
3. Work with the **coding agent** to land behavior in **`renpy_project/game/`**.
4. **Chief architect** validates structure and practice on code changes.

Details: **`docs/narrative_workflow.md`**.

## CI

GitHub Actions (`.github/workflows/gatekeeper.yml`): domain gatekeeper + historical linter on writers’ room markdown. No JSON beat validation.

---

## Development philosophy & scoping

* **Agentic context**: Clear folders so assistants load the right docs.
* **Consistency > Quality** for art pipeline where applicable.
* **Rule of 3 scope cap**: 3 primary characters, 6 backgrounds, 5 polished CGs per module guideline.
