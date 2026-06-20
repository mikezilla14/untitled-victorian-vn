# Release 1 MVP Full Review

Date: 2026-06-20

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
- Fresh repository unit-test run: 31 tests passed
- Fresh asset-manifest audit via `scripts/daily_asset_manifest.py`
- Review of `release1_route_matrix_results.md`, `runtime_model_comparison.md`, and `P1_corruption_forward.jsonl`
- Static inspection of all source `.rpy` files in the non-production game, excluding bundled ActionEditor internals from narrative grading
- Review of current `log.txt` (no current `traceback.txt` or `errors.txt` in the non-prod tree)
- Review of the Release 1 graph audit/gaps, grain gaps, integration checklist, and June 20 standup report

No complete human-equivalent manual playthrough of all required paths was performed as part of this static review. One runtime capture now exists (P1 corruption-forward). The remaining six matrix paths are still unrecorded.

## Executive Verdict

The project has a strong game inside an unfinished release candidate — and for the first time, one full success path is evidenced end-to-end.

**Overall project grade: B**

**Current public-build readiness: C+**

**MVP promotion verdict: DO NOT PROMOTE**

The writing, premise, character architecture, and state model remain materially better than the presentation and release proof around them. Since the June 19 review, the team has converted structural progress into one verified runtime proof: a corruption-forward Day 100–105 run reaches `day105_7_release_one_ending` with `manuscript_progress` 5, captured in JSONL and validated by the runtime comparison tool after a Day 2 mandatory-write fix. Phases 4 (dynamic chains/penance) and 5 (Book 1 loop) are complete on the integration checklist. Static balance checks pass for all manuscript gates and fail-state wiring.

What still prevents shipment is concentrated and familiar: no recorded zero-error Ren'Py lint result, full-validator false positives on `screens.rpy`, six of seven route-matrix paths still pending, five missing UI assets and all six central CGs absent, minimal audio use in active scenes, placeholder title/version metadata, development tooling mixed into the game tree, and planning documents that understate remaining blockers.

This should not be solved by adding more days or more systems. The MVP needs a hard stabilization, QA completion, and presentation pass.

## Grade Summary

| Element | Grade | Assessment |
|---|---:|---|
| Core premise and differentiation | A | A covert Irish maid turning class danger and private scandal into forbidden fiction is clear, specific, and marketable. |
| Cora's character architecture | A- | Her survival mask, Irish concealment, authorial hunger, and moral danger form a strong protagonist engine. |
| Five-day narrative spine | B+ | Escalation is coherent from exposure risk to attempted leverage to structural defeat and artistic diagnosis. |
| Ending and thematic resolution | A- | Day 105 closes the release thematically without pretending Cora can defeat class power with one photograph. |
| Supporting cast | B+ | Gideon, Stern, Missy, and Vance each embody a distinct pressure system rather than functioning as route furniture. |
| Character voice and canon alignment | B+ | All six day packages have valid narrative, psychology, and Victorian gate contracts; Day 102 prose formatting repair is still pending. |
| Choice design and branch memory | B+ | Choices alter state, relationships, manuscript framing, and consequences. P1 proves one corruption-forward path completes; other archetypes remain uncaptured. |
| Adult-market concept | A- | The kink ecology—service, surveillance, class authority, forbidden authorship, betrayal, and controlled submission—is unusually coherent. |
| Adult payoff delivery | B- | The prose has heat, but the promised visual manuscript payoff is largely absent. The game currently sells a stronger concept than build. |
| Manuscript writing system | B+ | P1 confirms five chapter completions and route-aware Book 1 integration; still closer to a sophisticated NVL sequence than a true minigame. |
| State architecture | B+ | Central classes, setter-driven flags, whitelisted states, targeted suspicion, anxiety, and named consequence windows are strong prototype architecture. |
| Code quality and maintainability | B | Validation recognizes the non-prod layout and 31 tests pass. Full lint still fails because the linter mistakes screen-language keywords for speakers, and dev/editor material remains mixed into runtime. |
| UI/UX and game feel | C+ | HUD, ledger, thought presentation, and book layout exist; missing UI art and incomplete audio/CG integration keep them prototype-grade. |
| Visual asset readiness | C | Runtime backgrounds and sprites are covered through the configured search pool. Five UI assets and all six CGs remain missing. |
| Audio readiness | C- | All 21 aliases resolve to physical source files in the non-prod pool, but active integration remains extremely thin and preview-track licensing still needs release treatment. |
| Testing and QA evidence | C | Thirty-one unit tests pass, all day contracts pass, and P1 runtime capture is green; six matrix paths and engine lint evidence are still missing. |
| Documentation and pipeline discipline | B- | Gates and handoffs are strong, but the June 20 standup claims no critical blockers while the playtest matrix remains 0/12 and eleven assets are still missing. |
| Packaging/release professionalism | D+ | Placeholder name/version, ActionEditor and test harness content, compiled artifacts, saves, cache, logs, and helper scripts require a deliberate build profile. |

