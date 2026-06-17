# DAG Tag Update

Use this skill when the user asks to add, refresh, recreate, audit, or repair `[DAG_*]`
comments in non-canon Ren'Py draft files.

## What to do

1. Load [`.agents/rules/non_prod_code_agent.md`](../../rules/non_prod_code_agent.md).
2. Treat `.rpy` draft scripts as the source of truth. Do not use `story_board.md` as the
   machine-readable graph source.
3. Update only `[DAG_*]` comments. Do not alter prose, menu text, routing, stat effects,
   staging, existing `[STATE]` / `[CHOICE]` / `[BEAT]` / `[ASSET]` markers, or asset tags.
4. Preserve any `[DAG_* ... manual]` tag unless the user explicitly asks to overwrite manual
   DAG tags.
5. If manual DAG tags are skipped, report the file, line, tag type, and what command/request
   would be needed to overwrite them.
6. After any DAG tag update or recreate, rerun downstream graph manifest generation and report
   any stale graph/storyboard references.

```powershell
py scripts/agent_next_step.py --pipeline dag-tag-update --stage 1
```

## Manual tags

Default behavior preserves human-managed tags:

```renpy
# [DAG_NODE id=day102_3_coras_choice type=choice manual]
```

Only overwrite manual tags when the human explicitly requests it, e.g. "overwrite manual DAG
tags" or an equivalent `--overwrite-manual-dag-tags` flag in a future updater command.

## Downstream refresh

After updating or recreating DAG tags, regenerate the graph outputs under:

```text
main-game/pipeline/releases/release-1-mvp/graph/
```

Then run `storyboard_sync` if the graph audit reports storyboard drift.
