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
            sys_msg "[[WARNING: Cora's anxiety has reached 70%% again. High anxiety will restrict her choices and lead to complete writing paralysis at 85%%. Manage her stress carefully.]]"

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


# [DAG_NODE id=advance_after_confrontation type=router]
label advance_after_confrontation:
    # DEPRECATED:
    # Old route-owner pattern. New chain and penance labels must return to their caller.
    # [STATE] Route lookup — add new days in StoryState.POST_PENANCE_ROUTES (classes_non_canon.rpy)
    $ _target = story.get_post_penance_target(time_manager.current_day, time_manager.time_of_day)
    $ story.consume_penance()
    if _target is None:
        return

    # [STATE] State/progression update
    $ time_manager.set_current_day(_target[0])
    $ set_time_period(_target[1])
    jump expression _target[2]


# ==============================================================================
# 2. DYNAMIC NARRATIVE CHAIN: MISS STERN ("The Sovereign Disciplines")
# ==============================================================================

# [DAG_NODE id=stern_chain_1 type=chain character=stern level=1]
label stern_chain_1:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning
    with fade

    show stern_sprite neutral at centre_bust

    # [BEAT] Step 1: The Linen Closet Audit. Narrow space, tight inspection

    "The west wing linen closet is narrower than a confessional and smells of starch and cold lye."

    if time_manager.time_of_day == "Morning":
        "Outside, the busy morning rush of the second-floor shift carries a muffled, mechanical hum."
    elif time_manager.time_of_day == "Evening":
        "The gas wall-sconces outside are already unlit, casting long, dim shadows across the threshold."
    else:
        "The quiet of the late-night corridor is absolute, making every rustle of cotton sound like a warning."

    "Miss Stern stands inside, her keys clutched in her hand like a small iron crop."
    "Her eyes move from my collar to the folded sheets, measuring the precision of my service."

    stern "Cora. The sheets for suite 402. Did you fold them with the lock-stitch hem outward, or did you simply tumble them in the country fashion?"

    # [CHOICE] Decision point
    # [DAG_CHOICE group=stern_chain_1_menu_1]
    menu:
        "Lower my head and act like a simple, stupid country girl. [[Shed Suspicion / Break Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(stern_susp=-10)
            $ story.complete_chain_beat("stern")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show stern_sprite neutral at right_bust with move # [asset auto]
            cora "Outward, Ma'am. Missy showed me, and I made sure to repeat it exactly so as not to offend."
            stern "Exactly is a large word for a small mind. Keep to that simple standard, Cora, and the Strand will remain a distant worry."

            "She dismisses me with a slight twitch of her chin."
            "My safety costs nothing but my pride. The door to her private ledger is shut."

        "Explain the geometry of the fold, meeting her gaze. [[Lean Into Tension / Progress Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="stern")
            $ story.complete_chain_beat("stern")

            cora "The outward stitch preserves the line of the silk, Ma'am. It prevents friction against the mahogany frame, keeping the fabric warm to the touch."

            "Miss Stern goes still."
            "Her chest rises once, her keys clicking softly in the quiet cupboard."

            stern "Touch? A girl who knows the grain of the guest's bed is a girl who spends too much time looking at what does not belong to her."

            "She steps closer. The heavy, warm scent of wool and lavender soap surrounds me."
            "Slowly, she raises the cold iron ring of her keys, placing the flat metal against the side of my neck to correct my posture, forcing my chin upward."

            stern "Keep that chin high, Cora Vale. But do not let me find you looking down at the silk again."

            "Her touch is brief, cold, and utterly improper."
            "I have shown too much edge, and she has marked the place where it sits."

    # [ASSET] Visual/staging command
    hide stern_sprite
    return


