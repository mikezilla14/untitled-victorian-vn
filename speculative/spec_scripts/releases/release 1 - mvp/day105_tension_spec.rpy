# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: tension | Source: day105_non_canon.rpy | Orchestrator: writers_room
# Lens: clock pressure, information asymmetry, dangerous silence

label day105_2_the_summons_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    "The clock on the mantel has stopped."
    "Or I have."
    "I cannot tell which is worse."

    gideon "Close the door."

    "Footsteps pause in the corridor."
    # TENSION HOOK: Vance may be one pace from the door — Cora knows, Gideon performs not knowing
    "Someone is listening who will report whether I flinch."

    gideon "Someone forced my box."

    if story.day4_escape_state == "fireplace":
        gideon "Soot in a room that was already cleaned. You left time on the wall."
    elif story.day4_escape_state == "missy_cover":
        gideon "Missy appeared when the corridor narrowed. Useful girl. Expensive for you."
    else:
        gideon "We are past denial. Good. Denial wastes the only currency you have left."

    "I count my breaths."
    "Four before he speaks again."
    "He waits for five."

    gideon "Where is it?"

    jump day105_3_leverage_collapses_spec


label day105_3_leverage_collapses_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    if story.has_photograph:
        "My fingers find the photograph."
        "The paper is warm from my body."
        "That should mean something."
        "It means I was caught carrying heat."

        cora "This ends you."

        gideon "No."

        "He says it softly."
        "Softness is a blade when you are the one holding nothing."

    gideon "Walk out and tell them."

    "He lists the institutions."
    "Each name lands like a lock turning."

    # TENSION: hold the match unstruck — delay burn beat for convergent choice
    if story.has_photograph:
        "He lifts the photograph."
        "He reaches for the match case."
        "He does not strike yet."
        "The unlit match is worse than the fire."

        menu:
            "The match hovers."

            "Stay silent. [Let him decide]":
                "He watches my face more than the paper."
                gideon "Interesting. You understand suspense."
                # convergent may merge: burn on next beat

            "Reach for it. [Futile grab]":
                "My hand closes on air."
                "He has already moved the photograph beyond my reach."
                $ story.set_has_photograph(False)
                $ story.set_day5_evidence_destroyed(True)

    jump day105_5_gideon_marks_cora_spec


label day105_5_gideon_marks_cora_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    gideon "You could be dismissed. Arrested. Ruined."

    "He picks up the newspaper."
    "The crease is perfect."
    "He has done this before to someone."

    gideon "I will not. Yet."

    "Silence after 'yet' is a room with no exit."

    gideon "You are interesting. Do not confuse that with safe."

    menu:
        "Do I take Gideon's money?"

        "Take it. [Hands steady — fear hidden]":
            $ story.set_day5_money_choice("taken")
            "The envelope is heavy."
            "He notes whether I look at the denomination."

        "Refuse it. [Voice too level]":
            $ story.set_day5_money_choice("refused")
            cora "No."
            gideon "Brave. Or stupid. The hotel keeps both."

    return
