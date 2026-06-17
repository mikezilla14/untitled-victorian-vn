# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day100_tension_spec.rpy
# Release 1 / Day 00 / Prologue / Tension Lens

label day100_main_tension:
    scene bg_country_estate_corridor_night
    with fade

    # [BEAT] Tension: High stakes, kinetic sneaking.
    "One false step on the third riser and the house will wake. The silence is a pressure."
    "I freeze when the grandfather clock downstairs chimed two. My heart beats against my ribs like a trapped bird."
    "I have three pages in my hand when the corridor floorboard groans behind me."
    jump day100_1_afternoon_boredom_tension


label day100_1_afternoon_boredom_tension:
    scene bg_country_estate_study
    with dissolve

    "Sir John's study. The door is slightly ajar—a sliver of dark wood like a trap."
    "I must recover the confiscated pages before the morning mail cart leaves for the station."
    "If he has read them, if he sends them to my next place, I am not merely dismissed—I am ruined."

    menu:
        "Where did he hide them?"

        "In the bureau drawer. [[Search the bureau: +15 Inspiration, +10 Corruption]]":
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            jump day100_2_desk_tension

        "Near the parlour door. [[Search the parlour entrance: +15 Corruption]]":
            $ apply_effects(corr=15)
            $ story.set_prologue_found("overheard")
            jump day100_2_parlour_tension


label day100_2_parlour_tension:
    "My hands are cold as I touch the wall. Voices inside the parlour rise and fall in a tight, breathless tempo."
    "It is George, the master of the stables, speaking in a low, sharp command that cuts the silence."
    "The raw adrenaline of their secret makes my skin prickle. It is dangerous material."
    jump day100_2_reconvergence_tension


label day100_2_desk_tension:
    "My fingers scramble through the desk drawers, paper rustling under my nails like dry leaves."
    "Under a stack of rent rolls, I find Sir John's letters—words of desperate, hidden want that make my breath stop."
    "The stakes are written in black ink: a master's ruin, and my own."
    jump day100_2_reconvergence_tension


label day100_2_reconvergence_tension:
    "A key turns in the outer door. The lock clicks."
    "Panic. I slide behind the window screen, folding myself into the dust-scented dark."
    "Sir John enters. He does not search the room; his gaze goes straight to my hiding place."
    "Sir John" "Come out, Vale."
    "The quietness of his voice is worse than a shout. It is the absolute authority of the house."

    menu:
        "How do I answer?"

        "Lie — I was seeking a draft in the study. [[prologue_holywell_posture = careful]]":
            $ story.set_prologue_holywell_posture("careful")
            cora "There was a draft, sir."
            cora_inner "My voice is level, country-flat. Let him hear a simpleton."

        "Deflect — the pages are my own. [[prologue_holywell_posture = eager]]":
            $ story.set_prologue_holywell_posture("eager")
            cora "They are my pages, sir."
            cora_inner "A dangerous word from a maid in a borrowed apron. I will not cower."

        "Submit — throw myself on his mercy. [[prologue_holywell_posture = desperate]]":
            $ story.set_prologue_holywell_posture("desperate")
            cora "Forgive me, sir."
            cora_inner "I bend my neck. Let him believe the submission is real."

    jump day100_3_night_daydream_tension


label day100_3_night_daydream_tension:
    scene bg_train_carriage_day
    with dissolve

    "The third-class carriage is a rattle of iron and coal smoke. The gentleman opposite watches me."
    "I feel the satchel between my boots. If my fingers tremble, he will see."
    "Wiltshire is a story closed. London rises through the smog like a cage."
    jump day100_3_arrival_tension


label day100_3_arrival_tension:
    "The carriage lurches as we hit the points. The satchel buckle slips; sheets of paper scatter."
    "I gather them frantically, sweeping the written lines under my skirt before the gentleman can read a word."
    "Waterloo station's iron ribs loom ahead. There is no turning back."
    jump day101_main
