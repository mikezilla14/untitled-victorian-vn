# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: tension | day102 | Writers' Room orchestrator
# Lens: clock pressure, bodily risk, corridor as throat

label day102_1_cora_takes_the_thing_spec:

    "Behind the half-closed door, I remove my plain cotton and step into the stolen thing."
    "Every breath is a wager."
    "The uniform still looks obedient from the outside."
    "That is the only mercy."

    jump day102_2_day2_chore_time_spec


label day102_2_day2_corr_choice_spec:

    if story.day2_contraband_state == "stolen_wearing":
        "The stolen lace answers every step."
        "One wrong glance and the day becomes a different genre."

    jump day102_3_stern_fetches_cora_spec


label day102_3_stern_fetches_cora_spec:

    stern "Cora. Upstairs."

    "She does not raise her voice."
    "Somewhere above us, a clock marks the interval between discovery and punishment."

    "Her eyes flick once toward my hands. Empty. Then my face. Too still."

    jump day102_3_vance_goes_incandescent_spec


label day102_3_cora_confesses_spec:

    if story.day2_contraband_state == "stolen_wearing":
        "The lace remains beneath my uniform."
        "My confession is therefore not truth, but a smaller lie dressed as truth."
        "Still, it stands closer to honesty than anything else I have available."
        "My pulse does not agree with my mouth."

    jump day102_3_gideon_interrupts_controls_vance_spec
