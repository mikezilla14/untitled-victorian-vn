# Active Character Visual Description Cards

This directory contains the active visual cards (`*.md`) for all main and secondary character sprites. These cards define the target style bible parameters, poses, outfits, and prompt templates, acting as the visual source of truth.

## Contract Compliance
All markdown visual cards in this directory are checked by the automated validation tool:
```powershell
python scripts/validate_art_fidelity.py
```
This ensures that attributes such as hair, eye, skin, and clothing descriptions remain fully synchronized with both the narrative profiles (`main-game/canon/`) and active game scripts, triggering a build error in the event of visual continuity drift.
