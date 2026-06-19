# Shared sandbox systems

This folder contains non-canon shared Ren'Py/Python systems used by the draft day scripts.

## Typical contents

- State classes and singleton helpers.
- Effect/stat helper functions.
- Story-chain, penance, and confrontation routing.
- Shared notes for systems that are still being promoted or stabilised.

## Rules

- Spine/day scripts should own progression jumps; shared systems should generally return control to the caller.
- Deprecated compatibility labels may remain here, but new day code should not route through them.
- Runtime behaviour changes here should be validated against the MVP systems integration checklist before promotion.
