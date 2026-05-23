# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: erotic | day102 | Writers' Room orchestrator
# Lens: contraband charge, shame-as-power, night indulgence (no canon relationship violations)

label day102_1_missy_finds_a_thing_spec:

    "She holds it up with two fingers."
    "The lace is lighter than it has any right to be."
    "It knows exactly what it is for."

    jump day102_2_day2_chore_time_spec


label day102_2_day2_chore_time_spec:

    if story.day2_contraband_state == "stolen_wearing":
        "The lace moves beneath my uniform with each step."
        "Heat and fear share the same pulse."
        "No one knows what I am carrying because I am carrying it as myself."

    jump day102_4_cora_sneaks_a_feel_spec


label day102_4_cora_sneaks_a_feel_spec:

    if story.day2_contraband_state == "stolen_wearing":

        "I lift the hem only enough to confirm the secret is still mine."
        "The mirror gives back a maid."
        "The skin beneath disagrees."

        "A woman can scrub ash from a stranger's hearth while carrying a private scandal beneath her skirt."
        "A woman can be unseen and still not be innocent."

    else:

        "I replay the afternoon until the room rearranges itself around Gideon's entrance."
        "No chapter comes."
        "Only heat stored where ink should have gone."
