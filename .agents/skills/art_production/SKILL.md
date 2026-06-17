# Art Production Skill

Use this skill when you want to **generate visual prompt logs, write character/location asset cards, design modular Savannah Hotel background layers, slice VNCCS sheets, or run automated visual-narrative continuity audits**.

## When to use

- **When adding new character sprites or background locations** to the visual novel asset manifest.
- **Before drafting prompts or generating image concepts** to ensure perfect alignment with the Style Bible.
- **During pre-PR validations** to run the Art-Narrative Fidelity Contract checker and block visual contradictions.
- **When cropping and slicing VNCCS sheets** to guarantee canvas alignment and zero in-engine sprite jumping.

## What to do

### 1. Asset Card Construction
- Run this skill to parse canonical files and generate card templates:
  ```yaml
  # YAML frontmatter in assets_source/character_cards/ or location_cards/
  ```
- Make sure to specify the `renpy_image_name` matching the manifest alias.

### 2. Prompt Generation & Log Logging
- Pull the appropriate template block from `docs/art/PROMPT_LIBRARY.md`.
- Fill in the brackets `[CHARACTER DESCRIPTION]` or `[LOCATION DESCRIPTION]` and append style-bible parameters.
- Log prompt outputs under `assets_source/prompts/`.

### 3. Visual Continuity Audits
- Run the visual linter script to scan character profiles and drafts for visual description discrepancies:
  ```powershell
  python scripts/validate_art_fidelity.py
  ```
- Resolve any contract violations reported (such as mismatched hair color or attire designations) before committing.

## Compliance Contract

Any mismatch between character cards, the fidelity database (`docs/contracts/art_fidelity_contract.json`), and narrative files (`main-game/canon/`) is a compliance breach and will block deployment at PR stage.
