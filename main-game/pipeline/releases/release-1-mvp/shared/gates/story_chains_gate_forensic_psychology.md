# Psychology Gate — Forensic Psychology Consultant
# Scope: story_chains (cross-cutting, Days 101–104)
# Release: release-1-mvp
# Contract anchor: day102
# Reviewed: 2026-06-28
# Prerequisite: `story_chains_gate_lead_narrative.md` — **PASS**
# Reference: `story_chains_convergent_report.md` (`code-revision-1`), `cora_character_canon.md`, character voice guides

## Verdict

**PSYCHOLOGICALLY CONSISTENT**

Optional-chain revision resolves the prior mechanical/psychological mismatch (safe paths that still advanced intimacy tracks). Branch logic now matches Cora's survival calculus and stepped escalation across Stern, Missy, and Vance.

## Choice-profile coherence

| Check | Result |
|-------|--------|
| **Abandon vs advance** | **Coherent.** Close Track arms exit without level advance — players who choose caution are not secretly rewarded with deeper optional intimacy. Abandon copy frames tactical withdrawal (Stern: stupidity as armour; Missy: useful trust without entanglement; Vance: forgettable furniture), not moral superiority. Aligns with `cora_character_canon.md` § Survival supremacy / tactical trust. |
| **Charged T1–T2** | **Coherent.** Each advance is a readable step: Stern (intellectual provocation), Missy (pact → shared danger), Vance (voyeur mirror). No option requires corruption or intimacy discontinuous with hotel-layer restraint. |
| **T3 gated climaxes** | **Coherent.** Anxiety/suspicion locks prevent collapse under compound witness pressure — matches composed-under-pressure profile and fail-state design. |
| **Menu captions** | **Coherent.** Tier-specific stakes; no unearned "romance" framing on Missy T1 (explicitly pact, not couple). |

## Character action logic

| Character | Assessment |
|-----------|------------|
| **Cora** | Observer-author using bodies and discipline as material; abandon paths preserve cover; climax paths accept exposure cost for manuscript fuel. Interior lines on penance/spine echo rationalise assignment vs voluntary atonement without self-pity spiral. |
| **Stern** | Discipline ladder reads as sublimated control → confessional heat → inspection ritual. Pulse-check at T2 and kneeling audit at T3 are consistent with `stern_voice_guide.md` (correction as appetite, not confession). |
| **Missy** | T1 solidarity → T2 chosen proximity under threat → T3 authorship betrayal. Sovereign yield at climax matches `missy_voice_guide.md` Path B (agency in vulnerability). Penance exile line ("worse than shouting") supports wounded-trust profile without flattening her to victim. |
| **Vance** | Petulant performance (T1) → humiliation named (T2) → collusion under Gideon shadow (T3). No sympathetic redemption; fear of Gideon remains active. Collusion outcome binds her in shared crime, not alliance. |

## Escalation pacing

| Track | Pacing |
|-------|--------|
| Stern | Posture → language theft → body audit. Heat steps through institutional register, not sudden romance. |
| Missy | Labour pact → danger bond → moral wound (page). Emotional injury at T3 is earned by T1–T2 trust seeds. |
| Vance | Stolen gaze → dominance reversal → key transfer. Voyeurism precedes touch; class mirror intact. |

Tier residue lines (`get_character_chain_level`) support continuity without requiring players to remember stat integers.

## Voice as psychology

- Cora spoken lines remain compressed under authority; charged private beats widen interior sovereignty appropriately.
- Missy shame vocabulary on safe/abandon paths; direct register only after earned intimacy at T3 climax.
- Stern never verbalises desire; improper touch stays framed as duty/audit.
- Vance petulance and performance anxiety present in T1 expanded exchange.

## Carry-forward / profile update

**No mandatory profile or voice-guide edits.**

Documented craft notes for future days (non-blocking):

1. **`*_chain_outcome` flags** — Release 2 may reference `abandoned` vs `climax` in main-spine dialogue beyond current one-line echoes.
2. **Missy `entangled` → penance** — If player reaches confrontation after closet bond without T3 climax, consider a middle interior line (optional scale-S).

## Lead narrative follow-up (resolved)

- Historical linter flag on `missy_chain_1` *cool* → fixed to *lose their heat* before this gate (Victorian may still sweep full file).

## Notes for Victorian Consultant

- Psychology gate cleared. Proceed with idiom/class register sweep on `story_chains_non_canon.rpy` and spine callback lines in Days 102–103.
- Flag if any charged beat language reads too modern for servant–guest boundary (none blocking at psychology layer).

## Resubmission gate

N/A — no `PSYCHOLOGICAL DRIFT`.

## Next pipeline step

Invoke **victorian_consultant** on reviewed files.
