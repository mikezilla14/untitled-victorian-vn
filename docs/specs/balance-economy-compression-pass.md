# Balance Economy Compression Pass

**Status:** `draft`  
**Target repo:** `mikezilla14/untitled-victorian-vn`  
**Primary scope:** `main-game/non-prod-game/` economy content and balance tooling  
**Owner:** Technical / systems, with writer-facing contract updates  
**Related spec:** `docs/specs/semantic-balance-profiles-implementation-plan.md`

---

## 1. Purpose

Compress the balance economy down to five retained profile families, using exact per-profile/per-intensity deltas instead of the current broad semantic-scaling model.

This is **not** a new balance framework. The repo already has one. This spec modifies the existing semantic profile system so it becomes smaller, exact, lintable, and harder for writers or tools to bypass.

The current source of truth is:

```text
main-game/draft/releases/planning/balance/effect_profiles.yaml
```

That file currently uses `stat_units`, global `intensities`, and profile definitions such as `safe`, `obedient`, `submissive`, `defiant`, `reckless`, `predatory`, and others. The resolver currently calculates deltas by multiplying a stat unit by an intensity multiplier and an optional scale modifier. That flexibility is now the problem: it creates too many valid deltas, too wide a min/max spread, and too many near-duplicate choice meanings.

This pass makes the balance table deliberately small and boring. The linter becomes the real contract.

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
main-game/draft/releases/planning/balance/bespoke_effect_allowlist.yaml
main-game/draft/releases/planning/balance/reports/balance_economy_compression_migration_report.csv
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

### 2.2 Prod guard: fail closed, do not drift silently

The generator currently writes both non-prod and prod runtime tables by default:

```text
main-game/non-prod-game/game/shared/balance_profiles_non_canon.rpy
main-game/prod-game/game/balance_profiles.rpy
```

This pass must not accidentally break prod, and it must not rely on developers remembering a safe flag forever.

`--non-prod-only` is allowed only as an explicit **migration-mode** command. It is not the long-term architecture.

The generator must fail closed if asked to write prod from a schema v2 profile table while prod still contains inactive profile calls or invalid intensities.

Before writing:

```text
main-game/prod-game/game/balance_profiles.rpy
```

`generate_balance_profiles_rpy.py` must scan prod scripts for inactive profile or invalid intensity references. If any are found, default generation fails with a clear error and points the developer to either:

```bash
py scripts/generate_balance_profiles_rpy.py --non-prod-only
```

or a full prod migration pass.

Fail on prod references to:

```text
safe
obedient
submissive
defiant
reckless
predatory
self_protective
trace
severe
numeric intensity overrides such as 1.4
```

Default generation must either update both targets safely or fail. Silent v1/v2 drift is forbidden.

---

## 3. Target Economy

### 3.1 Defined rows

Only these profile/intensity rows exist in the schema v2 balance table.

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

### 3.2 Migration-mode authoring policy

For this compression pass, migrated non-prod story content may use **standard only**:

```renpy
$ apply_balanced_effect("creative", intensity="standard")
$ apply_balanced_effect("curious", intensity="standard", witness="stern")
$ apply_balanced_effect("transgressive", intensity="standard", witness="vance")
$ apply_balanced_effect("observant", intensity="standard")
$ apply_balanced_effect("deceptive", intensity="standard", witness="missy")
```

The `minor` and `major` rows are real defined rows, but they are locked during migration mode. They exist for later tuning, not for first-pass migration.

### 3.3 Future tuning policy

Minor and major may only be used after the compression pass, and only with an explicit annotation:

```renpy
# [BALANCE intensity-exception: deliberate spike]
$ apply_balanced_effect("transgressive", intensity="major", witness="gideon")
```

The linter must support a mode/config split:

```yaml
allowed_story_intensities:
  migration_pass: ["standard"]
  tuning_pass: ["minor", "standard", "major"]
```

During this pass, the active content mode is `migration_pass`.

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

migration_mode:
  allowed_story_intensities:
    - standard

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
9. Reject `base_witness=True` for active profile calls during this migration pass.

### 5.2 Witness handling: no witness, no risky profile

For this repo, `witness_susp` is not a generic stat. It must become a named witness suspicion delta.

Any active profile row with `witness_susp > 0` requires an explicit valid `witness`.

These calls are invalid and must fail:

```renpy
$ apply_balanced_effect("curious", intensity="standard")
$ apply_balanced_effect("transgressive", intensity="standard")
$ apply_balanced_effect("deceptive", intensity="standard")
```

Valid versions:

```renpy
$ apply_balanced_effect("curious", intensity="standard", witness="stern")
$ apply_balanced_effect("transgressive", intensity="standard", witness="vance")
$ apply_balanced_effect("deceptive", intensity="standard", witness="missy")
```

The resolver and linter must never strip witness suspicion simply because no witness was supplied. That would hand out corruption with no risk and break the economy.

For private, prologue, or untracked scenes, the writer has three valid choices:

1. Use a no-witness profile such as `observant` or `creative`.
2. Add a valid narrative witness if the risk is meant to exist.
3. Use a bespoke effect with an explicit allowlist entry.

