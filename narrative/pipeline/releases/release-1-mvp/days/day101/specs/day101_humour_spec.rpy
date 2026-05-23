# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day101_humour_spec.rpy
# Release 1 / Day 01 / Humour Lens

label day101_main_humour:
    scene bg_savoy_corridor_morning
    with fade

    "The Savoy Hotel did not welcome girls like me."
    "It consumed them quietly, charged them for the vinegar used to clean the copper, and called the transaction an education."
    "My references in my pocket were immaculate. I had spent three hours perfecting the signature of a fictional Wiltshire vicar who apparently spent his entire life praising my punctuality."

    jump day101_1_morning_interview_humour


label day101_1_morning_interview_humour:
    scene bg_savoy_corridor_morning
    with dissolve
    show stern_sprite neutral at center

    "Miss Stern stands rather than sits."
    "It is a highly developed technique designed to make her look six inches taller than any human being has a right to be."
    "Her eyes drill through my cap. I am reasonably certain she is checking if I have harbored any socialist pamphlets in my curls."

    stern "Cora Vale."
    cora "Yes, Ma'am."
    stern "A maid in this house is hands without noise, feet without weight, and memory without a tongue. Can you be that?"

    menu:
        "How do I survive Stern's inspection?"

        "Lower my eyes. Let her mistake fear for obedience.":
            $ apply_effects(stern_susp=5, insp=5, corr=0)
            $ story.set_day1_interview_state("meek")
            cora "I can, Ma'am. I wish to work."
            stern "Wishing is for girls with leisure. You will work because you are told."
            cora "Yes, Ma'am."
            "I arrange my face into the traditional expression of a country turnip."
            "It is a very successful performance. Turnips rarely steal spoons."

        "Answer cleanly. Let competence do what meekness cannot.":
            $ apply_effects(stern_susp=15, insp=10, corr=0)
            $ story.set_day1_interview_state("competent")
            cora "I can be quiet, quick, and exact."
            stern "Exact? A dangerous word from a girl in a borrowed apron."
            "She says 'exact' as if it were a minor misdemeanor, like entering the parlor without knocking."

    jump day101_1_vance_throws_toy_humour


label day101_1_vance_throws_toy_humour:
    show vance_sprite angry at left
    "Then something small and silver strikes the skirting board and rolls directly under my boot."
    "A lady's silver toy. The sort of expensive nonsense that exists solely to give wealthy young ladies something to fling at servants when their tea is not hot enough."

    vance "You. Girl. Pick it up."
    cora "Yes, Miss."

    "I bend down, praying the seams of my borrowed corset do not give way with a report like a pistol shot."
    "I retrieve the silver trinket. It is remarkably heavy for something that does nothing."

    vance "Not like that. Have you never handled anything delicate?"
    "Only my own survival, Miss, which is rather brittle."

    show gideon_sprite cold at right
    gideon "Vance. You are making yourself visible."
    vance "I was only correcting her."
    gideon "The girl is new. Do not teach her bad habits before luncheon."

    "I stand there holding the silver toy. I am apparently invisible now that the master has spoken."
    "Discretion at the Savoy is a wonderful thing: it allows the wealthy to argue as if we were part of the wallpaper, and allows us to listen with the same professional indifference."

    jump day101_2_missy_meets_cora_humour


label day101_2_missy_meets_cora_humour:
    scene bg_laundry_room_day
    with fade
    show missy_sprite smiling at center

    missy "You must be Cora."
    cora "I must be."
    missy "I'm Missy. Miss Stern said I'm to show you where things go. If I showed you everything we'd both be dead before tea."
    cora "Is the work always this warm?"
    missy "Oh, this is a pleasant day. Wait until the boilers get a sulk on. Last November one of them spat lye at a housemaid's bonnet and we had to buy her a new one out of the charity box."

    "I almost like her immediately. It is always a relief to find that the local machinery is operated by humans rather than gargoyles."
    call end_slot(outcome="d1_reflect_done")
