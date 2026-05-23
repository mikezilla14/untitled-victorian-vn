# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day101_class_spec.rpy
# Release 1 / Day 01 / Class & Etiquette Lens

label day101_main_class:
    scene bg_savoy_corridor_morning
    with fade

    "The Savoy Hotel did not welcome girls like me."
    "It consumed them quietly, polished the brass after, and called the result service."
    "Every inch of this place was mapped by class. The grand marble steps were for guest slippers; the narrow, uncarpeted pine stairs were for the servants' boots."
    "To step across the threshold between them was a transgression of spatial law."

    jump day101_1_morning_interview_class


label day101_1_morning_interview_class:
    scene bg_savoy_corridor_morning
    with dissolve
    show stern_sprite neutral at center

    "Miss Stern stands rather than sits."
    # [ADDRESS: Forms of address and posture]
    "She has the rigid posture of the lower-middle class mimicking the nobility to control the poor."
    "Her eyes scan my apron, checking the starch and the alignment of the seams."

    stern "Cora Vale."
    cora "Yes, Ma'am."
    stern "Wishing is for girls with leisure. You will work because you are told. A maid in this house is hands without noise, feet without weight, and memory without a tongue. Can you be that?"

    menu:
        "How do I survive Stern's inspection?"

        "Lower my eyes. Let her mistake fear for obedience.":
            $ apply_effects(stern_susp=5, insp=5, corr=0)
            $ story.set_day1_interview_state("meek")
            cora "I can, Ma'am. I wish to work."
            stern "Wishing is for girls with leisure. You will work because you are told."
            cora "Yes, Ma'am."
            "The traditional submissive response. I keep my head bent at the exact fifteen-degree angle required of country girls."

        "Answer cleanly. Let competence do what meekness cannot.":
            $ apply_effects(stern_susp=15, insp=10, corr=0)
            $ story.set_day1_interview_state("competent")
            cora "I can be quiet, quick, and exact."
            stern "Exact? A dangerous word from a girl in a borrowed apron."
            "She resents the vocabulary. Maids are expected to have vocabularies of monosyllables."

    jump day101_1_vance_throws_toy_class


label day101_1_vance_throws_toy_class:
    show vance_sprite angry at left
    "Then something small and silver strikes the skirting board and rolls across the corridor carpet, stopping near my shoe."
    "A lady's toy. Miss Vance flings it as if the corridor were her private nursery."

    vance "You. Girl. Pick it up."
    cora "Yes, Miss."

    "I bend. I retrieve the silver trinket, taking care to touch only the metal, avoiding her kidskin gloves as I return it."
    # [ETIQUETTE: Hands off guest skin]

    vance "Not like that. Have you never handled anything delicate?"

    show gideon_sprite cold at right
    gideon "Vance."
    "The Master's voice has the cold, flat tone of absolute ownership."

    vance "I was only correcting her."
    gideon "You were making yourself visible."
    gideon "The girl is new. Do not teach her bad habits before luncheon."

    "He speaks of me as if I were a young retriever, not yet broken to the gun."
    "I stand in the silence, keeping the toy balanced on the palm of my hand until Vance snatches it."

    jump day101_2_coras_path_choice_class


label day101_2_coras_path_choice_class:
    scene bg_servants_corridor_dim
    with fade

    "The servants' corridor behind the guest wing is narrow, built of plain timber and grey paint, hidden behind the mahogany door of the Master Suite."
    "Beyond that door, we hear a muffled cry."

    vance "Please. I understand. I do."

    show missy_sprite shocked at left
    missy "Should we fetch Miss Stern?"

    "Missy's hand is on the laundry stack. She is terrified of crossing the threshold into guest business."

    menu:
        "How do I respect the boundaries?"

        "Pull Missy away. [Ghost path: +Inspiration, -Suspicion]":
            $ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5, insp=10, corr=0)
            $ story.set_corridor_state("ghost")
            cora "No."
            cora "Then Stern already knows, or Stern has chosen not to know. Either way, we are not the cure."
            "I pull her back by the sleeve of her coarse linen dress."
            "The first law of survival in service: never witness a master's failure of etiquette unless you have the leverage to survive it."

    call end_slot(outcome="d1_reflect_done")
