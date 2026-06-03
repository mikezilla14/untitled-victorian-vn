# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes
#
# SPRITE DIRECTION (managed by scripts/scene_direction.py — how to preserve manual staging):
# [asset auto]              -> auto-placed sprite line; the agent may rewrite/replace it on re-run
# [asset keep]              -> on a show line: lock THAT line so the agent never edits it
# [asset lock:scene]        -> before/after a `scene`: the agent skips the entire scene block
# [asset pin:Name=slot]     -> force Name into slot for the rest of the scene block
# [enter:Name] / [exit:Name] -> declare cast changes so auto placement stays correct
# Full policy: docs/contracts/sprite_layout_policy.yaml | spec: docs/specs/scene-direction-agent.md

# ==========================================
# NODE MAP
# ==========================================
# day100_main (Morning) — voice tutorial, third-class carriage
# day100_1_afternoon_boredom — reading, Holywell note, ambition choices
# day100_2_evening_flashback — Wiltshire discovery (overheard / read_letters)
# day100_2_parlour_branch / day100_2_desk_branch → day100_2_reconvergence
# day100_3_night_daydream — manuscript fantasy (~2.8), wake at Waterloo
# day100_3_arrival — handoff → day101_main


# ==========================================
# MAIN ENTRY — MORNING (train, leaving the west)
# ==========================================

label day100_main:

    # [STATE] State/progression update
    $ set_time_period("Morning")

    scene bg_train_carriage_day
    with fade

    # [BEAT] Tutorial: three voices — narrator (world), cora_inner (mind), cora (mask)

    "The train pulls east. Iron joints click like latches closing behind me."

    cora_inner "Wiltshire is already a story I am no longer inside."
    cora_inner "I keep my knees tight and my elbows pinned, occupying as little space as the third-class bench will grant."

    # [BEAT] Light HUD tutorial on first stat touch

    "A stout passenger opposite me smells of wet wool and coal grease. His knee brushes my skirt when the carriage lurches. Improper. Almost warm."

    cora_inner "In the country I had a benefactor's roof. Here I have forged paper in my pocket and a satchel that weighs like guilt."
    cora_inner "If anyone reads my name wrong, I am not merely dismissed. I am unmasked."

    "I fold my hands the way a respectable maid should. My mouth stays shut."

    cora "Excuse me, sir. Might I pass?"

    cora_inner "Six words. Country vowels polished flat. Good."
    cora_inner "He hears a dull girl. Let him."

    "He grunts and shifts an inch. Not kindness — arithmetic."

    sys_msg "Cora's thoughts appear in italics. Her spoken lines are what others hear — shorter, safer."

    cora_inner "Board school taught me grammar. Service taught me when not to use it."
    cora_inner "London is not a destination. It is an audition I cannot fail."

    # [STATE] State/progression update
    $ apply_effects(insp=5)
    sys_msg "Inspiration fuels writing. Corruption tracks appetite. Both rise from choices — watch the sidebar."

    # [STATE] State/progression update
    jump day100_1_afternoon_boredom


# ==========================================
# AFTERNOON — boredom, reading, Holywell Street
# ==========================================

