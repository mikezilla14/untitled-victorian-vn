# ═══════════════════════════════════════════════════════════════
#  screens.rpy
#  All UI screen definitions.
#  Visual design and layout live here — not in narrative files.
# ═══════════════════════════════════════════════════════════════

init -100 python:
    HUD_SIDEBAR_WIDTH = 300

    def hud_game_viewport():
        """Left offset and width of the story viewport (pixels)."""
        if not store.hud_sidebar_visible:
            return 0, config.screen_width
        return HUD_SIDEBAR_WIDTH, config.screen_width - HUD_SIDEBAR_WIDTH

    def hud_viewport_update(trans, st, at):
        """ATL function: scale master layer to the story area. Returns pause seconds."""
        sb, game_w = hud_game_viewport()
        if sb == 0:
            trans.xalign = 0.5
            trans.yalign = 0.5
            trans.xoffset = 0
            trans.xzoom = 1.0
            trans.yzoom = 1.0
        else:
            scale = float(game_w) / float(config.screen_width)
            trans.xalign = 0.0
            trans.yalign = 0.5
            trans.xoffset = int(sb)
            trans.xzoom = scale
            trans.yzoom = scale
        trans.subpixel = True
        return 0

    def hud_bind_master_viewport():
        renpy.show_layer_at(hud_master_viewport, layer="master")

    def hud_scene_callback(layer):
        if layer == "master":
            hud_bind_master_viewport()

    config.start_callbacks.append(hud_bind_master_viewport)
    config.scene_callbacks.append(hud_scene_callback)


transform hud_master_viewport:
    function hud_viewport_update


# ── STAT OVERLAY ───────────────────────────────────────────────
# Twine-style left sidebar; master layer scales to the story area when visible.
# Show at start:  show screen stats_overlay
# Hide on ending: hide screen stats_overlay
screen stats_overlay():
    zorder 100

    $ _susp_alpha = player.suspicion / 100.0
    $ _insp_cap = max(player.inspiration_cap, 1)
    $ _insp_fill = min(1.0, player.inspiration / float(_insp_cap))
    $ _ink_w = 56
    $ _ink_h = 120
    $ _cora_ui = "ui_cora_corrupted" if player.corruption_level >= 3 else "ui_cora_base"
    $ _gx, _gw = hud_game_viewport()

    # Suspicion vignette — story area only (not over the sidebar).
    add "ui_suspicion_vignette":
        xpos _gx
        xsize _gw
        ysize config.screen_height
        alpha _susp_alpha

    if hud_sidebar_visible:
        frame:
            style "hud_sidebar_frame"
            xpos 0
            yalign 0.5
            yfill True
            xsize HUD_SIDEBAR_WIDTH

            vbox:
                spacing 16
                xfill True
                yfill True

                # Top — Cora portrait
                fixed:
                    xalign 0.5
                    xysize (HUD_SIDEBAR_WIDTH - 32, 220)

                    add _cora_ui:
                        xalign 0.5
                        yalign 0.5
                        xysize (HUD_SIDEBAR_WIDTH - 32, 220)

                # Middle — game-state readouts
                vbox:
                    spacing 8
                    xfill True
                    yfill True

                    text "Day [time_manager.current_day]" size 16 color "#ffcc00" xalign 0.5
                    text "[time_manager.time_of_day]" size 14 color "#c8a97e" xalign 0.5

                    null height 8

                    text "Inspiration" size 12 color "#4fc3f799" xalign 0.5
                    text "[player.inspiration] / [player.inspiration_cap]" size 15 color "#4fc3f7" xalign 0.5

                    text "Corruption" size 12 color "#ef535099" xalign 0.5
                    text "Lv [player.corruption_level]  ([player.corruption_xp] XP)" size 15 color "#ef5350" xalign 0.5

                    text "Suspicion" size 12 color "#ffa72699" xalign 0.5
                    text "[player.suspicion]%" size 15 color "#ffa726" xalign 0.5

                    text "Manuscript" size 12 color "#b0bec599" xalign 0.5
                    text "[story.manuscript_progress] chapters" size 15 color "#b0bec5" xalign 0.5

                # Bottom — inkwell meter
                fixed:
                    xalign 0.5
                    xysize (_ink_w, _ink_h)

                    add "ui_inkwell_empty":
                        xysize (_ink_w, _ink_h)
                        xalign 0.5
                        yalign 0.5

                    if _insp_fill > 0:
                        add Transform(
                            "ui_inkwell_full",
                            crop=(0.0, 1.0 - _insp_fill, 1.0, _insp_fill),
                            xysize=(_ink_w, _ink_h),
                        ):
                            xalign 0.5
                            yalign 1.0

        textbutton "◂":
            style "hud_sidebar_tab"
            xpos HUD_SIDEBAR_WIDTH - 4
            yalign 0.5
            action SetVariable("hud_sidebar_visible", False)

    else:
        textbutton "▸":
            style "hud_sidebar_tab"
            xpos 0
            yalign 0.5
            action SetVariable("hud_sidebar_visible", True)

