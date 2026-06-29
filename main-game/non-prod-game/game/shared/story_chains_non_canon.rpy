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

# story_chains_non_canon.rpy
# Writers' Room - Release 1 / Dynamic Narrative Story Chains & Confrontations Draft
# Enforces character-specific suspicion thresholds, deferred penance routing, and deadlines.

# ==============================================================================
# 1. SUSPICION WATCHER & DYNAMIC WINDOW ROUTING (call/return — no spine jumps)
# ==============================================================================

# [DAG_NODE id=watch_suspicion type=penance_check]
label watch_suspicion:
    # Hard fail: consolidated anxiety breakdown
    if player.anxiety >= 100:

        # [STATE] State/progression update
        jump game_over_dismissed

    # Soft fail: queue confrontation labels for the next dynamic window to consume
    if player.is_confrontation_ready("stern"):

        # [STATE] State/progression update
        $ story.queue_penance("confrontation_stern")
    if player.is_confrontation_ready("vance"):

        # [STATE] State/progression update
        $ story.queue_penance("confrontation_vance")
    if player.is_confrontation_ready("missy"):

        # [STATE] State/progression update
        $ story.queue_penance("confrontation_missy")

    # Queue anxiety breakdown on first-time crossing of 70%
    if player.is_anxiety_ready():
        if not player.has_reached_70_before:

            # [STATE] State/progression update
            $ story.queue_penance("anxiety_breakdown_downtime")
            $ player.has_reached_70_before = True
        elif not player.anxiety_70_warning_shown:
            cora "My chest feels tight, and the air in the Savoy feels suffocatingly thin. The shadow of discovery is closing in. If I let my nerves fray any further, I will lose my grip entirely."
            sys_msg "[[WARNING: Cora's anxiety has reached 70%% again. High anxiety will restrict her choices and lead to complete writing paralysis at 85%%. Mind her nerves carefully.]]"

            # [STATE] State/progression update
            $ player.anxiety_70_warning_shown = True

    # Set warning flags and process second-time 75% warnings
    if player.anxiety >= 75:
        if not player.has_reached_75_before:

            # [STATE] State/progression update
            $ player.has_reached_75_before = True
        elif not player.anxiety_75_warning_shown:
            cora "My hands shake so much I can barely hold the pen. The threat is no longer a distant worry; it is a physical wall. I cannot risk another mistake."
            sys_msg "[[WARNING: Cora's anxiety has reached 75%% again. Her choices are locked. Reaching 85%% will cause complete writing paralysis.]]"

            # [STATE] State/progression update
            $ player.anxiety_75_warning_shown = True

    # Reset warning flags when anxiety drops back down
    if player.anxiety < 70:

        # [STATE] State/progression update
        $ player.anxiety_70_warning_shown = False
    if player.anxiety < 75:

        # [STATE] State/progression update
        $ player.anxiety_75_warning_shown = False

    return


# [DAG_NODE id=check_confrontations type=penance_check]
label check_confrontations:
    # Backward-compatible alias — prefer watch_suspicion in new code
    call watch_suspicion
    return


# [DAG_NODE id=consume_pending_penance type=penance_consume]
label consume_pending_penance(window_id):

    # [STATE] State/progression update
    $ _penance_label = story.consume_penance_at_window(window_id)
    if _penance_label:
        call expression _penance_label
    return


# [DAG_NODE id=story_window_penance_gate type=penance_consume]
label story_window_penance_gate(window_id):
    # Sacrifices the optional chain menu when penance is queued

    # Run the suspicion and anxiety check first to ensure any pending penance is queued
    call watch_suspicion

    # [STATE] State/progression update
    $ _penance_consumed = False
    if story.has_pending_penance():

        # [STATE] State/progression update
        $ _penance_label = story.consume_penance_at_window(window_id)
        if _penance_label:
            call expression _penance_label

            # [STATE] State/progression update
            $ _penance_consumed = True
    return


# [DAG_NODE id=advance_after_confrontation_deprecated type=router]
label advance_after_confrontation:
    # QUARANTINED (story-chain-routing-refactor): do not call from new code.
    $ renpy.log("DEPRECATED: advance_after_confrontation called — no-op quarantine")
    return


