# Release 1 MVP Full Review

Date: 2026-06-21

Requested lenses:

- Chief Architect: runtime structure, state discipline, validation, assets, packaging, and promotion readiness.
- Adult Market Reviewer: adult-VN promise, tension, payoff cadence, fetish clarity, and commercial presentation.
- Lead Narrative Editor: story architecture, character voice, continuity, choice meaning, and thematic resolution.

## Scope and Method

The path named in the request, `narrative/draft/releases/release-1-mvp/non_prod_renpy_project`, no longer exists. Repository documentation identifies `main-game/non-prod-game/` as the current equivalent and active non-production Ren'Py project. This review is therefore based on:

- `main-game/non-prod-game/`
- Direct Release 1 support files in `main-game/draft/releases/planning/`
- Release 1 graph, grain, balance, and QA artifacts in `main-game/pipeline/releases/release-1-mvp/`
- Canon and voice files directly required to judge the scripts

Production files were not used to give the non-production build credit. Backlog ideas were not counted as implemented features.

Evidence gathered:

- Fresh `scripts/validate.py --profile full` run
- Fresh scoped `scripts/validate.py --profile changed` run against non-prod Day 100–105 scripts
- Fresh `scripts/contract_validate.py` run for Day 100 through Day 105
- Fresh repository unit-test run: **61 tests passed** (up from 31 tests yesterday!)
- Fresh asset-manifest audit via `scripts/daily_asset_manifest.py`
- Review of `release1_route_matrix_results.md`, `runtime_model_comparison.md`, and captures `P1_corruption_forward.jsonl`, `P2_cautious.jsonl`, and `P4_deadline_1.jsonl`
- Static inspection of all source `.rpy` files in the non-production game, excluding bundled ActionEditor internals from narrative grading
- Review of current `log.txt` and `traceback.txt`
- Review of the Release 1 graph audit/gaps, grain gaps, integration checklist, and June 21 standup report

No complete human-equivalent manual playthrough of all required paths was performed as part of this static review. Three runtime captures now exist on disk (P1 corruption-forward, P2 cautious, and P4 deadline-1 fail). The remaining four matrix paths are still unrecorded.

## Executive Verdict

The project continues to resolve structural milestones, but a set of compliance violations in the latest menu features and linter false positives block clean validation.

**Overall project grade: B**

**Current public-build readiness: C+**

**MVP promotion verdict: DO NOT PROMOTE**

Since the June 20 review, the team has expanded testing coverage (unit tests doubled to 61 passed) and added key presentation and narrative systems. We now have three recorded playtest captures: P1 (corruption-forward) and P4 (deadline-1 game over) are validated as PASS, proving that the Day 3 deadline hard-fail system works. P2 (cautious path) successfully completes to the ending, though it flags a false failure in the comparison script due to a day-number indexing mismatch (expecting 105 but receiving 5). Additionally, the main menu has been enhanced with a premium carousel layout, dust motes particle effects, and bottom-navigation, and the Book 1 alt writing paths are fully integrated and documented for LLM export.

What prevents promotion is a mix of new compliance debt and legacy linter limitations:
1. **New Compliance Violations:** The new `menu_carousel.rpy` file contains three `default` variable declarations outside of `variables.rpy` (including a global default `game_menu_background_slide = None` at line 14). This violates the centralization requirement and fails the engineering compliance check.
2. **Screen Linter False Positives:** The addition of `menu_carousel.rpy` has exacerbated Ren'Py contract linter issues, generating dozens of false positives for screen-language statements (like `add`, `style_prefix`, `on`, `text`, etc.) being flagged as undefined dialogue speakers.
3. **Missing Assets:** Eleven assets (5 UI elements and 6 central story CGs) remain missing from disk.
4. **Remaining Captures:** Four of the seven playtest matrix paths (P3, P5, P6, P7) are still pending capture.

Promotion should resume only after the `menu_carousel.rpy` compliance issues are addressed, the linter is configured to bypass screen language, and remaining playtest paths are recorded.

## Grade Summary

