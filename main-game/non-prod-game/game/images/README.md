# Runtime image assets

This folder contains image assets loaded by the non-production Ren'Py project.

## Rules

- Keep runtime-ready assets here, not loose prompt exports or scratch files.
- Source/prompt/card material belongs under `assets_source/` or the relevant art documentation area.
- Generated debris such as temporary `ChatGPT Image*.png`, editor backup files, or removal scripts should be removed or gitignored unless intentionally referenced.
- Asset IDs and fallback expectations should be documented through the manifest/check-assets process.

## Subfolders

- `sprites/` — character and UI sprites.
- `ui/` — game interface images and overlays.
- Background folders/files should follow existing asset naming conventions and be manifest-visible before promotion.
