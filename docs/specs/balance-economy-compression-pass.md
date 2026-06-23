# Balance Economy Compression Pass

**Status:** `draft`  
**Target repo:** `mikezilla14/untitled-victorian-vn`  
**Primary scope:** `main-game/non-prod-game/` economy content and balance tooling  
**Owner:** Technical / systems, with writer-facing contract updates  
**Related spec:** `docs/specs/semantic-balance-profiles-implementation-plan.md`

---

## 1. Purpose

Compress the balance economy down to the five retained profile families from the approved balance table, using exact per-profile/per-intensity deltas instead of the current broad semantic-scaling model.

This is **not** a new balance framework. The repo already has one. This spec modifies the existing semantic profile system so it becomes smaller, more exact, and easier to balance.

The current source of truth is:

```text
main-game/draft/releases/planning/balance/effect_profiles.yaml
```

That file currently uses `stat_units`, global `intensities`, and profile definitions such as `safe`, `obedient`, `submissive`, `defiant`, `reckless`, `predatory`, and others. The resolver currently calculates deltas by multiplying a stat unit by an intensity multiplier and an optional scale modifier. That flexibility is now the problem: it creates too many valid deltas, too wide a min/max spread, and too many near-duplicate choice meanings.

This pass makes the balance table deliberately small and boring.

---

## 2. Scope

### 2.1 Primary files

Apply this pass to the **full non-prod game economy**:

```text
main-game/non-prod-game/game/days/*.rpy
main-game/non-prod-game/game/shared/story_chains_non_canon.rpy
main-game/draft/releases/planning/balance/effect_profiles.yaml
main-game/draft/releases/planning/balance/choice_catalogue.csv
main-game/draft/releases/planning/balance/profile_migration_worksheet.md
scripts/balance_resolver.py
scripts/generate_balance_profiles_rpy.py
scripts/balance_catalogue.py
scripts/validation/balance_profile_lint.py
scripts/tests/test_balance_resolver.py
scripts/tests/test_balance_catalogue.py
scripts/tests/test_balance_profile_lint.py
docs/contracts/authoring_intent.schema.json
.agents/skills/writer_add_effect/SKILL.md
.agents/rules/writers_desk.md
.agents/rules/non_prod_code_agent.md
docs/specs/semantic-balance-profiles-implementation-plan.md
```

### 2.2 Prod guard

The generator currently writes both non-prod and prod runtime tables by default:

```text
main-game/non-prod-game/game/shared/balance_profiles_non_canon.rpy
main-game/prod-game/game/balance_profiles.rpy
```

This pass must not accidentally break prod.

Use one of these strategies:

1. **Preferred for this pass:** regenerate **non-prod only** and leave prod balance tables untouched until a separate prod promotion pass.
2. Or migrate every existing prod `apply_balanced_effect(...)` call that references inactive profiles or invalid intensities before regenerating prod.

Do not silently regenerate prod while prod still contains old profile calls.

---

## 3. Target Active Economy

Only these profile/intensity rows are active.

| profile | intensity | insp | corr | witness_susp |
|---|---:|---:|---:|---:|
| creative | minor | 2 | 1 | 0 |
| creative | standard | 5 | 3 | 0 |
| creative | major | 12 | 6 | 0 |
| curious | minor | 1 | 2 | 5 |
| curious | standard | 3 | 6 | 10 |
| curious | major | 6 | 12 | 15 |
| transgressive | minor | 0 | 4 | 10 |
| transgressive | standard | 0 | 10 | 15 |
| transgressive | major | 0 | 24 | 25 |
| observant | minor | 1 | 0 | 0 |
| observant | standard | 2 | 0 | 0 |
| observant | major | 5 | 0 | 0 |
| deceptive | minor | 0 | 6 | 5 |
| deceptive | standard | 0 | 8 | 10 |
| deceptive | major | 0 | 20 | 25 |

For this migration pass, non-prod content should use **standard only**:

```renpy
$ apply_balanced_effect("creative", intensity="standard")
$ apply_balanced_effect("curious", intensity="standard", witness="stern")
$ apply_balanced_effect("transgressive", intensity="standard", witness="vance")
$ apply_balanced_effect("observant", intensity="standard")
$ apply_balanced_effect("deceptive", intensity="standard", witness="missy")
```

The `minor` and `major` rows stay active for later hand-tuning, but they should not appear in migrated non-prod story content after this pass.

---

## 4. Replace the Current Scaling Model

### 4.1 Current model

The current YAML uses global units:

```yaml
stat_units:
  insp: 50
  corr: 20
  susp: 100
```

and global intensities:

```yaml
intensities:
  trace: 0.05
  minor: 0.10
  standard: 0.25
  major: 0.40
  severe: 0.60
```

The resolver then multiplies unit × intensity × override scale.

That gives the system too many legal values, including numeric override multipliers. It is elegant, but it is overbuilt for the current three-stat economy.

### 4.2 Required model

Change `effect_profiles.yaml` to a **schema v2 exact-delta table**.

Recommended structure:

```yaml
schema_version: 2

valid_witnesses:
  - stern
  - vance
  - gideon
  - missy

active_intensities:
  - minor
  - standard
  - major

profiles:
  creative:
    active: true
    deltas:
      minor:    { insp: 2,  corr: 1,  witness_susp: 0 }
      standard: { insp: 5,  corr: 3,  witness_susp: 0 }
      major:    { insp: 12, corr: 6,  witness_susp: 0 }

  curious:
    active: true
    deltas:
      minor:    { insp: 1, corr: 2,  witness_susp: 5 }
      standard: { insp: 3, corr: 6,  witness_susp: 10 }
      major:    { insp: 6, corr: 12, witness_susp: 15 }

  transgressive:
    active: true
    deltas:
      minor:    { insp: 0, corr: 4,  witness_susp: 10 }
      standard: { insp: 0, corr: 10, witness_susp: 15 }
      major:    { insp: 0, corr: 24, witness_susp: 25 }

  observant:
    active: true
    deltas:
      minor:    { insp: 1, corr: 0, witness_susp: 0 }
      standard: { insp: 2, corr: 0, witness_susp: 0 }
      major:    { insp: 5, corr: 0, witness_susp: 0 }

  deceptive:
    active: true
    deltas:
      minor:    { insp: 0, corr: 6,  witness_susp: 5 }
      standard: { insp: 0, corr: 8,  witness_susp: 10 }
      major:    { insp: 0, corr: 20, witness_susp: 25 }

  safe:
    active: false
    legacy_spec: { insp: trace }
    migration_hint: observant

  obedient:
    active: false
    legacy_spec: { corr: minor, insp: trace }
    migration_hint: observant_or_deceptive

  submissive:
    active: false
    legacy_spec: { corr: standard, insp: minor }
    migration_hint: curious_or_transgressive

  defiant:
    active: false
    legacy_spec: { insp: standard, witness_susp: minor }
    migration_hint: observant_or_deceptive

  reckless:
    active: false
    legacy_spec: { corr: major, insp: standard, witness_susp: standard }
    migration_hint: transgressive_or_deceptive

  predatory:
    active: false
    legacy_spec: { corr: major, insp: minor, witness_susp: minor }
    migration_hint: transgressive

  self_protective:
    active: false
    legacy_spec: { insp: minor }
    migration_hint: observant
```

Do not keep `trace`, `severe`, or numeric multiplier intensities active.

---

## 5. Resolver Behaviour

Update:

```text
scripts/balance_resolver.py
```

The existing architecture should stay intact:

```text
apply_balanced_effect(...) -> balance_resolver.resolve_balanced_effect(...) -> apply_effects(...)
```

`apply_effects(...)` remains the mutation gateway.

### 5.1 New resolver rules

`resolve_balanced_effect(profile, intensity_override="standard", witness=None, base_witness=False)` must:

1. Load schema v2 exact delta rows.
2. Reject unknown profiles.
3. Reject inactive profiles by default.
4. Reject inactive intensities.
5. Reject numeric intensity overrides.
6. Resolve the exact integer row for `(profile, intensity)`.
7. Return only non-zero kwargs.
8. Map `witness_susp` to the actual repo-specific witness key:
   - `stern_susp`
   - `vance_susp`
   - `gideon_susp`
   - `missy_susp`

