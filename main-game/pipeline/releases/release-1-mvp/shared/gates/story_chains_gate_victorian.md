# Historical Gate — Victorian Consultant
# Scope: story_chains (cross-cutting, Days 101–104)
# Release: release-1-mvp
# Contract anchor: day102
# Reviewed: 2026-06-28
# Prerequisite: `story_chains_gate_lead_narrative.md` — **PASS**; `story_chains_gate_forensic_psychology.md` — **PSYCHOLOGICALLY_CONSISTENT**
# Policy: `main-game/canon/historical_guardrails.md` (1891 Savoy baseline)

## Verdict

**HISTORICALLY SOUND**

No `MAJOR_VIOLATION`. No mandatory rewrites. `historical_linter.py` clean on all reviewed files after `missy_chain_1` *cool* → *lose their heat* fix.

## Files audited

| File | Linter | Manual audit |
|------|--------|--------------|
| `story_chains_non_canon.rpy` | Clean | Full chain + penance pass |
| `day102_non_canon.rpy` | Clean | Spine callback (`missy_chain_was_abandoned`) |
| `day103_non_canon.rpy` | Clean | Spine callbacks (`stern_chain_spine_echo`, `vance_chain_spine_echo`) |

## Societal audit

| Element | Assessment |
|---------|------------|
| Stern linen-closet / quarters intrusion | Housekeeper authority over maids; private quarters entry period-plausible for discipline |
| Stern marble-step penance (public) | Visible servant humiliation before guests — authentic hierarchy punishment |
| Missy laundry labour + night tubs | Division of labour; shared shift cover as social debt |
| Vance handkerchief / staircase grief | Companion performance of respectability; back-stair privacy |
| Vance cold-silk penance | Class insult via feminine labour — maid washing companion's chemises by hand |
| Gideon shadow (Vance T1/T3) | Patron authority over companion; not egalitarian familiarity |
| Master Suite vacant-room inspection | Transgressive intimacy under guise of audit — dramatically intentional, not normalized |

## Linguistic audit

| Line / pattern | Assessment |
|----------------|------------|
| Cora `Ma'am` / `Miss` / interior register | Correct service forms; no contractions to superiors in new spoken lines |
| Stern clipped institutional commands | Lower-middle authority register — OK |
| Missy sin/shame vocabulary (`God keep us quiet`) | Period-appropriate moral shield per voice guide |
| Vance petulant rage (`vulgar creature`, `potato`) | Class-contempt register — OK |
| `Chubb patent` (Missy T2) | Plausible — Chubb locks widely known by 1891 |
| `electric bulbs` / `electric light` (Vance chains) | Savoy electric installation (1889+) — OK for service/back areas in this build |
| `performance` (literary/narrative sense) | Acceptable in Cora authorial interior |
| Tier-3 blocked menus (`You cannot press further`) | Meta tutorial voice — not historical dialogue; pre-existing UI pattern (non-blocking) |

## Technology & setting

- Laundry copper boilers, gas corridor jets, wax candle fallback in evening suite — consistent with 1891 service hotel.
- No telephones, no anachronistic servant-quarter electric luxuries beyond documented Savoy public/installation context.

## Class & gender

- Cora does not casually familarise with Vance or Stern; charged beats remain transgressive, not normalized cross-class friendship.
- Missy T3 stolen silk chemise — contraband from guest suite; class transgression line appropriate.
- Vance T2 thumb on cheek — dramatic power reversal; not presented as accepted etiquette.

## Optional polish (non-blocking)

| Location | Note |
|----------|------|
| `confrontation_missy` — `closed that track myself` | Borderline modern metaphor in `cora_inner`. If revised later: *closed that door myself* or *chose the safe path myself*. |
| Tier-3 lock messages | Consider diegetic `cora_inner` rewrite in scale-**S** pass (lead narrative note 2). |

## Notes for promotion

- Mirror reviewed prose to `main-game/prod-game/game/story_chains.rpy` verbatim.
- Promote chain API from `classes_non_canon.rpy` to `classes.rpy` before route-matrix P7 capture.

## Resubmission gate

N/A — historical gate clear. Story-chain brief may close; proceed to `implement-spec` / prod promotion.
