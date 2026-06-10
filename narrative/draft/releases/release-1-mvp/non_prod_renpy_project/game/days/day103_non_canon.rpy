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

# day103_non_canon.rpy
# Release 1 / Day 03 non-canon Ren'Py-shaped draft
# Erotic and dramatic heightening at Spice Level 3.5 (Dramatic Middle Ground + Restrained Heat).
# Verified and synchronized with baseline variable structure and runtime APIs.

# ==========================================
# DAY 3 NODE MAP
# ==========================================
# day103_morning (entry gate)
#   -> 031 - servants corridor am reflection
#   -> 031 - corridor-insp-chain
#   -> 031 - corridor-corr-chain
#   -> 031 - optional-character-chain
#   -> 032 - suite-gideon-tea (summons)
#   -> 032 - suite-cora-vs-gideon (brush test)
#   -> 032 - suite-gideon-beat (keyhole order)
#   -> 033 - bedroom-cora-frantic-writing-event
#   -> 034 - room-stern-suspicion
#   -> 032 - suite-night-tea (9 PM summons)
#   -> 033 - bedroom-final-write (manuscript retelling minigame)
#   -> day104_1 (handoff)


# ==========================================
# 030 - ENTRY DEADLINE GATE
# ==========================================

# [DAG_NODE id=day103 type=time_period day=103 period=Morning]
label day103:

    # [STATE] State/progression update
    jump day103_morning


# [DAG_NODE id=day103_morning type=time_period day=103 period=Morning]
label day103_morning:
    
    # [STATE] Check writing deadline progress
    if story.manuscript_progress == 0:

        # [STATE] State/progression update
        jump game_over_deadline_1

    # [STATE] TimeManager initializations
    $ time_manager.set_current_day(3)
    $ set_time_period("Morning")

    call day103_morning_consequence_window

    # [STATE] State/progression update
    jump day103_1_servants_corridor


# [DAG_NODE id=day103_morning_consequence_window type=dynamic_window day=103 period=Morning window=consequence penance=true returns_to=day103_morning]
label day103_morning_consequence_window:
    # Watch-only: penance consumes the morning story-chain window
    call watch_suspicion
    return


# ==========================================
# 031 - CONTEXTUAL GRIND / CORRIDOR ENTRY
# ==========================================

# [DAG_NODE id=day103_1_servants_corridor type=work day=103]
label day103_1_servants_corridor:

    # [ASSET] Existing Day 3 servants' corridor morning background
    scene bg_servants_corridor_morning
    with fade

    "The bell rings before the sky has decided whether it means to become morning."
    cora_inner "My body rises before my mind agrees."
    cora_inner "That is service, then: obedience practiced until it looks like instinct."

    cora_inner "Yesterday has not ended."
    cora_inner "It has merely put on a clean apron."

    # [BEAT] Consequence texture from Day 2 tea choice
    if story.day2_tea_choice == "predator":

        "The hotel has found unpleasant work for me with suspicious efficiency."
        "Crystal shattered in the Master Suite overnight. I spend the first hours on my knees, picking bright teeth from the rug."
        "Vance did not accuse me aloud."
        "She did not need to."

        # [STATE] State/progression update
        $ apply_effects(vance_susp=10, insp=0, corr=0)

    elif story.day2_tea_choice == "prey":

        "Stern performs a surprise inspection of the servants' quarters."
        "Drawers opened. Footlockers searched. Bedding turned back like bodies."

        if story.day2_contraband_state == "stolen_wearing":
            "The stolen lace is still beneath my uniform."
            "Stern's hands pass within inches of condemning me and find only folded cotton."
            "I survive by the width of cloth."
        else:
            "My belongings are too sparse to betray me."
            "Stern finds nothing and resents the failure."

        # [STATE] State/progression update
        $ apply_effects(stern_susp=15, insp=0, corr=0)

    else:

        "Missy does not speak to me."
        "Not in the laundry. Not by the stair. Not when Stern sets us both to six hours of brass and silence."
        cora_inner "Betrayal, I learn, is noisy only in plays. In life it polishes banisters until its wrists ache."

        # [STATE] State/progression update
        $ apply_effects(missy_susp=5, insp=10, corr=0)

    cora_inner "By late morning, the corridor outside the guest wing feels less like architecture and more like a decision waiting to happen."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day103_1_servants_corridor_menu_1]
    menu:
        "Which discipline keeps my hands steady?"

        "Order. Safety in structure. [[Inspiration]]":

            # [STATE] State/progression update
            jump day103_1_corridor_insp_chain

        "Exposure. Safety in knowing the threat. [[Corruption]]":

            # [STATE] State/progression update
            jump day103_1_corridor_corr_chain


# ==========================================
# 031 - CORRIDOR INSPIRATION CHAIN
# ==========================================

