# Documentation

This folder contains project documentation, contracts, feature specs, onboarding material, art
workflow references, and generated documentation catalogue artifacts.

## Main indexes

| File | Purpose |
|------|---------|
| [DOCUMENTATION_CATALOG.md](DOCUMENTATION_CATALOG.md) | Generated cross-project documentation catalogue. |
| [DOCUMENTATION_AUDIT.md](DOCUMENTATION_AUDIT.md) | Generated stale-doc and missing-README report. |
| [agents/README.md](agents/README.md) | Agent workflow documentation index. |
| [contracts/README.md](contracts/README.md) | Machine-readable handoff contract index. |
| [specs/README.md](specs/README.md) | Feature spec index and required sections. |
| [art/README.md](art/README.md) | Visual asset production documentation. |

## Maintenance

Update source docs first, then refresh generated artifacts:

```powershell
py scripts/documentation_audit.py --write
py scripts/documentation_audit.py --check
```