# ==============================================================================
# 2. DYNAMIC NARRATIVE CHAIN: MISS STERN ("The Sovereign Disciplines")
# ==============================================================================

# [DAG_NODE id=stern_chain_1 type=chain character=stern level=1]
label stern_chain_1:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning
    with fade

    show stern_sprite neutral at centre_bust

    # [BEAT] Step 1: Posture audit — who controls the body in service

    "The west wing linen closet is narrower than a confessional and smells of starch and cold lye."

    if time_manager.time_of_day == "Morning":
        "Outside, the second-floor shift is in full voice. A footman passes the door; if Miss Stern raises hers, the whole corridor will hear it."
    elif time_manager.time_of_day == "Evening":
        "The gas wall-sconces outside are already unlit. In the dim, her inspection feels less like duty and more like a private summons."
    else:
        "The late-night corridor is empty, which makes every rustle of cotton sound like evidence."

    "Miss Stern stands inside, her keys clutched in her hand like a small iron crop."
    "Her eyes move from my collar to the folded sheets, measuring the precision of my service."

    stern "Cora. The sheets for suite 402. Did you fold them with the lock-stitch hem outward, or did you simply tumble them in the country fashion?"

    # [CHOICE] Decision point
    # [DAG_CHOICE group=stern_chain_1_menu_1]
    menu:
        "Play the country fool and vanish from her ledger. [[Shed Suspicion / Close Track]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(stern_susp=-10)
            $ story.abandon_chain_beat("stern")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show stern_sprite neutral at right_bust with move # [asset auto]
            cora "Outward, Ma'am. Missy showed me. I repeated it so as not to offend."
            stern "Exactly is a large word for a small mind. Keep to that simple standard, Cora, and the Strand will remain a distant worry."

            "She dismisses me with a slight twitch of her chin."
            "I have bought safety with stupidity. The door to her private discipline stays shut."

        "Answer her geometry and let her mark my posture. [[Lean Into Tension / Advance]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="stern")
            $ story.complete_chain_beat("stern", path="safe_progress")

            cora "The outward stitch preserves the line of the silk, Ma'am. It keeps the hem from catching on the mahogany frame."

            "Miss Stern goes still."
            "Her chest rises once, her keys clicking softly in the quiet cupboard."

            stern "A girl who knows the grain of a guest's bed spends too much time looking at what does not belong to her."

            "She steps closer. The heavy scent of wool and lavender soap surrounds me."
            "She raises the cold iron ring of her keys and sets the flat metal against the side of my neck, forcing my chin upward."

            stern "Keep that chin high, Cora Vale. Do not let me find you looking down at the silk again."

            "Her touch is brief, cold, and utterly improper."
            "She has found the place on my body where discipline might later sit."

    # [ASSET] Visual/staging command
    hide stern_sprite
    return


# [DAG_NODE id=stern_chain_2 type=chain character=stern level=2]
label stern_chain_2:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with fade

    show stern_sprite neutral at centre_bust

    # [BEAT] Step 2: Knowledge extraction — notebook as confessional
    if time_manager.time_of_day == "Evening":
        "The servants' quarters are thick with grey London twilight. Anyone on the landing could hear a raised voice through the thin door."
    else:
        "A cold late-night draft rattles the windowpane. In the dark, confession sounds less like speech and more like theft."

    "I am resting on the edge of the narrow bed when the door handle jiggles. Miss Stern enters before the latch can sound."
    "I scramble to slide the cheap notebook under my apron, but her hand descends."
    "She does not snatch it. She presses her thumb onto the leather cover, pinning it against my lap."

    if story.get_character_chain_level("stern") >= 1:
        "The place on my neck where her keys rested still remembers the cold."

    stern "A ledger of kitchen weights, Cora? Or does a chambermaid believe she has thoughts worth preserving in ink?"

    # [CHOICE] Decision point
    # [DAG_CHOICE group=stern_chain_2_menu_1]
    menu:
        "Surrender the notebook as a spelling exercise. [[Shed Suspicion / Close Track]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(stern_susp=-10)
            $ story.abandon_chain_beat("stern")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show stern_sprite neutral at right_bust with move # [asset auto]
            cora "Only my letters, Ma'am. My mother said a maid who cannot spell the inventory is of no use to a fine house."
            stern "Your mother was sensible. Keep to spelling 'apron' and 'lye', Cora. Leave the long words to those who do not have to wash them."

            "She draws her hand back and leaves. The notebook survives. The story does not."

        "Read her the passage and let her feel the theft of being seen. [[Advance / Confessional Heat]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="stern")
            $ story.complete_chain_beat("stern", path="safe_progress")

            cora "I was writing about the west corridor, Ma'am."
            stern "Speak plainly, girl."
            cora "I wrote: 'The warden of the floor has a voice like iron, but her keys shake when she touches the maid's collar. She has a secret appetite for the dust she pretends to clean.'"

            "Miss Stern's keys slip from her fingers, striking the floor with a bright clatter."
            "She does not bend to retrieve them."
            "She steps forward instead, pinning me flat against the small wooden desk."
            "Her fingers slide beneath my apron and press against my corset, as if checking whether the ink has entered my blood."

            stern "You are a monstrous creature, Cora Vale. A thief who steals the thoughts of her betters."
            cora "Is it theft if it is true, Ma'am?"
            stern "If I find this notebook again, I will burn it. And then I will write a reference for you that will make the Strand look inviting."

            "Her hand remains one second longer than warning requires."
            "She leaves me with a threat that reads exactly like an invitation."

    # [ASSET] Visual/staging command
    hide stern_sprite
    return


