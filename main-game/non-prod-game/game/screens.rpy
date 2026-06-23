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

    $ _insp_cap         = max(player.inspiration_cap, 1)
    $ _insp_fill        = min(1.0, player.inspiration / float(_insp_cap))
    $ _ink_w            = 300
    $ _ink_h            = 300
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
        alpha 0.0

    if hud_sidebar_visible:
        frame:
            style "hud_sidebar_frame"
            xpos 0
            yalign 0.5
            yfill True
            xsize HUD_SIDEBAR_WIDTH

            # Top Section: Portrait and Stats
            vbox:
                xalign 0.5
                xsize _bar_w
                yalign 0.0
                spacing 16

                # ── ZONE 1: Portrait + Identity ────────────────────────
                vbox:
                    spacing 8
                    xfill True

                    fixed:
                        xalign 0.5
                        xysize (_bar_w, 190)
                        add _cora_ui:
                            xalign 0.5
                            yalign 0.5
                            xysize (HUD_SIDEBAR_WIDTH - 130, 240)

                    text "Cora" size 16 color "#c8a97e" xalign 0.5 bold True

                    hbox:
                        xalign 0.5
                        spacing 6
                        text "Day [time_manager.current_day]" size 14 color "#9a7e5a"
                        text "·" size 14 color "#5a4a2a"
                        text "[time_manager.time_of_day]" size 14 color "#9a7e5a"

                # ── Divider ────────────────────────────────────────────
                add "ui_sidebar_divider":
                    xalign 0.5
                    xsize _bar_w
                    ysize 10

                # ── ZONE 2: Stats ─────────────────────────────────────
                vbox:
                    spacing 20
                    xfill True

                    # Anxiety
                    vbox:
                        spacing 6
                        xfill True
                        fixed:
                            xsize _bar_w
                            ysize 20
                            text "ANXIETY" size 12 color "#6a5030" xalign 0.0 yalign 0.5
                            text "[player.anxiety]%" size 12 color "#b87830" xalign 1.0 yalign 0.5
                        fixed:
                            xsize _bar_w
                            ysize 12
                            add Solid("#1e150a"):
                                xsize _bar_w
                                ysize 12
                            if player.anxiety > 0:
                                add Solid("#7a4a10"):
                                    xsize int(_bar_w * player.anxiety / 100)
                                    ysize 12

                    # Corruption
                    vbox:
                        spacing 6
                        xfill True
                        fixed:
                            xsize _bar_w
                            ysize 20
                            text "CORRUPTION" size 12 color "#6a5030" xalign 0.0 yalign 0.5
                            text "Lv [_corruption_label]" size 12 color "#7a2828" xalign 1.0 yalign 0.5
                        fixed:
                            xsize _bar_w
                            ysize 12
                            add Solid("#150808"):
                                xsize _bar_w
                                ysize 12
                            if _xp_frac > 0:
                                add Solid("#5a1818"):
                                    xsize int(_bar_w * _xp_frac)
                                    ysize 12

                    # Manuscript
                    vbox:
                        spacing 8
                        xfill True
                        text "MANUSCRIPT" size 12 color "#6a5030"
                        hbox:
                            spacing 8
                            for i in range(HUD_MAX_CHAPTERS):
                                if i < story.manuscript_progress:
                                    text "■" size 18 color "#c8a97e"
                                else:
                                    text "□" size 18 color "#3a2a14"

            # Bottom Section: Inkwell (Inspiration)
            vbox:
                xalign 0.5
                xsize _bar_w
                yalign 1.0
                spacing 16

                # ── Divider ────────────────────────────────────────────
                add "ui_sidebar_divider":
                    xalign 0.5
                    xsize _bar_w
                    ysize 10

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
                            xsize=_ink_w,
                            ysize=int(_ink_h * _insp_fill),
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
# Displays current stats and per-character suspicion breakdown; player clicks to continue.
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


