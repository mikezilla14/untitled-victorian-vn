# ═══════════════════════════════════════════════════════════════
#  screens.rpy
#  All UI screen definitions.
#  Visual design and layout live here — not in narrative files.
# ═══════════════════════════════════════════════════════════════

# ── STAT OVERLAY ───────────────────────────────────────────────
# Placeholder HUD displayed during gameplay.
# Show at start:  show screen stats_overlay
# Hide on ending: hide screen stats_overlay
screen stats_overlay():
    zorder 100
    frame:
        xalign 0.0 yalign 0.0
        xpadding 10 ypadding 10
        background "#00000088"
        vbox:
            text "Day [time_manager.current_day] — [time_manager.time_of_day]"              size 16 color "#ffcc00"
            text "Inspiration: [player.inspiration]"                      size 14 color "#4fc3f7"
            text "Corruption: Lvl [player.corruption_level] ([player.corruption_xp] XP)" size 14 color "#ef5350"
            text "Suspicion: [player.suspicion]%"                         size 14 color "#ffa726"

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
# Displays current stats and manuscript progress; player clicks to continue.
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
            text "Suspicion:    [player.suspicion]%" size 14 color "#ffa726"

            null height 8

            text "Chapters written:  [story.manuscript_progress]" size 14 color "#b0bec5"

            null height 16

            textbutton "Close" xalign 0.5 action Return() style "ledger_button"

style ledger_button:
    background "#2a2a2a"
    hover_background "#3d3d3d"
    padding (16, 6)

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

    frame:
        id "window"
        background Solid("#000000ee")
        xalign 0.5
        yalign 1.0
        xfill True
        ysize 280
        xpadding 100
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

    vbox:
        xalign 0.5
        yalign 0.5
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