# [DAG_NODE id=stern_chain_2 type=chain character=stern level=2]
label stern_chain_2:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with fade

    show stern_sprite neutral at centre_bust

    # [BEAT] Step 2: The Notebook Extraction. High-tension boundary crossing
    if time_manager.time_of_day == "Evening":
        "The servants' quarters are thick with the grey London twilight, the copper steam pipes muttering behind the wall."
    else:
        "A cold late-night draft rattles the small windowpane, casting flickering candle-shadows across the narrow floor."

    "I am resting on the edge of the narrow bed when the door handles jiggles. Miss Stern enters before the latch can sound."
    "I scramble to slide the cheap notebook under my uniform apron, but her hand descends."
    "She does not snatch it. She merely presses her thumb onto the leather cover, keeping it pinned against my lap."

    stern "A ledger of kitchen weights, Cora? Or does a chambermaid believe she has thoughts worth preserving in ink?"

    # [CHOICE] Decision point
    # [DAG_CHOICE group=stern_chain_2_menu_1]
    menu:
        "Apologize and call it a spelling exercise. [[Shed Suspicion / Break Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(stern_susp=-10)
            $ story.complete_chain_beat("stern")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show stern_sprite neutral at right_bust with move # [asset auto]
            cora "Only my letters, Ma'am. My mother said a maid who cannot spell the inventory is of no use to a fine house."
            stern "Your mother was sensible. Keep to spelling 'apron' and 'lye', Cora. Leave the long words to those who do not have to wash them."

            "She draws her hand back and leaves. The notebook is safe, but the ink in my veins feels cold."

        "Hold the notebook tight. Read her a scandalous anonymous passage. [[Progress Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="stern")
            $ story.complete_chain_beat("stern")

            cora "I was writing about the west corridor, Ma'am."
            stern "Speak plainly, girl."
            cora "I wrote: 'The warden of the floor has a voice like iron, but her keys shake when she touches the maid's collar. She has a secret appetite for the dust she pretends to clean.'"

            "Miss Stern's keys slip from her fingers, striking the floor with a bright, silver clatter."
            "She does not bend to retrieve them."
            "Instead, she steps forward, pinning me flat against the small wooden desk."
            "Her breathing is ragged, her face inches from mine, her fingers sliding beneath my coarse uniform apron to press directly against my corset, checking my pulse."

            stern "You are a monstrous creature, Cora Vale. A thief who steals the thoughts of her betters."
            cora "Is it theft if it is true, Ma'am?"
            stern "If I find this notebook again... I will burn it. And then I will write a reference for you that will make the Strand look inviting."

            "Her hand remains pressed against my chest for one second longer than warning requires."
            "Her touch is hot, trembling, and full of dread."
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

    # [BEAT] Step 3: The Vacant Room Corrective. Level 4 tease, intimate submission
    if time_manager.time_of_day == "Afternoon":
        "The afternoon sun filters through the velvet drapes of the vacant Master Suite, casting a dusty, golden glare across the carpet."
    else:
        "The evening drapes are drawn tight, the electric wall-sconces deactivated; only a single wax candle burns on the dressing table."

    "Miss Stern stands beside the vanity. She has pulled out a drawer and dumped its contents onto the floor: a dry rose, banker's stubs, and three scraps of paper."
    "Her keys hang from her belt, clicking as she turns her head to study me."

    stern "A guest leaves many things. The young maid sees them as souvenirs. I see them as evidence of character."
    stern "Tell me, Cora. What do you see?"

    # [CHOICE] Decision point
    # [DAG_CHOICE group=stern_chain_3_menu_1]
    menu:
        "Play the blind servant, turning away from her gaze. [[Shed Suspicion / Lost Opportunity: Safe option, but you lose this climax forever.]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(stern_susp=-15)
            $ story.complete_chain_beat("stern")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show stern_sprite neutral at right_bust with move # [asset auto]
            cora "Dust, Ma'am. And scraps that should have been swept before the second floor shift."
            stern "Correct. A drawer is a box for linens, not a confessional."

            "She nods, satisfied with my simple maid's mask."
            "I remain a ghost in her hotel, safe but starved for the book's ending. The fire between us is extinguished, never to be rekindled."

        "Seize the one-time opportunity: Step into her space and audit the stubs. [[Climax: 2.2 Spice. Spikes Suspicion (+25) and Corruption (+20), raising Anxiety. Requires: Anxiety < 75 and Stern Suspicion < 80]]" if player.anxiety < 75 and player.get_total_suspicion("stern") < 80:

            # [STATE] State/progression update
            $ apply_balanced_effect("transgressive", intensity="standard", witness="stern")
            $ story.complete_chain_beat("stern")

            cora "I see a banker's draft stub, Ma'am. And a dry rose from a florist on the Strand that closed last month."
            cora "The guest was spending money he did not yet have, on a woman who did not want to wait for it."

            "Miss Stern turns on me so quickly the hem of her heavy black wool dress brushes my boots."

            stern "Enough!"
            stern "Your cleverness is a disease, Cora. You look through the guests' pockets with your eyes."

            "She grabs me by the wrists. Her grip is iron-tight, pulling my arms behind my back and forcing me down onto my knees on the thick pile of the Savoy carpet before the vanity."
            "Her face is flushed, her neat lace cap slipping slightly askew from the sudden exertion. Her breath comes hot against my face as she leans down, her chest pressing against my shoulder."

            stern "Since you are so fond of this floor, you will remain here. On your knees. I will inspect your uniform's inner seams to ensure you have stolen nothing else."

            "She bends over me, her hands tracing the coarse cotton of my skirt. Slowly, her fingers slide beneath the heavy apron, reaching the rear laces of my corset and unhooking the hem to check the hidden linings."
            "Her fingers are warm, lingering against my bare thighs above my stockings under the guise of an audit. The heat of her hand makes my skin shiver, every brush of her fingertips sending a sharp, sweet jolt of dread and desire through my spine."
            "I tremble, my chest pressing hard against the vanity drawer, the scent of lavender and starch thick in my throat."

            stern "A maid who cannot be trusted must be thoroughly occupied, Cora Vale."

            "Her fingers slide higher, tracing the curve of my hip with a slow, deliberate pressure that has nothing to do with housekeeping."
            "I let out a soft gasp, my head falling back against her shoulder, feeling the rapid beat of her heart behind her starch collar."

            stern "Do not move, Cora. If you speak a word of this... if you breathe..."

            "She leaves me flushed, breathing heavily, and ruined on the floor."
            "The raw material I have gathered is pure fire, but my name is now safely written in her private book."

        "Seize the one-time opportunity... [[Locked: Anxiety too high (>= 75) or Suspicion too high (>= 80). Choosing this would trigger an immediate breakdown or public dismissal.]]" if player.anxiety >= 75 or player.get_total_suspicion("stern") >= 80:

            # [STATE] Blocked path: descriptive diegetic message explaining the mechanic

            "You cannot press further. Your hands shake too violently from your frayed nerves (Anxiety: [player.anxiety]/75), and the dread of Miss Stern's iron keys is a physical barrier. To push her now, when she already watches your every step with deep mistrust (Stern Suspicion: [player.stern_suspicion]/80), would invite an immediate breakdown or public dismissal."

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

    # [BEAT] Step 1: The Lye-Steam French Seam. Damp, close contact

    "The laundry room is a thick, humid fog of lye and boiling starch."

    if time_manager.time_of_day == "Morning":
        "The copper boilers are shrieking under full morning pressure, turning every face soft at the edges."
    elif time_manager.time_of_day == "Afternoon":
        "The afternoon heat is suffocating, steam dripping down the grey slate walls like grease."
    else:
        "The late-night tubs are cooling, the quiet hum of the boilers sounding like a sleeping beast."

    "Missy is sitting on a wicker laundry hamper, her fingers red and raw from the coarse soap."
    "A torn lace collar lies in her lap, and she is trying to sew it with trembling hands."

    missy "If Miss Stern sees this tear, she'll dock my pay three shillings. It was that gentleman in room 301. He threw his boots at the door while I was changing the wash-water. He has no right, Cora. None at all."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=missy_chain_1_menu_1]
    menu:
        "Help her stitch it silently. Comfort her. [[Shed Suspicion / Break Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(missy_susp=-10)
            $ story.complete_chain_beat("missy")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show missy_sprite smiling at right_bust with move # [asset auto]
            cora "Give it here. My mother taught me the French seam. It hides the raw edge completely, so even Stern's glass won't find it."
            "I take the needle. We sit together on the wicker hamper, our shoulders touching in the warm steam."

            missy "You're a good friend, Cora. Most girls here would have carried the tale to Miss Stern to get the credit."

            "Her trust feels heavy. But it keeps my cover secure."

        "Stroke her cheek, questioning her with tender, quiet romance. [[Progress Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="missy")
            $ story.complete_chain_beat("missy")

            cora "You shouldn't have to bear his cruelty, Missy. Was it the wine, or is he always that monstrous when the door is closed?"

            "I reach out, my fingers tracing the damp, flushed skin of her cheek, brushing a wet curl of hair behind her ear with lingering, safe tenderness."
            "Missy flinches, her breath catching, but she does not retreat. Her defensive moral shield falters under the unexpected warmth."

            missy "Cora... your hands are so soft. Not like mine. You don't belong over the lye-tubs."
            cora "We belong where we can protect each other, Missy."

            "She looks up, her eyes wide, quiet, and exceptionally focused in the steam."
            "I have treated her pain with tenderness, and the physical heat between us has become real, rooted in the beginning of trust."

    # [ASSET] Visual/staging command
    hide missy_sprite
    return


