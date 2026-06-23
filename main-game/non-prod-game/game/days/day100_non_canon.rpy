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
# day100_main (Night) — kinetic crawl; Irish linguistic vigilance
# day100_1_afternoon_boredom — Lady Eleanor's rooms; search choices
# day100_2_evening_flashback — (compat bridge, routes to search resolution)
# day100_2_parlour_branch / day100_2_desk_branch → day100_2_reconvergence
# day100_3_night_daydream — train daydream (~2.8–3.0 spice level)
# day100_3_arrival — Waterloo arrival & Day 101 handoff


# ==========================================
# MAIN ENTRY — WILTSHIRE HOUSE AT NIGHT
# ==========================================

# [DAG_NODE id=day100_main type=work day=100]
label day100_main:

    # [STATE] State/progression update
    $ set_time_period("Night")

    scene bg_country_estate_corridor_night
    with fade

    # [enter:Cora]
    show cora_sprite base at centre_bust with moveinright # [asset auto]
    show cora_sprite base at centre_bust:
        zoom 1.2
        ypos 0.9

    # [ASSET] Visual/staging command
    show vance_sprite base at left:
        ypos 0.98
        xpos 0.15
        zoom 0.6

    # [BEAT] Kinetic start in motion. Cora hunts confiscated manuscript pages before dawn

    "Cora had three pages in her hand when the door opened."
    "She blew out the candle too late."

    cora_inner "Wiltshire at night is a cold vault, but my chest is tight and hot."
    cora_inner "I keep my boots in my left hand, the rough wool of my stockings catching on the bare floorboards."
    cora_inner "I know every riser that groans, every latch that clicks — the map a fugitive maid learns."
    cora_inner "My secret manuscript pages are pressed flat against my ribs, hidden under my bodice."
    cora_inner "But three pages are missing. Confiscated. Snatched from my trunk while I scrubbed the grates."

    "A grandfather clock tolls three. The vibration runs through the floorboards like a warning."

    cora_inner "In my head the words come soft, looping — my mother's Cork lilt. I swallow it whole."
    cora_inner "Out loud I must be flat. English. Sterile. One slip and I am Irish street-grub, not Vale the maid."

    "A floorboard creaks downstairs. I freeze, my breath catching in my throat."
    "I wait in the clock's shadow, counting heartbeats until the house resets to silence."

    cora_inner "I am terrified, but I am in control."
    cora_inner "Wiltshire has no room for a maid who writes. To they who rule, a maid is wallpaper that walks."
    cora_inner "If the Lady read those pages, she will have me stripped and searched. If Sir John reads them, I am unmasked."

    # [STATE] State/progression update
    jump day100_1_afternoon_boredom_setup


# Compat stub to keep labels consistent
label day100_1_afternoon_boredom_setup:

    # [STATE] State/progression update
    jump day100_1_afternoon_boredom


# [DAG_NODE id=day100_1_afternoon_boredom type=work day=100]
label day100_1_afternoon_boredom:

    # [ASSET] Visual/staging command
    scene bg_country_estate_study
    with dissolve

    # [enter:Cora]
    show cora_sprite base at centre_bust with moveinright # [asset auto]
    show cora_sprite guarded_travel at left_bust # [asset keep]
    # [BEAT] Entering Lady Eleanor's private study to retrieve confiscated pages

    cora_inner "Lady Eleanor's withdrawing room. The door stands open by a finger's width."
    cora_inner "It smells of costly amber, lavender-water, and the wet coal-smog leaking from the hearth."
    cora_inner "I must find my pages before the morning train. They hold appetite dressed as literature."
    cora_inner "Where would Eleanor Wiltshire hide evidence of a servant's transgressive imagination?"

    # [CHOICE] Search location determines prologue_found flag
    # [DAG_CHOICE group=day100_1_afternoon_boredom_menu_1]
    menu:
        "Where did she hide them?"

        "In the walnut bureau drawer. [[Search the bureau: Careful, corrupting]]":

            # [STATE] Semantic balance profile: Cora snoops through Lady Eleanor's private correspondence
            $ apply_balanced_effect("curious", intensity="major")
            $ story.set_prologue_found("read_letters")

            cora_inner "The bureau is where she locks the letters that make her hands tremble."

            # [STATE] State/progression update
            jump day100_2_evening_flashback

        "By the private parlour settee. [[Search the parlour entrance: Transgressive]]":

            # [STATE] Semantic balance profile: Cora chooses the riskier entrance to eavesdrop
            $ apply_balanced_effect("transgressive", intensity="major")
            $ story.set_prologue_found("overheard")

            cora_inner "The small parlour. A muffled gasp slips from behind the heavy velvet drapes."

            # [STATE] State/progression update
            jump day100_2_evening_flashback


