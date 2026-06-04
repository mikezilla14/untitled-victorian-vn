# Backlog documentation

This folder holds deferred designs and non-MVP implementation notes. Backlog files are not active
contracts until promoted by the Chief Architect or explicitly routed through the orchestrator.

## Files

| File | Purpose |
|------|---------|
| [mvp_backlog.md](mvp_backlog.md) | Human-curated MVP task backlog. |
| [book1-writing-feature-mvp.md](book1-writing-feature-mvp.md) | Active non-prod MVP backlog for the Book1 manuscript rendering feature. |
| [narrative-json-beat-pipeline.md](narrative-json-beat-pipeline.md) | Deferred JSON beat pipeline design. |
| [editors-desk-writing-mechanic.md](editors-desk-writing-mechanic.md) | Deferred Editors' Desk mechanic design. |
| [beat_schema.json](beat_schema.json) | Draft schema for future beat-catalog work. |

## Promotion rule

Before backlog work becomes active implementation, add or update a spec under `docs/specs/`, route
through `.agents/rules/orchestrator.md`, and refresh the documentation catalogue.