### 5.2 Witness handling

For this repo, `witness_susp` is not a generic stat. It must become a named witness suspicion delta.

If a profile row has `witness_susp > 0` and the current scene has a tracked witness, supply `witness`.

Example:

```renpy
$ apply_balanced_effect("deceptive", intensity="standard", witness="stern")
```

resolves to:

```python
{ "corr": 8, "stern_susp": 10 }
```

If there is **no valid tracked witness** in the scene, do not invent one. Resolve only the non-witness part of the effect, and the catalogue should make the missing witness explicit. This is necessary because some prologue or private beats are corrupting but not visible to `stern`, `vance`, `gideon`, or `missy`.

Do not use `base_witness=True` during this pass. Base suspicion and suspicion-repair effects remain bespoke unless explicitly redesigned.

---

## 6. Generator Updates

Update:

```text
scripts/generate_balance_profiles_rpy.py
```

The generated `.rpy` must now include:

```renpy
BALANCE_SCHEMA_VERSION = 2
BALANCE_ACTIVE_INTENSITIES = ("minor", "standard", "major")
BALANCE_VALID_WITNESSES = ("stern", "vance", "gideon", "missy")

BALANCE_PROFILES = {
    "creative": {
        "active": True,
        "deltas": {
            "minor": {"insp": 2, "corr": 1, "witness_susp": 0},
            "standard": {"insp": 5, "corr": 3, "witness_susp": 0},
            "major": {"insp": 12, "corr": 6, "witness_susp": 0},
        },
    },
}
```

The generated runtime resolver must mirror the Python resolver exactly.

### 6.1 Non-prod generation default for this pass

For this task, use:

```bash
py scripts/generate_balance_profiles_rpy.py --non-prod-only
```

Do not run the default generator mode unless prod migration is also complete.

---

## 7. Non-Prod Migration Rule

The current non-prod scripts have already been partially migrated to semantic profiles, and the choice catalogue stores:

```text
effect_profile
effect_intensity
effect_witness
effect_base_witness
effect_resolved_from_profile
resolved delta columns
```

This pass should rewrite existing non-prod economy choices so they only use active standard profiles.

### 7.1 Required migration output

After this pass, migrated non-prod content should only contain:

```renpy
apply_balanced_effect("creative", intensity="standard", ...)
apply_balanced_effect("curious", intensity="standard", ...)
apply_balanced_effect("transgressive", intensity="standard", ...)
apply_balanced_effect("observant", intensity="standard", ...)
apply_balanced_effect("deceptive", intensity="standard", ...)
```

No migrated non-prod story choice should use:

```text
safe
obedient
submissive
defiant
reckless
predatory
self_protective
trace
minor
major
severe
numeric intensity overrides such as 1.4
```

---

## 8. Migration Strength Source

Use the legacy raw graph as the primary old-strength reference where available:

```text
main-game/pipeline/releases/release-1-mvp/graph/release1_effects.csv
```

That file records old raw calls, raw inspiration/corruption/suspicion deltas, source file, and line number.

Use it as the first-pass compression guide because it contains the pre-semantic-migration values such as:

```text
apply_effects(insp=15, corr=10)
apply_effects(corr=15)
apply_effects(stern_susp=15, insp=10, corr=10)
apply_effects(vance_susp=15, insp=10, corr=10)
```

---

## 9. Approximate Mapping Rules

This is a light first pass. Do not try to preserve exact numeric totals.

Use legacy `corruption_delta` as the main strength signal.

| legacy corruption | default new profile |
|---:|---|
| 0 | `observant_standard` or `creative_standard` |
| 1-5 | `creative_standard` or `curious_standard` |
| 6-9 | `curious_standard` or `deceptive_standard` |
| 10+ | `transgressive_standard` unless the beat is clearly a lie/cover-up, then `deceptive_standard` |

### 9.1 Context overrides

