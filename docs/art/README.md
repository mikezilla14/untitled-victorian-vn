# Visual Novel Art Prompt Workflow & Production Manual

Welcome to the repo-owned visual asset production documentation suite. This manual organizes all guidelines, templates, naming conventions, and validation contracts required to deliver a polished, Victorian-era styled aesthetic for the Untitled Victorian Visual Novel.

> [!NOTE]
> **MVP Core Directive**: Generate visual concepts quickly, drop rough placeholder layers into the Ren'Py engine to maintain pipeline flow, and focus high-fidelity manual cleanup exclusively on approved, high-frequency characters and background environments.

---

## Documentation Map

To understand and execute visual asset production, consult the following guides:

| Reference Document | Target Audience | Key Purpose |
|--------------------|-----------------|-------------|
| 🎨 [STYLE_BIBLE.md](STYLE_BIBLE.md) | Art Director / Prompt Specialist | Locked visual descriptors, character profiles, anime style anchors. |
| 📝 [PROMPT_LIBRARY.md](PROMPT_LIBRARY.md) | Prompt Engineer / Writers | Compact, copy-pasteable image generation prompt templates. |
| 📇 [ASSET_CARD_SCHEMA.md](ASSET_CARD_SCHEMA.md) | Technical Artist / Developers | YAML frontmatter specifications for character, background, and UI cards. |
| 🏷️ [ASSET_NAMING.md](ASSET_NAMING.md) | Asset Manager / Linter | lowercase snake_case file structures and Ren'Py manifest aliases. |
| ✂️ [VNCCS_SPRITE_SHEETS.md](VNCCS_SPRITE_SHEETS.md) | Sprite Artist / Slice Engineer | Sheet slicing techniques, grid sizing, and transparency alignment. |
| 🗺️ [BACKGROUND_LAYERING.md](BACKGROUND_LAYERING.md) | Background Artist / Layering | Savannah Hotel base-and-overlay architecture, daytime/candlelight mood stacks. |
| 🔄 [PRODUCTION_WORKFLOW.md](PRODUCTION_WORKFLOW.md) | Production Orchestrator | Interactive production loop from draft request to final signed-off asset. |

---

## Future Backlog Preservation Rules

To prepare the codebase for a future layered "paper-doll" character sprite system without overloading the initial MVP release, follow these rules:

1. **Retain Raw Assets**: Always save original uncropped VNCCS grid rendering sheets under `assets_source/vnccs_sheets/{character}/`.
2. **Anchor Coordinate Logs**: When slicing individual sprites from sheets, document the coordinate bounds, original cell orders, and source prompt seeds inside their corresponding active cards.
3. **Canvas Consistency**: Export all sprites placed onto a uniform canvas size matching their respective character models. This preserves coordinate relationships for prospective layered rendering swaps.
