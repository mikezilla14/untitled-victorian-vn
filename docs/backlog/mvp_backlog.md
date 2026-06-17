# 📋 MVP Production Workflow Backlog

This backlog organizes the remaining tasks required to complete the **Playable 5-Day MVP Demo** into two distinct, highly actionable pipelines: **Narrative Workflow** and **Coding Workflow**. 

Tasks are pre-formatted for direct allocation to human developers or specific specialist agents (from [AGENTS.md](../../AGENTS.md)).

---

## 🎨 Pipeline A: Narrative Workflow (Lore, Voice, & Gating)
*Focus: Creative writing, historical accuracy sweeps, psychological profiling, and gating validation.*

### 🟢 [N-1] Historical Linter Anachronisms Cleansing
* **Description:** Complete (2026-06-10). Replaced modern clinical terms in non-canon character profiles with 1891 period-appropriate vocabulary; `historical_linter.py` clean on all three bible files.
* **Affected Files:**
  * [cora_character_non_canon.md](../../main-game/draft/bible/cora_character_non_canon.md) — "trauma" → "grievous shock"
  * [stern_character_non_canon.md](../../main-game/draft/bible/stern_character_non_canon.md) — "trauma" → "grievous shock"
  * [vance_character_non_canon.md](../../main-game/draft/bible/vance_character_non_canon.md) — "projecting" → "casting"
* **Assignee:** `victorian_consultant`
* **Verification Command:**
  ```powershell
  py scripts/historical_linter.py --file main-game/draft/bible/cora_character_non_canon.md
  ```

---

### 🟢 [N-2] Day 100 Prologue Specialist Gates Clearance
* **Description:** Complete (2026-06-10). Rewrote prologue to start in motion, generated all three specialist gates, and validated successfully.
* **Target Paths:** Write verdict markdown and JSON sidecars inside:
  * `main-game/pipeline/releases/release-1-mvp/days/day100/gates/`
* **Required Gates:**
  * **Lead Narrative Gate:** Check story boarding, stat alignments, and voice guides.
  * **Forensic Psychology Gate:** Verify psychological consistency of the desk search / overheard dialogue choices.
  * **Victorian Gate:** Double check period-appropriate idioms.
* **Assignee:** `lead_narrative_editor` + `forensic_psychology_consultant` + `victorian_consultant`
* **Verification Command:**
  ```powershell
  py scripts/validate.py --profile changed --agent human --files "main-game/non-prod-game/game/days/day100_non_canon.rpy"
  ```

---

### 🟢 [N-3] Day 103 Writers' Room Pipeline Convergence
* **Description:** Complete (2026-06-10). All Day 103 Writers' Room pipeline deliverables (convergent report, sandboxed specs, and gate reviews) are generated and validated.
* **Target Paths:** Create directory and populate:
  * `main-game/pipeline/releases/release-1-mvp/days/day103/`
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

### 🟢 [N-4] Day 104 Writers' Room Pipeline Convergence
* **Description:** Complete (2026-06-10). All Day 104 Writers' Room pipeline deliverables (convergent report, sandboxed specs, and gate reviews) are generated and validated.
* **Target Paths:** Create directory and populate:
  * `main-game/pipeline/releases/release-1-mvp/days/day104/`
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
* **Affected File:** [day102_non_canon.rpy](../../main-game/non-prod-game/game/days/day102_non_canon.rpy)
* **Assignee:** `convergent_writer` or Script Tool
* **Action Command:**
  ```powershell
  py scripts/format_non_canon.py
  ```

---

