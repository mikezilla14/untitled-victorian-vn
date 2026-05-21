# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes

# story_chains_non_canon.rpy
# Writers' Room - Release 1 / Dynamic Narrative Story Chains & Confrontations Draft
# Enforces character-specific suspicion thresholds, deferred penance routing, and deadlines.

# ==============================================================================
# 1. DEFERRED CONFRONTRATIONS CHECKPOINT & TIME-ADVANCEMENT ROUTER
# ==============================================================================

label check_confrontations:
    # Game Over Dismissal check (Suspicion >= 100)
    if player.suspicion >= 100:

        # [STATE] State/progression update
        jump game_over_dismissed

    # Confrontation gates checked at the start of non-work personal slots (50%)
    if player.stern_suspicion >= 50:

        # [STATE] State/progression update
        jump confrontation_stern
    elif player.vance_suspicion >= 50:

        # [STATE] State/progression update
        jump confrontation_vance
    elif player.missy_suspicion >= 50:

        # [STATE] State/progression update
        jump confrontation_missy
    return


label advance_after_confrontation:
    # Router to advance time after penance, skipping the current personal/ledger/writing slot.
    if time_manager.current_day == 1:
        if time_manager.time_of_day == "Evening":

            # [STATE] State/progression update
            $ set_time_period("Night")
            jump day101_4_writing_or_visiting
        elif time_manager.time_of_day == "Night":

            # [STATE] State/progression update
            $ time_manager.set_current_day(2)
            $ set_time_period("Morning")
            jump day102_1_cora_missy_first_shift

    elif time_manager.current_day == 2:
        if time_manager.time_of_day == "Afternoon":

            # [STATE] State/progression update
            $ set_time_period("Evening")
            jump day102_3_stern_fetches_cora
        elif time_manager.time_of_day == "Night":

            # [STATE] State/progression update
            $ time_manager.set_current_day(3)
            $ set_time_period("Morning")
            jump day103_morning

    elif time_manager.current_day == 3:
        if time_manager.time_of_day == "Morning":

            # [STATE] State/progression update
            $ set_time_period("Afternoon")
            jump day103_2_suite_gideon_tea
        elif time_manager.time_of_day == "Evening":

            # [STATE] State/progression update
            $ set_time_period("Night")
            jump day103_4_room_stern_suspicion
        elif time_manager.time_of_day == "Night":

            # [STATE] State/progression update
            $ time_manager.set_current_day(4)
            $ set_time_period("Morning")
            jump day104_1

    elif time_manager.current_day == 4:
        # Day 4 penance consumes writing time before bed, resulting in a draft failure at dawn.
        if story.penance_triggered:

            # [STATE] State/progression update
            $ story.set_penance_triggered(False)
            $ set_time_period("Night")
            jump day104_6_false_dawn_ending
        else:
            if time_manager.time_of_day == "Evening":

                # [STATE] State/progression update
                $ set_time_period("Night")
                jump day104_5_triumphant_chapter
            elif time_manager.time_of_day == "Night":

                # [STATE] State/progression update
                $ time_manager.set_current_day(5)
                $ set_time_period("Morning")
                jump day105_1_monster_reemerges

    return


# ==============================================================================
# 2. CHARACTER STORY CHAIN BEATS (content only)
# ==============================================================================
# Slot-entry menus live in day10X_non_canon.rpy (contextual copy per REFLECT node).
# Routing uses StoryState.chain_available() and StoryState.resolve_chain_label()
# from classes_non_canon.rpy (promote into renpy_project/game/classes.rpy).
# Never hard-code stern_chain_N in day files.


# ==============================================================================
# 3. DYNAMIC NARRATIVE CHAIN: MISS STERN
# ==============================================================================

label stern_chain_1:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning
    with fade

    show stern_sprite neutral at center

    "Miss Stern stands outside the linen closet, a ledger of supplies clutched like a weapon."
    "Her eyes are small, cold calipers."

    stern "Cora. The sheets for suite 402. Did you fold them with the lock-stitch hem outward, or did you simply tumble them in the country fashion?"
    
    # [CHOICE] Decision point
    menu:
        "Lower my head and let her lecture me. [Safety first]":

            # [STATE] State/progression update
            $ apply_effects(stern_susp=-10, insp=5, corr=0)
            $ story.set_stern_chain_level(1)
            cora "Outward, Ma'am. Missy showed me, and I made sure to repeat it exactly."
            stern "Exactly is a large word for a small mind. Keep that precision, and you may survive another week."
            "She dismisses me with a slight twitch of her chin."
            "Safety costs nothing but pride."

        "Explain the geometry of the fold with quiet competence. [Ambition/Exposure]":

            # [STATE] State/progression update
            $ apply_effects(stern_susp=10, insp=10, corr=0)
            $ story.set_stern_chain_level(1)
            cora "The outward stitch preserves the line of the silk, Ma'am. It prevents friction against the mahogany frame."
            stern "Ma-hog-any?"
            "She repeats the syllables as if they were a crime I committed."
            stern "A girl who knows the grain of the guest's bed is a girl who spends too much time looking at what does not belong to her."
            "I have shown too much edge."

    # [ASSET] Visual/staging command
    hide stern_sprite
    jump advance_after_confrontation