# [DAG_NODE id=missy_chain_2 type=chain character=missy level=2]
label missy_chain_2:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_dim
    with fade

    show missy_sprite neutral at centre_bust

    # [BEAT] Step 2: The Broom Closet Hiding. Pressed chest-to-chest
    if time_manager.time_of_day == "Evening":
        "The corridor gas jets are turned low, casting long, dark shadows along the service lift."
    else:
        "The late-night quarters are silent, the faint sound of footsteps echoing on the stairs above."

    "Missy leans in close, her breath smelling faintly of lye and the peppermint she keeps to mask it."

    missy "I saw Mr. Locke's valet carrying a leather case down the back stairs. It had brass hinges and a double lock."
    missy "He looked at me like he wanted to choke me for being there. They hide things, Cora. Terrible things."

    "Suddenly, heavy footsteps echo at the end of the hall. The shadow of Miss Stern's keys appears on the wall."
    "Before I can think, I grab Missy by the wrist and drag her into the narrow cedar broom closet, closing the door behind us into pitch blackness."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=missy_chain_2_menu_1]
    menu:
        "Tell her to keep quiet for her own safety. [[Shed Suspicion / Break Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(missy_susp=-15)
            $ story.complete_chain_beat("missy")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show missy_sprite neutral at right_bust with move # [asset auto]
            cora "Don't look at it again, Missy. Valets keep secrets because they are paid to. We are paid only to wash the sheets."
            missy "You're right. I'll forget I ever saw it. God keep us quiet."

            "She smiles, relieved by my caution. The secret stays safe."

        "Press her chest-to-chest in the dark, whispering with sensual agency. [[Progress Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="missy")
            $ story.complete_chain_beat("missy")

            "The broom closet is tiny, smelling of cedar oil and damp aprons."
            "We are pressed chest-to-chest, our breathing echoing in the small enclosure."
            "I slide my hand over Missy's narrow waist to steady her, my fingers sinking into the soft cloth of her corset."
            "Missy does not pull away. In the dark, her face is inches from mine, her lips parted, her eyes reflecting the sliver of gas-lamp light under the door."

            cora "Double locks? Was it a Chubb patent?"
            missy "Cora... please. We are too close. If Miss Stern opens this door..."
            cora "Then let her find us. Your skin is too warm for locks, Missy."

            "Missy gasps softly, her hands clutching my shoulders, her chest rising against mine as she actively chooses to lean into the touch."
            "The social danger of Miss Stern's keys outside becomes the structural frame that heightens our physical proximity."
            "We are not prying; we are catching fire in the dark, and her yield is a conscious, sovereign choice."

    # [ASSET] Visual/staging command
    hide missy_sprite
    return