# [DAG_NODE id=day103_1_corridor_insp_chain type=work day=103]
label day103_1_corridor_insp_chain:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_morning
    with dissolve

    # [STATE] Cora chooses craft as stabiliser
    $ story.set_day3_corridor_chain("inspiration")
    $ apply_effects(stern_susp=-5, insp=15, corr=0)

    cora_inner "I count what can be counted."
    "The bell-pull rhythm. The servant stair's turn. The distance between Stern's office and the Master Suite."
    cora_inner "A hotel is not a building. It is a machine for sorting bodies by permission."

    "Guests move through carpet and light."
    "Servants move through steam and corners."
    "Men like Mr. Locke move through both and call the passage natural."

    cora_inner "That is the sentence I keep."
    cora_inner "That is the one worth risking ink for."

    "A footman passes with a tea tray and nods toward the upper corridor."
    "Mr. Locke has requested tea."
    "Not from the kitchen."
    "From me."

    # [STATE] State/progression update
    call day103_1_optional_character_chain

    # [STATE] State/progression update
    jump day103_afternoon


# ==========================================
# 031 - CORRIDOR CORRUPTION CHAIN
# ==========================================

# [DAG_NODE id=day103_1_corridor_corr_chain type=work day=103]
label day103_1_corridor_corr_chain:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_morning
    with dissolve

    # [STATE] Cora chooses appetite as stabiliser
    $ story.set_day3_corridor_chain("corruption")
    $ apply_effects(vance_susp=10, insp=0, corr=15)

    cora_inner "I should keep away from the guest wing."
    cora_inner "Instead, I find errands."
    "A towel that must be replaced. A coal scuttle that must be checked. A folded cloth that could be straighter if straightness mattered to anyone but me."

    cora_inner "The truth is uglier: I want the door to open."
    cora_inner "I want the room to notice me again."
    cora_inner "I want to know whether his silence yesterday was mercy, amusement, or appetite sharpened into manners."

    if story.day2_contraband_state == "stolen_wearing":
        cora_inner "The stolen lace is no longer new against my skin."
        cora_inner "That makes it worse."
        cora_inner "A sin repeated starts pretending to be clothing."

    "A footman appears at the bend of the corridor."

    "He does not quite meet my eyes."
    "That is how I know the order has travelled through more than one mouth."

    "Mr. Locke requests tea."
    "And he has asked that I bring it."

    # [STATE] State/progression update
    call day103_1_optional_character_chain

    # [STATE] State/progression update
    jump day103_afternoon


# ==========================================
# 031 - OPTIONAL CHARACTER CHAIN (DAY 3 MORNING)
# ==========================================

