# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day101_mystery_spec.rpy
# Release 1 / Day 01 / Mystery Lens

label day101_main_mystery:
    scene bg_savoy_corridor_morning
    with fade

    "The Savoy Hotel did not welcome girls like me."
    "It consumed them quietly, polished the brass to hide the bloodstains, and called the silence discretion."
    "The hotel was a labyrinth of locked doors, service shafts, and private staircases, where every guest had a name they had left at the station and a box they kept under the bed."
    "I had come to solve the cipher."

    jump day101_1_vance_throws_toy_mystery


label day101_1_vance_throws_toy_mystery:
    show vance_sprite angry at left
    "Then something small and silver strikes the skirting board and spins across the carpet, stopping near my shoe."
    "A lady's silver toy. A heavy, hollow thing. As it hits, I hear a tiny, metallic click from inside it."

    vance "You. Girl. Pick it up."

    "I bend. I retrieve the silver trinket."
    # [CLUE: The hollow trinket]
    "My thumb traces the seam. There is a hidden catch, worn smooth by frequent opening. A container for secrets, small enough to be carried in a glove."

    vance "Not like that. Have you never handled anything delicate?"

    show gideon_sprite cold at right
    gideon "Vance."
    "The Master stands there. His eyes do not look at my face; they drop instantly to my hand, where I hold the silver toy."
    "His fingers twitch slightly toward his pocket, where the shape of a key makes a small, sharp corner in the wool of his waistcoat."
    # [CLUE: The waistcoat key]

    gideon "The girl is new. Do not teach her bad habits before luncheon."

    "He steps forward, taking the trinket from my hand with a swiftness that is almost a snatch."
    "The exchange is too fast. He is hiding the click."

    jump day101_2_coras_path_choice_mystery


label day101_2_coras_path_choice_mystery:
    scene bg_servants_corridor_dim
    with fade

    "The servants' corridor behind the guest wing is a maze of identical doors."
    "The plaster walls are thin, but the carpets are thick enough to swallow all footsteps."
    "Beyond the service door near the Master Suite, we hear a muffled exchange."

    vance "Please. I understand. I do."

    show missy_sprite shocked at left
    missy "Should we fetch Miss Stern?"

    "Missy's eyes are wide. She knows the layout of this wing better than I do, but she doesn't know the maps the guests draw in their minds."

    menu:
        "Which path unlocks the door?"

        "Look for myself. [Prey path: +Inspiration, +Suspicion]":
            $ apply_effects(vance_susp=35, insp=15, corr=5)
            $ story.set_corridor_state("prey")
            cora "Stay there."
            cora "Quiet."

            "I press my eye to the narrow space between the door and the frame."
            "The room inside is dimly lit, but I can see Vance kneeling on the floor."
            "Her hands are empty. On the small writing desk behind her sits a mahogany box with brass corners."
            "The lid is open, exposing a velvet lining, but the contents are missing."
            # [CLUE: The empty box]
            "Mr. Locke holds her chin with two fingers."
            "Gideon" "Do we have an audience?"
            "I pull back. The latch of the service door makes a tiny rattle."
            "We run, our soft-soled shoes making no sound on the runner, but I keep the image of the open brass box locked in my mind."

    jump day101_3_taking_stock_day1_mystery


label day101_3_taking_stock_day1_mystery:
    scene bg_servants_quarters_dusk
    with fade

    "I open the ledger. The ink is black, a permanent record of the day's puzzles."
    "I draw three columns: Command, Witness, Consequence."
    "But beneath them, I write the three clues: The hollow toy with the hidden latch, the key in Gideon's waistcoat pocket, and the empty mahogany box in the Master Suite."
    # [PAYOFF LATER: The lockbox combination]
    "They are pieces of a puzzle that does not yet have a border."
    "I fold the page and slip my forged reference sheet beneath the leather cover. One day, the keys will match the locks."
    call end_slot(outcome="d1_reflect_done")
