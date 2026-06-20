# Writer: Add Effect

Lets the Writer attach a **stat consequence** to a moment in emotional terms (e.g. "Refusing the
money should sting her inspiration but feed the corruption"). The Desk maps intent to a **semantic
balance profile** — it never asks her for raw numbers and never invents counters.

## What to do

1. Load [`.agents/rules/writers_desk.md`](../../rules/writers_desk.md).
2. Interview the **meaning** of the beat (deference, defiance, snooping, surrender, scandal appetite,
   etc.). Pick a profile from the closed vocabulary in
   [`effect_profiles.yaml`](../../../main-game/draft/releases/planning/balance/effect_profiles.yaml):
   `safe`, `observant`, `curious`, `obedient`, `submissive`, `defiant`, `deceptive`,
   `transgressive`, `reckless`, `predatory`, `self_protective`, `creative`.
3. Set **intensity** only when the beat is deliberately softer or harsher than typical for that scene
   (`trace` | `minor` | `standard` | `major` | `severe`; default `standard`).
4. Set **witness** when the profile raises witness suspicion (`defiant`, `deceptive`, `reckless`,
   `predatory`): `stern` | `vance` | `gideon` | `missy`. Use `base_witness: true` only for durable
   recognition, not momentary heat.
5. Record the semantic shape in **Authoring Intent** (`requested_effects`) — not raw stat deltas.
6. Use **bespoke** (`kind: bespoke` + `deltas` + reason) only when profiles cannot express the beat:
   negative suspicion recovery, write-gate inspiration spends, fixed manuscript rewards, or other
   one-off tuning documented in the migration worksheet.
7. If she asks for a **genuinely new stat or mechanic**, **stop and escalate to**
   [`.agents/rules/chief_architect.md`](../../rules/chief_architect.md) — do not fabricate one.
8. Placement is handled downstream by `non_prod_code_agent` during shaping.

## Authoring Intent shape (preferred)

```yaml
requested_effects:
  - trigger: choice_lower_eyes
    profile: submissive
    intensity: standard
    witness: stern
    base_witness: false
    narrative_meaning: "Cora accepts Stern's authority and learns from surrendering control."
```

## Bespoke shape (exceptional)

```yaml
requested_effects:
  - trigger: ch3_write_spend
    kind: bespoke
    bespoke_reason: write_spend
    deltas:
      insp: -20
    narrative_meaning: "Fixed chapter write cost; not profile-scaled."
```

## Code agent emission

The code agent emits profile effects as:

```renpy
# [STATE] Semantic balance profile: <narrative_meaning>
$ apply_balanced_effect("submissive", intensity="standard", witness="stern")
```

Bespoke effects as:

```renpy
# [STATE bespoke] <reason>
$ apply_effects(insp=-20)
```

## Outputs

- Updated Authoring Intent with semantic `requested_effects`; effects placed in draft (via code agent).

## Reference

- Profile meanings and migration examples:
  [`profile_migration_worksheet.md`](../../../main-game/draft/releases/planning/balance/profile_migration_worksheet.md)
- Implementation plan:
  [`semantic-balance-profiles-implementation-plan.md`](../../../docs/specs/semantic-balance-profiles-implementation-plan.md)
