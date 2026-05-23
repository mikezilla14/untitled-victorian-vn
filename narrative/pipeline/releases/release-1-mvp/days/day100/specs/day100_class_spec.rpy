# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day100_class_spec.rpy
# Release 1 / Day 00 / Prologue / Class & Etiquette Lens

label day100_main_class:
    scene bg_train_carriage_day
    with fade

    # [BEAT] Class: The third-class carriage constraints and spatial boundaries.
    "In the third-class carriage, the air is thick with the smell of wet wool and cheap coal. We are packed like bricks in a cellar."
    "I keep my knees pulled tight, my elbows pinned to my ribs. A servant in transit must occupy as little space as possible."
    "The forged references in my pocket are my passport. They say I have a right to enter the Savoy's back doors."

    jump day100_2_discovery_flashback_class


label day100_2_discovery_flashback_class:
    scene bg_country_estate_study
    with dissolve
    play music "themes/melancholy"

    # [ADDRESS:] Etiquette of spatial permission.
    "Sir John's study was a territory I entered only by license."
    "I was hands and a broom. Nothing more."
    "But the open bureau was a breach of etiquette. The papers lay scattered, exposing the master's private thoughts to the chambermaid's eyes."
    "And from the parlour came that sound — a cross-class friction."

    menu:
        "The oak door, or the open desk?"

        "Investigate the parlour door. [Etiquette breach: +15 Corruption]":
            $ apply_effects(insp=0, corr=15)
            $ story.set_prologue_found("overheard")
            jump day100_2_parlour_class

        "Dust the papers on the desk. [Read the letter: +15 Inspiration, +10 Corruption]":
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            jump day100_2_desk_class


label day100_2_parlour_class:
    # [BEAT] Overhearing elite transgression.
    "I move to the door. To touch the handle would be a dismissal; to press my ear to the panel is a theft."
    "Sir John's voice has lost its parliamentary weight. It is thin, pleading."
    "Sir John" "George, the housemaid is in the hall. She has the dusting-license."
    "George" "The housemaid does not exist, John. She is only furniture that walks."
    "I stand in the corridor. I am furniture, yes. But furniture with memory."
    jump day100_2_reconvergence_class


label day100_2_desk_class:
    # [BEAT] Reading private aristocratic text.
    "I approach the desk. To read the master's mail is the highest violation of service."
    "The ink is Sir John's elegant, expensive hand."
    "Cora" "He writes of things no gentleman should put on paper. Transgressions of class and flesh."
    "I memorize the elegant slopes of his 'y's and the curves of his 'd's."
    "A maid who can copy such a hand is no longer just a maid. She is a dangerous cataloguer."
    jump day100_2_reconvergence_class


label day100_2_reconvergence_class:
    # [BEAT] The reckoning.
    "Sir John enters the study."
    "He sees me. His posture straightens immediately, the master-shape returning like starch."
    "Sir John" "Vale. You are looking at the desk."
    "cora" "I was only dusting the leather, Sir."
    "Sir John" "You are dismissed. You will leave the estate before dinner. And if you speak of what you have seen, I will see to it that your name is blackened in every registry in the South."
    $ renpy.block_rollback()
    jump day100_3_awakening_class


label day100_3_awakening_class:
    scene bg_train_carriage_day
    with dissolve
    play sound "sfx/train_whistle"

    "The train whistle shrieks. The dream dissolves."
    "I wake, my satchel flat on my lap."
    "My hands are clean, but my references are forged. I am carrying a master's handwriting in my bag, and his secrets."
    "The Savoy Hotel lies ahead in the grey fog."
    "It is a machine of class and etiquette, and I intend to be the wrench in the gears."
    jump day101_main
