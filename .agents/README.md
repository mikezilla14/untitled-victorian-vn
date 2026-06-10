# `.agents/` — rule and skill library

This folder holds **agent role definitions** (markdown) and **Cursor skills** (thin wrappers). Nothing here executes automatically except what your IDE loads from project rules or skills.

## Entry point

**Always start with the Production Orchestrator** unless you are doing a narrowly scoped task the orchestrator would delegate anyway (e.g. only a historical question → load Victorian consultant directly).

| Entry | File |
|-------|------|
| **Primary (all production tasks)** | [`rules/orchestrator.md`](rules/orchestrator.md) |
| Narrative-only (skip code routing) | [`rules/writers_room.md`](rules/writers_room.md) |
| Repo-wide human index | [`../AGENTS.md`](../AGENTS.md) |

## Folder layout

```
.agents/
  README.md                 ← you are here
  rules/                    ← paste as system prompts
    orchestrator.md         ← router (read-only)
    writers_room.md         ← narrative orchestration
    writers_room/README.md  ← sub-agent index (no duplicate rules)
    *_agent.md / *_consultant.md / divergent_*.md
    dev_bible.md            ← pointer → docs/dev_bible.md
  skills/                   ← Cursor skill discovery (see AGENTS.md table)
    orchestrator/, produce_day/, promote_day/, review_scene/
    revise_narrative/, rewrite_narrative/, implement_spec/, market_review/
    historical_check/, divergent_writer/, convergent_writer/, spiciness_tuner/
    documentation_audit/, dag_tag_update/, storyboard_sync/, daily_standup/
    writer_write_scene/, writer_rewrite_scene/, writer_add_flag/, writer_add_effect/
    writer_add_branch/, writer_write_book/, writer_contract_check/
    writer_log_exception/, writer_status/   ← prose-first Writer's Desk skills
```

## How invocation works

1. Human pastes **`orchestrator.md`** (or a skill that loads it).
2. Human states a natural-language task.
3. Orchestrator selects a **pipeline** (see [`docs/agents/PIPELINE_REFERENCE.md`](../docs/agents/PIPELINE_REFERENCE.md)).
4. For each stage, human pastes the named agent's **full** `rules/<agent>.md` plus artifacts from the prior stage.
   - Helper: `py scripts/agent_next_step.py --pipeline <name> --stage <n>`
5. After file edits, run `scripts/validate.py` or `scripts/orchestrate_review.py` as appropriate.

## Agent registry

| ID | Rule file | Pipeline roles |
|----|-----------|----------------|
| `orchestrator` | `orchestrator.md` | All pipelines (coordinator) |
| `writers_room` | `writers_room.md` | `produce-day`, `revise-narrative`, `rewrite-narrative`, `spice-tune` |
| `divergent_writer` | `divergent_writer_base.md` + `divergent_writer_personas.md` | Sub-agent of writers_room |
| `convergent_writer` | `convergent_writer.md` | Sub-agent of writers_room |
| `lead_narrative_editor` | `lead_narrative_editor.md` | Gates, `canon-update`, `review-scene` |
| `forensic_psychology_consultant` | `forensic_psychology_consultant.md` | Gates, `promote-day`, `canon-update` |
| `victorian_consultant` | `victorian_consultant.md` | Gates, `historical-check`, `canon-update` |
| `spiciness_tuning_agent` | `spiciness_tuning_agent.md` | `spice-tune` |
| `adult_market_reviewer` | `adult_market_reviewer.md` | `market-review` (read-only) |
| `non_prod_code_agent` | `non_prod_code_agent.md` | `produce-day`, `implement-spec`, `dag-tag-update` |
| `scene_direction` | `scene_direction_agent.md` | `produce-day`, `rewrite-narrative`, `revise-narrative`, `spice-tune` (sprite-placement post-process) |
| `prod_code_agent` | `prod_code_agent.md` | `promote-day`, `promote-framework` |
| `chief_architect` | `chief_architect.md` | Code review, promotion validation |
| `gatekeeper_orchestrator` | `gatekeeper_orchestrator.md` | PR / `scripts/gatekeeper.py` |
| `documentation_steward` | `documentation_steward.md` | `documentation-audit`, `storyboard-sync`, `dag-tag-update` downstream reference check |
| `writers_desk` | `writers_desk.md` | Prose-first concierge: routes `writer_*` skills to `produce-day`, `revise-narrative`, `rewrite-narrative`, `implement-spec`; see [`docs/specs/writers-desk-agent-framework.md`](../docs/specs/writers-desk-agent-framework.md) |

Domain permissions: [`.guardrails.yml`](../.guardrails.yml) (enforced by `scripts/gatekeeper.py` when `--agent` is set).

## Gate order (promotion drafts)

On `dayrdd_non_canon.rpy`, always **sequential**:

1. `lead_narrative_editor`
2. `forensic_psychology_consultant`
3. `victorian_consultant`

`review-scene` may run these **in parallel** on existing content; writers' room does not.

## Related docs

- [`docs/agents/GETTING_STARTED.md`](../docs/agents/GETTING_STARTED.md)
- [`docs/agents/PIPELINE_REFERENCE.md`](../docs/agents/PIPELINE_REFERENCE.md)
- [`docs/agents/CONTRACTS.md`](../docs/agents/CONTRACTS.md)
- [`docs/agents/BRANCH_WORKFLOW_CONTRACT.md`](../docs/agents/BRANCH_WORKFLOW_CONTRACT.md)
- [`docs/DOCUMENTATION_CATALOG.md`](../docs/DOCUMENTATION_CATALOG.md) — generated cross-project documentation index
- [`docs/dev_bible.md`](../docs/dev_bible.md) — engineering MVP contract
- [`docs/game_mechanics_bible.md`](../docs/game_mechanics_bible.md) — player-facing mechanics
