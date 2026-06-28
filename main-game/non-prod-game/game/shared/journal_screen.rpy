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

# Narrative Pressure UI: Objective Journal Screen

screen journal_screen():
    modal True
    tag menu
    zorder 90
    on "show" action Function(initialize_narrative_pressure_states)

    # Clean dark overlay behind journal
    add Solid("#09090bdf")

    # Center log frame representing Cora's diary
    frame:
        background Solid("#1c1c1f")
        padding (30, 25)
        xalign 0.5
        yalign 0.45
        xsize 900
        ysize 600
        has vbox:
            spacing 15

        # Title Block
        hbox:
            xfill True
            text "CORA'S JOURNAL" color "#c0a060" font gui.interface_text_font size 26 yalign 0.5
            textbutton "Close" action Hide("journal_screen") yalign 0.5 xalign 1.0 text_hover_color "#ff3333" text_size 14

        # Tab Navigation
        hbox:
            spacing 10
            xfill True
            
            textbutton "Current Manuscript" action SetVariable("journal_tab", "manuscript") text_color ("#c0a060" if journal_tab == "manuscript" else "#888899") text_size 13
            textbutton "Active Leads" action SetVariable("journal_tab", "active") text_color ("#c0a060" if journal_tab == "active" else "#888899") text_size 13
            textbutton "Opportunities" action SetVariable("journal_tab", "optional") text_color ("#c0a060" if journal_tab == "optional" else "#888899") text_size 13
            textbutton "Risks" action SetVariable("journal_tab", "risks") text_color ("#c0a060" if journal_tab == "risks" else "#888899") text_size 13
            textbutton "Completed & Expired" action SetVariable("journal_tab", "history") text_color ("#c0a060" if journal_tab == "history" else "#888899") text_size 13

        # Divider
        frame:
            xfill True
            ysize 1
            background Solid("#3f3f46")
            padding (0, 0)

        # Tab Content Areas
        side "c r":
            xsize 840
            ysize 440

            viewport id "journal_vp":
                xsize 820
                ysize 440
                mousewheel True
                draggable True

                vbox:
                    spacing 15
                    xfill True

                    if journal_tab == "manuscript":
                        use journal_manuscript_tab()
                    elif journal_tab == "active":
                        use journal_objectives_tab(category="story", active_only=True)
                    elif journal_tab == "optional":
                        use journal_objectives_tab(category="optional", active_only=True)
                    elif journal_tab == "risks":
                        use journal_risks_tab()
                    elif journal_tab == "history":
                        use journal_history_tab()

            vbar value YScrollValue("journal_vp") style "vscrollbar"


screen journal_manuscript_tab():
    python:
        assignment = writing_assignments.get(current_assignment_id)
        
    if not assignment:
        text "No active writing assignment." color "#888899" italic True size 14
    else:
        vbox:
            spacing 15
            xfill True
            
            # Title & Status
            hbox:
                spacing 10
                text "Title:" color "#888899" size 14
                text assignment["title"] color "#ffffff" bold True size 16
                text f"({assignment['status'].capitalize()})" color ("#22c55e" if assignment["status"] == "ready" else "#eab308") size 13 yalign 0.5

            # Required stats count
            python:
                usable_value = get_usable_material_value(current_assignment_id)
                required_value = assignment["required_material"]
                
                # Check tags and criteria in unconsumed list
                unconsumed = [m for m in manuscript_material if m.get("assignment_id") == current_assignment_id and not m.get("consumed")]
                standard_cnt = len(unconsumed)
                scandal_cnt = sum(1 for m in unconsumed if "scandal" in m.get("tags", []))
                blackmail_cnt = sum(1 for m in unconsumed if ("evidence" in m.get("tags", []) or "blackmail" in m.get("tags", [])))

            # Materials Progression Grid
            frame:
                background Solid("#27272a")
                padding (15, 12)
                xfill True
                has vbox:
                    spacing 8
                
                text "Material & Evidence Inventory" color "#c0a060" bold True size 13
                text f"- Standard Notes: {usable_value} / {required_value} value" color ("#ffffff" if usable_value >= required_value else "#a1a1aa") size 12
                text f"- Scandalous Discoveries: {scandal_cnt} collected" color "#a1a1aa" size 12
                text f"- Blackmail evidence: {blackmail_cnt} found" color "#a1a1aa" size 12

            # Collected Notes Details
            vbox:
                spacing 8
                text "Collected Notes" color "#c0a060" bold True size 13
                if unconsumed:
                    for m in unconsumed:
                        text f"• {m.get('journal_text', '')}" color "#dddddd" size 12
                else:
                    text "No notes or discoveries collected for this chapter yet." color "#71717a" italic True size 12

            # Draft Options Availability List
            vbox:
                spacing 8
                text "Available Draft Variants" color "#c0a060" bold True size 13
                
                for variant_name in ["respectable", "scandalous", "blackmail"]:
                    if variant_name in assignment["variants"]:
                        python:
                            is_unlocked = variant_name in assignment.get("available_variants", ["respectable"])
                            reqs = assignment["variants"][variant_name]
                            color_code = "#ffffff" if is_unlocked else "#71717a"
                        
                        hbox:
                            spacing 10
                            text f"- {variant_name.capitalize()} Version:" color color_code size 13
                            if is_unlocked:
                                text "Ready" color "#22c55e" size 11 yalign 0.5
                            else:
                                text f"Locked (Requires Corruption {reqs.get('required_corruption', 0)})" color "#e11d48" size 11 yalign 0.5


