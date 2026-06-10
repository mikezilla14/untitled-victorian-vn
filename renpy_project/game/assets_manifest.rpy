# ═══════════════════════════════════════════════════════════════
#  assets_manifest.rpy
#  Centralized visual/audio asset declarations with safe fallbacks.
#  Missing files degrade to placeholders instead of breaking startup.
#
#  Canvas: 1920 × 1080 px  (gui.init in gui.rpy)
#  Sidebar: 300 px wide (left edge) — story viewport: 1620 × 1080 px
# ═══════════════════════════════════════════════════════════════

init -50 python:
    import os
    from renpy.display.image import Solid

    _missing_image_assets = []
    _missing_audio_assets = []

    def _abs(rel_path):
        # Assets live under <project>/game/, while config.basedir points to <project>/.
        return os.path.join(config.basedir, "game", rel_path)

    def declare_image_with_fallback(image_id, rel_path, color="#222222"):
        if os.path.exists(_abs(rel_path)):
            renpy.image(image_id, rel_path)
        else:
            renpy.image(image_id, Solid(color))
            _missing_image_assets.append((image_id, rel_path))

    def register_audio(name, rel_path):
        if os.path.exists(_abs(rel_path)):
            return rel_path
        _missing_audio_assets.append((name, rel_path))
        return None

    def report_missing_assets():
        if _missing_image_assets:
            renpy.log("MISSING IMAGE ASSETS:")
            for image_id, rel in _missing_image_assets:
                renpy.log(" - {} -> {}".format(image_id, rel))
        if _missing_audio_assets:
            renpy.log("MISSING AUDIO ASSETS:")
            for name, rel in _missing_audio_assets:
                renpy.log(" - {} -> {}".format(name, rel))