# [DAG_NODE id=day103_1_optional_character_chain type=dynamic_window day=103 period=Morning window=story_chain returns_to=day103_morning]
label day103_1_optional_character_chain:

    call story_window_penance_gate("day103_morning")
    if _penance_consumed:
        return

    # [CHOICE] Contextual grind gate after corridor reflection; resolver picks chain beat
    # [DAG_CHOICE group=day103_1_optional_character_chain_menu_1]
    menu:
        "The corridor is still deciding what kind of morning this will be."

        "Follow Stern's discipline before the guest wing wakes." if story.chain_available("stern"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("stern")
            call expression _chain_label

        "Find Missy while the house is still bruised from yesterday." if story.chain_available("missy"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("missy")
            call expression _chain_label

        "Watch the Locke Suite door before the tea order becomes a summons." if story.chain_available("vance"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("vance")
            call expression _chain_label

        "Keep moving with the cart and give no one a reason.":
            if story.day3_corridor_chain == "corruption":
                cora_inner "Exposure promised safety."
                cora_inner "Silence is cheaper until luncheon."
            else:
                cora_inner "Structure will not save me from Mr. Locke."
                cora_inner "It may keep my hands steady long enough to serve him tea without trembling."
            "I let the corridor pass without choosing a shadow."

            # [STATE] State/progression update
            $ apply_effects(insp=10, corr=0)

    return


# ==========================================
# 032 - SUITE: GIDEON TEA
# ==========================================

# [DAG_NODE id=day103_afternoon type=time_period day=103 period=Afternoon]
label day103_afternoon:

    # [STATE] State/progression update
    jump day103_2_suite_gideon_tea


# [DAG_NODE id=day103_2_suite_gideon_tea type=work day=103 period=Afternoon]
label day103_2_suite_gideon_tea:

    # [STATE] TimeManager transition to Afternoon
    $ set_time_period("Afternoon")

    # [ASSET] Existing Day 3 Master Suite day background
    scene bg_master_suite_day
    with fade

    show gideon_sprite neutral at right
    show vance_sprite submissive at left

    "The Master Suite receives me with the politeness of a trap."
    "Vance sits at the vanity. Her hands are folded in her lap, but the pale curve of her shoulders trembles slightly as the heavy aroma of warm silk and French powder rises between us."
    "Mr. Locke stands behind her, not touching her, which somehow makes the whole room more aware of his hands."

    gideon "You."

    # [ASSET] Visual/staging command
    show vance_sprite kneeling_cowed_dressing_gown at centre_full_body:
        zoom 0.75
        ypos 1.1

    # [ASSET] Visual/staging command
    with move # [asset keep]
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show vance_sprite kneeling_cowed_dressing_gown at centre_bust with move # [asset auto]
    show gideon_sprite neutral at right_bust with move # [asset auto]
    cora "Sir."

    "I set the tea tray down."
    "The cups make a small sound against the table. Too loud, sharp in the afternoon quiet."

    gideon "Ms. Vance's maid is indisposed. You will assist her."

    vance "That is not necessary."

    gideon "It is not a negotiation."

    "Vance goes quiet."
    "Not defeated. Not exactly."
    "Contained, her chest rising and falling beneath the fine lace of her collar."

    "Mr. Locke lifts a silver-backed brush from the vanity and offers it to me, his fingers lingering briefly near mine as he releases it."

    gideon "Her hair. Carefully."

    "The mirror catches all three of us."
    "Vance seated. Mr. Locke standing. Me behind her with a servant's hands and a writer's eyes mapping out the hot, silent geometry of the dressing room."

    # [STATE] State/progression update
    jump day103_2_suite_cora_vs_gideon


# ==========================================
# 032 - SUITE: CORA VS GIDEON
# ==========================================

# [DAG_NODE id=day103_2_suite_cora_vs_gideon type=work day=103]
label day103_2_suite_cora_vs_gideon:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite neutral at right
    show vance_sprite submissive at left

    "I draw the brush through Vance's hair."
    "It is heavier than it looks. Softer than she is, sliding through my fingertips like warm copper wire."

    gideon "Tell me. Do you find Ms. Vance beautiful?"

    "The brush pauses for less than a second."
    "Still enough for him to notice, his dark eyes meeting mine in the vanity glass."

    vance "Gideon."

    gideon "I asked the girl."

    "The room tightens around the question, heavy and thick with a sudden, physical charge."
    cora_inner "He has not summoned me for tea."
    cora_inner "He has summoned me for position."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day103_2_suite_cora_vs_gideon_menu_1]
    menu:
        "How do I answer the test?"

        "Answer like a craftsman. Describe what is visible, not what is wanted. [[Inspiration]]":

            # [STATE] State/progression update
            jump day103_2_cora_vs_gideon_insp

        "Let him see that I understand the charge in the room. [[Corruption]]":

            # [STATE] State/progression update
            jump day103_2_cora_vs_gideon_corr

        "Retreat into the maid's mask. Drop the brush. [[Suspicion + Inspiration]]":

            # [STATE] State/progression update
            jump day103_2_cora_vs_gideon_ghost


# ==========================================
# 032 - TEST BRANCH: INSPIRATION
# ==========================================

# [DAG_NODE id=day103_2_cora_vs_gideon_insp type=work day=103]
label day103_2_cora_vs_gideon_insp:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite neutral at right
    show vance_sprite submissive at left

    # [STATE] Predator/accomplice angle, but framed through craft rather than cartoon cruelty
    $ story.set_day3_brush_choice("predator")
    $ apply_effects(vance_susp=0, insp=20, corr=5)

    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show vance_sprite submissive at centre_bust with move # [asset auto]
    show gideon_sprite neutral at right_bust with move # [asset auto]
    cora "Yes, Sir."

    gideon "That is not an answer."

    cora "Her face holds anger better than softness. It gives the bones more purpose."

    "Vance inhales, her throat flushing a deep pink under the glass."
    "The brush keeps moving, rhythmic, precise."

    gideon "And her weakness?"

    cora "She lets other people see when they have wounded her."

    "The sentence leaves my mouth dressed as observation."
    "It lands as cruelty."

    vance "You insolent—"

    gideon "No."

    "Vance stops, her chest heaving as she clutches the vanity edge."

    gideon "She answered well."

    "In the mirror, his eyes lock onto mine with a cold, sharp interest."
    "Approval should not feel like a hand at the back of the neck, warm and heavy."

    # [STATE] State/progression update
    jump day103_2_suite_gideon_beat


# ==========================================
# 032 - TEST BRANCH: CORRUPTION
# ==========================================

# [DAG_NODE id=day103_2_cora_vs_gideon_corr type=work day=103]
label day103_2_cora_vs_gideon_corr:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite neutral at right
    show vance_sprite submissive at left

    # [STATE] Prey/deviant angle. Cora lets desire show and becomes visible
    $ story.set_day3_brush_choice("prey")
    $ apply_effects(vance_susp=5, insp=5, corr=20)

    "I look up into the mirror."
    "Not at Vance."
    "At him."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show vance_sprite submissive at centre_bust with move # [asset auto]
    show gideon_sprite neutral at right_bust with move # [asset auto]
    cora "Yes, Sir."

    gideon "Why?"

    "The question is too close to the thing beneath the thing, the physical weight in the air."

    cora "Because she is trying not to feel what everyone in the room can see."

    "Vance goes completely rigid beneath the brush, her red hair pooling over my knuckles."

    gideon "And what can everyone see?"

    "My face warms, the heat spreading under the collar of my uniform."
    "I let it."

    cora "That she has been corrected."

    "The word stays in the mirror between us, heavy, silent, and thick with implication."

    gideon "Corrected."

    "He tastes it, then smiles without showing his teeth, his gaze dropping slowly to my hands."

    gideon "A precise servant is a rare thing."

    "I have shown too much."
    "Worse: he knows I meant to, and he enjoys the transgression."

    # [STATE] State/progression update
    jump day103_2_suite_gideon_beat


# ==========================================
# 032 - TEST BRANCH: GHOST
# ==========================================

# [DAG_NODE id=day103_2_cora_vs_gideon_ghost type=work day=103]
label day103_2_cora_vs_gideon_ghost:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite neutral at right
    show vance_sprite submissive at left

    # [STATE] Ghost/mouse angle. Apparent panic, but Cora still records the scene
    $ story.set_day3_brush_choice("ghost")
    $ apply_effects(vance_susp=15, insp=15, corr=0)

    "The brush catches in a knot."
    "Vance flinches."
    "His eyes lift to the mirror, sharp and commanding."

    gideon "Carefully, I said."

    "My fingers fail me on command."
    "The brush slips and strikes the floor with a bright, silver crack."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show vance_sprite submissive at centre_bust with move # [asset auto]
    show gideon_sprite neutral at right_bust with move # [asset auto]
    cora "Forgive me, Sir."

    "I drop immediately to retrieve it, my uniform skirt catching against the leather of Gideon's boots."
    "A terrified maid. Nothing more."
    "From the floor, I see the room differently, the proximity making my breath shallow: Vance's clenched slipper, Mr. Locke's polished boot inches from my knee, the hem of my own uniform trembling."

    gideon "Clumsy."

    cora "Yes, Sir."

    "Let him have the word."
    "I take the angle and store the details."

    # [STATE] State/progression update
    jump day103_2_suite_gideon_beat


# ==========================================
# 032 - SUITE: GIDEON BEAT
# ==========================================

# [DAG_NODE id=day103_2_suite_gideon_beat type=work day=103]
label day103_2_suite_gideon_beat:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center
    show vance_sprite submissive at left

    "Vance is dismissed behind the dressing screen before the brushing is properly finished."
    "She goes because he expects her to go, her silk rustling in the dark corner."
    "The screen closes with a sound softer than a door and somehow less merciful."

    "I reach for the tea tray."
    "Mr. Locke steps into my path, his chest almost touching mine."

    gideon "No. Leave it."

    "He is close enough now that I can see the faint mark where his collar presses his throat. I can smell his tobacco and clean linen."
    "Human, then."
    "Inconvenient."

    gideon "You observe too much."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show vance_sprite submissive at centre_bust with move # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "I try to be useful, Sir."

    gideon "Useful girls do not stare through keyholes."

    cora_inner "There it is."
    cora_inner "Not accusation. Confirmation."

    if story.day1_corridor_state == "prey":
        "My stomach drops. Yesterday's floorboard. His eyes at the door. Not nearly. Not almost. He knew."
    elif story.day1_corridor_state == "predator":
        "Missy opened the door. I stood back. It did not matter. Mr. Locke is the sort of man who notices the person who benefits."
    else:
        "I walked away. I did. But perhaps listening leaves a shape of its own, a silent tension."

    gideon "You also lie better than your references suggest."

    cora "Sir?"

    gideon "Do not spoil this by pretending stupidity."

    cora_inner "The words should frighten me."
    cora_inner "They do. My heart hammer-strokes against my ribs."
    cora_inner "They also unlock something warm."

    gideon "Tonight. Nine o'clock. You will bring tea. Alone."

    cora "Miss Stern assigns the evening duties, Sir."

    "The rebellion is microscopic, a small intake of breath."
    "His attention sharpens anyway, his dark eyes narrowing with intense amusement."

    gideon "Then Miss Stern will have assigned correctly."

    "He opens the door behind me."
    "Dismissal. Invitation. Threat."
    "All the same movement."

    gideon "Go."

    # [STATE] State/progression update
    jump day103_3_bedroom_cora_frantic_writing_event


# ==========================================
# 033 - BEDROOM: CORA FRANTIC WRITING EVENT
# ==========================================

# [DAG_NODE id=day103_evening type=time_period day=103 period=Evening]
label day103_evening:

    # [STATE] State/progression update
    jump day103_3_bedroom_cora_frantic_writing_event


# [DAG_NODE id=day103_evening_consequence_window type=dynamic_window day=103 period=Evening window=consequence penance=true returns_to=day103_evening]
label day103_evening_consequence_window:
    call watch_suspicion
    call consume_pending_penance("day103_evening")
    return


# [DAG_NODE id=day103_3_bedroom_cora_frantic_writing_event type=write day=103 period=Evening]
label day103_3_bedroom_cora_frantic_writing_event:
    # [STATE] TimeManager transition to Evening
    $ set_time_period("Evening")

    call day103_evening_consequence_window

    # [ASSET] Existing servants' quarters dusk background
    scene bg_servants_quarters_dusk
    with fade

    "I make it back to my room without dropping the tray."
    "I do not remember the corridor. I remember only his voice, low and physical."
    "I remember his sentence."

    "Do not spoil this by pretending stupidity."

    cora_inner "The words crawl under the door with me."

    # [STATE] State/progression update
    $ show_ledger_ui()

    cora_inner "I have less than an hour before nine."
    cora_inner "Enough time to prepare."
    cora_inner "Enough time to write."
    cora_inner "Not enough time to be sane about either."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day103_3_bedroom_cora_frantic_writing_event_menu_1]
    menu:
        "Write with whatever time is left. [[Frantic Write]]":

            # [STATE] State/progression update
            jump day103_3_frantic_write

        "Prepare my uniform and mask. [[Prepare Mask]]":

            # [STATE] State/progression update
            jump day103_3_prepare_mask

        "Re-read the dangerous words. [[Indulge Words]]":

            # [STATE] State/progression update
            jump day103_3_indulge_words


# ==========================================
# 033 - FRANTIC WRITE
# ==========================================

# [DAG_NODE id=day103_3_frantic_write type=write]
label day103_3_frantic_write:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    $ story.set_day3_twilight_action("frantic_write")
    $ apply_effects(stern_susp=10, insp=20, corr=0)

    "I light the candle too early and waste wax with both hands."
    "No time for neatness. No time for the ledger's polite categories."
    "I write as if the door is already opening."

    if story.day3_brush_choice == "predator":
        "A maid stands behind a lady with a brush in her hand and discovers that service can be a weapon if the room is arranged correctly."
    elif story.day3_brush_choice == "prey":
        "A maid looks into a mirror and lets the dangerous man see the exact place where fear becomes want."
    else:
        "A maid drops a silver brush and learns that the floor has its own witness box."

    "The sentences are too fast, too hot, too honest."
    "Good."
    "There will be time to make them respectable later."

    # [STATE] State/progression update
    $ story.set_day3_frantic_pages_written(True)

    jump day103_4_room_stern_suspicion


# ==========================================
# 033 - PREPARE MASK
# ==========================================

# [DAG_NODE id=day103_3_prepare_mask type=work day=103]
label day103_3_prepare_mask:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with dissolve

    $ story.set_day3_twilight_action("prepare_mask")
    $ apply_effects(stern_susp=-20, insp=0, corr=0)

    "I force my hands into useful work."
    "Collar pressed. Cuffs scrubbed. Apron inspected for ink, ash, and evidence of having a mind."

    "A perfect uniform is a kind of locked door."
    "Stern trusts what looks maintained."
    "Men trust what looks available."
    "Both are wrong often enough to be useful."

    if story.day2_contraband_state == "stolen_wearing":
        "I consider removing the stolen lace."
        "I do not."
        "The uniform lies better with a secret under it, warm against my ribs."

    # [STATE] State/progression update
    jump day103_4_room_stern_suspicion


# ==========================================
# 033 - INDULGE WORDS
# ==========================================

# [DAG_NODE id=day103_3_indulge_words type=work day=103]
label day103_3_indulge_words:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with dissolve

    $ story.set_day3_twilight_action("indulge_words")
    $ apply_effects(stern_susp=5, insp=5, corr=20)

    cora_inner "I do not write the chapter."
    cora_inner "I write only what he said."

    "You observe too much."
    "You lie better than your references suggest."
    "Do not spoil this by pretending stupidity."

    "Each sentence is a hook."
    "I hang myself on them willingly, feeling the slow, physical heat they stir."

    "This is not craft yet."
    "It is the thing before craft."
    "The private damage that later pretends it was research all along."

    # [STATE] State/progression update
    jump day103_4_room_stern_suspicion


# ==========================================
# 034 - ROOM: STERN SUSPICION
# ==========================================

# [DAG_NODE id=day103_4_room_stern_suspicion type=work day=103]
label day103_4_room_stern_suspicion:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with fade

    cora_inner "A knock comes at my door."
    cora_inner "Not Mr. Locke's."
    cora_inner "Worse."

    # [ASSET] Visual/staging command
    show stern_sprite stern at center

    stern "Open."

    "I open."

    stern "You have been called upstairs this evening."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show stern_sprite stern at right_bust with move # [asset auto]
    cora "Yes, Ma'am."

    stern "Do you know why?"

    "A trap with no clever answer."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day103_4_room_stern_suspicion_menu_1]
    menu:
        "How do I answer Stern?"

        "Be boring. Make the summons sound like ordinary service. [[-Suspicion]]":

            # [STATE] State/progression update
            $ story.set_day3_stern_response("boring")
            $ apply_effects(stern_susp=-10, insp=0, corr=0)

            cora "Mr. Locke requested tea, Ma'am. I assumed the kitchen was short-handed."

            stern "You assumed."

            cora "Poorly, Ma'am. I should have asked you first."

            "Stern studies the apology for hooks."
            "Finding none, she dislikes it."

            stern "You will carry the tray, set it down, and return immediately. No conversation. No wandering. No delay."

            cora "Yes, Ma'am."

        "Tell a partial truth. Admit he unsettles me. [[+Inspiration, mixed risk]]":

            # [STATE] State/progression update
            $ story.set_day3_stern_response("partial_truth")
            $ apply_effects(stern_susp=5, insp=10, corr=0)

            cora "I don't know, Ma'am. He asks questions in a way that makes answers feel unsafe."

            "Stern's face changes by almost nothing."
            "Almost nothing is not nothing."

            stern "Then remember that silence is also an answer. Often the better one."

            "Advice. Warning. Confession."
            "Stern packages all three as discipline."

            stern "You will return directly after delivering the tray. If you are delayed, I will know."

            cora "Yes, Ma'am."

        "Play stupid. Make her underestimate me. [[+Suspicion if she sees through it]]":

            # [STATE] State/progression update
            $ story.set_day3_stern_response("stupid")
            $ apply_effects(stern_susp=10, insp=0, corr=5)

            cora "I thought gentlemen often wanted tea, Ma'am."

            "The stupidity hangs there, shiny and false."

            stern "Do not insult me with innocence you cannot afford."

            "My stomach tightens."

            stern "You are new, not empty. Learn the difference before someone else teaches it cruelly."

            cora "Yes, Ma'am."

    stern "And Cora."

    cora "Ma'am?"

    stern "A guest's attention is not a promotion."

    # [ASSET] Visual/staging command
    hide stern_sprite

    "She leaves before I can answer."
    cora_inner "Which is mercy, because I had none."

    # [STATE] State/progression update
    jump day103_2_suite_night_tea


