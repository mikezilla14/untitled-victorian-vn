# Release 1 MVP Full Review

Date: 2026-06-13

Scope: This audit is based only on the current non-production game in `main-game/non-prod-game` and directly associated Release 1 planning, graph, gate, and draft-bible files.

Review lenses applied:
- Chief Architect: runtime structure, state contract, validation, assets, promotion readiness.
- Adult Market Reviewer: adult VN market promise, tension loop, pacing, fetish/choice clarity.
- Lead Narrative Editor: story architecture, voice/canon alignment, continuity, player-facing payoff.

## Executive Verdict

The MVP is close in content shape, but not yet ship-ready.

Overall grade: **B-**

The game now has a real spine, real state architecture, real choice consequences, a coherent five-day arc, and a distinctive adult-game thesis: Cora converts danger, class pressure, shame, appetite, and observation into forbidden manuscript chapters. That is the project. It is strong, unusual, and marketable.

The reason it is not yet an A-level MVP is production proof. Validation currently fails. Asset drift is large. Scene direction and formatting checks are out of date. Branch smoke testing is not evidenced. Several declared CG/audio payoffs are not physically present or not actively shown. The story and mechanics have reached "playable design complete"; the build has not yet reached "player-trust complete."

## Grade Summary

| Element | Grade | Rationale |
|---|---:|---|
| Core premise and hook | A- | Victorian class pressure plus erotic manuscript authorship is clear, specific, and differentiated. |
| Narrative spine | B+ | Day 100-105 arc is coherent, escalates well, and lands on a strong "diagnosis, not victory" ending. |
| Cora character arc | A- | Cora's movement from performed maid to diagnostic author is the MVP's strongest emotional throughline. |
| Gideon/Vance/Stern/Missy dynamics | B+ | Each secondary axis has a clear use, though some optional content risks over-weighting side chains before main proof is playtested. |
| Adult market viability | B+ | The premise is very viable, but visible CG/explicit payoff support is not yet strong enough for a high-confidence F95-style release. |
| Erotic tension and spice delivery | B | The text has heat and consequence. It still leans literary/analytical more than immediately visual or reward-forward. |
| Manuscript retelling mechanic | B+ | Structurally excellent and narratively distinctive; needs visual/UI proof and stronger player-facing presentation. |
| Choice consequence design | B | Branch flags and stat gates are good. Needs full route smoke tests and balancing proof. |
| State architecture | B+ | Setter-driven `StoryState`, targeted suspicion, anxiety, and writing gates are strong. One deprecated `susp=` call remains. |
| UI and game feel | C+ | Sidebar/ledger/NVL systems exist, but asset fallbacks and missing art prevent polished feel. |
| Asset readiness | D+ | The largest ship blocker. Validation reports 55 missing declared images and 19 missing declared audios in the scoped run. Standup reports 42 missing assets. Either way, this is not release-clean. |
| Validation and promotion readiness | C | Writer-room contracts pass, but validation fails on scene direction and non-canon formatting; Ren'Py contract lint was skipped for scoped non-prod scripts. |
| Documentation/planning discipline | B+ | Storyboard, graph audit, gates, and standups are useful and mostly current; graph gaps remain. |
| MVP ship readiness | C+ | Content is substantially there. Release discipline, assets, branch testing, and final integration are not. |

## What Is Working

### 1. The project finally has a playable dramatic identity

The MVP is no longer a generic historical VN with adult content. It has a specific engine:

Cora experiences constrained, dangerous, class-bound hotel events, then rewrites them into a forbidden manuscript where the adult payoff and psychological self-diagnosis happen.

That structure is explicitly documented in `planning/story_board.md` under "Adult Payoff Structure: Manuscript Retelling Minigame" and implemented through `book1_non_canon.rpy`. The Book 1 chapter map includes day-specific manuscript chapters (`day1_chapter`, `day2_chapter`, `day3_chapter`, `day4_triumphant_chapter`, `day5_reckoning_chapter`) and routes them through `book1_write_chapter`.

This is the best market asset the game has. It gives the restrained hotel scenes permission to stay socially plausible while still promising adult VN payoff.

### 2. Cora's arc lands