Do **not** add a global rumour, paranoia, or ambient suspicion pool in this pass. Hard validation is the MVP-safe fix.

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
BALANCE_MIGRATION_ALLOWED_STORY_INTENSITIES = ("standard",)
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

### 6.1 Migration command

For this task, explicit non-prod-only generation is permitted:

```bash
py scripts/generate_balance_profiles_rpy.py --non-prod-only
```

### 6.2 Default command safety

Default generation must run a prod compatibility scan before writing prod. If prod contains inactive profiles or invalid intensities, default generation must fail before writing either output.

The error should be direct, for example:

```text
Cannot write prod balance_profiles.rpy from schema v2.
Prod contains inactive balance profile calls: safe, obedient, defiant.
Run --non-prod-only for migration mode or migrate prod first.
```

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
apply_balanced_effect("curious", intensity="standard", witness="...")
apply_balanced_effect("transgressive", intensity="standard", witness="...")
apply_balanced_effect("observant", intensity="standard")
apply_balanced_effect("deceptive", intensity="standard", witness="...")
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
base_witness=True
```

### 7.2 Risky profiles require witnesses

For migrated content, these standard profiles require witnesses:

```text
curious
transgressive
deceptive
```

These standard profiles do not require witnesses:

```text
creative
observant
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

Because `curious_standard` now includes witness suspicion, the migration has two safe options:

```renpy
$ apply_balanced_effect("curious", intensity="standard", witness="stern")
```

if a tracked witness is narratively valid, or:

```renpy
$ apply_balanced_effect("creative", intensity="standard")
```

if the beat is private manuscript fuel rather than externally risky snooping.

Do not use `curious` with no witness.

### 10.2 Day 100 parlour entrance

Legacy graph:

```text
apply_effects(corr=15)
```

Current meaning: deliberate eavesdropping / illicit discovery.

If a tracked witness is narratively valid:

```renpy
$ apply_balanced_effect("transgressive", intensity="standard", witness="stern")
```

If no tracked witness is narratively valid, use an allowlisted bespoke exception or remap the beat to `creative_standard` only if the intent is private erotic inspiration rather than risky transgression.

Do not use `transgressive` with no witness.

### 10.3 Day 102 framing Missy

Legacy graph:

```text
apply_effects(vance_susp=0, insp=0, corr=20)
```

Migration:

```renpy
$ apply_balanced_effect("deceptive", intensity="standard", witness="stern")
```

or another valid witness if the scene context supports it.

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

Keep these bespoke with strict reason syntax:

```renpy
# [STATE bespoke: negative_suspicion]
$ apply_effects(stern_susp=-10)
```

Reason: the compressed profile table does not contain negative deltas, and it should not. Negative suspicion is a repair mechanic, not a standard choice reward.

### 10.6 Story chains

The shared story chains are part of the playable non-prod economy and must be included.

Migration rule:

```text
progress_chain with corr 5-10 -> curious_standard or deceptive_standard, with valid witness
climax/spice chain with corr 20 -> transgressive_standard, with valid witness
shed_suspicion chain with negative susp -> bespoke: negative_suspicion
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
risky profile without witness
base_witness=True in migrated active profile calls
direct player stat mutation
unmarked raw apply_effects(...)
malformed bespoke reason
bespoke kwargs that do not match the declared reason
mixed bespoke kwargs without allowlist entry
```

The linter already detects direct player stat assignment and raw `apply_effects(...)` calls. This pass tightens that policy: once the migration is complete, unmarked raw `apply_effects(...)` should fail, not warn.

---

## 12. Bespoke Effect Rules

The old loose marker is no longer enough:

```renpy
# [STATE bespoke]
$ apply_effects(...)
```

Replace it with strict reason syntax:

```renpy
# [STATE bespoke: negative_suspicion]
$ apply_effects(stern_susp=-10)
```

The linter must validate the actual parsed kwargs, not just the comment string.

### 12.1 Allowed bespoke categories

| bespoke reason | allowed kwargs | hard restrictions |
|---|---|---|
| `negative_suspicion` | `stern_susp`, `vance_susp`, `missy_susp`, `gideon_susp` | values must be negative only; no `insp`; no `corr`; no base suspicion |
| `write_spend` | `insp` | must be negative only; no `corr`; no suspicion |
| `fixed_manuscript_reward` | preferably named helper, otherwise allowlisted kwargs only | must be explicitly allowlisted |
| `gate_failure_penalty` | small fixed suspicion only | must be explicitly allowlisted |
| `legacy_exception` | any | forbidden unless listed in the allowlist file |

Remove `recovery_mix` as a general allowed category. It is too vague and too easy to abuse.

### 12.2 Bespoke allowlist

Mixed bespoke numeric effects must appear in:

```text
main-game/draft/releases/planning/balance/bespoke_effect_allowlist.yaml
```

Example:

```yaml
allowed_bespoke_effects:
  day104_missy_repair_partial_truth:
    file: main-game/non-prod-game/game/days/day104_non_canon.rpy
    label: day104_4_missy_repair
    line_hint: tender_romance_path_b_intimacy
    reason: fixed authored repair beat
    allowed_kwargs:
      missy_susp: -25
      vance_susp: 5
      insp: 15
      corr: 10
    expires_after: balance_compression_pass
```

Without a matching allowlist row, mixed bespoke effects fail lint.

---

## 13. Catalogue and Migration Report

Update:

```text
scripts/balance_catalogue.py
```

The live catalogue should represent the current state of the game economy. It must not carry migration archaeology forever.

Do **not** add permanent historical columns such as:

```text
old_raw_call
old_insp_delta
old_corr_delta
old_witness_delta
old_profile
old_intensity
new_profile
new_intensity
migration_reason
bespoke_reason
```

to:

```text
main-game/draft/releases/planning/balance/choice_catalogue.csv
```

Instead, write migration metadata to a separate transient report:

```text
main-game/draft/releases/planning/balance/reports/balance_economy_compression_migration_report.csv
```

Recommended report columns:

```text
source_file
line_number
label
choice_id
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
bespoke_reason
allowlist_id
migration_reason
```

The catalogue validator must compare active profile rows against the exact v2 table, not the old scale-derived resolver.

---

## 14. Authoring Contract Changes

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
Default to standard. Minor/major require explicit balance exception annotation.
Numeric intensity is forbidden.
Inactive profiles are forbidden.
Risky profiles require an explicit valid witness.
Bespoke effects require strict reason syntax and may be linted against an allowlist.
```

---

## 15. Tests

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
curious without witness fails
transgressive without witness fails
deceptive without witness fails
base_witness=True fails for active profile calls
```

Update linter tests for:

```python
standard-only migration mode
minor/major blocked without BALANCE intensity-exception annotation
malformed bespoke marker fails
negative_suspicion with positive value fails
negative_suspicion touching insp/corr fails
write_spend with positive insp fails
mixed bespoke call without allowlist fails
prod generation fails closed when inactive prod references exist
```

---

## 16. Acceptance Criteria

This pass is complete when:

1. `effect_profiles.yaml` uses schema v2 exact deltas.
2. Only `creative`, `curious`, `transgressive`, `observant`, and `deceptive` are active profiles.
3. Only `minor`, `standard`, and `major` are defined intensity names.
4. Migration-mode story content only uses `standard` intensity.
5. All old profiles remain present as inactive metadata or are recorded in a migration appendix.
6. No migrated non-prod story content uses inactive profiles.
7. No migrated non-prod story content uses `minor`, `major`, `trace`, `severe`, or numeric intensity unless the current lint mode explicitly allows it.
8. Risky profiles with `witness_susp > 0` fail without an explicit valid witness.
9. Negative suspicion, write spends, and mixed authored exceptions are marked with strict bespoke reason syntax.
10. Bespoke calls are validated by parsed kwargs, not by comment tags alone.
11. Mixed bespoke calls require `bespoke_effect_allowlist.yaml` entries.
12. `recovery_mix` is not accepted as a generic bespoke reason.
13. `story_chains_non_canon.rpy` is included in the migration and lint scope.
14. `choice_catalogue.csv` regenerates cleanly with exact v2 deltas and no migration-history schema bloat.
15. Migration history is written to `reports/balance_economy_compression_migration_report.csv`.
16. `balance_profile_lint.py` fails inactive profile calls, missing risky witnesses, invalid intensities, and malformed bespoke effects.
17. Resolver tests assert exact values, not scale-derived approximations.
18. Non-prod runs without balance resolver errors.
19. Default generator execution fails closed if prod still contains inactive profile calls or invalid intensities.
20. Prod is not accidentally overwritten with schema v2 tables while prod still contains incompatible calls.

---

## 17. Implementation Order

1. Add schema v2 support to `balance_resolver.py`.
2. Update `effect_profiles.yaml` with exact active rows and inactive legacy rows.
3. Add strict witness validation for risky profiles.
4. Update generator for schema v2.
5. Add prod compatibility scan and fail-closed default generation.
6. Regenerate **non-prod runtime table only** in migration mode unless prod calls are also migrated.
7. Update resolver tests for exact values and failure cases.
8. Add strict bespoke reason parsing and kwargs validation to the linter.
9. Add `bespoke_effect_allowlist.yaml` support.
10. Migrate `main-game/non-prod-game/game/days/*.rpy`.
11. Migrate `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy`.
12. Regenerate `choice_catalogue.csv` without migration-history schema bloat.
13. Generate `reports/balance_economy_compression_migration_report.csv`.
14. Update linter scope and fail rules.
15. Update Writer's Desk, non-prod code agent, and authoring schema.
16. Run validation and produce the migration report.

---

## 18. Design Note

Keep the `apply_balanced_effect -> apply_effects` architecture. Kill the over-flexible multiplier economy.

The new balance table should be small, inspectable, and intentionally constrained. That is the right shape for MVP: fewer valid choices for the authoring tools, clearer stat meaning for the player, and a much smaller surface area for balance drift.

The critical rule is this: comments are not the contract. Parsed effect calls are the contract. The linter must validate what the script actually does.