# Compat bridge for routing
# [DAG_NODE id=day100_2_evening_flashback type=work day=100]
label day100_2_evening_flashback:
    if story.prologue_found == "read_letters":

        # [STATE] State/progression update
        jump day100_2_desk_branch
    else:

        # [STATE] State/progression update
        jump day100_2_parlour_branch


# [DAG_NODE id=day100_2_parlour_branch type=work day=100]
label day100_2_parlour_branch:

    # [BEAT] Erotic/Tension: Cora witnesses Lady Eleanor's illicit encounter with the under-housemaid Margaret

    show cora_sprite flushed at left_bust # [asset keep]

    "I press my forehead to the cold paneling, my eye aligned with the keyhole's narrow slit."
    "The air through the wood is hot — damp skin, crushed violets, the iron sweetness of fear."

    "Lady Eleanor's silk dinner dress is piled at her waist like discarded skin."
    "Margaret, the under-housemaid, kneels between her thighs. Her rough hands grip Eleanor's pinned hair."
    "The Lady of the house arches against the settee, her white throat straining, her mouth open on a breathless sob."

    "Lady Eleanor" "Hush, Margaret... if Sir John should wake..."
    "Margaret" "Then let him wake, my Lady. You asked me to stay."

    "The sound of fabric tearing softly. A harsh, filthy whisper. Eleanor does not push her away."
    "She clings to the girl's coarse sleeves, her fine rings catching on plain linen."

    "My thighs press together under rough wool. The absolute hypocrisy of it."
    "This is the woman who lectures the village girls on modesty and chastity."

    cora_inner "So the saint of Wiltshire opens in the dark for a maid's rough hands."
    cora_inner "Blood hums between my legs — not shame, but a sudden, blinding tally of power."
    cora_inner "A Lady's ruin is total. I file that away like ink."

    # [STATE] State/progression update
    jump day100_2_reconvergence


# [DAG_NODE id=day100_2_desk_branch type=work day=100]
label day100_2_desk_branch:

    # [BEAT] Erotic/Mystery: Lady Eleanor's letters to Margaret; Sir John's Savoy lockbox clue among the papers

    show cora_sprite focused at left_bust # [asset keep]

    "My fingers slide through the drawers like a thief in the night, paper rustling under my nails."
    "Deep beneath charity ledgers, wrapped in soiled ribbon, I find a packet in Lady Eleanor's elegant sloped hand."

    "Cora (reading)" "'...when you pinned me against the laundry press, with your mouth at my throat... I have never felt such low, delicious agony. To have my wrists held in your plain, strong hands...'"
    "Cora (reading)" "'...if Sir John should suspect, I am ruined — my name, my children, everything. But my body is no longer mine when you enter the room...'"

    "Under the ribbon packet, a single sheet in a man's wild hand — Sir John's, unmistakable."

    "Cora (reading)" "'...the locked box of photographic plates remains at the Savoy, the key secured with the solicitor on the Strand...'"

    cora_inner "Ink has weight. It pulls heat into the body — a pulse between the legs that reading ought not to teach."
    cora_inner "She preaches temperance downward while drowning in a maid's plain sleeves."
    cora_inner "And he writes of London, of a secret box. I have read their blood in the ink."

    # [STATE] State/progression update
    jump day100_2_reconvergence


