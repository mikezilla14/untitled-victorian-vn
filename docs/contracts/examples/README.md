# Contract examples

This folder contains sample JSON sidecars for the schemas in [../README.md](../README.md).

Examples are illustrative, not production handoffs. When a schema changes, update its matching
example in the same change and run:

```powershell
py scripts/documentation_audit.py --write
py scripts/contract_validate.py --help
```