## What Is Working

### 1. The project has a real dramatic and commercial identity

The strongest idea is the separation between restrained hotel reality and Cora's hotter authored reconstruction. The Savoy is not merely scenery. It is a machine of rooms, keys, uniforms, permissions, gossip, and unequal credibility. Cora survives by observing that machine and converts its concealed appetites into prose.

The opening establishes the manuscript as bodily risk rather than optional lore: `day100_non_canon.rpy` begins with the pages hidden against Cora's body and ends with Holywell Street as payment, danger, and ambition. The closing returns to the manuscript after Gideon dismantles the fantasy that evidence alone creates power.

That loop is excellent:

1. Cora witnesses or causes danger.
2. The player chooses how she interprets it.
3. Stats and relationships record the cost.
4. The manuscript transforms the event into adult content and self-analysis.
5. The transformed material changes what kind of Cora reaches Day 105.

This is the project to protect. Additional generic VN systems would weaken it.

### 2. Day 105 understands the story's actual thesis

The photograph is not a magic victory token. Gideon's class protection means truth without rank is weak, and Cora must confront her own use of Missy as part of the same machine she condemns. The final manuscript section explicitly expands Gideon from singular monster into visible instrument of a larger structure.

The ending also preserves forward momentum:

- Cora completes the Release 1 manuscript.
- Gideon leaves but marks her as future interest.
- Vance remains bound to him.
- Missy's final physical position changes according to trust damage.
- Money and entanglement choices carry forward.

This is a satisfying demo ending because it resolves the release's question—what has Cora learned?—while leaving the campaign question open.

### 3. Cora is compelling because she is dangerous, not clean

Cora's canon and scripts agree on the most important point: she is not a pure whistleblower. She wants survival, money, craft, recognition, and sometimes the thrill of capability. She can protect Missy, use her, or turn her into narrative material. She can study suffering without being morally outside it.

That makes player choice meaningful. Observer, predator, prey, and ghost are not cosmetic personality badges; they are different methods of surviving and authoring the same class trap.

The character would be less interesting if the team softened her into a modern moral spokesperson. Do not do that.

### 4. The supporting cast has functional thematic separation

- **Gideon** is recognition, sovereignty, and institutional impunity. His best function is not simple villainy but the terrifying fact that he understands Cora and can afford to be amused.
- **Stern** turns discipline into both domination and working-class armor. Her optional chain extends the same idea rather than contradicting it.
- **Missy** is the strongest moral consequence system. Her intimacy only works when supported by trust, and betrayal changes her final relationship to Cora.
- **Vance** is the cost of exchanging sovereignty for protection and luxury. Her cruelty is displaced humiliation, which keeps her from becoming a flat jealous mistress.

The optional chains also serve distinct adult tastes: procedural dominance, romantic/tactile trust, and class voyeurism/power reversal. That breadth is commercially useful because it grows from character rather than from disconnected fetish scenes.

### 5. The state architecture is thoughtful

The current non-prod class layer provides:

- Central `TimeManager`, `PlayerStats`, and `StoryState` instances
- Character-specific base and acute suspicion
- Derived global anxiety
- Whitelisted mutually exclusive story states
- Setter-driven tracked flags
- Named consequence windows
- Dynamic optional-chain label resolution
- Manuscript chapter completion and Release 1 completion state
- Writing gates with explicit inspiration/corruption requirements

The earlier generic `apply_effects(susp=...)` runtime hazard is no longer present in player scripts. Current calls target specific witnesses.

This is a good foundation for an MVP. It should be frozen and stabilized rather than expanded.

### 6. Narrative production discipline is strong

Fresh contract validation passes for Day 100, 101, 102, 103, 104, and 105. Each day has:

- Convergent report
- Spec scripts
- Lead narrative gate
- Forensic psychology gate
- Victorian gate
- Promotion handoff

Day 105 also has its profile delta. All gate JSON files report non-blocking pass-equivalent verdicts.

Fresh scoped validation of the non-prod day scripts reports:

- Historical lint sound across the day scripts and Book 1 files
- Scene direction up to date
- Non-canon formatter would change zero files
- Engineering compliance passes for the current non-prod path
- Ren'Py contract checks pass when correctly scoped to episodic day scripts
- All 31 repository tests pass, including validation-path regression tests

The static balance report (`balance_report.md`, generated 2026-06-19) passes all manuscript gate hooks, fail-state references, and Book 1 slot wiring checks.

### 7. Structural asset coverage remains strong in the runtime pool

The June 20 asset reconciliation reports every declared background, sprite, and audio alias present somewhere in the runtime search pool. Backgrounds, sprites, and audio are complete at the union level. The deficit remains concentrated in presentation assets: five UI pieces and six event/manuscript CGs.

Notable reconciliation detail: `ui_sidebar_bg.png` exists on disk in production but is undeclared because the manifest expects `ui_sidebar_bg.webp`. That is integration debt, not missing art.

### 8. One full success path is now evidenced (new since June 19)

The route matrix records **P1 PASS** on 2026-06-20 after a Day 2 mandatory-write fix:

| Item | Value |
|------|--------|
| Run ID | `P1_corruption_forward` |
| Ending | `day105_7_release_one_ending` |
| `manuscript_progress` | 5 |
| Capture | `main-game/non-prod-game/debug_captures/P1_corruption_forward.jsonl` (260 events) |
| Comparison | `runtime_model_comparison.md` — structure PASS, assertions PASS |

This is the first machine-verified proof that the Release 1 spine, writing gates, Book 1 ladder, and MVP ending can complete without harness cheats. It does not yet prove cautious, fail-state, or penance paths.

Integration checklist Phases 4 and 5 are at 100% (dynamic chains/penance and Book 1 loop). Overall checklist completion is 60/130 (46.2%).

## What Is Not Working

### 1. The full release validator is still not green

Engineering compliance passes, and regression tests confirm that non-prod day/shared files and `variables.rpy` are discovered correctly.

The fresh full validation still fails because `renpy_contract_linter.py` scans `screens.rpy` as though screen-language statements were dialogue. It reports words such as `text`, `add`, `style`, `background`, and `textbutton` as undefined speakers, plus Python builtin `getattr` as an unresolved callable.

These are false positives. The standalone contract check passes when scoped to the episodic day scripts, and the repository's builtin-suppression tests pass. The linter nevertheless needs a file-type-aware parser or an explicit exclusion for screen language before the official full validation command can be trusted.

Separately, the Chief Architect requires actual `renpy lint` with zero errors. Repository contract lint and unit tests are not a substitute for the engine's own lint command.

**Ship impact: blocking.**

### 2. The route matrix is started but far from complete

Progress since June 19 is real but narrow:

| Status | Count |
|--------|------:|
| Runtime captures recorded | 1 / 7 |
| Integration checklist playtest sign-off | 0 / 12 |
| Abstract sim paths still pending capture | P2, P3, P7 |

P1 validates corruption-forward completion. Still needed:

- A cautious completion (P2)
- Low-corruption rejection (P3)
- Both manuscript deadline failures (P4, P5)
- Anxiety dismissal (P6)
- Stern, Missy, and Vance confrontation/penance (P7)
- Save/load across day boundaries and inside the Book 1 screen

