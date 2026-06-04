# Agent documentation

This folder is the human-readable companion to the rule files under `.agents/rules/`.
If the rule file and this folder disagree, the rule file wins.

## Files

| File | Purpose |
|------|---------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | First-run walkthrough for documentation-driven agent orchestration. |
| [PIPELINE_REFERENCE.md](PIPELINE_REFERENCE.md) | Human index of orchestrator pipelines and stage order. |
| [CONTRACTS.md](CONTRACTS.md) | Handoff rules, validation tools, and JSON sidecar expectations. |
| [BRANCH_WORKFLOW_CONTRACT.md](BRANCH_WORKFLOW_CONTRACT.md) | Branch/worktree hygiene for multi-tool agent handoffs. |

## Maintenance

When a rule file, skill, validation script, or pipeline changes, update this folder in the same
change and run:

```powershell
py scripts/documentation_audit.py --write
py scripts/documentation_audit.py --check
```