# ── LEDGER UI ──────────────────────────────────────────────────
# Called via $ show_ledger_ui() at reflection and writing-gate moments.
# Displays current stats and manuscript progress; player clicks to continue.
screen ledger_ui():
    modal True
    zorder 200

    frame:
        xalign 0.5 yalign 0.4
        xpadding 30 ypadding 24
        background "#0d0d0dcc"

        vbox:
            spacing 8

            text "― THE LEDGER ―" xalign 0.5 size 18 color "#c8a97e"

            null height 8

            text "Inspiration:  [player.inspiration] / [player.inspiration_cap]" size 14 color "#4fc3f7"
            text "Corruption:   Lv [player.corruption_level]  ([player.corruption_xp] XP)" size 14 color "#ef5350"
            text "Suspicion:    [player.suspicion]%" size 14 color "#ffa726"

            null height 8

            text "Chapters written:  [story.manuscript_progress]" size 14 color "#b0bec5"

            null height 16

            textbutton "Close" xalign 0.5 action Return() style "ledger_button"

style ledger_button:
    background "#2a2a2a"
    hover_background "#3d3d3d"
    padding (16, 6)

style hud_sidebar_frame is frame:
    background "#0d0d0df2"
    padding (16, 20)

style hud_sidebar_tab is button:
    background "#1a1a1acc"
    hover_background "#2a2a2aee"
    padding (8, 16)
    xsize 36

# ── FUTURE SCREENS ─────────────────────────────────────────────
# Add new screens here as the project grows:
#   screen writing_desk():   ...
#   screen payment_notice(): ...
#   screen chapter_select(): ...

# ── DEFAULT REN'PY UI OVERRIDES ──────────────────────────────────
# Required to prevent dialogue from rendering at (0,0) without a box.

screen say(who, what):
    style_prefix "say"

    $ _gx, _gw = hud_game_viewport()

    frame:
        id "window"
        background Solid("#000000ee")
        xpos _gx
        xsize _gw
        yalign 1.0
        ysize 280
        xpadding 48
        ypadding 30

        if who is not None:
            text who:
                id "who"
                bold True
                size 32
                ypos 0
                color "#ffffff"

        text what:
            id "what"
            size 28
            color "#eeeeee"
            ypos 40


screen choice(items):
    style_prefix "choice"

    $ _gx, _gw = hud_game_viewport()

    vbox:
        xanchor 0.5
        xpos _gx + (_gw // 2)
        yalign 0.5
        xmaximum _gw - 80
        spacing 10

        for i in items:
            textbutton i.caption:
                action i.action
                text_size 22
                text_color "#ffffff"
                text_hover_color "#ffcc00"
                background Solid("#000000aa")
                hover_background Solid("#222222ee")
                xpadding 20 ypadding 10