label stern_chain_2:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with fade

    show stern_sprite neutral at center

    "I am resting in the servants' hall when Miss Stern enters."
    "Before I can slide the cheap notebook under my apron, her hand descends."
    "She does not snatch it. She merely presses her thumb onto the cover."

    stern "A ledger of kitchen weights, Cora? Or does a chambermaid believe she has thoughts worth preserving in ink?"
    
    # [CHOICE] Decision point
    menu:
        "Apologize and call it a spelling exercise. [Safety first]":

            # [STATE] State/progression update
            $ apply_effects(stern_susp=-10, insp=5, corr=0)
            $ story.set_stern_chain_level(2)
            cora "Only my letters, Ma'am. My mother said a maid who cannot spell the inventory is of no use to a fine house."
            stern "Your mother was sensible. Keep to spelling 'apron' and 'lye', Cora. Leave the long words to those who do not have to wash them."
            "She leaves. The notebook is safe, but my fingers feel stained."

        "Meet her eyes. Defend the right to write. [Ambition/Exposure]":

            # [STATE] State/progression update
            $ apply_effects(stern_susp=15, insp=15, corr=10)
            $ story.set_stern_chain_level(2)
            cora "A kitchen has many stories, Ma'am. Sometimes a girl needs to see the shape of her day to know she has lived it."
            stern "Shape? Stories?"
            stern "The Savoy has exactly one story, Cora Vale. It is called profit. You are the grease in the gears."
            stern "If I find this book in your hand again, I will burn it. And then I will write a reference for you that will make the Strand look inviting."
            "A threat. Clear, heavy, and very useful for Chapter 2."

    # [ASSET] Visual/staging command
    hide stern_sprite
    jump advance_after_confrontation


label stern_chain_3:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with fade

    show stern_sprite neutral at center

    "Miss Stern summons me to the vacant Locke suite. She is holding a drawer from the dressing table."
    "She turns it over, dumping three scraps of paper and a dry rose onto the carpet."

    stern "A guest leaves many things. The young maid sees them as souvenirs. I see them as evidence of character."
    stern "Tell me, Cora. What do you see?"

    # [CHOICE] Decision point
    menu:
        "Pretend to see only rubbish. [Safety first]":

            # [STATE] State/progression update
            $ apply_effects(stern_susp=-15, insp=5, corr=0)
            $ story.set_stern_chain_level(3)
            cora "Dust, Ma'am. And scraps that should have been swept before the second floor shift."
            stern "Correct. A drawer is a box for linens, not a confessional."
            "She nods, satisfied with my stupidity. I remain a ghost in her hotel."

        "Analyze the scrap: extract the drama. [Ambition/Exposure]":

            # [STATE] State/progression update
            $ apply_effects(stern_susp=15, insp=20, corr=10)
            $ story.set_stern_chain_level(3)
            cora "A banker's draft stub, Ma'am. And a dry rose from a florist on the Strand that closed last month."
            cora "The guest was spending money he did not yet have, on a woman who did not want to wait for it."
            stern "Enough!"
            stern "Your cleverness is a disease, Cora. You look through the guests' pockets with your eyes."
            stern "I will be watching you. Every hour. Every scrap."
            "I have pushed her to the limit, but the materials I gathered are pure fire."

    # [ASSET] Visual/staging command
    hide stern_sprite
    jump advance_after_confrontation


# ==============================================================================
# 4. DYNAMIC NARRATIVE CHAIN: MISSY
# ==============================================================================

