# day100.rpy
# Release 1 / Day 00 — Prologue (Wiltshire → London train → Day 101 handoff)
# Source: narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day100_non_canon.rpy

# ==========================================
# MAIN ENTRY — WILTSHIRE HOUSE AT NIGHT
# ==========================================

label day100_main:

    # [STATE] State/progression update
    $ set_time_period("Night")

    scene bg_country_estate_corridor_night
    with fade

    # [BEAT] Kinetic start in motion. Cora is sneaking through the dark hallway

    "Cora had three pages in her hand when the door opened."
    "She blew out the candle too late."

    cora_inner "Wiltshire at night is a cold vault, but my chest is tight and hot."
    cora_inner "I keep my boots in my left hand, the rough wool of my stockings catching on the bare floorboards."
    cora_inner "I know the layout of this estate intimately—every riser that groans, every latch that clicks."
    cora_inner "My secret manuscript pages are pressed flat against my ribs, hidden under my bodice."
    cora_inner "But these three pages are missing. Confiscated. Snatched from my trunk during the afternoon shift."

    "A floorboard creaks downstairs. I freeze, my breath catching in my throat."
    "I wait in the shadow of a grandfather clock, counting my heartbeats until the house resets to silence."

    cora_inner "I am terrified, but I am in control."
    cora_inner "Wiltshire has no room for a maid who writes. To they who rule, a maid is wallpaper that walks."
    cora_inner "If Sir John reads those pages, I am not merely dismissed. I am unmasked."

    # [STATE] State/progression update
    jump day100_1_afternoon_boredom_setup


label day100_1_afternoon_boredom_setup:

    # [STATE] State/progression update
    jump day100_1_afternoon_boredom


label day100_1_afternoon_boredom:

    # [ASSET] Visual/staging command
    scene bg_country_estate_study
    with dissolve

    # [BEAT] Entering the forbidden room (study) to retrieve pages

    cora_inner "Sir John's study. The door is slightly ajar—a sliver of dark mahogany."
    cora_inner "It smells of tobacco, dried roses, and the heavy, lingering heat of a dying fire."
    cora_inner "I must find the pages before the morning mail cart leaves for the station."
    cora_inner "They contain details he must never see. Appetite dressed as literature."

    # [CHOICE] Search location determines prologue_found flag
    menu:
        "Where did he hide them?"

        "In the walnut bureau drawer. [[Search the bureau: +15 Inspiration, +10 Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")

            cora_inner "The bureau is where his private correspondence lies. Sir John's own secrets."

            # [STATE] State/progression update
            jump day100_2_desk_branch

        "By the parlour settee. [[Search the parlour entrance: +15 Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(corr=15)
            $ story.set_prologue_found("overheard")

            cora_inner "The parlour door. If he took them there, he may have left them on the small table."

            # [STATE] State/progression update
            jump day100_2_parlour_branch


label day100_2_evening_flashback:
    if story.prologue_found == "read_letters":

        # [STATE] State/progression update
        jump day100_2_desk_branch
    else:

        # [STATE] State/progression update
        jump day100_2_parlour_branch


label day100_2_parlour_branch:

    # [BEAT] Erotic/Tension: Overhearing the master's private, scandalous affair

    "I press my ear to the parlour door. The cold oak warms immediately against my cheek."
    "The murmur through the wood is not servants. It is Sir John and George, the master of stables."
    "The voices are hushed, heavy with an appetite that has no name in Wiltshire."

    "Sir John" "No... George, please. The housemaid is in the study..."
    "George" "The housemaid does not exist, John. She is furniture that walks. Let the collar be undone."

    "A buckle clicks. A low groan from Sir John—helpless, stripped of his parliamentary weight."
    "My thighs press together under rough linen. The door seems to pulse, or my blood does."

    cora_inner "Secret rooms, undone collars. I am at the keyhole with a notebook in my bones."

    # [STATE] State/progression update
    jump day100_2_reconvergence


label day100_2_desk_branch:

    # [BEAT] Erotic/Mystery: Reading Sir John's letters containing Strand/Savoy lockbox clues

    "My fingers scramble through the desk drawers, paper rustling under my nails."
    "Under a stack of rent rolls, I find a bundle of letters in Sir John's sloped, wild hand."

    "Cora (reading)" "'...the taste of your skin in the shadow of the bureau remains my only memory. I have written your name on my palms... to feel your hands undo my collar, your mouth at the hollow of my throat...'"
    "Cora (reading)" "'...the locked box of photographic plates remains at the Savoy, the key secured with the solicitor on the Strand...'"

    cora_inner "Ink has weight. It pulls heat into the body—a pulse between the legs that reading ought not to teach."
    cora_inner "He writes of London, of a secret box. And I have read his blood in the ink."

    # [STATE] State/progression update
    jump day100_2_reconvergence


