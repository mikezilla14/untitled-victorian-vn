# Narrative Pressure UI: Interactive Playtest & Integration Verification label

# This label can be jumped to from the Ren'Py console during development to manually smoke-test.

label test_narrative_pressure_system:

    # 1. Initialize variables & enable HUD
    $ hud_enabled = True
    $ cinema_mode = False
    $ journal_updated_indicator = False
    $ begin_notification_bundle()
    $ activate_objective("obj_assignment_01_material")
    $ flush_notification_bundle()

    "Narrative Pressure System: Playtest initialized. Check the upper-left corner of the screen for the active HUD."

    # 2. Set Context: Cora is in the Servants' Corridor. Stern is present and watches her.
    $ set_scene_context(location="servants_corridor", present=["stern"], relevant=["stern"])
    
    "Cora stands in the corridor. Ms. Stern is present."
    "The HUD local threat should prioritize Ms. Stern."

    # 3. Choice: safe chore vs risky eavesdropping
    menu:
        "What does Cora do?"

        "Perform standard chores. [[Safe Detail: 1 focus, Tier 1 material]]":
            $ begin_notification_bundle()
            $ spend_focus(1)
            $ add_material("mat_safe_chore_detail")
            $ flush_notification_bundle()
            
            cora_inner "I scrub the grates diligently. Eleanor shifts some linens nervously, paying me no mind."
            cora_inner "It is thin material, but it is safe."

        "Lingers by Ms. Stern's office door. [[Improper Discovery: 2 focus, Tier 2 material, Suspicion Risk]]":
            $ begin_notification_bundle()
            $ spend_focus(2)
            $ add_material("mat_locked_room_glimpse")
            $ add_stat_delta("suspicion", 20, character="stern")
            $ flush_notification_bundle()
            
            cora_inner "I press my shoulder against the jamb. Through the gap, I catch sight of Eleanor's personal ledger left unlocked."
            cora_inner "Ms. Stern's boot heels click behind me. I slip away, but she casts a sharp look in my direction."

    # 4. Update Context: Gideon enters the scene and becomes the primary threat.
    $ set_scene_context(location="drawing_room", present=["stern", "gideon"], relevant=["gideon"])
    
    "Cora moves to the drawing room. Gideon enters. Ms. Stern remains."
    "Since Gideon has higher global context priority, the HUD should display Gideon."

    # 5. Opportunity expiry warning test
    $ begin_notification_bundle()
    $ spend_focus(3) # This drops focus below 2, which should expire "obj_follow_vance"
    $ flush_notification_bundle()

    "We spent additional focus slots. Check the journal to verify if 'Follow Vance after supper' has faded."

    # 6. Writing assignment completion draft evaluation
    python:
        assignment = writing_assignments[current_assignment_id]
        usable_val = get_usable_material_value(current_assignment_id)
        is_ready = assignment["status"] == "ready"
        unlocked_list = assignment.get("available_variants", ["respectable"])

    if is_ready:
        "Cora sits at her desk. She has gathered [usable_val] material points. Her manuscript is ready."
        
        # Display selection options dynamically based on unlocks
        menu:
            "Select draft version to compose:"

            "Respectable Version" if "respectable" in unlocked_list:
                $ complete_assignment(current_assignment_id, "respectable")
                "Cora pens a safe, dry depiction. The draft is acceptable."

            "Scandalous Version" if "scandalous" in unlocked_list:
                $ complete_assignment(current_assignment_id, "scandalous")
                "Cora writes a sharp, stinging portrayal exposing Eleanor's hypocrisy."

            "Blackmail Version" if "blackmail" in unlocked_list:
                $ complete_assignment(current_assignment_id, "blackmail")
                "Cora weaves Gideon's personal note into the text, creating lethal leverage."
    else:
        "Cora sits at her desk, but she lacks sufficient material to write a draft."
        "Current gathered material value: [usable_val] / 5."

    $ begin_notification_bundle()
    $ complete_objective("obj_assignment_01_material")
    $ flush_notification_bundle()

    "Playtest sequence finished. Check the Journal History tab for objective logs."

    return