# [DAG_NODE id=missy_chain_3 type=chain character=missy level=3]
label missy_chain_3:

    # [ASSET] Visual/staging command
    scene bg_laundry_room_day
    with fade

    show missy_sprite shocked at centre_bust

    # [BEAT] Step 3: The Untouched Silk. Level 3 erotic climax, unlacing
    if time_manager.time_of_day == "Afternoon":
        "The laundry boilers are silent, the late-afternoon steam settling in damp layers over the floor."
    else:
        "The late-night laundry is completely vacant, the only light coming from the red embers of the boiler furnace."

    "Missy stops me near the wash-tubs, holding a discarded scrap of my manuscript."
    "Her face is pale under the electric light, her fingers shaking."

    missy "Is this... me, Cora? 'The laundry girl with raw fingers who believed every promise she found in a pocket'?"
    missy "Did you write this? Have you been prying into my soul to make a story?"

    # [CHOICE] Decision point
    # [DAG_CHOICE group=missy_chain_3_menu_1]
    menu:
        "Tear the page and beg her forgiveness. [[Shed Suspicion / Lost Opportunity: Safe option, but you lose this climax forever.]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(missy_susp=-20)
            $ story.complete_chain_beat("missy")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show missy_sprite shocked at right_bust with move # [asset auto]
            cora "It was a draft, Missy. A stupid, cruel exercise. I was trying to find the words, and I used what was closest."
            "I take the page and tear it into four pieces before her."
            cora "I am sorry. Truly."

            "She looks at the torn paper, then at me. The wound remains, but the suspicion is broken. Yet, the trust that could have flowered between us is dead."

        "Seize the one-time opportunity: Defend the writing and unlace her apron. [[Climax: 2.2 Spice. Spikes Suspicion (+20) and Corruption (+20), raising Anxiety. Requires: Anxiety < 75 and Missy Suspicion < 80]]" if player.anxiety < 75 and player.get_total_suspicion("missy") < 80:

            # [STATE] State/progression update
            $ apply_balanced_effect("transgressive", intensity="standard", witness="missy")
            $ story.complete_chain_beat("missy")

            cora "It is a story, Missy. A beautiful one. It shows how much better you are than the sheets you wash. And I want to write the ending with you."

            "I step closer. My fingers reach behind her waist, finding the rough linen knot of her outer maid's apron. Missy flinches, her eyes wide, but she holds herself still, her breathing shallow as she allows me to untie it."
            "The apron slips from her shoulders, pooling on the floor between our boots. Beneath the coarse uniform, she is wearing the stolen silk chemise from suite 402—soft, cream-coloured silk that clutches her damp curves in a way no chambermaid is permitted."

            cora "You don't belong in coarse cotton, Missy."

            "The white silk catches the warm red glow of the laundry furnace, glowing like hot amber against her throat. My fingers trace the delicate lace collar of the chemise, then slide downward over her collarbone, feeling the frantic, fluttering beat of her pulse."
            "I slide my hands beneath the silk straps, pushing them slowly down her arms, exposing the soft, bare curve of her shoulders to the warm furnace air. She gasps, her hands gripping my forearms, her knuckles turning white."

            missy "Cora... if Miss Stern catches us... we'll be dismissed. Ruined."
            cora "Then we will leave together. But not before we see the ending."

            "I pull her flush against me, my lips brushing the side of her neck, inhaling the sweet, heavy scent of lavender soap and warm skin. Missy trembles, her forehead dropping onto my shoulder as she yields to the heat of the embrace."

            missy "Then show me the ending, Cora. I want to see it with you."

            "Our lips meet in a frantic, silent kiss, taste of peppermint and heat, a mutual surrender in the dark, steam-choked room."
            "The trust is absolute, and the physical entanglement is complete—a dramatic middle ground of pure, mutual, and sovereign passion."

        "Seize the one-time opportunity... [[Locked: Anxiety too high (>= 75) or Suspicion too high (>= 80). Choosing this would trigger an immediate breakdown or public dismissal.]]" if player.anxiety >= 75 or player.get_total_suspicion("missy") >= 80:

            # [STATE] Blocked path: descriptive diegetic message explaining the mechanic

            "You cannot press further. Your nerves are too frayed (Anxiety: [player.anxiety]/75), and the fear of Missy betraying you to Stern is too real. To take such a step, when her suspicion of your prying is already too high (Missy Suspicion: [player.missy_suspicion]/80), would push you over the edge into ruin."

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

    # [BEAT] Step 1: The Dropped Silk Handkerchief. Class voyeurism

    "The grand guest corridor is silent, the red carpet absorbing every sound."

    if time_manager.time_of_day == "Morning":
        "The morning sun filters through the leaded glass, making the brass fixtures shine."
    elif time_manager.time_of_day == "Evening":
        "The evening wall-sconces cast a warm, dim light across the mahogany panels."
    else:
        "The late-night corridor is cold, the electric bulbs hum in the silent hall."

    "Miss Vance walks down the corridor. As she turns the corner, a silk handkerchief slips from her sleeve."
    "It lies on the red carpet like a dropped petal."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=vance_chain_1_menu_1]
    menu:
        "Return it silently with a perfect maid's bow. [[Shed Suspicion / Break Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(vance_susp=-10)
            $ story.complete_chain_beat("vance")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show vance_sprite neutral at right_bust with move # [asset auto]
            cora "Your handkerchief, Miss."
            "I offer it on my flat palm, my eyes fixed on her hem."

            vance "Ah. Useless little thing. Keep it or burn it, girl."

            "She sweeps past. Low risk, minimal reward."

        "Cover it with my shoe, sliding it into my apron. [[Progress Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="vance")
            $ story.complete_chain_beat("vance")

            "I step forward, cover the silk with my shoe, and slide it into my apron pocket."
            "Later, from the end of the hall, I watch her search her sleeve, her face tightening with a petulant panic."
            "She catches my eye and realizes what I did, her mouth opening in a silent, scandalized gasp."
            "The way she uses her hands when she is thwarted is a perfect detail for my manuscript."

    # [ASSET] Visual/staging command
    hide vance_sprite
    return