Dynamic `call expression` targets are used for character chains. Static graph extraction explicitly cannot fully resolve them. This increases the importance of runtime path testing.

The integration checklist still marks P1 unchecked even though `release1_route_matrix_results.md` records it PASS. Planning artifacts need sync.

**Ship impact: blocking.**

### 3. Deadline and fail-state wiring still has open items

Static balance checks confirm fail labels exist and are referenced. The Chief Architect standup report nevertheless flags that **deadline hard-fail gates still require wiring**, and Phase 2 of the integration checklist remains at 2/8 (25%). Abstract simulation suggests P4–P6 should pass, but none have runtime captures yet.

**Ship impact: blocking until P4–P6 are captured or explicitly waived with evidence.**

### 4. The adult promise is visually underdelivered

The storyboard calls manuscript retellings the MVP's primary adult-game handshake. The manifest declares:

- `cg_manuscript_retelling_d1_corridor`
- `cg_manuscript_retelling_d2_lace`
- `cg_manuscript_retelling_d3_brush`
- `cg_manuscript_retelling_d4_false_dawn`
- `cg_gideon_photograph`
- `cg_photograph_burning`

All six are absent from disk. The photograph show commands in Day 104/105 are commented out. The manuscript CG declarations are unused by active script scanning.

The Book 1 system can set `book1_page_image`, but its default is the also-missing `ui_book_cover` in paths that rely on undeclared UI skin assets. The result is that the strongest market-facing concept is currently supported mainly by text and fallback behavior.

For a literary itch.io prototype this may be tolerable. For an F95-style adult VN launch, it is not. Players will understand the premise but may reasonably conclude that the game is promising future erotic presentation rather than delivering it.

**Ship impact: blocking for target-market release.**

### 5. The audio files exist, but the soundscape is still barely integrated

All 21 declared aliases resolve to physical files through the non-prod manifest and search pool. The set includes themes, footsteps, steam, fireplace ambience, writing sounds, keys, doors, a train whistle, a slap, and clatter effects.

Actual script use remains minimal. The Book 1 entry conditionally plays `audio_themes_private_ink`; the main day scripts do not yet establish a consistent ambience/theme/SFX layer. Phase 6 audio tasks in the integration checklist remain largely unchecked.

The Savoy still requires auditory class texture—bells, doors, footsteps, laundry, muted rooms, writing sounds—not merely files sitting in a folder. Preview-track licensing, attribution, and final replacement policy also need to be explicit before distribution.

**Ship impact: high, though a deliberately scoped minimum audio pass is sufficient.**

### 6. Asset debt is still concentrated in UI and CG payoff

The cross-project reconciliation reports zero missing backgrounds, zero missing sprites, and zero missing audio aliases in the runtime search pool. It still reports eleven missing assets:

- Five UI assets: book UI background, illustration border, price badge, sidebar background, and sidebar divider
- Six event illustrations: four manuscript retellings, Gideon's photograph, and the burning photograph

The non-prod project deliberately pulls most shared images from `main-game/prod-game/game` using `config.searchpath`. This makes the sandbox playable, but the public packaging contract must include or copy those resolved assets. A non-prod folder that only works beside the repository's production asset tree is not a self-contained release.

**Ship impact: blocking where used on the main route; high elsewhere.**

### 7. The manuscript "minigame" is overnamed

The Book 1 layer is a route-aware manuscript presentation system:

- It chooses chapter blocks from prior state.
- It changes prose by branch.
- It tracks completion.
- It can display an illustration.
- It uses a custom NVL presentation.

What it does not yet clearly provide is an interactive minigame loop inside the writing sequence. Most player agency occurs before the scene, not during composition.

That is not a design failure. The writing sequences are valuable as authored payoff. The failure is expectation management. Either:

- Present them as "manuscript sequences" or "authored retellings," or
- Add one or two meaningful in-sequence choices that alter language, illustration, cost, or later publication outcome.

Do not build a large drafting simulator for this MVP.