# ==========================================
# 032 CONTINUATION - NIGHT TEA / ULTIMATUM PAYOFF
# ==========================================

# [DAG_NODE id=day103_night type=time_period day=103 period=Night]
label day103_night:

    # [STATE] State/progression update
    jump day103_2_suite_night_tea


# [DAG_NODE id=day103_night_consequence_window type=dynamic_window day=103 period=Night window=consequence penance=true returns_to=day103_night]
label day103_night_consequence_window:
    call watch_suspicion
    call consume_pending_penance("day103_night")
    return


# [DAG_NODE id=day103_2_suite_night_tea type=work day=103 period=Night]
label day103_2_suite_night_tea:

    # [STATE] TimeManager transition to Night
    $ set_time_period("Night")

    # [ASSET] Existing Day 3 Master Suite night background
    scene bg_master_suite_night
    with fade

    cora_inner "At nine, I carry tea through a hotel that has gone quiet enough to hear itself lying."
    cora_inner "The tray is heavier than it should be."
    cora_inner "That is because it contains a choice."

    # [ASSET] Visual/staging command
    show gideon_sprite dominant at center

    gideon "You came."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "I was instructed to bring tea, Sir."

    gideon "By whom?"

    "A smile without warmth."
    "He knows exactly what he is asking."

    cora "By the needs of the house."

    "He laughs once."
    "Quietly."
    "It is worse than approval, sending a small spike of heat down my spine."

    gideon "Set it down."

    "I do."
    "He does not drink. He circles the table slowly, his cuffs clicking, his collar undone to expose the strong, pale column of his neck."

    gideon "You write."

    "The room falls out from under me, leaving only the sound of my shallow breathing."

    cora "Sir?"

    gideon "Again. Do not spoil this."

    "My hands remain at my sides."
    "I am proud of that, in the distant way one might admire a burning building for standing upright under pressure."

    if story.day3_twilight_action == "frantic_write":
        "The fresh pages are hidden beneath my ledger downstairs."
        "The ink may still be wet."
    else:
        "The unwritten pages accuse me from my room."
        "Somehow that feels no safer."

    gideon "A servant who watches is irritating. A servant who records is dangerous."

    cora "I record nothing of consequence."

    gideon "Then you are wasting both ink and opportunity."

    cora_inner "There is no clean category for this."
    cora_inner "Not threat. Not flirtation. Not patronage."
    cora_inner "A man with power has discovered a locked cabinet and is deciding whether to force it open or purchase the key, his physical presence crowding the small space between us."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day103_2_suite_night_tea_menu_1]
    menu:
        "How do I survive Gideon's knowledge?"

        "Deny him access. Keep the book mine. [[Defiance]]":

            # [STATE] State/progression update
            jump day103_2_night_defy_gideon

        "Offer him a controlled fragment. Make curiosity serve me. [[Bargain]]":

            # [STATE] State/progression update
            jump day103_2_night_bargain_gideon

        "Let him frighten me. Gather every detail. [[Surrender]]":

            # [STATE] State/progression update
            jump day103_2_night_surrender_gideon


