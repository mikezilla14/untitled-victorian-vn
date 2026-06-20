# Feature lifecycle registry

This registry is the repo-level answer to: **does this feature still exist, who owns it, and should agents use it by default?**

Use it during documentation audits, standups, promotion prep, and agent routing reviews. It is intentionally human-readable first; scripts may consume it later if needed.

## Status vocabulary

| Status | Meaning | Default agent behaviour |
|--------|---------|-------------------------|
| `required-mvp` | Required before the current MVP can be called structurally complete. | Route through the normal production pipeline and validate. |
| `active-support` | Supports authoring, review, promotion, or QA but is not itself a player-facing MVP feature. | Use when the owning process calls for it. |
| `optional-dev` | Useful development or planning convenience. | Do not assume it is required for ship. |
| `experimental` | Exploration or prototype. | Do not route through it unless the user explicitly asks. |
| `deprecated-retained` | Compatibility or historical support only. | Do not use in new code; preserve only until removal criteria are met. |
| `remove-candidate` | Safe candidate for archive or deletion after one audit cycle. | Do not use. |

## Required lifecycle gates

Every new feature, system, agent, or sizeable process document must pass through this registry.

| Gate | Required answer |
|------|-----------------|
| **Add** | What feature exists, where does it live, and which status does it start with? |
| **Wire** | Which process or agent may invoke it? What validation proves it is safe? |
| **Review** | Does it still match current repo structure, MVP scope, and agent routing? |
| **Promote / demote** | Should it become required, remain support-only, become optional, or be deprecated? |
| **Remove / archive** | What evidence proves no current process depends on it? |

## Active process menu

The everyday agent menu should stay small. Features below may be numerous, but day-to-day routing should normally collapse to these processes.

| Human wants to... | Default process | Lifecycle expectation |
|-------------------|-----------------|----------------------|
| Write or change prose | Writer's Desk → `writer-author`, `revise-narrative`, or `rewrite-narrative` | Any new flags/effects are captured in Authoring Intent before code wiring. |
| Implement or wire a system | Orchestrator → `implement-spec` | Feature row must exist or be added in this registry. |
| Promote draft to runtime | `promote-day` or `promote-framework` | Required-MVP and active-support features must have validation evidence. |
| Check readiness | MVP checklist + validation scripts | Registry statuses should match actual checklist and test evidence. |
| Clean docs/process drift | `documentation-audit` | Documentation steward updates this registry before regenerating catalogues. |

## Active feature inventory

