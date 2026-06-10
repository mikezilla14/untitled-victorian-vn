# 📋 MVP Production Workflow Backlog

This backlog organizes the remaining tasks required to complete the **Playable 5-Day MVP Demo** into two distinct, highly actionable pipelines: **Narrative Workflow** and **Coding Workflow**. 

Tasks are pre-formatted for direct allocation to human developers or specific specialist agents (from [AGENTS.md](../../AGENTS.md)).

---

## 🎨 Pipeline A: Narrative Workflow (Lore, Voice, & Gating)
*Focus: Creative writing, historical accuracy sweeps, psychological profiling, and gating validation.*

### 🟢 [N-1] Historical Linter Anachronisms Cleansing
* **Description:** Complete (2026-06-10). Replaced modern clinical terms in non-canon character profiles with 1891 period-appropriate vocabulary; `historical_linter.py` clean on all three bible files.
* **Affected Files:**
  * [cora_character_non_canon.md](../../narrative/draft/bible/cora_character_non_canon.md) — "trauma" → "grievous shock"
  * [stern_character_non_canon.md](../../narrative/draft/bible/stern_character_non_canon.md) — "trauma" → "grievous shock"
  * [vance_character_non_canon.md](../../narrative/draft/bible/vance_character_non_canon.md) — "projecting" → "casting"
* **Assignee:** `victorian_consultant`
* **Verification Command:**
  ```powershell
  py scripts/historical_linter.py --file narrative/draft/bible/cora_character_non_canon.md
  ```

---

### 🟢 [N-2] Day 100 Prologue Specialist Gates Clearance
* **Description:** Complete (2026-06-10). Rewrote prologue to start in motion, generated all three specialist gates, and validated successfully.
* **Target Paths:** Write verdict markdown and JSON sidecars inside:
  * `narrative/pipeline/releases/release-1-mvp/days/day100/gates/`
* **Required Gates:**
  * **Lead Narrative Gate:** Check story boarding, stat alignments, and voice guides.
  * **Forensic Psychology Gate:** Verify psychological consistency of the desk search / overheard dialogue choices.
  * **Victorian Gate:** Double check period-appropriate idioms.
* **Assignee:** `lead_narrative_editor` + `forensic_psychology_consultant` + `victorian_consultant`
* **Verification Command:**
  ```powershell
  py scripts/validate.py --profile changed --agent human --files "narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day100_non_canon.rpy"
  ```

---

### 🔴 [N-3] Day 103 Writers' Room Pipeline Convergence
* **Description:** Day 103 has been promoted into production, but its official Writers' Room pipeline folder is completely missing. Generate the convergent report, sandboxed specs, and gate reviews.
* **Target Paths:** Create directory and populate:
  * `narrative/pipeline/releases/release-1-mvp/days/day103/`
