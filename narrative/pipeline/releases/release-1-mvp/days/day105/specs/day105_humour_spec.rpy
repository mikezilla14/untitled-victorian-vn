# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: humour | Source: day105_non_canon.rpy | Orchestrator: writers_room
# Lens: era-appropriate wit, class embarrassment, power subtext in banter

label day105_2_the_summons_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    "Gideon reads the Morning Post as though the headlines owe him money."

    gideon "Close the door, Cora."

    cora "Yes, sir."

    gideon "Not for privacy. For theatre. You have a taste for theatre, I think."

    cora "I have a taste for employment, sir."

    "The paper folds once."
    "He is excellent at making cruelty look like housekeeping."

    gideon "Someone forced my private box."

    if story.day4_escape_state == "bold_lie":
        gideon "A girl dusting a locked desk in an already-clean room."
        cora "The dust was aspirational, sir."
        "His mouth twitches."
        "Not amusement."
        "Appraisal."
    elif story.day4_escape_state == "missy_cover":
        gideon "Missy appeared at a convenient moment."
        cora "The corridor is narrow. People collide."
        gideon "You collide with strategy. Less charming."
    else:
        gideon "We are past denial."
        cora "Then we are past my favourite part of the interview."

    jump day105_3_leverage_collapses_spec


label day105_3_leverage_collapses_spec:

    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center

    if story.has_photograph:
        "I produce the photograph with the solemnity of a witness and the competence of a thief."
        cora "You may wish to sit down, sir."
        gideon "I am standing precisely where standing is most insulting."
    else:
        cora "I know what was in the envelope."
        gideon "You know what you wanted to know while committing theft. Different curriculum."

    gideon "Imagine you tell your story in the street."

    "He counts on his fingers."
    "Solicitor. Employer. Publisher. Polite women."

    gideon "And every indecent man will dine with me anyway."

    cora "A crowded social calendar, sir."

    gideon "You are not funny."

    cora "No, sir. I am inconvenient."

    # ALT — PRESSURE RELEASE: burn beat played as etiquette failure
    if story.has_photograph:
        gideon "This paper is not flammable enough for tragedy."
        "He burns it anyway."
        "The performance is for me."
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
            gideon "How literary. How poorly paid."
            jump day105_5_gideon_marks_cora_spec

        "Because you frightened me. [Prey / Adversary]":
            cora "Because you frightened me."
            gideon "And did I succeed?"
            cora "You are succeeding now, sir."
            jump day105_5_gideon_marks_cora_spec


label day105_5_gideon_marks_cora_spec:

    gideon "Go downstairs."

    cora "And tomorrow, sir?"

    gideon "Tomorrow I leave. Monsters rarely keep rooms on account."

    cora "I shall inform the dust, sir."

    "He almost smiles."
    "Almost is a wage increase in this hotel."

    return
