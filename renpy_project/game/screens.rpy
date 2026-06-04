# ═══════════════════════════════════════════════════════════════
#  screens.rpy
#  All UI screen definitions.
#  Visual design and layout live here — not in narrative files.
# ═══════════════════════════════════════════════════════════════

init -100 python:
    HUD_SIDEBAR_WIDTH = 300
    HUD_MAX_CHAPTERS  = 5

    def hud_game_viewport():
        """Left offset and width of the story viewport (pixels)."""
        if not store.hud_sidebar_visible:
            return 0, config.screen_width
        return HUD_SIDEBAR_WIDTH, config.screen_width - HUD_SIDEBAR_WIDTH

    def _hud_clear_master_layer_at():
        renpy.show_layer_at([], layer="master")

    config.start_callbacks.append(_hud_clear_master_layer_at)


# ── STAT OVERLAY ───────────────────────────────────────────────
# Left sidebar with three zones: portrait / stats / inkwell.
# Show at start:  show screen stats_overlay
# Hide on ending: hide screen stats_overlay
screen stats_overlay():
    zorder 100

    $ _susp_alpha       = player.anxiety / 100.0
    $ _insp_cap         = max(player.inspiration_cap, 1)
    $ _insp_fill        = min(1.0, player.inspiration / float(_insp_cap))
    $ _ink_w            = 64
    $ _ink_h            = 110
    $ _cora_ui          = "ui_cora_corrupted" if player.corruption_level >= 3 else "ui_cora_base"
    $ _gx, _gw          = hud_game_viewport()
    $ _roman            = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
    $ _corruption_label = _roman[min(player.corruption_level, 10)]
    $ _xp_frac          = min(1.0, player.corruption_xp / 20.0)
    $ _bar_w            = HUD_SIDEBAR_WIDTH - 32

    # Ambient vignette — always-present subtle scene framing (story area only)
    add "ui_vignette_ambient":
        xpos _gx
        xsize _gw
        ysize config.screen_height

    # Suspicion vignette — scales with anxiety (story area only)
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
                spacing 0
                xfill True
                yfill True

                # ── ZONE 1: Portrait + Identity ────────────────────────
                vbox:
                    spacing 5
                    xfill True

                    fixed:
                        xalign 0.5
                        xysize (HUD_SIDEBAR_WIDTH - 32, 190)
                        add _cora_ui:
                            xalign 0.5
                            yalign 0.5
                            xysize (HUD_SIDEBAR_WIDTH - 32, 190)

                    text "Cora" size 14 color "#c8a97e" xalign 0.5 bold True

                    hbox:
                        xalign 0.5
                        spacing 6
                        text "Day [time_manager.current_day]" size 12 color "#9a7e5a"
                        text "·" size 12 color "#5a4a2a"
                        text "[time_manager.time_of_day]" size 12 color "#9a7e5a"

                # ── Divider ────────────────────────────────────────────
                null height 10
                add "ui_sidebar_divider":
                    xalign 0.5
                    xsize _bar_w
                    ysize 10
                null height 10

                # ── ZONE 2: Stats ─────────────────────────────────────
                vbox:
                    spacing 16
                    xfill True
                    yfill True

                    # Anxiety
                    vbox:
                        spacing 5
                        xfill True
                        fixed:
                            xfill True
                            ysize 18
                            text "ANXIETY" size 10 color "#6a5030" xalign 0.0 yalign 0.5
                            text "[player.anxiety]%" size 10 color "#b87830" xalign 1.0 yalign 0.5
                        fixed:
                            xfill True
                            ysize 10
                            add Solid("#1e150a"):
                                xsize _bar_w
                                ysize 10
                            if player.anxiety > 0:
                                add Solid("#7a4a10"):
                                    xsize int(_bar_w * player.anxiety / 100)
                                    ysize 10

                    # Corruption
                    vbox:
                        spacing 5
                        xfill True
                        fixed:
                            xfill True
                            ysize 18
                            text "CORRUPTION" size 10 color "#6a5030" xalign 0.0 yalign 0.5
                            text "Lv [_corruption_label]" size 10 color "#7a2828" xalign 1.0 yalign 0.5
                        fixed:
                            xfill True
                            ysize 6
                            add Solid("#150808"):
                                xsize _bar_w
                                ysize 6
                            if _xp_frac > 0:
                                add Solid("#5a1818"):
                                    xsize int(_bar_w * _xp_frac)
                                    ysize 6

                    # Manuscript
                    vbox:
                        spacing 6
                        xfill True
                        text "MANUSCRIPT" size 10 color "#6a5030"
                        hbox:
                            spacing 8
                            for i in range(HUD_MAX_CHAPTERS):
                                if i < story.manuscript_progress:
                                    text "■" size 16 color "#c8a97e"
                                else:
                                    text "□" size 16 color "#3a2a14"

                # ── Divider ────────────────────────────────────────────
                null height 10
                add "ui_sidebar_divider":
                    xalign 0.5
                    xsize _bar_w
                    ysize 10
                null height 10

                # ── ZONE 3: Inkwell (Inspiration) ─────────────────────
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