# ==========================================
# NIGHT TEA - DEFY GIDEON
# ==========================================

# [DAG_NODE id=day103_2_night_defy_gideon type=work day=103]
label day103_2_night_defy_gideon:

    # [ASSET] Visual/staging command
    scene bg_master_suite_night
    with dissolve

    show gideon_sprite dominant at center

    $ story.set_day3_ultimatum("defied")
    $ apply_effects(vance_susp=20, insp=20, corr=0)

    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "My writing is not part of my service, Sir."

    "There."
    "A sentence that can get me dismissed."
    "Or worse, retained."

    gideon "Everything in this house becomes service if a guest is sufficiently interested."

    cora "Then the house is mistaken."

    "Silence."
    "Not empty silence. Selected silence. The kind a man uses when deciding how much force a door requires."

    gideon "You are either brave or poorly educated in consequences."

    cora "I expect those often look similar from above, Sir."

    "His face changes."
    "Only slightly."
    "Enough, his eyes flashing with a sudden, dark appreciation."

    gideon "Go. Before you become less amusing."

    "I leave with the tray untouched."
    "My knees nearly fail in the corridor, trembling violently."
    "They wait until he cannot see."

    # [STATE] State/progression update
    jump day103_3_bedroom_final_write


# ==========================================
# NIGHT TEA - BARGAIN GIDEON
# ==========================================