label day100_1_afternoon_boredom:

    # [STATE] State/progression update
    $ set_time_period("Afternoon")

    scene bg_train_carriage_day
    with dissolve

    "The sheep on the hillsides thin to slate roofs, then brick kilns, then a low soot that marks London's approach."

    cora_inner "Boredom on a train is a dangerous luxury. The mind roams where the body cannot."

    "I take out a cheap novel from the lending library shelf in my satchel — moral, tedious, approved."

    cora_inner "I read three pages and despise every virtuous heroine who faints on schedule."

    "Under the novel lies my own work: half-filled sheets in a hand too neat for honesty."

    cora_inner "Improper subject matter. Undone collars. Private hunger dressed as literature."
    cora_inner "I am not a reformer. I am a girl who needs coin and a name that is not laughed at."

    "Tucked beneath the manuscript is a creased handbill I have memorized without meaning to."

    "Cora (reading)" "'Holywell Street — discreet consideration of manuscripts of sensation. No sermons. No names returned to employers. Terms by interview.'"

    cora_inner "Illicit publishers behind respectable facades. The sort of street respectable men visit with their hats low."
    cora_inner "They pay for what housekeepers burn."

    # [CHOICE] Decision point
    menu:
        "Why am I really doing this?"

        "For the shillings home. [[+5 Inspiration]]":

            # [STATE] State/progression update
            $ apply_effects(insp=5)
            $ story.set_prologue_why_write("money_home")
            cora_inner "Mother's cough. Father's pride. Seven shillings a month if I keep my place — more if the pages sell."
            cora_inner "Sentiment is a luxury. Rent is not."

        "To catalogue what power hides. [[+5 Inspiration, +5 Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(insp=5, corr=5)
            $ story.set_prologue_why_write("cataloguer")
            cora_inner "I want the machine on paper — who kneels, who commands, who pretends."
            cora_inner "Truth is a weapon even when I am too small to swing it."

        "Because scandal tastes better than porridge. [[+10 Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(corr=10)
            $ story.set_prologue_why_write("scandal_hungry")
            cora_inner "I will not pretend innocence is a meal."
            cora_inner "The country taught me appetite has no rank. London will teach me price."

    # [CHOICE] Decision point
    menu:
        "The Holywell Street handbill promises discretion. How do I answer it in my head?"

        "Carefully — one chapter, no ruin. [[Holywell: careful]]":

            # [STATE] State/progression update
            $ story.set_prologue_holywell_posture("careful")
            cora_inner "I will walk that street as if I were buying ribbon. No gasps. No dropped names."

        "Eager — I need a publisher before courage fails. [[Holywell: eager, +5 Inspiration]]":

            # [STATE] State/progression update
            $ apply_effects(insp=5)
            $ story.set_prologue_holywell_posture("eager")
            cora_inner "The Savoy is cover. Holywell is the work. I can serve tables and still be an author after the lamps are lit."

        "Desperate — I will pay any fee they ask. [[Holywell: desperate, +5 Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(corr=5)
            $ story.set_prologue_holywell_posture("desperate")
            cora_inner "If they want spice, I will learn the recipe. I have already learned the heat."

    "My eyes grow heavy. The soot-smeared glass turns dark."
    cora_inner "The carriage glare dissolves into dark oak and velvet — a library I was expelled from."

    # [STATE] State/progression update
    jump day100_2_evening_flashback


# ==========================================
# EVENING — Wiltshire flashback (discovery)
# ==========================================

label day100_2_evening_flashback:

    # [STATE] State/progression update
    $ set_time_period("Evening")

    scene bg_country_estate_study
    with dissolve

    play music "themes/melancholy" fadein 1.5

    "Sir John's library was the only territory in Wiltshire where I could breathe — by license, not by right."

    cora_inner "Calfskin and dried roses. Tobacco sharp as reproach. Heat that did not belong to autumn."

    cora_inner "He let the library maid learn to read. Perhaps he thought titles made dusting efficient."
    cora_inner "A girl who reads does not stop at spines. She reads drawers. She reads men."

    "Tuesday afternoon. The house held its country drawl."
    "I had been sent to dust the bureau. The keys sat in the brass lock. Papers lay open like a dare."

    "From the adjoining parlour came a sound that was not tea nor footsteps."

    cora_inner "A gasp — ragged, wet. Leather creaking in rhythm."
    cora_inner "The raw margins of a house that sermons in public."

    # [CHOICE] Decision point
    menu:
        "The parlour's breath, or the desk's quiet ink?"

        "Press my ear to the parlour door. [[Overhear: +15 Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(corr=15)
            $ story.set_prologue_found("overheard")
            jump day100_2_parlour_branch

        "Read what the desk offers. [[Read letters: +15 Inspiration, +10 Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            jump day100_2_desk_branch


label day100_2_parlour_branch:

    "The murmur through the oak is not servants. It is appetite with the locks left off."

    cora_inner "To touch the handle would be dismissal. To listen is theft. I have always been a hungry thief."

    "I press my ear to the panel. The wood warms against my cheek."

    "Sir John" "No... George, please. The housemaid is in the study..."
    "George" "The housemaid does not exist, John. She is furniture that walks. Let the collar be undone."

    "Velvet rustles. A buckle clicks. A low groan from Sir John — helpless, stripped of parliamentary weight."

    cora_inner "My thighs press together under rough linen. The door seems to pulse, or my blood does."
    cora_inner "They speak of skin, of sweat, of a master kneeling where no vicar could see."
    cora_inner "The world is not rules and curtsies. It is secret rooms — and I am at the keyhole with a notebook in my bones."

    # [STATE] State/progression update
    jump day100_2_reconvergence


