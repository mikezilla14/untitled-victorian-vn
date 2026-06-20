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

    def _find_asset(rel_path):
        paths_to_check = []
        if hasattr(config, 'searchpath'):
            for p in config.searchpath:
                if os.path.isabs(p):
                    paths_to_check.append(os.path.join(p, rel_path))
                else:
                    paths_to_check.append(os.path.join(config.basedir, p, rel_path))
        paths_to_check.append(os.path.join(config.basedir, "game", rel_path))
        
        for p in paths_to_check:
            if os.path.exists(p):
                return True
        return False

    def declare_image_with_fallback(image_id, rel_path, color="#222222"):
        is_sprite = "_sprite" in image_id
        
        if _find_asset(rel_path):
            displayable = renpy.display.im.Image(rel_path)
        else:
            displayable = Solid(color)
            _missing_image_assets.append((image_id, rel_path))
            
        if is_sprite:
            char_name = image_id.split("_sprite")[0]
            displayable = At(displayable, sprite_highlight(char_name))
            
        renpy.image(image_id, displayable)

    def register_audio(name, rel_path):
        # 1. Check local game directory first
        local_path = os.path.join(config.basedir, "game", rel_path)
        if os.path.exists(local_path):
            return rel_path
            
        # 2. Check search path (e.g. prod-game)
        if hasattr(config, 'searchpath'):
            for p in config.searchpath:
                if os.path.isabs(p):
                    full_path = os.path.join(p, rel_path)
                else:
                    full_path = os.path.join(config.basedir, p, rel_path)
                if os.path.exists(full_path):
                    # Return absolute path so Ren'Py can locate and play the file
                    return os.path.abspath(full_path)
                    
        # 3. Mark as missing
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
    declare_image_with_fallback("bg_savoy_corridor_morning", "images/backgrounds/bg_savoy_corridor_morning.webp")
    declare_image_with_fallback("bg_laundry_room_day", "images/backgrounds/bg_laundry_room_day.webp")
    declare_image_with_fallback("bg_servants_corridor_dim", "images/backgrounds/bg_servants_corridor_dim.webp")
    declare_image_with_fallback("bg_servants_quarters_dusk", "images/backgrounds/bg_servants_quarters_dusk.webp")
    declare_image_with_fallback("bg_servants_quarters_dusk side", "images/backgrounds/bg_servants_quarters_side_dusk.webp")
    declare_image_with_fallback("bg_cora_desk_night", "images/backgrounds/bg_cora_desk_night.webp")
    declare_image_with_fallback("bg_master_suite_day", "images/backgrounds/bg_master_suite_day.webp")
    declare_image_with_fallback("bg_master_suite_tea", "images/backgrounds/bg_master_suite_tea.webp")
    declare_image_with_fallback("bg_servants_corridor_day", "images/backgrounds/bg_servants_corridor_day.webp")
    declare_image_with_fallback("bg_servants_corridor_morning", "images/backgrounds/bg_servants_corridor_morning.webp")
    declare_image_with_fallback("bg_master_suite_night", "images/backgrounds/bg_master_suite_night.webp")
    declare_image_with_fallback("bg_savoy_front_facade", "images/backgrounds/bg_savoy_front_facade.webp")
    declare_image_with_fallback("bg_stern_office_entrance", "images/backgrounds/bg_stern_office_entrance.webp")
    declare_image_with_fallback("bg_stern_office_reverse", "images/backgrounds/bg_stern_office_reverse.webp")
    declare_image_with_fallback("bg_savoy_corridor_right_morning", "images/backgrounds/bg_savoy_corridor_right_morning.webp")
    declare_image_with_fallback("bg_servants_corridor_dusk", "images/backgrounds/bg_servants_corridor_dusk.webp")
    declare_image_with_fallback("bg_country_estate_corridor_night", "images/backgrounds/bg_country_estate_corridor_night.webp", "#141210")
    declare_image_with_fallback("bg_train_carriage_day", "images/backgrounds/bg_train_carriage_day.webp", "#2a2520")
    declare_image_with_fallback("bg_country_estate_study", "images/backgrounds/bg_country_estate_study.webp", "#1e1810")

    # ── Sprites: Stern ────────────────────────────────────────────
    # [~700 × 1080 px, transparent background]
    # Full-height sprite sized for the 1920 × 1080 canvas. Transparent PNG or
    # lossless WebP. Width will vary with pose but should not exceed ~800 px.
    declare_image_with_fallback("stern_sprite neutral", "images/sprites/stern/neutral.png", "#555555")
    declare_image_with_fallback("stern_sprite stern", "images/sprites/stern/stern.png", "#555555")
    declare_image_with_fallback("stern_sprite angry", "images/sprites/stern/angry.png", "#555555")
    declare_image_with_fallback("stern_sprite accusing", "images/sprites/stern/accusing.png", "#555555")

    # ── Sprites: Vance ────────────────────────────────────────────
    # [~700 × 1080 px, transparent background]  (same spec as Stern above)
    declare_image_with_fallback("vance_sprite neutral", "images/sprites/vance/neutral.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite angry", "images/sprites/vance/angry.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite indignant", "images/sprites/vance/indignant.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite submissive", "images/sprites/vance/submissive.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite cowed", "images/sprites/vance/cowed.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite defeated", "images/sprites/vance/defeated.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite mirror_watch_terror", "images/sprites/vance/mirror_watch_terror.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite confused", "images/sprites/vance/confused.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite shocked", "images/sprites/vance/shocked.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite indignant_dressing_gown", "images/sprites/vance/indignant_dressing_gown.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite mirror_watch_terror_dressing_gown", "images/sprites/vance/mirror_watch_terror_dressing_gown.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite confused_dressing_gown", "images/sprites/vance/confused_dressing_gown.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite shocked_gown", "images/sprites/vance/shocked_dressing_gown.png", "#7b3f98")    
    declare_image_with_fallback("vance_sprite angry_cowed_dressing_gown", "images/sprites/vance/angry_cowed_dressing_gown.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite angry_dressing_gown", "images/sprites/vance/angry_dressing_gown.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite angry_dressing_gown_hair_down", "images/sprites/vance/angry_dressing_gown_hair_down.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite angry_dressing_gown_hair_down_front", "images/sprites/vance/angry_dressing_gown_hair_down_front.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite angry_pointing", "images/sprites/vance/angry_pointing.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite kneeling_cowed_dressing_gown", "images/sprites/vance/kneeling_cowed_dressing_gown.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite kneeling_dressing_gown_modern", "images/sprites/vance/kneeling_dressing_gown_modern.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite kneeling_dressing_ground_skin", "images/sprites/vance/kneeling_dressing_ground_skin.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite lounging_dressing_gown", "images/sprites/vance/lounging_dressing_gown.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite neutral_dressing_gown", "images/sprites/vance/neutral_dressing_gown.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite neutral_dressing_gown_dark", "images/sprites/vance/neutral_dressing_gown_dark.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite neutral_kneeling_dressing_gown", "images/sprites/vance/neutral_kneeling_dressing_gown.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite reaching_dressing_gown", "images/sprites/vance/reaching_dressing_gown.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite smiling", "images/sprites/vance/smiling.png", "#7b3f98")
    declare_image_with_fallback("vance_sprite snide", "images/sprites/vance/snide.png", "#7b3f98")

    # ── Sprites: Gideon ───────────────────────────────────────────
    # [~700 × 1080 px, transparent background]  (same spec as Stern above)
    declare_image_with_fallback("gideon_sprite cold", "images/sprites/gideon/cold.png", "#a30000")
    # neutral.png missing on disk — neutralf is interim stand-in until art pass
    declare_image_with_fallback("gideon_sprite neutral", "images/sprites/gideon/neutralf.png", "#a30000")
    declare_image_with_fallback("gideon_sprite neutralf", "images/sprites/gideon/neutralf.png", "#a30000")
    declare_image_with_fallback("gideon_sprite dominant", "images/sprites/gideon/dominant.png", "#a30000")
    declare_image_with_fallback("gideon_sprite angry", "images/sprites/gideon/angry.png", "#a30000")

    # ── Sprites: Missy ────────────────────────────────────────────
    # [~700 × 1080 px, transparent background]  (same spec as Stern above)
    declare_image_with_fallback("missy_sprite neutral", "images/sprites/missy/neutral.png", "#5fa8d3")
    declare_image_with_fallback("missy_sprite smiling", "images/sprites/missy/smiling.png", "#5fa8d3")
    declare_image_with_fallback("missy_sprite naive", "images/sprites/missy/naive.png", "#5fa8d3")
    declare_image_with_fallback("missy_sprite shocked", "images/sprites/missy/shocked.png", "#5fa8d3")
    declare_image_with_fallback("missy_sprite hesitant", "images/sprites/missy/hesitant.png", "#5fa8d3")
    declare_image_with_fallback("missy_sprite confused", "images/sprites/missy/confused.png", "#5fa8d3")

    # ── Sprites: Cora (scene-dependent) ──────────────────────────
    # [~700 × 1080 px, transparent background]  (same spec as Stern above)
    declare_image_with_fallback("cora_sprite base", "images/sprites/cora/base.png", "#d4a574")
    declare_image_with_fallback("cora_sprite base_travel", "images/sprites/cora/base_travel.png", "#d4a574")
    declare_image_with_fallback("cora_sprite guarded", "images/sprites/cora/guarded.png", "#d4a574")
    declare_image_with_fallback("cora_sprite guarded_travel", "images/sprites/cora/guarded_travel.png", "#d4a574")
    declare_image_with_fallback("cora_sprite focused", "images/sprites/cora/focused.png", "#d4a574")
    declare_image_with_fallback("cora_sprite flushed", "images/sprites/cora/flushed.png", "#d4a574")
    declare_image_with_fallback("cora_sprite collar_travel", "images/sprites/cora/collar_travel.png", "#d4a574")

    # ── UI: persistent HUD (stats_overlay) ───────────────────────
    #
    # ui_cora_base:
    #   [268 × 190 px]  Exact display size in sidebar (HUD_SIDEBAR_WIDTH - 32 × 190).
    #   Design at 2× (536 × 380 px) and let Ren'Py scale down for sharpness.
    #   Cora portrait, framed bust shot. Used at corruption_level 1–2.
    declare_image_with_fallback("ui_cora_base", "images/sprites/cora/ui/ui_cora_base.webp", "#d4a574")
    #
    # ui_cora_corrupted:
    #   [268 × 190 px]  Same dimensions as ui_cora_base (design at 2×: 536 × 380 px).
    #   Swapped in at corruption_level >= 3. Should read as visibly changed — colder,
    #   more controlled, slight desaturation or shadow shift.
    declare_image_with_fallback("ui_cora_corrupted", "images/sprites/cora/ui/ui_cora_corrupted.webp", "#8b2942")
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
    declare_image_with_fallback("ui_sidebar_divider", "images/ui/ui_sidebar_divider.png", "#2a1e0f")
    #
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
    declare_image_with_fallback("ui_inkwell_empty", "images/ui/ui_inkwell_empty.png", "#1a1a1a")
    declare_image_with_fallback("ui_inkwell_full", "images/ui/ui_inkwell_full.png", "#1e5a8a")

    # ── UI: Book Writing Screen Assets ───────────────────────────
    declare_image_with_fallback("ui_book_writing_paper", "images/ui/book_writing_paper.webp", "#f4efe2")
    declare_image_with_fallback("ui_book_cover", "images/ui/book_cover.webp", "#3d2314")
    declare_image_with_fallback("ui_book_ui_bg", "images/ui/book_ui_bg.png", "#1c1410")
    declare_image_with_fallback("ui_cora_mini_base", "images/sprites/cora/ui/ui_cora_mini_base.webp", "#d4a574")
    declare_image_with_fallback("ui_cora_mini_corrupted", "images/sprites/cora/ui/ui_cora_mini_corrupted.webp", "#8b2942")
    declare_image_with_fallback("ui_illustration_border", "images/ui/illustration_border.png", "#5a5a5a")
    declare_image_with_fallback("ui_price_badge", "images/ui/price_badge.png", "#3a1a0a")

    # ── UI: Main menu carousel [1920 × 1080 px] ──────────────────
    # Register each slide here, then add its alias to MAIN_MENU_SLIDES in menu_carousel.rpy.
    
    declare_image_with_fallback("main_menu_sweeney", "images/ui/main_menu_sweeney.png", "#1a120a")
    declare_image_with_fallback("main_menu_bride", "images/ui/main_menu_bride.png", "#1a120a")
    declare_image_with_fallback("main_menu_jekyll", "images/ui/main_menu_jekyll.png", "#1a120a")
    declare_image_with_fallback("main_menu_carmilla", "images/ui/main_menu_carmilla.png", "#1a120a")

    # ── Audio aliases (None when missing; guard before play) ──────
    audio_themes_melancholy = register_audio("themes/melancholy", "audio/themes/focus-serious-piano-solo-background-mysterious-SBA-300514033-preview.mp3")
    audio_sfx_train_whistle = register_audio("sfx/train_whistle", "audio/sfx/train-whistle-1-SBA-300283834-preview.mp3")
    audio_themes_savoy_tension = register_audio("themes/savoy_tension", "audio/themes/intrigue-and-mystery-SBA-300554190-preview.mp3")
    audio_themes_servants_floor_unease = register_audio("themes/servants_floor_unease", "audio/themes/intrigue-and-mystery-slow-SBA-352126014-preview.mp3")
    audio_themes_private_ink = register_audio("themes/private_ink", "audio/themes/hidden-corridors-SBA-346515348-preview.mp3")
    audio_themes_master_suite_pressure = register_audio("themes/master_suite_pressure", "audio/themes/book-of-secrets-mysterious-and-magical-orchestra-fantasy-SBA-347739672-preview.mp3")
    audio_themes_predator_game = register_audio("themes/predator_game", "audio/themes/somethings-happening-uneasy-chamber-strings-SBA-352568742-preview.mp3")
    audio_themes_defiance_and_dread = register_audio("themes/defiance_and_dread", "audio/themes/missteps-plucked-string-quartet-murder-mystery-podcast-secretive-quirky-and-ee-SBA-347666668-preview.mp3")

    audio_ambient_laundry_steam = register_audio("ambient/laundry_steam", "audio/ambient/steam-rise-fall-SBA-300024143-preview.mp3")
    audio_ambient_hotel_corridor_muffled = register_audio("ambient/hotel_corridor_muffled", "audio/ambient/footsteps-soft-sole-shoes-carpet-walking-SBA-300082366-preview.mp3")
    audio_ambient_servants_quarters_dusk = register_audio("ambient/servants_quarters_dusk", "audio/ambient/fireplace-crackling-ambience-01-SBA-300282371-preview.mp3")
    audio_ambient_master_suite_quiet = register_audio("ambient/master_suite_quiet", "audio/ambient/fireplace-crackling-ambience-01-SBA-300282371-preview.mp3")
    audio_ambient_fireplace_low = register_audio("ambient/fireplace_low", "audio/ambient/fireplace-crackling-ambience-01-SBA-300282371-preview.mp3")

    audio_sfx_corridor_slap_muffled = register_audio("sfx/corridor_slap_muffled", "audio/sfx/slap-SBA-300025105-preview.mp3")
    audio_sfx_floorboard_creak = register_audio("sfx/floorboard_creak", "audio/sfx/floor-creak-2-SBA-300025818-preview.mp3")
    audio_sfx_ink_scratch = register_audio("sfx/ink_scratch", "audio/sfx/pencil-writing-words-on-paper-2-SBA-300421138-preview.mp3")
    audio_sfx_washbasin_clatter = register_audio("sfx/washbasin_clatter", "audio/sfx/wire-cutters-drop-slide-metal-surface-SBA-300148274-preview.mp3")
    audio_sfx_lockpick_tension = register_audio("sfx/lockpick_tension", "audio/sfx/key-door-entrance-SBA-300020884-preview.mp3")
    audio_sfx_key_in_door = register_audio("sfx/key_in_door", "audio/sfx/locking-door-with-key-SBA-300055511-preview.mp3")
    audio_sfx_brush_drop_clatter = register_audio("sfx/brush_drop_clatter", "audio/sfx/sink-clatter-1-SBA-300021334-preview.mp3")
    audio_sfx_door_handle_jiggle = register_audio("sfx/door_handle_jiggle", "audio/sfx/locked-wooden-door-handle-moves-SBA-300055693-preview.mp3")

    # Thought overlay UI — mc_sprite_thought_icon is a placeholder until final art is created.
    declare_image_with_fallback("mc_sprite_thought_icon", "images/sprites/cora/ui/mc_sprite_thought_icon.png", "#d4a574")

    # ── Event Illustrations (CGs) ───────────────────────────────
    # [1920 × 1080 px]
    declare_image_with_fallback("cg_manuscript_retelling_d1_corridor", "images/cgs/cg_manuscript_retelling_d1_corridor.png", "#2b1c10")
    declare_image_with_fallback("cg_manuscript_retelling_d2_lace", "images/cgs/cg_manuscript_retelling_d2_lace.png", "#2b1c10")
    declare_image_with_fallback("cg_manuscript_retelling_d3_brush", "images/cgs/cg_manuscript_retelling_d3_brush.png", "#2b1c10")
    declare_image_with_fallback("cg_manuscript_retelling_d4_false_dawn", "images/cgs/cg_manuscript_retelling_d4_false_dawn.png", "#2b1c10")
    declare_image_with_fallback("cg_gideon_photograph", "images/cgs/cg_gideon_photograph.png", "#2b1c10")
    declare_image_with_fallback("cg_photograph_burning", "images/cgs/cg_photograph_burning.png", "#2b1c10")

    report_missing_assets()
