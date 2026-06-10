# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day100_mystery_spec.rpy
# Release 1 / Day 00 / Prologue / Mystery Lens

label day100_main_mystery:
    scene bg_country_estate_corridor_night
    with fade

    # [BEAT] Mystery: Secrets, locks, and hidden references.
    "In Sir John's study, every drawer holds a double life."
    "I have spent months observing the patterns: the keys left in the brass lock, the letters hidden under rent rolls."
    "They think a maid does not look at the spines, but I have read the drawers."
    jump day100_1_afternoon_boredom_mystery


label day100_1_afternoon_boredom_mystery:
    scene bg_country_estate_study
    with dissolve

    "The master's desk contains more than accounts. It holds his secret instructions."
    "My confiscated manuscript pages are somewhere in this room, and I will not leave without them."
    "If I am caught, I have forged references in my pocket, but they are a fragile shield."

    menu:
        "Where did he hide the pages?"

        "In the walnut bureau. [[Search the bureau: +15 Inspiration, +10 Corruption]]":
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            jump day100_2_desk_mystery

        "By the parlour door. [[Search the parlour entrance: +15 Corruption]]":
            $ apply_effects(corr=15)
            $ story.set_prologue_found("overheard")
            jump day100_2_parlour_mystery


label day100_2_parlour_mystery:
    "The parlour door is slightly ajar. I hear voices discussing a secret lockbox in London."
    "George" "The Savoy lockbox is secure, John. The key remains with the solicitor on the Strand."
    "Sir John" "And if the papers are found? If a servant opens it?"
    "George" "The servants see nothing. They are wallpaper."
    "A lockbox at the Savoy. A key on the Strand. A mystery that matches my ambition."
    jump day100_2_reconvergence_mystery


label day100_2_desk_mystery:
    "My fingers touch a hidden latch in the walnut drawer. A secret compartment opens."
    "Inside is a letter to George, mentioning a locked photographic plate box at the Savoy."
    "The instructions are clear: a London secret, hidden under the master's respectability."
    jump day100_2_reconvergence_mystery


label day100_2_reconvergence_mystery:
    "A floorboard creaks. I slip behind the screen, my hand tight on the walnut bureau."
    "Sir John enters. He holds my manuscript pages. His eyes are cold, measuring my trespass."
    "Sir John" "Come out, Vale."
    "He knows I have seen his drawers. The secret between us is a dangerous lever."
    jump day100_3_night_daydream_mystery


label day100_3_night_daydream_mystery:
    scene bg_train_carriage_day
    with dissolve

    "The train moves east toward London. The gentleman opposite watches my satchel."
    "I have the reference for the Savoy, but my thoughts are on the lockbox and the key on the Strand."
    "Wiltshire ends. The city is a puzzle of locks, and I bring the key in my pages."
    jump day101_main