* **Required Output Deliverables:**
  * `synthesis/day103_convergent_report.md`
  * `specs/` (Sandboxed Ren'Py-shaped spec files)
  * `gates/` (All 3 gate verdicts: Narrative, Forensic Psychology, Victorian)
* **Assignee:** `convergent_writer` + Gates
* **Verification Command:**
  ```powershell
  py scripts/validate.py --profile full
  ```

---

### 🔴 [N-4] Day 104 Writers' Room Pipeline Convergence
* **Description:** Day 104 has been promoted into production, but its official Writers' Room pipeline folder is completely missing. Generate the convergent report, sandboxed specs, and gate reviews.
* **Target Paths:** Create directory and populate:
  * `narrative/pipeline/releases/release-1-mvp/days/day104/`
* **Required Output Deliverables:**
  * `synthesis/day104_convergent_report.md`
  * `specs/` (Sandboxed Ren'Py-shaped spec files)
  * `gates/` (All 3 gate verdicts: Narrative, Forensic Psychology, Victorian)
* **Assignee:** `convergent_writer` + Gates
* **Verification Command:**
  ```powershell
  py scripts/validate.py --profile full
  ```

---

### 🟡 [N-5] Prose Formatting Repair for Day 102 Draft
* **Description:** The non-canon formatting check failed for the Day 102 draft file. Standardize its indentation and structure to ensure clean linter compliance.
* **Affected File:** [day102_non_canon.rpy](../../narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy)
* **Assignee:** `convergent_writer` or Script Tool
* **Action Command:**
  ```powershell
  py scripts/format_non_canon.py
  ```

---

### 🔴 [N-6] Complete Story Chains Rewrite (From Scratch)
* **Description:** Complete, from-scratch rewrite of `story_chains_non_canon.rpy` to transform optional character paths into high-tension, Level 3/4 spicier narrative tracks (Missy, Stern, and Vance). The chains must serve as the primary engine for high-risk stat gains, accommodate dynamic day/time contexts, and force sharp opportunity-cost player decisions.
* **Affected File:** [story_chains_non_canon.rpy](../../narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy)
* **Assignee:** `convergent_writer` + specialist editors
* **Verification Command:**
  ```powershell
  py scripts/validate.py --profile narrative --files "narrative/draft/releases/release-1-mvp/shared/story_chains_non_canon.rpy"
  ```

---
---

## 💻 Pipeline B: Coding Workflow (Ren'Py Development & Integration)
*Focus: Script integration, runtime flow, state discipline, and tool chain repair.*

### 🔴 [C-1] Day 100 Prologue Production Promotion
* **Description:** Once Day 100 clears its specialist narrative gates (Task `[N-2]`), promote the draft script verbatim into production.
* **Source File:** [day100_non_canon.rpy](../../narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day100_non_canon.rpy)
* **Target File:** `[NEW]` `renpy_project/game/day100.rpy`
* **Assignee:** `prod_code_agent`
* **Verification Command:**
  ```powershell
  py scripts/validate.py --profile code --files "renpy_project/game/day100.rpy"
  ```

---

### 🔴 [C-2] Game Start Entry Point Integration
* **Description:** The production runtime currently skips Day 100, jumping directly to Day 101. Integrate the Prologue so the game launches correctly.
* **Affected File:** [script.rpy](../../renpy_project/game/script.rpy#L15) (Line 15)
* **Action:** Change the target of the `start` label jump:
  ```diff
  - jump day101_main
  + jump day100_main
  ```
* **Assignee:** `prod_code_agent`
* **Verification Command:**
  ```powershell
  # Check for correct jump target alignment
  py scripts/validate.py --profile code
  ```

---

### 🔴 [C-3] Purge Temporary Day 102 & 103 Transition Stubs
* **Description:** Clean up non-prod transition stubs in production scripts that were created during sequential drafting.
* **Action Items:**
  * In [day102.rpy](../../renpy_project/game/day102.rpy), purge the temporary `day103_morning` stub. 
  * In [day103.rpy](../../renpy_project/game/day103.rpy), purge the `# HANDOFF STUB` and the temporary `day104_041` stub.
* **Assignee:** `prod_code_agent`
* **Verification Command:** Run Ren'Py Lint to ensure clean compilation.

---

### 🔴 [C-4] Purge Temporary Day 104 Transition Stubs
* **Description:** Clean up non-prod transition stubs in the production script for Day 104.
* **Action Item:**
  * In [day104.rpy](../../renpy_project/game/day104.rpy), purge the temporary `day105_1_monster_reemerges` stub.
* **Assignee:** `prod_code_agent`
* **Verification Command:** Run Ren'Py Lint.

---

### 🟡 [C-5] Central Assets Manifest Audit & Verification
* **Description:** Verify that every asset referenced in the newly promoted Day 103, Day 104, and Day 105 files is declared in the Central Assets Manifest to prevent runtime graphics crashes.
* **Affected File:** [assets_manifest.rpy](../../renpy_project/game/assets_manifest.rpy)
* **Audit Checklist:** Check references for:
  * Sprite: `vance_sprite mirror_watch_terror`
  * CGs: `cg_manuscript_retelling_d3_brush`, `cg_manuscript_retelling_d4_false_dawn`, `cg_gideon_photograph`
* **Assignee:** `chief_architect`
* **Verification Command:** Check the `report_missing_assets()` output inside `log.txt` during game start.

---

### 🟢 [C-6] Repair agent_next_step.py Typo
* **Description:** Fix the unescaped double-quote syntax error on line 143 of the pipeline script so standard diagnostic listings can run without crashing.
* **Affected File:** [agent_next_step.py](../../scripts/agent_next_step.py#L143) (Line 143)
* **Suggested Fix:**
  ```diff
  - print("Validate: py scripts/validate.py --profile changed --agent <name> --files /"<paths>/"")
  + print("Validate: py scripts/validate.py --profile changed --agent <name> --files /"<paths>/"")
  ```
* **Assignee:** `chief_architect`
* **Verification Command:**
  ```powershell
  py scripts/agent_next_step.py --list-pipelines
  ```
