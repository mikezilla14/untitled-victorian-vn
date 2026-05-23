# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: thematic | Source: day105_non_canon.rpy | Orchestrator: writers_room
# Lens: machine behind the man, observation vs participation, manuscript as dissection

# ==========================================
# THEMATIC RE-IMAGINING — DAY 105 (SAMPLE BEATS)
# ==========================================
# FROM: day105_non_canon — nodes 1, 3, 5, 6
# CANON FLAG: none — aligns with release thesis (structural power > Gideon)

label day105_1_monster_reemerges_spec:

    scene bg_master_suite_day
    with fade

    "Morning does not arrive."
    "The room simply becomes visible again, as if the hotel turned a key in me."

    if story.has_photograph:
        "The floorboard is level."
        "That is how I know something has been taken: the house prefers surfaces without secrets."
    else:
        "The lockbox still holds what I could not carry."
        "Absence can weigh as much as paper."

    "The summons is not a threat."
    "It is an appointment with the machinery."

    jump day105_3_leverage_collapses_spec


label day105_3_leverage_collapses_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    if story.has_photograph:
        "I lay the photograph down the way one lays a scalpel: carefully, knowing the cut goes both ways."
        cora "You are in it."
        gideon "So are you. Theft is a kind of portrait too."
    else:
        cora "I saw the envelope."
        gideon "You saw a reflection in glass. Servants are always looking at themselves when they think they look at us."

    gideon "Shall I teach you the arithmetic of reputation?"

    "He does not raise his voice."
    "He does not need to."
    "The room is already full of men who are not here."

    gideon "Police. Solicitor. Employer. Publisher. Polite women. Indecent men."
    gideon "None of them need to enter to vote."

    # THEMATIC: reframe burn as autopsy of false hope, not grief for image
    if story.has_photograph:
        "He takes the photograph to the grate."
        "The flame is small."
        "It eats the face first."
        "I mourn, absurdly, not Gideon's ruin — my belief that evidence was the same as sight."

        $ story.set_has_photograph(False)
        $ story.set_day5_evidence_destroyed(True)

    jump day105_6_manuscript_reckoning_spec


label day105_6_manuscript_reckoning_spec:

    scene bg_cora_desk_night
    with fade

    "The desk is an altar I built for a god who does not answer."

    if story.day5_dynamic == "muse":
        "I write the room around him until he fits."
        "Carriage. Letterhead. Lowered eyes. Refusal dressed as taste."
        "On the page he shrinks because the machine grows."
    elif story.day5_dynamic == "witness":
        "I write the cost of naming the machine aloud."
        "Who is believed. Who is displayed. Who is corrected for accuracy."
    else:
        "I write hunger without romance."
        "The tool in my hand is still a servant's hand."

    "The ending is not victory."
    "It is diagnosis."

    $ story.complete_manuscript_chapter("day5_reckoning_chapter")
    return