### 8. Some adult content is mechanically labeled rather than dramatically presented

Optional chain menus contain player-facing captions such as "Climax: 2.2 Spice," explicit stat deltas, suspicion thresholds, and anxiety requirements. These are useful during balancing but can feel like design-document text inside the fiction.

The game must choose whether this transparency is part of its final identity. If it is, style it as a deliberate risk forecast or authorial ledger. If it is not, move exact numbers and internal spice labels to a tooltip, accessibility option, or developer mode.

The current wording risks flattening tension by telling the player the scene's rating before the scene earns it.

**Ship impact: medium.**

### 9. The prose is sometimes more diagnostic than sensory

The writing is strongest when Cora's analysis emerges from physical detail, social procedure, and compromised action. It is weaker when narration explains the thesis immediately after dramatizing it.

Day 105 earns its analytical register because it is the release's reckoning. Earlier scenes should be more selective. The adult audience needs to feel the steam, cloth, proximity, silence, key, collar, and fear before receiving Cora's diagnosis.

Day 102 prose formatting repair is still pending per the Lead Narrative Editor standup report.

This is not a request to make the literal hotel action indiscriminately explicit. The better division remains:

- Hotel reality: restrained, plausible, dangerous, tactile
- Manuscript layer: heightened, eroticized, revealing, visually distinct

**Ship impact: polish, not structural blocker.**

### 10. The README and release metadata are stale

The non-prod README still describes:

- A five-day structure despite Day 100 plus Day 101–105
- Older flat file locations rather than `game/days/` and `game/shared/`
- Older feature/stat descriptions
- "Placeholder prose"
- A structure with files such as `classes.rpy` that do not match the current non-prod filenames

The build metadata remains:

- `config.name = "Untitled Victorian VN"`
- `config.version = "1.0"`
- `build.name = "UntitledVictorianVN"`

An MVP can keep a working title, but a public package should not accidentally present prototype metadata as a polished 1.0.

**Ship impact: high for release professionalism.**

### 11. Development tooling is mixed into the runtime project

The project tree contains:

- `AEditor/`
- A test-writing harness
- `.rpyc` compiled files
- local saves
- cache data
- log files
- an editor/warp library
- helper scripts and project metadata

The latest `log.txt` shows a successful Ren'Py 8.5.2 interface start on June 20. No current `traceback.txt` or `errors.txt` is present in the non-prod tree — an improvement over the June 19 baseline.

Create an explicit distribution profile that excludes development-only files. Do not delete useful sandbox tools from the repository merely to package the game.

**Ship impact: blocking for packaging, not for internal development.**

### 12. Planning signals contradict remaining blockers (new emphasis)

The June 20 standup reports:

- "No critical blockages or pending actions"
- Chief Architect: "Asset Manifest Sync: All declared assets exist physically on disk"
- Adult Market Reviewer: "None (all market and erotic engine structures verified)"

Meanwhile:

- Playtest matrix sign-off is 0/12
- Daily asset manifest reports eleven missing assets
- Full validation is not green
- Engine lint is not recorded
- Six route captures are pending

This is a process-trust problem. Automated standup optimism must not replace ship criteria.

**Ship impact: medium for team coordination; high if mistaken for release clearance.**

## Market Viability

**Current market viability: B+**

**Potential after a focused ship pass: A-**

The project has a stronger niche proposition than most early adult VN builds. It is not selling generic Victorian decadence. It is selling authorship as transgression:

> A precarious Irish chambermaid steals knowledge from a luxury hotel's private rooms and turns class violence, appetite, and betrayal into a forbidden book.

That pitch supports multiple desirable audience hooks:

- Maid/service hierarchy
- Dominant aristocratic male pressure
- Female intimacy based on earned trust
- Mature authority in Stern
- Humiliated upper-class companion in Vance
- Voyeurism and surveillance
- Corruption and risk progression
- Writing/creation as erotic transformation
- Choices that change the protagonist's moral and erotic lens

