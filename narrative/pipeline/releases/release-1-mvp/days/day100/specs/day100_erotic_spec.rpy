# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day100_erotic_spec.rpy
# Release 1 / Day 00 / Prologue / Erotic Lens

# [BEAT] Erotic: Wiltshire corridor at night, close heat, skin and heartbeat.
label day100_main_erotic:
    scene bg_country_estate_corridor_night
    with fade

    "The Wiltshire house at night is a cold vault, but my chest is tight and hot."
    "I keep my boots in my hand, the rough wool of my stockings catching on the bare floorboards."
    "My secret manuscript sheets are in my corset, pressing sharp against my skin with every shallow breath."
    jump day100_1_afternoon_boredom_erotic


label day100_1_afternoon_boredom_erotic:
    scene bg_country_estate_study
    with dissolve

    "The master's study smells of dried roses and the heavy, lingering heat of a fire long burnt down."
    "My hands tremble as I touch the walnut bureau. The wood feels smooth, almost like skin, under my fingertips."
    "I am seeking the three confiscated pages—my own words, which describe a physical, private hunger that gentry houses burn."

    menu:
        "Where did he hide them?"

        "In the walnut bureau, where his private correspondence lies. [[Search the bureau: +15 Inspiration, +10 Corruption]]":
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            jump day100_2_desk_erotic

        "By the parlour settee, where he sits when he reads. [[Search the parlour entrance: +15 Corruption]]":
            $ apply_effects(corr=15)
            $ story.set_prologue_found("overheard")
            jump day100_2_parlour_erotic


label day100_2_parlour_erotic:
    # [EROTIC LIFT] The raw murmur of physical intimacy.
    "I press my ear to the panel. The cold oak warms immediately against my cheek."
    "The murmur from the parlour is wet, heavy, and rhythmic—a gasp, a buckle sliding open."
    "Sir John" "No... George, please. The household is asleep..."
    "George" "The house is dead, John. Let the collar be undone."
    "A low, helpless moan follows. I stand frozen, my thighs pressing together in the dark, my blood pulsing in my throat."
    jump day100_2_reconvergence_erotic


label day100_2_desk_erotic:
    # [EROTIC LIFT] Illicit handwriting and sensory want.
    "My fingers slide into the deep drawer, finding a bundle of letters in Sir John's sloped, wild hand."
    "Cora (reading)" "'...the taste of your skin in the shadow of the bureau remains my only memory. I have written your name on my palms...'"
    "A hot flush rises from my chest to my neck. Ink has weight; it pulls physical heat into my body."
    jump day100_2_reconvergence_erotic


label day100_2_reconvergence_erotic:
    # [BEAT] Hiding and caught.
    "Footsteps approach. I slip behind the heavy velvet drapes, holding my breath, my back pressed against the cold glass."
    "The latch clicks. Sir John enters. His collar is undone, his chest rising and falling in ragged, grey gasps."
    "He does not raise his voice. He knows I am here."
    "Sir John" "Come out, Vale."
    "He looks at me, his eyes dark with the shame of a master caught in his undone dress."
    jump day100_3_night_daydream_erotic


label day100_3_night_daydream_erotic:
    scene bg_train_carriage_day
    with dissolve

    "The train lurches east, soot-smeared window cool against my forehead."
    "If I close my eyes, the coal grease smells of the library's velvet heat."

    if story.prologue_found == "overheard":
        "I replay the parlour's breath until the carriage rocks in time with it—wet, rhythmic, secret."
    else:
        "I replay the letters' ink until the words move on my skin like Sir John's palms."

    "Wiltshire ends. The fantasy is mine, and the hunger travels with me to London."
    jump day101_main
