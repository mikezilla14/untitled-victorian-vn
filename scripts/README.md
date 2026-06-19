# Scripts

This folder contains local and CI helper scripts for validation, migration, catalogue refreshes, deterministic post-processing, route inspection, and agent workflow support. Scripts are meant to be run from the repository root.

See also: [`docs/architecture/scripts_refactor_map.md`](../docs/architecture/scripts_refactor_map.md).

## Common commands

| Command | Purpose | Owner/process |
|---------|---------|---------------|
| `py scripts/validate.py --profile changed --agent human --files "<paths>"` | Standard changed-file validation entry. | Chief architect / gatekeeper |
| `py scripts/orchestrate_review.py --files "<paths>"` | Pre-PR narrative contract bundle. | Chief architect / writers' room |
| `py scripts/contract_validate.py --day day105 --release release-1-mvp` | Validate per-day JSON/markdown handoffs. | Chief architect / documentation steward |
| `py scripts/scene_direction.py --check --files "<day_non_canon.rpy>"` | Check deterministic sprite placement lines. | Scene direction agent |
| `py scripts/format_non_canon.py <paths>` | Normalize non-canon script formatting/staging markers. | Non-prod code / scene direction |
| `py scripts/documentation_audit.py --write` | Refresh documentation catalogue and audit artifacts. | Documentation steward |
| `py scripts/documentation_audit.py --check` | Fail when generated documentation catalogue artifacts are stale. | Documentation steward |
| `py scripts/balance_report.py --release release-1-mvp` | Static testing/balance report for non-prod sandbox (gates, fail states, grain manifest, catalogues). | Chief architect |
| `py main-game/pipeline/tools/build_grain_manifest.py --release release-1-mvp` | Extract balance grains and gap report from sandbox `.rpy` files. | Chief architect / dag_tag_update |
| `py main-game/pipeline/tools/build_choice_catalogue.py --release release-1-mvp` | Import graph choices/effects into `choice_catalogue.csv`. | Chief architect |
| `py main-game/pipeline/tools/simulate_balance.py --release release-1-mvp` | Abstract policy/gate simulation and fuzz distribution report. | Chief architect |
| `py main-game/pipeline/tools/compare_runtime_to_model.py --release release-1-mvp` | Compare JSONL playtest captures to balance_targets matrix. | Chief architect |
| `py scripts/agent_next_step.py --pipeline <name> --stage <n>` | Print the next agent/rule for a pipeline stage. | Orchestrator |
| `py scripts/resolve_work_item.py --from-standup --next` | Turn a standup work item into the next routed task. | Daily standup / action-from-standup |

## Categories

The current folder is intentionally still mostly flat. Do not infer that every file here is equally active or equally safe for agents to use.

| Category | What belongs there long-term | Movement rule |
|----------|------------------------------|---------------|
| `core/` | Path helpers and repo-wide constants, especially `narrative_paths.py`. | Move last, if ever. |
| `validation/` | Validation entrypoints, linters, contract checks, compliance checks. | Root wrappers must preserve old commands. |
| `agents/` | Agent routing helpers, standup routing, work-item resolution. | Planning helpers must route into active processes. |
| `docs/` | Documentation catalogue/audit implementation. | Keep `scripts/documentation_audit.py` as stable wrapper. |
| `scene/` | Scene-direction and non-canon formatting implementation. | Keep staging/prose boundaries intact. |
| `assets/` | Asset manifest checks, asset promotion helpers, image/audio utility scripts. | Runtime asset validation remains separate from source art workflows. |
| `graph/` | Story graph and DAG manifest helpers. | Audit support only; not storyboard source of truth. |
| `validation/` | Testing/balance static reports and future validation internals. | Root `scripts/balance_report.py` stays the stable wrapper. |
| `archive/one_off_migrations/` | One-off migration scripts. | Never route normal agent work through archive. |

## Compatibility policy

Root-level commands referenced by `AGENTS.md`, `.agents/skills/**`, `docs/agents/**`, CI, or normal human workflow are stable public entrypoints. If implementation moves into a subfolder, leave a root wrapper with the same CLI.

Do not remove a root wrapper until:

1. no docs or skill files reference the old command;
2. no CI or scheduled task calls it;
3. the feature lifecycle registry marks the old path as removable;
4. the human approves deletion.

## Maintenance

When adding a script, document its role here if it becomes part of normal agent, CI, or human workflow. One-off migrations should live under `scripts/archive/one_off_migrations/`.

When moving a script, update [`docs/architecture/scripts_refactor_map.md`](../docs/architecture/scripts_refactor_map.md), run the documentation audit, and preserve root command compatibility unless the PR explicitly removes a deprecated wrapper.
