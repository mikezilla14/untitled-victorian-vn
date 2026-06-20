# Convergent Decision Report — day100
# Release: Release 1 - MVP
# Pass: editor-revision-1
# Trigger: day100_narrative_change_brief.md (Option B hybrid merge)
# Personas considered: erotic, class, tension, thematic, mystery
# Draft output: main-game/non-prod-game/game/days/day100_non_canon.rpy
# Prior pass: rewrite-narrative-synthesis (2026-06-10 — superseded for discovery/reconvergence prose)

## Revision delta (editor-revision-1)

| Area | Prior draft | This revision |
|------|-------------|---------------|
| Inciting scandal | Sir John / George (master–stableman) | **Lady Eleanor Wiltshire + under-housemaid Margaret** (sapphic, class-coded) |
| Discovery spice | ~2.5 live / 2.8 daydream | **~3.0–3.2 live** (keyhole / letters); **2.8–3.0 daydream** echo |
| Reconvergence | Sir John catches Cora alone | **Lady catches Cora first** → demands expulsion → **Sir John dismisses at wife's behest** |
| Irish erasure | Ambient | **Explicit** Cork-lilt vigilance (main, reconvergence, train, Waterloo) |
| False Dawn | Implicit | **Interior only** after dismissal — secrets may have price someday |
| Exit | Dismissal + Savoy threat | **Unchanged outcome** |
| Mystery hook | Savoy lockbox / Strand in Sir John letter | **Preserved** — Sir John sheet among Lady Eleanor's papers |
| Flags / menus | All three prologue flags | **Preserved** — `prologue_found`, `prologue_holywell_posture`, `prologue_why_write` |
| `# CANON FLAG` | None | **NEEDS HUMAN CONFIRMATION** — Lady Eleanor Wiltshire + Margaret are one-scene Wiltshire NPCs; not yet in `main-game/canon/` |

## 1. Considered (inventory)

| Persona | Focus | Labels |
|---------|-------|--------|
| erotic | Lady + Margaret live discovery; daydream echo | `day100_2_parlour_branch`, `day100_2_desk_branch`, `day100_3_night_daydream` |
| class | Lady's behest; Sir John's dismissal authority; maid speech lock | `day100_2_reconvergence`, `day100_3_arrival` |
| tension | Night crawl; caught sequence; Waterloo spill | `day100_main`, `day100_2_reconvergence`, `day100_3_arrival` |
| thematic | Hypocrisy; Irish erasure; ink as currency (interior) | `day100_main`, `day100_2_reconvergence` |
| mystery | Savoy lockbox / Strand in desk branch | `day100_2_desk_branch` |

## 2. Included (merged into draft)

| Persona | Target label | What changed |
|---------|--------------|--------------|
| erotic | `day100_2_parlour_branch` | Keyhole voyeur beat — Lady Eleanor and Margaret; spice floor 3.0+ |
| erotic | `day100_2_desk_branch` | Lady's explicit letters to Margaret |
| mystery | `day100_2_desk_branch` | Sir John's Savoy lockbox letter slipped under Lady's packet |
| class | `day100_2_reconvergence` | Lady Irish slur → linguistic vigilance; Sir John "My wife is correct" dismissal |
| thematic | `day100_main` | Cork lilt swallowed; English maid mask |
| thematic | `day100_2_reconvergence` | Gendered ruin observation; False-Dawn interior seed (no blackmail) |
| tension | `day100_3_arrival` | Manuscript spill; accent mask at Waterloo |
| erotic | `day100_3_night_daydream` | Branch daydream retuned to Lady/Margaret; posture Holywell tempo preserved |

## 3. Cut (not in draft)

| Idea | Rationale | Disposition |
|------|-----------|-------------|
| Cora blackmails Eleanor for sovereigns + reference | Contradicts `cora_character_canon.md` Breaking Point | Rejected (per brief) |
| Sir John / George scandal | Replaced per brief | Rejected |
| Folding-screen hide beat | Lady catches Cora at bureau post-discovery — cleaner cause chain | Rejected |
| Lady Eleanor / George stableman (donor rewrite) | Wrong scandal geometry | Rejected |

## 4. Structural & canon decisions

- **Spine preserved:** All eight labels; all flag setters; `jump day101_main` handoff unchanged.
- **Balance:** All stat choices use `apply_balanced_effect()` — 7 profile calls, 0 bespoke.
- **Voice lock:** Spoken Cora to Sir John ≤8 words, no contractions (verified at authoring).

## 5. Downstream gate notes

- **Lead Narrative Editor:** Re-review required — prior `day100_gate_lead_narrative.md` (2026-06-10) invalidated.
- **Forensic Psychology:** Verify Lady-first / Sir John-second confrontation; posture menus still map to early-game survival modes; False-Dawn interior does not over-seed Predator before Day 101.
- **Victorian Consultant:** Lady + Margaret sapphic scandal; Irish slur; Margaret's speech to Lady — period register check.

## 6. Validation

- `py scripts/validate.py --profile changed --agent writers_room --skip-gate-checks` — **PASS** (2026-06-20)