screen suspicion_attention(character):
    zorder 210

    $ _gx, _gw = hud_game_viewport()
    $ _name = SUSPICION_CHARACTER_NAMES.get(character, character.title())
    $ _tier = suspicion_tier(player.get_total_suspicion(character)).upper()
    $ _alpha = 0.95 if suspicion_focus_intensity >= 2 else 0.72
    $ _border = "#c8a97e" if suspicion_focus_intensity >= 2 else "#7a4a10"

    frame:
        xpos 0.4
        ypos 0.5
        xanchor 0.5
        yanchor 0.5
        xpadding 14
        ypadding 8
        background Solid("#0d0d0dcc")

        hbox:
            spacing 10
            at Transform(alpha=_alpha)
            text "EYE" size 14 color _border bold True
            text _name size 14 color "#dfcbb5" bold True
            text _tier size 12 color "#9a7e5a"


# ── THOUGHT OVERLAY ────────────────────────────────────────────
# Dual-layer dialogue + internal monologue system.
# Usage: cora_inner has screen="thought_overlay" wired in characters.rpy
# Writer contract: cora_inner "text"  — freezes last speaker on screen.
# Assets required (not yet created): images/sprites/ui/mc_sprite_thought_icon.png
#   Fallback: solid colour block registered in assets_manifest.rpy.

init python:
    def get_anchor_dialogue():
        """Returns the line immediately before this thought if it was a named speaker.
        _history_list[-1] is the current cora_inner entry (already appended before
        the screen renders), so we check [-2] for the preceding line."""
        if len(_history_list) >= 2 and _history_list[-2].who is not None:
            return _history_list[-2]
        return None

transform thought_fade:
    alpha 0.0
    linear 0.5 alpha 1.0

style thought_text:
    font "DejaVuSans.ttf"
    size 28
    color "#f5f0e8"
    line_leading 6

screen thought_overlay(who, what):
    # LAYER 1: Freeze the last external speaker's line on screen.
    # Only rendered when a named character preceded this thought.
    $ anchor_line = get_anchor_dialogue()
    if anchor_line:
        frame:
            xpos HUD_SIDEBAR_WIDTH
            xsize config.screen_width - HUD_SIDEBAR_WIDTH
            yalign 1.0
            background Solid("#000000cc")
            padding (60, 20, 60, 30)
            vbox:
                spacing 8
                if anchor_line.who:
                    text anchor_line.who style "say_label"
                text anchor_line.what style "say_dialogue"

    # LAYER 2: Isolated thought UI — locked to story viewport (xpos 300).
    fixed:
        xpos 300
        ypos 100
        xysize (1620, 1080)

        # Icon — left anchor for the thought bubble row
        add "mc_sprite_thought_icon":
            at thought_fade
            crop (150, 0, 500, 500)
            zoom 1.2
            xysize (80, 80)
            xpos 60
            ypos 20

        # Bubble — explicit position and size so xsize is honoured
        frame:
            at thought_fade
            xpos 160
            ypos 0
            xmaximum 1380
            background Frame("gui/thoughtbubble.png", 30, 30)
            padding (40, 30)

            text what style "thought_text" id "what"


# ── PENNY DREADFUL BOOK WRITING SCREEN ───────────────────────────
# Overrides standard NVL mode rendering for chapter writing events.
#
# Right-panel layout (1920x1080, right half x:960-1920):
#   ypos  40-125   Masthead / chapter title
#   ypos 125-165   Route-provenance subtitle
#   ypos 165-785   Illustration frame (620px tall)
#   ypos 800-840   Plate caption / image caption
#   ypos 850-920   Publisher footer / price badge
#   (Stats HUD removed — book is emotional escape, not a pressure dashboard)
#
# plate mode applies runtime sepia/hatch treatment to the current image.
# Hand-finished plate_book_* assets bypass the transform entirely.

# Runtime Victorian plate treatment.
# Applied to the illustration in plate mode.
# Requires Ren'Py 7.4+ matrixcolor ATL support.
transform book1_plate_treatment:
    matrixcolor SepiaMatrix(0.9) * ContrastMatrix(1.12)