The Day 105 manuscript reckoning works because it denies the cheap victory. The photograph does not defeat the class machine. Gideon is not simply "beaten." Cora's book becomes a tool for understanding power, hunger, witnessing, and complicity.

Strong examples:
- `day105_6_manuscript_reckoning` branches Cora's final interpretation by `day5_dynamic`.
- `day105_5_gideon_marks_cora` gives Gideon the strong thesis line: Cora is "interesting," not powerful.
- The final chapter sets `release1_manuscript_completed` and `release1_completed`, then calls `book1_write_chapter(chapter_key="day5_reckoning_chapter", current_day=105)`.

This is more mature than a normal demo cliffhanger. It gives Release 1 a thematic close while preserving forward pressure for Release 2.

### 3. The state model is much healthier than typical prototype state

The non-prod shared class layer is a real design:
- `PlayerStats` separates base suspicion from acute suspicion.
- Anxiety is derived from per-character suspicion using independent probability.
- `StoryState` uses whitelisted string states and boolean setters.
- Optional chains use `story.resolve_chain_label(character)` and named dynamic windows rather than ad hoc route sprawl.
- Writing gates use AND semantics via `has_story_fuel(*WRITE_GATE_CHx)`.

This is architecturally promising. It gives the team a way to tune relationship danger, manuscript progress, corruption, and fail states without replacing the story.

### 4. The optional chains are meaningful rather than decorative

Stern, Missy, and Vance optional chains are not generic affection points. They create different flavors of pressure:
- Stern: discipline, exposure, procedural domination.
- Missy: intimacy, betrayal, repair, romantic trust.
- Vance: class voyeurism, humiliation, dangerous frivolity.

The graph audit found 9 chain labels and 33 menus across the release. The optional chain system is real enough to be a selling feature if it is tested and presented clearly.

### 5. The writing gates and fail-state concept are right

The game correctly understands that "adult content as reward" is not enough. The manuscript should be a deadline, a hunger meter, and a moral record.

Implemented examples:
- Day 101 write option is gated by `has_story_fuel(*WRITE_GATE_CH1)`.
- Day 103 checks `story.manuscript_progress == 0` and jumps to `game_over_deadline_1`.
- Day 104 false-dawn path checks `story.manuscript_progress < 2` and can jump to `game_over_deadline_2`.
- Day 105 checks corruption before final reckoning and can jump to `bad_ending_rejection`.

This is the right MVP shape. It needs proof, not reinvention.

## What Is Not Working

### 1. The build is not validation-clean

The scoped validation run failed.

Important results:
- Domain gatekeeper passed.
- Engineering compliance passed.
- Asset references in active scripts are declared in manifest.
- Historical lint passed for Day 100-105, Book 1, story chains, classes, and functions.
- Writer-room pipeline contracts passed for Day 100, 101, 102, 103, 104, and 105.
- Validation failed on scene direction check.
- Validation failed on non-canon formatting check.

Concrete validation failure:
- Scene direction out of date: `day103_non_canon.rpy`, `day104_non_canon.rpy`.
- The formatter reported 1 file would change: `day103_non_canon.rpy`.

Ship impact: **blocking**. This cannot be considered release-clean while validation fails.

### 2. Asset drift is the biggest production blocker

The current daily standup reports 42 declared assets missing from non-prod disk. The direct validation run against the scoped non-prod set reported an even larger mismatch: 55 missing declared images and 19 missing declared audios.

Even allowing for tooling path-extension disagreement, the conclusion is the same: the asset layer is not ship-ready.

High-impact missing or weakly supported areas:
- Key backgrounds such as `bg_master_suite_night`, `bg_country_estate_corridor_night`, `bg_train_carriage_day`, and multiple servant/hotel rooms.
- Book-writing UI assets such as `ui_book_writing_paper`, `ui_book_cover`, `ui_book_ui_bg`, `ui_price_badge`.
- Manuscript retelling CGs: `cg_manuscript_retelling_d1_corridor`, `cg_manuscript_retelling_d2_lace`, `cg_manuscript_retelling_d3_brush`, `cg_manuscript_retelling_d4_false_dawn`.
- Photograph CGs: `cg_gideon_photograph`, `cg_photograph_burning`.
- Audio aliases are declared but not referenced in active game scripts, and validation reports 19 missing physical audios.