# [DAG_NODE id=day103_2_night_bargain_gideon type=work day=103]
label day103_2_night_bargain_gideon:

    # [ASSET] Visual/staging command
    scene bg_master_suite_night
    with dissolve

    show gideon_sprite dominant at center

    $ story.set_day3_ultimatum("bargained")
    $ apply_effects(vance_susp=10, insp=15, corr=10)

    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "A fragment, perhaps. If it keeps you from imagining worse."

    gideon "You negotiate quickly."

    cora "Servants learn prices, Sir. Usually by paying them."

    "That earns a pause, his fingers tapping the silver tray."

    gideon "Recite it."

    "So I give him three sentences."
    "Not the true ones."
    "Not the safest ones either."

    cora "A house teaches silence as if silence were virtue. But silence is only obedience with its throat cut. A girl who listens long enough may mistake the wound for a mouth."

    "Mr. Locke watches me through all of it, his eyes fixed on my lips."

    gideon "You are wasted below stairs."

    cora "Many things are, Sir."

    "The answer comes too fast."
    "He notices, his breathing slowing."

    gideon "Careful. I enjoy cleverness most when it knows it is trapped."

    "I lower my eyes."
    "Not in surrender."
    "In bookkeeping."

    gideon "Go. Bring better tea tomorrow."

    "Tomorrow."
    "So the door has not closed."
    "It has learned my name."

    # [STATE] State/progression update
    jump day103_3_bedroom_final_write


