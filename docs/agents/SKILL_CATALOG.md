# Skill catalogue (canonical)

**Single index** for skill → agent rule → pipeline → contract. If any other doc disagrees, update the outlier to match this table and [PIPELINE_REFERENCE.md](PIPELINE_REFERENCE.md).

**Sandbox day path (MVP):** `main-game/non-prod-game/game/days/dayNNN_non_canon.rpy`

## How to invoke (any skill)

1. Pick a skill row below (or load the **entry** skill for your lane).
2. Paste the listed **agent rule** as the system prompt (skills load the rule for you).
3. Run the **pipeline** stages in order; use `py scripts/agent_next_step.py --pipeline <id> --stage <n>`.
4. Validate with the listed **contract / command** before handoff or PR.
5. Multi-tool edits: run [`branch_handoff`](../../.agents/skills/branch_handoff/SKILL.md) first.

## Three entry lanes

| Lane | When | Entry skill or rule |
|------|------|---------------------|
| **Technical production** | Code, promotion, technical day draft, architecture | [`orchestrator`](../../.agents/skills/orchestrator/SKILL.md) → `orchestrator.md` |
| **Prose-first (Writer)** | Plain-language scenes, choices, flags — no Ren'Py | Any `writer_*` skill → `writers_desk.md` |
| **Documentation hygiene** | READMEs, specs, catalogue, storyboard doc | [`documentation_audit`](../../.agents/skills/documentation_audit/SKILL.md) → `documentation_steward.md` |

---

## Pipeline skills (1 skill : 1 pipeline)

| Skill | Natural-language trigger (examples) | Agent rule | Pipeline | Contracts / schemas | Validate |
|-------|-------------------------------------|------------|----------|----------------------|----------|
| [`orchestrator`](../../.agents/skills/orchestrator/SKILL.md) | Any production task; routing only | `orchestrator.md` | *(routes)* | Handoff contract | — |
| [`produce_day`](../../.agents/skills/produce_day/SKILL.md) | "Produce day N", "Draft day N" (technical) | `writers_room.md` → … | `produce-day` | `gate_verdict`, convergent report | `validate.py` + `contract_validate.py` |
| [`writer_write_scene`](../../.agents/skills/writer_write_scene/SKILL.md) | "Write the corridor scene…" (plain language) | `writers_desk.md` → … | `writer-author` | `authoring_intent` | `contract_validate.py` |
| [`promote_day`](../../.agents/skills/promote_day/SKILL.md) | "Promote day N to production" | `chief_architect.md` → … | `promote-day` | `promotion_handoff`, gates | `--strict-gates` |
| [`review_scene`](../../.agents/skills/review_scene/SKILL.md) | "Review day N for canon/psych/history" | gate rules (parallel) | `review-scene` | gate verdicts (read-only) | — |
| [`revise_narrative`](../../.agents/skills/revise_narrative/SKILL.md) | Brief OPEN; localized prose repair | `writers_room.md` → … | `revise-narrative` | `narrative_change_brief`, gates | `contract_validate.py` |
| [`rewrite_narrative`](../../.agents/skills/rewrite_narrative/SKILL.md) | "Full rewrite day N afternoon" | `writers_room.md` → … | `rewrite-narrative` | gates, convergent report | `contract_validate.py` |
| [`implement_spec`](../../.agents/skills/implement_spec/SKILL.md) | "Implement spec X" | `non_prod_code_agent.md` → … | `implement-spec` | engineering compliance | `validate.py --profile code` |
| [`market_review`](../../.agents/skills/market_review/SKILL.md) | "F95 review", "market viability" | `adult_market_reviewer.md` | `market-review` | *(read-only)* | — |
| [`spiciness_tuner`](../../.agents/skills/spiciness_tuner/SKILL.md) | "Tune to spice level 3", "hotter/milder" | `spiciness_tuning_agent.md` → … | `spice-tune` | variants in `pipeline/experiments/` | gates if prose changes |
| [`historical_check`](../../.agents/skills/historical_check/SKILL.md) | "Can Cora have X in 1891?" | `victorian_consultant.md` | `historical-check` | historical guardrails | `historical_linter.py` (optional) |
| [`documentation_audit`](../../.agents/skills/documentation_audit/SKILL.md) | "Documentation audit", stale READMEs | `documentation_steward.md` | `documentation-audit` | `documentation_catalog` | `documentation_audit.py --check` |
| [`storyboard_sync`](../../.agents/skills/storyboard_sync/SKILL.md) | "Update storyboard after rewrite" | `documentation_steward.md` | `storyboard-sync` | `story_board.md` (doc) | — |
| [`dag_tag_update`](../../.agents/skills/dag_tag_update/SKILL.md) | "Refresh DAG tags on day 104" | `non_prod_code_agent.md` → steward | `dag-tag-update` | graph manifest | graph audit scripts |

---

## Writer's Desk skills (all load `writers_desk.md` first)

