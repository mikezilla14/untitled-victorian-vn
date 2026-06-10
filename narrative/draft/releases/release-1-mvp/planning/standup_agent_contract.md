# Standup → Agent action contract

Use this when pointing **any** code or prose Cursor agent at today's work.

## 1. Point the agent

Paste or @-reference:

```
narrative/draft/releases/release-1-mvp/planning/daily_standup_report.md
```

Add:

> Action the highest-priority item using the action_from_standup skill.

## 2. What the agent must run

```powershell
py scripts/resolve_work_item.py --from-standup --next
```

This returns a **work packet** with specs, files, agent rule, skill, and verify commands.

## 3. Lanes

| You need | Agent rule (typical) | Skill (typical) |
|----------|----------------------|-----------------|
| Prose / rewrite | `writers_room.md` | `rewrite_narrative`, `revise_narrative`, `convergent_writer` |
| Non-prod code | `non_prod_code_agent.md` | `implement_spec` |
| Production promote | `prod_code_agent.md` | `promote_day` |
| Gates only | `lead_narrative_editor.md` | `review_scene` |
| Architecture / assets | `chief_architect.md` | `check_assets`, `documentation_audit` |

## 4. If no spec is listed

Resolver falls back in order: backlog section → integration checklist phase → `docs/specs/README.md` → day pipeline `specs/` folder.

If still ambiguous, the agent must ask — not invent scope.

## 5. Done means

- Verify commands from the packet pass.
- Checklist box marked `[x]` or backlog item noted complete.
- `py scripts/daily_standup.py --report` refreshed.