screen nvl(dialogue, items=None):
    # Left side: Manuscript Paper
    add "ui_book_writing_paper" xpos 0 ypos 0

    # Right side Panel Wrapper
    frame:
        xpos 960
        ypos 0
        xysize (960, 1080)
        background None
        padding (0, 0)

        # 1. Masthead — static title, or dynamic chapter title if set
        $ _b1_chapter_title = getattr(store, "book1_chapter_title", "")
        $ _b1_subtitle      = getattr(store, "book1_chapter_subtitle", "")

        vbox:
            xpos 96
            ypos 40
            xsize 768
            spacing 2

            if _b1_chapter_title:
                text "[_b1_chapter_title]" size 28 bold True color "#2c1b17" xalign 0.5
            else:
                text "CORALIE VALE;" size 32 bold True color "#2c1b17" xalign 0.5
                text "OR," size 18 italic True color "#2c1b17" xalign 0.5
                text "THE TERROR OF THE SAVOY CORRIDORS." size 22 bold True color "#2c1b17" xalign 0.5

            # Route-provenance subtitle (visible when set by book1_set_chapter_title)
            if _b1_subtitle:
                null height 6
                text "— [_b1_subtitle] —" size 16 italic True color "#7a5c3c" xalign 0.5

        # 2. Illustration Frame (expanded to fill space from removed HUD)
        $ _b1_page_image = getattr(store, "book1_page_image", "ui_book_cover")
        $ _b1_page_mode  = getattr(store, "book1_page_mode", "cover")

        frame:
            xpos 96
            ypos 165
            xysize (768, 620)
            background Frame("ui_illustration_border", 6, 6)
            padding (10, 10)

            if _b1_page_mode == "plate":
                # Runtime plate treatment: sepia/contrast matrix + overlay layers
                add _b1_page_image at book1_plate_treatment xalign 0.5 yalign 0.5 xysize (748, 600)
                add "ui_book_plate_paper_overlay"      xalign 0.5 yalign 0.5 xysize (748, 600)
                add "ui_book_plate_hatch_overlay"      xalign 0.5 yalign 0.5 xysize (748, 600)
                add "ui_illustration_border_plate"     xalign 0.5 yalign 0.5
            else:
                add _b1_page_image xalign 0.5 yalign 0.5 xysize (748, 600)

        # 3. Plate / Image Caption (visible when set)
        $ _b1_caption = getattr(store, "book1_plate_caption", "")
        if _b1_caption:
            frame:
                xpos 96
                ypos 800
                xysize (768, 40)
                background None
                text "[_b1_caption]" size 16 italic True color "#3a2510" xalign 0.5 yalign 0.5

        # 4. Price Banner & Publisher Slug Footer
        frame:
            xpos 96
            ypos 850
            xysize (768, 70)
            background None

            hbox:
                xalign 0.1
                yalign 0.5
                add "ui_price_badge" xysize (140, 40)

            text "LONDON: PRINTED AND PUBLISHED BY SIR GIDEON LOCKE, SAVOY STRAND." size 14 color "#5f5f5f" xalign 0.5 yalign 0.5

    # Manuscript Text Viewport (Left Side)
    window:
        id "window"
        background None
        xpos 100
        ypos 100
        xysize (760, 880)
        padding (40, 40)

        vbox:
            spacing 20

            # Author thought marginalia — sparse pencilled composition notes.
            # Visible only when book1_author_thought is non-empty.
            # Rendered above the prose, visually separate from manuscript text.
            $ _b1_thought = getattr(store, "book1_author_thought", "")
            if _b1_thought:
                text "[_b1_thought]" size 18 italic True color "#7a6050" xalign 0.0
                null height 8

            # NVL dialogue text
            for d in dialogue:
                window:
                    id d.window_id
                    background None

                    vbox:
                        if d.who:
                            text d.who:
                                id d.who_id
                                bold True
                                size 36
                                color "#261c14"
                                xalign 0.5
                            null height 20
                        text d.what:
                            id d.what_id
                            size 28
                            color "#261c14"
                            line_leading 6
                            justify True