Use `creative_standard` for:

```text
writing, imagination, erotic prose, artistic confidence, private inspiration, turning experience into manuscript fuel
```

Use `curious_standard` for:

```text
snooping, reading hidden material, asking dangerous questions, watching forbidden behaviour, following clues
```

Use `transgressive_standard` for:

```text
boundary-crossing, sexual/social rule-breaking, accepting corruption, deliberate moral compromise, power-seeking
```

Use `observant_standard` for:

```text
careful noticing, professional competence, reading the room, restraint, non-corrupt awareness
```

Use `deceptive_standard` for:

```text
lying, hiding evidence, framing someone, performing innocence, manipulating a conversation, using someone as cover
```

---

## 10. Repo-Specific Migration Examples

### 10.1 Day 100 bureau search

Legacy graph:

```text
apply_effects(insp=15, corr=10)
```

Current meaning: snooping through private correspondence.

Migration:

```renpy
$ apply_balanced_effect("curious", intensity="standard")
```

Reason: dangerous knowledge-seeking, not pure transgression.

### 10.2 Day 100 parlour entrance

Legacy graph:

```text
apply_effects(corr=15)
```

Current meaning: deliberate eavesdropping / illicit discovery.

Migration:

```renpy
$ apply_balanced_effect("transgressive", intensity="standard")
```

If no valid tracked witness is present, do not attach `witness`.

### 10.3 Day 102 framing Missy

Legacy graph:

```text
apply_effects(vance_susp=0, insp=0, corr=20)
```

Migration:

```renpy
$ apply_balanced_effect("deceptive", intensity="standard")
```

Reason: the core act is concealment/framing, not simple rule-breaking.

### 10.4 Day 103 surrender / high corruption route

Legacy graph:

```text
apply_effects(vance_susp=15, insp=10, corr=25)
```

Migration:

```renpy
$ apply_balanced_effect("transgressive", intensity="standard", witness="vance")
```

Reason: very high corruption plus visible social/sexual risk.

### 10.5 Suspicion-repair choices

Legacy negative suspicion examples exist across days and chains.

Keep these bespoke:

```renpy
# [STATE bespoke] Suspicion repair / recovery effect.
$ apply_effects(stern_susp=-10)
```

Reason: the compressed profile table does not contain negative deltas, and it should not. Negative suspicion is a repair mechanic, not a standard choice reward.

### 10.6 Story chains

The shared story chains are part of the playable non-prod economy and must be included.

Migration rule:

```text
progress_chain with corr 5-10 -> curious_standard or deceptive_standard
climax/spice chain with corr 20 -> transgressive_standard
shed_suspicion chain with negative susp -> bespoke
```

---

## 11. Linter Changes

The current balance profile linter only targets non-prod day files under:

```text
/non-prod-game/game/days/
```

Change it to include:

```text
main-game/non-prod-game/game/days/*.rpy
main-game/non-prod-game/game/shared/story_chains_non_canon.rpy
```

Exclude debug/test harness files unless they are part of the playable release path.

### 11.1 New linter failures

Fail on:

```text
inactive profile reference
inactive intensity reference
numeric intensity override
missing active profile row
wrong exact delta value
direct player stat mutation
unmarked raw apply_effects(...)
base_witness=True in migrated standard profile calls
```

The linter already detects direct player stat assignment and raw `apply_effects(...)` calls. This pass tightens that policy: once the migration is complete, unmarked raw `apply_effects(...)` should fail, not warn.

Valid bespoke raw calls must keep:

```renpy
# [STATE bespoke]
$ apply_effects(...)
```

Allowed bespoke reasons:

```text
negative_suspicion
write_spend
recovery_mix
fixed_reward
one-off gate cost
```

---

## 12. Catalogue Changes

Update:

```text
scripts/balance_catalogue.py
```

The catalogue already has useful columns:

```text
effect_profile
effect_intensity
effect_witness
effect_base_witness
effect_resolved_from_profile
insp_delta
corr_xp_delta
stern_susp_delta
missy_susp_delta
vance_susp_delta
gideon_susp_delta
stern_base_delta
vance_base_delta
missy_base_delta
gideon_base_delta
design_note
```