Ship impact: **blocking for a public demo**, especially for an adult VN. Fallback solids prevent crashes, but they do not sell the fantasy.

### 3. The CG promise is not player-facing enough yet

The storyboard promises manuscript retelling CGs as the MVP's adult-game handshake. The manifest declares them. But actual script usage is weak:
- `cg_gideon_photograph` and `cg_photograph_burning` are commented out in Day 104/105.
- `cg_manuscript_retelling_*` images are declared but not actively shown by day scripts.
- The NVL writing screen uses `book1_page_image` fallback behavior, but the review did not find reliable state assignment that maps each chapter route to a specific CG in the player path.

Market impact: **major**. The prose can carry tension, but an F95-style audience will expect the adult premise to become visible early. If the first release relies mostly on text and placeholder/fallback visuals, the demo will be judged as more literary prototype than adult VN.

### 4. One deprecated runtime effect remains in Day 102

`day102_4_cora_sneaks_a_feel` calls:

`$ apply_effects(susp=10, insp=5, corr=15)`

But `functions_non_canon.rpy` explicitly raises `ValueError` when generic `susp` is used. Suspicion must be assigned to a specific witness (`stern_susp`, `vance_susp`, `missy_susp`, `gideon_susp`).

Ship impact: **blocking if reachable**. This is a runtime crash in the indulgence path unless changed to a character-specific suspicion field.

### 5. The writing/minigame terminology overpromises interactivity

The "manuscript retelling minigame" is currently more of a state-aware NVL writing presentation than a minigame. That is not automatically bad. The problem is expectation management.

What exists:
- Route-aware chapter text.
- NVL rendering override.
- Chapter completion tracking.
- Debug harness labels.

What is not yet clear:
- Whether the player makes active choices inside the writing UI.
- Whether chapter images change visibly by route.
- Whether writing feels like a mechanic rather than a cutscene reward.

Ship impact: **medium to high**. The system can ship as "manuscript scenes" or "writing sequences." If marketed or framed as a minigame, it needs more visible interaction.

### 6. Branch completeness needs proof, not confidence

The graph audit is encouraging:
- 169 labels.
- 33 menus.
- 97 branches extracted.
- 92 parsed `apply_effects` calls.
- 13 gates.
- No ambiguous choice groups.
- No missing or incomplete `apply_effects`.
- No gate pass/fail ambiguity.
- No penance/opportunity-cost gaps.

But the same audit still records:
- 13 missing DAG gate tags.
- 11 dynamic jump targets.
- 9 optional chain window metadata gaps.
- 13 router outcome mismatches.
- 32 storyboard drift notes.

The audit says "Ready for first balancing spreadsheet skeleton." That is not the same as "Ready to ship."

Ship impact: **medium**. The structure is probably sound, but main-route and branch-route smoke tests are still required.

### 7. Dev debris and tool artifacts are still in the non-prod project

The non-prod project includes development/test/editor material:
- `test_day2_writing_non_canon.rpy`
- `AEditor/`
- backup-like files with suffixes such as `~` and `_`
- `git_status.txt`
- `resize_backgrounds.py`
- image source/input folders and utility batch files

Some of this may be acceptable in a sandbox, but it is not acceptable in a cleaned MVP package without an explicit packaging rule.

Ship impact: **medium**. It will not necessarily break the game, but it will make the project look rough and can create accidental labels/assets in Ren'Py.

## Market Viability

Market viability grade: **B+ now, A- possible after asset and payoff pass**

This is marketable because it has a clear kink ecology rather than isolated spicy scenes:
- Class power.
- Service hierarchy.
- Surveillance.
- Forbidden authorship.
- Shame transformed into craft.
- Optional betrayal/repair.
- A powerful male antagonist/patron who recognizes Cora without granting her power.

The strongest market hook is not "Victorian maid sees scandal." It is:

**A chambermaid survives a class machine by turning its private cruelties into a forbidden penny dreadful, and the player's choices decide whether her authorial voice becomes witness, predator, prey, or accomplice.**

