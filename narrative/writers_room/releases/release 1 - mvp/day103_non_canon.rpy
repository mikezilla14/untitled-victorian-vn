# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes

# day103_non_canon.rpy
# Release 1 / Day 03 non-canon Ren'Py-shaped draft
# Source intent: rewritten from Twine node map and existing Day 3 script.
# Asset constraint: uses only assets already present in the supplied Day 3 Ren'Py draft.
# Promotion note: delete the temporary day103_morning stub from day102_non_canon.rpy when this file is promoted.
# Promotion note: replace story/player helper calls with exact runtime method names during implementation.

# ==========================================
# DAY 3 NODE MAP
# ==========================================
# 031
#   -> 031-corridor-insp-chain
#   -> 031-corridor-corr-chain
#   -> 032-suite-gideon-tea
#   -> 032-suite-cora-vs-gideon
#   -> 032-suite-gideon-beat
#   -> 033-bedroom-cora-frantic-writing-event
#   -> 034-room-stern-suspicion
#   -> day104_1


# ==========================================
# 031 - CONTEXTUAL GRIND / CORRIDOR ENTRY
# ==========================================

label day103_1_servants_corridor:
    call check_confrontations

    # [ASSET] Existing Day 3 servants' corridor morning background
    scene bg_servants_corridor_morning
    with fade

    "The bell rings before the sky has decided whether it means to become morning."
    "My body rises before my mind agrees."
    "That is service, then: obedience practiced until it looks like instinct."

    "Yesterday has not ended."
    "It has merely put on a clean apron."

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
        "Betrayal, I learn, is noisy only in plays. In life it polishes banisters until its wrists ache."

        # [STATE] State/progression update
        $ apply_effects(missy_susp=5, insp=10, corr=0)

    "By late morning, the corridor outside the guest wing feels less like architecture and more like a decision waiting to happen."

    # [CHOICE] Decision point
    menu:
        "Which discipline keeps my hands steady?"

        "Order. Safety in structure. [Inspiration]":

            # [STATE] State/progression update
            jump day103_1_corridor_insp_chain

        "Exposure. Safety in knowing the threat. [Corruption]":

            # [STATE] State/progression update
            jump day103_1_corridor_corr_chain


# ==========================================
# 031 - CORRIDOR INSPIRATION CHAIN
# ==========================================

label day103_1_corridor_insp_chain:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_morning
    with dissolve

    # [STATE] Cora chooses craft as stabiliser
    $ story.set_day3_corridor_chain("inspiration")
    $ apply_effects(susp=-5, insp=15, corr=0)

    "I count what can be counted."
    "The bell-pull rhythm. The servant stair's turn. The distance between Stern's office and the Master Suite."
    "A hotel is not a building. It is a machine for sorting bodies by permission."

    "Guests move through carpet and light."
    "Servants move through steam and corners."
    "Men like Mr. Locke move through both and call the passage natural."

    "That is the sentence I keep."
    "That is the one worth risking ink for."

    "A footman passes with a tea tray and nods toward the upper corridor."
    "Mr. Locke has requested tea."
    "Not from the kitchen."
    "From me."

    # [STATE] State/progression update
    jump day103_1_optional_character_chain


# ==========================================
# 031 - CORRIDOR CORRUPTION CHAIN
# ==========================================

label day103_1_corridor_corr_chain:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_morning
    with dissolve

    # [STATE] Cora chooses appetite as stabiliser
    $ story.set_day3_corridor_chain("corruption")
    $ apply_effects(susp=10, insp=0, corr=15)

    "I should keep away from the guest wing."
    "Instead, I find errands."
    "A towel that must be replaced. A coal scuttle that must be checked. A folded cloth that could be straighter if straightness mattered to anyone but me."

    "The truth is uglier: I want the door to open."
    "I want the room to notice me again."
    "I want to know whether his silence yesterday was mercy, amusement, or appetite sharpened into manners."

    if story.day2_contraband_state == "stolen_wearing":
        "The stolen lace is no longer new against my skin."
        "That makes it worse."
        "A sin repeated starts pretending to be clothing."

    "A footman appears at the bend of the corridor."

    "He does not quite meet my eyes."
    "That is how I know the order has travelled through more than one mouth."

    "Mr. Locke requests tea."
    "And he has asked that I bring it."

    # [STATE] State/progression update
    jump day103_1_optional_character_chain


# ==========================================
# 031 - OPTIONAL CHARACTER CHAIN (DAY 3 MORNING)
# ==========================================

