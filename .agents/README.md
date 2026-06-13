# `.agents/` — rule and skill library



This folder holds **agent role definitions** (markdown) and **Cursor skills** (thin wrappers). Nothing here executes automatically except what your IDE loads from project rules or skills.



## Entry points (three lanes)



| Lane | Rule file | Skill index |

|------|-----------|-------------|

| **Technical production** | [`rules/orchestrator.md`](rules/orchestrator.md) | [`orchestrator`](../.agents/skills/orchestrator/SKILL.md) |

| **Prose-first (Writer)** | [`rules/writers_desk.md`](rules/writers_desk.md) | [`SKILL_CATALOG.md`](../docs/agents/SKILL_CATALOG.md) § Writer's Desk |

| **Documentation hygiene** | [`rules/documentation_steward.md`](rules/documentation_steward.md) | [`documentation_audit`](../.agents/skills/documentation_audit/SKILL.md) |



Narrow bypass: historical question only → [`victorian_consultant.md`](rules/victorian_consultant.md) + [`historical_check`](../.agents/skills/historical_check/SKILL.md).



Repo-wide index: [`../AGENTS.md`](../AGENTS.md) · Skill catalogue: [`../docs/agents/SKILL_CATALOG.md`](../docs/agents/SKILL_CATALOG.md)



## Folder layout



```

.agents/

  README.md                 ← you are here

  rules/                    ← paste as system prompts

    orchestrator.md         ← technical router (read-only)

    writers_desk.md         ← prose-first entry

    documentation_steward.md

    writers_room.md         ← narrative orchestration

    writers_room/README.md  ← sub-agent index

    *_agent.md / *_consultant.md / divergent_*.md

  skills/                   ← one skill per callable workflow (see SKILL_CATALOG.md)

```



## How invocation works



1. Pick lane → load entry rule or skill (see [`SKILL_CATALOG.md`](../docs/agents/SKILL_CATALOG.md)).

2. State task in plain language.

3. Run pipeline stages; helper: `py scripts/agent_next_step.py --pipeline <name> --stage <n>`

4. Paste each stage agent's **full** `rules/<agent>.md` + prior artifacts.

5. After gated prose (if staged scenes): [`scene_direction`](../.agents/skills/scene_direction/SKILL.md) post-process.

6. Validate: `scripts/validate.py` / `scripts/orchestrate_review.py`



**Sandbox day path:** `narrative/draft/releases/<release>/non_prod_renpy_project/game/days/dayrdd_non_canon.rpy`



## Agent registry



| ID | Rule file | Pipeline roles |

|----|-----------|----------------|

| `orchestrator` | `orchestrator.md` | Routes all technical pipelines |

| `writers_desk` | `writers_desk.md` | Entry → `writer-author`, `revise-narrative`, `rewrite-narrative`, `flag-wiring-only` |

| `writers_room` | `writers_room.md` | `produce-day`, `writer-author`, `revise-narrative`, `rewrite-narrative`, `spice-tune` |

| `documentation_steward` | `documentation_steward.md` | `documentation-audit`, `storyboard-sync`, `dag-tag-update` stage 2 |

| `divergent_writer` | `divergent_writer_base.md` + personas | Sub-agent of `writers_room` |

| `convergent_writer` | `convergent_writer.md` | Sub-agent of `writers_room` |

| `lead_narrative_editor` | `lead_narrative_editor.md` | Gates, `canon-update`, `review-scene` |

| `forensic_psychology_consultant` | `forensic_psychology_consultant.md` | Gates, `promote-day`, `canon-update` |

| `victorian_consultant` | `victorian_consultant.md` | Gates, `historical-check`, `canon-update` |

| `spiciness_tuning_agent` | `spiciness_tuning_agent.md` | `spice-tune` |

| `adult_market_reviewer` | `adult_market_reviewer.md` | `market-review` (read-only) |

| `non_prod_code_agent` | `non_prod_code_agent.md` | `produce-day`, `writer-author`, `implement-spec`, `dag-tag-update`, `flag-wiring-only` |

| `scene_direction` | `scene_direction_agent.md` | Cross-cutting post-process (not a pipeline id) |

| `prod_code_agent` | `prod_code_agent.md` | `promote-day`, `promote-framework` |

| `chief_architect` | `chief_architect.md` | Code review, promotion validation |

| `gatekeeper_orchestrator` | `gatekeeper_orchestrator.md` | PR / `scripts/gatekeeper.py` |



Domain permissions: [`.guardrails.yml`](../.guardrails.yml)



## Gate order (promotion drafts)



On sandbox `dayrdd_non_canon.rpy`, always **sequential**:



1. `lead_narrative_editor`

2. `forensic_psychology_consultant`

3. `victorian_consultant`



`review-scene` runs these **in parallel** on existing content.



## Related docs



- [`docs/agents/SKILL_CATALOG.md`](../docs/agents/SKILL_CATALOG.md) — **canonical** skill → pipeline map

- [`docs/agents/GETTING_STARTED.md`](../docs/agents/GETTING_STARTED.md)

- [`docs/agents/PIPELINE_REFERENCE.md`](../docs/agents/PIPELINE_REFERENCE.md)

- [`docs/agents/CONTRACTS.md`](../docs/agents/CONTRACTS.md)