That is a good hook. It is sharper than the average adult VN premise.

The current risk is that the game may read too restrained too long if players do not see a visible erotic manuscript payoff by Day 101/102. The prose is often excellent, but the target market will not grade restraint generously unless it is clearly building toward visible reward.

## Tone And Tension Breakdown

### What works

The best writing understands that erotic tension here is not just bodies. It is permission, class, surveillance, and private authorship.

Examples:
- Day 101 writing sequence lets Cora process voyeurism as structure, appetite, or distance.
- Day 102 indulgence scene turns the contraband into private bodily scandal.
- Day 104 triumphant chapter is hot because it is false victory: Cora mistakes fiction for leverage.
- Day 105 final reckoning correctly reframes the book as diagnosis instead of simple empowerment fantasy.

### What needs escalation

The manuscript layer should become more visibly hotter than the hotel layer. Right now it is often thematically hotter, but not always visually or interactively hotter.

Recommended escalation:
- Make the first manuscript writing scene an unmistakable adult payoff beat by Day 101 or Day 102.
- Ensure at least one manuscript CG or edited illustration appears in the first 30-45 minutes.
- Make route flavor visible in the writing UI, not only in prose.
- Add a clear "this is Cora's authored fantasy" visual language, so the game can be restrained in reality and bolder on the page.

Do not solve this by making the literal hotel scenes bluntly explicit. The project's better answer is to make the manuscript scenes more seductive, theatrical, and visibly different.

## Narrative Review

Narrative grade: **B+**

The story spine is coherent:
- Day 100: arrival, secret manuscript, motive.
- Day 101: first hotel contact, corridor identity, first writing pressure.
- Day 102: contraband scandal and tea-room crisis.
- Day 103: Gideon test, Stern suspicion, ultimatum, writing pressure.
- Day 104: lockbox, photograph, escape, false dawn.
- Day 105: leverage collapse, Cora's motive named, manuscript reckoning, Release 2 seed.

The best thing in the current story is that Cora does not "win" by producing evidence. She learns that evidence needs a listener with power. That is exactly the right Victorian/class thesis for this game.

Voice/canon status is encouraging:
- Historical lint passed across the scoped narrative files.
- Day 100-105 writer-room pipelines all have reports/specs/gates.
- Day 105 contract validation passes all three gates and promotion handoff.

Narrative risks:
- Missy scenes can become emotionally stronger than the main Gideon/manuscript line if optional content is too available or too rewarding.
- Some book prose is highly analytical. Strong for theme, but the adult audience may need more sensory immediacy.
- Day 105's thematic close is strong, but it should not feel like the player has been denied payoff. That makes the earlier manuscript payoff even more important.

## Architecture Review

Architecture grade: **B**

Strengths:
- Central state objects are the right direction.
- String states are whitelisted.
- Boolean flags are setter-driven.
- Suspicion is character-specific and better modeled than a single heat bar.
- Anxiety as derived compound risk is elegant and thematically appropriate.
- Dynamic windows and chain labels are a good compromise between VN spine and optional content.

Weaknesses:
- Generic `susp=` call in Day 102 violates the current contract and can crash.
- Validation says Ren'Py contract lint skipped because no Ren'Py game scripts were detected under the current argument/profile behavior; this should be fixed or separately linted before promotion.
- Deprecated routers remain for compatibility. That is acceptable for now, but must not become a dumping ground.
- Dynamic jump/call targets need simulator awareness or explicit test coverage.

## UI / UX Review

UI grade: **C+**

What works:
- Persistent stats overlay exists.
- Ledger UI exists.
- Thought overlay supports Cora's inner voice.
- NVL book-writing screen exists and uses manuscript/penny dreadful framing.
- Ending labels hide the stats overlay.

What does not:
- Many UI assets are missing/fallbacked.
- Book screen assets are declared but reported missing.
- Audio is not integrated into active scripts.
- Sidebar/ledger are functional, but not yet proven polished across all scenes.
- The writing screen risks feeling like a text renderer unless art/state feedback is added.

For this particular project, UI is not just polish. The book-writing UI is part of the fantasy. It needs to feel like Cora's illicit object, not a debug overlay.