label day103_1_optional_character_chain:

    # [CHOICE] Contextual grind gate after corridor reflection; resolver picks chain beat.
    menu:
        "The corridor is still deciding what kind of morning this will be."

        "Follow Stern's discipline before the guest wing wakes." if story.chain_available("stern"):
            $ _chain_label = story.resolve_chain_label("stern")
            jump expression _chain_label

        "Find Missy while the house is still bruised from yesterday." if story.chain_available("missy"):
            $ _chain_label = story.resolve_chain_label("missy")
            jump expression _chain_label

        "Watch the Locke Suite door before the tea order becomes a summons." if story.chain_available("vance"):
            $ _chain_label = story.resolve_chain_label("vance")
            jump expression _chain_label

        "Keep moving with the cart and give no one a reason.":
            if story.day3_corridor_chain == "corruption":
                "Exposure promised safety."
                "Silence is cheaper until luncheon."
            else:
                "Structure will not save me from Mr. Locke."
                "It may keep my hands steady long enough to serve him tea without trembling."
            "I let the corridor pass without choosing a shadow."

            # [STATE] State/progression update
            $ apply_effects(insp=10, corr=0)
            jump advance_after_confrontation


# ==========================================
# 032 - SUITE: GIDEON TEA
# ==========================================

label day103_2_suite_gideon_tea:

    # [ASSET] Existing Day 3 Master Suite day background
    scene bg_master_suite_day
    with fade

    show gideon_sprite neutral at right
    show vance_sprite defeated at left

    "The Master Suite receives me with the politeness of a trap."
    "Vance sits at the vanity. Her hands are folded in her lap."
    "Mr. Locke stands behind her, not touching her, which somehow makes the whole room more aware of his hands."

    gideon "You."

    cora "Sir."

    "I set the tea tray down."
    "The cups make a small sound against the table. Too loud."

    gideon "Ms. Vance's maid is indisposed. You will assist her."

    vance "That is not necessary."

    gideon "It is not a negotiation."

    "Vance goes quiet."
    "Not defeated. Not exactly."
    "Contained."

    "Mr. Locke lifts a silver-backed brush from the vanity and offers it to me."

    gideon "Her hair. Carefully."

    "The mirror catches all three of us."
    "Vance seated. Mr. Locke standing. Me behind her with a servant's hands and a writer's eyes."

    # [STATE] State/progression update
    jump day103_2_suite_cora_vs_gideon


# ==========================================
# 032 - SUITE: CORA VS GIDEON
# ==========================================

label day103_2_suite_cora_vs_gideon:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite neutral at right
    show vance_sprite defeated at left

    "I draw the brush through Vance's hair."
    "It is heavier than it looks. Softer than she is."

    gideon "Tell me. Do you find Ms. Vance beautiful?"

    "The brush pauses for less than a second."
    "Still enough for him to notice."

    vance "Gideon."

    gideon "I asked the girl."

    "The room tightens around the question."
    "He has not summoned me for tea."
    "He has summoned me for position."

    # [CHOICE] Decision point
    menu:
        "How do I answer the test?"

        "Answer like a craftsman. Describe what is visible, not what is wanted. [Inspiration]":

            # [STATE] State/progression update
            jump day103_2_cora_vs_gideon_insp

        "Let him see that I understand the charge in the room. [Corruption]":

            # [STATE] State/progression update
            jump day103_2_cora_vs_gideon_corr

        "Retreat into the maid's mask. Drop the brush. [Suspicion + Inspiration]":

            # [STATE] State/progression update
            jump day103_2_cora_vs_gideon_ghost


# ==========================================
# 032 - TEST BRANCH: INSPIRATION
# ==========================================

label day103_2_cora_vs_gideon_insp:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite neutral at right
    show vance_sprite defeated at left

    # [STATE] Predator/accomplice angle, but framed through craft rather than cartoon cruelty
    $ story.set_day3_brush_choice("predator")
    $ apply_effects(vance_susp=0, insp=20, corr=5)

    cora "Yes, Sir."

    gideon "That is not an answer."

    cora "Her face holds anger better than softness. It gives the bones more purpose."

    "Vance inhales."
    "The brush keeps moving."

    gideon "And her weakness?"

    cora "She lets other people see when they have wounded her."

    "The sentence leaves my mouth dressed as observation."
    "It lands as cruelty."

    vance "You insolent—"

    gideon "No."

    "Vance stops."

    gideon "She answered well."

    "In the mirror, his eyes meet mine."
    "Approval should not feel like a hand at the back of the neck."

    # [STATE] State/progression update
    jump day103_2_suite_gideon_beat


# ==========================================
# 032 - TEST BRANCH: CORRUPTION
# ==========================================

