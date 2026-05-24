# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: tension | day103 | Writers' Room orchestrator
# Lens: claustrophobia, keyhole-risk, Stern's shadow, exposure-anxiety, Level 3.5 spice

label day103_1_servants_corridor_tension_spec:

    scene bg_servants_corridor_morning
    with fade

    "Stern's inspection has left the servants' quarters raw."
    "Every drawer is a confession waiting to be opened."
    "Suspicion is not a stat here; it is the creak of the floorboard outside my door."

    jump day103_2_suite_gideon_tea_tension_spec


label day103_2_suite_gideon_tea_tension_spec:

    scene bg_master_suite_day
    with dissolve

    "The vanity is a trap."
    "Vance's slipper clenches against the carpet. In the mirror, Gideon's neutral mask is more terrifying than anger."

    gideon "Tell me. Do you find Miss Vance beautiful?"

    menu:
        "Retreat into the maid's mask. Drop the brush. [Ghost]":
            "My fingers turn to paper under his stare."
            "The brush slips from my wet palms, striking the parquet floor with a loud, silver crack."
            cora "Forgive me, Sir."
            "I drop immediately to my knees to retrieve it, my skirt catching against Gideon's polished boots."
            "From the floor, the world is all boot-heels and cuffs. The threat of dismissal is an iron band around my throat."
            jump day103_2_suite_gideon_beat_tension_spec


label day103_2_suite_gideon_beat_tension_spec:

    gideon "Useful girls do not stare through keyholes."
    "The confirmation lands like a hand on my collar."
    "He knew."
    "Yesterday, when I stood in the corridor, he was already tracking the silhouette of my listening."
    gideon "Tonight. Nine o'clock. Alone."

    jump day103_4_room_stern_suspicion_tension_spec


label day103_4_room_stern_suspicion_tension_spec:

    scene bg_servants_quarters_dusk
    with fade
    show stern_sprite stern at center

    stern "You have been called upstairs this evening."
    stern "A guest's attention is not a promotion, Cora Vale. It is a quick way to find yourself on the Strand without a character."

    menu:
        "Play stupid. Make her underestimate me. [Suspicion/Corruption risk]":
            cora "I thought gentlemen often wanted tea, Ma'am."
            stern "Do not insult me with innocence you cannot afford."
            stern "Learn the difference before someone else teaches it cruelly."
            jump day103_2_suite_night_tea_tension_spec


label day103_2_suite_night_tea_tension_spec:

    scene bg_master_suite_night
    with fade

    "Nine o'clock."
    "The hotel is too quiet, like a beast waiting for the latch to click."
    "Mr. Locke watches me set the tray down. The silver cups clink, revealing the tremor in my fingers."

    gideon "A servant who watches is irritating. A servant who records is dangerous."
    "He knows about the book."
    "If he tells Stern, my trunk is in the street before the fire is out."
    "He holds my life in his hands like a scrap of waste paper."
