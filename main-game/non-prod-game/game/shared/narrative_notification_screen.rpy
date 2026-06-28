# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes
#
# SPRITE DIRECTION (managed by scripts/scene_direction.py — how to preserve manual staging):
# [asset auto]              -> auto-placed sprite line; the agent may rewrite/replace it on re-run
# [asset keep]              -> on a show line: lock THAT line so the agent never edits it
# [asset lock:scene]        -> before/after a `scene`: the agent skips the entire scene block
# [asset pin:Name=slot]     -> force Name into slot for the rest of the scene block
# [enter:Name] / [exit:Name] -> declare cast changes so auto placement stays correct
# Full policy: docs/contracts/sprite_layout_policy.yaml | spec: docs/specs/scene-direction-agent.md

# Narrative Pressure UI: Composite Notification Screens & Logic

init python:

    def begin_notification_bundle():
        """
        Begins a new transaction of notifications.
        All subsequent stat deltas, materials, and objectives added before flush
        will be grouped into a single visual card display.
        """
        global pending_notification_bundle
        pending_notification_bundle = {
            "level": "standard",
            "items": []
        }


    def flush_notification_bundle():
        """
        Flushes and displays the aggregated notification cards on screen.
        If any item crosses a threshold (like a suspicion breakpoint),
        the presentation rises to modal/breakpoint status.
        """
        global pending_notification_bundle
        if not pending_notification_bundle or not pending_notification_bundle["items"]:
            pending_notification_bundle = None
            return

        # Show the overlay screen passing the bundle
        renpy.show_screen("narrative_notification_overlay", bundle=pending_notification_bundle)
        
        # Clear transaction state
        pending_notification_bundle = None


# Notification Cues Theme Dictionary
define notification_theme = {
    "suspicion": {
        "color": "#8b0000",
        "icon": "👁",
        "label": "Suspicion"
    },
    "corruption": {
        "color": "#4b0082",
        "icon": "✒",
        "label": "Corruption"
    },
    "inspiration": {
        "color": "#d2b48c",
        "icon": "🪶",
        "label": "Inspiration"
    },
    "objective": {
        "color": "#c0a060",
        "icon": "📋",
        "label": "Objective"
    },
    "opportunity": {
        "color": "#8f7a5a",
        "icon": "⏳",
        "label": "Opportunity"
    }
}


screen narrative_notification_overlay(bundle=None):
    # Ensure overlay sits on top of typical panels
    zorder 100

    if bundle:
        python:
            scr = renpy.current_screen()
            if scr:
                scr.modal = (bundle.get("level") == "breakpoint")
        # Outer frame container aligned to top-right
        frame:
            background Solid("#151518ee") # Dark translucent background
            xalign 0.95
            yalign 0.05
            xminimum 320
            xmaximum 450
            padding (15, 15)
            has vbox:
                spacing 12

            # Header indicating standard bundle or breakpoint warning
            if bundle.get("level") == "breakpoint":
                text "CRITICAL PRESSURE DETECTED" color "#ff3333" bold True size 14 xalign 0.5
            else:
                text "NOTIFICATIONS" color "#888899" size 11 kerning 1.0 xalign 0.5

            # Render each notification list item
            for item in bundle.get("items", []):
                python:
                    item_type = item.get("type", "inspiration")
                    theme = notification_theme.get(item_type, notification_theme["inspiration"])
                    color_hex = theme["color"]
                    icon_char = theme["icon"]
                    label_text = theme["label"]

                hbox:
                    spacing 12
                    # Left icon container
                    frame:
                        background Solid(color_hex)
                        xsize 30
                        ysize 30
                        padding (0, 0)
                        text icon_char size 18 color "#ffffff" align (0.5, 0.5)

                    # Right text content block
                    vbox:
                        spacing 2
                        text item.get("title", label_text) color color_hex bold True size 13
                        if item.get("body"):
                            text item.get("body") color "#dddddd" size 12

            # Close action button for modal breakpoints
            if bundle.get("level") == "breakpoint":
                null height 5
                button:
                    background Solid("#333338")
                    padding (8, 5)
                    xalign 0.5
                    hover_background Solid("#ff3333")
                    action Hide("narrative_notification_overlay")
                    text "Acknowledge" color "#ffffff" size 12 align (0.5, 0.5)
            else:
                # Auto-dismiss timer for standard notifications
                timer 3.5 action Hide("narrative_notification_overlay")