# [DAG_NODE id=vance_chain_2 type=chain character=vance level=2]
label vance_chain_2:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_dim
    with fade

    show vance_sprite angry at centre_bust

    # [BEAT] Step 2: The Staircase Grief. Power reversal
    if time_manager.time_of_day == "Evening":
        "The back staircase is dark with the evening shadows, the damp scent of the cellars rising through the boards."
    else:
        "The late-night staircase is cold, a single flickering candle casting long shadows on the brick wall."

    "I find Miss Vance sitting on the bottom step of the back staircase."
    "She has her face in her hands, her shoulders shaking with a dry, tearless grief after Gideon's harsh correction."
    "The electric bulb makes her red hair look like spun copper."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=vance_chain_2_menu_1]
    menu:
        "Slip past silently in the shadows. [[Shed Suspicion / Break Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(vance_susp=-15)
            $ story.complete_chain_beat("vance")

            "I step back into the shadow of the doorway. I do not breathe."
            "She does not see me. My cover is safe."

        "Confront her. Wipe a tear with my rough thumb. [[Progress Chain]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("curious", intensity="standard", witness="vance")
            $ story.complete_chain_beat("vance")

            "I step out of the shadow, standing directly before her."
            "I watch the way she catches her breath, the petulance of her grief."
            "Vance looks up, her eyes wide with fury."

            vance "What are you staring at, you vulgar creature? Get back to the cellars!"

            "Instead of bowing, I bend down, my rough, lye-stained thumb wiping a wet tear from her cheek."
            "My touch is coarse, deliberate, and holding her chin steady."

            # [ASSET] Visual/staging command
            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show vance_sprite angry at right_bust with move # [asset auto]
            cora "I see a lady who is trying not to look like she has been corrected."
            vance "You... you dare touch me?"
            cora "The maid who watches, Miss, is the one holding the door. Remember that when you return to his suite."

            "She shakes with a mix of fury and submission, unable to look away."
            "I have made a dangerous enemy, but I have unlocked the heart of the book."

    # [ASSET] Visual/staging command
    hide vance_sprite
    return


