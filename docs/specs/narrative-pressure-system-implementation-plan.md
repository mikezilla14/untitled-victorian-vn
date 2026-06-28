# Narrative Pressure UI, Objective Journal, and Manuscript Readiness System Implementation Plan

Status: `planned`

Parent spec: [narrative-pressure-system.md](narrative-pressure-system.md)

## Goal

Implement the reframed narrative pressure system in the non-prod environment first, followed by production promotion. This plan splits work into three independent phases: Mechanics, UI Code, and Prose.

---

## Technical Strategy

1. **State Serialization**: Declare dynamic dictionaries/lists utilizing Ren'Py `default` statements (not `define` or inside `init python` blocks) to ensure save-game serialization compatibility.
2. **Non-prod First**: Build, integrate, and validate the code entirely in `main-game/non-prod-game/game/shared/` before promotion.
3. **Restrained Presentation**: Implement screen widgets using standard placeholder outlines and simple text cues first. Custom assets are deferred to a polish phase.

---

## Phased Task List

### Phase A - Mechanics & Data Layer (Core Engine)

Focuses strictly on the statistical model, state machines, calculations, and mathematical rules.

- [ ] **T_MECH.1: Declare Data Classes & States**
  - Add to `narrative_pressure_data.rpy`:
    - `suspicion` (dict mapping character keys to values)
    - `corruption` (integer)
    - `material_library` (dict mapping material IDs to metadata shapes)
    - `manuscript_material` (list of active/unspent materials)
    - `objectives` (dict mapping objective IDs to state objects)
    - `writing_assignments` (dict of assignments and requirements)
    - `chapter_focus_remaining` (integer)
    - `character_context` (present/relevant characters map)
    - `draft_quality` (dict of quality scores)
- [ ] **T_MECH.2: Implement Material Collection & Focus logic**
  - Add to `narrative_pressure_system.rpy`:
    - `add_material(material_id)`
    - `spend_focus(amount)`
    - `check_assignment_readiness()`
    - `update_available_variants(assignment_id)`
    - `complete_assignment(assignment_id, selected_variant)`
    - `expire_chapter_material(chapter_id)`
- [ ] **T_MECH.3: Implement Objective Lifecycle Controller**
  - Add to `narrative_pressure_system.rpy`:
    - `activate_objective(obj_id)`
    - `complete_objective(obj_id)`
    - `fail_objective(obj_id)`
    - `expire_objective(obj_id)`
- [ ] **T_MECH.4: Implement Suspicion Context Priority Calculator**
  - Add to `narrative_pressure_system.rpy`:
    - `set_scene_context(location, present, relevant)`
    - `get_hud_risk_character()` (calculates context score priorities)

---

### Phase B - Code & UI Wiring (Screens & Layouts)

Focuses strictly on rendering screens, visual transitions, overlay auto-hide visibility, and transaction batching.

- [ ] **T_CODE.1: Implement Notification Transaction Manager**
  - Add queue states and functions:
    - `pending_notification_bundle` default state
    - `begin_notification_bundle()`
    - `add_bundle_item(item_data)`
    - `flush_notification_bundle()`
- [ ] **T_CODE.2: Build Composite Notification Screen**
  - Implement the screen `narrative_notification_overlay` in `narrative_notification_screen.rpy`.
  - Display composite cards containing themed colors and standard/breakpoint layout text.
- [ ] **T_CODE.3: Build Objective Journal Screen**
  - Implement `journal_screen` in `journal_screen.rpy` with tabs for Current Manuscript, Active Objectives, Optional Opportunities, Risks, and Completed tasks.
- [ ] **T_CODE.4: Build Overlay HUD Screen**
  - Implement `narrative_hud` in `hud_screen.rpy`.
  - Control visibility centrally using global overlays `hud_enabled` and `cinema_mode`.

---

### Phase C - Prose & Script Integration (Content & Writing)

Focuses on writing the actual story content, descriptive logs, warning text, and integrating them into game scenes.

- [ ] **T_PROSE.1: Write Material Registries & Library Descriptions**
  - Populate `material_library` with immersive narrative descriptions, tiers, and category tags.
- [ ] **T_PROSE.2: Write Objective Details & Risk Warnings**
  - Write journal text entries, descriptions, and warning notes for active and expiring objectives.
- [ ] **T_PROSE.3: Write Non-Diegetic Cues & Breakpoint Warning Variants**
  - Write text deltas for standard cues and breakpoint monologue crossings for each watcher (Vance, Stern, Missy, Gideon).
- [ ] **T_PROSE.4: Author Script Smoke Test Sequence**
  - Author a dummy scene sequence (`label test_narrative_pressure_system`) using the wrapper APIs to prove the integrated flow.

---

## Verification Plan

### Automated Validation
Run the project's linter checklist:
```powershell
py scripts/validate.py --profile changed --agent writers_room --skip-gate-checks --files "main-game/non-prod-game/game/shared/narrative_pressure_data.rpy" "main-game/non-prod-game/game/shared/narrative_pressure_system.rpy" "main-game/non-prod-game/game/shared/narrative_notification_screen.rpy" "main-game/non-prod-game/game/shared/journal_screen.rpy" "main-game/non-prod-game/game/shared/hud_screen.rpy"
```

### Manual Smoke-Testing Matrix
- **Phase A (Mechanics)**: Call `add_material` and verify states via debug console. Validate variant draft lock constraints.
- **Phase B (UI Code)**: Show screens `journal_screen` and `narrative_hud`. Trigger transactions, confirm multiple updates flush as a single composite notification.
- **Phase C (Prose)**: Play through the dummy scene, reading the resulting objective log entries, notification cards, and writing outcomes.
