# Agent rule files

This folder contains specialist role prompts. Load the full markdown file as the system prompt when
the Production Orchestrator names that agent.

## Source of truth

- Primary router: [orchestrator.md](orchestrator.md)
- Human index: [../README.md](../README.md)
- Repo-wide quick start: [../../AGENTS.md](../../AGENTS.md)

## Maintenance

When adding or renaming a rule file, update:

- [../README.md](../README.md)
- [../../AGENTS.md](../../AGENTS.md)
- [../../docs/agents/PIPELINE_REFERENCE.md](../../docs/agents/PIPELINE_REFERENCE.md)
- [../../scripts/agent_next_step.py](../../scripts/agent_next_step.py)

Then run `py scripts/documentation_audit.py --write`.