label missy_chain_1:

    # [ASSET] Visual/staging command
    scene bg_laundry_room_day
    with fade

    show missy_sprite smiling at center

    "Missy is sitting on a laundry hamper, her fingers red and raw from the lye."
    "She has a small, torn lace collar in her lap. She is trying to sew it with trembling hands."

    missy "If Stern sees this tear, she'll dock my pay three shillings. It was that beast in room 301. He threw his boots at the door while I was changing the water."

    # [CHOICE] Decision point
    menu:
        "Help her stitch it. Comfort her. [Safety/Bond]":

            # [STATE] State/progression update
            $ apply_effects(missy_susp=-10, insp=10, corr=0)
            $ story.set_missy_chain_level(1)
            cora "Give it here. My mother taught me the French seam. It hides the raw edge completely."
            "I take the needle. We sit together in the steam, our shoulders touching."
            missy "You're a good friend, Cora. Most girls here would have told Stern to get the credit."
            "Her trust feels heavy. But it keeps my cover secure."

        "Question her about the boots: get the sensory details. [Ambition/Exploit]":

            # [STATE] State/progression update
            $ apply_effects(missy_susp=10, insp=15, corr=5)
            $ story.set_missy_chain_level(1)
            cora "Did he shout? What did his voice sound like when he threw them? Was it the wine, or something else?"
            missy "What? Why are you asking that?"
            "She pulls the lace back, looking at me with a sudden, sharp confusion."
            missy "He was angry, Cora. That's all. It isn't a play. It's my wages."
            "I have treated her pain as copy, and she felt the needle."

    # [ASSET] Visual/staging command
    hide missy_sprite
    jump advance_after_confrontation


label missy_chain_2:

    # [ASSET] Visual/staging command
    scene bg_laundry_room_day
    with fade

    show missy_sprite neutral at center

    "Missy leans in close over the wash-tub, her breath smelling of cheap peppermint."

    missy "I saw Mr. Locke's valet carrying a leather case down the back stairs. It wasn't luggage. It had brass hinges and a double lock."
    missy "He looked at me like he wanted to choke me for being there."

    # [CHOICE] Decision point
    menu:
        "Tell her to keep quiet for her own safety. [Safety/Bond]":

            # [STATE] State/progression update
            $ apply_effects(missy_susp=-15, insp=10, corr=0)
            $ story.set_missy_chain_level(2)
            cora "Then don't look at it again, Missy. Valets keep secrets because they are paid to. We are paid only to wash the shirts."
            missy "You're right. I'll forget I ever saw it."
            "She smiles, relieved by my caution. The secret stays safe."

        "Encourage her gossip. Press for the lock's design. [Ambition/Exploit]":

            # [STATE] State/progression update
            $ apply_effects(missy_susp=15, insp=20, corr=10)
            $ story.set_missy_chain_level(2)
            cora "Double locks? Were they the new Chubb patent, or the older brass wards?"
            cora "What else did the valet have? Did he have a key on his chain?"
            missy "Cora, why do you want to know about the locks?"
            "Her eyes narrow. She steps back from the wash-tub."
            missy "You're going to get us both dismissed. You look at this hotel like you're planning to steal it."
            "Her suspicion rises, but the details of the Chubb lock fit perfectly into the manuscript."

    # [ASSET] Visual/staging command
    hide missy_sprite
    jump advance_after_confrontation


label missy_chain_3:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_dim
    with fade

    show missy_sprite shocked at center

    "Missy stops me in the dim corridor outside the quarters. She is holding a discarded scrap of my draft."
    "Her face is pale under the electric light."

    missy "Is this... me, Cora? 'The laundry girl with raw fingers who believed every promise she found in a pocket'?"
    missy "Did you write this? Have you been using my words to make a story?"

    # [CHOICE] Decision point
    menu:
        "Apologize. Tear the page. Beg her forgiveness. [Safety/Bond]":

            # [STATE] State/progression update
            $ apply_effects(missy_susp=-20, insp=5, corr=0)
            $ story.set_missy_chain_level(3)
            cora "It was a draft, Missy. A stupid, cruel exercise. I was trying to find the words, and I used what was closest."
            "I take the page and tear it into four pieces before her."
            cora "I am sorry. Truly."
            "She looks at the torn paper, then at me. The wound remains, but the suspicion is broken."

        "Defend the writing. Tell her it makes her permanent. [Ambition/Exploit]":

            # [STATE] State/progression update
            $ apply_effects(missy_susp=20, insp=20, corr=15)
            $ story.set_missy_chain_level(3)
            cora "It is a story, Missy. A beautiful one. It shows how hard this place is, and how much better you are than the sheets you wash."
            missy "Better?"
            missy "You made me look like an idiot, Cora. A servant girl for people to laugh at on their sofas."
            missy "I trusted you. And you turned me into grease."
            "She turns and walks away. The trust is gone forever, but the cold truth of her anger is the best prose I have ever drafted."

    # [ASSET] Visual/staging command
    hide missy_sprite
    jump advance_after_confrontation


