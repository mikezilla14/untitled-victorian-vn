# Documentation Audit

Use this skill when the user asks to update stale README files, catalogue project documentation,
sync docs with current repo state, run documentation hygiene before a commit, or perform the weekly
documentation maintenance pass.

## What to do

1. Load [`.agents/rules/documentation_steward.md`](../../rules/documentation_steward.md).
2. Inspect current repo state before editing; do not rely on old catalogue text.
3. Update stale README/project/spec/contract docs and add missing folder README files where needed.
4. Refresh generated catalogue artifacts:

```powershell
py scripts/documentation_audit.py --write
```

5. Verify generated artifacts are current:

```powershell
py scripts/documentation_audit.py --check
```

6. When part of a commit/PR, run validation for changed files:

```powershell
py scripts/validate.py --profile changed --agent documentation_steward --files "<changed files>"
```

## Outputs

- `docs/DOCUMENTATION_CATALOG.md` - human-readable cross-project documentation catalogue.
- `docs/DOCUMENTATION_AUDIT.md` - current audit findings and missing README coverage.
- `docs/documentation_catalog.json` - machine-readable catalogue matching
  `docs/contracts/documentation_catalog.schema.json`.

## Weekly use

The GitHub Actions workflow runs this audit weekly and on PRs. For local maintenance, run the same
`--write` command first, then commit the refreshed documentation artifacts.