# [DAG_NODE id=stern_chain_3 type=chain character=stern level=3]
label stern_chain_3:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with fade

    show stern_sprite neutral at centre_bust

    # [BEAT] Step 3: Public discipline vs private inspection — kneeling as spectacle risk
    if time_manager.time_of_day == "Afternoon":
        "The afternoon sun filters through the vacant suite drapes. A guest floor this bright makes every improper posture visible."
    else:
        "The evening drapes are drawn tight. Only one candle burns on the dressing table — enough light for inspection, not enough for witnesses."

    "Miss Stern stands beside the vanity. She has emptied a drawer onto the carpet: a dry rose, banker's stubs, three scraps of paper."
    "Her keys hang from her belt, clicking as she turns to study me."

    if story.get_character_chain_level("stern") >= 2:
        stern "You still write, I think. The notebook was only the first confession."

    stern "A guest leaves many things. The young maid sees them as souvenirs. I see them as evidence of character."
    stern "Tell me, Cora. What do you see?"

    # [CHOICE] Decision point
    # [DAG_CHOICE group=stern_chain_3_menu_1]
    menu:
        "Play the blind servant and let the fire die forever. [[Close Track / Lose Climax]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(stern_susp=-15)
            $ story.abandon_chain_beat("stern")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show stern_sprite neutral at right_bust with move # [asset auto]
            cora "Dust, Ma'am. And scraps that should have been swept before the second floor shift."
            stern "Correct. A drawer is a box for linens, not a confessional."

            "She nods, satisfied with my simple maid's mask."
            "I remain a ghost in her hotel — safe, starved, and never to be touched that way again."

        "Kneel for her inspection and read what the stubs confess. [[One-Time Climax — High Risk]]" if player.anxiety < 75 and player.get_total_suspicion("stern") < 80:

            # [BEAT] Climax spice ~2.2 — hotel layer inspection, not explicit H-scene
            # [STATE] State/progression update
            $ apply_balanced_effect("transgressive", intensity="standard", witness="stern")
            $ story.complete_chain_beat("stern", path="climax")

            cora "A banker's draft stub, Ma'am. And a dry rose from a florist on the Strand that closed last month."
            cora "The guest was spending money he did not yet have, on a woman who would not wait."

            "Miss Stern turns so quickly the hem of her wool dress brushes my boots."

            stern "Enough."
            stern "Your cleverness is a disease. You look through guests' pockets with your eyes."

            "She seizes my wrists, pulls my arms behind my back, and forces me to my knees on the Savoy carpet before the vanity."
            "Her lace cap slips slightly askew. Her breath comes hot against my face as she leans down."

            stern "Since you are so fond of this floor, remain here. I will inspect your uniform's inner seams."

            "Her hands trace my skirt beneath the apron, checking hidden linings with a slowness that has nothing to do with housekeeping."
            "Warm fingers linger above my stockings. My skin shivers between dread and want."

            stern "A maid who cannot be trusted must be thoroughly occupied, Cora Vale."
            stern "Do not move. If you speak a word of this — if you breathe —"

            "She leaves me flushed on the floor."
            "Pure material for the book — and my name now lives in her private ledger."

        "Press further... [[Locked: Anxiety >= 75 or Stern Suspicion >= 80]]" if player.anxiety >= 75 or player.get_total_suspicion("stern") >= 80:

            # [STATE] Blocked path: descriptive diegetic message explaining the mechanic

            "You cannot press further. Your hands shake too violently (Anxiety: [player.anxiety]/75), and Miss Stern's iron watch is already too close (Stern Suspicion: [player.stern_suspicion]/80). Another step would invite breakdown or dismissal."

    # [ASSET] Visual/staging command
    hide stern_sprite
    return


