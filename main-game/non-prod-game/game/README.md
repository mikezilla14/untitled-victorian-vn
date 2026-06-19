# Non-prod Ren'Py `game/` folder

This is the sandbox Ren'Py `game/` directory. It is loaded by Ren'Py during non-production runs, but it is **not** the shipping canon source.

## What belongs here

- Draft day scripts under `days/`.
- Shared sandbox mechanics under `shared/`.
- UI, GUI, images, audio, and dev-only Ren'Py support files needed to run the sandbox project.
- Test harnesses that are intentionally excluded from the player `start` path.

## What does not belong here

- Final production-only hotfixes that have not been mirrored back to the matching non-canon draft.
- One-off migration scripts that are not required by the Ren'Py project.
- Untracked/generated image debris that is not intentionally referenced by the asset manifest.

## Agent rule of thumb

If the task changes player-facing runtime behaviour, prefer changing the relevant draft file here first, then promote through `main-game/prod-game/`. If the task is documentation-only, do not edit runtime `.rpy` files as part of the same pass.