# ==============================================================================
# 5. DYNAMIC NARRATIVE CHAIN: VANCE
# ==============================================================================

label vance_chain_1:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning
    with fade

    show vance_sprite neutral at center

    "Miss Vance walks down the VIP corridor. As she turns the corner, her silk handkerchief slips from her sleeve."
    "It lies on the red carpet like a dropped petal."

    # [CHOICE] Decision point
    menu:
        "Return it silently with a perfect maid's bow. [Safety first]":

            # [STATE] State/progression update
            $ apply_effects(vance_susp=-10, insp=5, corr=0)
            $ story.set_vance_chain_level(1)
            cora "Your handkerchief, Miss."
            "I offer it on my flat palm, my eyes fixed on her hem."
            vance "Ah. Useless little thing. Keep it or burn it, girl."
            "She sweeps past. Low risk, minimal reward."

        "Keep it. Observe her reaction when she misses it. [Ambition/Exposure]":

            # [STATE] State/progression update
            $ apply_effects(vance_susp=15, insp=15, corr=5)
            $ story.set_vance_chain_level(1)
            "I step forward, cover the silk with my shoe, and slide it into my apron."
            "Later, from the end of the hall, I watch her search her sleeve, her face tightening with a small, petulant panic."
            "The way she uses her hands when she is thwarted — that petulance — is a perfect detail for the mistress in Chapter 1."

    # [ASSET] Visual/staging command
    hide vance_sprite
    jump advance_after_confrontation


label vance_chain_2:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_dim
    with fade

    show vance_sprite angry at center

    "I find Vance sitting on the bottom step of the back staircase."
    "She has her face in her hands. Her shoulders are shaking. The electric light makes her red hair look like copper wire."

    # [CHOICE] Decision point
    menu:
        "Slip past silently in the shadows. [Safety first]":

            # [STATE] State/progression update
            $ apply_effects(vance_susp=-15, insp=5, corr=0)
            $ story.set_vance_chain_level(2)
            "I step back into the shadow of the doorway. I do not breathe."
            "She does not see me. I remain a ghost in the Savoy."

        "Stay and watch. Record the rhythm of her grief. [Ambition/Exposure]":

            # [STATE] State/progression update
            $ apply_effects(vance_susp=15, insp=20, corr=10)
            $ story.set_vance_chain_level(2)
            "I remain standing in the light. I watch the way she catches her breath, the sharp, dry gasp that has no tears in it."
            "Vance looks up suddenly. Her eyes find mine."
            vance "What are you staring at, you vulgar creature? Get back to the cellars!"
            "I bow and retreat, but the rhythm of her fake grief is already safe in my mind."

    # [ASSET] Visual/staging command
    hide vance_sprite
    jump advance_after_confrontation


label vance_chain_3:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with fade

    show vance_sprite angry at center

    "Miss Vance catches me inside the suite bedroom. She is holding a brass key she must have taken from Mr. Locke's desk."
    "She looks at me with a wild, cornered intensity."

    vance "You. You've been watching me. You were outside the door when he... when we..."
    vance "What do you want, girl? Speak, or I will tell Stern you stole my pearl pin."

    # [CHOICE] Decision point
    menu:
        "Bow and play the simple country girl. [Safety first]":

            # [STATE] State/progression update
            $ apply_effects(vance_susp=-20, insp=5, corr=0)
            $ story.set_vance_chain_level(3)
            cora "I saw nothing, Miss. I only came to turn down the blankets. I am very simple, and I do not know the guests' business."
            vance "Simple. Yes. You look like a potato."
            "She turns away, dismissed by my performance. My cover is safe."

        "Look her in the eyes. Let her see my knowledge. [Ambition/Exposure]":

            # [STATE] State/progression update
            $ apply_effects(vance_susp=20, insp=20, corr=20)
            $ story.set_vance_chain_level(3)
            cora "I see a lady who is afraid of a key, Miss."
            cora "And a master who does not need to raise his voice to make her kneel."
            "Vance takes a step back. Her mouth opens in absolute terror."
            vance "You... you devil."
            "She leaves, shaking with fear. I have made a deadly enemy, but I have unlocked the heart of the book."

    # [ASSET] Visual/staging command
    hide vance_sprite
    jump advance_after_confrontation


# ==============================================================================
# 5. CONFRONTATIONS AND PENANCE
# ==============================================================================