label day103_2_cora_vs_gideon_corr:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite neutral at right
    show vance_sprite defeated at left

    # [STATE] Prey/deviant angle. Cora lets desire show and becomes visible
    $ story.set_day3_brush_choice("prey")
    $ apply_effects(vance_susp=5, insp=5, corr=20)

    "I look up into the mirror."
    "Not at Vance."
    "At him."

    cora "Yes, Sir."

    gideon "Why?"

    "The question is too close to the thing beneath the thing."

    cora "Because she is trying not to feel what everyone in the room can see."

    "Vance goes rigid beneath the brush."

    gideon "And what can everyone see?"

    "My face warms."
    "I let it."

    cora "That she has been corrected."

    "The word stays in the mirror between us."

    gideon "Corrected."

    "He tastes it, then smiles without showing his teeth."

    gideon "A precise servant is a rare thing."

    "I have shown too much."
    "Worse: he knows I meant to."

    # [STATE] State/progression update
    jump day103_2_suite_gideon_beat


# ==========================================
# 032 - TEST BRANCH: GHOST
# ==========================================

label day103_2_cora_vs_gideon_ghost:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite neutral at right
    show vance_sprite defeated at left

    # [STATE] Ghost/mouse angle. Apparent panic, but Cora still records the scene
    $ story.set_day3_brush_choice("ghost")
    $ apply_effects(vance_susp=10, stern_susp=5, insp=15, corr=0)

    "The brush catches in a knot."
    "Vance flinches."
    "His eyes lift to the mirror."

    gideon "Carefully, I said."

    "My fingers fail me on command."
    "The brush slips and strikes the floor with a bright, silver crack."

    cora "Forgive me, Sir."

    "I drop immediately to retrieve it."
    "A terrified maid. Nothing more."
    "From the floor, I see the room differently: Vance's clenched slipper, Mr. Locke's polished boot, the hem of my own uniform trembling against my knee."

    gideon "Clumsy."

    cora "Yes, Sir."

    "Let him have the word."
    "I take the angle."

    # [STATE] State/progression update
    jump day103_2_suite_gideon_beat


# ==========================================
# 032 - SUITE: GIDEON BEAT
# ==========================================

label day103_2_suite_gideon_beat:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at center
    show vance_sprite defeated at left

    "Vance is dismissed behind the dressing screen before the brushing is properly finished."
    "She goes because he expects her to go."
    "The screen closes with a sound softer than a door and somehow less merciful."

    "I reach for the tea tray."
    "Mr. Locke steps into my path."

    gideon "No. Leave it."

    "He is close enough now that I can see the faint mark where his collar presses his throat."
    "Human, then."
    "Inconvenient."

    gideon "You observe too much."

    cora "I try to be useful, Sir."

    gideon "Useful girls do not stare through keyholes."

    "There it is."
    "Not accusation. Confirmation."

    if story.day1_corridor_state == "prey":
        "My stomach drops. Yesterday's floorboard. His eyes at the door. Not nearly. Not almost. He knew."
    elif story.day1_corridor_state == "predator":
        "Missy opened the door. I stood back. It did not matter. Mr. Locke is the sort of man who notices the person who benefits."
    else:
        "I walked away. I did. But perhaps listening leaves a shape of its own."

    gideon "You also lie better than your references suggest."

    cora "Sir?"

    gideon "Do not spoil this by pretending stupidity."

    "The words should frighten me."
    "They do."
    "They also unlock something."

    gideon "Tonight. Nine o'clock. You will bring tea. Alone."

    cora "Miss Stern assigns the evening duties, Sir."

    "The rebellion is microscopic."
    "His attention sharpens anyway."

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

label day103_3_bedroom_cora_frantic_writing_event:
    call check_confrontations

    # [ASSET] Existing servants' quarters dusk background
    scene bg_servants_quarters_dusk
    with fade

    "I make it back to my room without dropping the tray."
    "I do not remember the corridor."
    "I remember his sentence."

    "Do not spoil this by pretending stupidity."

    "The words crawl under the door with me."

    # [STATE] State/progression update
    $ show_ledger_ui()

    "I have less than an hour before nine."
    "Enough time to prepare."
    "Enough time to write."
    "Not enough time to be sane about either."

    # [CHOICE] Decision point
    menu:
        "Write with whatever time is left. [Frantic Write]":

            # [STATE] State/progression update
            jump day103_3_frantic_write

        "Prepare my uniform and mask. [Prepare Mask]":

            # [STATE] State/progression update
            jump day103_3_prepare_mask

        "Re-read the dangerous words. [Indulge Words]":

            # [STATE] State/progression update
            jump day103_3_indulge_words