# [DAG_NODE id=vance_chain_3 type=chain character=vance level=3]
label vance_chain_3:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with fade

    show vance_sprite angry at centre_bust

    # [BEAT] Step 3: The Desk Blackmail. Level 4 tease, Gideon shadow
    if time_manager.time_of_day == "Afternoon":
        "The Master Suite is bright with the afternoon sun, the writing desk lying open."
    else:
        "The late-night suite is silent, only the faint embers of the fireplace lighting the room."

    "Miss Vance catches me inside the suite bedroom. She is holding a brass desk key she must have stolen from Mr. Locke's cabinet."
    "She looks at me with a wild, cornered intensity."

    vance "You. You've been watching me. You were outside the door when he... when we..."
    vance "What do you want, girl? Speak, or I will tell Stern you stole my pearl pin."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=vance_chain_3_menu_1]
    menu:
        "Play the simple country maid to allay her fears. [[Shed Suspicion / Lost Opportunity: Safe option, but you lose this climax forever.]]":

            # [STATE] State/progression update
            $ apply_balanced_effect("creative", intensity="standard")
            # [STATE bespoke: negative_suspicion]
            $ apply_effects(vance_susp=-20)
            $ story.complete_chain_beat("vance")

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show vance_sprite angry at right_bust with move # [asset auto]
            cora "I saw nothing, Miss. I only came to turn down the blankets. I am very simple and do not know the guests' business."
            vance "Simple. Yes. You look like a potato."

            "She turns away, dismissed by my performance. My cover is safe, but the key to her private rebellion is forever lost to me."

        "Seize the one-time opportunity: Corner her against the vanity and audit her collar marks. [[Climax: 2.2 Spice. Spikes Suspicion (+20) and Corruption (+20), raising Anxiety. Requires: Anxiety < 75 and Vance Suspicion < 80]]" if player.anxiety < 75 and player.get_total_suspicion("vance") < 80:

            # [STATE] State/progression update
            $ apply_balanced_effect("transgressive", intensity="standard", witness="vance")
            $ story.complete_chain_beat("vance")

            cora "I see a lady who is afraid of a key, Miss."
            cora "And a master who does not need to raise his voice to make her kneel."

            "I step forward, forcing her back until her hips strike the hard mahogany edge of the vanity. She gasps, her hands clutching the dressing table's drawers as she tries to hold her ground, but her eyes are wide with a dark, submissive fascination."
            "I reach out, my fingers slowly tracing the faint, red collar marks that Gideon's heavy touch left on her pale throat. Vance shivers, her head tilting back as my rough, lye-stained skin rubs against the delicate silk of her high collar."
            "I slide my hand lower, tracing the silk fabric of her bodice, feeling the tight constriction of her whalebone stays. Her chest rises and falls rapidly against my palm, her breath hitching."

            vance "Gideon... he will kill you if he finds you here."
            cora "Then he will have to find us first. Let us write the next chapter together in the closet."

            "I reach down and pry the small brass cabinet key from her fingers, letting my hand linger against her hot palm, brushing our thumbs together. Her fingers close weakly around mine before she lets go, her head drooping in surrender."
            "She looks down, her submission complete, the shadow of Gideon's power wrapping around both of us, a shared secret that binds us in corruption."

        "Seize the one-time opportunity... [[Locked: Anxiety too high (>= 75) or Suspicion too high (>= 80). Choosing this would trigger an immediate breakdown or public dismissal.]]" if player.anxiety >= 75 or player.get_total_suspicion("vance") >= 80:

            # [STATE] Blocked path: descriptive diegetic message explaining the mechanic

            "The shadow of the door looms too large. You cannot risk Sir Gideon returning and finding you in his mistress's quarters. Your anxiety is too high (Anxiety: [player.anxiety]/75), or her suspicion of you is too dangerous (Vance Suspicion: [player.vance_suspicion]/80) to survive discovery in the Master Suite."

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

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show stern_sprite neutral at right_bust with move # [asset auto]
    cora "Ma'am—"

    stern "Quiet. You will spend your night scrubbing the grand marble steps of the entrance hall."
    stern "On your knees. With the coarse soap."
    stern "And if I find a single speck of dirt before dawn, you will leave without a character."

    # [ASSET] Visual/staging command
    hide stern_sprite

    "The penance is brutal."
    "My hands are raw, my back is ruined, and I have had no time to look at the manuscript tonight."
    "The night is completely lost to stone and lye."

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

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show vance_sprite angry at right_bust with move # [asset auto]
    cora "Miss Vance, I was only—"

    vance "You will wash my silk chemises again. Every one of them. By hand."
    vance "In the cold water. Until your knuckles bleed."
    vance "And if they do not smell of lavender by morning, I will tell Stern you touched my purse."

    # [ASSET] Visual/staging command
    hide vance_sprite

    "I spend the night over the cold laundry tubs, my fingers numb and my mind empty of words."
    "The manuscript waits, untouched, while I wash the sweat of my betters out of silk."
    "The night is lost."

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

    "I spend the night in the steam and lye, carrying the weight of both our shifts."
    "My ambition is buried under wet cotton. I cannot write a single line."

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