The market danger is not that the story is too slow. It is that the build may look evasive because the visible payoff is not ready. Slow burn works when the player can see the promised fire. The MVP needs an unmistakable manuscript payoff in its first substantial session and at least one later escalation.

P1 now proves the narrative engine can deliver a full arc. It does not yet prove the visible adult presentation layer matches the pitch.

The right escalation is not "make every hotel scene explicit." It is:

- Deliver the manuscript layer visibly.
- Make route flavor legible in art and presentation.
- Preserve the literal hotel's restraint so the fantasy contrast remains meaningful.

## Tone and Tension Breakdown

### Strong

- Class rules are erotic pressure rather than historical wallpaper.
- Stern's keys, inspections, and procedural language create a credible dominance grammar.
- Missy's intimacy is connected to trust and therefore has emotional stakes.
- Vance's submission and displaced cruelty make her simultaneously threatening and pitiable.
- Gideon's composure makes him more dangerous than a shouting villain.
- Cora's manuscript allows desire to be both payoff and evidence of character.

### Weak or incomplete

- Major visual peaks are absent.
- The early payoff relies heavily on prose.
- Debug-like spice labels can pre-chew tension.
- Audio does not yet make the Savoy feel inhabited.
- The Book 1 UI lacks its intended physical-object quality.
- Some prose explains power after the scene has already shown it.

## Production vs Draft Reality

### Implemented in the non-production build

- Entry from `label start` into Day 100
- Day 100–105 narrative spine
- Main branch states and route-aware ending flavor
- Character-specific suspicion and derived anxiety
- Optional Stern, Missy, and Vance chains (Phase 4 complete)
- Penance/confrontation labels
- Writing gates and manuscript progress (Phase 5 complete)
- Four fail/bad-ending labels (static wiring verified; runtime capture incomplete)
- Book 1 route-aware chapter blocks
- HUD, ledger, thought, and NVL manuscript screens
- Asset fallbacks
- All 21 declared audio aliases backed by physical preview/source files in non-prod
- Runtime background and sprite coverage through the configured non-prod plus shared production-asset search pool
- Valid gate/handoff contracts for every release day
- **P1 corruption-forward runtime capture to MVP ending**

### Declared or designed but not convincingly delivered

- Manuscript retelling CG set
- Photograph/burning CGs
- Complete Book 1 UI skin
- Integrated soundscape
- Proven full-route balance (1/7 captures)
- Proven Ren'Py contract/lint cleanliness on full profile
- Public distribution packaging

### Documentation/tooling drift

- Legacy request path no longer exists
- README structure is outdated
- Full contract lint is not screen-language-aware and emits false positives
- `check_assets.py` audits production top-level scripts rather than the scoped non-prod project
- June 20 standup understates blockers relative to checklist and asset manifest
- Integration checklist P1 checkbox not synced with route matrix PASS
- Graph/grain reports retain dynamic-target and untagged-balance-gate notes (8 major grain gaps, no blockers)
- Checklist completion does not demonstrate route QA

## Required to Ship the MVP

### P0 — Hard blockers

1. **Make the full validation command reliable and green.**
   - Stop the contract linter from treating screen-language keywords as dialogue speakers.
   - Keep the now-working non-prod path regression tests.
   - Produce a recorded zero-error Ren'Py lint result.

2. **Complete and record runtime QA.**
   - Finish the required path matrix from `label start` (P2–P7 after P1).
   - Record route, ending, state, and save/load results.
   - Test dynamic chain calls and penance consumption.
   - Sync integration checklist and standup messaging with actual capture status.
   - Confirm no route can soft-lock manuscript progress unintentionally.

3. **Close main-route visual gaps.**
   - Resolve the five remaining UI assets and manifest/path mismatches (including `ui_sidebar_bg` format registration).
   - Deliver at least two manuscript payoff CGs, including one early.
   - Either deliver photograph CGs and enable them or remove the MVP promise.

4. **Create a clean distribution profile.**
   - Exclude ActionEditor, tests, saves, cache, `.rpyc`, logs, editor libraries, and helper scripts from the public package.
   - Test the packaged build, not only the working project.

### P1 — Required quality