# ── SIDEBAR ────────────────────────────────────────────────────
# Always shown — never use show/hide screen on this.
# Toggle by flipping sidebar_open; the panel slides off-screen via xpos
# so no Ren'Py window-hide transition fires and the bg never flickers.
screen sidebar():
    zorder 150

    # Panel — moves left off-screen when closed, never destroyed
    frame:
        background "#0d0d0dcc"
        xsize 260
        yfill True
        xpos (0 if sidebar_open else -260)

        vbox:
            xpadding 14 ypadding 14
            spacing 10

            # MC portrait — swap null for Add(Image("...")) when sprite is ready
            null height 220

            text "― STATS ―" xalign 0.5 size 16 color "#c8a97e"
            null height 2
            text "Day [time_manager.current_day]" size 13 color "#ffcc00"
            text "[time_manager.time_of_day]" size 12 color "#ccaa66"
            null height 4
            text "Inspiration:  [player.inspiration] / [player.inspiration_cap]" size 13 color "#4fc3f7"
            text "Corruption:   Lv [player.corruption_level]  ([player.corruption_xp] XP)" size 13 color "#ef5350"
            text "Suspicion:    [player.suspicion]%" size 13 color "#ffa726"

    # Toggle tab — tracks the panel's right edge so it's always clickable
    textbutton ("◀" if sidebar_open else "▶"):
        xpos (260 if sidebar_open else 0)
        yalign 0.5
        action ToggleVariable("sidebar_open")
        style "sidebar_toggle_btn"

style sidebar_toggle_btn:
    background "#1a1a1acc"
    hover_background "#2e2e2ecc"
    xpadding 6
    ypadding 14

style sidebar_toggle_btn_text:
    size 14
    color "#c8a97e"
    hover_color "#e8c99e"


# ── LEDGER UI ──────────────────────────────────────────────────
# Called via $ show_ledger_ui() at reflection and writing-gate moments.
# Displays current stats and per-character suspicion breakdown; player clicks to continue.
screen ledger_ui():
    modal True
    zorder 300

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
            text "Anxiety:      [player.anxiety]%" size 14 color "#ffa726"

            null height 4

            text "  Stern   [player.get_total_suspicion('stern')]%" size 12 color "#ffa72680"
            text "  Vance   [player.get_total_suspicion('vance')]%" size 12 color "#ffa72680"
            text "  Gideon  [player.get_total_suspicion('gideon')]%" size 12 color "#ffa72680"
            text "  Missy   [player.get_total_suspicion('missy')]%" size 12 color "#ffa72680"

            null height 8

            text "Chapters written:  [story.manuscript_progress]" size 14 color "#b0bec5"

            null height 16

            textbutton "Close" xalign 0.5 action Return() style "ledger_button"


style ledger_button:
    background "#2a2a2a"
    hover_background "#3d3d3d"
    padding (16, 6)

style hud_sidebar_frame is frame:
    background "ui_sidebar_bg"
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
    zorder 200
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
    zorder 200
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
