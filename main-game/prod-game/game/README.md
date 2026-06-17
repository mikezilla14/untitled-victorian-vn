# Ren'Py game scripts

This folder is the playable runtime source for the visual novel. Promoted `day*.rpy` files are
episodic canon; draft and speculative material belongs under `main-game/`.

## Boundaries

- Production day scripts are written by `prod_code_agent` or humans after promotion review.
- Code/framework changes are reviewed by `chief_architect`.
- Documentation-only changes should cite these files but not alter runtime behavior.

Run standard validation from the repo root:

```powershell
py scripts/validate.py --profile changed --agent human --files "<paths>"
```
