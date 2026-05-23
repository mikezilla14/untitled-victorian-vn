# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: class | Source: day105_non_canon.rpy | Orchestrator: writers_room
# Lens: status friction, forms of address, spatial permission

label day105_2_the_summons_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    # ADDRESS: Cora → Gideon: "Mr. Locke" until he permits familiarity (he does not)
    "I wait on the threshold until he looks up."
    "Guests are not kept waiting. Servants are."

    gideon "Close the door, Cora."

    "I close it."
    "I do not lean on it."
    "A maid leans. A maid is dismissed."

    gideon "Someone forced the lock on my private box."

    if story.day4_escape_state == "bold_lie":
        gideon "Dusting a locked desk in a clean room."
        cora "The room was not clean, sir. Only occupied."
    elif story.day4_escape_state == "missy_cover":
        gideon "Missy appeared when she was useful."
        # ETIQUETTE REPAIR variant when humour/erotic cross lines — formality restored
        cora "I reported what I was told to report, sir."
    else:
        gideon "We are past denial."
        cora "Yes, sir."

    jump day105_3_leverage_collapses_spec


label day105_3_leverage_collapses_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    "He remains seated."
    "I remain standing."
    "The geometry is the argument."

    if story.has_photograph:
        "I should not place anything on his table without permission."
        "I place the photograph anyway."
        "That is the trespass he wanted to discuss."

        gideon "Walk into the street and speak."

    gideon "The police will ask why you were in my rooms."

    cora "They will ask you first, sir."

    gideon "They will ask me last."

    "There it is."
    "Order of questioning is order of power."

    if story.has_photograph:
        "He takes the photograph to the fireplace."
        "He does not ask me to watch."
        "Watching is a servant's job. I watch."

        $ story.set_has_photograph(False)
        $ story.set_day5_evidence_destroyed(True)

    jump day105_4_why_did_you_do_it_spec


label day105_4_why_did_you_do_it_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    gideon "Why?"

    menu:
        "Why did I do it?"

        "To finish the book. [Observer / Muse]":
            cora "To finish my book, sir."
            # HISTORICAL RISK: flag for consultant — "book" vs "manuscript" register
            jump day105_5_gideon_marks_cora_spec

        "Because people like you survive by not being seen. [Ghost / Witness]":
            cora "Because people like you survive by not being seen, sir."
            gideon "People like me are seen constantly."
            cora "You are looked at, sir. That is not the same."
            jump day105_5_gideon_marks_cora_spec


label day105_5_gideon_marks_cora_spec:

    gideon "Go back downstairs."

    cora "Yes, sir."

    "The envelope on the table."
    "I do not touch it until he turns away."
    "Even then, I wait one breath."
    "Servants who reach too quickly are thieves twice."

    menu:
        "Do I take Gideon's money?"

        "Take it. [Pocket without counting — proper discretion]":
            $ story.set_day5_money_choice("taken")

        "Refuse it. [Bow — no speech]":
            $ story.set_day5_money_choice("refused")

        "Leave it untouched. [Step back three paces]":
            $ story.set_day5_money_choice("deferred")

    return