### 🟢 [N-6] Complete Story Chains Rewrite (From Scratch)
* **Description:** Complete (2026-06-10). Completed, from-scratch rewrite of `story_chains_non_canon.rpy` to transform optional character paths into high-tension, Level 3/4 spicier narrative tracks (Missy, Stern, and Vance) at 2.8 and 2.2-2.5 spice. The chains serve as the primary engine for high-risk stat gains, accommodate dynamic day/time contexts, and force sharp opportunity-cost player decisions with descriptive diegetic locks.
* **Affected File:** [story_chains_non_canon.rpy](../../main-game/non-prod-game/game/shared/story_chains_non_canon.rpy)
* **Assignee:** `convergent_writer` + specialist editors
* **Verification Command:**
  ```powershell
  py scripts/validate.py --profile narrative --files "main-game/draft/releases/release-1-mvp/shared/story_chains_non_canon.rpy"
  ```

---
---

## 💻 Pipeline B: Coding Workflow (Ren'Py Development & Integration)
*Focus: Script integration, runtime flow, state discipline, and tool chain repair.*

### 🟢 [C-1] Day 100 Prologue Production Promotion
* **Description:** Complete (2026-06-10). Promoted `day100_non_canon.rpy` verbatim into `main-game/prod-game/game/day100.rpy`; added prologue `StoryState` fields (`prologue_why_write`, `prologue_holywell_posture`) and Day 100 asset fallbacks in production manifest; wrote `day100_promotion_handoff.json`.
* **Source File:** [day100_non_canon.rpy](../../main-game/non-prod-game/game/days/day100_non_canon.rpy)
* **Target File:** `main-game/prod-game/game/day100.rpy`
* **Assignee:** `prod_code_agent`
* **Verification Command:**
  ```powershell
  py scripts/validate.py --profile code --files "main-game/prod-game/game/day100.rpy"
  ```

---

### 🟢 [C-2] Game Start Entry Point Integration
* **Description:** Complete (2026-06-10). Non-prod `script.rpy` already jumped to `day100_main`; production `script.rpy` updated to match. Added `bg_country_estate_corridor_night` fallback to non-prod manifest.
* **Affected File:** [script.rpy](../../main-game/prod-game/game/script.rpy#L15)
* **Assignee:** `prod_code_agent`
* **Verification Command:**
  ```powershell
  py scripts/validate.py --profile code
  ```

---

### 🟢 [C-3] Purge Temporary Day 102 & 103 Transition Stubs
* **Description:** Complete (2026-06-10). Removed `HANDOFF STUB` / `label day104_1` forwarder from non-prod `day103_non_canon.rpy`; night exit now jumps directly to `day104_1_false_dawn_suite_window`. Removed stale promotion notes from `day102_non_canon.rpy` and `day104_non_canon.rpy`. Production `day103.rpy` already lacked the handoff stub.
* **Assignee:** `non_prod_code_agent` → `prod_code_agent`
* **Verification Command:**
  ```powershell
  py scripts/validate.py --profile code --files "main-game/prod-game/game/day102.rpy,main-game/prod-game/game/day103.rpy"
  ```

---

### 🟢 [C-4] Purge Temporary Day 104 Transition Stubs
* **Description:** Complete (2026-06-10). No forwarder stub existed in production `day104.rpy` (legitimate `jump day105_1_monster_reemerges` to promoted `day105.rpy`). Non-prod `day104_6_false_dawn_ending` aligned with production spine (`set_time_period`, `resolve_turn`); removed stale Day 105 stub promotion note from `day105_non_canon.rpy`.
* **Assignee:** `non_prod_code_agent` → `prod_code_agent`
* **Verification Command:**
  ```powershell
  py scripts/validate.py --profile code --files "main-game/prod-game/game/day104.rpy"
  ```

---

### 🟢 [C-5] Central Assets Manifest Audit & Verification
* **Description:** Complete (2026-06-10). Verified that every asset referenced in day files is declared in the Central Assets Manifest, including declaring `cg_manuscript_retelling_d1-d4`, `cg_gideon_photograph`, and `cg_photograph_burning` to prevent future runtime crashes. Compliance check passes.
* **Affected File:** [assets_manifest.rpy](../../main-game/prod-game/game/assets_manifest.rpy)
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