label confrontation_stern:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning
    with fade

    show stern_sprite neutral at center

    "Miss Stern stands before me, her hands folded over her keys."

    stern "You have been seen, Cora Vale. In the west wing. In the laundry room. Spying. Whispering."
    stern "A maid with an opinion is a maid who belongs on the Strand."

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

    # [STATE] State/progression update
    $ apply_effects(stern_susp=-35, insp=0, corr=5)
    $ story.set_penance_triggered(True)
    jump advance_after_confrontation


label confrontation_vance:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning
    with fade

    show vance_sprite angry at center

    "Miss Vance corners me near the service elevator."

    vance "You insolent, spying creature. I told Gideon you were looking through the grates."
    vance "He said you were too small to kill. I disagreed."

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

    # [STATE] State/progression update
    $ apply_effects(vance_susp=-35, insp=0, corr=5)
    $ story.set_penance_triggered(True)
    jump advance_after_confrontation


label confrontation_missy:

    # [ASSET] Visual/staging command
    scene bg_laundry_room_day
    with fade

    show missy_sprite shocked at center

    "Missy stands in my doorway, her eyes swollen from crying."

    missy "I know what you are, Cora. You're a spy. You've been using me. You've been watching Vance and Locke and writing it down."
    missy "I won't let you ruin me. If Stern asks, I'll tell her everything."

    # [CHOICE] Decision point
    menu:
        "Plead with her. Offer to help her finish her extra shifts tonight.":

            # [STATE] State/progression update
            $ apply_effects(missy_susp=-35, insp=5, corr=0)
            $ story.set_penance_triggered(True)
            
            cora "Missy, please. If you tell her, I am ruined. Let me help you. I'll do the night tubs for you."
            
            missy "You'll... you'll do my shifts?"
            
            cora "Yes. Every sheet."
            
            "She stares at me, then nods slowly, her face hardened by my betrayal."
            
            missy "Then get to the boilers. And don't speak to me again."

            # [ASSET] Visual/staging command
            hide missy_sprite

            "I spend the night in the steam and lye, carrying the weight of both our shifts."
            "My ambition is buried under wet cotton. I cannot write a single line."

            # [STATE] State/progression update
            jump advance_after_confrontation


# ==============================================================================
# 6. DEADLINE FAIL STATE LABELS (SPEC SPECIFICATION)
# ==============================================================================

label game_over_deadline_1:

    # [ASSET] Visual/staging command
    hide screen stats_overlay
    sys "═══ GAME OVER: FIRST DEADLINE FAILED ═══"
    cora "I stare at the blank page."
    cora "Day 2 has ended, and I have not even written the first chapter."
    cora "Without a single page of progress, my ambition is nothing but a childish delusion."
    cora "I cannot face the publisher. I cannot face the page."
    cora "I have failed before I even truly began."
    sys "[[GAME OVER. You failed to write Chapter 1 by Day 2 Night. Manage your time and stats to ensure you have enough inspiration to write.]"
    return

label game_over_deadline_2:

    # [ASSET] Visual/staging command
    hide screen stats_overlay
    sys "═══ GAME OVER: DRAFT DEADLINE FAILED ═══"
    cora "The night of Day 4 passes into grey dawn."
    cora "My desk is littered with scraps of paper, but the draft is incomplete. I have only one chapter done."
    cora "The publisher's courier will arrive tomorrow. I have nothing to give him but excuses."
    cora "I have lost my chance. The door is closed."
    sys "[[GAME OVER. You failed to complete a second chapter/draft by Day 4 Night. Balance your stats and avoid confrontations to protect your writing slots!]"
    return


label game_over_dismissed:

    # [ASSET] Visual/staging command
    hide screen stats_overlay

    sys "═══ GAME OVER: NERVOUS BREAKDOWN ═══"

    cora "I could not keep the walls of my mind standing."
    cora "It was not a single eye that caught me. It was the weight of them all."
    cora "Vance's sharp contempt, Missy's mounting fear, Stern's cold, measuring gaze... they accumulated in my chest like lead."
    cora "The weight of their combined eyes cracks my mask."
    cora "I made a fatal slip in my duties, and Miss Stern found absolute cause to dismiss me."
    
    stern "Pack your things. A girl whose nerves are in such tatters cannot be trusted with the Savoy's quiet."
    
    cora "My hands were shaking too hard to tie my trunk. I stood on the Strand with nothing but a ruined reputation and the memory of electric light."
    cora "Without a character, London is a very cold, very hungry place."

    sys "[[GAME OVER. Your accumulated Anxiety reached 100%, causing a complete breakdown and leading to your dismissal. Manage your internal strain by spreading suspicion across different characters and triggering penances before your nerves fail you.]"

    return