init -40 python:
    # ── Backgrounds ───────────────────────────────────────────────
    # [1920 × 1080 px]
    # Full canvas. The sidebar covers the leftmost 300 px at runtime; keep
    # focal content within the right 1620 px. WebP preferred for file size.
    declare_image_with_fallback("bg_savoy_corridor_morning", "images/backgrounds/bg_savoy_corridor_morning.png")
    declare_image_with_fallback("bg_laundry_room_day", "images/backgrounds/bg_laundry_room_day.webp")
    declare_image_with_fallback("bg_servants_corridor_dim", "images/backgrounds/bg_servants_corridor_dim.webp")
    declare_image_with_fallback("bg_servants_quarters_dusk", "images/backgrounds/bg_servants_quarters_dusk.webp")
    declare_image_with_fallback("bg_cora_desk_night", "images/backgrounds/bg_cora_desk_night.webp")
    declare_image_with_fallback("bg_master_suite_day", "images/backgrounds/bg_master_suite_day.webp")
    declare_image_with_fallback("bg_master_suite_tea", "images/backgrounds/bg_master_suite_tea.webp")
    declare_image_with_fallback("bg_servants_corridor_day", "images/backgrounds/bg_servants_corridor_day.webp")
    declare_image_with_fallback("bg_servants_corridor_morning", "images/backgrounds/bg_servants_corridor_morning.webp")
    declare_image_with_fallback("bg_master_suite_night", "images/backgrounds/bg_master_suite_night.webp")
    declare_image_with_fallback("bg_savoy_front_facade", "images/backgrounds/bg_savoy_front_facade.png")
    declare_image_with_fallback("bg_country_estate_corridor_night", "images/backgrounds/bg_country_estate_corridor_night.png", "#141210")
    declare_image_with_fallback("bg_country_estate_study", "images/backgrounds/bg_country_estate_study.png", "#1e1810")
    declare_image_with_fallback("bg_train_carriage_day", "images/backgrounds/bg_train_carriage_day.png", "#2a2520")

    # ── Sprites: Stern ────────────────────────────────────────────
    # [~700 × 1080 px, transparent background]
    # Full-height sprite sized for the 1920 × 1080 canvas. Transparent PNG or
    # lossless WebP. Width will vary with pose but should not exceed ~800 px.
    declare_image_with_fallback("stern_sprite neutral", "images/sprites/stern/neutral.png", "#555555")
    declare_image_with_fallback("stern_sprite stern", "images/sprites/stern/stern.webp", "#555555")

    # ── Sprites: Vance ────────────────────────────────────────────
    # [~700 × 1080 px, transparent background]  (same spec as Stern above)
    declare_image_with_fallback("vance_sprite neutral", "images/sprites/vance/neutral.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite angry", "images/sprites/vance/angry.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite indignant", "images/sprites/vance/indignant.webp", "#7b3f98")
    declare_image_with_fallback("vance_sprite submissive", "images/sprites/vance/submissive.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite cowed", "images/sprites/vance/cowed.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite defeated", "images/sprites/vance/defeated.webp", "#7b3f98")
    declare_image_with_fallback("vance_sprite mirror_watch_terror", "images/sprites/vance/mirror_watch_terror.webp", "#7b3f98")
    declare_image_with_fallback("vance_sprite confused", "images/sprites/vance/confused.webp", "#7b3f98")
    declare_image_with_fallback("vance_sprite shocked", "images/sprites/vance/shocked.webp", "#7b3f98")

    # ── Sprites: Gideon ───────────────────────────────────────────
    # [~700 × 1080 px, transparent background]  (same spec as Stern above)
    declare_image_with_fallback("gideon_sprite cold", "images/sprites/gideon/cold.webp", "#a30000")
    declare_image_with_fallback("gideon_sprite neutral", "images/sprites/gideon/neutral.webp", "#a30000")
    declare_image_with_fallback("gideon_sprite dominant", "images/sprites/gideon/dominant.webp", "#a30000")
    declare_image_with_fallback("gideon_sprite angry", "images/sprites/gideon/angry.webp", "#a30000")

    # ── Sprites: Missy ────────────────────────────────────────────
    # [~700 × 1080 px, transparent background]  (same spec as Stern above)
    declare_image_with_fallback("missy_sprite neutral", "images/sprites/missy/neutral.webp", "#5fa8d3")
    declare_image_with_fallback("missy_sprite smiling", "images/sprites/missy/smiling.webp", "#5fa8d3")
    declare_image_with_fallback("missy_sprite naive", "images/sprites/missy/naive.webp", "#5fa8d3")
    declare_image_with_fallback("missy_sprite shocked", "images/sprites/missy/shocked.webp", "#5fa8d3")
    declare_image_with_fallback("missy_sprite hesitant", "images/sprites/missy/hesitant.webp", "#5fa8d3")
    declare_image_with_fallback("missy_sprite confused", "images/sprites/missy/confused.webp", "#5fa8d3")

    # ── Sprites: Cora (scene-dependent) ──────────────────────────
    # [~700 × 1080 px, transparent background]  (same spec as Stern above)
    declare_image_with_fallback("cora_sprite base", "images/sprites/cora/base.webp", "#d4a574")
    declare_image_with_fallback("cora_sprite guarded", "images/sprites/cora/guarded.webp", "#d4a574")
    declare_image_with_fallback("cora_sprite focused", "images/sprites/cora/focused.webp", "#d4a574")
    declare_image_with_fallback("cora_sprite flushed", "images/sprites/cora/flushed.webp", "#d4a574")
    declare_image_with_fallback("cora_sprite neutral", "images/sprites/cora/neutral.webp", "#d4a574")

    # ── UI: persistent HUD (stats_overlay) ───────────────────────
    #
    # ui_cora_base:
    #   [268 × 190 px]  Exact display size in sidebar (HUD_SIDEBAR_WIDTH - 32 × 190).
    #   Design at 2× (536 × 380 px) and let Ren'Py scale down for sharpness.
    #   Cora portrait, framed bust shot. Used at corruption_level 1–2.
    declare_image_with_fallback("ui_cora_base", "images/ui/ui_cora_base.webp", "#d4a574")
    #
    # ui_cora_corrupted:
    #   [268 × 190 px]  Same dimensions as ui_cora_base (design at 2×: 536 × 380 px).
    #   Swapped in at corruption_level >= 3. Should read as visibly changed — colder,
    #   more controlled, slight desaturation or shadow shift.
    declare_image_with_fallback("ui_cora_corrupted", "images/ui/ui_cora_corrupted.webp", "#8b2942")
    #
    # ui_sidebar_bg:
    #   [300 × 1080 px]  Full sidebar at canvas height.
    #   Aged dark-leather or near-black parchment texture. Warm near-black with subtle
    #   grain/wear. Semi-opaque (~95%) so the scene bleeds through faintly.
    declare_image_with_fallback("ui_sidebar_bg", "images/ui/ui_sidebar_bg.webp", "#1a120af2")
    #
    # ui_sidebar_divider:
    #   [268 × 10 px]  Exact display size (HUD_SIDEBAR_WIDTH - 32 × 10).
    #   Design at 2× (536 × 20 px) for sharpness. Victorian ornamental styling —
    #   ink smear, ruled-ledger line, or aged parchment crease. Subtle, not overwrought.
    declare_image_with_fallback("ui_sidebar_divider", "images/ui/ui_sidebar_divider.webp", "#2a1e0f")
    #
    # ui_vignette_ambient:
    #   [1920 × 1080 px]  Full canvas. Displayed scaled to the story viewport
    #   (1620 × 1080 px at runtime). Radial darkening at edges, ~20–30% max opacity.
    #   Provides constant cinematic framing, independent of the anxiety vignette.
    #   Fallback is transparent — missing asset produces no visible effect.
    declare_image_with_fallback("ui_vignette_ambient", "images/ui/ui_vignette_ambient.webp", "#00000000")
    #
    # ui_suspicion_vignette:
    #   [1920 × 1080 px]  Full canvas. Displayed scaled to story viewport (1620 × 1080 px).
    #   Rendered at alpha = player.anxiety / 100; fully opaque at anxiety 100.
    #   Deep red/crimson radial burn at edges — should feel oppressive at full intensity.
    declare_image_with_fallback("ui_suspicion_vignette", "images/ui/ui_suspicion_vignette.webp", "#3a0000")
    #
    # ui_inkwell_empty / ui_inkwell_full:
    #   [64 × 110 px]  Exact display size in sidebar.
    #   Design at 2× (128 × 220 px) for sharpness.
    #   ui_inkwell_empty: the glass/ceramic vessel, empty. Transparent interior required
    #                     so the layered fill crop shows through correctly.
    #   ui_inkwell_full:  identical vessel with interior filled with black ink to the brim.
    #                     The fill level is a crop from the bottom up proportional to
    #                     inspiration / inspiration_cap — the ink surface must align with
    #                     the vessel's interior top edge at 100% fill.
    declare_image_with_fallback("ui_inkwell_empty", "images/ui/ui_inkwell_empty.webp", "#1a1a1a")
    declare_image_with_fallback("ui_inkwell_full", "images/ui/ui_inkwell_full.webp", "#1e5a8a")

    # ── UI: Book Writing Screen Assets ───────────────────────────
    declare_image_with_fallback("ui_book_writing_paper", "images/ui/book_writing_paper.webp", "#f4efe2")
    declare_image_with_fallback("ui_book_cover", "images/ui/book_cover.webp", "#3d2314")
    declare_image_with_fallback("ui_book_ui_bg", "images/ui/book_ui_bg.webp", "#1c1410")
    declare_image_with_fallback("ui_cora_mini_base", "images/ui/ui_cora_mini_base.webp", "#d4a574")
    declare_image_with_fallback("ui_cora_mini_corrupted", "images/ui/ui_cora_mini_corrupted.webp", "#8b2942")
    declare_image_with_fallback("ui_illustration_border", "images/ui/illustration_border.webp", "#5a5a5a")
    declare_image_with_fallback("ui_price_badge", "images/ui/price_badge.webp", "#3a1a0a")

    # ── Audio aliases (None when missing; guard before play) ──────
    audio_themes_savoy_tension = register_audio("themes/savoy_tension", "audio/themes/savoy_tension.ogg")
    audio_themes_servants_floor_unease = register_audio("themes/servants_floor_unease", "audio/themes/servants_floor_unease.ogg")
    audio_themes_private_ink = register_audio("themes/private_ink", "audio/themes/private_ink.ogg")
    audio_themes_master_suite_pressure = register_audio("themes/master_suite_pressure", "audio/themes/master_suite_pressure.ogg")
    audio_themes_predator_game = register_audio("themes/predator_game", "audio/themes/predator_game.ogg")
    audio_themes_defiance_and_dread = register_audio("themes/defiance_and_dread", "audio/themes/defiance_and_dread.ogg")

    audio_ambient_laundry_steam = register_audio("ambient/laundry_steam", "audio/ambient/laundry_steam.ogg")
    audio_ambient_hotel_corridor_muffled = register_audio("ambient/hotel_corridor_muffled", "audio/ambient/hotel_corridor_muffled.ogg")
    audio_ambient_servants_quarters_dusk = register_audio("ambient/servants_quarters_dusk", "audio/ambient/servants_quarters_dusk.ogg")
    audio_ambient_master_suite_quiet = register_audio("ambient/master_suite_quiet", "audio/ambient/master_suite_quiet.ogg")
    audio_ambient_fireplace_low = register_audio("ambient/fireplace_low", "audio/ambient/fireplace_low.ogg")

    audio_sfx_corridor_slap_muffled = register_audio("sfx/corridor_slap_muffled", "audio/sfx/corridor_slap_muffled.ogg")
    audio_sfx_floorboard_creak = register_audio("sfx/floorboard_creak", "audio/sfx/floorboard_creak.ogg")
    audio_sfx_ink_scratch = register_audio("sfx/ink_scratch", "audio/sfx/ink_scratch.ogg")
    audio_sfx_washbasin_clatter = register_audio("sfx/washbasin_clatter", "audio/sfx/washbasin_clatter.ogg")
    audio_sfx_lockpick_tension = register_audio("sfx/lockpick_tension", "audio/sfx/lockpick_tension.ogg")
    audio_sfx_key_in_door = register_audio("sfx/key_in_door", "audio/sfx/key_in_door.ogg")
    audio_sfx_brush_drop_clatter = register_audio("sfx/brush_drop_clatter", "audio/sfx/brush_drop_clatter.ogg")
    audio_sfx_door_handle_jiggle = register_audio("sfx/door_handle_jiggle", "audio/sfx/door_handle_jiggle.ogg")

    report_missing_assets()
