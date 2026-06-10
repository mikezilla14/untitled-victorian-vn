# Action From Standup

Use when the user points a **code** or **prose** agent at the daily standup report and wants work executed — not just status readout.

**Entry document:** `narrative/draft/releases/release-1-mvp/planning/daily_standup_report.md`  
(or dated: `planning/standups/daily_standup_YYYY-MM-DD.md`)

## What to do

### 1. Read the standup

Open the latest standup report. Human priorities live under **Today's Critical Actions** in the text block. Machine routing lives in **Agent work queue** (JSON).

### 2. Resolve the work packet

Run the resolver (do not guess specs from memory):

```powershell
# Highest-priority item from latest standup
py scripts/resolve_work_item.py --from-standup --next

# Specific backlog id
py scripts/resolve_work_item.py --task N-6

# All queued items
py scripts/resolve_work_item.py --from-standup
```

The output **work packet** lists:

| Field | Use |
|-------|-----|
| `agent_rule` | Load as system prompt |
| `skill_path` | Follow workflow steps |
| `pipeline` / `pipeline_stage` | Chain with `agent_next_step.py` when present |
| `specs` | Read **in order** before editing |
| `files` | Primary edit targets |
| `verify` | Run after edits |

### 3. Route by lane

| Lane | Typical agent | Do |
|------|---------------|-----|
| `prose` | `writers_room`, consultants | Rewrite dialogue/narrative only in allowed paths; never patch `$ apply_effects` blocks |
| `code` | `non_prod_code_agent`, `prod_code_agent` | Scaffold/wire only; copy prose verbatim from approved drafts |
| `gate` | `lead_narrative_editor` + consultants | Write gate verdicts under `narrative/pipeline/.../gates/` |
| `integration` | `non_prod_code_agent` | Systems checklist work in non-prod tree |
| `audit` | `chief_architect`, `documentation_steward` | Read-only review or manifest/docs sync |

If `lane` is `unknown`, search `docs/backlog/mvp_backlog.md` and `planning/mvp_systems_integration_checklist.md`, then stop and ask the human before inventing scope.

### 4. Spec fallback order

When the packet spec list is thin or a path is missing:

1. `docs/backlog/mvp_backlog.md` — section matching `[N-x]` / `[C-x]`
2. `planning/mvp_systems_integration_checklist.md` — matching phase section
3. `docs/specs/README.md` — pick the relevant spec by keyword
4. `narrative/pipeline/releases/release-1-mvp/days/dayNN/specs/` — day sandbox specs if the task is day-scoped
5. `.agents/rules/writers_room.md` or `non_prod_code_agent.md` — contracts for prose vs code boundaries

Never skip reading the packet's `specs` that exist on disk.

### 5. Execute and verify

1. Load the resolved `agent_rule` file.
2. Follow the resolved `skill`.
3. Implement only what the specs + backlog excerpt describe.
4. Run every `verify` command from the packet.
5. Mark the matching checklist `[x]` or note backlog completion in your handoff message.
6. Regenerate standup: `py scripts/daily_standup.py --report`

### 6. Respect blockers

If `blocked_by` is non-empty (e.g. `C-1` blocked by `N-2`), **do not** start the task. Resolve or hand off the blocker first.

## Partner coordination (prose agents)

When `planning/mvp_systems_integration_checklist.md` Partner contract items are unchecked:

- Do **not** rename spine labels or menu branch structure.
- Do **not** edit `$ apply_effects(...)`, `$ story.set_*`, or `complete_manuscript_chapter` lines unless the user explicitly overrides the freeze.

## Registry maintenance

Add or update entries in `docs/backlog/task_registry.json` when new backlog tasks appear so standup items keep resolving automatically.