# ==========================================
# NIGHT TEA - SURRENDER GIDEON
# ==========================================

# [DAG_NODE id=day103_2_night_surrender_gideon type=work day=103]
label day103_2_night_surrender_gideon:

    # [ASSET] Visual/staging command
    scene bg_master_suite_night
    with dissolve

    show gideon_sprite dominant at center

    $ story.set_day3_ultimatum("surrendered")
    $ apply_effects(vance_susp=15, insp=10, corr=25)

    "I could deny him."
    "I could lie better."
    "Instead, I let the fear and the heavy physical heat show."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "What do you want from me, Sir?"

    gideon "That is the first honest question you have asked."

    "He circles the tea table slowly, closing the distance until I can feel the warmth of his chest."
    "No touch."
    "No raised voice."
    "Only proximity, which rich men use as if space itself were another servant to be manipulated."

    gideon "I want to know whether you are merely curious, or whether you have the discipline to become dangerous."

    cora "And if I don't?"

    gideon "Then you will make an instructive failure."

    "The words should close something in me."
    "They open it instead, a delicious tremor running down my spine."

    gideon "Go. Write whatever frightened thing you are trying not to write."

    "Dismissed."
    "Not spared."
    "Sent back to my quarters sharpened, flushed, and ashamed."

    # [STATE] State/progression update
    jump day103_3_bedroom_final_write