5. **Integrate a minimum sound pass.**
   - Writing theme
   - Hotel/corridor ambience
   - Master Suite pressure theme
   - A small set of high-value effects: key, door, floorboard, writing
   - Resolve licensing/attribution and final-use status for preview tracks before distribution

6. **Clarify the writing feature.**
   - Rename it as a manuscript sequence unless meaningful in-sequence choices are added.
   - Ensure route-specific illustration/prose state is visible to the player.

7. **Decide the information-design policy.**
   - Keep exact stat thresholds only if the ledger/risk-forecast presentation makes them feel intentional.
   - Remove internal "Spice 2.2" language from final-facing menu copy or move it to an optional UI layer.

8. **Update player-facing documentation and metadata.**
   - Correct project structure and day count.
   - Describe current mechanics accurately.
   - Set an honest MVP/demo version.
   - Add content warnings, adult-age clarity, tags, credits, licenses, and save-compatibility expectations.

9. **Finish fail-state wiring and verify with captures.**
   - Close Phase 2 checklist items and record P4–P6 runtime evidence.

### P2 — Strong polish

10. **Tighten explanatory narration.**
    - Preserve Day 105's diagnostic power.
    - In earlier scenes, favor image, sensation, behavior, and implication before thesis.
    - Complete Day 102 prose formatting repair.

11. **Resolve graph/documentation drift.**
    - Refresh graph artifacts after final script freeze.
    - Tag or document the eight major untagged balance gates in grain gaps.
    - Document dynamic chain windows.
    - Synchronize storyboard labels and current state names.

12. **Run presentation QA.**
    - 16:9 desktop resolutions
    - Text overflow and long menu captions
    - Skip/rollback behavior around Python state and Book 1
    - Save/load inside manuscript screens
    - Main-menu, preferences, history, accessibility, and ending return flow

## Recommended Ship Sequence

1. Freeze story scope and state API.
2. Fix screen-language linting and obtain a clean engine-lint record.
3. Sync checklist/route matrix/standup reporting.
4. Run remaining route captures (P4 next, then P2/P3) and fix runtime blockers.
5. Close core UI assets and manifest/path mismatches.
6. Add the early and late manuscript CG payoffs.
7. Add the minimum soundscape.
8. Remove or restyle debug-facing menu language.
9. Package a clean candidate.
10. Test the packaged candidate on a clean machine/profile.
11. Perform one final narrative/market pass against only what the player can actually see.

## Action Items by Reviewer Category

### Ship

- Core premise
- Day 100–105 spine
- Day 105 structural-power ending
- Cora's morally dangerous authorship
- Character-specific suspicion/anxiety model
- Missy trust consequences
- Stern/Missy/Vance optional-chain concept
- Gideon's recurring-pressure role
- Route-aware manuscript prose
- P1 corruption-forward runtime proof

### Rewrite

- Stale README and public-facing descriptions
- Menu captions that expose internal spice labels as final copy
- Selected explanatory passages that restate already-dramatized themes
- Day 102 prose formatting repair

### Escalate

- Early manuscript visual payoff
- Route-specific Book 1 presentation
- Audio use and environmental texture
- Visual treatment of the photograph and its destruction
- Clear marketing tags and adult premise in the first session
- Remaining route-matrix captures (P2–P7)

### Cut or exclude from distribution

- ActionEditor runtime content
- Test harness labels
- saves/cache/compiled/log/editor artifacts
- Unused manifest promises that will not be delivered for MVP

### Defer

- Additional days
- Large new relationship systems
- A complex writing simulator
- More optional chains beyond the current three-level structure
- Broad animation or voice acting

## Final Promotion Verdict

**DO NOT PROMOTE**

The narrative and system design are strong enough to become the MVP; the current build is not yet a trustworthy or market-complete release candidate. P1 is meaningful progress — it proves one corruption-forward arc completes with full manuscript progress — but promotion should resume only after the full validator is green, the remaining route matrix is recorded, the manuscript's visual payoff is physically present, fail-state captures are complete, and a clean packaged build passes engine lint and smoke testing.
