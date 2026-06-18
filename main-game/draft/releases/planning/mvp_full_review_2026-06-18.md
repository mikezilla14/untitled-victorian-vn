# Release 1 MVP Full Review

Date: 2026-06-18

Requested lenses:

- Chief Architect: runtime structure, state discipline, validation, assets, packaging, and promotion readiness.
- Adult Market Reviewer: adult-VN promise, tension, payoff cadence, fetish clarity, and commercial presentation.
- Lead Narrative Editor: story architecture, character voice, continuity, choice meaning, and thematic resolution.

## Scope and Method

The path named in the request, `narrative/draft/releases/release-1-mvp/non_prod_renpy_project`, no longer exists. Repository documentation identifies `main-game/non-prod-game/` as the current equivalent and active non-production Ren'Py project. This review is therefore based on:

- `main-game/non-prod-game/`
- Direct Release 1 support files in `main-game/draft/releases/planning/`
- Release 1 graph and gate artifacts in `main-game/pipeline/releases/release-1-mvp/`
- Canon and voice files directly required to judge the scripts

Production files were not used to give the non-production build credit. Backlog ideas were not counted as implemented features.

Evidence gathered:

- Fresh `scripts/validate.py` run against the scoped project
- Fresh `scripts/contract_validate.py` run for Day 100 through Day 105
- Fresh asset-manifest audit
- Static inspection of all source `.rpy` files in the non-production game, excluding bundled ActionEditor internals from narrative grading
- Review of current `log.txt` and `traceback.txt`
- Review of the Release 1 graph audit/gaps and integration checklist

No complete human-equivalent route playthrough was performed as part of this static review. The absence of recorded route-matrix results is itself a ship-readiness finding.

## Executive Verdict

The project has a strong game inside an unfinished release candidate.

**Overall project grade: B**

**Current public-build readiness: C-**

**MVP promotion verdict: DO NOT PROMOTE**

The writing, premise, character architecture, and state model are materially better than the presentation and release proof around them. The five-day arc is coherent and distinctive. Cora's forbidden manuscript is not a decorative side system; it is the project's thematic and commercial center. The game also has meaningful branch memory, relationship pressure, fail states, and an unusually thoughtful class-erotic framework.

What prevents shipment is no longer primarily missing story. It is missing confidence and missing delivery: no evidenced full route matrix, no zero-error Ren'Py lint result, a validator blind spot for the current non-prod path, 25 declared images and 16 declared audio files absent from disk, all 21 audio aliases unused by the asset scanner, six central CGs absent and not shown, placeholder-facing title/version metadata, and development tooling mixed into the game tree.

This should not be solved by adding more days or more systems. The MVP needs a hard stabilization and presentation pass.

## Grade Summary

| Element | Grade | Assessment |
|---|---:|---|
| Core premise and differentiation | A | A covert Irish maid turning class danger and private scandal into forbidden fiction is clear, specific, and marketable. |
| Cora's character architecture | A- | Her survival mask, Irish concealment, authorial hunger, and moral danger form a strong protagonist engine. |
| Five-day narrative spine | B+ | Escalation is coherent from exposure risk to attempted leverage to structural defeat and artistic diagnosis. |
| Ending and thematic resolution | A- | Day 105 closes the release thematically without pretending Cora can defeat class power with one photograph. |
| Supporting cast | B+ | Gideon, Stern, Missy, and Vance each embody a distinct pressure system rather than functioning as route furniture. |
| Character voice and canon alignment | B+ | All six day packages have valid narrative, psychology, and Victorian gate contracts; some prose still reads more analytical than embodied. |
| Choice design and branch memory | B+ | Choices alter state, relationships, manuscript framing, and consequences. Full balancing and reachability proof are missing. |
| Adult-market concept | A- | The kink ecology—service, surveillance, class authority, forbidden authorship, betrayal, and controlled submission—is unusually coherent. |
| Adult payoff delivery | B- | The prose has heat, but the promised visual manuscript payoff is largely absent. The game currently sells a stronger concept than build. |
| Manuscript writing system | B+ | It is structurally integrated and route-aware, but presently closer to a sophisticated NVL sequence than a true minigame. |
| State architecture | B+ | Central classes, setter-driven flags, whitelisted states, targeted suspicion, anxiety, and named consequence windows are strong prototype architecture. |
| Code quality and maintainability | B- | The structure is intelligible, but validation policy does not correctly recognize all scoped files, lint proof is absent, and dev/editor material is mixed into runtime. |
| UI/UX and game feel | C+ | HUD, ledger, thought presentation, and book layout exist; missing UI art and incomplete audio/CG integration keep them prototype-grade. |
| Visual asset readiness | D+ | Twenty-five declared images are absent, including the manuscript CG set and major UI/background assets. |
| Audio readiness | D | Five preview music files exist, but the audit finds 16 declared files absent and all 21 aliases unused in active script scanning. |
| Testing and QA evidence | D+ | Contracts pass and the project has launched, but there is no completed spine/branch/fail-state matrix and no zero-error Ren'Py lint evidence. |
| Documentation and pipeline discipline | B | Gates and handoffs are strong; README details, graph drift, path handling, and current completion claims remain inconsistent. |
| Packaging/release professionalism | D+ | Placeholder name/version, ActionEditor and test harness content, compiled artifacts, saves, logs, and stale crash evidence require a deliberate build profile. |

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

