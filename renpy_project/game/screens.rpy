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

# ── FUTURE SCREENS ─────────────────────────────────────────────
# Add new screens here as the project grows:
#   screen writing_desk():   ...
#   screen payment_notice(): ...
#   screen chapter_select(): ...

# ── DEFAULT REN'PY UI OVERRIDES ──────────────────────────────────
# Required to prevent dialogue from rendering at (0,0) without a box.

screen say(who, what):
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