# ==========================================
# 033 - FRANTIC WRITE
# ==========================================

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

    # [PROMOTION NOTE]
    # This is not automatically a full chapter. It banks progress/material toward the night decision.

    # [STATE] State/progression update
    $ story.set_day3_frantic_pages_written(True)

    jump day103_4_room_stern_suspicion


# ==========================================
# 033 - PREPARE MASK
# ==========================================

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
        "The uniform lies better with a secret under it."

    # [STATE] State/progression update
    jump day103_4_room_stern_suspicion


# ==========================================
# 033 - INDULGE WORDS
# ==========================================

label day103_3_indulge_words:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with dissolve

    $ story.set_day3_twilight_action("indulge_words")
    $ apply_effects(vance_susp=5, insp=5, corr=20)

    "I do not write the chapter."
    "I write only what he said."

    "You observe too much."
    "You lie better than your references suggest."
    "Do not spoil this by pretending stupidity."

    "Each sentence is a hook."
    "I hang myself on them willingly."

    "This is not craft yet."
    "It is the thing before craft."
    "The private damage that later pretends it was research all along."

    # [STATE] State/progression update
    jump day103_4_room_stern_suspicion


# ==========================================
# 034 - ROOM: STERN SUSPICION
# ==========================================

label day103_4_room_stern_suspicion:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with fade

    "A knock comes at my door."
    "Not Mr. Locke's."
    "Worse."

    # [ASSET] Visual/staging command
    show stern_sprite stern at center

    stern "Open."

    "I open."

    stern "You have been called upstairs this evening."

    cora "Yes, Ma'am."

    stern "Do you know why?"

    "A trap with no clever answer."

    # [CHOICE] Decision point
    menu:
        "How do I answer Stern?"

        "Be boring. Make the summons sound like ordinary service. [-Suspicion]":

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

        "Tell a partial truth. Admit he unsettles me. [+Inspiration, mixed risk]":

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

        "Play stupid. Make her underestimate me. [+Suspicion if she sees through it]":

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
    "Which is mercy, because I had none."

    # [STATE] State/progression update
    jump day103_2_suite_night_tea


# ==========================================
# 032 CONTINUATION - NIGHT TEA / ULTIMATUM PAYOFF
# ==========================================

label day103_2_suite_night_tea:

    # [ASSET] Existing Day 3 Master Suite night background
    scene bg_master_suite_night
    with fade

    "At nine, I carry tea through a hotel that has gone quiet enough to hear itself lying."
    "The tray is heavier than it should be."
    "That is because it contains a choice."

    # [ASSET] Visual/staging command
    show gideon_sprite dominant at center

    gideon "You came."

    cora "I was instructed to bring tea, Sir."

    gideon "By whom?"

    "A smile without warmth."
    "He knows exactly what he is asking."

    cora "By the needs of the house."

    "He laughs once."
    "Quietly."
    "It is worse than approval."

    gideon "Set it down."

    "I do."
    "He does not drink."

    gideon "You write."

    "The room falls out from under me."

    cora "Sir?"

    gideon "Again. Do not spoil this."

    "My hands remain at my sides."
    "I am proud of that, in the distant way one might admire a burning building for standing upright."

    if story.day3_twilight_action == "frantic_write":
        "The fresh pages are hidden beneath my ledger downstairs."
        "The ink may still be wet."
    else:
        "The unwritten pages accuse me from my room."
        "Somehow that feels no safer."

    gideon "A servant who watches is irritating. A servant who records is dangerous."

    cora "I record nothing of consequence."

    gideon "Then you are wasting both ink and opportunity."

    "There is no clean category for this."
    "Not threat. Not flirtation. Not patronage."
    "A man with power has discovered a locked cabinet and is deciding whether to force it open or purchase the key."

    # [CHOICE] Decision point
    menu:
        "How do I survive Gideon's knowledge?"

        "Deny him access. Keep the book mine. [Defiance]":

            # [STATE] State/progression update
            jump day103_2_night_defy_gideon

        "Offer him a controlled fragment. Make curiosity serve me. [Bargain]":

            # [STATE] State/progression update
            jump day103_2_night_bargain_gideon

        "Let him frighten me. Gather every detail. [Surrender]":

            # [STATE] State/progression update
            jump day103_2_night_surrender_gideon


# ==========================================
# NIGHT TEA - DEFY GIDEON
# ==========================================

label day103_2_night_defy_gideon:

    # [ASSET] Visual/staging command
    scene bg_master_suite_night
    with dissolve

    show gideon_sprite dominant at center

    $ story.set_day3_ultimatum("defied")
    $ apply_effects(susp=20, insp=20, corr=0)

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
    "Enough."

    gideon "Go. Before you become less amusing."

    "I leave with the tray untouched."
    "My knees nearly fail in the corridor."
    "They wait until he cannot see."

    # [STATE] State/progression update
    jump day103_3_bedroom_final_write


