# Story Chains Convergent Report — code-revision-1

**Pass:** `code-revision-1` (2026-06-28)  
**Brief:** `main-game/draft/releases/release-1-mvp/story_chains_narrative_change_brief.md`  
**Target:** `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy`  
**Personas synthesized:** tension, class, erotic, thematic, mystery (convergent-only pass after API land)

## Revision delta

### Mechanical (prior commit in session)
- `abandon_chain_beat` / `complete_chain_beat(path=)` wired on all chain menus
- Outcome flags + spine/penance query helpers on `StoryState`
- Spine callbacks in `day102_non_canon.rpy`, `day103_non_canon.rpy`

### Prose (this pass)
| Track | Tier differentiation |
|-------|------------------------|
| **Stern** | T1 posture audit → T2 notebook confessional → T3 public kneeling inspection; tier residue via `get_character_chain_level` |
| **Missy** | T1 labour pact → T2 valet-case closet bond → T3 manuscript betrayal climax |
| **Vance** | T1 expanded voyeur exchange + tea-crisis echo → T2 staircase mirror → T3 key collusion |
| **Penance** | Stern = visible marble humiliation; Vance = cold silk/lavender class insult; Missy = social exile |

### Menu copy
- Removed player-facing `2.2 Spice` labels; moved to `[BEAT]` comments
- Safe arms: `Close Track`; charged arms: tier-specific advance labels

### Gates (2026-06-28)
- Lead narrative: **PASS** — `shared/gates/story_chains_gate_lead_narrative.md`
- Forensic psychology: **PSYCHOLOGICALLY_CONSISTENT** — `shared/gates/story_chains_gate_forensic_psychology.md`
- Victorian: **HISTORICALLY_SOUND** — `shared/gates/story_chains_gate_victorian.md`
- Brief: **CLOSED**

### Out of scope (deferred)
- Prod promotion (`classes.rpy`, `story_chains.rpy`)

## MUST FIX checklist status (brief §)

| # | Item | Status |
|---|------|--------|
| 1–4 | Mechanical honesty + outcomes | **Done** (API pass) |
| 5–7 | Dramatic jobs + Vance T1 + time-of-day stakes | **Done** (this pass) |
| 8 | Penance prose distinct | **Done** (this pass) |
| 9 | anxiety_breakdown preserved | **Done** |
| 10–11 | Voice/historical | **Pending gates** |
| 12 | Spine callbacks | **Done** |
| 13 | validate.py | **Run after edit** |
| 14 | Clean artifact | **Done** |

## Handoff

Re-run gates on `story_chains_non_canon.rpy` + touched day spine lines. Promote to prod via `implement-spec` after PASS.
