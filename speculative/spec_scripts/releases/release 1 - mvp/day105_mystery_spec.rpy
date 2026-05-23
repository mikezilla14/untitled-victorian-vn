# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: mystery | Source: day105_non_canon.rpy | Orchestrator: writers_room
# Lens: clues, red herrings, fair-play revelation, hotel-as-labyrinth

label day105_1_monster_reemerges_spec:

    scene bg_master_suite_day
    with fade

    # CLUE: summons paper has Savoy crest pressed wrong side — fresh print, not guest stationery
    "The message on the tray is folded too crisply for a servant's hand."
    "Someone upstairs wanted it to look official."

    if story.has_photograph:
        # CLUE: empty floorboard — nail scratch fresh
        "The plank is replaced level, but the nail heads are brighter than the wood."
        "Someone opened it after I did."
    else:
        # RED HERRING: Cora imagines photograph still in box — true but not provable
        "The lockbox is closed."
        "I cannot prove what is inside without opening it again."

    jump day105_2_the_summons_spec


label day105_2_the_summons_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    gideon "Close the door."

    # CLUE: newspaper folded to Financial Times shipping notices — Gideon leaving is planned
    "The paper is open to departures."
    "He wanted me to see it without asking."

    gideon "Someone forced my box."

    if story.day4_escape_state == "missy_cover":
        # CLUE: Missy named on yesterday's chore slate in margin — who wrote it?
        gideon "Missy appeared when the corridor narrowed."
        "I file the detail."
        "Someone assigned her route."

    gideon "Where is it?"

    jump day105_3_leverage_collapses_spec


label day105_3_leverage_collapses_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    if story.has_photograph:
        cora "This is proof."
        gideon "It is paper. Proof requires a room that believes you."

    gideon "Police. Solicitor. Employer. Publisher."

    # PAYOFF LATER: Gideon does not burn — seals envelope with wax from desk drawer
    if story.has_photograph:
        "He does not reach for the grate."
        "He takes wax from the desk."
        "Seals the photograph inside a new envelope."
        "Labels it with a hand I do not recognise."

        $ story.set_has_photograph(False)
        $ story.set_day5_evidence_destroyed(True)
        # CANON FLAG: canon draft burns photo — convergent picks burn vs seal for Release 2 hook

    jump day105_5_gideon_marks_cora_spec


label day105_5_gideon_marks_cora_spec:

    gideon "Tomorrow I leave the Savoy."

    # CLUE: he says monsters are rarely convenient — implies larger network, not lone villain
    gideon "We will meet when it is interesting."

    # PAYOFF LATER: envelope money is crisp Bank of England notes, sequential serial band — patron?
    "The envelope on the table is heavier than travel money should be."

    return