# [DAG_NODE id=day100_2_reconvergence type=work day=100]
label day100_2_reconvergence:

    # [BEAT] Lady catches Cora; Sir John dismisses at his wife's behest

    show cora_sprite guarded_travel at left_bust # [asset keep]

    "A sharp rustle behind me. The door swings wide."
    "Lady Eleanor stands in the threshold. Her hair is wild, her collar crooked, her eyes wide with manic terror."
    "She has my three missing manuscript pages clutched in her hand. She knows what I have seen."

    # [enter:Lady_eleanor]
    show lady_eleanor_sprite panicked at right_bust with moveinright # [asset auto]
    lady_eleanor "You... you Irish guttersnipe."
    lady_eleanor "You dare search my rooms? You dare write this filth about flesh and touch?"

    cora_inner "Careful. My head screams in my mother's soft, looping lilt. Swallow it. Choke it down."
    cora_inner "Flat tongue. English country girl. She must not hear the Cork in my throat."

    lady_eleanor "I will not have your eyes in this house another hour. Sir John! Sir John!"

    "Footsteps in the hall. Sir John enters — collar straight, face grey, authority intact."
    "He takes the manuscript pages from his wife's shaking hand. His gaze finds me."

    # [enter:Sir_john]
    show lady_eleanor_sprite panicked at centre_bust with move # [asset auto]
    show sir_john_sprite cold at right_bust with moveinright # [asset auto]
    sir_john "Come out, Vale."

    "The quietness of his voice is worse than a shout. It is the absolute authority of the house."
    "I step out from beside the bureau."

    # [CHOICE] Caught reaction sets the prologue_holywell_posture flag
    # [DAG_CHOICE group=day100_1_afternoon_boredom_menu_2]
    menu:
        "How do I answer?"

        "Lie — I was seeking a draft in the study. [[Careful posture]]":

            # [STATE] State/progression update
            $ story.set_prologue_holywell_posture("careful")

            cora "There was a draft, sir."

            cora_inner "My voice is level, country-flat. Let him hear a simpleton."
            cora_inner "I must protect my secrets. A careful posture is the safest mask."

        "Deflect — they are my pages. [[Eager posture]]":

            # [STATE] Semantic balance profile: Cora asserts herself without full submission
            $ apply_balanced_effect("observant", intensity="minor")
            $ story.set_prologue_holywell_posture("eager")

            cora "They are my pages, sir."

            cora_inner "A dangerous word from a maid in a borrowed apron. I will not cower."
            cora_inner "My writing is mine. I want a publisher before my courage fails."

        "Submit — throw myself on his mercy. [[Desperate posture]]":

            # [STATE] Semantic balance profile: Cora performs surrender to survive dismissal
            $ apply_balanced_effect("obedient", intensity="minor")
            $ story.set_prologue_holywell_posture("desperate")

            cora "Forgive me, sir."

            cora_inner "I bend my neck. Let him believe the submission is real."
            cora_inner "I am desperate. I will pay whatever price London demands."

    lady_eleanor "Send her away. Tonight. Before she breathes a word in the village."

    "Sir John looks at the pages. His chest rises once — controlled, cold."
    sir_john "You write of skin. Of touch. Of things a decent housemaid should not name."
    sir_john "You observed too clearly, Vale. And you wrote too well."
    sir_john "Why did you write this filth?"

    # [CHOICE] Ambition choice sets the prologue_why_write flag
    # [DAG_CHOICE group=day100_2_evening_flashback_menu_1]
    menu:
        "Why did I write it?"

        "For the shillings home. [[Practical ambition]]":

            # [STATE] Semantic balance profile: Cora frames writing as household necessity
            $ apply_balanced_effect("safe", intensity="minor")
            $ story.set_prologue_why_write("money_home")

            cora_inner "Mother's cough. Father's pride. Shillings are the only language they understand."
            cora_inner "Sentiment is a luxury. Rent is not."

        "To catalogue what power hides. [[Curious, corrupting]]":

            # [STATE] Semantic balance profile: Cora admits she maps power for the manuscript
            $ apply_balanced_effect("curious", intensity="minor")
            $ story.set_prologue_why_write("cataloguer")

            cora_inner "I want the machine on paper — who kneels, who commands, who pretends."
            cora_inner "Truth is a weapon even when I am too small to swing it."

        "Because scandal tastes better than porridge. [[Transgressive]]":

            # [STATE] Semantic balance profile: Cora embraces scandal as appetite
            $ apply_balanced_effect("transgressive", intensity="standard")
            $ story.set_prologue_why_write("scandal_hungry")

            cora_inner "I will not pretend innocence is a meal."
            cora_inner "Wiltshire taught me appetite. London will teach me price."

    "Sir John crumples the three pages into his pocket. Lady Eleanor watches, white as flour."
    sir_john "My wife is correct. Pack your trunk. You leave on the morning train."

    cora "I understand, sir."

    sir_john "I will give you a reference for the Savoy, Vale. But if a word of what you have seen — or written — leaves your mouth, no decent house in England will have you."
    sir_john "Your name will be blackened. You will be in the gutter."

    cora_inner "Threat and thrill share a pulse. A Lady's ruin is absolute; a Lord's is negotiable."
    cora_inner "If their secrets have weight, perhaps mine will too — one day. Not tonight."
    cora_inner "Wiltshire ends here."

    # [STATE] State/progression update
    $ renpy.block_rollback()

    jump day100_3_night_daydream


# ==========================================
# TRAIN TRANSITION — WATERLOO & DAYDREAM
# ==========================================

