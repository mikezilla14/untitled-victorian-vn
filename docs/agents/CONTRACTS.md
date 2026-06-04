# Agent contracts and enforcement

## Handoff contract (every stage)

Each specialist invocation receives:

| Input | Description |
|-------|-------------|
| Role context | Full paste of that agent's `.agents/rules/<name>.md` |
| Task input | Specific artifact (path, scene, question) |
| Prior output | Verdicts, `REJECT` notes, briefs from previous stages |

Each specialist returns:

| Output | Description |
|--------|-------------|
| Verdict | Labelled status (`PASS`, `REJECT`, `HISTORICALLY SOUND`, etc.) |
| References | File paths for any violation |
| Fix list | Concrete actions if rejecting |

Defined in [`.agents/rules/orchestrator.md`](../../.agents/rules/orchestrator.md) § Handoff Contract.

## Branch/worktree hygiene

Multi-tool workflows must use one branch per goal, not one branch per tool. Before any agent edits files, run:

```powershell
py scripts/agent_git_preflight.py --require-feature-branch --fail-if-dirty
```

See [`docs/agents/BRANCH_WORKFLOW_CONTRACT.md`](BRANCH_WORKFLOW_CONTRACT.md) and the [`branch_handoff`](../../.agents/skills/branch_handoff/SKILL.md) skill.

## Creative–technical boundary

| Rule | Enforced by |
|------|-------------|
| Writers' room owns all dialogue and narrator prose in promotion drafts | `writers_room`, gates |
| Code agents copy creative text **verbatim** | `non_prod_code_agent`, `prod_code_agent`, chief architect |
| Code agents must not patch prose inline | → file `dayrdd_narrative_change_brief.md` → `revise-narrative` |
| Prod promotion is copy, not rewrite | `prod_code_agent` |

## File domain permissions

[`.guardrails.yml`](../../.guardrails.yml) maps paths to `mutable_by` agent IDs.

Enforcement:

```powershell
py scripts/gatekeeper.py --agent writers_room --files "path/to/file"
```

Registered agents: `chief_architect`, `lead_narrative_editor`, `forensic_psychology_consultant`, `writers_room`, `spiciness_tuning_agent`, `victorian_consultant`, `prod_code_agent`, `non_prod_code_agent`, `gatekeeper_orchestrator`, `orchestrator`, `adult_market_reviewer` (read-only — no mutable paths).

Sub-agents (`divergent_writer`, `convergent_writer`) operate under `writers_room` permissions.

## Automated validation

| Tool | What it checks |
|------|----------------|
| `scripts/validate.py` | CI entry: gatekeeper domains, engineering compliance, Ren'Py linter, historical linter, writers-room pipeline |
| `scripts/writers_room_pipeline.py` | Shared logic: convergent report, spec scripts, gate verdict files |
| `scripts/orchestrate_review.py` | Local bundle: naming, engineering, Ren'Py, historical linter, **writers' room pipeline** |
| `scripts/agent_next_step.py` | Prints next agent rule file for a pipeline stage |
| `scripts/agent_git_preflight.py` | Branch, dirty tree, and worktree hygiene before agent edits |
| `scripts/engineering_compliance.py` | State discipline, day naming |
| `scripts/renpy_contract_linter.py` | Speaker/symbol contracts |
| `scripts/historical_linter.py` | Victorian language slice |

### Writers' room pipeline (when `*_non_canon.rpy` changes)

Implemented in `scripts/writers_room_pipeline.py`:

1. `dayrdd_convergent_report.md` exists and is not a placeholder
2. At least one `dayrdd_<persona>_spec.rpy` in `narrative/pipeline/`
3. **Gate verdicts** (when any gate file exists for that day, all three are required):
   - `dayrdd_gate_lead_narrative.md` — verdict `PASS` or `REJECT`
   - `dayrdd_gate_forensic_psychology.md` — e.g. `PSYCHOLOGICALLY CONSISTENT`
   - `dayrdd_gate_victorian.md` — e.g. `HISTORICALLY SOUND`

Flags for `validate.py`:

| Flag | Effect |
|------|--------|
| (default) | Gate checks on; partial OK if **no** gate files yet (warn only) |
| `--skip-gate-checks` | WIP — skip gate file validation |
| `--strict-gates` | Require all three gate files before promotion |

Gate file content must include a `## Verdict` section with a recognized label (not `TODO` / placeholder).

### JSON handoff contracts (dual-artifact)

When markdown handoff files exist, agents must also write the matching JSON sidecar. Schemas live in [`docs/contracts/`](../contracts/README.md).

| Artifact | JSON path | Schema |
|----------|-----------|--------|
| Gate verdict | `dayrdd_gate_<gate>.json` | `gate_verdict.schema.json` |
| Narrative change brief | `dayrdd_narrative_change_brief.json` | `narrative_change_brief.schema.json` |
| Profile delta | `dayrdd_profile_delta.json` | `profile_delta.schema.json` |
| Promotion handoff | `dayrdd_promotion_handoff.json` | `promotion_handoff.schema.json` |

JSON `verdict` values use underscores (e.g. `PSYCHOLOGICALLY_CONSISTENT`); markdown may use spaces. CI checks that both agree.

```powershell
py scripts/contract_validate.py --day day105 --release "release 1 - mvp"
py scripts/validate.py --skip-json-contracts --files "..."   # WIP only
```

## Context firewall

For **new** writing assignments, do not load:

- `narrative/pipeline/` (unless human requests archive mining)
- Other days' spec scripts
- `narrative/pipeline/experiments/` (unless brief points there)

See [`narrative/pipeline/README.md`](../../narrative/pipeline/README.md).

## Gate artifact naming

| Gate | File pattern |
|------|----------------|
| Narrative | `dayrdd_gate_lead_narrative.md` |
| Psychology | `dayrdd_gate_forensic_psychology.md` |
| Victorian | `dayrdd_gate_victorian.md` |
| Profile change report | `dayrdd_forensic_psychology_profile_report.md` |

## Escalation (orchestrator)

- Same `REJECT` **twice** on one issue → human
- Specialist conflict → human
- Missing input → stop; do not guess
- Creative drift in promotion → reject; `revise-narrative`

## Engineering canon

| Doc | Role |
|-----|------|
| [`docs/dev_bible.md`](../dev_bible.md) | Ren'Py MVP architecture contract |
| [`docs/game_mechanics_bible.md`](../game_mechanics_bible.md) | Player mechanics |
| [`docs/compliance_checklist.md`](../compliance_checklist.md) | PR human checklist |
