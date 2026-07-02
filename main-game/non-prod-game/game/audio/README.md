# Non-prod audio (preview files)

Preview MP3 assets for the **non-prod sandbox** (`main-game/non-prod-game/`). Ren'Py auto-discovers files here; logical names are registered in [`../shared/assets_manifest.rpy`](../shared/assets_manifest.rpy).

## Layout

| Subfolder | Role |
|-----------|------|
| `themes/` | Background music loops |
| `ambient/` | Room/atmosphere beds |
| `sfx/` | One-shot sound effects |

Filenames retain source-library IDs (e.g. `SBA-*-preview.mp3`) for traceability to approved asset cards under `assets_source/`.

## Promotion

Approved audio is copied to `main-game/prod-game/game/audio/` and declared in `main-game/prod-game/game/assets_manifest.rpy` during promotion. Always guard playback in scripts (`if audio_name: renpy.play(...)`) until manifest registration exists.

## Validation

```powershell
py scripts/check_assets.py
py scripts/validate.py --profile changed --agent human --files "main-game/non-prod-game/game/shared/assets_manifest.rpy"
```

See also: [`check_assets`](../../../../.agents/skills/check_assets/SKILL.md) skill.