# [DAG_NODE id=day100_3_night_daydream type=work day=100]
label day100_3_night_daydream:

    # [STATE] State/progression update
    $ set_time_period("Night")

    scene bg_train_carriage_day
    with dissolve

    # [enter:Cora]
    show cora_sprite base at centre_bust with moveinright # [asset auto]
    show cora_sprite base_travel at left_bust # [asset keep]
    "The train pulls east. Iron joints click like latches closing behind me."
    "Coal smoke, damp wool, rain on glass. The third-class bench is hard."

    cora_inner "London is not a destination. It is an escape with teeth."
    cora_inner "Wiltshire recedes into the smog. My satchel is at my feet, my manuscript hidden inside."
    cora_inner "They will think me an English country girl. They must never hear the Cork in my throat."

    cora_inner "To survive there, I must decide what shape I will take. How will I move through the Savoy?"

    # [CHOICE] Archetype seed choice
    menu:
        "How will I survive in London?"

        "By becoming unseen, listening, and moving through the gaps. [[Ghost Focus: +1 Ghost]]":

            # [STATE] State/progression update
            $ story.set_run_archetype_seed("ghost")
            $ apply_archetype_edge("ghost", 1)
            cora_inner "Yes. Let them look past me. I will be the shadow that hears everything and says nothing."
            cora_inner "A ghost is never trapped. A ghost has already escaped."

        "By reading the threat, appeasing them, and redirecting the danger. [[Prey Focus: +1 Prey]]":

            # [STATE] State/progression update
            $ story.set_run_archetype_seed("prey")
            $ apply_archetype_edge("prey", 1)
            cora_inner "Yes. I will know their weight before they swing it. I will bend so I do not break."
            cora_inner "The prey knows the forest better than the hunter ever will."

        "By testing their boundaries, baiting them, and beginning to use them as material. [[Predator Focus: +1 Predator]]":

            # [STATE] State/progression update
            $ story.set_run_archetype_seed("predator")
            $ apply_archetype_edge("predator", 1)
            cora_inner "Yes. I will find where they are soft. I will provoke them until they show their teeth, and then I will write it."
            cora_inner "Let them hunt. I will be the one who feeds on the aftermath."

    # [BEAT] Daydream: 2.8–3.0 spice level reliving the discovery

    cora_inner "If I close my eyes, the coal grease smells of the withdrawing room's velvet heat."

    if story.prologue_found == "overheard":
        cora_inner "I replay the parlour's breath until the carriage rocks in time with it."
        cora_inner "Margaret's rough hands in Eleanor's pinned hair. The Lady's helpless, gasping surrender."
        cora_inner "The raw reality of mistress opened where no vicar could see."
    else:
        cora_inner "I replay the letters' ink until the words move on my skin like Margaret's plain sleeves."
        cora_inner "Wrists held at the laundry press. Mouth at the throat. Eleanor's ink-wet confession."
        cora_inner "Desire written in black ink, transferring heat to my thighs."

    cora_inner "In the daydream I am not the maid at the door. I am the author who opened it."

    if story.prologue_holywell_posture == "careful":
        cora_inner "I write the undoing slowly — a button, a breath — enough to sell, not enough to hang me."
    elif story.prologue_holywell_posture == "eager":
        cora_inner "I write faster than shame can catch me. Slide the coins across before the ink dries."
    else:
        cora_inner "I write until the reader looks away, flushed. Desperation makes good spice."

    cora_inner "The fantasy is mine, and the hunger travels with me to London."

    # [STATE] State/progression update
    jump day100_3_arrival


# [DAG_NODE id=day100_3_arrival type=work day=100]
label day100_3_arrival:

    "The train whistle screams. A metal throat tearing through the smog."
    "The carriage lurches as we hit the Waterloo points. My satchel slips."
    "Pages scatter across the dirty floorboards — my manuscript, bold where it should be chaste."

    "The gentleman opposite lowers his newspaper. His gaze drifts toward the floor."

    cora "Forgive me, sir."

    cora_inner "Three words. Flat. Safe. English as a parson's daughter."
    "I sweep the sheets under my skirt before he can read a single line."

    "He clears his throat and raises the paper — politeness as a wall."
    "I buckle the satchel. My fingers tremble."

    "Outside, Waterloo's iron ribs rise through the soot."

    cora_inner "The Savoy waits — employment, mask, material."
    cora_inner "Holywell waits — payment, risk, the author I pretend I am destined to become."
    cora_inner "Very well. Let it try."

    # [STATE] Handoff to Day 101 Morning
    $ time_manager.set_current_day(1)
    $ set_time_period("Morning")

    jump day101_main
