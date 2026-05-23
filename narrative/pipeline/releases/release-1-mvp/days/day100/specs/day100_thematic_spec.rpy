# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day100_thematic_spec.rpy
# Release 1 / Day 00 / Prologue / Thematic Lens

label day100_main_thematic:
    scene bg_train_carriage_day
    with fade

    # [BEAT] Env/metaphor: London soot swallowing Wiltshire's light.
    "The soot-stained window of the third-class carriage does not merely block the sun."
    "It coats the light in grease, turning the green hills of Wiltshire into dark, grey tombs of memory."
    "Every clatter of the iron track is a word I did not say. A silence I carried out of the gates."

    "A country maid is born in the soil and expected to return to it."
    "London, however, is built of bricks and cold slate, where dirt does not nourish — it only stains."

    jump day100_2_discovery_flashback_thematic


label day100_2_discovery_flashback_thematic:
    scene bg_country_estate_study
    with dissolve
    play music "themes/melancholy"

    "In the master's study, the air was different."
    "It smelled of dried roses and calfskin bindings — objects that had lived, died, and been preserved for those who could afford the dust."
    "I was the duster. The mute instrument of preservation."
    "But the open desk and the sound from the parlour were cracks in the glass."

    menu:
        "The parlour's raw breath, or the desk's quiet ink?"

        "Investigate the parlour. [Corruption focus]":
            $ apply_effects(insp=0, corr=15)
            $ story.set_prologue_found("overheard")
            jump day100_2_parlour_thematic

        "Examine the desk. [Inspiration focus]":
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            jump day100_2_desk_thematic


label day100_2_parlour_thematic:
    # [BEAT] Metaphor: The voyeur's burden.
    "I press my ear to the panelled oak. The wood feels hot against my skin."
    "Inside, the voices of Sir John and George strip away their master-shapes. They speak like creatures trapped in their own skin."
    "Sir John's breathing is a ragged thing, like a bird caught in a chimney."
    "George" "Let the house see us, John. The house is only stone, and stone has no tongue."
    "The truth of their appetite enters me through the oak. It is the raw, heavy fuel of things unpermitted."
    jump day100_2_reconvergence_thematic


label day100_2_desk_thematic:
    # [BEAT] Metaphor: Ink as blood.
    "The letter is left open. The ink is fresh, a wet black scar on the parchment."
    "I read the elegant, trembling lines. They are Sir John's words, but they bleed out of the columns of his budget ledger."
    "Cora" "He writes of a touch as if it were a banker's draft. A currency of fingers and dark corners."
    "In reading them, I steal the ink. I put my own hand to the draft and sign his name."
    jump day100_2_reconvergence_thematic


label day100_2_reconvergence_thematic:
    # [BEAT] Metaphor: The shadow of the master.
    "A shadow falls over the desk. The Master stands there."
    "His face is grey, the colour of a dry sheet. He looks at me and sees his own ink on my fingers."
    "Sir John" "You are dismissed, Cora Vale. Before the lamps are lit."
    "His anger is not loud; it is the quiet, heavy weight of a drawer closing."
    $ renpy.block_rollback()
    jump day100_3_awakening_thematic


label day100_3_awakening_thematic:
    scene bg_train_carriage_day
    with dissolve
    play sound "sfx/train_whistle"

    "The train whistle screams, a metal throat tearing open the silence."
    "I wake, my breath damp against the window."
    "Wiltshire is dead. The paper sheets on the floorboards are the only bones I have left."
    "A manuscript of other people's desires, and a reference built of elegant lies."
    "I fold them away, tucking my secrets inside my linen."
    "London looms in the smoke. The Savoy is waiting, and I bring my hunger with me."
    jump day101_main