Fresh validation also reports:

- Historical lint sound across the day scripts and Book 1 files
- Scene direction up to date
- Non-canon formatter would change zero files
- All active image references declared in the manifest

These are real improvements over the June 13 baseline.

## What Is Not Working

### 1. Release validation is not trustworthy enough

The fresh aggregate validation fails engineering compliance by claiming the defaults in `main-game/non-prod-game/game/variables.rpy` are outside `variables.rpy`, even though that file is explicitly the centralized variables file. This appears to be a path-recognition defect in the validation policy.

More seriously, both the aggregate validator and direct `renpy_contract_linter.py` invocation report:

> No Ren'Py game scripts provided. Skipping Ren'Py contract lint.

The scripts were provided. The tooling simply does not recognize this current non-prod layout correctly.

This means the project cannot presently prove several Chief Architect contracts through its normal release command:

- Speaker definitions
- Callable symbols
- Label naming
- String interpolation hazards
- State assignment discipline
- Other Ren'Py source contracts

Static review did not find a remaining generic suspicion call, and current logs show successful interface startup, but that is not a substitute for a supported lint path.

**Ship impact: blocking.**

### 2. There is no evidenced complete route test

The integration checklist still leaves the main spine, branch axes, fail states, and required playtest paths unchecked. The graph audit is useful but not equivalent to executing the game.

At minimum the team still needs evidence for:

- A normal Day 100-to-Day 105 completion
- A cautious completion
- A corruption-forward completion
- Low-corruption rejection
- Both manuscript deadline failures
- Anxiety dismissal
- Stern, Missy, and Vance confrontation/penance
- All major branch-state values
- Save/load across day boundaries and inside the Book 1 screen

Dynamic `call expression` targets are used for character chains. They are a reasonable design, but static graph extraction explicitly cannot fully resolve them. This increases the importance of runtime path testing.

**Ship impact: blocking.**

### 3. The adult promise is visually underdelivered

The storyboard calls manuscript retellings the MVP's primary adult-game handshake. The manifest declares:

- `cg_manuscript_retelling_d1_corridor`
- `cg_manuscript_retelling_d2_lace`
- `cg_manuscript_retelling_d3_brush`
- `cg_manuscript_retelling_d4_false_dawn`
- `cg_gideon_photograph`
- `cg_photograph_burning`

All six are absent from disk. The photograph show commands in Day 104/105 are commented out. The manuscript CG declarations are unused by active script scanning.

The Book 1 system can set `book1_page_image`, but its default is the also-missing `ui_book_cover`. The result is that the strongest market-facing concept is currently supported mainly by text and fallback behavior.

For a literary itch.io prototype this may be tolerable. For an F95-style adult VN launch, it is not. Players will understand the premise but may reasonably conclude that the game is promising future erotic presentation rather than delivering it.

**Ship impact: blocking for target-market release.**

### 4. The audio layer is effectively unintegrated

Five preview MP3 tracks physically exist and are registered under some theme aliases. The Book 1 entry conditionally plays `audio_themes_private_ink`.

However, the asset audit reports:

- 16 declared audio files absent
- 21 declared audio aliases unused by active-script scanning
- Zero referenced audio aliases detected in code by the audit

The discrepancy between the guarded Book 1 play statement and the scanner's zero-reference result suggests the scanner does not understand variable-backed audio use. That is another tooling weakness, but it does not change the player-facing conclusion: there is no demonstrated full soundscape.

The Savoy requires auditory class texture—bells, doors, footsteps, laundry, muted rooms, writing sounds—not merely background music. Silence makes the hotel feel less like a social machine.

**Ship impact: high, though a deliberately scoped minimum audio pass is sufficient.**

### 5. Visual and UI asset debt remains high

The fresh asset audit reports 25 missing declared images. Important gaps include:

- Train and country-estate prologue backgrounds
- Master Suite night
- Servants' quarters side view
- Four Vance expressions
- Sidebar and divider assets
- Book paper, cover, background, border, and price badge
- Mini Cora UI states
- The complete manuscript CG set
- Photograph and burning CGs

Fallbacks protect runtime continuity, but they hide the very production gaps that a public demo must expose and resolve. A fallback is a development feature, not a finished asset.

**Ship impact: blocking where used on the main route; high elsewhere.**

### 6. The manuscript “minigame” is overnamed

The Book 1 layer is a route-aware manuscript presentation system:

- It chooses chapter blocks from prior state.
- It changes prose by branch.
- It tracks completion.
- It can display an illustration.
- It uses a custom NVL presentation.

What it does not yet clearly provide is an interactive minigame loop inside the writing sequence. Most player agency occurs before the scene, not during composition.

That is not a design failure. The writing sequences are valuable as authored payoff. The failure is expectation management. Either:

- Present them as “manuscript sequences” or “authored retellings,” or
- Add one or two meaningful in-sequence choices that alter language, illustration, cost, or later publication outcome.

Do not build a large drafting simulator for this MVP.

### 7. Some adult content is mechanically labeled rather than dramatically presented

Optional chain menus contain player-facing captions such as “Climax: 2.2 Spice,” explicit stat deltas, suspicion thresholds, and anxiety requirements. These are useful during balancing but can feel like design-document text inside the fiction.

The game must choose whether this transparency is part of its final identity. If it is, style it as a deliberate risk forecast or authorial ledger. If it is not, move exact numbers and internal spice labels to a tooltip, accessibility option, or developer mode.

The current wording risks flattening tension by telling the player the scene's rating before the scene earns it.

**Ship impact: medium.**

### 8. The prose is sometimes more diagnostic than sensory

The writing is strongest when Cora's analysis emerges from physical detail, social procedure, and compromised action. It is weaker when narration explains the thesis immediately after dramatizing it.

Day 105 earns its analytical register because it is the release's reckoning. Earlier scenes should be more selective. The adult audience needs to feel the steam, cloth, proximity, silence, key, collar, and fear before receiving Cora's diagnosis.

This is not a request to make the literal hotel action indiscriminately explicit. The better division remains:

- Hotel reality: restrained, plausible, dangerous, tactile
- Manuscript layer: heightened, eroticized, revealing, visually distinct

**Ship impact: polish, not structural blocker.**

### 9. The README and release metadata are stale

The non-prod README still describes:

- A five-day structure despite Day 100 plus Day 101–105
- Older flat file locations rather than `game/days/` and `game/shared/`
- Older feature/stat descriptions
- “Placeholder prose”
- A structure with files such as `classes.rpy` that do not match the current non-prod filenames

The build metadata remains:

- `config.name = "Untitled Victorian VN"`
- `config.version = "1.0"`
- `build.name = "UntitledVictorianVN"`

An MVP can keep a working title, but a public package should not accidentally present prototype metadata as a polished 1.0.

**Ship impact: high for release professionalism.**

### 10. Development tooling is mixed into the runtime project

The project tree contains:

- `AEditor/`
- A test-writing harness
- `.rpyc` compiled files
- local saves
- cache data
- log and traceback files
- an editor/warp library
- helper scripts and project metadata

The latest `log.txt` shows Ren'Py 8.5.2 successfully reaching the interface after multiple starts on June 18. The current `traceback.txt` records an earlier ActionEditor syntax error at `ActionEditor_screens.rpy:1207`. The malformed token is no longer present in the current source, so the traceback appears stale, but it demonstrates why editor tooling should not be part of a public game build.

Create an explicit distribution profile that excludes development-only files. Do not delete useful sandbox tools from the repository merely to package the game.

**Ship impact: blocking for packaging, not for internal development.**

## Market Viability

**Current market viability: B**

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

The right escalation is not “make every hotel scene explicit.” It is:

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
- Optional Stern, Missy, and Vance chains
- Penance/confrontation labels
- Writing gates and manuscript progress
- Four fail/bad-ending labels
- Book 1 route-aware chapter blocks
- HUD, ledger, thought, and NVL manuscript screens
- Asset fallbacks
- Five physical preview music files
- Valid gate/handoff contracts for every release day

### Declared or designed but not convincingly delivered

- Manuscript retelling CG set
- Photograph/burning CGs
- Complete Book 1 UI skin
- Complete background/sprite coverage
- Integrated soundscape
- Proven full-route balance
- Proven Ren'Py contract/lint cleanliness
- Public distribution packaging

