# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: thematic | day102 | Writers' Room orchestrator
# Lens: evidence, proper-as-survival, manuscript fuel vs appetite

label day102_1_cora_missy_first_shift_spec:

    scene bg_master_suite_day
    with fade

    "The Master Suite is larger in daylight and less honest for it."
    "Breakfast has emptied the room of occupants, but not of them."
    "Vance is in the perfume lingering over the dressing table. Mr. Locke is in the chair angled toward the hearth, as if the room itself has learned to obey him."

    "The rich do not only leave crumbs."
    "They leave proof that someone lived loudly while pretending not to."

    jump day102_1_missy_finds_a_thing_spec


label day102_1_missy_finds_a_thing_spec:

    "Sheer lace. Expensive, intimate, and designed with no interest whatsoever in modesty."
    "Intimate things argue with a room's pretence of respectability."
    "All of yesterday's noise becomes touchable."

    jump day102_2_day2_chore_time_spec


label day102_2_day2_chore_time_spec:

    menu:
        "How do I carry the morning?"

        "Work fast. Catalogue the room, the people, the risk. [[Inspiration]]":
            "A story cannot live on heat alone."
            "It needs furniture. It needs weather. It needs a servant who knows which board complains beneath a careless foot."
            jump day102_2_day2_insp_choice_spec

        "Linger near the danger. Let the secret sharpen itself. [[Corruption]]":
            "Appetite is not a sin here."
            "It is a ledger entry the house has not yet learned to read."
            jump day102_2_day2_corr_choice_spec


label day102_3_gideon_interrupts_controls_vance_spec:

    gideon "A dismissal makes noise. We are finished with noise for today."
    "He does not spare me."
    "He spares the hotel's reputation, which is the same thing with better upholstery."

    if story.day2_tea_choice == "prey":
        "I have not escaped notice."
        "I have been filed."

    jump day102_4_night_spec


label day102_4_night_spec:

    "My ledger lies open."
    "My page waits beside it."
    "One records appetite. The other pretends to tame it."