# ==============================================================================
# 3. DYNAMIC NARRATIVE CHAIN: MISSY ("The Laundry Quarters Erotics")
# ==============================================================================

# [DAG_NODE id=missy_chain_1 type=chain character=missy level=1]
label missy_chain_1:

    # [ASSET] Visual/staging command
    scene bg_laundry_room_day
    with fade

    show missy_sprite smiling at centre_bust

    # [BEAT] Step 1: Mutual protection pact — labour solidarity, not romance yet

    "The laundry room is a thick, humid fog of lye and boiling starch."

    if time_manager.time_of_day == "Morning":
        "The boilers shriek under full pressure. Stern could appear on the service stair at any moment."
    elif time_manager.time_of_day == "Afternoon":
        "Afternoon heat turns the room into a visible furnace. Sweat makes every touch look like guilt."
    else:
        "The late-night tubs lose their heat in silence. Secrets spoken here have nowhere to hide."

    "Missy sits on a wicker hamper, fingers red from coarse soap."
    "A torn lace collar lies in her lap."

    missy "If Miss Stern sees this tear, she'll dock my pay three shillings. Room 301 — he threw his boots at the door while I changed the wash-water. He has no right, Cora."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=missy_chain_1_menu_1]
    menu:
        "Stitch in silence and owe her nothing beyond labour. [[Shed Suspicion / Close Track]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(missy_susp=-10)
            $ story.abandon_chain_beat("missy")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show missy_sprite smiling at right_bust with move # [asset auto]
            cora "Give it here. French seam. Stern's glass won't find the raw edge."
            "I take the needle. We sit shoulder to shoulder in the steam."

            missy "You're a good friend. Most girls would have carried the tale to Stern for credit."

            "Her trust is useful. It is not yet dangerous."

        "Comfort her with touch she did not ask for — yet. [[Advance / Trust Pact]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="missy")
            $ story.complete_chain_beat("missy", path="safe_progress")

            cora "You should not bear his cruelty, Missy. Was it the wine, or is he always that way behind a closed door?"

            "I trace the damp skin of her cheek, brushing a wet curl behind her ear."
            "Missy flinches, but she does not retreat. Her moral shield wavers under unexpected warmth."

            missy "Cora... your hands are soft. Not like mine."
            cora "We belong where we can protect each other."

            "Her eyes focus on me with quiet intensity."
            "This is not romance yet. It is a pact — two girls deciding the Savoy will not eat her alone."

    # [ASSET] Visual/staging command
    hide missy_sprite
    return


