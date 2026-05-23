# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day100_tension_spec.rpy
# Release 1 / Day 00 / Prologue / Tension Lens

label day100_main_tension:
    scene bg_train_carriage_day
    with fade

    # [BEAT] Tension: Silent carriage, ticking clock, impending arrival.
    "The click-clack of the tracks is not rhythmic. It is an accelerating countdown."
    "With every mile, the air in the carriage grows thinner, replaced by the heavy coal smoke of Waterloo."
    "I keep my hand pressed to my satchel. It holds the forged references and the half-written pages."
    "If the conductor looks too closely... if a passenger glimpses the loose ink... the game ends before it begins."

    jump day100_2_discovery_flashback_tension


label day100_2_discovery_flashback_tension:
    scene bg_country_estate_study
    with dissolve
    play music "themes/melancholy"

    # [TENSION HOOK] The dangerous silence of the study.
    "Sir John's study was too quiet. The silence was an alarm waiting to trigger."
    "I stood before the mahogany bureau, my feather duster raised like a flag of truce."
    "But the desk was left open. Sir John's letters lay exposed under the light."
    "And from the adjoining parlour, behind the oak door, came a sound."
    "Not a cough. A sudden, sharp gasp — a struggle."

    menu:
        "Risk the door, or risk the desk?"

        "Press close to the parlour door. [Overhear: +15 Corruption]":
            $ apply_effects(insp=0, corr=15)
            $ story.set_prologue_found("overheard")
            jump day100_2_parlour_tension

        "Examine the desk. [Read: +15 Inspiration, +10 Corruption]":
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            jump day100_2_desk_tension


label day100_2_parlour_tension:
    # [BEAT] Information asymmetry. Cora knows what Sir John hides.
    "I press my ear to the panel. My pulse thuds against the oak."
    "Inside, the master's voice is low, choked with a terror I have never heard in his speech."
    "Sir John" "George... stop. If the staff... if the housemaid..."
    "George" "The housemaid is a country mouse, John. She is down in the kitchens washing the lard from her sleeves."
    "I stand frozen. If Sir John turns the handle now, I am standing in his path. The proximity is a knife."
    jump day100_2_reconvergence_tension


label day100_2_desk_tension:
    # [BEAT] Impending discovery.
    "My hands are shaking as I lean over the desk."
    "The handwriting is Sir John's, but it has run wild. The lines overlap like tangled veins."
    "Cora" "He writes ofGeorge. He writes of the Strand... of a rented room... of improper acts that would hang a footman."
    "Every word is a liability. Every letter is a rope."
    "I hear a shoe click on the floorboards in the hall. My heart hammers against my ribs. I must fold them, I must put them back—"
    jump day100_2_reconvergence_tension


label day100_2_reconvergence_tension:
    # [BEAT] The trap closes.
    "The door handle jiggles."
    "I draw back, but Sir John is already in the study."
    "His eyes go straight to the open desk, then to my hands, then to my face."
    "Sir John" "You."
    "The single syllable is a dismissal. His voice is grey, cold, and final."
    "Sir John" "Get out, Cora Vale. If a single word leaves this library, I will see to it that you find no shelter in this county, or the next."
    $ renpy.block_rollback()
    jump day100_3_awakening_tension


label day100_3_awakening_tension:
    scene bg_train_carriage_day
    with dissolve
    play sound "sfx/train_whistle"

    "The train whistle screams, a sudden shock that pulls me from the dark study."
    "My satchel is on the carriage floorboards, its buckle open."
    "The manuscript pages have spilled like teeth across the wood."
    "The gentleman opposite me is lowering his newspaper. His eyes are drifting down to the elegant, scandalous lines."
    "I scramble in a frantic rush, my fingers burning as I sweep the sheets away from his gaze."
    "I tuck them back. I clamp the satchel shut."
    "The skyline of London looms through the smoke. The Savoy is a cage, but it is my only shelter."
    jump day101_main
