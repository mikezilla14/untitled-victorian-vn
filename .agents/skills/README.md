# Agent skills

Thin wrappers for Cursor skill picker and human invocation. Each skill loads an agent rule, names a pipeline (or cross-cutting step), and lists contracts/commands.

**Canonical index:** [`docs/agents/SKILL_CATALOG.md`](../../docs/agents/SKILL_CATALOG.md)

## Maintenance (when adding a skill)

1. Add one row to [`SKILL_CATALOG.md`](../../docs/agents/SKILL_CATALOG.md) (skill → agent → pipeline → contract).
2. Add the skill to the category table in [`AGENTS.md`](../../AGENTS.md).
3. Register pipeline stages in [`scripts/agent_next_step.py`](../../scripts/agent_next_step.py) when applicable.
4. Add agent to [`.agents/README.md`](../README.md) if new.
5. Run `py scripts/documentation_audit.py --write`.

## Conflict rules

- One **pipeline skill** maps to exactly one pipeline id (see catalogue).
- **Writer's Desk** skills all load `writers_desk.md` first — never skip to `writers_room` for prose-first intake.
- **`market_review`** is read-only; **`spiciness_tuner`** changes content — do not merge.
- **`scene_direction`** is a post-gate script step — not a narrative pipeline stage id.