# [DAG_NODE id=missy_chain_2 type=chain character=missy level=2]
label missy_chain_2:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_dim
    with fade

    show missy_sprite neutral at centre_bust

    # [BEAT] Step 2: Shared secret — valet case, danger-bonding in the dark
    if time_manager.time_of_day == "Evening":
        "The corridor gas jets burn low. Stern's keys on the wall would be the first sound of ruin."
    else:
        "Late night empties the service lift. Footsteps carry farther than they should."

    "Missy leans in, breath sharp with lye and peppermint."

    if story.get_character_chain_level("missy") >= 1:
        missy "You were kind to me over the tubs. I should not tell you this."

    missy "Mr. Locke's valet carried a leather case down the back stairs. Brass hinges. Double lock."
    missy "He looked at me like he wanted to choke me for seeing it. They hide things, Cora."

    "Footsteps echo at the end of the hall. Miss Stern's keys shadow the wainscoting."
    "I drag Missy into the cedar broom closet and shut the door on the light."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=missy_chain_2_menu_1]
    menu:
        "Tell her to forget the case and survive. [[Shed Suspicion / Close Track]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(missy_susp=-15)
            $ story.abandon_chain_beat("missy")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show missy_sprite neutral at right_bust with move # [asset auto]
            cora "Don't look at it again, Missy. Valets keep secrets because they are paid to."
            missy "You're right. I'll forget. God keep us quiet."

            "Relief softens her face. The secret stays buried — and so does whatever we might have become."

        "Hold her in the dark and make the danger ours. [[Advance / Entangled]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="missy")
            $ story.complete_chain_beat("missy", path="safe_progress")

            "The closet smells of cedar oil and damp aprons."
            "We are pressed chest to chest, breathing in the same inch of air."
            "My hand finds her waist. She does not pull away."

            cora "Double locks? Was it a Chubb patent?"
            missy "Cora... we are too close. If Stern opens this door..."
            cora "Then let her find us warm. Locks are not the only thing that can bind a person."

            "Missy gasps and leans into me — a conscious choice, not a stumble."
            "Stern's keys outside frame the heat. We are not prying now. We are choosing each other in the dark."

    # [ASSET] Visual/staging command
    hide missy_sprite
    return


# [DAG_NODE id=missy_chain_3 type=chain character=missy level=3]
label missy_chain_3:

    # [ASSET] Visual/staging command
    scene bg_laundry_room_day
    with fade

    show missy_sprite shocked at centre_bust

    # [BEAT] Step 3: Authorship betrayal — the page proves the crime
    if time_manager.time_of_day == "Afternoon":
        "The boilers are silent. Afternoon steam clings to the floor like a witness."
    else:
        "Only the furnace embers light the room. Intimacy here would be impossible to deny."

    "Missy stops me at the wash-tubs, holding a scrap of my manuscript."

    if story.get_character_chain_level("missy") >= 2:
        missy "After the closet... I thought we were protecting each other. Was I only material?"

    missy "Is this me, Cora? 'The laundry girl with raw fingers who believed every promise she found in a pocket'?"
    missy "Did you write this? Have you been prying into my soul to make a story?"

    # [CHOICE] Decision point
    # [DAG_CHOICE group=missy_chain_3_menu_1]
    menu:
        "Tear the page and bury what we might have been. [[Close Track / Lose Climax]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(missy_susp=-20)
            $ story.abandon_chain_beat("missy")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show missy_sprite shocked at right_bust with move # [asset auto]
            cora "A draft, Missy. Cruel practice. I used what was nearest."
            "I tear the page into four pieces before her."
            cora "I am sorry."

            "She watches the scraps fall. Suspicion breaks — but the trust that could have flowered is dead."

        "Defend the writing and ask her into the ending. [[One-Time Climax — High Risk]]" if player.anxiety < 75 and player.get_total_suspicion("missy") < 80:

            # [BEAT] Climax spice ~2.2 — mutual yield, stolen silk chemise
            # [STATE] State/progression update
            $ apply_balanced_effect("transgressive", intensity="standard", witness="missy")
            $ story.complete_chain_beat("missy", path="climax")

            cora "It is a story, Missy. It says you are better than the sheets you wash. I want to write the ending with you."

            "My fingers find the knot of her apron. Missy holds still as I untie it."
            "Beneath the coarse uniform: stolen cream silk from suite 402, clinging to damp curves no chambermaid is permitted."

            cora "You do not belong in coarse cotton."

            "Silk catches the furnace glow. I trace her collarbone, feeling her pulse flutter."
            "I ease the straps down her shoulders. She gasps but does not stop me."

            missy "If Stern catches us... we are ruined."
            cora "Then we leave together. But not before we see the ending."

            "Our lips meet — peppermint, heat, and a yield that is hers as much as mine."
            "I have not only used her. I have asked her to author the sin with me."

        "Press further... [[Locked: Anxiety >= 75 or Missy Suspicion >= 80]]" if player.anxiety >= 75 or player.get_total_suspicion("missy") >= 80:

            # [STATE] Blocked path: descriptive diegetic message explaining the mechanic

            "You cannot press further. Your nerves are too frayed (Anxiety: [player.anxiety]/75), and Missy's mistrust is too sharp (Missy Suspicion: [player.missy_suspicion]/80)."

    # [ASSET] Visual/staging command
    hide missy_sprite
    return


