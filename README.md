# Project Name: [Pending Title]

An AI-accelerated, adult pseudo-sandbox RPG visual novel set in a Victorian hotel. This project explores themes of dark gothic corruption, voyeurism, and the loss of purity, utilizing a dynamic "paper doll" visual state system.

## Repository Architecture (Monorepo)

This repository is structured as a Monorepo to maintain all creative, technical, and developmental assets in a single location. It features strict access controls via AI agent guardrails to ensure narrative and code fidelity.

* **`/docs`**: Production and architecture documentation. Contains the Game Dev Bible, Game Mechanics Bible.
* **`/narrative/writers_room`**: The rapid-prototyping drafting sandbox. Contains all `*_non_canon.md` episodic drafts, storyboards, and character profiles. Iterative AI generation happens here.
* **`/narrative/canon`**: The immutable truth folder. Only rigorously validated, canonical files reside here. Files are promoted into this directory by the Lead Narrative Editor only.
* **`/scripts`**: Python-based CI/CD tooling used for custom linting and validation of narrative schemas. 
* **`/.agents`**: The behavioral rules logic outlining the personas and strict functions of the AI development team.
* **`/art_pipeline`**: Asset generation tools (ComfyUI workflows, Stable Diffusion prompts).
* **`/renpy_project`**: The actual playable game. Contains the standard Ren'Py structure (`classes.rpy`, `screens.rpy`, episodic scripts).

## Tech Stack & Tools

* **Game Engine**: Ren'Py (v8+ for Python 3 support)
* **IDE**: Anti-gravity / Cursor / VSCode
* **AI Art Generation**: Stable Diffusion (ComfyUI) using Pony Diffusion V6 XL
* **Version Control**: Git / GitHub

---

## The AI Agent Framework & Guardrails

This project utilizes designated AI agent roles governed by explicit permissions enforced in **`.guardrails.yml`**. Agents are strictly prohibited from touching files outside their domains.

1. **Gatekeeper Orchestrator**: Enforces security policies and blocks unauthorized PRs.
2. **Chief Architect**: The technical gatekeeper. Designs class architecture and ensures Ren'Py code does not leak global states. Restricted to `framework_code` and `episodic_code`.
3. **Lead Narrative Editor**: The lore gatekeeper. Promotes drafts out of the Writers' Room into Canon. Owns the `canon_lore` domain.
4. **Writers' Room**: The creative engine. Generates continuous narrative drafts and ideas. Restricted to the `production_narrative` and `speculative_sandbox`.
5. **Victorian Consultant**: The historical continuity verifier. Flags anachronistic dialogue and dialect issues.
6. **Code Agent**: Implements validated rules directly into the Ren'Py logic.

## Narrative Generation & Promotion Pipeline

We use a formalized schema to ensure continuous generation remains tight, playable, and highly structured on a granular mechanical level. 

### 1. Authoring in the Writers' Room
Episodic sequences (Days) are written into discrete files (e.g. `day1_non_canon.md`). All player choices within the game must follow **`narrative/templates/beat_schema.json`**, ensuring that dialogue strictly tracks inline mechanic adjustments (e.g. `[+10 Corruption]`). Variables, choices, and aesthetic requirements are aggregated manually in `story_board.md`.

### 2. Validation & Linting
Before any file is considered for promotion, the following strict CI scripts are run locally:
* **Historical Linter** (`historical_linter.py`): Parses markdown to catch forbidden modern terminology (e.g. "okay", "teenager") as defined in `voice_guide.md`.
* **Beat Validator** (`validate_beats.py`): Extracts embedded JSON schemas in narrative files to verify minimum branching configurations and exact mechanic alignments.

### 3. Canon Promotion
Once a draft clears linting and the Lead Narrative Editor verifies tone consistency against `canon_lore`, the file is converted into `dayX_canon.md` and moved to `/narrative/canon/`. It becomes permanently immutable without human oversight.

---

## Development Philosophy & Scoping

* **Agentic AI Context**: By structuring the workspace logically, AI assistants rapidly ingest contextual documentation to generate functional logic without unprompted hallucinations.
* **Consistency > Quality**: The art pipeline prioritizes fixed seeds, control networks, and layer-based "Paperdoll" combinations over isolated generation to maintain narrative immersion. 
* **The "Rule of 3" Scope Cap**: To ensure rapid episodic releases, each module is strictly capped at 3 primary characters, 6 primary backgrounds, and 5 highly-polished event CGs.
