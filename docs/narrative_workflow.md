# Narrative workflow (MVP)

The product is a **playable Ren'Py MVP** in `renpy_project/`. Non-canon day scripts in `narrative/draft/` are supporting design/implementation input, not a parser pipeline.

## Your loop

**Automated (recommended):** Use the **Orchestrator** — see [`AGENTS.md`](../AGENTS.md) and paste [`.agents/rules/orchestrator.md`](../.agents/rules/orchestrator.md) as your system prompt, then state your task (e.g., `"Produce day 106: afternoon, Cora finds the ledger discrepancy"`). It runs the full pipeline below, routes each stage to the correct specialist agent, and surfaces blocking issues for human decision. Pipeline index: [`docs/agents/PIPELINE_REFERENCE.md`](agents/PIPELINE_REFERENCE.md).

**Manual:**

1. **Write a non-canon day draft** via the Writing Orchestration Agent (`writers_room`): load **`continuity_handoff.md`** (current day section only) + `story_board.md`; divergent personas → `narrative/pipeline/`; **convergent** synthesizes `dayrdd_non_canon.rpy` and publishes `dayrdd_convergent_report.md`; then **`lead_narrative_editor`**, then **`forensic_psychology_consultant`**, then **`victorian_consultant`** (in that order). After gates pass, convergent updates the **next** day's handoff section in `continuity_handoff.md`. Gate verdicts live under `narrative/pipeline/` (excluded from future assignment context).
2. **Revise narrative when code or review requires it** (`revise-narrative`): `non_prod_code_agent`, `lead_narrative_editor`, or `forensic_psychology_consultant` files `dayrdd_narrative_change_brief.md` (scale S/M/L); `writers_room` runs convergent-only, partial divergent pool, or full day pass; gates; then the requester resumes technical implementation with **verbatim** prose. Code agents must not invent dialogue.
3. **Psychology pass** — the **forensic psychology consultant** confirms player choices, branches, profile traits, and voice-guide psychology are consistent. If profiles or voice guides change, the consultant files a short change report explaining what changed, why, and future writing implications.
4. **Historical pass** — run `scripts/historical_linter.py` on the draft file. Fix or justify flagged anachronisms.
5. **Sandbox Implementation** — hand the non-canon draft to the **non-prod code agent** to wrap it in structural Ren'Py/Python logic inside the `narrative/draft/` folder. All creative text from the draft must be copied verbatim.
6. **Validation & Promotion** — hand the sandbox draft through **forensic psychology promotion review** and then to the **prod code agent** to promote the code into `renpy_project/game/dayrdd.rpy` and update the assets manifest.
7. **Architecture & Review** — the **chief architect** reviews Ren'Py production changes for technical methodology and ensures no creative drift (making sure dialogue and prose were preserved 100% verbatim from the Writers' Room).

## Day file naming contract

- **Non-canon draft scripts** must be named `dayrdd_non_canon.rpy`.
- **Ren'Py episodic runtime files** must be named `dayrdd.rpy`.
- `r` is the release number, and `dd` is the 2-digit day slot (`00`-`99`).
- Example: release 1 prologue/day 00 -> `day100_non_canon.rpy`; release 1 day 1 -> `day101_non_canon.rpy` and `day101.rpy`.
- This contract is enforced in CI via `scripts/engineering_compliance.py`.

## What is *not* in scope for MVP

- No required JSON beat payloads, no markdown→JSON→Ren’Py automation.
- Deferred ideas live in **`docs/backlog/`** (see `docs/backlog/narrative-json-beat-pipeline.md`).

## Optional non-canon draft conventions

These are suggestions, not rules:

- **Labels:** `label day2_morning:` as a line you intend to become a Ren’Py label.
- **Menus:** sketch branches with intent, e.g. `menu: # risky vs safe`.
- **State:** `$ player.raise_suspicion(10)` or plain English: “after choice: +Susp, flag read_letters”.
- **Characters:** `cora "..."` / `gideon "..."` matching how you expect sprites to be defined in the game.

The prod code agent promotes this into runtime Ren'Py that matches `classes.rpy` / `variables.rpy` patterns, ensuring all prose remains identical to the approved writers' room script.

## Supporting narrative databases

- **Main characters (non-canon):** `narrative/draft/<name>_character_non_canon.md`
- **Minor characters (non-canon):** `narrative/draft/characters_non_canon.md`
- **Locations (non-canon):** `narrative/draft/locations_non_canon.md`
- **Voice guides:** `narrative/canon/voice_guides/*_voice_guide.md`
- Canon mirrors should live in `narrative/canon/` using `_canon.md` equivalents.
- **Psychology reports:** `narrative/pipeline/releases/<release>/dayrdd_forensic_psychology_profile_report.md` or `narrative/pipeline/character_profile_reports/`