# ==============================================================================
# 4. DYNAMIC NARRATIVE CHAIN: MISS VANCE ("The Blackmail Collusion")
# ==============================================================================

# [DAG_NODE id=vance_chain_1 type=chain character=vance level=1]
label vance_chain_1:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning
    with fade

    show vance_sprite neutral at centre_bust

    # [BEAT] Step 1: Witnessed humiliation — Gideon's shadow on a dropped petal
    "The grand guest corridor is silent, the red carpet absorbing every sound."

    if time_manager.time_of_day == "Morning":
        "Morning light makes the brass shine. A guest might round the corner at any moment."
    elif time_manager.time_of_day == "Evening":
        "Evening sconces warm the mahogany. Performance feels easier when the hall is dim."
    else:
        "Late night hums in the electric bulbs. Theft of a glance feels louder than theft of silk."

    "Miss Vance walks the corridor. A silk handkerchief slips from her sleeve and falls like a petal."

    if story.day2_tea_choice == "prey":
        cora_inner "I have seen what Mr. Locke does to her when she fails. This small loss may cost more than silk."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=vance_chain_1_menu_1]
    menu:
        "Return the silk and be furniture. [[Shed Suspicion / Close Track]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(vance_susp=-10)
            $ story.abandon_chain_beat("vance")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show vance_sprite neutral at right_bust with move # [asset auto]
            cora "Your handkerchief, Miss."
            "I offer it on my flat palm, eyes on her hem."

            vance "Ah. Useless little thing. Keep it or burn it, girl."

            "She sweeps past. I remain forgettable."

        "Steal the handkerchief and study her panic. [[Advance / Voyeur]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="vance")
            $ story.complete_chain_beat("vance", path="safe_progress")

            "I cover the silk with my shoe and slide it into my apron pocket."

            vance "Girl. Has anyone passed? My handkerchief — it was here."

            cora "No one, Miss."

            "She searches her sleeve with increasing frenzy, cheeks flushing under lacquered hair."
            "From the corridor's end I watch her performance — petulance dressed as grief, authority dressed as helplessness."

            vance "You. You stood there like a post. Did you see it fall?"

            cora "I saw only the carpet, Miss."

            vance "Liar. Your eyes are too quick for a country fool."

            "She steps closer. Jasmine oil and warm skin press into my face."
            "She does not recover the handkerchief. She recovers her audience — and I am the mirror she hates."

            cora_inner "The way her hands shake when she is thwarted is already a sentence in the book."

    # [ASSET] Visual/staging command
    hide vance_sprite
    return


# [DAG_NODE id=vance_chain_2 type=chain character=vance level=2]
label vance_chain_2:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_dim
    with fade

    show vance_sprite angry at centre_bust

    # [BEAT] Step 2: Grief witnessed — class mask slips on the back stairs
    if time_manager.time_of_day == "Evening":
        "Evening shadows pool on the back staircase. A lady may cry here only if no one admits to seeing."
    else:
        "Late night cold climbs the brick. Grief sounds indecent without an audience to deny it."

    "Miss Vance sits on the bottom step, face in her hands, shoulders shaking with dry, tearless grief."

    if story.get_character_chain_level("vance") >= 1:
        cora_inner "I still have her handkerchief in my apron. She does not know it, but I have already stolen something from her."

    "The electric bulb turns her red hair to spun copper."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=vance_chain_2_menu_1]
    menu:
        "Slip past and leave her performance unseen. [[Shed Suspicion / Close Track]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(vance_susp=-15)
            $ story.abandon_chain_beat("vance")

            "I step back into the doorway shadow and do not breathe."
            "She never knows I was there."

        "Wipe her tear and reverse the mirror. [[Advance / Dominance Play]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="vance")
            $ story.complete_chain_beat("vance", path="safe_progress")

            "I step into the light before her."
            "Vance looks up, eyes wide with fury."

            vance "What are you staring at, you vulgar creature? Back to the cellars!"

            "I bend and wipe a wet tear with my rough thumb, holding her chin steady."

            # [ASSET] Visual/staging command
            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show vance_sprite angry at right_bust with move # [asset auto]
            cora "I see a lady trying not to look corrected."
            vance "You dare touch me?"
            cora "The maid who watches holds the door. Remember that when you return to his suite."

            "She trembles between fury and submission."
            "I have not comforted her. I have named the shape of her humiliation — and kept it."

    # [ASSET] Visual/staging command
    hide vance_sprite
    return


