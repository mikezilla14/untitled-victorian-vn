# Non-Canon MVP — Agent Review Report Card
**Project:** Untitled Victorian VN — Release 1 MVP (Days 100–105)
**Review Date:** 2026-05-23
**Branch:** `claude/non-canon-game-review-QC1H3`
**Reviewers:** Multi-agent panel (Lead Narrative Editor · Character/Voice Specialist · Victorian Consultant · Game Design Critic · Chief Architect)

---

## Overall Grade: B+

A high-quality first draft operating well above typical VN MVP standards. The literary ambition is genuine and largely realised. The mechanical architecture is production-ready at the canon layer. What keeps this from A territory is a small cluster of cross-cutting gaps — the archetype system is invisible to players, the prologue is underwritten relative to its load-bearing function, per-character suspicion in the chain draft contradicts the canonical runtime schema, and Irish identity specificity is promised by the character documents but absent from the prose. None are structural failures. All are fixable before promotion.

---

## Category Grades

| Category | Grade | Reviewer Role |
|---|---|---|
| [Story & Narrative](#1-story--narrative--a-) | A− | Lead Narrative Editor |
| [Character & Voice](#2-character--voice--a-) | A− | Character/Voice Specialist |
| [Gameplay & Mechanics](#3-gameplay--mechanics--b) | B+ | Game Design Critic |
| [Historical Accuracy](#4-historical-accuracy--b) | B+ | Victorian Consultant |
| [Technical Code Quality](#5-technical-code-quality--b) | B+ | Chief Architect |

---

## 1. Story & Narrative — A−

### Subgrades
| Criterion | Grade |
|---|---|
| Story Structure | A |
| Thematic Coherence | A+ |
| Narrative Pacing | A− |
| Branching Quality | B+ |
| Emotional Resonance | A |
| Plot Holes / Logical Gaps | B+ |

### Summary
The five-day arc executes the horror-film false-dawn structure with genuine craft. The thematic argument — that documentation is a form of power that does not require victory — is coherent from the first corridor choice to the final candlelight and delivered with the most consistent A+ of any category. The corruption/inspiration duality is not mechanical window-dressing: Inspiration produces *craft-as-dissection* while Corruption produces *appetite-as-distortion*, and neither is moralized.

Gideon's Day 105 leverage collapse is the arc's centerpiece: *"The police will ask why you were in my private rooms. My solicitor will ask who paid you... A publisher will ask whether a maid's scandal is worth a libel suit. Every decent woman in London will pretend she does not understand the accusation."* This converts a villain speech into a structural sociology lesson — exactly the correct register.

### Critical Strengths
- **The Gap mechanic** (internal vs. performed voice) is sustained at technical precision across all five days without a single register collapse
- **The false-dawn architecture** is stated in the Day 104 design header and then executed — Day 5 opens *"Morning arrives too cleanly. That should have warned me"*
- **The Missy betrayal aftermath** on the ghost path: *"There are many possible answers. None are small enough to fit in the corridor"* — economy of language converting moral failure into spatial observation

### Critical Weaknesses
- **Day 104 twilight dead loop:** `day104_4_twilight_ledger_false_dawn` jumps back to itself when suspicion ≥ 85, with no exit if both atonement and missy_repair are exhausted — hard mechanical blocker
- **Missy Cover / photograph prose contradiction:** `set_has_photograph(True)` is set but narration reads *"I stand in the corridor with empty hands"* — flag and prose directly contradict
- **Prologue underwritten:** Day 100 does the arc's heaviest lifting (Irish identity, forgery, literacy, manuscript) in fewer than 70 lines; the `prologue_found` flag sets two different discovery modes but produces no differentiated narration in subsequent days
- **Missy Debt emotional gap:** Players on the ghost path who do not use Missy as cover in Day 104 never see Missy respond to the Day 102 betrayal beyond corridor silence — the manuscript reckoning references her as *"debt"* but she never speaks for herself

### Lead Narrative Editor Agent Contribution
Voice Lock is the strongest output from this role — Cora's internal/external register, Gideon's economy, and Stern's procedural authority are consistently maintained. Stat-Story Alignment is less complete: the prologue's starting stat awards are not cross-referenced against the Day 101 writing gate in any formal document, and the Day 104 twilight loop represents an unresolved mechanical conflict that should have been flagged before this draft reached review. The label naming violation at `day103_2_suite_night_tea` (night scene carrying an Afternoon period digit) constitutes a compliance failure under Workflow step 2. The overall judgment: creative quality significantly exceeds procedural compliance record — the writing is exceptional, the systemic checks have identifiable gaps.

---

## 2. Character & Voice — A−

### Subgrades
| Criterion | Grade |
|---|---|
| Protagonist Depth (Cora / Gap Mechanic) | A |
| Supporting Character Distinctiveness | B+ |
| Character Arcs | A− |
| Relationship Dynamics | A |
| Voice Consistency | B+ |

### Summary
This is the project's most fully realised element. Cora's five-day tonal progression is legible and earned — the aphoristic internal voice clicks in on schedule without announcement, exactly as specified in the voice guide. Gideon is the strongest supporting performance: his economy, flat present-tense authority, and diagnostic rather than emotional attention hold across all five days. The Missy-Cora relationship correctly encodes both warmth and instrumentalisation without sentimentality.

The line *"I could use this. / I could also simply sit beside her for a minute and not turn her into material"* holds Cora's character (the thought exists) while granting the player an authentic moment — precisely the moral ambiguity the character document demands.

### Critical Strengths
- **The Day 2 Missy betrayal aftermath:** *"She does not cry. / That is the worst of it"* — the best single moment of relationship writing in the five days
- **Gideon's Day 5 summation:** *"Not powerful, Cora. Interesting. Do not confuse the two"* — the most concentrated expression of his character across all five days
- **The Ghost/Witness corridor path** renders sensory restraint as literary craft: *"A writer does not always need the picture. / Sometimes the keyhole is less useful than the wall"*
- **Class architecture** dramatised through grammar: Gideon commands in simple present with no conditional mood; Vance uses *"one"* to depersonalise corrections; Stern's authority is procedural rather than personal

### Critical Weaknesses
- **Day 3 Defy branch voice overshoot:** *"I expect those often look similar from above, Sir"* is a balanced, pointed riposte — Day 4/5 register on a Day 3 path, violating the Voice Guide's mandate that Day 3 deviations must be *"deniable"*
- **Vance underpowered in Days 4–5:** Her Day 5 beat (the guide specifies *"Cora cannot tell if this is loss or completion"*) is narrated in summary rather than dramatised with the analytical depth Cora should possess by this stage
- **Anti-Irish precarity underworked in prose:** The character document is explicit — *"she is not merely hiding scandal; she is hiding origin"* — but no internal beat shows a word, idiom, or consonant nearly escaping wrong
- **No Missy Voice Guide exists** despite Missy carrying the "Missy Debt" moral weight forward into Release 2; no Stern guide either

### Writers' Room & Victorian Consultant Agent Contributions
The Writers' Room's strongest contribution is the formal Voice Guides for Gideon and Vance — not adjective lists but per-day tonal progressions with dialogue rules and fail states specific enough to catch real inconsistencies. The Gideon Test (*"minimum number of words to accomplish exactly what he intends"*) is practical sentence-level guidance. The primary gap: no Missy Voice Guide despite her emotional centrality. The Victorian Consultant's contextual layer is strongest where embedded implicitly — vocabulary constraints, Vance's corrective register, Stern's procedural authority — but thinner on the specifically Irish texture of Cora's danger, which is documented in the character file but not rendered in the prose.

---

## 3. Gameplay & Mechanics — B+

### Subgrades
| Criterion | Grade |
|---|---|
| Stat System Design | B+ |
| Player Agency | A− |
| Archetype System | C+ |
| Fail State Design | B |
| Pacing of Mechanical Revelation | B− |
| Reward Loop | A− |

### Summary
The three-resource economy (Inspiration, Corruption, Anxiety) is conceptually elegant and thematically coherent. The single strongest mechanical idea is splitting Suspicion into three character-specific meters that sum into total Anxiety — this models how social pressure actually works (never one eye but the accumulation of them) and gives players a multi-front management problem.

The reward loop is the second-strongest area: the Chapter 1 write produces six meaningfully distinct paragraph combinations depending on corridor state and ledger focus. A player who explores multiple playthroughs discovers their choices genuinely shape what Cora writes — meaningful intrinsic reward reinforcing the meta-fiction premise.

### Critical Strengths
- **The Day 2 tea crisis** is the finest single branching moment: three options with distinct moral valences, different stat signatures, and forward ramifications persisting through Day 5's Gideon analysis
- **Dynamic prose generation** in writing scenes — the most distinctive mechanical idea in the build, executed with real craft
- **StoryState class architecture** — whitelisted setter pattern, chain availability gating, and carry-forward flag system are production-quality
- **The false-dawn / leverage collapse** on Days 4–5 is a mechanically sophisticated emotional move: player sense of agency deliberately built to be punctured

### Critical Weaknesses
- **No tutorial layer:** The HUD, the Inspiration cap, the Corruption/Inspiration capacity relationship, and the penance system are introduced with zero scaffolding — the most urgent shipping risk
- **Archetype system is player-invisible:** Observer/Predator/Prey/Ghost shapes the entire narrative but is never communicated to the player in text or UI; `cora_release1_flavour` is pure carry-forward data with no feedback loop within Release 1; labeling is inconsistent (Day 1 says *"Predator path,"* Day 3 says *"Inspiration"*)
- **Day 4 twilight loop:** The suspicion ≥ 85 blocked-write jumps back to `day104_4_twilight_ledger_false_dawn` — if atonement and missy_repair are exhausted, the player is stranded
- **Day 3 gate calibration risk:** The jump from ≥30 (Day 2) to ≥45 (Day 3) coincides with the day stacking the most mandatory suspicion-generating events — players managing Anxiety correctly arrive stat-depleted at the steepest gate
- **Chain scenes lack manuscript-loop payoff:** The nine optional character chains terminate at `advance_after_confrontation` without connecting the observed material to Cora's writing project — they function as pure stat dispensers

### Writers' Room & Chief Architect Contributions
The Writers' Room delivered the most complete mechanical documentation in the project: a fully populated storyboard with working node map, stat-gate specification, spine router contract, and nine character chain scenes. The tea crisis and five-way motivation branch demonstrate writers actively designing mechanics, not just writing prose around them. The primary gap: the archetype taxonomy is used as prose texture but how it should be communicated to the player during play remains an open design conversation. The Chief Architect's mechanical infrastructure is production-ready in its core contracts — the `StoryState` class, chain gating API, `PlayerStats` clamping, and `TimeManager` period enum are all correctly implemented and would survive promotion without material rework. The primary architectural debt is the Day 4 twilight loop condition, which the gatekeeper review should have caught.

---

## 4. Historical Accuracy — B+

### Subgrades
| Criterion | Grade |
|---|---|
| Period Accuracy (1891 Savoy) | B+ |
| Class and Social Hierarchy | A− |
| Language and Idiom | B+ |
| Irish Identity and Context | C+ |
| Setting Texture | B |

### Summary
The structural elements are historically sound: the upstairs/downstairs circulation architecture reflects the Savoy's design as a machine for class invisibility, Stern's management register maps to actual hotel housekeeping ideology of the period, and Gideon's Day 5 leverage speech accurately enumerates the institutional gatekeeping available to a wealthy gentleman accused by a female domestic servant in 1891. The line *"A guest's attention is not a promotion"* is the most historically accurate single line in the script.

### Critical Strengths
- **The upstairs/downstairs spatial segregation** — the servants' passage, the forbidden grand staircase, the creaking third board — correctly reflects the Savoy's deliberate architectural separation of service and guest circulation (opened 1889)
- **Gideon's leverage speech** accurately enumerates 1891 institutional power: the Labouchere Amendment (1885) exposure, the asymmetry that makes accusation by a servant radioactive to the accuser
- **Lockbox and photographic evidence** — carte de visite format, hairpin entry, aristocratic overconfidence as a period-specific failure mode — all period-plausible
- **Vance's corrective language** (*"As if obedience were not surrender, but etiquette"*) — acute observation of high-status submission idiom in 1891 social contexts

### Critical Weaknesses
- **"Ms. Vance" is a major anachronism:** The honorific "Ms." did not enter common usage until the 1950s–60s and was not standardised in British usage until the 1970s. In 1891 she would be "Miss Vance" or "Mrs. Vance." This propagates throughout the script and the character database — must be corrected at the source document level
- **"References" vs. "character":** The period term for a servant's testimonial was *"character,"* not "references" — a distinction with legal weight under the Servant's Character Act; the forgery is left without period-specific grounding
- **Literacy benefactor framing is pre-1870:** Board-school education was compulsory from 1870, extended in 1880 — by 1891 a woman of Cora's age would plausibly be literate from childhood schooling, not a benefactor's charity; the dramatic interest is what she *read*, not that she could read
- **Irish identity underworked in prose:** Anti-Irish structural prejudice is ambient (the masquerade mechanics are present) but never rendered in a specific internal beat where Cora's Irish register nearly surfaces — no idiom slips, no consonant dropped, no name almost pronounced wrong
- **Holywell Street absent from the script:** The locations database correctly identifies it; the Obscene Publications Act enforcement, the Society for the Suppression of Vice raids, anonymous payment — these constitute a legal and class-specific survival question the draft treats purely as a moral one

### Victorian Consultant Agent Contribution
The Consultant's influence is demonstrably present in structural elements but inconsistently applied at the line level. The guardrails document is too brief to have prevented the "Ms. Vance" anachronism or the literacy-benefactor problem — both are recurring constraint gaps rather than one-off errors. Most critically, the Consultant has not yet updated `historical_guardrails.md` to codify the lessons this draft raises: correct forms of address for female guests of ambiguous marital status; the "character" vs. "references" distinction; the 1891 literacy baseline; the Holywell Street legal risk profile. Language policing has been applied more rigorously to spoken dialogue than to first-person narration, a gap that must be explicitly closed.

---

## 5. Technical Code Quality — B+

### Subgrades
| Criterion | Grade |
|---|---|
| State Architecture | A |
| Naming Contract Compliance | B |
| Bracket Interpolation Safety | A |
| Speaker Contract | A+ |
| Code Cleanliness & Promotability | B+ |
| Framework Usage (promoted scripts) | A |
| Framework Usage (non-canon draft) | C+ |

### Summary
The promoted runtime scripts (day101–day104) are genuinely excellent: zero direct global state mutations, fully escaped bracket interpolations, and coherent day-flow handoffs. The grade does not reach A territory because `story_chains_non_canon.rpy` contains critical unresolved symbol violations — per-character suspicion attributes that do not exist on `PlayerStats`, and a single-option menu Ren'Py cannot render — that would produce immediate `AttributeError` crashes or runtime failures if promoted without correction.

### Critical Strengths
- **Zero direct state mutations in promoted scripts:** A complete grep of day101–104 finds no bare `story.field =` assignments — only setter calls; the most important invariant in the codebase holds perfectly
- **Bracket interpolation discipline:** Every decorative menu label is correctly double-escaped (`[[Inspiration]]`, `[[Defiance]]`, `[[Corruption]]`) across all promoted files
- **Single-source state instantiation:** `variables.rpy` is exactly three lines — no `default` drift into episodic files
- **Speaker contract: A+** — every dialogue token across all promoted scripts resolves to a defined character in `characters.rpy` without exception
- **Asset manifest infrastructure:** `declare_image_with_fallback` and `register_audio` catch missing assets at init time and degrade gracefully

### Critical Issues & Contract Violations
1. **CRITICAL — `apply_effects()` keyword mismatch in `story_chains_non_canon.rpy`:** The file calls `apply_effects(stern_susp=..., vance_susp=..., missy_susp=...)` throughout `check_confrontations` and all chain scenes. These keyword arguments do not exist in `functions.rpy`. `apply_effects(insp=0, corr=0, susp=0)` accepts only three kwargs — these calls would produce `TypeError` or silently discard all effects. The non-canon draft is built around a per-character suspicion model that the canonical runtime does not implement; resolution requires either (a) a human-authorized schema expansion of `PlayerStats`, or (b) remapping all per-character calls to the unified `susp` parameter.
2. **CRITICAL — `penance_triggered`, `chain_available()`, `resolve_chain_label()`, and character chain-level fields absent from canonical `classes.rpy`:** These are correctly spec'd in `classes_non_canon.rpy` under `# PROMOTE:` comments, but the merge has not been performed. Direct promotion would produce `AttributeError` on first invocation.
3. **MEDIUM — Missing `story.set_day3_night_action("write")` in `day103_3_bedroom_final_write` success path:** The barricade path sets the flag correctly; the write-success path does not — `day3_night_action` silently remains `"none"` on all successful chapter-three completions, corrupting any downstream logic keyed to this field.
4. **MEDIUM — `confrontation_missy` menu has only one option:** Ren'Py requires at least two options in a `menu:` block; a single-option menu displays as a forced non-choice and must be converted to linear narration or given a second branch before promotion.
5. **LOW — Malformed bracket escapes in `sys` game-over strings:** Lines 618, 630, 652 use `[[GAME OVER. ...text...]` — opening `[[` without closing `]]`; the parser will render garbled text. Also: `missy_sprite neutral` and `vance_sprite neutral` are referenced but absent from `assets_manifest.rpy`.

### Chief Architect & Code Agent Contributions
The Chief Architect's architectural foundation is strong — the `StoryState` class, `TimeManager`, `PlayerStats`, and the `functions.rpy` framework API are well-designed, internally consistent, and would survive promotion without rework. The weakness is in gatekeeper enforcement: `story_chains_non_canon.rpy` was authored with a fundamentally different state model (per-character suspicion, penance fields) that contradicts the canonical runtime, yet reached this review without those conflicts being flagged. The architecture for the chain system in `classes_non_canon.rpy` is well-designed — the intent is sound, only the execution gate is missing. The Code Agent's implementation of day101–104 is the clearest strength of this audit: disciplined framework usage, consistent setter-only state updates, correct bracket escaping, and clean day-flow handoffs demonstrate full internalization of the codebase contracts. The one concrete omission (missing `set_day3_night_action("write")` in the success path) reads as a copy-pattern error given the barricade path in the same label sets it correctly.

---

## Cross-Cutting Findings

### What the Agent Team Got Right
The project's most distinctive achievement is that it built a mechanically coherent, literarily ambitious, and historically grounded VN MVP in a single coordinated release cycle. The class-backed state architecture prevents the ad hoc variable sprawl that kills long-running Ren'Py projects; the Voice Guides produce line-level enforceable constraints rather than vague adjective lists; the false-dawn / leverage collapse structure demonstrates writers and architects working from the same thematic brief.

### Systemic Gaps Requiring Attention Before Promotion

| Priority | Issue | Owner |
|---|---|---|
| P0 | Per-character suspicion schema mismatch in chain draft vs. canonical `PlayerStats` | Chief Architect (human authorization required) |
| P0 | `classes_non_canon.rpy` PROMOTE fields not yet merged into `classes.rpy` | Chief Architect |
| P0 | Day 104 twilight dead loop (suspicion ≥ 85 jumps back to same label) | Code Agent |
| P1 | "Ms. Vance" corrected to "Miss Vance" throughout all files | Writers' Room + Victorian Consultant guardrails update |
| P1 | Missing `set_day3_night_action("write")` on success path in day103 | Code Agent |
| P1 | Archetype system communicated to player during play (UI or prose) | Writers' Room + Chief Architect |
| P1 | Missy Voice Guide created | Writers' Room |
| P1 | `confrontation_missy` single-option menu resolved | Code Agent |
| P2 | Prologue expanded with differentiated discovery paths | Writers' Room |
| P2 | Irish register near-surface beat added to internal narration | Writers' Room |
| P2 | Historical guardrails updated with address forms, "character" vs. "references," literacy baseline, Holywell Street risk profile | Victorian Consultant |
| P2 | Missy response scene added on ghost path between Day 102 and Day 105 | Writers' Room |
| P3 | Label naming convention corrected: `day103_2_suite_night_tea` → `day103_5_*` | Code Agent |
| P3 | Malformed `[[...]]` escapes in `story_chains_non_canon.rpy` game-over strings | Code Agent |
| P3 | Missing manifest entries: `missy_sprite neutral`, `vance_sprite neutral` | Chief Architect |

---

*Report generated by the multi-agent review panel. Grades reflect the state of the non-canon draft as of the review date. All P0 and P1 issues must be resolved before any promotion PR to the develop/ branch is opened.*