| Skill | Trigger | Routes to pipeline | Contracts |
|-------|---------|-------------------|-----------|
| [`writer_write_scene`](../../.agents/skills/writer_write_scene/SKILL.md) | New scene / day in plain language | `writer-author` | `authoring_intent` |
| [`writer_rewrite_scene`](../../.agents/skills/writer_rewrite_scene/SKILL.md) | Rewrite or revise existing prose | `revise-narrative` or `rewrite-narrative` | `authoring_intent` |
| [`writer_add_flag`](../../.agents/skills/writer_add_flag/SKILL.md) | "Remember if she kept the brooch" | `flag-wiring-only` | `authoring_intent` |
| [`writer_add_effect`](../../.agents/skills/writer_add_effect/SKILL.md) | Stat consequence in emotional terms | via Intent → target pipeline | `authoring_intent` |
| [`writer_add_branch`](../../.agents/skills/writer_add_branch/SKILL.md) | New choice by meaning (Observer/Predator/Prey/Ghost) | via Intent → `revise-narrative` / `writer-author` | `authoring_intent` |
| [`writer_write_book`](../../.agents/skills/writer_write_book/SKILL.md) | Book1 Holywell Street manuscript | `book_writing_engine` | label-based book writing contract |
| [`writer_contract_check`](../../.agents/skills/writer_contract_check/SKILL.md) | Pre-gate advisory review | *(no pipeline)* | `authoring_intent` |
| [`writer_log_exception`](../../.agents/skills/writer_log_exception/SKILL.md) | Log contract override | *(no pipeline)* | `exceptions/contract_exceptions.md` |
| [`writer_status`](../../.agents/skills/writer_status/SKILL.md) | "What's left before ship?" | *(advisory)* | exceptions + gates status |

Desk-owned pipelines: **`writer-author`**, **`flag-wiring-only`**.

---

## Cross-cutting skills (not pipelines)

| Skill | Agent rule | When | Contract / tool |
|-------|------------|------|-----------------|
| [`scene_direction`](../../.agents/skills/scene_direction/SKILL.md) | `scene_direction_agent.md` | After gated prose, before code wrap | `sprite_layout_policy.yaml` · `scene_direction.py` |
| [`check_assets`](../../.agents/skills/check_assets/SKILL.md) | `non_prod_code_agent.md` | Manifest sync before promotion | `assets_manifest.rpy` · `check_assets.py` |
| [`branch_handoff`](../../.agents/skills/branch_handoff/SKILL.md) | `orchestrator.md` (preflight) | Before any multi-tool agent edits | `BRANCH_WORKFLOW_CONTRACT.md` · `agent_git_preflight.py` |
| [`divergent_writer`](../../.agents/skills/divergent_writer/SKILL.md) | `divergent_writer_base.md` + persona | Sub-step of `writers_room` workflow A | spec scripts |
| [`convergent_writer`](../../.agents/skills/convergent_writer/SKILL.md) | `convergent_writer.md` | Sub-step of `writers_room` | convergent report |

**Scene direction hook:** run after gates on `produce-day`, `rewrite-narrative`, `revise-narrative`, `writer-author`, and `spice-tune` when prose changed cast — see PIPELINE_REFERENCE § Scene direction post-process.

---

## Planning & standup skills (chain into pipelines)

| Skill | Agent / doc | Output | Then |
|-------|-------------|--------|------|
| [`daily_standup`](../../.agents/skills/daily_standup/SKILL.md) | standup contract | `daily_standup_report.md` | human triage |
| [`integration_review`](../../.agents/skills/integration_review/SKILL.md) | planning lenses + checklist | `integration_review_report.md` | sprint / promotion planning |
| [`action_from_standup`](../../.agents/skills/action_from_standup/SKILL.md) | `resolve_work_item.py` | spec from `task_registry.json` | pipeline skill above |

---

## Specialist skills (narrow domain)

| Skill | Agent rule | Notes |
|-------|------------|-------|
| [`book_writing_engine`](../../.agents/skills/book_writing_engine/SKILL.md) | book writing rules | Book1 manuscript; context packet plus `book1_block_*` labels |
| [`art_production`](../../.agents/skills/art_production/SKILL.md) | art production rules | Prompt logs, asset cards, `art_fidelity_contract` |

---

## Gate & handoff contracts (all pipelines)

| Artifact | Markdown | JSON schema |
|----------|----------|-------------|
| Gate verdict | `dayrdd_gate_<gate>.md` | `gate_verdict.schema.json` |
| Narrative change brief | `dayrdd_narrative_change_brief.md` | `narrative_change_brief.schema.json` |
| Authoring intent (Desk) | `intents/dayrdd_authoring_intent.md` | `authoring_intent.schema.json` |
| Book1 writing context | optional JSON sidecar | `book_writing_contract.schema.json` |
| Promotion handoff | PR note | `promotion_handoff.schema.json` |
| Profile delta | profile report `.md` | `profile_delta.schema.json` |
| Documentation catalogue | `DOCUMENTATION_CATALOG.md` | `documentation_catalog.schema.json` |

Full detail: [`CONTRACTS.md`](CONTRACTS.md) · [`docs/contracts/README.md`](../contracts/README.md).

---

## Conflict rules (do not mix)

| Do not conflate | Use instead |
|-----------------|-------------|
| `market_review` (read-only F95 viability) | `spiciness_tuner` (change content to level 1–5) |
| `produce_day` (technical, starts at `writers_room`) | `writer_write_scene` → `writer-author` (prose-first, starts at `writers_desk`) |
| `scene_direction` (sprite staging script) | `spice-tune` or narrative pipelines (spice/prose logic) |
| `dag-tag-update` stage 1 (`non_prod_code_agent`) | `storyboard-sync` (`documentation_steward` only) |
| Bare "assess prod" | Ask one lens question first (orchestrator) |