| Element | Grade | Assessment |
|---|---:|---|
| Core premise and differentiation | A | A covert Irish maid turning class danger and private scandal into forbidden fiction is clear, specific, and marketable. |
| Cora's character architecture | A- | Her survival mask, Irish concealment, authorial hunger, and moral danger form a strong protagonist engine. |
| Five-day narrative spine | B+ | Escalation is coherent from exposure risk to attempted leverage to structural defeat and artistic diagnosis. |
| Ending and thematic resolution | A- | Day 105 closes the release thematically without pretending Cora can defeat class power with one photograph. |
| Supporting cast | B+ | Gideon, Stern, Missy, and Vance each embody a distinct pressure system rather than functioning as route furniture. |
| Character voice and canon alignment | B+ | All six day packages have valid narrative, psychology, and Victorian gate contracts; Day 102 prose formatting repair is still pending. |
| Choice design and branch memory | B+ | Choices alter state, relationships, manuscript framing, and consequences. P1, P2, and P4 captures are recorded, though P2 highlights a tool index mismatch. |
| Adult-market concept | A- | The kink ecology—service, surveillance, class authority, forbidden authorship, betrayal, and controlled submission—is unusually coherent. |
| Adult payoff delivery | B- | The prose has heat, but the promised visual manuscript payoff is largely absent. The game currently sells a stronger concept than build. |
| Manuscript writing system | B+ | Alt paths for Book 1 are implemented and documented; Sweeney Todd / Dracula transpositions render correctly on the NVL screens. |
| State architecture | B+ | Central classes, setter-driven flags, whitelisted states, targeted suspicion, anxiety, and named consequence windows are strong prototype architecture. |
| Code quality and maintainability | B- | Validation is blocked because the contract linter mistakes screen-language keywords for speakers, and `menu_carousel.rpy` introduces non-compliant defaults outside `variables.rpy`. |
| UI/UX and game feel | B- | Upgraded from C+. HUD, ledger, thought presentation, and book layout are reinforced by a dynamic menu carousel, dust motes, and bottom-navigation overlays. |
| Visual asset readiness | C | Runtime backgrounds and sprites are covered through the configured search pool. Five UI assets and all six CGs remain missing. |
| Audio readiness | C- | All 21 aliases resolve to physical source files in the non-prod pool, but active integration remains extremely thin and preview-track licensing still needs release treatment. |
| Testing and QA evidence | B- | Upgraded from C. Unit tests increased to 61 passed, and we now have three recorded captures (P1, P2, P4) on disk, though four matrix paths remain pending. |
| Documentation and pipeline discipline | B- | Gates and handoffs are strong. Book writing engine export is fully documented with integration and syntax validation guides. Checklist and matrix sync still pending. |
| Packaging/release professionalism | D+ | Placeholder name/version, ActionEditor and test harness content, compiled artifacts, saves, cache, logs, and helper scripts require a deliberate build profile. |

## What Is Working

### 1. Dynamic Presentation Enhancements (New since June 20)
Commit `311bc30` introduces major frontend polish to the non-production build. The main menu now supports a dynamic carousel with multiple layout selections, atmospheric dust motes particle effects, and an elegant bottom-navigation menu overlay. These additions substantially elevate the project's visual feel toward premium standards.

### 2. Book 1 Alt Paths and Engine Export (New since June 20)
Commit `c83a78c` completes the integration of Book 1 alt paths. Cora's manuscript now branches dynamically based on her stats:
- **Low Corruption ($\le 2$):** Routes to the respectable, generic "Slop Chapter I" (`day1_slop_chapter`).
- **High Corruption ($> 2$):** Routes to the transgressive, high-tension "Corrupted Alt Chapter I" (`day1_chapter`), utilizing transpositions of Sweeney Todd and Dracula themes.
The entire book writing engine has been packaged and documented (`docs/book-writing-engine-export/`) for external LLM parsing, including syntax validation and flag-wiring manuals.

### 3. Expanded QA and Capture Footprint (New since June 20)
The playtest matrix has expanded from 1 to 3 recorded captures on disk:
- **P1 (corruption-forward):** Validated PASS. Completes to `day105_7_release_one_ending` with manuscript progress 5.
- **P2 (cautious path):** Recorded capture completed. Verifies structural navigation to the ending, though the validation tool currently flags an assertion mismatch due to day representation (day 5 vs day 105).
- **P4 (deadline-1 fail):** Validated PASS. Successfully hits `game_over_deadline_1` on Day 3 morning when Cora fails to write, proving the deadline hard-fail logic functions correctly in runtime.
Additionally, the repository unit-test suite has doubled to **61 passed tests**, validating balance profiles, scene direction, and resolver configurations.

### 4. The project has a real dramatic and commercial identity
The strongest idea remains the separation between restrained hotel reality and Cora's hotter authored reconstruction. The Savoy is not merely scenery. It is a machine of rooms, keys, uniforms, permissions, gossip, and unequal credibility. Cora survives by observing that machine and converts its concealed appetites into prose.