# ==========================================
# 033 CONTINUATION - BEDROOM FINAL WRITE
# ==========================================

# [DAG_NODE id=day103_3_bedroom_final_write type=write]
label day103_3_bedroom_final_write:
    call day103_night_consequence_window

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with fade

    "I reach my room and close the door with both hands."
    "The candle is still low."
    "The page is still there."
    "So am I, apparently."

    if story.day3_ultimatum == "defied":
        "Defiance leaves a clean taste for approximately three breaths."
        "Then terror returns with its ledger open."
    elif story.day3_ultimatum == "bargained":
        "I gave him three sentences and kept the rest."
        "This feels like victory only if I ignore the fact that he now knows there is a rest."
    else:
        "He sent me back to write."
        "The command is poisonous because I wanted the same thing, my skin still tingling from his proximity."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day103_3_bedroom_final_write_menu_1]
    menu:
        "Can I turn the night into a chapter?"

        "Write until the candle dies. [[Chapter gate]]":

            # [PROMOTION NOTE]
            # Tune threshold later. Day 3 should be a major writing gate.
            if has_story_fuel(*WRITE_GATE_CH3) or story.day3_twilight_action == "frantic_write":

                "I write as if the lock is already failing, my fingers hot and quick."

                # [MANUSCRIPT PAYOFF - LEVEL 3.5]

                "The pen becomes a tool of intense reinterpretation, converting parlor constraint into raw physical heat."

                if story.day3_ultimatum == "defied":
                    "The chapter becomes a trap refused. A lord sets the snare beautifully, his fingers unhooking the lady's laces only for her to slip away into the cold, beautiful woods instead."
                elif story.day3_ultimatum == "bargained":
                    "The chapter becomes a negotiation conducted with a knife under the table. The master slides his palm over the maid's thigh to check her pulse, while every offered truth hides a hotter one behind it."
                else:
                    "The chapter becomes a summons. A girl walks toward the dark hearth and discovers that physical surrender can feel like authorship when the master's hand unbuttons her collar in the gold firelight."

                if story.day3_brush_choice == "predator":
                    "The mirror scene gives it teeth."
                    "She answered his question like a craftsman: Vance's beauty was in her bones, not her obedience, and her weakness was letting wounds show."
                    "On the page, that answer is the chapter's real edge. The maid already understood the room before the gentleman arranged it."
                elif story.day3_brush_choice == "prey":
                    "The mirror scene gives it heat and a specific peril."
                    "She looked at him when she should have looked at the lady. He saw her looking."
                    "On the page, that visibility is the chapter's fulcrum: the maid is most dangerous precisely when she is most readable, because readability assumes the reader knows what to do with her."
                else:
                    "The fallen brush gives it the angle no gentleman thinks to check."
                    "From the floor she saw the polished boot, the clenched slipper, the hem of her own uniform trembling against the carpet."
                    "On the page, the maid's clumsiness is her method. The view from below has its own authority and he never looked down long enough to claim it."

                # [STATE] State/progression update
                $ story.complete_manuscript_chapter("day3_chapter")
                call book1_write_chapter(chapter_key="day3_chapter", current_day=103)

                # [STATE] State/progression update
                $ apply_effects(stern_susp=5, insp=-20, corr=0)

                "Chapter Three is complete."
                "I do not feel safer."
                "I feel more legible, exposed on my own pages."

            else:

                "I try."
                "That is the most humiliating phrase in the English language."

                "The pen moves, stops, scratches, fails."
                "The material is too close. Mr. Locke is too close. My own want is too close behind him."

                "No chapter comes."
                "Only fragments, warm and useless."

                # [STATE] State/progression update
                $ story.set_day3_failed_write(True)
                $ apply_effects(stern_susp=0, insp=5, corr=5)

        "Do not write. Barricade the door and wait for morning. [[Safety over progress]]":

            # [STATE] State/progression update
            $ story.set_day3_night_action("barricade")
            $ apply_effects(stern_susp=10, insp=0, corr=0)

            "I push the washstand against the door."
            "It is not heavy enough to stop a determined man."
            "It is heavy enough to let me pretend there is a difference between fear and strategy."

            "At half past nine, footsteps pause outside."
            "The handle does not move."
            "That is worse, somehow, the silent proximity humming through the wood."

            "In the morning, the page is still blank."
            "But so is the doorway."

    # [STATE] State/progression update
    $ resolve_turn()
    jump day104_1


# ==========================================
# HANDOFF STUB
# ==========================================

# [DAG_NODE id=day104_1 type=work day=104]
label day104_1:

    # [STATE] State/progression update
    jump day104_1_false_dawn_suite_window
