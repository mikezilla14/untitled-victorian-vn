# Profile migration worksheet (Phase 2)

**Purpose:** Map legacy `apply_effects(...)` calls to semantic profiles before editing day scripts.  
**Rule:** Map **narrative meaning**, not numeric parity. Resolved values come from `effect_profiles.yaml` via the resolver.  
**Scope:** Non-prod day scripts only (`main-game/non-prod-game/game/days/`).

---

## Profile vocabulary (do not extend without architect review)

| Profile | Typical meaning | Witness required? |
|---------|-----------------|-------------------|
| `safe` | No risk; minimal insp trace | No |
| `observant` | Careful noticing | No |
| `curious` | Snooping / learning; mild corr | No |
| `obedient` | Deference; small corr + insp | No |
| `submissive` | Surrender to authority; corr + insp | No |
| `defiant` | Pushback; insp + witness susp | **Yes** |
| `deceptive` | Lying / misdirection | **Yes** |
| `transgressive` | Rule-breaking; corr + insp | No |
| `reckless` | High corr + insp + witness susp | **Yes** |
| `predatory` | Exploitative power play | **Yes** |
| `self_protective` | Withdrawal / boundaries | No |
| `creative` | Writing / craft focus | No |

**Intensity:** default `"standard"`. Use `"minor"` / `"major"` when the beat is deliberately softer or harsher than a typical choice in that scene.

**Bespoke:** Fixed manuscript rewards or one-off tuning → keep `# [STATE bespoke]` + raw `apply_effects(...)`.

---

## Day 100 — Prologue setup

| Location (approx) | Legacy pattern | Suggested profile | Intensity | Witness | Notes |
|-------------------|----------------|-------------------|-----------|---------|-------|
| Bureau search | `insp=15, corr=10` | `curious` | `major` | — | High curiosity beat |
| Parlour entrance | `corr=15` | `transgressive` | `major` | — | Corruption-forward entry |
| Eager posture | `insp=5` | `observant` | `minor` | — | |
| Desperate posture | `corr=5` | `obedient` | `minor` | — | |
| Why write (money) | `insp=5` | `safe` | `minor` | — | |
| Why write (cataloguer) | `insp=5, corr=5` | `curious` | `minor` | — | |
| Why write (scandal) | `corr=10` | `transgressive` | `standard` | — | |

Archetype seed choices (ghost/prey/predator): **no stat effects** — leave as flag-only.

**Phase 2 migration (2026-06-20):** All seven economy branches converted. Resolved kwargs:

| Choice | Profile | Intensity | Resolved kwargs |
|--------|---------|-----------|-----------------|
| Bureau search | `curious` | `major` | `insp=20, corr=3` |
| Parlour entrance | `transgressive` | `major` | `insp=20, corr=8` |
| Eager posture | `observant` | `minor` | `insp=2` |
| Desperate posture | `obedient` | `minor` | `insp=1, corr=1` |
| Why write (money) | `safe` | `minor` | `insp=1` |
| Why write (cataloguer) | `curious` | `minor` | `insp=5, corr=1` |
| Why write (scandal) | `transgressive` | `standard` | `insp=12, corr=5` |

Careful posture: flag-only (no stat effect). Archetype seeds: unchanged (`apply_archetype_edge` only).

---

## Day 101 — Early shaping (highest density)

| Scene beat | Legacy pattern (examples) | Suggested profile | Witness | Notes |
|------------|---------------------------|-------------------|---------|-------|
| Interview meek | `stern_susp=5, insp=5` | `submissive` | `stern` | Menu: `[[Submit to Stern]]` not numeric |
| Interview competent | `stern_susp=15, insp=10` | `defiant` or `observant` | `stern` | Pick by whether Cora pushes back |
| Stern relation subservient | `stern_susp=5, corr=5` | `obedient` | `stern` | |
| Stern relation resistant | `stern_susp=10, insp=5` | `defiant` | `stern` | |
| Stern relation complicit | `stern_susp=15, insp=10, corr=10` | `transgressive` | `stern` | Consider `major` intensity |
| Vance subservient | `vance_susp=5, insp=5` | `submissive` | `vance` | |
| Vance defiant | `vance_susp=15, insp=10, corr=5` | `defiant` | `vance` | |
| Vance ghostly | `vance_susp=10, insp=10` | `self_protective` | `vance` | Or `observant` if she watches more than hides |
| Corridor predator seed | `insp=10, corr=5` | `predatory` | context | Assign witness to whoever sees the beat |

**Sign-off column (fill during Phase 2 PR):**

| choice_id / line | Profile locked | PR | Resolved kwargs verified |
|------------------|----------------|-----|--------------------------|
| | | | |

---

## Day 102 — Writing readiness

Map write-adjacent choices and corruption/inspiration shaping beats. Manuscript gate **costs** (`attempt_write`, negative insp) stay bespoke — not profile-scaled.

| Beat type | Action |
|-----------|--------|
| Branch that shapes corr/insp before write gate | Profile |
| Fixed write spend / gate check | Bespoke or existing helpers |
| Slop/chastening feedback | Flag-only |

---

## Day 103 — Risky Level 3 route

Focus on choices that materially move corruption_xp or multi-witness suspicion on the optimized path.

---

## Day 104 — Optimized Level 4 route

Focus on corruption-forward branches and anxiety-adjacent suspicion (via witness profiles, not direct anxiety deltas).

---

## Day 105 — Soft-fail reckoning

Convert economy-shaping choices; preserve bespoke beats tied to ending routing.

---

## Per-choice migration checklist

1. Classify intent → profile from table above.  
2. Set `intensity` (default `"standard"`).  
3. Set `witness` if profile includes `witness_susp`.  
4. Replace menu caption — remove hard numbers (spec §13).  
5. Add `# [STATE] Semantic balance profile: <meaning>`.  
6. Run resolver / unit test to record expected kwargs in sign-off column.  
7. Leave intentional fixed values as `# [STATE bespoke]`.

---

## Example after migration

```renpy
menu:
    "Lower your eyes. [[Submit to Stern]]":
        # [STATE] Semantic balance profile: Cora survives by accepting Stern's authority.
        $ apply_balanced_effect("submissive", intensity="standard", witness="stern")
        $ story.set_day1_interview_state("meek")
```

**Do not** expect resolved kwargs to match legacy numbers until balance table tuning is complete.
