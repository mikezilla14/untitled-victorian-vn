# Agent skills

This folder holds thin skill wrappers for common workflows. A skill should point to the relevant
rule file, name the pipeline, and list the commands or artifacts a human/IDE agent needs.

## Maintenance

When adding a skill:

- Add a row to [../../AGENTS.md](../../AGENTS.md).
- Add any new specialist rule to [../README.md](../README.md).
- Register new pipeline stages in [../../scripts/agent_next_step.py](../../scripts/agent_next_step.py) when applicable.
- Run `py scripts/documentation_audit.py --write`.
