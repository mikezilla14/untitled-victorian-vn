# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day100_class_spec.rpy
# Release 1 / Day 00 / Prologue / Class Lens

label day100_main_class:
    scene bg_country_estate_corridor_night
    with fade

    # [BEAT] Class: Servant spatial awareness, invisibility as a mask.
    "In Wiltshire, a maid is a clockwork doll that moves dust from one surface to another."
    "I have spent three years learning to be silent, to walk without sound, to keep my gaze on the floorboards."
    "But tonight, the silence is a trespass. I am walking where only the family's boots belong."
    jump day100_1_afternoon_boredom_class


label day100_1_afternoon_boredom_class:
    scene bg_country_estate_study
    with dissolve

    "The master's desk is a seat of parliament, of rent rolls, of local law. A maid has no business here."
    "Sir John allowed me to read his books; perhaps he thought letters made my dusting more efficient."
    "He did not expect me to write. A writing maid is a monster in the house."

    menu:
        "Where did he hide the pages?"

        "In the Walnut Bureau. [[Search the bureau: +15 Inspiration, +10 Corruption]]":
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            jump day100_2_desk_class

        "By the Parlour door. [[Search the parlour entrance: +15 Corruption]]":
            $ apply_effects(corr=15)
            $ story.set_prologue_found("overheard")
            jump day100_2_parlour_class


label day100_2_parlour_class:
    "I stand by the door. The voices through the wood discuss the house as if we, the servants, were furniture."
    "George" "The maid does not exist, John. She is a tool that walks. Let the collar be undone."
    "To them, I am a domestic tool, useful enough to ignore. The writing will turn that tool into a weapon."
    jump day100_2_reconvergence_class


label day100_2_desk_class:
    "I open the drawer. The letters reveal Sir John's secret want—the master of the house kneeling where no vicar would see."
    "The social geometry is simple: they command in public, but crawl in private. And I have the record."
    jump day100_2_reconvergence_class


label day100_2_reconvergence_class:
    "Footsteps. I slide behind the screen, my apron rustling slightly in the dark."
    "Sir John enters. He has my manuscript pages in his hand. The threat of the master is cold."
    "Sir John" "Come out, Vale."
    "He does not raise his voice; he does not need to. The entire weight of England's law stands behind him."

    menu:
        "Why did you write this filth?"

        "For the shillings home. [[+5 Inspiration]]":
            $ apply_effects(insp=5)
            $ story.set_prologue_why_write("money_home")
            cora_inner "My mother's cough. My father's pride. Shillings are the only language they understand."

        "To catalogue what power hides. [[+5 Inspiration, +5 Corruption]]":
            $ apply_effects(insp=5, corr=5)
            $ story.set_prologue_why_write("cataloguer")
            cora_inner "I want the record. Who kneels, who commands. The truth under the respectability."

        "Because scandal tastes better than porridge. [[+10 Corruption]]":
            $ apply_effects(corr=10)
            $ story.set_prologue_why_write("scandal_hungry")
            cora_inner "I will not pretend innocence is a meal. Wiltshire taught me appetite; London will teach me price."

    "Sir John" "You are dismissed. Pack your trunk. You leave for London on the morning train."
    "Sir John" "I will give you a reference for the Savoy, Vale. But if a word of this leaves your mouth, I will blacken your name to the gutter where you belong."
    jump day100_3_night_daydream_class


label day100_3_night_daydream_class:
    scene bg_train_carriage_day
    with dissolve

    "The third-class bench is hard, coal grease coating my cuffs. London is an escape with teeth."
    "A maid dismissed without a clean reference is a girl pushed toward the Strand. I have the reference, but it is a leash."
    "Wiltshire ends. London waits—a machine of power, and I bring the pen that writes it."
    jump day101_main
