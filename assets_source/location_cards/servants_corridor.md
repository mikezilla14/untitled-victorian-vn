---
asset_id: "servants_corridor"
asset_type: "background"
location: "service_corridors"
scene_use: "transit, chore work, servant gossip, surveillance points"
source_mode: "text-to-image"
base_or_overlay: "base"
mood: "dusty, atmospheric, repetitive, confined"
lighting: "high_window_morning"
time_of_day: "morning"
palette: "desaturated_mahogany, warm_amber, dust_grey"
reusability_notes: "used repeatedly for servants' floors hallway transit throughout the five-day arc"
removable_details: ["door_number_12", "hanging_lamp_glow"]
layer_group: "base_architecture"
prompt_template: "Template 4"
prompt: "An environment plate of a Savoy Hotel servant service corridor, 1891 late Victorian era. Moody transitional hallway with dark mahogany wainscoting, cream patterned wallpaper, brass sconce lamps lining the walls, a repeated row of paneled wooden doors recrossing in deep perspective. Soft morning sunlight filtering through a high small window, dusty ambient atmosphere. Painterly visual novel background style, watercolor washes, rich desaturated wood tones, no characters --no characters, 3d, photograph, neon"
source_reference: "corridor_plate_ref_001"
status: "approved"
renpy_image_name: "bg_servants_corridor_morning"
renpy_target_path: "images/backgrounds/bg_servants_corridor_morning.webp"
source_output_path: "assets_source/generated_concepts/corridor_morning_raw.png"
approved_output_path: "assets_source/approved_assets/bg_servants_corridor_morning_v001.webp"
notes: "Optimized for dialogue readability. Bottom third desaturated by 15%."
---

# Savoy Servants' Corridor: Background Visual Card

The service corridors of the Savoy represent the confined, repetitive, and heavily monitored spaces inhabited by domestic staff. Features wainscoting and wooden doors that lead to guest suites and linen closets.

## Modular Layering Configuration

To reuse this corridor across multiple time-of-day scenarios and story moments, apply these overlay configurations:

*   **Base Plate (`bg_servants_corridor_base.webp`)**: Clean structural perspective plate. Natural wood wainscoting, cream wallpaper, clean doors without numbers. Sconce lamps are unlit.
*   **Morning Light Overlay (`overlay_servants_corridor_light_morning.webp`)**: High-contrast, cool morning light shafts falling from the high small window. Adds dust motes in the air.
*   **Twilight Dim Overlay (`bg_servants_corridor_dim.webp` / `overlay_corridor_dim.webp`)**: Desaturated, bluish shadow layer, unlit lamps, representing dusk or twilight.
*   **Lamp Glow Overlay (`overlay_servants_corridor_lamp_glow.webp`)**: Rich amber, warm gaslight halos emitting from brass sconce brackets, casting deep, elongated shadows.
*   **Plaque Overlay (`overlay_servants_corridor_door_number_12.webp`)**: High-detail brass numbers aligned onto the nearest door frame to designate Room 12.
