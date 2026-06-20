# Narrative Gate — Lead Narrative Editor
# dayrdd: day100
# Release: release-1-mvp
# Draft: main-game/non-prod-game/game/days/day100_non_canon.rpy
# Reviewed: 2026-06-20
# Reference: day100_narrative_change_brief.md, day100_convergent_report.md (Pass: editor-revision-1), story_board.md

## Verdict

**PASS**

The editor-revision-1 prologue satisfies the Option B hybrid merge brief. Inciting scandal now centres on Lady Eleanor Wiltshire and under-housemaid Margaret; exit condition remains Sir John's dismissal at his wife's behest with Savoy reference under threat. All locked spine flags fire; Cora voice lock holds on spoken lines to Sir John.

## Canon cross-reference

| Check | Result |
|-------|--------|
| Breaking Point (`cora_character_canon.md`) | OK — Absolute dismissal after impropriety proximity; no blackmail exit. |
| Story board spine (labels, menus, flags) | OK — All eight labels through `day101_main`; `prologue_found`, `prologue_why_write`, `prologue_holywell_posture` all set. |
| Irish erasure / performed self | OK — Cork lilt vs flat English mask in main, reconvergence, train, Waterloo. |
| False Dawn foreshadow | OK — Interior only (`day100_2_reconvergence`, lines 289–290); tempered by dismissal, not triumph. |
| Mystery hook | OK — Savoy lockbox / Strand solicitor preserved in desk branch via Sir John's sheet among Lady's papers. |

## Stat-story alignment

- Search choices use `apply_balanced_effect("curious", major)` and `apply_balanced_effect("transgressive", major)`.
- Posture menu: `careful` (no stat), `eager` (`observant` minor), `desperate` (`obedient` minor).
- Why-write menu: `money_home` (`safe` minor), `cataloguer` (`curious` minor), `scandal_hungry` (`transgressive` standard).
- Archetype seed menu unchanged; `apply_archetype_edge` on train.

## Implementation alignment

- Exit via `jump day101_main` after `time_manager.set_current_day(1)` and `set_time_period("Morning")`.
- Approved StoryState setters only; `renpy.block_rollback()` before train transition preserved.

## Voice check

| Character | Assessment |
|-----------|------------|
| Cora (spoken to Sir John) | **Voice lock.** `"There was a draft, sir."` (5), `"They are my pages, sir."` (5), `"Forgive me, sir."` (3), `"I understand, sir."` (3), Waterloo `"Forgive me, sir."` (3) — all ≤8 words, no contractions. |
| Cora (inner) | Hyper-literate, sensory, Irish vigilance; Gap intact under Lady's slur beat. |
| Sir John | Cold authority; performs dismissal validating wife (`"My wife is correct."`). |
| Lady Eleanor | Class venom under panic; one-scene Wiltshire NPC — see editorial note. |

## Editorial notes (non-blocking)

1. **Lady Eleanor + Margaret:** Flagged `NEEDS HUMAN CONFIRMATION` for canon registry — acceptable as one-scene prologue NPCs until human adds to draft bible or canon.
2. **Spice elevation:** Live discovery branches meet brief's ~3.0 marketing floor; reconvergence stays class-tension only (≤2.5 live).
3. **Prior gate (2026-06-10):** Superseded by this revision; Sir John/George scandal removed.

## Resubmission gate

N/A — Approved for forensic psychology gate.
