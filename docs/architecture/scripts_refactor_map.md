# Scripts refactor map

This document is pass 3 of the repo audit: classify the current `scripts/` surface and define a safe migration path before any physical file movement.

The guiding rule is conservative: **do not break existing agent commands to make the folder tree prettier.** Root-level script entrypoints stay stable until wrappers and docs prove the new structure is safe.

## Current problem

`scripts/` has become a mixed shelf:

- validation and CI checks;
- agent routing helpers;
- documentation catalogue tools;
- deterministic post-processors;
- asset and art helpers;
- route/balance/testing utilities;
- one-off migrations and local convenience scripts.

That is not fatal, but it makes agent use brittle because every helper looks equally official.

## Target structure

This is the desired long-term shape. It is **not** a command to move everything in one PR.

```text
scripts/
├── README.md                         # stable command index
├── validate.py                       # compatibility wrapper / canonical entrypoint
├── orchestrate_review.py             # compatibility wrapper / canonical entrypoint
├── contract_validate.py              # compatibility wrapper / canonical entrypoint
├── documentation_audit.py            # compatibility wrapper / canonical entrypoint
├── scene_direction.py                # compatibility wrapper / canonical entrypoint
├── format_non_canon.py               # compatibility wrapper / canonical entrypoint
├── agent_next_step.py                # compatibility wrapper / canonical entrypoint
├── resolve_work_item.py              # compatibility wrapper / canonical entrypoint
├── core/
│   └── narrative_paths.py            # path source of truth; move last, if ever
├── validation/
│   ├── validate_impl.py
│   ├── contract_validate_impl.py
│   ├── renpy_contract_linter.py
│   ├── engineering_compliance.py
│   └── historical_linter.py
├── agents/
│   ├── agent_next_step_impl.py
│   ├── orchestrate_review_impl.py
│   ├── resolve_work_item_impl.py
│   └── daily_standup_impl.py
├── docs/
│   └── documentation_audit_impl.py
├── scene/
│   ├── scene_direction_impl.py
│   └── format_non_canon_impl.py
├── assets/
│   ├── check_assets.py
│   ├── promote_assets.py
│   ├── daily_asset_manifest.py
│   └── resize_backgrounds.py
├── graph/
│   └── build_story_graph_manifest.py
└── archive/
    └── one_off_migrations/
```

## Stable public commands

These commands are referenced by agent docs and should remain valid even after internals move.

| Command | Category | Stability rule |
|---------|----------|----------------|
| `py scripts/validate.py --profile changed --agent <agent> --files "<paths>"` | Validation | Keep root wrapper permanently. |
| `py scripts/orchestrate_review.py --files "<paths>"` | Validation / review bundle | Keep root wrapper until all docs and CI call the new module path. |
| `py scripts/contract_validate.py --day day105 --release release-1-mvp` | Contract validation | Keep root wrapper permanently. |
| `py scripts/documentation_audit.py --write` | Documentation | Keep root wrapper permanently. |
| `py scripts/documentation_audit.py --check` | Documentation | Keep root wrapper permanently. |
| `py scripts/scene_direction.py --check --files "<day_non_canon.rpy>"` | Scene post-process | Keep root wrapper permanently. |
| `py scripts/format_non_canon.py <paths>` | Scene / non-canon formatting | Keep root wrapper until stage docs are updated. |
| `py scripts/agent_next_step.py --pipeline <name> --stage <n>` | Agent routing | Keep root wrapper permanently. |
| `py scripts/resolve_work_item.py --from-standup --next` | Standup routing | Keep root wrapper while standup remains supported. |

## Migration order

### Phase 3A — classify and document

Status: this document.

- Add this map.
- Update `scripts/README.md` so each script category has an owner and movement rule.
- Update the feature lifecycle registry to track script refactor work.
- Do not move files yet.

### Phase 3B — add packages without moving entrypoints

- Add subfolders only when the first implementation module is moved.
- Add `__init__.py` only where Python package imports require it.
- Keep root command wrappers in place.
- Wrapper rule: root script parses CLI or delegates to the implementation module without changing command syntax.

### Phase 3C — move low-risk internals first

Move scripts that are not directly referenced by AGENTS, skill docs, CI, or common human commands.

Good early candidates:

- one-off migrations into `scripts/archive/one_off_migrations/`;
- asset helper internals into `scripts/assets/`;
- graph-manifest helpers into `scripts/graph/`.

Bad early candidates:

- `validate.py`;
- `documentation_audit.py`;
- `agent_next_step.py`;
- `narrative_paths.py`;
- `scene_direction.py`.

### Phase 3D — wrapper-backed movement

Only after docs and audit pass:

1. Move implementation into category folder.
2. Leave root wrapper with the exact old CLI.
3. Update imports/tests/docs.
4. Run documentation audit and changed-file validation.
5. Do not remove wrapper in the same PR.

### Phase 3E — retire wrappers only with evidence

A root wrapper can be removed only when:

- no docs mention the old command;
- no CI/job config calls it;
- no agent skill references it;
- the feature lifecycle registry marks the old path as `remove-candidate`;
- the human explicitly approves deletion.

## Ownership by category

| Category | Owner/process | Examples | Notes |
|----------|---------------|----------|-------|
| `core` | Chief architect | `narrative_paths.py` | Path source of truth. Move last, if ever. |
| `validation` | Chief architect / gatekeeper | `validate.py`, `contract_validate.py`, linters | Root wrappers stay stable. |
| `agents` | Orchestrator / documentation steward | `agent_next_step.py`, `resolve_work_item.py`, `daily_standup.py` | Planning helpers must route into active processes. |
| `docs` | Documentation steward | `documentation_audit.py` | Generated catalogue/audit workflow depends on stable command. |
| `scene` | Scene direction agent / non-prod code | `scene_direction.py`, `format_non_canon.py` | Only touches staging/formatting surfaces, not prose. |
| `assets` | Art production / check-assets | `check_assets.py`, asset promotion helpers | Runtime manifest validation remains separate from art source docs. |
| `graph` | DAG tag update / documentation steward | story graph manifest builders | Audit and balancing support, not storyboard replacement. |
| `archive` | Human / chief architect | one-off migrations | Never route normal agent work through archive. |

## Do-not-break rules

- Do not change script CLI syntax in the same PR that moves implementation.
- Do not move `narrative_paths.py` until every importer is known.
- Do not move `validate.py` without a root wrapper.
- Do not move `documentation_audit.py` without also proving catalogue generation still works.
- Do not convert script refactor work into runtime Ren'Py changes.
- Do not use this refactor to over-modularize day prose or time-period labels.

## Validation checklist for future physical moves

```powershell
py scripts/documentation_audit.py --write
py scripts/documentation_audit.py --check
py scripts/validate.py --profile changed --agent chief_architect --files "<changed scripts>"
py scripts/validate.py --profile changed --agent documentation_steward --files "<changed docs>"
```

Also grep docs for the old command path before deleting or relocating a root-level command:

```powershell
rg "scripts/<script_name>.py"
```

## Pass 3 decision

Pass 3 creates the migration contract but does not physically move scripts. That is intentional. Physical moves should happen in narrow PRs after the generated documentation catalogue is refreshed locally and import references can be checked by running the repo test/validation commands.