# [DAG_NODE id=vance_chain_3 type=chain character=vance level=3]
label vance_chain_3:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with fade

    show vance_sprite angry at centre_bust

    # [BEAT] Step 3: Shared crime — brass key as collusion under Gideon's shadow
    if time_manager.time_of_day == "Afternoon":
        "Afternoon sun fills the suite. Discovery here would be instant and theatrical."
    else:
        "Fireplace embers barely light the room. Collusion thrives where witnesses cannot see."

    "Miss Vance catches me in the bedroom, clutching a brass desk key."

    if story.get_character_chain_level("vance") >= 2:
        vance "You watched me on the stairs. You always watch."

    vance "You were outside the door when he... when we..."
    vance "What do you want? Speak, or I will tell Stern you stole my pearl pin."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=vance_chain_3_menu_1]
    menu:
        "Play the potato maid and let the key go. [[Close Track / Lose Climax]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(vance_susp=-20)
            $ story.abandon_chain_beat("vance")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show vance_sprite angry at right_bust with move # [asset auto]
            cora "I saw nothing, Miss. I came to turn down the blankets."
            vance "Simple. Yes. You look like a potato."

            "She turns away. The collusion dies unborn."

        "Corner her at the vanity and name Gideon's mark on her throat. [[One-Time Climax — High Risk]]" if player.anxiety < 75 and player.get_total_suspicion("vance") < 80:

            # [BEAT] Climax spice ~2.2 — collar marks, key transfer, Gideon shadow
            # [STATE] State/progression update
            $ apply_balanced_effect("transgressive", intensity="standard", witness="vance")
            $ story.complete_chain_beat("vance", path="climax")

            cora "I see a lady afraid of a key, Miss."
            cora "And a master who need not raise his voice to make her kneel."

            "I force her back until her hips strike the vanity edge."
            "My thumb traces the faint red collar marks Gideon's touch left on her throat."

            vance "Gideon will kill you if he finds you here."
            cora "Then let him find us both holding the same secret."

            "I pry the brass key from her fingers. Our palms linger — hers hot, mine rough."
            "She droops in surrender, Gideon's shadow wrapping us both."

        "Press further... [[Locked: Anxiety >= 75 or Vance Suspicion >= 80]]" if player.anxiety >= 75 or player.get_total_suspicion("vance") >= 80:

            # [STATE] Blocked path: descriptive diegetic message explaining the mechanic

            "The suite door looms too large. Anxiety: [player.anxiety]/75. Vance Suspicion: [player.vance_suspicion]/80. Discovery here would be dismissal."

    # [ASSET] Visual/staging command
    hide vance_sprite
    return


# ==============================================================================
# 5. CONFRONTATIONS AND PENANCE (STAT RECOVERY VEHICLES)
# ==============================================================================

# [DAG_NODE id=confrontation_stern type=penance]
label confrontation_stern:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning
    with fade

    show stern_sprite neutral at centre_bust

    "Miss Stern stands before me, her hands folded over her keys."

    stern "You have been seen, Cora Vale. In the west wing. In the laundry room. Spying. Whispering."
    stern "A maid with an opinion is a maid who belongs on the Strand."

    if story.stern_chain_penance_echo():
        cora_inner "She has already touched me where a maid should not be touched. This feels like the next page of the same discipline."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show stern_sprite neutral at right_bust with move # [asset auto]
    cora "Ma'am—"

    stern "Quiet. You will spend your night scrubbing the grand marble steps of the entrance hall."
    stern "On your knees. With the coarse soap."
    stern "The guests will see a maid who has learned her place in the open air."
    stern "And if I find a single speck of dirt before dawn, you will leave without a character."

    # [ASSET] Visual/staging command
    hide stern_sprite

    "I scrub until the marble shines and my knees bruise."
    "Footmen pass above me with luggage and laughter. The humiliation is the point."
    "My hands are raw. The manuscript receives nothing tonight."

    # Penance effects: reduces Stern suspicion by 35, but advances time, consuming the slot.

    # [STATE bespoke: legacy_exception]
    $ apply_effects(stern_susp=-35, corr=5)
    return