| Feature | Status | Runtime? | Primary files | Agent/process entry | Validation / evidence | Decision / next review |
|---------|--------|----------|---------------|---------------------|-----------------------|------------------------|
| Manuscript fuel gates | `required-mvp` | Yes | `main-game/non-prod-game/game/shared/functions_non_canon.rpy`, `main-game/non-prod-game/game/shared/classes_non_canon.rpy`, day scripts | `produce_day`, `implement_spec`, `promote_day` | `main-game/draft/releases/planning/mvp_systems_integration_checklist.md` Phase 1 | Keep. Next review: confirm all player write slots use the same gate semantics. |
| Manuscript progress / chapter completion | `required-mvp` | Yes | day scripts, `book1_non_canon.rpy`, `screens.rpy` | `produce_day`, `writer_write_book`, `promote_day` | MVP checklist Phase 1.3 and Phase 5 | Keep. Next review: verify every successful write has progress, feedback, and failure routing. |
| Hard fail states | `required-mvp` | Yes | `endings.rpy`, day scripts, `script.rpy`, story chains | `implement_spec`, `promote_day` | MVP checklist Phase 2 and playtest matrix | Keep. Next review: smoke-test dismissed/deadline endings from `start`. |
| Soft fail / rejection ending | `required-mvp` | Yes | `day105_non_canon.rpy`, `endings.rpy` | `produce_day`, `promote_day` | MVP checklist Phase 2.2 | Keep. Next review: ensure cautious playthrough feedback points to life-experience/writing-quality cause. |
| Story chains | `required-mvp` | Yes | `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy`, day scripts | `produce_day`, `implement_spec`, `review_scene` | MVP checklist Phase 4 | Keep. Next review: confirm chains return to caller and spine owns time progression. |
| Penance / confrontation routing | `required-mvp` | Yes | `story_chains_non_canon.rpy`, day scripts | `produce_day`, `implement_spec`, `review_scene` | MVP checklist Phase 4.3 | Keep. Next review: verify one confrontation per character across intended runs. |
| Book1 writing engine | `required-mvp` | Yes | `main-game/non-prod-game/game/days/book1_non_canon.rpy`, write slots, `screens.rpy` | `writer_write_book`, `produce_day`, `promote_day` | MVP checklist Phase 5 | Keep. Next review: validate label-based manuscript prose remains separate from hotel prose. |
| Structural asset manifest / asset checking | `required-mvp` | Yes | `assets_manifest.rpy`, `scripts/check_assets.py`, image/audio folders | `check_assets`, `promote_day` | MVP checklist Phase 6 | Keep. Next review: missing structural UI/audio assets must be manifest-visible before ship. |
| Testing and balance framework | `required-mvp` | Non-prod capture harness only | `scripts/balance_report.py`, `main-game/pipeline/tools/{build_grain_manifest,build_choice_catalogue,simulate_balance,compare_runtime_to_model}.py`, `balance_model.py`, `main-game/non-prod-game/game/shared/debug_run_capture.rpy`, `screens.rpy` (debug overlay), `main-game/draft/releases/planning/balance/`, `main-game/pipeline/releases/release-1-mvp/{grain,balance,reports,qa}/` | `chief_architect`, documentation steward | `py scripts/balance_report.py --release release-1-mvp`; `py main-game/pipeline/tools/simulate_balance.py --release release-1-mvp`; non-prod F10 overlay + JSONL under `debug_captures/` | Keep. **Implemented:** static report, grain manifest, choice catalogue, abstract simulator, JSONL capture harness (2026-06-20). Next review: P1–P7 playtest captures + runtime/model comparison. |
| Semantic balance profiles | `active-support` | Non-prod sandbox + prod resolver framework | `effect_profiles.yaml`, `choice_catalogue.csv`, `scripts/balance_resolver.py`, `scripts/balance_catalogue.py`, `scripts/validation/balance_profile_lint.py`, `scripts/generate_balance_profiles_rpy.py`, `build_choice_catalogue.py`, `balance_profiles_non_canon.rpy`, `balance_profiles.rpy`, `authoring_intent.schema.json`, Writer's Desk skills/rules | `implement-spec`, `non_prod_code_agent`, `prod_code_agent`, `writer_add_effect`, `balance_report.py` | `py scripts/generate_balance_profiles_rpy.py --check`; `py scripts/balance_profile_lint.py`; `py main-game/pipeline/tools/build_choice_catalogue.py --check`; `py main-game/pipeline/tools/compare_runtime_to_model.py`; `py -m pytest scripts/tests/test_balance_profile_lint.py scripts/tests/test_balance_catalogue.py scripts/tests/test_compare_runtime_capture.py scripts/tests/test_balance_resolver.py`; `py scripts/balance_report.py` | **Phases 1–7 complete (2026-06-20):** prod `balance_profiles.rpy` + `apply_balanced_effect` promoted; day script migration remains per `promote-day`. |
| Scene direction | `active-support` | No direct prose/runtime logic | `scripts/scene_direction.py`, `.agents/rules/scene_direction_agent.md`, `.agents/skills/scene_direction/SKILL.md`, `docs/contracts/sprite_layout_policy.yaml` | `scene_direction`; post-gate hook from prose-changing pipelines | `scene_direction.py --check`; documentation audit link checks | Keep. Next review: confirm no manual staging is overwritten and four-character overflow is surfaced. |
| DAG tags / graph manifest | `active-support` | No direct runtime logic | `.rpy` `[DAG_*]` comments, `main-game/pipeline/tools/build_story_graph_manifest.py`, graph outputs | `dag_tag_update`, `storyboard_sync` | Graph audit outputs | Keep. Not a second storyboard; use to confirm implementation-level structure. |
| Documentation audit/catalogue | `active-support` | No | `scripts/documentation_audit.py`, `docs/DOCUMENTATION_AUDIT.md`, `docs/DOCUMENTATION_CATALOG.md`, `docs/documentation_catalog.json` | `documentation_audit` | `documentation_audit.py --check` | Keep. Documentation steward must update this registry before regenerating catalogue/audit files. |
| Feature lifecycle registry | `active-support` | No | `docs/architecture/feature_lifecycle_registry.md` | `documentation_audit`, `daily_standup`, `chief_architect` | Human review plus documentation audit | Keep. This is the source of truth for feature status/deprecation decisions. |
| Active path contract | `active-support` | No | `docs/architecture/path_contract.md`, `scripts/narrative_paths.py` | Documentation steward, chief architect | Documentation audit plus grep for stale path patterns | Keep. Use as human-readable companion to `scripts/narrative_paths.py`. |
| Active processes guide | `active-support` | No | `docs/architecture/active_processes.md` | Orchestrator, documentation steward | Human routing review | Keep. Update when the everyday agent menu changes. |
| Scripts refactor map | `active-support` | No | `docs/architecture/scripts_refactor_map.md`, `scripts/README.md` | Chief architect, documentation steward | Documentation audit plus wrapper-backed migration checks | Keep. Use as migration contract before any physical `scripts/` move. |
| Writer's Desk | `active-support` | No | `.agents/rules/writers_desk.md`, `.agents/skills/writer_*`, authoring intent schemas | Writer-facing entry lane | `authoring_intent` contract validation | Keep. It captures intent and routes; it does not write runtime scripts directly. |
| Daily standup | `optional-dev` | No | `scripts/daily_standup.py`, planning standup reports | `daily_standup` | Human triage | Keep, but non-blocking for ship. Any task it surfaces must route through an active process. |
| Action from standup | `optional-dev` | No | `scripts/resolve_work_item.py`, `docs/backlog/task_registry.json`, `action_from_standup` skill | `action_from_standup` | Human review of selected work item | Keep as a planning accelerator, not default task routing. |
| Market review | `optional-dev` | No | `.agents/rules/adult_market_reviewer.md`, `market_review` skill | `market_review` | Read-only report | Keep read-only. Approved changes route through narrative/spice pipelines. |
| Art production skill | `optional-dev` | No direct runtime logic | `.agents/skills/art_production/SKILL.md`, art docs, asset source files | `art_production` | Asset cards / manifest checks | Keep separate from runtime asset validation. Runtime assets still validate through manifest/check-assets. |
| ActionEditor (`AEditor`) | `optional-dev` | Dev-only | `main-game/non-prod-game/game/AEditor/` | Manual dev tooling | README boundary | Keep dev-only. Not part of player path or normal agent route. |
| Deprecated story routers | `deprecated-retained` | Compatibility only | compatibility labels in story chain / day routing | None for new work | Grep guard: no new `jump end_slot` or `jump advance_after_confrontation` | Retain temporarily. Removal requires proof no current day jumps to them. |
| Legacy narrative path parser | `deprecated-retained` | No | `scripts/narrative_paths.py` legacy parser and prefixes | Migration/debug only | No new docs should point at legacy paths | Retain until docs/scripts no longer reference `narrative/`, `renpy_project/`, or old non-prod path forms. |
| One-off migration scripts | `remove-candidate` | No | `scripts/archive/one_off_migrations/` | None | Archive-only | Keep archived. Never route normal agent work through them. |
| Dev debris in image folders | `remove-candidate` | No | generated scratch files under image folders | None | MVP checklist Phase 7.6 | Remove or gitignore in cleanup pass after confirming nothing is manifest-referenced. |