# ==========================================
# NIGHT TEA - BARGAIN GIDEON
# ==========================================

label day103_2_night_bargain_gideon:

    # [ASSET] Visual/staging command
    scene bg_master_suite_night
    with dissolve

    show gideon_sprite dominant at center

    $ story.set_day3_ultimatum("bargained")
    $ apply_effects(susp=10, insp=15, corr=10)

    cora "A fragment, perhaps. If it keeps you from imagining worse."

    gideon "You negotiate quickly."

    cora "Servants learn prices, Sir. Usually by paying them."

    "That earns a pause."

    gideon "Recite it."

    "So I give him three sentences."
    "Not the true ones."
    "Not the safest ones either."

    cora "A house teaches silence as if silence were virtue. But silence is only obedience with its throat cut. A girl who listens long enough may mistake the wound for a mouth."

    "Mr. Locke watches me through all of it."

    gideon "You are wasted below stairs."

    cora "Many things are, Sir."

    "The answer comes too fast."
    "He notices."

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

label day103_2_night_surrender_gideon:

    # [ASSET] Visual/staging command
    scene bg_master_suite_night
    with dissolve

    show gideon_sprite dominant at center

    $ story.set_day3_ultimatum("surrendered")
    $ apply_effects(susp=15, insp=10, corr=25)

    "I could deny him."
    "I could lie better."
    "Instead, I let the fear show."

    cora "What do you want from me, Sir?"

    gideon "That is the first honest question you have asked."

    "He circles the tea table slowly."
    "No touch."
    "No raised voice."
    "Only proximity, which rich men use as if space itself were another servant."

    gideon "I want to know whether you are merely curious, or whether you have the discipline to become dangerous."

    cora "And if I don't?"

    gideon "Then you will make an instructive failure."

    "The words should close something in me."
    "They open it instead."

    gideon "Go. Write whatever frightened thing you are trying not to write."

    "Dismissed."
    "Not spared."
    "Sent back sharpened and ashamed."

    # [STATE] State/progression update
    jump day103_3_bedroom_final_write


# ==========================================
# 033 CONTINUATION - BEDROOM FINAL WRITE
# ==========================================

label day103_3_bedroom_final_write:
    call check_confrontations

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
        "The command is poisonous because I wanted the same thing."

    # [CHOICE] Decision point
    menu:
        "Can I turn the night into a chapter?"

        "Write until the candle dies. [Chapter gate]":

            # [PROMOTION NOTE]
            # Tune threshold later. Day 3 should be a major writing gate.
            if player.has_story_fuel(required_total=45) or story.day3_twilight_action == "frantic_write":

                "I write as if the lock is already failing."

                if story.day3_ultimatum == "defied":
                    "The chapter becomes a trap refused. A lord sets the snare beautifully and cannot understand why the prey would choose the cold woods instead."
                elif story.day3_ultimatum == "bargained":
                    "The chapter becomes a negotiation conducted with a knife under the table. Every offered truth hides a better one behind it."
                else:
                    "The chapter becomes a summons. A girl walks toward danger and discovers that obedience can feel like authorship when the page is cruel enough."

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
                $ apply_effects(stern_susp=5, insp=-20, corr=0)

                "Chapter Three is complete."
                "I do not feel safer."
                "I feel more legible."

            else:

                "I try."
                "That is the most humiliating phrase in the English language."

                "The pen moves, stops, scratches, fails."
                "The material is too close. Mr. Locke is too close. My own want is too close behind him."

                "No chapter comes."
                "Only fragments."

                # [STATE] State/progression update
                $ story.set_day3_failed_write(True)
                $ apply_effects(stern_susp=0, insp=5, corr=5)

        "Do not write. Barricade the door and wait for morning. [Safety over progress]":

            # [STATE] State/progression update
            $ story.set_day3_night_action("barricade")
            $ apply_effects(stern_susp=10, insp=0, corr=0)

            "I push the washstand against the door."
            "It is not heavy enough to stop a determined man."
            "It is heavy enough to let me pretend there is a difference between fear and strategy."

            "At half past nine, footsteps pause outside."
            "The handle does not move."
            "That is worse, somehow."

            "In the morning, the page is still blank."
            "But so is the doorway."

    # [STATE] State/progression update
    jump day104_1


# ==========================================
# HANDOFF STUB
# ==========================================

label day104_1:

    # [STATE] State/progression update
    jump day104_1_false_dawn_suite_window
