# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: mystery | day102 | Writers' Room orchestrator
# Lens: who knew, pattern-reading, misdirection without new facts

label day102_1_cora_deceives_missy_spec:

    "Obvious things are where blame waits."
    "A trunk is not a hiding place."
    "It is a question addressed to the man who owns it."

    jump day102_3_cora_pretends_to_find_it_spec


label day102_3_cora_pretends_to_find_it_spec:

    elif story.day2_contraband_state == "stolen_wearing":
        "A second small lace ribbon lies caught under the hatbox lining."
        "Not the garment itself."
        "Enough to teach the room the wrong lesson."

        cora "There is a loose piece here, Madam. Perhaps the rest was misplaced while packing."

    jump day102_3_gideon_interrupts_controls_vance_spec


label day102_3_gideon_interrupts_controls_vance_spec:

    elif story.day2_tea_choice == "predator":

        "He understands too quickly."
        "Men like him do not need proof when pattern will do."

        gideon "Found what you misplaced."

        "He has chosen which story the afternoon will believe."

    else:

        "His eyes touch mine for the smallest fraction of time."
        "He has not believed me."
        "He has not exposed me."
        "He is keeping a note."
