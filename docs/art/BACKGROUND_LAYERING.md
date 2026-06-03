# Savoy Hotel Background Layering & Overlay Specifications

This document defines the modular, base-and-overlay background strategy designed to support asset reuse across the Savoy Hotel's repeated architectural spaces.

---

## 🏢 The Reusability Mandate

A visual novel set entirely inside a luxury hotel offers a massive opportunity for asset optimization:
*   Instead of generating dozens of separate background rooms, we generate a highly polished, clean **Base Architecture Plate**.
*   We use transparent, layered **Overlays** to dynamically modify the lighting, room identity, time of day, and narrative context in real-time.

---

## 🚫 Designing for the Modular System

When generating or painting background environment plates, follow these strict separation rules:

*   **No Baked-In Text/Plaques**: Never bake room numbers, desk signage, or directional text directly into base backgrounds. These must live on independent detail overlay layers.
*   **Neutralize Core Assets**: Remove highly specific props, localized stains, unique paintings, or distinctive ornaments from base architectural layers.
*   **Decouple Lighting Glows**: Base backgrounds should be painted with clean, diffuse shadows. Dynamic shadows, high-contrast window rays, lamp halos, and fireplace glows must be isolated onto light/mood overlay layers.

---

## 🎨 Recommended Background Layer Groups

Organize all in-game environmental components into these standardized layering groups:

| Layer Group | Filename Prefix | Purpose & Example |
|-------------|-----------------|-------------------|
| **Base Architecture** | `bg_` | Clean structural plate. e.g. `bg_servants_corridor_base_v001.webp` |
| **Lighting Overlay** | `overlay_` | Windows light shafts, lamp halos. e.g. `overlay_corridor_light_morning_v001.webp` |
| **Mood/Shadow Overlay** | `overlay_` | Flickering candlelight shadow, twilight desaturation wash. |
| **Room Identity/Signage** | `overlay_` | Door plaques, room numbers. e.g. `overlay_corridor_door_number_12_v001.webp` |
| **Painting/Detail Overlay** | `overlay_` | Swappable wall paintings, mirrors, framed decorations. |
| **Prop Overlay** | `overlay_` | Scattered linens, dropped utility brushes, teacups on a side table. |
| **Special Event Overlay** | `overlay_` | Narrative blood pools, opened lock boxes, unlocked cabinet hatches. |

---

## 🔄 Ren'Py In-Engine Assembly Example

By decoupling backgrounds into base layers and overlays, we assemble rooms dynamically at runtime using simple `show` statements with standard position configurations:

```renpy
# Set up servants' corridor base hallway
scene bg_servants_corridor_base

# Add high-contrast morning light shaft
show overlay_servants_corridor_light_morning at truecenter

# Designate the door as Room 12
show overlay_servants_corridor_door_number_12 at truecenter

# Turn on lamp glow highlights
show overlay_servants_corridor_lamp_glow at truecenter

cora "The corridor is cold in the early hours..."
```

This saves massive file sizes, ensures absolute spatial consistency, and allows writing dramatic events (like a bulb breaking, a light shifting, or a prop appearing) using lightweight code swaps rather than heavy background transitions.