Add or derive these fields in the migration report:

```text
old_raw_call
old_insp_delta
old_corr_delta
old_witness_delta
old_profile
old_intensity
new_profile
new_intensity
new_witness
new_insp_delta
new_corr_delta
new_witness_susp_delta
migration_reason
bespoke_reason
```

The catalogue validator must compare active profile rows against the exact v2 table, not the old scale-derived resolver.

---

## 13. Authoring Contract Changes

Update:

```text
docs/contracts/authoring_intent.schema.json
```

Replace the old profile enum with:

```json
"balance_profile": {
  "type": "string",
  "enum": [
    "creative",
    "curious",
    "transgressive",
    "observant",
    "deceptive"
  ]
}
```

Replace the old intensity enum with:

```json
"balance_intensity_name": {
  "type": "string",
  "enum": ["minor", "standard", "major"]
}
```

For Writer's Desk / non-prod authoring, add a policy note:

```text
Default to standard. Minor/major require explicit balance justification.
Numeric intensity is forbidden.
Inactive profiles are forbidden.
```

---

## 14. Tests

Update:

```text
scripts/tests/test_balance_resolver.py
```

Remove tests that assert old profile behaviour such as:

```text
submissive
defiant
reckless
numeric intensity scaling
safe_trace
```

Add tests for exact rows:

```python
creative standard -> {"insp": 5, "corr": 3}
curious standard + witness stern -> {"insp": 3, "corr": 6, "stern_susp": 10}
transgressive major + witness vance -> {"corr": 24, "vance_susp": 25}
observant standard -> {"insp": 2}
deceptive standard + witness missy -> {"corr": 8, "missy_susp": 10}
```

Add failure tests:

```python
safe is inactive
obedient is inactive
reckless is inactive
trace intensity is invalid
severe intensity is invalid
numeric intensity is invalid
unknown witness fails
base_witness=True fails in migrated standard content lint
```

---

## 15. Acceptance Criteria

This pass is complete when:

1. `effect_profiles.yaml` uses schema v2 exact deltas.
2. Only `creative`, `curious`, `transgressive`, `observant`, and `deceptive` are active.
3. Only `minor`, `standard`, and `major` are active intensity names.
4. All old profiles remain present as inactive metadata or are recorded in a migration appendix.
5. No migrated non-prod story content uses inactive profiles.
6. No migrated non-prod story content uses `minor`, `major`, `trace`, `severe`, or numeric intensity.
7. All migrated non-prod economy choices use standard intensity only.
8. Negative suspicion, write spends, and recovery mixes remain marked bespoke.
9. `story_chains_non_canon.rpy` is included in the migration and lint scope.
10. `choice_catalogue.csv` regenerates cleanly with exact v2 deltas.
11. `balance_profile_lint.py` fails inactive profile calls.
12. Resolver tests assert exact values, not scale-derived approximations.
13. Non-prod runs without balance resolver errors.
14. Prod is not accidentally broken by regenerating prod balance tables while prod still contains old profile calls.

---

## 16. Implementation Order

1. Add schema v2 support to `balance_resolver.py`.
2. Update `effect_profiles.yaml` with exact active rows and inactive legacy rows.
3. Update generator for schema v2.
4. Regenerate **non-prod runtime table only** unless prod calls are also migrated.
5. Update tests for exact values.
6. Migrate `main-game/non-prod-game/game/days/*.rpy`.
7. Migrate `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy`.
8. Regenerate `choice_catalogue.csv`.
9. Update linter scope and fail rules.
10. Update Writer's Desk, non-prod code agent, and authoring schema.
11. Run validation and produce the migration report.

---

## 17. Design Note

Keep the `apply_balanced_effect -> apply_effects` architecture. Kill the over-flexible multiplier economy.

The new balance table should be small, inspectable, and intentionally constrained. That is the right shape for MVP: fewer valid choices for the authoring tools, clearer stat meaning for the player, and a much smaller surface area for balance drift.