## Rules for adding a feature

1. Add the feature here before or with the implementation PR.
2. Give it one status, one owner/process entry, and one validation signal.
3. If the feature is `experimental`, say what would promote it to `active-support` or `required-mvp`.
4. If the feature is `deprecated-retained`, say what proves it can be removed.
5. If the feature is `remove-candidate`, do not delete it in the same PR that first marks it removable unless the human explicitly approves removal.

## Documentation steward checklist

When running `documentation-audit`, the steward must check this registry before regenerating catalogue/audit outputs:

- New feature/spec/agent exists but no row here → add row or mark `NEEDS HUMAN CONFIRMATION`.
- Registry row points to missing files → fix row or route to `chief_architect` if implementation moved.
- Registry says `required-mvp` but checklist/test evidence is missing → leave status, add next-review note.
- Registry says `optional-dev`, `experimental`, or `deprecated-retained` but an active process routes through it by default → escalate to human.
- Registry says `remove-candidate` and no process references it after one audit cycle → propose archive/delete PR.

## Current pass-4 notes

- This pass updates stale non-prod project documentation and adds an active path contract.
- It still does not physically move scripts or patch large generated/reference files by risky hand reconstruction.
- `scripts/narrative_paths.py` remains the implementation source of truth for active paths.
- Remaining stale path mentions in large docs should be fixed by local documentation-steward regeneration or careful local patching.