# ── BALANCE DEBUG OVERLAY (non-prod only; F10) ─────────────────
screen debug_grain_overlay_toggle():
    zorder 200
    key "toggle_debug_grain_overlay" action Function(toggle_debug_grain_overlay)


screen debug_grain_overlay():
    zorder 199
    if debug_grain_overlay_visible:
        frame:
            xalign 1.0
            yalign 0.0
            xpadding 12
            ypadding 8
            background "#000000aa"

            vbox:
                spacing 4
                text "Balance debug (F10)" size 14 color "#ffd166" bold True
                text "Label: [balance_capture.current_label]" size 13 color "#ffffff"
                text "Day [time_manager.current_day] · [time_manager.time_of_day]" size 13 color "#cccccc"
                text "Insp [player.inspiration]/[player.inspiration_cap] · Corr L[player.corruption_level] · MS [story.manuscript_progress]" size 13 color "#cccccc"
                if balance_capture.active:
                    text "CAPTURE: [balance_capture.run_id] (#[balance_capture.sequence])" size 13 color "#06d6a0"
                else:
                    text "Capture off — use debug menu or `jump debug_capture_start`" size 12 color "#888888"

                text "Matrix runs (restart from prologue):" size 11 color "#888888"
                hbox:
                    spacing 6
                    textbutton "P1" action [Function(balance_capture.start, "P1_corruption_forward"), Jump("start")] text_size 11
                    textbutton "P2" action [Function(balance_capture.start, "P2_cautious"), Jump("start")] text_size 11
                    textbutton "P3" action [Function(balance_capture.start, "P3_low_corruption"), Jump("start")] text_size 11
                    textbutton "P4" action [Function(balance_capture.start, "P4_deadline_1"), Jump("start")] text_size 11
                hbox:
                    spacing 6
                    textbutton "P5" action [Function(balance_capture.start, "P5_deadline_2"), Jump("start")] text_size 11
                    textbutton "P6" action [Function(balance_capture.start, "P6_anxiety_collapse"), Jump("start")] text_size 11
                    textbutton "P7" action [Function(balance_capture.start, "P7_penance"), Jump("start")] text_size 11
                hbox:
                    spacing 8
                    textbutton "Stop" action Function(balance_capture.stop, "overlay_stop") text_size 12
                    textbutton "Hide" action [SetVariable("debug_grain_overlay_visible", False), Hide("debug_grain_overlay")] text_size 12


# ── DAY/TIME TRANSITION SCREEN ──────────────────────────────────
# Centrally styled day/time transition screens.
style time_transition_day_text:
    size 40
    color "#c8a97e"
    xalign 0.5
    bold True

style time_transition_period_text:
    size 28
    color "#dfcbb5"
    xalign 0.5
    italic True

screen time_transition_screen(day, period):
    modal True
    zorder 300 # Displays above stats overlay (zorder 100) and say screen

    # Dismiss on keyboard/gamepad dismiss keys
    key "dismiss" action Return()

    # Dismiss on click anywhere
    button:
        action Return()
        xfill True
        yfill True
        background None # Invisible button

    add Solid("#000000") # Full black screen

    vbox:
        align (0.5, 0.5)
        spacing 15

        text "DAY [day]" style "time_transition_day_text"
        
        # Muted gold horizontal separator
        add Solid("#9a7e5a"):
            xalign 0.5
            xsize 120
            ysize 2

        text "[period]" style "time_transition_period_text"

label time_transition_label(day, period):
    # Hide the HUD stats overlay so it doesn't stand out over the black screen
    hide screen stats_overlay
    
    # Show the transition screen
    show screen time_transition_screen(day, period)
    
    # Fade to black
    with fade

    # Pause for 2.0 seconds (player can click to dismiss)
    $ renpy.pause(2.0)

    # Hide transition screen
    hide screen time_transition_screen
    
    # Fade back to the game scene
    with fade

    # Restore the stats overlay HUD
    show screen stats_overlay
    return

