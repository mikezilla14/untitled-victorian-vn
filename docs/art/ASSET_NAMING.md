# Visual Novel Asset Naming Specification

To prevent file chaos and ensure clean integration with automated testing tools, all visual assets must follow these strict naming rules.

---

## 🏷️ Global Formatting Standards

*   **Strict Case Policy**: All folder names, filenames, and Ren'Py manifest aliases must be written in **lowercase `snake_case`**.
*   **No Spaces or Special Characters**: Never use spaces, hyphens, parentheses, or brackets in file paths.
*   **Zero-Padding Version Tags**: Every active asset must end with a three-digit version tag: `_v###` (e.g. `_v001`, `_v012`).
*   **No "Final" Filename Spam**: Never rename files to include `_final`, `_approved`, `_new_v2`, or similar tags. If an asset is updated, increment its version number (e.g. `_v001.webp` -> `_v002.webp`).

---

## 👥 Character Sprite Filename Convention

All character sprite crops exported to `assets_source/approved_assets/` and integrated into the engine must use this naming formula:

```text
{character}_{pose_family}_{expression}_{outfit}_v###.png
```

*   `character`: Cora, Gideon, Stern, Vance, or Missy.
*   `pose_family`: Core body posture class (e.g. `standing_front`, `writing_side`, `kneeling_left`).
*   `expression`: Subtle facial state (e.g. `neutral`, `guarded`, `cowed`, `dominant`, `indignant`, `shocked`).
*   `outfit`: Costume classification (e.g. `maid`, `suit`, `housekeeper`, `gown`).

### Sprite Examples:
*   `cora_standing_front_guarded_maid_v001.png`
*   `gideon_standing_front_dominant_suit_v001.png`
*   `stern_standing_front_severe_housekeeper_v002.png`
*   `vance_kneeling_left_cowed_gown_v001.png`

---

## 🖼️ Background Filename Convention

Background layers, background plates, and overlay elements must use these structural formulas:

### Base Architectural Plates
```text
bg_{location}_{base_or_state}_v###.png
```

### Overlay Modifiers (Lighting, Shadows, Signage)
```text
overlay_{location}_{function}_{variant}_v###.png
```

### Background Examples:
*   `bg_servants_corridor_base_v001.png`
*   `overlay_servants_corridor_light_morning_v001.png`
*   `overlay_servants_corridor_door_number_12_v001.png`
*   `bg_master_suite_day_v001.png`
*   `overlay_master_suite_candlelight_mood_v001.png`

---

## 🎛️ UI/HUD Filename Convention

UI components follow a simple prefix pattern:

```text
ui_{element_name}_{state}_v###.png
```

### UI Examples:
*   `ui_inkwell_empty_v001.png`
*   `ui_inkwell_full_v001.png`
*   `ui_cora_corrupted_v002.png`

---

## 🔄 Ren'Py Manifest Display Aliases

To keep script files human-readable and clean, declare simpler, descriptive display aliases in `assets_manifest.rpy` that map directly to the versioned files:

```renpy
# Example Sprite Declaration
declare_image_with_fallback("cora_sprite guarded", "images/sprites/cora/cora_standing_front_guarded_maid_v001.webp")

# Example Background Declaration
declare_image_with_fallback("bg_servants_corridor_morning", "images/backgrounds/bg_servants_corridor_morning.webp")
```

At runtime, writers will use the simple manifest aliases:
```renpy
scene bg_servants_corridor_morning
show cora_sprite guarded at center
```
This decouples script writing from underlying image version revisions.