label day100_2_desk_branch:

    cora_inner "The parlour stays shut. The letters are louder."

    "My fingers find the top drawer. Sir John's hand — sloped, frantic, fevered."

    "Cora (reading)" "'...the taste of your skin in the shadow of the bureau remains my only memory. I have written your name on my palms... to feel your hands undo my collar, your mouth at the hollow of my throat while the household sleeps...'"

    cora_inner "Ink has weight. It pulls heat into the body — a pulse between the legs that reading ought not to teach."
    cora_inner "He writes of London, the Savoy, a locked box of photographic plates. He writes instruction."
    cora_inner "A maid who can copy such a hand is not a maid. She is a cataloguer with a key."

    # [STATE] State/progression update
    jump day100_2_reconvergence


label day100_2_reconvergence:

    "The latch clicks. Sir John stands in the doorway."

    "His collar is undone. His chest rises in ragged gasps. His eyes are glass with shame and fury."

    "Sir John" "Cora Vale."
    "cora" "Sir..."
    "Sir John" "You are dismissed. Leave before nightfall. Take your trunk."
    "Sir John" "If a word of what you have seen — or read — leaves your mouth, no decent house in England will have you. Your name will be blackened. You will be in the gutter where your quiet eyes belong."

    cora_inner "Threat and thrill share a pulse. Wiltshire ends here — in a man's undone collar."

    "The study dissolves. Iron rails take its place..."

    # [STATE] State/progression update
    $ renpy.block_rollback()

    jump day100_3_night_daydream


# ==========================================
# NIGHT — daydream (~2.8), wake, arrival
# ==========================================

label day100_3_night_daydream:

    # [STATE] State/progression update
    $ set_time_period("Night")

    scene bg_train_carriage_day
    with dissolve

    play sound "sfx/train_whistle"

    "A whistle tears through the tunnel-dark. My forehead strikes the cold glass."

    cora_inner "Not memory now. Hunger with the brakes off — the sort I sell on Holywell Street in dreams."

    if story.prologue_found == "overheard":
        cora_inner "I replay the parlour until the train rocks in time with it."
    else:
        cora_inner "I replay the ink until the letters move on my skin like hands."

    "The carriage is empty enough for sin if sin requires only a shut eye."

    if story.prologue_why_write == "money_home":
        cora_inner "I imagine a publisher counting shillings while I count breaths — respectable on the page, indecent underneath."
    elif story.prologue_why_write == "cataloguer":
        cora_inner "I imagine the scene filed under Power: Sir John on his knees, names crossed out, truth stamped PAID."
    else:
        cora_inner "I imagine the scene hotter than truth — collars torn because the reader paid for torn."

    "In the daydream I am not the maid at the door. I am the author who opened it."

    cora_inner "Holywell Street narrows to a lamp-lit window. A clerk with ink-stained cuffs does not ask if I am decent."
    cora_inner "He asks if the scene wets the page."

    "On the imagined page, wool gives way to skin. Propriety is a costume hung on a chair."

    if story.prologue_holywell_posture == "careful":
        cora_inner "I write the undoing slowly — a button, a breath, a blush — enough to sell, not enough to hang me."
    elif story.prologue_holywell_posture == "eager":
        cora_inner "I write faster than shame can catch me. The clerk slides coins across before the ink dries."
    else:
        cora_inner "I write until the clerk looks away, flushed. Desperation makes good spice. I hate that I know it."

    "The fantasy crests — not love, not virtue — only heat converted to currency."

    cora_inner "My hand tightens in my lap. The daydream is mine. The guilt is also mine. Both can travel to London."

    "The tunnel ends. Grey light returns."

    # [STATE] State/progression update
    jump day100_3_arrival


label day100_3_arrival:

    "My satchel has slipped. The buckle gapes."

    cora_inner "Pages scatter — my script, bold where it should be chaste: undone trousers, skin, a locked door."

    "The gentleman opposite lowers his newspaper. His gaze drifts toward the floor."

    cora "Forgive me, sir."

    cora_inner "Six words again. Steady. Stupid. Safe."

    "I sweep the sheets under my skirt before he reads a second line."

    cora_inner "If a conductor saw this, I would not lose the Savoy alone. I would lose the city."

    "He clears his throat and raises the paper — politeness as a wall."

    "I buckle the satchel. My fingers tremble."

    "Outside, Waterloo's iron ribs rise through smog."

    cora_inner "The Savoy waits — employment, mask, material."
    cora_inner "Holywell waits — payment, risk, the author I pretend I am destined to become."

    cora_inner "I bring the broom, the apron, the forged references."
    cora_inner "I bring the manuscript and the appetite that writes it."
    cora_inner "London does not welcome girls like me. It consumes them and polishes the brass after."
    cora_inner "Very well. Let it try."

    # [STATE] State/progression update
    $ time_manager.set_current_day(1)
    $ set_time_period("Morning")

    jump day101_main
