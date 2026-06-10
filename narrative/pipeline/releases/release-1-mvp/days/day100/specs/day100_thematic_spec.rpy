# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day100_thematic_spec.rpy
# Release 1 / Day 00 / Prologue / Thematic Lens

label day100_main_thematic:
    scene bg_country_estate_corridor_night
    with fade

    # [BEAT] Metaphor: Dust, silence, and class boundary.
    "In the dark, Sir John's country house is only a system of locks and cold stone."
    "I have dust on my apron by day, but tonight I have my own work in my fingers."
    "The silence is not a peace; it is a weight that punishes a maid who steps out of her place."
    jump day100_1_afternoon_boredom_thematic


label day100_1_afternoon_boredom_thematic:
    scene bg_country_estate_study
    with dissolve

    "The master's study smells of dried roses and the cold, soot-stained air of parliament."
    "I am here to steal back my pages—my record of what their respectability hides."
    "A writing maid is a trespasser in their garden of calfskin and gold leaf."

    menu:
        "Where did he hide the pages?"

        "In the walnut bureau. [[Search the bureau: +15 Inspiration, +10 Corruption]]":
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            jump day100_2_desk_thematic

        "By the parlour door. [[Search the parlour entrance: +15 Corruption]]":
            $ apply_effects(corr=15)
            $ story.set_prologue_found("overheard")
            jump day100_2_parlour_thematic


label day100_2_parlour_thematic:
    "The parlour door is thick oak, but the truth of their appetite cuts through it like a knife."
    "They speak of skin as if it were a debt, master and servant stripped of their titles in the dark."
    "It is the raw, unwritten fuel I need for my pages. The truth beneath the mask."
    jump day100_2_reconvergence_thematic


label day100_2_desk_thematic:
    "The drawer is open. The letters are a wild ledger of Sir John's forbidden want."
    "I read the elegant, trembling ink. It is a currency of fingers and dark corners."
    "In reading his shame, I steal his authority. The ink is mine now."
    jump day100_2_reconvergence_thematic


label day100_2_reconvergence_thematic:
    "The shadow of the master falls across the door. Sir John stands there with my manuscript."
    "His voice is quiet, like a drawer closing on a secret."
    "Sir John" "Come out, Vale."
    "He looks at me, his face grey with the shame of a man whose ink is on a servant's fingers."
    jump day100_3_night_daydream_thematic


label day100_3_night_daydream_thematic:
    scene bg_train_carriage_day
    with dissolve

    "The train whistle screams, a metal throat tearing open the soot-grey air."
    "Wiltshire is a country tomb behind me. London gathers ahead—smog and slate and brick."
    "I fold my manuscript sheets away in my satchel. I bring the ink, the reference, and the hunger."
    jump day101_main