The opening establishes the manuscript as bodily risk rather than optional lore: `day100_non_canon.rpy` begins with the pages hidden against Cora's body and ends with Holywell Street as payment, danger, and ambition. The closing returns to the manuscript after Gideon dismantles the fantasy that evidence alone creates power.

This loop is excellent:
1. Cora witnesses or causes danger.
2. The player chooses how she interprets it.
3. Stats and relationships record the cost.
4. The manuscript transforms the event into adult content and self-analysis.
5. The transformed material changes what kind of Cora reaches Day 105.

### 5. Day 105 understands the story's actual thesis
The photograph is not a magic victory token. Gideon's class protection means truth without rank is weak, and Cora must confront her own use of Missy as part of the same machine she condemns. The final manuscript section explicitly expands Gideon from singular monster into visible instrument of a larger structure.

The ending also preserves forward momentum:
- Cora completes the Release 1 manuscript.
- Gideon leaves but marks her as future interest.
- Vance remains bound to him.
- Missy's final physical position changes according to trust damage.
- Money and entanglement choices carry forward.

### 6. State architecture is thoughtful
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

## What Is Not Working

### 1. New Engineering Compliance Violations (New since June 20)
The introduction of `menu_carousel.rpy` violates centralized variable discipline:
- `menu_carousel.rpy:14` contains `default game_menu_background_slide = None`, introducing a saving global default outside of `variables.rpy`.
- `menu_carousel.rpy:294` and `:484` define screen-local defaults (`default page_name_value = ...` and `default device = "keyboard"`), which are valid in Ren'Py screen syntax but trigger regex violations in `scripts/engineering_compliance.py`.
Central variables must be migrated, and the compliance script needs to differentiate between global and screen-local defaults.

### 2. Expanded Screen-Language Linter Failures (New since June 20)
Because `menu_carousel.rpy` is heavily screen-based, `renpy_contract_linter.py` attempts to parse it as dialogue script. This generates dozens of false-positive warnings, flagging standard layout commands (such as `add`, `style_prefix`, `on`, `text`, `scrollbars`, `key`, `textbutton`, `size_group`, `background`, `layout`, and `foreground`) as undefined characters, and builtin/standard Python calls (such as `or`, `CurrentScreenName`, and `GamepadExists`) as unresolved callables. The linter must be updated to ignore screen language files or properly parse them.

### 3. Assertion Mismatch on P2 Cautious Path (New since June 20)
The cautious playtest capture `P2_cautious.jsonl` completes the run, but the comparison tool flags a failure on the assertion `assert_reaches_day_at_least: 105`. The runtime saves the day stat as `5` (0-5 indexing from Day 100), while the model target specifies `105`. This representation mismatch needs to be synchronized in the assertion definitions or the comparison resolver.

### 4. The route matrix is started but far from complete
Progress since June 20 is real (matrix captures are at 3 / 7), but the integration checklist playtest sign-off remains at 0 / 12, and four central paths are still pending runtime capture:
- Low-corruption rejection (P3)
- Day 4 manuscript deadline failure (P5)
- Anxiety dismissal / game over (P6)
- Stern, Missy, and Vance confrontation/penance (P7)

### 5. The adult promise is visually underdelivered
The storyboard calls manuscript retellings the MVP's primary adult-game handshake. The manifest declares six illustrations:
- `cg_manuscript_retelling_d1_corridor`
- `cg_manuscript_retelling_d2_lace`
- `cg_manuscript_retelling_d3_brush`
- `cg_manuscript_retelling_d4_false_dawn`
- `cg_gideon_photograph`
- `cg_photograph_burning`

All six are absent from disk. The photograph show commands in Day 104/105 are commented out. The manuscript CG declarations are unused by active script scanning. The Book 1 system falls back to missing UI skins, meaning the primary market hook is supported solely by text.

### 6. Asset debt is still concentrated in UI and CG payoff
The cross-project reconciliation reports eleven missing assets:
- Five UI assets: book UI background, illustration border, price badge, sidebar background, and sidebar divider.
- Six event illustrations listed above.

### 7. Audio is barely integrated
The main day scripts do not yet establish a consistent ambience/theme/SFX layer. Phase 6 audio tasks in the integration checklist remain largely unchecked. The Savoy still requires auditory class texture—bells, doors, footsteps, laundry, muted rooms, writing sounds—not merely files sitting in a folder.

