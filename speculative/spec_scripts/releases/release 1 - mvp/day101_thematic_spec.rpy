# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day101_thematic_spec.rpy
# Release 1 / Day 01 / Thematic Lens

label day101_main_thematic:
    scene bg_savoy_corridor_morning
    with fade

    "The Savoy Hotel did not welcome girls like me."
    "It consumed them quietly, polished the brass after, and called the result service."
    "The soot of London hung outside the windows, a grey shroud pressing against the glass, trying to look in at the gold leaf and marble."
    "Here, cleanliness was not next to godliness; it was a luxury bought with other people's blood."

    jump day101_1_morning_interview_thematic


label day101_1_morning_interview_thematic:
    scene bg_savoy_corridor_morning
    with dissolve
    show stern_sprite neutral at center

    "Miss Stern stands rather than sits. She is a pillar of dark wool and iron discipline, a warden of the hotel's silent machine."
    "Her eyes move from my cap to my boots, weighing every inch of my body for any sign of rural rot."

    stern "Cora Vale."
    cora "Yes, Ma'am."
    stern "Wishing is for girls with leisure. You will work because you are told."
    cora "Yes, Ma'am."

    "She hears a dull country girl. A blank slate she can write the hotel's rules upon."
    "Let her believe she owns the pen."

    jump day101_1_vance_throws_toy_thematic


label day101_1_vance_throws_toy_thematic:
    show vance_sprite angry at left
    "Then something small and silver strikes the skirting board and spins across the carpet."
    "A lady's silver trinket. A heavy, useless thing, forged in Birmingham to be dropped in London."

    vance "You. Girl. Pick it up."

    "I bend. The cold silver bites my fingers. A physical reminder of the distance between those who drop and those who retrieve."

    show gideon_sprite cold at right
    gideon "Vance."
    "One word. The corridor changes temperature, the gold leaf on the walls suddenly feeling cold and sharp as needles."

    jump day101_2_coras_path_choice_thematic


label day101_2_coras_path_choice_thematic:
    scene bg_servants_corridor_dim
    with fade

    # [BEAT] The keyhole as a moral lens.
    "The servants' corridor is a throat of bare plaster and gas-hiss. It carries sound the way a body carries fever."
    "Through the service door near the Master Suite, we hear a muffled cry."

    vance "Please. I understand. I do."

    "Missy goes still, her stack of white sheets trembling like birch leaves."
    "The moment is the choice of what I become in order to use it."

    menu:
        "How do I take the material?"

        "Let Missy's concern open the door. [Predator path: +Inspiration, +Corruption]":
            $ apply_effects(missy_susp=10, insp=10, corr=5)
            $ story.set_corridor_state("predator")
            cora "You may be right. If she's hurt, someone should check."

            "I step back into the shadows. I use Missy's clean heart as a shield, pushing her toward the keyhole while I watch from the dark."
            "The division of labor: she takes the guilt, I take the story."

        "Pull Missy away. [Ghost path: +Inspiration, -Suspicion]":
            $ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5, insp=10, corr=0)
            $ story.set_corridor_state("ghost")
            cora "No."
            "I pull her wrist. We are shadow-people here; if we touch the gold leaf, we leave grey finger-prints."

    jump day101_4_write_the_chapter_thematic


label day101_4_write_the_chapter_thematic:
    scene bg_cora_desk_night
    with dissolve

    "My narrow room is a cell of unpainted pine, smelling of cheap tallow and damp plaster."
    "I open the ledger. The paper is rough, wood-pulp that remembers the forest it was torn from."
    "My pen is the only part of me that does not wear an apron."

    "I write a maid who learns that innocence is a tool left unattended. She places a sweeter girl before a dangerous door and discovers that guilt has a sweet, metallic taste."
    "The soot outside the window presses closer, a silent editor watching my progress."
    "Tomorrow I will carry the towels. Tonight, I carry the ink."
    call end_slot(outcome="d1_write_ch1")
