# Project Name: [Pending Title]

An AI-accelerated, adult pseudo-sandbox RPG visual novel set in a Victorian hotel. This project explores themes of dark gothic corruption, voyeurism, and the loss of purity, utilizing a dynamic "paper doll" visual state system.

## Repository architecture (monorepo)

* **`/docs`**: Studio and mechanics docs. **`docs/narrative_workflow.md`** describes the MVP narrative loop (non-canon Ren'Py draft `.rpy` -> promoted runtime `.rpy` in `renpy_project/`).
* **`/docs/backlog`**: Deferred tooling (e.g. optional JSON beat schema), not required for MVP.
* **`/narrative`**: Story workspace — see [`narrative/README.md`](narrative/README.md).
  * **`/narrative/canon`**: Static promoted lore and voice guides.
  * **`/narrative/draft`**: Non-canon promotion drafts (`dayrdd_non_canon.rpy`), planning, bible databases.
  * **`/narrative/pipeline`**: Pre-draft exploration (specs, ideas, gates) — per-day typed folders.
* **`/renpy_project/game`**: **Episodic canon** — shipped `dayrdd.rpy` runtime scripts.
* **`/scripts`**: Tooling and validation scripts.
  * **`validate.py`**: CI entry — domains, engineering, Ren'Py lint, historical lint, writers' room pipeline (convergent + spec scripts + gate verdicts).
  * **`agent_next_step.py`**: Prints the next agent rule file for a pipeline stage (`py scripts/agent_next_step.py --pipeline produce-day --stage 1`).
  * **`orchestrate_review.py`**: Pre-PR contract bundle + remediation prompt. Use `py scripts/orchestrate_review.py --files <paths>` before PRs.
* **`/.agents`**: AI role rules.
* **`/art_pipeline`**: Asset tooling (when present).
* **`/renpy_project`**: The playable game — **core MVP deliverable**.

## Tech stack

* **Game engine**: Ren'Py (v8+)
* **Version control**: Git / GitHub

## AI agent system

**Start here:** [`AGENTS.md`](AGENTS.md) — single entry point, agent catalog, pipelines, and validation commands.

Paste [`.agents/rules/orchestrator.md`](.agents/rules/orchestrator.md) as your system prompt, then state your task. See [`docs/agents/GETTING_STARTED.md`](docs/agents/GETTING_STARTED.md) for a zero-prior-knowledge walkthrough.

## AI roles (short)

* **Orchestrator**: Decomposes a production task into ordered agent pipelines (`produce-day`, `review-scene`, `implement-spec`, `promote-day`, `promote-framework`, etc.).
* **Prod code agent**: Promotes non-canon drafts and framework designs into production (`renpy_project/` and `docs/canon/`) while preserving creative text verbatim.
* **Non-prod code agent**: Focuses on sandbox/draft implementations strictly in `narrative/draft/` preserving dialogue and prose verbatim.
* **Chief architect**: Enforces Ren’Py methodology, reviews code changes, and checks creative-technical boundaries.
* **Writers’ room (orchestration)**: Runs divergent spec scripts → convergent synthesis → `dayrdd_non_canon.rpy`; owns 100% of creative prose/dialogue in the promotion draft. Do not load pipeline `ideas/` or `synthesis/` for new assignments (see `narrative/README.md`).
* **Spiciness tuner**: Interactive 1-5 erotic intensity dial for whole-story, day, scene, passage, branch, and visual-brief variants. Level 5 is the default historical-fidelity-first project setting; lower levels progressively prioritize erotic fantasy.
* **Victorian consultant / historical linter**: Era-appropriate language checks on writers’ room narrative drafts in CI.

## Narrative → game workflow (MVP)

**Automated (recommended):** See [`AGENTS.md`](AGENTS.md) — paste `.agents/rules/orchestrator.md` as your system prompt, then state your task (e.g. `"Produce day N: [brief]"` or `"Promote day N"`).

**Manual:**
1. Write a **non-canon Ren'Py draft script** (`dayrdd_non_canon.rpy`) in `narrative/draft/`.
2. CI runs **`scripts/historical_linter.py`** on changed writers-room narrative drafts (`*_non_canon.rpy`).
3. Work with the **non-prod code agent** to implement technical wrapping and python logic inside the non-canon draft files under `narrative/draft/`.
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