## Market Viability

**Current market viability: B+**

**Potential after a focused ship pass: A-**

The project has a stronger niche proposition than most early adult VN builds. It is not selling generic Victorian decadence. It is selling authorship as transgression:

> A precarious Irish chambermaid steals knowledge from a luxury hotel's private rooms and turns class violence, appetite, and betrayal into a forbidden book.

That pitch supports multiple desirable audience hooks: maid/service hierarchy, dominant aristocratic male pressure, female intimacy based on earned trust, mature authority in Stern, and writing as erotic transformation.

The market danger is that the build looks evasive because the visual payoff is absent. The MVP needs an unmistakable manuscript payoff in its first substantial session. Delivering the manuscript layer visually and preserving the hotel's restraint is key.

## Required to Ship the MVP

### P0 — Hard blockers

1. **Resolve compliance violations in `menu_carousel.rpy`.**
   - Centralize global `default game_menu_background_slide` variables to `variables.rpy`.
   - Update `engineering_compliance.py` to ignore screen-local defaults inside `screen` definitions.

2. **Make the full validation command reliable and green.**
   - Stop the contract linter from treating screen-language keywords as dialogue speakers.
   - Address unresolved callables (`getattr`, `or`, `CurrentScreenName`, `GamepadExists`) in screen files.

3. **Complete and record runtime QA.**
   - Capture remaining paths P3, P5, P6, and P7.
   - Sync the playtest matrix and integration checklist to reflect the 3 / 7 recorded captures.
   - Fix the P2 assertion day-number format difference.

4. **Close main-route visual gaps.**
   - Deliver the five remaining UI assets and reconcile manifest/path mismatches.
   - Deliver at least two manuscript payoff CGs, including one early.

5. **Create a clean distribution profile.**
   - Exclude ActionEditor, tests, saves, cache, `.rpyc`, logs, editor libraries, and helper scripts from the public package.

### P1 — Required quality

6. **Integrate a minimum sound pass.**
   - Writing theme, hotel/corridor ambience, Master Suite pressure theme, and basic SFX (key, door, floorboard).

7. **Clarify the writing feature.**
   - Rename it as a manuscript sequence unless meaningful in-sequence choices are added.

8. **Update player-facing documentation and metadata.**
   - Correct project structure and day count in the README. Set an honest MVP version.

9. **Finish fail-state wiring and verify with captures.**
   - Close Phase 2 checklist items and record P5–P6 runtime evidence.

## Recommended Ship Sequence

1. Centralize the `menu_carousel.rpy` global variables to `variables.rpy` and address engineering compliance.
2. Fix screen-language linting and obtain a clean engine-lint record.
3. Sync checklist/route matrix/standup reporting.
4. Run remaining route captures (P5 next, then P3/P6/P7) and fix runtime blockers.
5. Close core UI assets and manifest/path mismatches.
6. Add the early and late manuscript CG payoffs.
7. Add the minimum soundscape.
8. Remove or restyle debug-facing menu language.
9. Package a clean candidate and test on a clean machine/profile.

## Action Items by Reviewer Category

### Ship
- Core premise and Day 100–105 spine
- Cora's morally dangerous authorship
- Character-specific suspicion/anxiety model
- Missy trust consequences and optional chains
- Book 1 Alt Paths and exported writing engine
- Dynamic main menu layout, carousel, and dust motes

### Rewrite / Fix
- Stale README and public-facing descriptions
- `menu_carousel.rpy` non-compliant default declarations
- `compare_runtime_to_model.py` cautious day comparison assertion
- Menu captions that expose internal spice labels as final copy
- Day 102 prose formatting repair

### Escalate
- Early manuscript visual payoff
- Audio use and environmental texture
- Remaining route-matrix captures (P3, P5, P6, P7)
- Syncing checklist playtest matrix with captured JSONL files

### Cut or exclude from distribution
- ActionEditor runtime content and test harness labels
- saves/cache/compiled/log/editor artifacts
- Unused manifest promises that will not be delivered for MVP

## Final Promotion Verdict

**DO NOT PROMOTE**

The narrative and system design are strong enough to become the MVP; the current build is not yet a trustworthy or market-complete release candidate. Significant structural progress has been made with the integration of Book 1 alt paths and the addition of playtest captures P2 and P4. However, promotion should resume only after the `menu_carousel.rpy` compliance issues are fixed, the linter false positives are resolved, the remaining route matrix is recorded, and the manuscript's visual payoff is physically present.
