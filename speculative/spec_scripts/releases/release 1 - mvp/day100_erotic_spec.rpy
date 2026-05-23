# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day100_erotic_spec.rpy
# Release 1 / Day 00 / Prologue / Erotic Lens

label day100_main_erotic:
    scene bg_train_carriage_day
    with fade

    # [BEAT] Erotic: Sensory description, rising temperature, physical awareness.
    "In the close, humid atmosphere of the carriage, the air is thick with the scent of coal grease and skin."
    "I keep my arms pinned to my sides, but the heat of the opposite passenger's leg is a constant, vibrating boundary."
    "I feel my pulse in my throat. I am traveling with forged paper, but my body carries a different, hot inclination."

    jump day100_2_discovery_flashback_erotic


label day100_2_discovery_flashback_erotic:
    scene bg_country_estate_study
    with dissolve
    play music "themes/melancholy"

    # [EROTIC LIFT] The study as a space of secret desires.
    "Sir John's library was a place of dust and dead bindings, but today the air was alive."
    "The velvet drapes hung thick and heavy, keeping the cold autumn air out, and the heat in."
    "The master's desk was left open, his private letters exposed to the light."
    "And from the adjoining parlour, behind the oak door, came the sound."
    "A wet, rhythmic gasp. A soft, breathless surrender."

    menu:
        "Risk the door, or risk the letters?"

        "Press my ear to the parlour door. [Overhear: +15 Corruption]":
            $ apply_effects(insp=0, corr=15)
            $ story.set_prologue_found("overheard")
            jump day100_2_parlour_erotic

        "Read the open letter. [Read letters: +15 Inspiration, +10 Corruption]":
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            jump day100_2_desk_erotic


label day100_2_parlour_erotic:
    # [BEAT] The voyeuristic charge.
    "I press my ear to the panel. The cold oak warms immediately against my skin."
    "The voices inside are hushed, heavy with an appetite that has no name in Wiltshire."
    "Sir John" "George... no. Not here. The door is unlocked..."
    "George" "Let it be open. Your skin is too hot for locks."
    "A soft, damp moan follows. I stand frozen, my thighs pressing together in the dark."
    "The raw reality of their transgression enters me. It is the fuel of my writing."
    jump day100_2_reconvergence_erotic


label day100_2_desk_erotic:
    # [BEAT] Illicit handwriting and desire.
    "I approach the desk. My fingers hover over the open pages."
    "The ink is Sir John's hand, but it is sloped, wild, a frantic ledger of want."
    "Cora (reading)" "'...the taste of your skin in the shadow of the bureau remains my only memory. I have written your name on my palms...'"
    "I feel a flush rise on my neck. The power of the written word to evoke desire is a physical thing."
    "I am only a chambermaid, but I have read his blood in the ink."
    jump day100_2_reconvergence_erotic


label day100_2_reconvergence_erotic:
    # [BEAT] The discovery.
    "The latch clicks. Sir John stands in the doorway."
    "His chest is rising and falling, his collar slightly loose."
    "He looks at me, his eyes dark with the shame of a man who has been seen in his underwear."
    "Sir John" "Vale. You... you are dismissed. Pack your trunk immediately."
    "His voice shakes. His authority is gone, replaced by a trembling shame."
    $ renpy.block_rollback()
    jump day100_3_awakening_erotic


label day100_3_awakening_erotic:
    scene bg_train_carriage_day
    with dissolve
    play sound "sfx/train_whistle"

    "The train whistle screams, pulling me from the memory's heat."
    "I wake, my forehead flushed against the soot-chilled glass."
    "My satchel has spilled. The sheets of my manuscript are scattered across my boots."
    "I gather them up quickly, my hands brushing the floorboards."
    "I bring my secrets to the Savoy. The gentry's desires are my ink."
    jump day101_main
