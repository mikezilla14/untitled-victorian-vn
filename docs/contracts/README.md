# Agent handoff contracts (JSON)

Machine-readable sidecars complement markdown artifacts. **Markdown remains authoritative for reasoning**; JSON is for routing, CI, and orchestrator logic.

## Dual-artifact rule

| Handoff | Markdown (human) | JSON (machine) |
|---------|------------------|----------------|
| Gate verdict | `dayrdd_gate_<gate>.md` | `dayrdd_gate_<gate>.json` |
| Narrative change brief | `dayrdd_narrative_change_brief.md` | `dayrdd_narrative_change_brief.json` |
| Profile update report | `dayrdd_forensic_psychology_profile_report.md` | `dayrdd_profile_delta.json` |
| Promotion handoff | (optional note in PR) | `dayrdd_promotion_handoff.json` |

When a markdown gate file exists, the matching `.json` **must** exist and `verdict` must agree with the markdown `## Verdict` section.

## Schemas

| Schema | File |
|--------|------|
| Gate verdict | [`gate_verdict.schema.json`](gate_verdict.schema.json) |
| Narrative change brief | [`narrative_change_brief.schema.json`](narrative_change_brief.schema.json) |
| Profile delta | [`profile_delta.schema.json`](profile_delta.schema.json) |
| Promotion handoff | [`promotion_handoff.schema.json`](promotion_handoff.schema.json) |

Examples: [`examples/`](examples/)

## Validation

```powershell
py scripts/contract_validate.py --day day105 --release "release 1 - mvp"
py scripts/validate.py --files "narrative/draft/releases/release-1-mvp/days/day105/day105_non_canon.rpy"
```

`validate.py` includes JSON contract checks when gate markdown files exist.

## Deferred

Full narrative **beats** as JSON (`docs/backlog/beat_schema.json`) — not part of MVP handoffs.
