# Active processes

This document is the short operational menu for everyday work. It keeps the agent system from becoming a pile of individually plausible but overlapping lanes.

For feature status and deprecation decisions, use [`feature_lifecycle_registry.md`](feature_lifecycle_registry.md).

## Default menu

| Need | Use | Do not use |
|------|-----|------------|
| Write or revise prose from plain language | Writer's Desk, then `writer-author`, `revise-narrative`, or `rewrite-narrative` | Direct code-agent prose edits |
| Implement approved sandbox mechanics/specs | Orchestrator → `implement-spec` | Ad hoc edits that bypass contracts |
| Promote draft/runtime work | `promote-day` or `promote-framework` | Manual copy without promotion handoff |
| Review readiness | MVP checklist, validation scripts, gates, and route matrix evidence | Subjective “looks good” review only |
| Clean documentation/process drift | `documentation-audit` | Manual doc edits without registry/catalogue follow-up |

## Process ownership

| Process | Owner | Writes | Must check |
|---------|-------|--------|------------|
| Writer's Desk | `writers_desk` | Authoring intents and contract exceptions | Existing pipeline routes and feature registry if new flags/effects are introduced |
| Writers' Room | `writers_room` and sub-agents | Non-canon prose and pipeline artifacts | Gates, context firewall, authoring intent |
| Non-prod implementation | `non_prod_code_agent` | Sandbox `.rpy` and approved non-prod code | `scripts/narrative_paths.py`, contracts, feature registry |
| Scene direction | `scene_direction` | `[asset auto]` show/hide lines only | Sprite layout policy and manual staging locks |
| Promotion | `chief_architect` + `prod_code_agent` | Production day/framework files | MVP checklist, gates, validation, promotion handoff |
| Documentation hygiene | `documentation_steward` | Docs, READMEs, catalogues/audits | Feature lifecycle registry before catalogue regeneration |
| Planning standup | `daily_standup` / `action_from_standup` | Daily automated check reports | Live validation only; routes failures to active processes |
| Integration review | `integration_review` | Weekly/ad-hoc planning reports | Checklist, backlog, specialist grades — not daily |

## Feature creation rule

A new feature is not “real” until it has all four of these:

1. **Location:** the concrete files or folders where it lives.
2. **Owner:** which agent/process may touch it.
3. **Validation:** how to prove it still works or is safe to use.
4. **Lifecycle status:** a row in `feature_lifecycle_registry.md`.

No feature should live only in a conversation, one commit message, or a one-off spec.

## Deprecation rule

Do not delete a built feature merely because it looks unused. First mark it as `deprecated-retained` or `remove-candidate` in the registry, then prove one of these:

- no active process routes through it;
- no current runtime/day script references it;
- a newer feature has replaced it and the replacement is documented;
- the human explicitly approves removal.

## Folder refactor rule

Folder movement should be a separate pass after process drift is stable.

Before moving files:

1. Update or confirm `scripts/narrative_paths.py`.
2. Update docs and READMEs.
3. Preserve wrappers or compatibility imports for scripts used by agents.
4. Run documentation audit and changed-file validation.
5. Keep prose-writing ergonomics intact; do not turn day prose into over-modular system calls merely to satisfy tooling.
