# Character-Specific Suspicion Implementation Plan

Status: `partial`

Parent spec: [character-specific-suspicion.md](character-specific-suspicion.md)

## Goal

Implement breakpoint-based, character-specific suspicion feedback without restoring the removed global red suspicion vignette. The existing runtime already has two-tier per-character suspicion on `PlayerStats`; this work adds event feedback, breakpoint memory, monologue selection, and a restrained character-focus UI.

## Current Runtime Baseline

- `PlayerStats` already tracks `stern`, `vance`, `gideon`, and `missy` with base and acute suspicion.
- `PlayerStats.add_suspicion(char, acute_amount=0, base_amount=0)` already clamps and recalculates anxiety.
- `apply_effects(...)` already accepts `stern_susp`, `stern_base`, `vance_susp`, `vance_base`, `missy_susp`, `missy_base`, `gideon_susp`, and `gideon_base`.
- `cora_inner` exists in production but does not use the non-prod thought overlay yet.
- Non-prod shared files have an auto-highlight system and callbacks; production does not currently have `renpy_project/game/00auto_highlight.rpy`.
- The old anxiety-scaled `ui_suspicion_vignette` was removed from the HUD and manifest.

## Implementation Strategy

Implement this in four narrow passes:

1. Implement and validate each feature pass in the non-prod Ren'Py project.
2. Promote the validated non-prod shape into production.
3. Re-run production validation after promotion.

Within that non-prod-first path, use four narrow implementation passes:

1. Mechanics and API: add breakpoint memory, tier helpers, monologue lookup, and `raise_suspicion`.
2. Runtime integration: route existing `apply_effects(..._susp, ..._base)` through the new helper without breaking existing scripts.
3. Feedback UI: add `suspicion_focus`, a small eye/attention screen, and optional sprite focus integration.
4. Content and smoke scene: seed monologue tables and add a temporary/dev-only test path or documented manual smoke sequence.

Production and non-prod should remain aligned, but production should not blindly copy non-prod-only writing-gate differences.
New feature behavior should never be implemented in production first.

## Architectural Decisions

- Store breakpoint history on `PlayerStats`, not loose globals, because suspicion state already lives there.
- Trigger breakpoints from total suspicion (`base + acute`), because anxiety and confrontation checks already operate on total suspicion.
- Trigger breakpoint feedback only on upward crossings. Suspicion reductions never fire monologues.
- Keep `apply_effects` as the existing narrative API, but add `raise_suspicion` as the explicit low-level helper and future writer-facing call.
- Keep anxiety automatic from suspicion totals for current runtime compatibility. Do not add separate manual anxiety APIs in this pass unless a later design explicitly changes the model.
- Keep authored suspicion prose in `suspicion_monologues_non_canon.rpy` first, then promote to `suspicion_monologues.rpy`; runtime functions should only perform lookup and trigger behavior.
- Use text/symbol placeholder UI first. Final eye art is a polish task.

## Task List

### Phase 0 - Prep And Scope Lock

- [x] T0.1 Confirm the non-prod shared-file move is intentional before editing moved shared files in bulk.
- [x] T0.2 Re-run `git status --short` and record unrelated dirty files before implementation.
- [x] T0.3 Confirm whether production should receive the auto-highlight module now or whether sprite emphasis remains non-prod-only for this pass.
- [x] T0.4 Decide whether debug-only testing labels are allowed in production or should live only in non-prod.

Acceptance:

- The implementation target set is explicit before code changes begin.
- No unrelated moved/deleted non-prod files are reverted.

### Phase 1 - Mechanics And API

- [x] T1.1 Add suspicion constants to `renpy_project/game/functions.rpy` or another runtime utility block:
  - `SUSPICION_BREAKPOINTS = [15, 35, 60, 85]`
  - `SUSPICION_TIERS`
  - `ANXIETY_TIERS`
- [x] T1.2 Add `suspicion_breakpoints_seen` to `PlayerStats.__init__`, initialized for each tracked character.
- [x] T1.3 Add `suspicion_tier(value)` and `anxiety_tier(value)` helpers.
- [x] T1.4 Add `crossed_suspicion_breakpoints(old, new)` helper.
- [x] T1.5 Add `PlayerStats.record_suspicion_breakpoints(character, breakpoints)` or equivalent method that records newly crossed breakpoints and returns only unseen breakpoints.
- [x] T1.6 Add `raise_suspicion(character, amount=0, base_amount=0, reason=None, scene_context=None, feedback=True)`:
  - validate character against `player.tracked_characters`
  - read old total suspicion
  - call `player.add_suspicion(character, acute_amount=amount, base_amount=base_amount)`
  - read new total suspicion
  - skip feedback if total did not change
  - invoke minor feedback for non-zero changes
  - invoke breakpoint feedback only for unseen upward breakpoint crossings
