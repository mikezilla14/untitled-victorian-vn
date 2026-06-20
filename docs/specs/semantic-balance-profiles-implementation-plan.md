# Semantic Balance Profiles — Implementation Plan

**Status:** `active-support` (Phase 7 complete — prod framework promoted)  
**Parent spec:** Semantic Balance Profiles over Existing `apply_effects` Scaffolding  
**Target tree:** `main-game/non-prod-game/` for Phases 1–5; production promotion deferred to Phase 7  
**Owner:** Technical / systems (`non_prod_code_agent`, `chief_architect` for lint/CI)

---

## Phase 0 — Prep and scope lock

| ID | Task | Status | Decision |
|----|------|--------|----------|
| T0.1 | Confirm non-prod-only scope for Phases 1–5 | **Done** | Human confirmed 2026-06-20: Phases 1–5 touch **non-prod only**. No edits to `main-game/prod-game/` until Phase 7 (`promote-framework`). |
| T0.2 | Feature lifecycle registry row | **Done** | See [`feature_lifecycle_registry.md`](../architecture/feature_lifecycle_registry.md) — `semantic-balance-profiles`. |
| T0.3 | Profile→legacy mapping worksheet | **Done** | [`profile_migration_worksheet.md`](../../main-game/draft/releases/planning/balance/profile_migration_worksheet.md) |
| T0.4 | Phase 1 lint severity defaults | **Done** | See [Lint severity policy](#lint-severity-policy) below. |

### Scope lock (T0.1)

```text
Phases 1–5: non-prod sandbox only
  ├── main-game/non-prod-game/game/shared/
  ├── main-game/non-prod-game/game/days/
  ├── main-game/draft/releases/planning/balance/
  ├── scripts/balance_resolver.py (and validation tooling)
  └── NO changes to main-game/prod-game/

Phase 7: production promotion (separate promote-framework pass after non-prod proof)
```

**Rationale:** Resolver, lint, catalogue, and day-script migration must prove out in the balance sandbox before copying to prod. Existing prod `apply_effects(...)` calls remain valid and unchanged until explicit promotion.

### Lint severity policy (T0.4)

| Rule | Phase 1–4 | Phase 5+ |
|------|-------------|----------|
| Direct `player.*` stat mutation | **FAIL** | **FAIL** |
| Unknown profile / intensity / witness | **FAIL** | **FAIL** |
| Witness missing on `witness_susp` profiles | **FAIL** | **FAIL** |
| Raw `apply_effects(...)` without `# [STATE bespoke]` | **WARN** | **FAIL** |
| CSV profile row vs resolver mismatch | **FAIL** (once Phase 4 ships) | **FAIL** |

---

## Architecture

```text
Writer intent → semantic effect profile → resolved apply_effects kwargs → PlayerStats methods
```

**Mutation choke point:** `apply_effects(...)` only. `apply_balanced_effect(...)` resolves; it never mutates.

### File map

| File | Role |
|------|------|
| `main-game/draft/releases/planning/balance/effect_profiles.yaml` | Source of truth (profiles, intensities, stat units) |
| `main-game/non-prod-game/game/shared/balance_profiles_non_canon.rpy` | Generated runtime table + `init -1 python in balance_resolver:` |
| `main-game/prod-game/game/balance_profiles.rpy` | Production runtime table (same YAML source; promoted Phase 7) |
| `scripts/balance_resolver.py` | Canonical Python resolver (lint, CSV, tests) |
| `scripts/generate_balance_profiles_rpy.py` | YAML → non-prod + prod `.rpy` generator with `--check` |
| `main-game/non-prod-game/game/shared/functions_non_canon.rpy` | Global `apply_balanced_effect` wrapper (end of file) |
| `main-game/prod-game/game/functions.rpy` | Production `apply_balanced_effect` wrapper (Phase 7) |

**Init order:** `balance_resolver` at `-1` → `apply_effects` + wrapper at `0` → capture wrap at `999`.

---

## Phase 1 — Resolver scaffolding (no script migration)

- [x] T1.1 `effect_profiles.yaml`
- [x] T1.2 `scripts/balance_resolver.py`
- [x] T1.3 `scripts/generate_balance_profiles_rpy.py`
- [x] T1.4 Global wrapper in `functions_non_canon.rpy`
- [x] T1.5 Unit tests (`scripts/tests/test_balance_resolver.py`)
- [x] T1.6 Generator sync check (`py scripts/generate_balance_profiles_rpy.py --check`)

**Acceptance:** Game runs unchanged; existing `apply_effects` calls work; no prod files touched.

---

## Phase 2 — High-impact branch migration

Target files (non-prod only): `day100`–`day105_non_canon.rpy`. Use [`profile_migration_worksheet.md`](../../main-game/draft/releases/planning/balance/profile_migration_worksheet.md).

- [x] **day100** — 7 branches migrated (2026-06-20)
- [x] **day101** — 24 profiles + 2 bespoke (2026-06-20)
- [x] **day102** — 7 profiles + 3 bespoke (2026-06-20)
- [x] **day103** — 15 profiles + 6 bespoke (2026-06-20)
- [x] **day104** — 4 profiles + 10 bespoke (2026-06-20)
- [x] **day105** — 5 profiles + 2 bespoke (2026-06-20)

**Phase 2 complete** for non-prod day100–day105. Bespoke calls retained for negative suspicion, write spends, and multi-witness recovery mixes.

---

## Phase 3 — Writer's Desk protocol

- [x] `.agents/skills/writer_add_effect/SKILL.md` — semantic profile interview + bespoke exceptions
- [x] `.agents/rules/writers_desk.md` — Stat Delta Protocol + shaping emission rules
- [x] `docs/specs/writers-desk-agent-framework.md` — §9, intent template, worked example
- [x] `docs/contracts/authoring_intent.schema.json` — `semantic_effect` / `bespoke_effect` oneOf
- [x] `.agents/rules/non_prod_code_agent.md` — `apply_balanced_effect` emission from intent

---

## Phase 4 — Catalogue generation

- [x] Extended `choice_catalogue.csv` schema (semantic + base suspicion columns)
- [x] `scripts/balance_catalogue.py` — extract, resolve, validate
- [x] `build_choice_catalogue.py` — script scan + resolver-derived deltas
- [x] Balance report semantic profile checks + usage summary
- [x] `scripts/tests/test_balance_catalogue.py`

---

## Phase 5 — Linter enforcement

- [x] `scripts/validation/balance_profile_lint.py` — profile/witness/intensity FAIL; bespoke WARN until ≥80% migration
- [x] `scripts/balance_profile_lint.py` — CLI wired into `validate.py` for `*_non_canon.rpy`
- [x] `scripts/engineering_compliance.py` — per-character acute/base suspicion direct-write guard
- [x] `scripts/validation/balance_report_impl.py` — script-level lint in semantic profile checks
- [x] `scripts/tests/test_balance_profile_lint.py`

**Policy:** Unmarked raw `apply_effects` promotes WARN → FAIL when profile migration ratio reaches 80% (currently ~73%).

## Phase 6 — Runtime capture and balance proof

- [x] `BalanceCapture.log_balanced_effect` — emits `balanced_effect` JSONL events with profile + resolved kwargs
- [x] `compare_runtime_to_model.py` — rejects rollback-contaminated captures for balance proof; re-validates `balanced_effect` events against resolver
- [x] `scripts/tests/test_compare_runtime_capture.py`
- [x] `debug_captures/README.md` — rollback policy for official matrix captures

**Policy:** Rollback events stay in the JSONL stream for debugging, but balance proof requires forward-only captures unless `--allow-rollback`.

---

## Phase 7 — Production promotion

- [x] `main-game/prod-game/game/balance_profiles.rpy` — generated from `effect_profiles.yaml` (`init -1 python in balance_resolver:`)
- [x] `apply_balanced_effect(...)` in `main-game/prod-game/game/functions.rpy`
- [x] `scripts/generate_balance_profiles_rpy.py` — writes non-prod + prod targets; `--check` validates both
- [x] `.guardrails.yml` — `balance_profiles.rpy` under `episodic_code`

**Scope:** Framework promotion via `promote-framework`. Prod day scripts still use legacy `apply_effects(...)` until per-day `promote-day` passes migrate branches.

---

## Acceptance criteria (spec §21)

- [ ] 1–14 per parent spec — tracked in Phase PRs

---

## Open decisions

| Question | Owner | Default if unresolved |
|----------|-------|----------------------|
| Profile mapping sign-off when resolved ≠ legacy | Lead Editor + systems | Document delta in design_note; rebalance intentional |
| Phase 5 WARN→FAIL flip threshold | Human | ≥80% economy branches migrated |
| Prod file naming | Chief architect | `balance_profiles.rpy` at promotion |
