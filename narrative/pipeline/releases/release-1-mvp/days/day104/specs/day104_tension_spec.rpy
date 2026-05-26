# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: tension | day104 | Writers' Room orchestrator
# Lens: exposure anxiety, keyhole risk, Stern's shadow, lockbox threat

label day104_1_false_dawn_suite_window_tension_spec:

    scene bg_master_suite_day
    with fade

    "My throat is tight as I stand in the silent Master Suite."
    "Every floorboard creak sounds like an executioner's step."
    "If Stern finds me here, it is not merely dismissal; it is the end of the book."

    jump day104_1_lockbox_evidence_tension_spec


label day104_1_lockbox_evidence_tension_spec:

    "The hairpin bends under my slick, sweating fingers."
    "Any second the key will turn. Any second Gideon's boots will echo."
    "Then the click of the lock. Inside, the photographic paper. Compromising, terrifying."

    jump day104_2_return_early_tension_spec


label day104_2_return_early_tension_spec:

    "The lock on the outer door rattles. They are early!"
    "I am cornered. A trapped mouse in a gilded cage."

    menu:
        "Where do I run?"

        "Cold hearth.":
            "I squeeze into the black, suffocating chimney, soot filling my throat."

        "Stand and lie.":
            "My heart beats like a drum against my ribs. I stand trembling with a dust cloth."

        "Use Missy.":
            "I throw Missy into the room as a human shield and bolt."

    jump day104_3_stern_pressure_tension_spec


label day104_3_stern_pressure_tension_spec:

    scene bg_servants_quarters_dusk
    with fade

    "Miss Stern watches me with cold, analytical eyes."
    "She does not need evidence; she smells my guilt."
    "My hands shake as I try to hold my head steady."

    jump day104_4_twilight_ledger_false_dawn_tension_spec


label day104_4_twilight_ledger_false_dawn_tension_spec:

    "The ledger lies before me, but my fingers can barely grip the pen."
    "Gideon's photograph is under the floorboard. If he searches the room... if Stern checks..."

    jump day104_5_triumphant_chapter_tension_spec


label day104_5_triumphant_chapter_tension_spec:

    scene bg_cora_desk_night
    with fade

    "The candle flickers, casting grotesque shadows."
    "I write in a frantic sprint, translating my terror into fictional triumphs."
    "But fiction does not mend the loose floorboard."

    jump day104_6_false_dawn_ending_tension_spec


label day104_6_false_dawn_ending_tension_spec:

    "Gideon's photo waits in the dark under the bed."
    "Tomorrow the balance changes, or the trap closes."
    "I sleep in the teeth of the beast."