- [x] T1.7 Mirror the same mechanical changes into `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/classes_non_canon.rpy` and `functions_non_canon.rpy`, preserving non-prod-only writing-gate semantics.

Acceptance:

- A direct `raise_suspicion("vance", 12)` changes only Vance suspicion.
- A direct `raise_suspicion("vance", -5)` lowers Vance suspicion and does not trigger breakpoint monologue.
- Breakpoint history survives normal stat updates.

### Phase 2 - Existing `apply_effects` Integration

- [x] T2.1 Update production `apply_effects` so each non-zero acute/base suspicion delta routes through `raise_suspicion`.
- [x] T2.2 Preserve existing `apply_effects` return behavior for inspiration spending.
- [x] T2.3 Preserve the hard error for deprecated generic `susp`.
- [x] T2.4 Decide and document whether multiple character suspicion changes in one `apply_effects` call may produce multiple feedback beats.
- [x] T2.5 If multiple beats are allowed, process them in deterministic order: `stern`, `vance`, `gideon`, `missy`.
- [x] T2.6 Mirror into non-prod `functions_non_canon.rpy`.

Acceptance:

- Existing day scripts using `apply_effects(vance_susp=35, insp=15, corr=5)` still work.
- Existing calls with only inspiration/corruption do not show suspicion feedback.
- Generic `apply_effects(susp=...)` still fails.

### Phase 3 - Monologue Table

- [x] T3.1 Add `suspicion_monologues` table in a dedicated prose/data file, non-prod first:
  - `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/suspicion_monologues_non_canon.rpy`
  - `renpy_project/game/suspicion_monologues.rpy`
- [x] T3.2 Implement `get_suspicion_monologue(character, tier, anxiety, reason=None, scene_context=None)`.
- [x] T3.3 Implement fallback lookup in this order:
  - character + tier + anxiety + reason + scene context
  - character + tier + anxiety + reason
  - character + tier + anxiety
  - character + tier
  - generic + tier + anxiety
  - generic fallback
- [x] T3.4 Seed at least one line for every character at `noticed`.
- [x] T3.5 Seed generic fallback lines for `noticed`, `watching`, `dangerous`, and `critical` across low/high anxiety.
- [x] T3.6 Keep all lines one sentence unless a later writing pass explicitly expands them.
- [x] T3.7 Promote the validated non-prod table into production; non-prod remains the feature source path.

Acceptance:

- Every breakpoint can produce a non-empty line.
- Missing reason/context combinations resolve through fallback.
- The line selected for high anxiety differs from low anxiety where both exist.

### Phase 4 - Feedback Labels And UI State

- [x] T4.1 Add defaults in `variables.rpy`:
  - `suspicion_focus = None`
  - `suspicion_focus_intensity = 0`
- [x] T4.2 Add `label suspicion_feedback_minor(character, old, new)` in a runtime script file.
- [x] T4.3 Add `label suspicion_breakpoint(character, breakpoint, reason=None, scene_context=None)`.
- [x] T4.4 Use `cora_inner` for breakpoint monologues.
- [x] T4.5 Add `screen suspicion_attention(character)` as a small text/symbol UI near the dialogue box or HUD edge.
- [x] T4.6 Display broad tier labels only, not exact numbers, in the player-facing attention UI.
- [x] T4.7 Ensure the attention UI hides when `suspicion_focus` is `None`.
- [x] T4.8 Mirror labels/screens/defaults into non-prod locations.

Acceptance:

- Minor changes produce a brief focus pulse and no monologue.
- Breakpoint changes produce a brief focus pulse plus exactly one `cora_inner` line.
- No full-screen red vignette returns.

### Phase 5 - Sprite Highlight Integration

- [x] T5.1 Decide whether to promote non-prod `00auto_highlight.rpy` to production or implement suspicion focus only in non-prod first.
- [x] T5.2 If promoting, update production `characters.rpy` to pass callbacks matching non-prod `characters.rpy`.
- [x] T5.3 Update highlight priority:
  - suspicion focus wins
  - active speaker is second
  - idle dim is fallback
