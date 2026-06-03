#
#
#
#
#

define UI_LEFT = 300

init python:
    def vp_x(frac):
        return UI_LEFT + int((config.screen_width - UI_LEFT) * frac)


transform right_bust:
    crop (200, 0, 800, 1000)
    zoom 0.8
    xanchor 0.5
    xpos vp_x(0.8)
    ypos 1.0
    yalign 1.0

transform centre_bust:
    crop (200, 0, 800, 1000)
    zoom 0.8
    xanchor 0.5
    xpos vp_x(0.5)
    ypos 1.0
    yalign 1.0    

transform left_bust:
    crop (200, 0, 800, 1000)
    zoom 0.8
    xanchor 0.5
    xpos vp_x(0.2)
    ypos 1.0
    yalign 1.0

# ── Four-character slots ────────────────────────────────────────
# Placeholder vp_x fractions + zoom; tune visually later.
# The Scene Direction Agent only ever emits the canonical names below.

transform left_bust4:
    crop (200, 0, 800, 1000)
    zoom 0.7
    xanchor 0.5
    xpos vp_x(0.12)
    ypos 1.0
    yalign 1.0

transform centre_left_bust4:
    crop (200, 0, 800, 1000)
    zoom 0.7
    xanchor 0.5
    xpos vp_x(0.38)
    ypos 1.0
    yalign 1.0

transform centre_right_bust4:
    crop (200, 0, 800, 1000)
    zoom 0.7
    xanchor 0.5
    xpos vp_x(0.62)
    ypos 1.0
    yalign 1.0

transform right_bust4:
    crop (200, 0, 800, 1000)
    zoom 0.7
    xanchor 0.5
    xpos vp_x(0.88)
    ypos 1.0
    yalign 1.0

# Defensive aliases for legacy/manual usage. Canonical output never uses these;
# the agent folds left_centre_bust4 -> centre_left_bust4, right_centre_bust4 -> centre_right_bust4.
transform left_centre_bust4:
    crop (200, 0, 800, 1000)
    zoom 0.7
    xanchor 0.5
    xpos vp_x(0.38)
    ypos 1.0
    yalign 1.0

transform right_centre_bust4:
    crop (200, 0, 800, 1000)
    zoom 0.7
    xanchor 0.5
    xpos vp_x(0.62)
    ypos 1.0
    yalign 1.0

transform right_reframe:
    crop (300, 0, 500, 1000)
    zoom 0.7
    xanchor 0.5
    xpos 0.85
    ypos 1.0
    yalign 1.0

transform right_reframe_mirror:
    crop (300, 0, 500, 1000)
    zoom 0.7
    xanchor 0.5
    xpos 0.65
    ypos 1.0
    xzoom -1.0    
    
transform left_reframe:
    crop (300, 0, 500, 1000)
    zoom 0.7
    xanchor 0.5
    xpos vp_x(0.2)
    yalign 1.0
    xzoom -1.0

transform left_reframe_mirror:
    crop (300, 0, 500, 1000)
    zoom 0.7
    xanchor 0.5
    xpos vp_x(0.2)
    yalign 1.0

transform right_full_body:
    zoom 0.60
    ypos 1.06   
    xanchor 0.5
    xpos vp_x(0.8)
    yalign 1.0

transform centre_full_body:
    zoom 0.60
    ypos 1.06   
    xanchor 0.5
    xpos vp_x(0.5)
    yalign 1.0    

transform left_full_body:
    zoom 0.60
    ypos 1.06   
    xanchor 0.5
    xpos vp_x(0.2)
    yalign 1.0         



