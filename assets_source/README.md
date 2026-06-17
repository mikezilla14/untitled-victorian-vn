# Savoy Hotel Visual Novel: Active Assets Source Directory

This directory acts as the active workspace and repository for raw assets, generation prompt files, sliced frames, and approved media prior to their integration into the Ren'Py engine under `main-game/prod-game/game/images/`.

## Directory Structure

```text
assets_source/
├── character_cards/      # Active character visual description cards (*.md)
├── location_cards/       # Active background scene visual cards (*.md)
├── prompts/              # Generation prompt logs and text experiments
├── vnccs_sheets/         # Raw VNCCS grid sprite sheets categorized by character
├── generated_concepts/   # Raw generations, uncleaned background plates, crop sandboxes
└── approved_assets/      # Verified, sliced, compressed, and ready production assets
```

## Workflow References

See [docs/art/README.md](../docs/art/README.md) for full style bible parameters, slicing instructions, background layering configurations, and compliance lint checking routines.