- [x] T5.4 Add a restrained suspicion transform state: slight scale, brightness, or contrast shift only.
- [x] T5.5 Ensure `cora_inner` does not accidentally highlight Cora or clear the suspicion target too early.

Acceptance:

- If Vance notices while Stern is speaking, Vance receives suspicion focus.
- Active speaker highlighting still works when there is no suspicion focus.
- Inner monologue does not produce focus bugs.

### Phase 6 - Content Pass

- [x] T6.1 Write 5-8 Vance monologue lines.
- [x] T6.2 Write 5-8 Stern monologue lines.
- [x] T6.3 Write 5-8 Gideon monologue lines.
- [x] T6.4 Write 5-8 Missy monologue lines.
- [x] T6.5 Add reason tags only for already common script contexts, such as `recognised_detail`, `pattern_detected`, `disciplinary_notice`, or `hurt_trust`.
- [x] T6.6 Run a prose pass for tone consistency: knife-tip, not diary.

Acceptance:

- Lines reflect each character's threat profile.
- Fallback lines are good enough to ship without sounding like placeholders.

### Phase 7 - Tests And Validation

- [ ] T7.1 Add or update a lightweight script/test fixture if the repo has an existing Ren'Py lint harness for function-level checks.
- [ ] T7.2 Manually test Vance crossing 15 from below.
- [ ] T7.3 Manually test Vance rising within the same tier.
- [ ] T7.4 Manually test Stern crossing multiple breakpoints in one jump; only the highest crossed breakpoint should monologue, unless implementation deliberately queues all.
- [ ] T7.5 Manually test suspicion reduction.
- [ ] T7.6 Manually test high-anxiety monologue selection.
- [x] T7.7 Run production validation:

```powershell
py scripts/validate.py --profile changed --agent human --files "renpy_project/game/classes.rpy,renpy_project/game/functions.rpy,renpy_project/game/variables.rpy,renpy_project/game/screens.rpy,renpy_project/game/script.rpy,renpy_project/game/characters.rpy"
```

- [x] T7.8 Run non-prod validation:

```powershell
py scripts/validate.py --profile changed --agent writers_room --skip-gate-checks --files "narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/classes_non_canon.rpy,narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/functions_non_canon.rpy,narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/screens.rpy,narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/characters.rpy"
```

Acceptance:

- Validation exits successfully.
- Asset audit may report existing missing physical assets, but active referenced image/audio declarations must remain synchronized.
- Manual smoke checks match the spec.

## Suggested Implementation Order

1. T0.1-T0.4
2. Implement T1.1-T1.7 in non-prod shared files.
3. Implement T3.1-T3.6 in non-prod, keeping authored prose in `suspicion_monologues_non_canon.rpy`.
4. Implement T4.1-T4.8 in non-prod.
5. Implement T2.1-T2.6 in non-prod.
6. Run non-prod validation and manual smoke checks.
7. Promote the validated non-prod mechanics, UI, and prose table into production.
8. Run production validation and manual smoke checks.
9. Decide and implement Phase 5 sprite highlight integration through the same non-prod-first promotion path.
10. Complete Phase 6 content pass through the same non-prod-first promotion path.
11. Run final production and non-prod validation.

## Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| `apply_effects` triggers too many interruption beats | Scenes feel choppy | Minor feedback for every change, monologue only on unseen upward breakpoints. |
| Multiple character deltas in one call create ambiguous focus | Wrong character appears psychologically important | Use deterministic processing order and document it. |
| Production lacks callback-based auto-highlight | Sprite focus cannot be implemented cleanly | Ship mechanical/UI pass first; promote non-prod highlight module as a separate task. |
| Breakpoint history stored outside `PlayerStats` drifts from saves | Repeated monologues or missing monologues | Keep breakpoint history class-backed on `PlayerStats`. |
| Fallback prose sounds generic | System feels mechanical | Seed strong generic fallback lines and keep them short. |
| Non-prod writing-gate differences get overwritten | Draft sandbox regresses | Mirror only suspicion-specific changes into non-prod. |

## Done Definition

- Existing suspicion deltas still work through `apply_effects`.
- `raise_suspicion` exists and is safe for direct scene use.
- Suspicion breakpoints are tracked per character and do not retrigger.
- UI feedback identifies the suspicious character without a persistent full-screen vignette.
- Breakpoint monologues use table-driven authored lines with fallback.
- Production and non-prod validation pass.
- The parent spec is updated from `planned` to `partial` or `implemented`, depending on shipped scope.
