# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: thematic | day104 | Writers' Room orchestrator
# Lens: craft-as-defense, performing self, manuscript taxonomy, false dawn relief

label day104_1_false_dawn_suite_window_thematic_spec:

    scene bg_master_suite_day
    with fade

    "Morning enters the Master Suite as if nothing terrible has ever happened here."
    "That is the talent of expensive rooms. They reset themselves like a well-oiled ledger."
    "Everyone is wrong in a useful direction today, which is the only form of privacy a maid can afford."

    jump day104_1_lockbox_evidence_thematic_spec


label day104_1_lockbox_evidence_thematic_spec:

    "Inside the lockbox: banknotes, folded letters, and the stiff photographic paper."
    "The photograph is smaller than a prayer book, yet it holds a life."
    "Gideon and another gentleman. Ruin pressed on small paper."
    "Here is the ending for the manuscript. The knife is shaped correctly."

    jump day104_2_return_early_thematic_spec


label day104_2_return_early_thematic_spec:

    "A key turns. False dawns simply let the sun in first before the trap is sprung."
    "I stand by the desk with his ruin pressed against my ribs like a second heart."

    menu:
        "Sixty seconds. How do I survive?"

        "Hide in the cold hearth. Keep the evidence.":
            "I crawl into the unlit, silent soot. The chimney has angles gentlemen never check."

        "Stand in the room and lie cleanly. Keep the evidence.":
            "I wipe the desk as if dust is a personal insult to Miss Stern."

        "Use Missy as cover. Lose the evidence, preserve the alibi.":
            "Panic makes the first decision. Ambition improves it."

    jump day104_3_stern_pressure_thematic_spec


label day104_3_stern_pressure_thematic_spec:

    scene bg_servants_quarters_dusk
    with fade

    "Stern does not need evidence to suspect disorder; she smells it like mildew."
    "She warns me against guest notice. Tonight, no proof feels like grace."

    jump day104_4_twilight_ledger_false_dawn_thematic_spec


label day104_4_twilight_ledger_false_dawn_thematic_spec:

    "The ledger sits open on my desk. My hands are numb."
    "The manuscript waits, not for more material, but for courage."

    jump day104_5_triumphant_chapter_thematic_spec


label day104_5_triumphant_chapter_thematic_spec:

    scene bg_cora_desk_night
    with fade

    "The chapter comes all at once. In this chapter, the lord's secret is not named."
    "It is placed on a table in a sealed envelope, poisoning every polite sentence."
    "The heroine defeats him completely. She is untouchable."

    jump day104_6_false_dawn_ending_thematic_spec


label day104_6_false_dawn_ending_thematic_spec:

    "Tomorrow I will decide how to use the proof. Tomorrow the balance changes."
    "Outside my room, the hotel breathes around me. Not beaten. Only sleeping."
    "I mistake the difference for victory."