## Asset Review

Asset grade: **D+**

This is the most urgent gap.

The asset manifest is useful and well-intentioned: fallback declarations mean the build can avoid hard crashes. But fallbacks are not shippable for an adult VN demo that depends on place, mood, class texture, and manuscript imagery.

Minimum asset requirement for MVP:
- All active backgrounds physically present.
- Cora, Gideon, Stern, Missy, Vance core sprites physically present in active poses.
- Book-writing UI assets present.
- At least two manuscript payoff CGs present and actually shown.
- Photograph and burning/evidence moment visually represented, or the CG declarations removed/deferred.
- Music or ambient audio hooked into at least major mode shifts: hotel floor, suite, writing, danger.

## Required To Ship The MVP

### Blockers

1. Fix the Day 102 generic suspicion crash.
   - Replace `apply_effects(susp=10, insp=5, corr=15)` in `day102_4_cora_sneaks_a_feel` with a character-specific suspicion target.

2. Get validation green.
   - Refresh scene direction for Day 103 and Day 104.
   - Run non-canon formatting repair for the file validation says would change.
   - Re-run `scripts/validate.py` on the scoped non-prod files until it passes.

3. Resolve asset drift for active MVP paths.
   - Either add the missing assets, correct manifest paths/extensions, or explicitly defer unused declarations.
   - Do not ship with manuscript CGs declared but invisible/missing.

4. Run a main-spine playthrough.
   - Day 100 start through Day 105 ending.
   - Confirm stats overlay, ledger, writing UI, deadline gates, and endings.

5. Run a branch smoke matrix.
   - At minimum: predator/prey/ghost routes, Missy betrayal/repair, Day 104 photograph/no photograph, Day 105 dynamic outcomes.

### High Priority

6. Make the first adult manuscript payoff visible.
   - Day 101 or Day 102 must visibly communicate: "This is where the adult game lives."

7. Verify Book 1 route rendering.
   - Use the existing `test_day2_writing_harness` or equivalent to prove all chapter variants render and return safely.

8. Clean packaging/development debris.
   - Exclude test harnesses, backup files, source/input images, and editor plugins from any public package unless intentionally included.

9. Integrate audio intentionally.
   - Current audio aliases are declared but not actively used in scoped scripts. Add minimal music/ambience cues or remove/defer claims.

10. Close graph/documentation drift.
   - Add missing balancing-relevant DAG gate tags.
   - Decide whether router outcome mismatches are expected deprecated compatibility routes.
   - Sync storyboard if script labels are planning-relevant.

## Recommended Action Items

- **Ship:** Preserve the Cora/Gideon Day 105 leverage-collapse ending. It is the correct MVP thesis.
- **Ship:** Preserve the manuscript-reckoning structure and route-aware Book 1 chapters.
- **Ship:** Preserve the anxiety/suspicion architecture and chain-window design.
- **Rewrite:** Tighten any early writing-scene passages that are more analytical than sensorial. The first payoff must be felt before it is interpreted.
- **Escalate:** Add visible manuscript CG/UI payoff by Day 101/102.
- **Escalate:** Make Book 1 page image selection route-aware and obvious to the player.
- **Escalate:** Add music/ambience for writing, suite pressure, and danger states.
- **Cut/Defer:** Remove or package-exclude unused dev/test/editor artifacts from the MVP build.
- **Cut/Defer:** Do not promise a "minigame" unless interactivity is added. Call it writing sequence/manuscript scene if it remains mostly presentation.
- **Fix:** Replace the remaining generic `susp=` effect.
- **Fix:** Scene direction and formatting validation drift.
- **Fix:** Missing assets or bad manifest paths.

## Promotion Verdict

**PROMOTE WITH CHANGES / DO NOT PUBLIC-SHIP YET**

The non-production MVP has enough story, structure, and market identity to move toward promotion. It should not be publicly shipped until validation is green, the Day 102 effect crash is fixed, active assets are physically present, and the manuscript payoff is visible rather than mostly declared. The project is close in the way a strong stage rehearsal is close: the performances are there, but the lights, cues, props, and safety checks still decide whether the audience sees the show you actually built.
