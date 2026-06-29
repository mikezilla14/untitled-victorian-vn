# Release 1 MVP Full Review

Date: 2026-06-28

Prior review: [`mvp_full_review_2026-06-21.md`](mvp_full_review_2026-06-21.md)

Requested lenses:

- Chief Architect: runtime structure, state discipline, validation, assets, packaging, and promotion readiness.
- Adult Market Reviewer: adult-VN promise, tension, payoff cadence, fetish clarity, and commercial presentation.
- Lead Narrative Editor: story architecture, character voice, continuity, choice meaning, and thematic resolution.

## Scope and Method

The path named in the request, `narrative/draft/releases/release-1-mvp/non_prod_renpy_project`, no longer exists. Repository documentation identifies `main-game/non-prod-game/` as the current equivalent and active non-production Ren'Py project. This review is therefore based on:

- `main-game/non-prod-game/`
- `main-game/prod-game/` (promotion target only — not credited for non-prod gaps)
- Direct Release 1 support files in `main-game/draft/releases/planning/`
- Release 1 graph, grain, balance, and QA artifacts in `main-game/pipeline/releases/release-1-mvp/`
- Canon and voice files directly required to judge the scripts

Production files were not used to give the non-production build credit. Backlog ideas were not counted as implemented features.

Evidence gathered:

- Fresh `scripts/validate.py --profile full` run — **PASS**
- Fresh `scripts/contract_validate.py` run for Day 100 and Day 105 — **PASS**
- Fresh repository unit-test run: **67 tests passed** (up from 61 on 2026-06-21)
- Fresh asset-manifest audit via `scripts/daily_asset_manifest.py`
- Fresh `scripts/balance_report.py --release release-1-mvp` — verdict **INCOMPLETE**
- Fresh `compare_runtime_to_model.py --release release-1-mvp` regeneration
- Review of `release1_route_matrix_results.md`, `runtime_model_comparison.md`, and captures `P1_corruption_forward.jsonl`, `P2_cautious.jsonl`, and `P4_deadline_1.jsonl`
- Static inspection of non-production source `.rpy` files, excluding bundled ActionEditor internals from narrative grading
- Review of current `log.txt` (clean Ren'Py 8.5.2 load on 2026-06-28; no active `traceback.txt`)
- Review of integration checklist, June 28 standup report, and sprint-close status

No complete human-equivalent manual playthrough of all required paths was performed as part of this static review. Three runtime captures exist on disk (P1 corruption-forward, P2 cautious, P4 deadline-1 fail). The remaining four matrix paths are still unrecorded.

## Executive Verdict

The project has cleared the validation blockers that stalled the June 21 review and added substantial player-facing systems, but release proof and visual payoff remain incomplete.

**Overall project grade: B+**

**Current public-build readiness: B-**

**MVP promotion verdict: DO NOT PROMOTE**

Since the June 21 review, the team resolved the `menu_carousel.rpy` compliance debt and screen-language linter false positives. Full repository validation now passes cleanly. New systems landed in non-prod: narrative pressure (objective journal, manuscript readiness, notification bundles), HUD sidebar and ledger UI, balance-engine choice catalogue integration, and expanded game-over wiring. Unit tests rose to 67 passed. Book 1 MVP engine was promoted to `main-game/prod-game/` with Day 100–105 runtime scripts present.

What still prevents promotion:

1. **Incomplete route matrix:** 3 / 7 captures recorded (P1, P2, P4). P3, P5, P6, and P7 are missing. `release1_route_matrix_results.md` is out of sync — it still lists only P1 as complete.
2. **P2 assertion tooling gap:** The cautious capture completes to `day105_7_release_one_ending`, but `assert_reaches_day_at_least: 105` fails because runtime stores day as `5` (slot index) while the model expects `105`.
3. **Missing visual payoff:** All seven declared event illustrations (six manuscript CGs plus photograph pair) are absent from disk. Active `show` commands in Day 104/105 remain commented out.
4. **Asset drift:** Twelve declared assets missing from both engines (five UI book-plate elements, seven CGs). Non-prod and prod asset pools have diverged significantly — prod holds most Savoy backgrounds and cast sprites; non-prod holds a different subset (country-estate backgrounds, partial Eleanor sprites, full audio pool).
5. **Playtest sign-off lag:** Integration checklist playtest matrix remains 0 / 12. Phase 2 fail-state verification is 2 / 8 despite static wiring passing.
6. **Packaging debt:** ActionEditor, test harnesses, debug capture overlay, placeholder metadata, and dev debris still require a deliberate distribution profile.

Promotion should resume only after the route matrix is complete and documented, the P2 day-index assertion is fixed, at least two manuscript CGs are on disk and wired, and a clean distribution candidate is tested on a fresh profile.

## Grade Summary

| Element | Grade | Assessment |
|---|---:|---|
| Core premise and differentiation | A | A covert Irish maid turning class danger and private scandal into forbidden fiction is clear, specific, and marketable. |
| Cora's character architecture | A- | Her survival mask, Irish concealment, authorial hunger, and moral danger form a strong protagonist engine. |
| Five-day narrative spine | B+ | Escalation is coherent from exposure risk to attempted leverage to structural defeat and artistic diagnosis. |
| Ending and thematic resolution | A- | Day 105 closes the release thematically without pretending Cora can defeat class power with one photograph. |
| Supporting cast | B+ | Gideon, Stern, Missy, and Vance each embody a distinct pressure system rather than functioning as route furniture. |
| Character voice and canon alignment | B+ | All six day packages have valid narrative, psychology, and Victorian gate contracts; Day 102 prose formatting repair is still pending. |
| Choice design and branch memory | B+ | Choices alter state, relationships, manuscript framing, and consequences. P1, P2, and P4 captures are recorded; P2 highlights a tool index mismatch. |
| Adult-market concept | A- | The kink ecology—service, surveillance, class authority, forbidden authorship, betrayal, and controlled submission—is unusually coherent. |
| Adult payoff delivery | B- | The prose has heat, but the promised visual manuscript payoff is largely absent. The game currently sells a stronger concept than build. |
| Manuscript writing system | B+ | Alt paths for Book 1 are implemented and documented; Sweeney Todd / Dracula transpositions render correctly on NVL screens. |
| Narrative pressure / player guidance | B | Objective journal, material bank, notification bundles, and manuscript readiness checks add commercial-grade onboarding to the writing loop. |
| State architecture | B+ | Central classes, setter-driven flags, whitelisted states, targeted suspicion, anxiety, named consequence windows, and balance profiles are strong prototype architecture. |
| Code quality and maintainability | B | Upgraded from B-. Full validation passes. `menu_carousel` variables centralized; screen-language linter is screen-aware. Day 103 Ch3 gate uses inline floor checks rather than `has_story_fuel(*WRITE_GATE_CH3)` — balance report flags a WARN. |
| UI/UX and game feel | B | Upgraded from B-. HUD sidebar, ledger, thought presentation, narrative-pressure notifications, dynamic menu carousel, dust motes, and bottom-navigation overlays substantially improve feel. |
| Visual asset readiness | C | Runtime backgrounds and sprites are covered through configured fallbacks in non-prod. Five UI book-plate assets and all seven CGs remain missing. Prod/non-prod asset pools are not reconciled. |
| Audio readiness | B- | Upgraded from C-. All 21 aliases resolve in non-prod; guarded `play` patterns are wired in Day 100 and book1. Broader day-script ambience integration remains thin; preview-track licensing still needs release treatment. |
| Testing and QA evidence | B- | Unit tests at 67 passed. Three recorded captures (P1, P2, P4) on disk; four matrix paths pending. Balance report verdict INCOMPLETE. Checklist playtest sign-off 0 / 12. |
| Documentation and pipeline discipline | B | Gates and handoffs are strong. Balance framework, book-writing engine export, and playtest checklist are documented. Route matrix markdown is stale vs captures. |
| Packaging/release professionalism | D+ | Placeholder name/version, ActionEditor and test harness content, compiled artifacts, saves, cache, logs, and helper scripts require a deliberate build profile. |

## What Is Working

### 1. Validation and compliance unblocked (New since June 21)

The June 21 blockers are resolved:

- `game_menu_background_slide` and related carousel state moved to `variables.rpy` (commit `4bfb134`).
- `renpy_contract_linter.py` is screen-language aware (commit `30850d1`).
- Fresh `scripts/validate.py --profile full` exits **0** with all Day 100–105 gate contracts, convergent reports, and spec scripts green.

This is the single largest engineering improvement since the prior review.

### 2. Narrative pressure and HUD systems (New since June 21)

Commits `e6bc0ef`, `484cdcf`, and `c4ce260` add player-facing guidance infrastructure:

- **Objective journal** with active/complete states and focus-cost tracking.
- **Manuscript material bank** with tiered snoop discoveries feeding writing readiness.
- **Notification bundles** for stat deltas, suspicion changes, and new objectives.
- **HUD sidebar, stats overlay, and ledger UI** with supporting asset cache.

Day 100 prologue now calls `add_material`, `add_stat_delta`, and `apply_balanced_effect` through the semantic balance profile layer, connecting narrative choices to the new pressure UI.

### 3. Balance engine and economy compression (New since June 21)

Commits `93f23fd`, `5ced503`, and `c124614` establish:

- Choice catalogue management and migration scripts.
- Generated `balance_profiles_non_canon.rpy` with semantic effect resolution.
- Balance economy compression spec and migration report.
- `apply_balanced_effect` as the preferred mutation path for new branches.

Static balance report confirms all manuscript gate constants, `complete_manuscript_chapter` hooks, and fail-state label wiring. Abstract simulator and runtime captures still diverge on cautious and low-corruption paths.

### 4. Book 1 alt paths and prod promotion (carried forward, extended)

Book 1 alt routing remains operational:

- **Low Corruption (≤ 2):** Routes to respectable "Slop Chapter I" (`day1_slop_chapter`).
- **High Corruption (> 2):** Routes to transgressive "Corrupted Alt Chapter I" (`day1_chapter`).

Commit `f337cbe` promotes the Book 1 MVP engine and vertical slice to `main-game/prod-game/`. Production now contains `day100.rpy` through `day105.rpy`. Non-prod remains the integration sandbox with richer systems not yet promoted.

### 5. Expanded QA and capture footprint (unchanged since June 20)

The playtest matrix holds 3 / 7 recorded captures:

- **P1 (corruption-forward):** Validated PASS. Completes to `day105_7_release_one_ending` with manuscript progress 5.
- **P2 (cautious path):** Recorded capture completed to MVP ending. Validation tool flags assertion mismatch (day `5` vs expected `105`).
- **P4 (deadline-1 fail):** Validated PASS. Hits `game_over_deadline_1` on Day 3 morning when Cora fails to write.

Unit tests increased to **67 passed**, covering balance profiles, scene direction, and resolver configurations.

### 6. Dynamic presentation enhancements (carried forward)

The main menu supports a dynamic carousel with multiple layout selections, atmospheric dust motes, and bottom-navigation overlay. Visual feel is substantially above gray-box prototype.

### 7. The project has a real dramatic and commercial identity

The strongest idea remains the separation between restrained hotel reality and Cora's hotter authored reconstruction. The Savoy is not merely scenery. It is a machine of rooms, keys, uniforms, permissions, gossip, and unequal credibility. Cora survives by observing that machine and converts its concealed appetites into prose.

The opening establishes the manuscript as bodily risk rather than optional lore: `day100_non_canon.rpy` begins with the pages hidden against Cora's body and ends with Holywell Street as payment, danger, and ambition. The closing returns to the manuscript after Gideon dismantles the fantasy that evidence alone creates power.

This loop is excellent:

1. Cora witnesses or causes danger.
2. The player chooses how she interprets it.
3. Stats and relationships record the cost.
4. The manuscript transforms the event into adult content and self-analysis.
5. The transformed material changes what kind of Cora reaches Day 105.

### 8. Day 105 understands the story's actual thesis

The photograph is not a magic victory token. Gideon's class protection means truth without rank is weak, and Cora must confront her own use of Missy as part of the same machine she condemns. The final manuscript section explicitly expands Gideon from singular monster into visible instrument of a larger structure.

### 9. State architecture is thoughtful

The current non-prod class layer provides:

- Central `TimeManager`, `PlayerStats`, and `StoryState` instances.
- Character-specific base and acute suspicion.
- Derived global anxiety.
- Whitelisted mutually exclusive story states.
- Setter-driven tracked flags.
- Named consequence windows.
- Dynamic optional-chain label resolution.
- Manuscript chapter completion and Release 1 completion state.
- Writing gates with explicit inspiration/corruption requirements.
- Semantic balance profiles via `apply_balanced_effect`.

### 10. Integration checklist milestones

Phases 4 (dynamic chains & penance), 5 (book writing system), and 6 (structural assets) are **100% complete** on the integration checklist. Phase 1 (writing gates) is at 89%. Overall checklist: **79 / 130 (60.8%)**.

## What Is Not Working

### 1. Route matrix incomplete and documentation stale

Progress since June 20 is real but stalled:

- **Captures on disk:** 3 / 7 (P1, P2, P4).
- **Integration checklist playtest sign-off:** 0 / 12.
- **`release1_route_matrix_results.md`:** Lists only P1 as PASS; does not reflect P2 or P4 captures that exist and pass structure checks.

Four central paths still need runtime capture:

- Low-corruption rejection (P3)
- Day 4 manuscript deadline failure (P5)
- Anxiety dismissal / game over (P6)
- Stern, Missy, and Vance confrontation/penance (P7)

### 2. P2 cautious path assertion mismatch (carried forward)

The cautious playtest capture `P2_cautious.jsonl` completes to `day105_7_release_one_ending`, but the comparison tool flags failure on `assert_reaches_day_at_least: 105`. Runtime stores day as `5` (Release 1 slot index from Day 100); the model target specifies `105`. This representation mismatch must be synchronized in assertion definitions or the comparison resolver.

### 3. The adult promise is visually underdelivered (carried forward)

The storyboard calls manuscript retellings the MVP's primary adult-game handshake. The manifest declares seven illustrations:

- `cg_manuscript_retelling_d1_corridor`
- `cg_manuscript_retelling_d2_lace`
- `cg_manuscript_retelling_d3_brush`
- `cg_manuscript_retelling_d4_false_dawn`
- `cg_book_d2_hatbox_tableau`
- `cg_gideon_photograph`
- `cg_photograph_burning`

All seven are absent from disk. The photograph `show` commands in Day 104/105 are commented out. Manuscript CG declarations exist in the manifest but are unused by active script scanning. The primary market hook is supported solely by text and NVL book layout.

### 4. Asset debt concentrated in UI plates and CG payoff

The cross-project reconciliation reports twelve missing assets:

- Five UI assets: `ui_book_blank`, `ui_book_plate_hatch_overlay`, `ui_book_plate_paper_overlay`, `ui_illustration_border_plate`, `ui_sidebar_bg`.
- Seven event illustrations listed above.

Additionally, prod and non-prod asset pools have diverged: prod holds 90 declared assets on disk; non-prod holds 47. Many Savoy backgrounds and cast sprites exist only in prod; non-prod has country-estate and partial Eleanor sprites prod lacks.

### 5. Fail-state wiring is static-only

Balance report confirms all four fail labels (`game_over_dismissed`, `game_over_deadline_1`, `game_over_deadline_2`, `bad_ending_rejection`) are defined and referenced. P4 proves deadline-1 at runtime. P5, P6, and P3 endings have abstract-simulator PASS but no JSONL evidence. Integration checklist Phase 2 remains at 2 / 8.

### 6. Day 103 Ch3 gate pattern inconsistency

`balance_report.py` warns that Day 103 Ch3 write does not use `has_story_fuel(*WRITE_GATE_CH3)` — it uses inline `player.inspiration` and `player.corruption_level` floor checks instead. Functionally equivalent but inconsistent with the established gate contract pattern.

### 7. Code hygiene and promotion prep lagging

Phase 7 of the integration checklist is 1 / 6:

- No recorded zero-error `renpy lint` on current non-prod tree (last lint report dated 2026-06-19).
- README and public-facing metadata still stale.
- `classes_non_canon.rpy` header comment still says "NOT loaded" despite Ren'Py loading all `.rpy` under `game/`.
- Dev debris in `images/` (`rembg.bat`, scratch PNGs) not gitignored.
- `storyboard_sync` not run after recent mechanics land.

### 8. Standup automation reports stale blockers

The June 28 standup still flags a compile error at `day100_non_canon.rpy:141` (ATL statement). Fresh `log.txt` from 2026-06-28 shows a clean Ren'Py load with no traceback. The standup script appears to be reading stale error artifacts rather than current compile state. This undermines automated health grading (Chief Architect: D).

### 9. Audio integration remains thin outside prologue and book1

All 21 audio aliases resolve in non-prod, and guarded plays exist in Day 100 and `book1_write_chapter`. Main day scripts (101–105) do not yet establish a consistent ambience/theme/SFX layer across the hotel spine. The Savoy still needs auditory class texture in active scenes, not merely files in a folder.

## Market Viability

**Current market viability: B+**

**Potential after a focused ship pass: A-**

The project has a stronger niche proposition than most early adult VN builds. It is not selling generic Victorian decadence. It is selling authorship as transgression:

> A precarious Irish chambermaid steals knowledge from a luxury hotel's private rooms and turns class violence, appetite, and betrayal into a forbidden book.

That pitch supports multiple desirable audience hooks: maid/service hierarchy, dominant aristocratic male pressure, female intimacy based on earned trust, mature authority in Stern, and writing as erotic transformation.

The narrative pressure system strengthens commercial onboarding — players now receive explicit manuscript-readiness feedback rather than guessing at gate math.

The market danger remains unchanged: the build looks evasive because the visual payoff is absent. The MVP needs an unmistakable manuscript payoff in its first substantial session. Delivering the manuscript layer visually while preserving the hotel's restraint is key.

## Required to Ship the MVP

### P0 — Hard blockers

1. **Complete and record runtime QA.**
   - Capture remaining paths P3, P5, P6, and P7.
   - Sync `release1_route_matrix_results.md` to reflect the 3 / 7 captures already on disk (P1, P2, P4).
   - Fix the P2 `assert_reaches_day_at_least` day-number format difference.

2. **Close main-route visual gaps.**
   - Deliver the five remaining UI book-plate assets and reconcile manifest/path mismatches.
   - Deliver at least two manuscript payoff CGs, including one early.
   - Uncomment and wire `show` commands in Day 104/105 when photograph CGs land.

3. **Create a clean distribution profile.**
   - Exclude ActionEditor, test harnesses, debug capture overlay, saves, cache, `.rpyc`, logs, editor libraries, and helper scripts from the public package.

4. **Reconcile prod/non-prod asset pools.**
   - Decide which engine is the ship candidate and align backgrounds/sprites so the playable build does not depend on cross-tree fallbacks.

### P1 — Required quality

5. **Integrate a minimum sound pass across Days 101–105.**
   - Writing theme, hotel/corridor ambience, Master Suite pressure theme, and basic SFX (key, door, floorboard).

6. **Normalize Day 103 Ch3 gate to `has_story_fuel(*WRITE_GATE_CH3)`.**
   - Close the balance-report WARN and keep gate patterns consistent.

7. **Update player-facing documentation and metadata.**
   - Correct project structure and day count in the README. Set an honest MVP version.

8. **Finish fail-state playtest verification.**
   - Close Phase 2 checklist items with P3, P5, P6 runtime evidence.

9. **Run fresh `renpy lint` and close Phase 7 hygiene items.**
   - Record zero-error lint. Remove dev debris. Fix stale class header comment.

10. **Repair standup error detection.**
    - Ensure automated health reports read current compile state, not stale traceback files.

## Recommended Ship Sequence

1. Sync `release1_route_matrix_results.md` with existing P1/P2/P4 captures; fix P2 day-index assertion.
2. Run remaining route captures (P5 next, then P3/P6/P7) and fix runtime blockers.
3. Close core UI book-plate assets and manifest/path mismatches.
4. Add the early and late manuscript CG payoffs; wire `show` commands.
5. Reconcile prod/non-prod asset pools for the chosen ship candidate.
6. Add the minimum soundscape across the day spine.
7. Run fresh `renpy lint`; remove or restyle debug-facing menu language.
8. Package a clean candidate and test on a clean machine/profile.

## Action Items by Reviewer Category

### Ship

- Core premise and Day 100–105 spine
- Cora's morally dangerous authorship
- Character-specific suspicion/anxiety model
- Missy trust consequences and optional chains
- Book 1 alt paths and exported writing engine
- Dynamic main menu layout, carousel, and dust motes
- Narrative pressure HUD, objective journal, and notification bundles
- Full repository validation passing

### Rewrite / Fix

- Stale README and public-facing descriptions
- `compare_runtime_to_model.py` cautious day comparison assertion
- `release1_route_matrix_results.md` sync with on-disk captures
- Menu captions that expose internal spice labels as final copy
- Day 102 prose formatting repair
- Day 103 Ch3 gate to use `has_story_fuel(*WRITE_GATE_CH3)`

### Escalate

- Early manuscript visual payoff
- Audio use and environmental texture across Days 101–105
- Remaining route-matrix captures (P3, P5, P6, P7)
- Prod/non-prod asset pool reconciliation
- Standup automation stale-error detection

### Cut or exclude from distribution

- ActionEditor runtime content and test harness labels
- Debug capture overlay (`debug_run_capture.rpy`, F10 matrix buttons)
- saves/cache/compiled/log/editor artifacts
- Unused manifest promises that will not be delivered for MVP

## Final Promotion Verdict

**DO NOT PROMOTE**

The narrative and system design are strong enough to become the MVP; the current build is not yet a trustworthy or market-complete release candidate. Significant structural progress has been made since June 21: validation is green, compliance debt is cleared, narrative pressure and balance systems are integrated, and Book 1 is promoted to prod. However, promotion should resume only after the route matrix is complete and documented, the manuscript's visual payoff is physically present, prod/non-prod assets are reconciled, and a clean distribution candidate passes lint and manual QA on a fresh profile.
