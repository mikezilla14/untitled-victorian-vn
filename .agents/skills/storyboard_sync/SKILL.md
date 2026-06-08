# Storyboard Sync

Use this skill after manual or agent-authored `.rpy` rewrites when `story_board.md` needs to be
updated to reflect current script structure.

## What to do

1. Load [`.agents/rules/documentation_steward.md`](../../rules/documentation_steward.md).
2. Read the changed `.rpy` files first. They are the structural source of truth.
3. Read the current storyboard:

```text
narrative/draft/releases/release-1-mvp/planning/story_board.md
```

4. If available, read current graph audit/gap outputs from:

```text
narrative/pipeline/releases/release-1-mvp/graph/
```

5. Update only the affected storyboard sections where practical:

- lineage and workflow references
- story structure diagram
- state/flag tables
- spine/router tables
- confrontation/check entry points
- scene ledger
- graph audit links
- open drift notes or questions

6. Do not edit `.rpy` files. Do not invent labels, routes, gates, or effects that are absent from
   scripts or graph audit evidence.
7. Preserve the "Story Board Lineage & Ownership" header.

```powershell
py scripts/agent_next_step.py --pipeline storyboard-sync --stage 1
```

## Direction of truth

```text
.rpy draft scripts + optional DAG tags
        |
        v
graph manifest / CSVs / audit reports
        |
        v
storyboard drift notes and human documentation updates
```

The storyboard may guide planning, but it is not the machine-readable graph source.