screen journal_objectives_tab(category, active_only=True):
    python:
        # Filter objectives
        objs = []
        for o_id, obj in objectives.items():
            if active_only and obj["status"] != "active":
                continue
            if category == "story" and obj["category"] not in ["story", "manuscript"]:
                continue
            if category == "optional" and obj["category"] != "optional":
                continue
            objs.append(obj)
            
    if not objs:
        text "No entries in this section." color "#888899" italic True size 13
    else:
        vbox:
            spacing 12
            xfill True
            for obj in objs:
                frame:
                    background Solid("#27272a")
                    padding (12, 10)
                    xfill True
                    has vbox:
                        spacing 4
                    
                    text obj["title"] color "#c0a060" bold True size 14
                    text obj["description"] color "#dddddd" size 12
                    
                    if obj.get("risk_text"):
                        text f"Risk: {obj['risk_text']}" color "#ff3333" italic True size 11
                        
                    if obj.get("focus_cost", 0) > 0:
                        text f"Focus Cost: {obj['focus_cost']} slots" color "#8f7a5a" size 11


screen journal_risks_tab():
    vbox:
        spacing 15
        xfill True
        
        text "Immediate Threats & Observers" color "#c0a060" bold True size 14
        
        python:
            # Generate risk texts based on suspicion levels
            watchers = [
                ("vance", "Vance"),
                ("gideon", "Gideon"),
                ("stern", "Ms. Stern"),
                ("missy", "Missy")
            ]
            has_any_risk = False

        for char_key, char_name in watchers:
            python:
                susp_val = suspicion.get(char_key, 0)
                is_present = character_context.get(char_key, {}).get("present", False)
                is_rel = character_context.get(char_key, {}).get("scene_relevant", False)
                
            if susp_val > 0 or is_present:
                python:
                    has_any_risk = True
                    # Categorize threat tier description
                    if susp_val >= 85:
                        tier_label = "CRITICAL RISK"
                        color_code = "#ef4444"
                    elif susp_val >= 60:
                        tier_label = "DANGEROUS"
                        color_code = "#f97316"
                    elif susp_val >= 35:
                        tier_label = "WATCHFUL"
                        color_code = "#eab308"
                    elif susp_val >= 15:
                        tier_label = "NOTICED"
                        color_code = "#a1a1aa"
                    else:
                        tier_label = "QUIET"
                        color_code = "#71717a"
                
                frame:
                    background Solid("#27272a")
                    padding (12, 10)
                    xfill True
                    hbox:
                        xfill True
                        vbox:
                            spacing 3
                            hbox:
                                spacing 8
                                text char_name color "#ffffff" bold True size 14
                                if is_present:
                                    text "[[Present in Scene]]" color "#22c55e" italic True size 11 yalign 0.5
                            text f"Current Stature: {tier_label}" color color_code size 12
                        
                        vbox:
                            xalign 1.0
                            yalign 0.5
                            text f"Suspicion Tier: {tier_label}" color color_code bold True size 11

        if not has_any_risk:
            text "Cora is currently under no immediate scrutiny. No character is watchful." color "#888899" italic True size 13


screen journal_history_tab():
    python:
        # Completed / Failed / Expired
        history_objs = [obj for obj in objectives.values() if obj["status"] in ["complete", "failed", "expired"]]
        
    if not history_objs:
        text "No completed or expired activities recorded." color "#888899" italic True size 13
    else:
        vbox:
            spacing 10
            xfill True
            for obj in history_objs:
                hbox:
                    xfill True
                    vbox:
                        text obj["title"] color "#888899" strikethrough (obj["status"] in ["failed", "expired"]) size 13
                    text obj["status"].upper() color ("#22c55e" if obj["status"] == "complete" else "#ef4444") size 11 xalign 1.0 yalign 0.5
