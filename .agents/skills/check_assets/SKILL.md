# Check Assets

Use this skill when you want to **validate that the Ren'Py asset manifest (`assets_manifest.rpy`) is fully synchronized** with the assets referenced in active game scripts (dialogues, backgrounds, sprites, audios).

## When to use

- **Before promoting any Day draft** to the production game to ensure that no new image or audio asset is missing from the centralized manifest.
- **When checking compliance** for active gameplay files to prevent runtime solid-color fallback issues or startup failures.
- **As a regression check** during codebase cleanups or when assets are renamed, deleted, or added.

## What to do

1. Ensure the production game scripts under `renpy_project/game/` are fully structured.
2. Run the automated asset checker script to scan all game files:
   ```powershell
   py scripts/check_assets.py
   ```
3. **Analyze the Audit Results:**
   - **Compliance Pass:** If the script outputs `[COMPLIANCE PASS]`, the manifest is fully up-to-date and all referenced active assets are correctly declared.
   - **Compliance Failure:** If the script outputs `[COMPLIANCE FAILURE]`, inspect the reported list of unmanifested images or audio tracks and add their declarations (using `declare_image_with_fallback` or `register_audio`) to `renpy_project/game/assets_manifest.rpy`.
   - **Physical File Status:** The script will also report which declared manifest files do not physically exist on disk. Note that missing physical files are normal for local checkouts and will automatically degrade to safe, colored placeholders at runtime without crashing the game.
   - **Unused Declarations:** The script will report any assets declared in the manifest but never referenced in the active code. This is useful for pruning stale declarations.

## Compliance Contract

CI and the domain gatekeeper require all active, referenced assets to be declared in `assets_manifest.rpy`. An exit code of `1` from the validation script indicates a compliance breach.