label day100_2_reconvergence:

    # [BEAT] Hiding and Caught. High tension, quiet confrontation

    "A key turns in the hallway lock. Footsteps approach."
    "Panic. I slide behind the folding velvet screen, holding my breath, my back pressed against the cold glass."
    "Sir John enters. He has my three missing manuscript pages in his hand."
    "He does not search the room. His eyes go straight to the screen."

    "Sir John" "Come out, Vale."

    "The quietness of his voice is worse than a shout. It is the absolute authority of the house."
    "I step out from the shadow of the screen."

    # [CHOICE] Caught reaction sets the prologue_holywell_posture flag
    menu:
        "How do I answer?"

        "Lie — I was seeking a draft in the study. [[Careful posture]]":

            # [STATE] State/progression update
            $ story.set_prologue_holywell_posture("careful")

            cora "There was a draft, sir."

            cora_inner "My voice is level, country-flat. Let him hear a simpleton."
            cora_inner "I must protect my secrets. A careful posture is the safest mask."

        "Deflect — they are my pages. [[Eager posture]]":

            # [STATE] State/progression update
            $ apply_effects(insp=5)
            $ story.set_prologue_holywell_posture("eager")

            cora "They are my pages, sir."

            cora_inner "A dangerous word from a maid in a borrowed apron. I will not cower."
            cora_inner "My writing is mine. I want a publisher before my courage fails."

        "Submit — throw myself on his mercy. [[Desperate posture]]":

            # [STATE] State/progression update
            $ apply_effects(corr=5)
            $ story.set_prologue_holywell_posture("desperate")

            cora "Forgive me, sir."

            cora_inner "I bend my neck. Let him believe the submission is real."
            cora_inner "I am desperate. I will pay whatever price London demands."

    "Sir John looks at the pages, his chest rising in ragged gasps. His collar is undone, his skin flushed."
    "Sir John" "You write of skin. Of trousers. Of things a decent housemaid does not even know the names of."
    "Sir John" "You observed too clearly, Vale. And you wrote too well."
    "Sir John" "Why did you write this filth?"

    # [CHOICE] Ambition choice sets the prologue_why_write flag
    menu:
        "Why did I write it?"

        "For the shillings home. [[+5 Inspiration]]":

            # [STATE] State/progression update
            $ apply_effects(insp=5)
            $ story.set_prologue_why_write("money_home")

            cora_inner "Mother's cough. Father's pride. Shillings are the only language they understand."
            cora_inner "Sentiment is a luxury. Rent is not."

        "To catalogue what power hides. [[+5 Inspiration, +5 Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(insp=5, corr=5)
            $ story.set_prologue_why_write("cataloguer")

            cora_inner "I want the machine on paper—who kneels, who commands, who pretends."
            cora_inner "Truth is a weapon even when I am too small to swing it."

        "Because scandal tastes better than porridge. [[+10 Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(corr=10)
            $ story.set_prologue_why_write("scandal_hungry")

            cora_inner "I will not pretend innocence is a meal."
            cora_inner "Wiltshire taught me appetite. London will teach me price."

    "Sir John Crumples the three pages into his pocket. His gaze is dark with shame and fury."
    "Sir John" "You are dismissed. Pack your trunk. You leave for London on the morning train."

    cora "I understand, sir."

    "Sir John" "I will give you a reference for the Savoy, Vale. But if a word of what you have seen—or written—leaves your mouth, no decent house in England will have you."
    "Sir John" "Your name will be blackened. You will be in the gutter."

    cora_inner "Threat and thrill share a pulse. Wiltshire ends here."

    # [STATE] State/progression update
    $ renpy.block_rollback()

    jump day100_3_night_daydream


# ==========================================
# TRAIN TRANSITION — WATERLOO & DAYDREAM
# ==========================================

label day100_3_night_daydream:

    # [STATE] State/progression update
    $ set_time_period("Night")

    scene bg_train_carriage_day
    with dissolve

    "The train pulls east. Iron joints click like latches closing behind me."
    "Coal smoke, damp wool, rain on glass. The third-class bench is hard."

    cora_inner "London is not a destination. It is an escape with teeth."
    cora_inner "Wiltshire recedes into the smog. My satchel is at my feet, my manuscript hidden inside."

    # [BEAT] Daydream: 2.8 spice level reliving the discovery

    cora_inner "If I close my eyes, the coal grease smells of the library's velvet heat."

    if story.prologue_found == "overheard":
        cora_inner "I replay the parlour's breath until the carriage rocks in time with it."
        cora_inner "George's fingers pulling Sir John's collar open. Sir John's helpless, gasping surrender."
        cora_inner "The raw reality of master kneeling where no vicar could see."
    else:
        cora_inner "I replay the letters' ink until the words move on my skin like Sir John's palms."
        cora_inner "The touch at the bureau, the mouth at the hollow of the throat."
        cora_inner "Desire written in black ink, transferring heat to my thighs."

    cora_inner "In the daydream I am not the maid at the door. I am the author who opened it."

    if story.prologue_holywell_posture == "careful":
        cora_inner "I write the undoing slowly—a button, a breath—enough to sell, not enough to hang me."
    elif story.prologue_holywell_posture == "eager":
        cora_inner "I write faster than shame can catch me. Slide the coins across before the ink dries."
    else:
        cora_inner "I write until the reader looks away, flushed. Desperation makes good spice."

    cora_inner "The fantasy is mine, and the hunger travels with me to London."

    # [STATE] State/progression update
    jump day100_3_arrival


label day100_3_arrival:

    "The train whistle screams. A metal throat tearing through the smog."
    "The carriage lurches as we hit the Waterloo points. My satchel slips."
    "Pages scatter across the dirty floorboards—my manuscript, bold where it should be chaste."

    "The gentleman opposite lowers his newspaper. His gaze drifts toward the floor."

    cora "Forgive me, sir."

    cora_inner "Three words. Flat. Safe."
    "I sweep the sheets under my skirt before he can read a single line."

    "He clears his throat and raises the paper—politeness as a wall."
    "I buckle the satchel. My fingers tremble."

    "Outside, Waterloo's iron ribs rise through the soot."

    cora_inner "The Savoy waits—employment, mask, material."
    cora_inner "Holywell waits—payment, risk, the author I pretend I am destined to become."
    cora_inner "Very well. Let it try."

    # [STATE] Handoff to Day 101 Morning
    $ time_manager.set_current_day(1)
    $ set_time_period("Morning")

    jump day101_main