### Documentation/tooling drift

- Legacy request path no longer exists
- README structure is outdated
- Validator path recognition is incorrect for current non-prod files
- Graph report retains dynamic-target, metadata, router, and storyboard drift notes
- Checklist completion does not demonstrate route QA

## Required to Ship the MVP

### P0 — Hard blockers

1. **Repair the validation path.**
   - Make engineering compliance recognize `main-game/non-prod-game/game/variables.rpy`.
   - Make `renpy_contract_linter.py` recognize the non-prod day/shared layout.
   - Produce a recorded zero-error Ren'Py lint result.

2. **Complete and record runtime QA.**
   - Run the required path matrix from `label start`.
   - Record route, ending, state, and save/load results.
   - Test dynamic chain calls and penance consumption.
   - Confirm no route can soft-lock manuscript progress unintentionally.

3. **Close main-route visual gaps.**
   - Add or replace every missing image used on the core spine.
   - Deliver the Book 1 UI's essential physical-object assets.
   - Deliver at least two manuscript payoff CGs, including one early.
   - Either deliver photograph CGs and enable them or remove the MVP promise.

4. **Create a clean distribution profile.**
   - Exclude ActionEditor, tests, saves, cache, `.rpyc`, logs, tracebacks, editor libraries, and helper scripts from the public package.
   - Test the packaged build, not only the working project.

### P1 — Required quality

5. **Integrate a minimum sound pass.**
   - Writing theme
   - Hotel/corridor ambience
   - Master Suite pressure theme
   - A small set of high-value effects: key, door, floorboard, writing
   - Resolve licensing/attribution for preview tracks before distribution

6. **Clarify the writing feature.**
   - Rename it as a manuscript sequence unless meaningful in-sequence choices are added.
   - Ensure route-specific illustration/prose state is visible to the player.

7. **Decide the information-design policy.**
   - Keep exact stat thresholds only if the ledger/risk-forecast presentation makes them feel intentional.
   - Remove internal “Spice 2.2” language from final-facing menu copy or move it to an optional UI layer.

8. **Update player-facing documentation and metadata.**
   - Correct project structure and day count.
   - Describe current mechanics accurately.
   - Set an honest MVP/demo version.
   - Add content warnings, adult-age clarity, tags, credits, licenses, and save-compatibility expectations.

### P2 — Strong polish

9. **Tighten explanatory narration.**
   - Preserve Day 105's diagnostic power.
   - In earlier scenes, favor image, sensation, behavior, and implication before thesis.

10. **Resolve graph/documentation drift.**
    - Refresh graph artifacts after final script freeze.
    - Document dynamic chain windows.
    - Retire or explicitly mark compatibility routers.
    - Synchronize storyboard labels and current state names.

11. **Run presentation QA.**
    - 16:9 desktop resolutions
    - Text overflow and long menu captions
    - Skip/rollback behavior around Python state and Book 1
    - Save/load inside manuscript screens
    - Main-menu, preferences, history, accessibility, and ending return flow

## Recommended Ship Sequence

1. Freeze story scope and state API.
2. Fix lint/validation recognition.
3. Run the route matrix and fix runtime blockers.
4. Close core backgrounds/UI assets.
5. Add the early and late manuscript CG payoffs.
6. Add the minimum soundscape.
7. Remove or restyle debug-facing menu language.
8. Package a clean candidate.
9. Test the packaged candidate on a clean machine/profile.
10. Perform one final narrative/market pass against only what the player can actually see.

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

### Rewrite

- Stale README and public-facing descriptions
- Menu captions that expose internal spice labels as final copy
- Selected explanatory passages that restate already-dramatized themes

### Escalate

- Early manuscript visual payoff
- Route-specific Book 1 presentation
- Sound and environmental texture
- Visual treatment of the photograph and its destruction
- Clear marketing tags and adult premise in the first session

### Cut or exclude from distribution

- ActionEditor runtime content
- Test harness labels
- saves/cache/compiled/log/traceback/editor artifacts
- Unused manifest promises that will not be delivered for MVP

### Defer

- Additional days
- Large new relationship systems
- A complex writing simulator
- More optional chains beyond the current three-level structure
- Broad animation or voice acting

## Final Promotion Verdict

**DO NOT PROMOTE**

The narrative and system design are strong enough to become the MVP; the current build is not yet a trustworthy or market-complete release candidate. Promotion should resume only after validation recognizes the project, a full route matrix is recorded, the manuscript's visual payoff is physically present, and a clean packaged build passes lint and smoke testing.

