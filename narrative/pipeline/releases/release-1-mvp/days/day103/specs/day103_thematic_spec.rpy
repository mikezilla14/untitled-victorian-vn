# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# Persona: thematic | day103 | Writers' Room orchestrator
# Lens: craft-as-defense, the performing self, manuscript taxonomy, power-appetite duality

label day103_1_servants_corridor_thematic_spec:

    scene bg_servants_corridor_morning
    with fade

    "The Savoy does not sleep; it merely resets its gears."
    "Yesterday's sins are swept under the runner, policed by broom and lye."
    "I carry the ledger in my pocket like a second spine."
    "To write is to perform a autopsy on my own captivity."

    jump day103_2_suite_gideon_tea_thematic_spec


label day103_2_suite_gideon_tea_thematic_spec:

    scene bg_master_suite_day
    with dissolve

    "The vanity mirror catches the tripartite arrangement: the lady seated, the master looming, the maid acting as the silent pivot."
    "I draw the silver brush through her copper hair."
    "It is a exercise in mass and resistance. I must look like a machine folding silk, while my eyes count the brush-strokes."

    gideon "Tell me, Cora. Do you find Miss Vance beautiful?"

    menu:
        "Answer like a craftsman. Describe the bones, not the sentiment. [Inspiration]":
            cora "Yes, Sir. Her face holds anger better than softness. It gives the bones more purpose."
            "The sentence is a description of architecture, not beauty."
            "But Gideon smiles. He enjoys a servant who treats people like inventory."
            jump day103_2_suite_gideon_beat_thematic_spec


label day103_2_suite_gideon_beat_thematic_spec:

    gideon "Tonight. Nine o'clock. You will bring tea. Alone."
    cora "Miss Stern assigns the evening duties, Sir."
    gideon "Then Miss Stern will have assigned correctly."

    "He is not asking."
    "He is mapping the house's borders, and he has decided that my performance belongs to him."

    jump day103_2_suite_night_tea_thematic_spec


label day103_2_suite_night_tea_thematic_spec:

    scene bg_master_suite_night
    with fade

    "The night is silent enough to hear the Savoy breathing."
    "Mr. Locke stands near the cold hearth. Proximity in the dark is different from proximity in the daylight; it has no social safety."

    gideon "You write. Do not spoil this by pretending stupidity."

    menu:
        "Deny him access. Keep the book mine. [Defiance]":
            cora "My writing is not part of my service, Sir."
            gideon "Everything in this house becomes service if a guest is sufficiently interested."
            cora "Then the house is mistaken."
            "The words are dangerous. They are the first true things I have said, and they taste like ink and copper."

        "Offer him a controlled fragment. [Bargain]":
            cora "A fragment, perhaps. If it keeps you from imagining worse."
            cora "A house teaches silence as if silence were virtue. But silence is only obedience with its throat cut. A girl who listens long enough may mistake the wound for a mouth."
            gideon "You are wasted below stairs."

    jump day103_3_bedroom_final_write_thematic_spec


label day103_3_bedroom_final_write_thematic_spec:

    scene bg_cora_desk_night
    with dissolve

    "I reach my room and close the door."
    "The manuscript waits, hungry for the day's remains."
    "Gideon has seen the ink. That makes the book a weapon we are both holding, and I must decide which side of the blade is mine."
