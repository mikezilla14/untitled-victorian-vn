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

## Active feature inventory

| Feature | Status | Runtime? | Primary files | Agent/process entry | Validation / evidence | Decision |
|---------|--------|----------|---------------|---------------------|-----------------------|----------|
| Manuscript fuel gates | `required-mvp` | Yes | `main-game/non-prod-game/game/shared/functions_non_canon.rpy`, `main-game/non-prod-game/game/shared/classes_non_canon.rpy`, day scripts | `produce_day`, `implement_spec`, `promote_day` | `main-game/draft/releases/planning/mvp_systems_integration_checklist.md` Phase 1 | Keep and verify in playtest matrix. |
| Manuscript progress / chapter completion | `required-mvp` | Yes | day scripts, `book1_non_canon.rpy`, `screens.rpy` | `produce_day`, `writer_write_book`, `promote_day` | MVP checklist Phase 1.3 and Phase 5 | Keep; every write slot must update or intentionally skip progress. |
| Hard fail states | `required-mvp` | Yes | `endings.rpy`, day scripts, `script.rpy`, story chains | `implement_spec`, `promote_day` | MVP checklist Phase 2 and playtest matrix | Keep; must be smoke-tested from `start`. |
| Soft fail / rejection ending | `required-mvp` | Yes | `day105_non_canon.rpy`, `endings.rpy` | `produce_day`, `promote_day` | MVP checklist Phase 2.2 | Keep unless design explicitly replaces it. |
| Story chains | `required-mvp` | Yes | `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy`, day scripts | `produce_day`, `implement_spec`, `review_scene` | MVP checklist Phase 4 | Keep; spine owns jumps, chains return to caller. |
| Penance / confrontation routing | `required-mvp` | Yes | `story_chains_non_canon.rpy`, day scripts | `produce_day`, `implement_spec`, `review_scene` | MVP checklist Phase 4.3 | Keep; verify one confrontation per character across runs. |
| Book1 writing engine | `required-mvp` | Yes | `main-game/non-prod-game/game/days/book1_non_canon.rpy`, write slots, `screens.rpy` | `writer_write_book`, `produce_day`, `promote_day` | MVP checklist Phase 5 | Keep; label-based manuscript prose remains separate from hotel prose. |
| Structural asset manifest / asset checking | `required-mvp` | Yes | `assets_manifest.rpy`, `scripts/check_assets.py`, image/audio folders | `check_assets`, `promote_day` | MVP checklist Phase 6 | Keep; missing files may fallback, but manifest drift must be visible. |
| Scene direction | `active-support` | No direct prose/runtime logic | `scripts/scene_direction.py`, `.agents/rules/scene_direction_agent.md`, `.agents/skills/scene_direction/SKILL.md`, `docs/contracts/sprite_layout_policy.yaml` | `scene_direction`; post-gate hook from prose-changing pipelines | `scene_direction.py --check`; documentation audit link checks | Keep as deterministic post-processor; it only owns `[asset auto]` show/hide lines. |
| DAG tags / graph manifest | `active-support` | No direct runtime logic | `.rpy` `[DAG_*]` comments, `main-game/pipeline/tools/build_story_graph_manifest.py`, graph outputs | `dag_tag_update`, `storyboard_sync` | Graph audit outputs | Keep as audit/balancing support, not as a replacement for storyboard or script structure. |
| Documentation audit/catalogue | `active-support` | No | `scripts/documentation_audit.py`, `docs/DOCUMENTATION_AUDIT.md`, `docs/DOCUMENTATION_CATALOG.md`, `docs/documentation_catalog.json` | `documentation_audit` | `documentation_audit.py --check` | Keep; run after source doc changes. |
| Writer's Desk | `active-support` | No | `.agents/rules/writers_desk.md`, `.agents/skills/writer_*`, authoring intent schemas | Writer-facing entry lane | `authoring_intent` contract validation | Keep; it captures intent and routes, it does not write runtime scripts directly. |
| Daily standup | `optional-dev` | No | `scripts/daily_standup.py`, planning standup reports | `daily_standup` | Human triage | Keep, but non-blocking for ship. |
| Action from standup | `optional-dev` | No | `scripts/resolve_work_item.py`, `docs/backlog/task_registry.json`, `action_from_standup` skill | `action_from_standup` | Human review of selected work item | Keep as a planning accelerator, not default task routing. |
| Market review | `optional-dev` | No | `.agents/rules/adult_market_reviewer.md`, `market_review` skill | `market_review` | Read-only report | Keep read-only; approved changes route through narrative/spice pipelines. |
| Art production skill | `optional-dev` | No direct runtime logic | `.agents/skills/art_production/SKILL.md`, art docs, asset source files | `art_production` | Asset cards / manifest checks | Keep separate from runtime asset validation. |
| ActionEditor (`AEditor`) | `optional-dev` | Dev-only | `main-game/non-prod-game/game/AEditor/` | Manual dev tooling | README boundary | Keep dev-only; not part of player path. |
| Deprecated story routers | `deprecated-retained` | Compatibility only | compatibility labels in story chain / day routing | None for new work | Grep guard: no new `jump end_slot` or `jump advance_after_confrontation` | Retain temporarily; no new calls. |
| Legacy narrative path parser | `deprecated-retained` | No | `scripts/narrative_paths.py` legacy parser and prefixes | Migration/debug only | No new docs should point at legacy paths | Retain until no docs/scripts reference legacy folders. |
| One-off migration scripts | `remove-candidate` | No | `scripts/archive/one_off_migrations/` | None | Archive-only | Keep archived; never route normal agent work through them. |
| Dev debris in image folders | `remove-candidate` | No | generated scratch files under image folders | None | MVP checklist Phase 7.6 | Remove or gitignore in cleanup pass. |

## Rules for adding a feature

1. Add the feature here before or with the implementation PR.
2. Give it one status, one owner/process entry, and one validation signal.
3. If the feature is `experimental`, say what would promote it to `active-support` or `required-mvp`.
4. If the feature is `deprecated-retained`, say what proves it can be removed.

## Current pass-1 notes

- This registry is intentionally conservative: it does not move files or delete legacy compatibility code.
- Physical folder refactoring should wait until path drift and README coverage are stable.
- `scripts/narrative_paths.py` remains the source of truth for active day paths.
