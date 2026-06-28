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

# Narrative Pressure UI: Overlay HUD Screen

init python:
    # Register the HUD overlay centrally to be rendered by Ren'Py automatically
    config.overlay_screens.append("narrative_hud")

screen narrative_hud():
    python:
        initialize_narrative_pressure_states()
    # Only render when enabled, not in cinematic mode, not during choice blocks
    if hud_enabled and not cinema_mode and not renpy.get_screen("choice") and not renpy.get_screen("main_menu"):
        
        # Upper left corner: Stat summaries & watch threat indicator
        frame:
            background Solid("#1c1c1fcc") # Translucent dark background
            padding (10, 8)
            xalign 0.02
            yalign 0.02
            xsize 280
            has vbox:
                spacing 4
            
            # 1. Manuscript Readiness State
            python:
                assignment = writing_assignments.get(current_assignment_id)
                
            if assignment:
                python:
                    usable_val = get_usable_material_value(current_assignment_id)
                    required_val = assignment["required_material"]
                    status_text = assignment["status"].capitalize()
                    status_color = "#22c55e" if assignment["status"] == "ready" else "#eab308"
                
                hbox:
                    spacing 8
                    text "Manuscript:" color "#888899" size 11
                    text f"{status_text} ({usable_val}/{required_val})" color status_color bold True size 11 yalign 0.5
            else:
                text "Manuscript: None active" color "#71717a" size 11

            # 2. Watch Scrutiny Risk (Highest scene threat)
            python:
                risk_char = get_hud_risk_character()
                
            if risk_char:
                python:
                    susp_val = suspicion.get(risk_char, 0)
                    if susp_val >= 85:
                        risk_desc = "Critical Scrutiny"
                        risk_color = "#ef4444"
                    elif susp_val >= 60:
                        risk_desc = "Dangerous"
                        risk_color = "#f97316"
                    elif susp_val >= 35:
                        risk_desc = "Watching"
                        risk_color = "#eab308"
                    elif susp_val >= 15:
                        risk_desc = "Noticed"
                        risk_color = "#a1a1aa"
                    else:
                        risk_desc = "Watchful"
                        risk_color = "#71717a"
                hbox:
                    spacing 8
                    text "Local Threat:" color "#888899" size 11
                    text f"{risk_char.capitalize()} ({risk_desc})" color risk_color bold True size 11 yalign 0.5
            else:
                text "Local Threat: None immediate" color "#22c55e" size 11

            # 3. Focus and Opportunities
            hbox:
                spacing 8
                text "Focus Slots:" color "#888899" size 11
                text f"{chapter_focus_remaining} slots" color "#8f7a5a" bold True size 11

        # Upper right corner: Interactive Journal Button with "Updated" indicator
        button:
            background Solid("#1c1c1fcc")
            hover_background Solid("#27272acc")
            padding (10, 8)
            xalign 0.98
            yalign 0.02
            action [SetVariable("journal_updated_indicator", False), Show("journal_screen")]
            
            hbox:
                spacing 8
                text "📋 Journal" color "#c0a060" bold True size 12 yalign 0.5
                if journal_updated_indicator:
                    # Small gold alert dot
                    frame:
                        background Solid("#eab308")
                        xsize 8
                        ysize 8
                        padding (0, 0)
                        yalign 0.5
