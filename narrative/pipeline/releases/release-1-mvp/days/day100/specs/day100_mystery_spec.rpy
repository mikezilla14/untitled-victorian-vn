# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day100_mystery_spec.rpy
# Release 1 / Day 00 / Prologue / Mystery Lens

label day100_main_mystery:
    scene bg_train_carriage_day
    with fade

    # [BEAT] Mystery: Clues in the carriage, secrets in the bag.
    "A secret is a physical weight. I feel it in the satchel, pressed flat between my knees."
    "I have forged references from Wiltshire, but the ink is too dark, the paper too heavy."
    "If anyone were to search... if the police were to question me..."
    "I must study the passengers. I must know the signs of suspicion."

    jump day100_2_discovery_flashback_mystery


label day100_2_discovery_flashback_mystery:
    scene bg_country_estate_study
    with dissolve
    play music "themes/melancholy"

    # [CLUE] Sir John's open desk and letters.
    "Sir John's desk was an archive of things he wished to bury."
    "He was a careful man, usually. He locked the cabinet. He burned the drafts."
    "But today, the keys were left in the lock."
    "And from the adjoining parlour, behind the oak door, came the sound."
    "A sharp, muffled cry. A secret slipping out."

    menu:
        "The sound behind the door, or the secrets on the desk?"

        "Eavesdrop at the parlour door. [Corruption focus: +15 Corruption]":
            $ apply_effects(insp=0, corr=15)
            $ story.set_prologue_found("overheard")
            jump day100_2_parlour_mystery

        "Examine the open letters. [Clue focus: +15 Inspiration, +10 Corruption]":
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            jump day100_2_desk_mystery


label day100_2_parlour_mystery:
    # [BEAT] Gathering the auditory clue.
    "I press my ear to the panel. I listen like a detective."
    "Sir John's voice is low, but the words are clear through the keyhole."
    "Sir John" "George, the letters are in the bureau. If someone..."
    "George" "The housemaid doesn't know the alphabet, John. She is safe."
    "I draw back. The letters. The letters are evidence."
    jump day100_2_reconvergence_mystery


label day100_2_desk_mystery:
    # [CLUE] Reading the evidence.
    "I lean over the bureau. My eyes scan the ink."
    "The letter is to George. It details dates, a room in London, a deposit in a London bank."
    "Cora" "He writes of a photograph. A photograph kept in a locked box at the Savoy."
    # [PAYOFF LATER] The Savoy lockbox photograph hook!
    "The Savoy. He is going there, then. He is keeping his secrets in the city."
    "I hear his footsteps returning. I slide the letters back into the slot."
    jump day100_2_reconvergence_mystery


label day100_2_reconvergence_mystery:
    # [BEAT] The discovery of the spy.
    "The door swings open. Sir John stands there."
    "His eyes go straight to the bureau, then to me."
    "Sir John" "What are you doing here, Vale?"
    "cora" "I was only dusting the cabinet, Sir."
    "Sir John" "Get out. You are dismissed. If a word of this leaves this library, I will ruin you."
    $ renpy.block_rollback()
    jump day100_3_awakening_mystery


label day100_3_awakening_mystery:
    scene bg_train_carriage_day
    with dissolve
    play sound "sfx/train_whistle"

    "The train whistle screams, pulling me back to Waterloo."
    "My satchel is open on the floorboards, its contents spilled."
    "The manuscript pages, yes, and the forged reference."
    "I gather them up, my mind turning over the clue I gathered."
    "Sir John has secrets. He has a lockbox at the Savoy."
    "I am going there. I have his hand, his writing, and his secrets in my head."
    jump day101_main