# [DAG_NODE id=confrontation_vance type=penance]
label confrontation_vance:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning
    with fade

    show vance_sprite angry at centre_bust

    "Miss Vance corners me near the service elevator."

    vance "You insolent, spying creature. I told Gideon you were looking through the grates."
    vance "He said you were too small to kill. I disagreed."

    if story.vance_chain_penance_echo():
        cora_inner "She knows I have watched her. Gideon is the audience in her head even when he is not in the room."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show vance_sprite angry at right_bust with move # [asset auto]
    cora "Miss Vance, I was only—"

    vance "You will wash my silk chemises again. Every one. By hand."
    vance "Cold water. No fire under the tub."
    vance "Lavender until I can smell it from the corridor — or I tell Stern you touched my purse."

    # [ASSET] Visual/staging command
    hide vance_sprite

    "The water bites. Silk slithers like skin that refuses to belong to me."
    "My knuckles split. Lavender rises, sweet and insulting — class perfume forced through a maid's cracked hands."
    "The manuscript waits, untouched."

    # Penance effects: reduces Vance suspicion by 35, but advances time, consuming the slot.

    # [STATE bespoke: legacy_exception]
    $ apply_effects(vance_susp=-35, corr=5)
    return


# [DAG_NODE id=confrontation_missy type=penance]
label confrontation_missy:

    # [ASSET] Visual/staging command
    scene bg_laundry_room_day
    with fade

    show missy_sprite shocked at centre_bust

    "Missy stands in my doorway, her eyes swollen from crying."

    missy "I know what you are, Cora. You're a spy. You've been using me. You've been watching Vance and Locke and writing it down."
    missy "I won't let you ruin me. If Stern asks, I'll tell her everything."

    if story.missy_chain_penance_echo_betrayal():
        cora_inner "She is right. I used what she gave me. The page was only the proof."
    elif story.missy_chain_was_abandoned():
        cora_inner "I closed that track myself. That does not make her wrong to call me a spy."

    # [STATE bespoke: legacy_exception]
    $ apply_effects(missy_susp=-35, insp=5)
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show missy_sprite shocked at right_bust with move # [asset auto]
    cora "Missy, please. If you tell her, I am ruined. Let me help you. I'll do the night tubs for you."

    missy "You'll... you'll do my shifts?"

    cora "Yes. Every sheet."

    "She stares at me, then nods slowly, her face hardened by my betrayal."

    missy "Then get to the boilers. And don't speak to me again."

    # [ASSET] Visual/staging command
    hide missy_sprite

    "She does not watch me leave. That is worse than shouting."
    "I boil sheets that are not mine until the steam scalds my face."
    "Exile is the penance — not the labour. The pen refuses to move."

    # Penance effects: reduces Missy suspicion by 35, but advances time, consuming the slot.
    return


# [DAG_NODE id=anxiety_breakdown_downtime type=penance]
label anxiety_breakdown_downtime:
    # Staging/acting

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with fade

    "My hands shake so violently I can barely hold the brass key ring. The walls of the Savoy seem to press closer, the hum of the gas lamps sounding like a chorus of whispers."
    "Every step in the corridor, every rustle of silk, feels like an accusation. I cannot push further. I cannot ask questions."
    "Tonight, I keep my head low. I speak only when spoken to, fold the linen with double-stitch seams, and scrub the floors until the wood is clean."
    "By the time the dawn shift begins, my muscles ache, but the immediate panic has receded. The eyes watching me have drifted back to their own concerns."

    # Relieve anxiety by dynamically decreasing suspicion across the board

    # [STATE] State/progression update
    $ player.relieve_downtime_anxiety()
    return
