# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: erotic | Source: day105_non_canon.rpy | Orchestrator: writers_room
# Lens: desire, transgression, voyeuristic charge, negotiated power

label day105_2_the_summons_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    "Heat in the room is not from the fire."
    "It is from being looked at while pretending to be furniture."

    gideon "Close the door."

    "The latch clicks."
    "A small sound."
    "It feels like a collar."

    gideon "You have a taste for theatre."

    cora "I have a taste for survival dressed as obedience."

    gideon "Someone opened my box."

    "He does not stand."
    "Power does not need height when the other person is already lowered."

    jump day105_3_leverage_collapses_spec


label day105_3_leverage_collapses_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    if story.has_photograph:
        "I place the photograph between us like a confession."
        "His eyes move over the image, then over me."
        "He is comparing which exposure shames him more."

        cora "You are in it."

        gideon "So are you. Thieves always want to be seen when they think they hold the frame."

    else:
        cora "I saw what was in the envelope."
        gideon "You saw what you wanted while trespassing. Desire makes poor evidence."

    gideon "Walk out and speak."

    "He steps closer."
    "Not touching."
    "Worse."

    gideon "Every indecent man will dine with me."

    # EROTIC LIFT: burn as intimacy of destruction — sensory not pornographic
    if story.has_photograph:
        "He carries the photograph to the grate."
        "He holds the match near my face before he strikes it."
        "I feel the heat on my cheek before the paper curls."

        $ story.set_has_photograph(False)
        $ story.set_day5_evidence_destroyed(True)

    jump day105_5_gideon_marks_cora_spec


label day105_5_gideon_marks_cora_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    gideon "You are interesting. Do not confuse that with safe."

    "The envelope on the table."
    "Money."
    "He will not put it in my hand."

    menu:
        "Do I take Gideon's money?"

        "Take it. [Fingers brush his — accident or choice]":
            $ story.set_day5_money_choice("taken")
            "Our skin touches once."
            "He notices."
            "He likes that I notice he noticed."

        "Refuse it. [Step back — breath visible]":
            $ story.set_day5_money_choice("refused")
            cora "No."
            gideon "Pride is attractive when it cannot afford itself."

        "Leave it untouched. [Held gaze]":
            $ story.set_day5_money_choice("deferred")
            "I do not touch the envelope."
            "I do not look away."

    # DENIED: no erotic beat on departure — thematic/class need restraint at ending
    gideon "Go downstairs."

    return
