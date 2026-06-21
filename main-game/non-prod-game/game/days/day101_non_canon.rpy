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

# day101_non_canon.rpy
# Release 1 / Day 01 non-canon Ren'Py-shaped draft
# Pass: editor-revision-1 — selective merge per day101_narrative_change_brief.md
# Source intent: rewritten from Twine node map and existing Day 1 script.
# Asset constraint: uses only assets already present in the supplied Day 1 Ren'Py draft.
# Promotion note: replace story/player helper calls with the exact project runtime method names during implementation.

# ==========================================
# DAY 1 NODE MAP
# ==========================================
# main
#   -> 011-cora_waiting
#   -> 011-morning_interview
#   -> 011-vance_throws_toy
#   -> 012-missy_meets_cora
#   -> 012-coras_path_choice
#   -> 013-taking_stock_day1
#   -> 013-corruption_choice / 013-inspiration_choice
#   -> 014-writing_or_visiting
#   -> 014-write_the_chapter / 014-visit_missy
#   -> day102_1_cora_missy_first_shift


# ==========================================
# MAIN ENTRY
# ==========================================


# [DAG_NODE id=day101_main type=work day=101]
label day101_main:

    # [BEAT] Arrival precarity — Irish mask, ruin geometry, performed Wiltshire identity
    scene bg_savoy_corridor_morning:
        zoom 1.0
        xysize (1920,1080)

    # [ASSET] Visual/staging command
    with fade

    cora_inner "The Savoy does not merely employ girls like me. It strips them of their names, swallows them down, and polishes the brass with whatever is left."
    cora_inner "I hold my breath against the heavy, suffocating scent of expensive coal smoke, gas lamps, and the wet lavender water used to mask the smell of London's rot."
    cora_inner "Behind my teeth, my mother's soft, looping Cork lilt scrambles to escape. I force it down. Deep. Below the floorboards."
    cora_inner "Here, I must speak with the rounded, flat, hollow vowels of a Wiltshire parson's daughter. A single slip—one wild, soft Irish consonant—and my papers will be matches for the grate."
    cora_inner "And after the grate? The workhouse. Or the damp, gas-lit alleys of Holywell Street, selling my skin where I once hoped to sell my words."

    # [STATE] State/progression update
    jump day101_1_cora_waiting


# ==========================================
# 011 - CORA WAITING
# ==========================================

# [DAG_NODE id=day101_1_cora_waiting type=work day=101]
label day101_1_cora_waiting:

    # [ASSET] Existing Day 1 corridor background
    scene bg_savoy_corridor_morning:
        zoom 1.0
        xysize (1920,1080)

    # [ASSET] Visual/staging command
    with dissolve

    # [ASSET] Visual/staging command
    show cora_sprite guarded_travel at left:
        zoom 0.5
        xpos 350
        ypos 1.05
        xzoom -1.0

    # [ASSET] Visual/staging command
    with dissolve

    cora_inner "I stand outside Miss Stern's door, my traveling dress damp at the hem, my palms sweating against my small valise."
    cora_inner "Sir John's reference sits in my pocket like a blade with his name on the handle. He gave it cold, conditional, already regretted. If Stern smells the ink of my lies, the trap slams shut before I begin."

    "From behind the heavy mahogany door, a clock ticks with a heavy, metallic precision—the heartbeat of a house that owns every second of my day."

    "A maid passes carrying towels white enough to blind. A footman steps past with a silver tray."

    cora_inner "No one asks who I am."
    cora_inner "That is the first rule of this place. Be useful enough to ignore."

    stern "Enter." 

    # [STATE] State/progression update
    jump day101_1_morning_interview


# ==========================================
# 011 - MORNING INTERVIEW
# ==========================================

# [DAG_NODE id=day101_1_morning_interview type=work day=101]
label day101_1_morning_interview:

    # [ASSET] Visual/staging command
    scene bg_stern_office_entrance:
        zoom 1.0
        xysize (1920,1080)

    # [ASSET] Visual/staging command
    with dissolve

    # [ASSET] Visual/staging command
    show stern_sprite neutral at right:
        zoom 0.6
        xpos 0.85

    "Miss Stern stands rather than sits." 
    cora_inner "It is not courtesy. It is measurement."

    # [ASSET] Visual/staging command
    scene bg_stern_office_reverse:
        zoom 1.0
        xysize (1920,1080)

    # [ASSET] Visual/staging command
    with dissolve

    # [ASSET] Visual/staging command
    hide bg_stern_office_entrance
    hide stern_sprite neutral
    show stern_sprite neutral at right_full_body
    # [ASSET] Visual/staging command
    show cora_sprite base_travel at left_full_body
    with dissolve

    "Her eyes move from my cap to my boots." # camera?
    cora_inner "Weighing every inch for disobedience."
    stern "Cora Vale."
    
    # [ASSET] Visual/staging command
    show stern_sprite neutral at right_reframe
    # [ASSET] Visual/staging command
    show cora_sprite base_travel at left_reframe_mirror
    with moveinleft

    cora "Yes, Ma'am."

    stern "Sir John's reference speaks to your quiet nature. Your lack of curiosity."

    cora_inner "The paper is his leash. Wiltshire ended in dismissal at his wife's behest—not in my triumph."

    cora "I keep my eyes on my work, Ma'am."

    stern "You have worked in service before."

    cora_inner "The lie is waiting for me, neat as a folded sheet."

    cora "Yes, Ma'am. In the country."

    stern "The country forgives slowness. The Savoy does not."
    stern "A maid in this house is hands without noise, feet without weight, and memory without a tongue."
    stern "Can you be that?"

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day101_1_morning_interview_menu_1]
    menu:
        "How do I survive Stern's inspection?" 

        "Lower my eyes. Let her mistake fear for obedience.":

            # [STATE] Semantic balance profile: Cora survives Stern by performing meek obedience
            $ apply_balanced_effect("submissive", intensity="standard")
            $ story.set_day1_interview_state("meek")
            $ apply_archetype_edge("prey", 1)

            # [ASSET] Visual/staging command
            show cora_sprite guarded_travel at left_reframe
            # [ASSET] Visual/staging command
            show stern_sprite neutral at right_reframe
            with dissolve

            cora "I can, Ma'am. I only wish to work hard."
            stern "Wishing is for girls with leisure. You will work because you are told."
            cora "Yes, Ma'am."

            cora_inner "She hears a dull country girl."
            cora_inner "Good. Let the woman keep that version of me."

        "Answer cleanly. Let competence do what meekness cannot.":

            # [STATE] Semantic balance profile: Competence draws Stern's scrutiny
            $ apply_balanced_effect("defiant", intensity="standard", witness="stern")
            $ story.set_day1_interview_state("competent")
            $ apply_archetype_edge("ghost", 1)

            # [ASSET] Visual/staging command
            show cora_sprite base_travel at left_reframe
            # [ASSET] Visual/staging command
            show stern_sprite neutral at right_reframe
            # [ASSET] Visual/staging command
            with dissolve            

            cora "I can be quiet, quick, and exact. If I err, it will not be from carelessness."
            stern "Exact?"
            cora "Yes, Ma'am."
            stern "A dangerous word from a girl in a borrowed apron."

            cora_inner "There."
            cora_inner "She sees it. Not all of it, but enough to dislike me."

    stern "You speak with some polish, Vale. But polish can hide a great deal of dust."

    "Miss Stern steps from behind her desk. Her leather boots click with slow, deliberate pacing."
    "The scent of starch, vinegar, and cold lavender presses into my space. She stops inches from me, her height casting a long shadow over my face."
    "With a slow, clinical movement, she reaches out. Her fingers—dry, firm, and smelling faintly of carbolic soap—brush the collar of my traveling dress, tracing the line of my throat with a lingering, diagnostic pressure."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day101_1_morning_interview_menu_2]
    menu:
        "How do I respond to her invasive touch?"

        "Lower my chin, allowing her fingers to adjust the fabric, matching her slow rhythm.":

            # [STATE] Semantic balance profile: Cora yields to Stern's invasive touch
            $ apply_balanced_effect("obedient", intensity="standard")
            $ story.set_day1_stern_relation("subservient")
            $ apply_archetype_edge("prey", 1)

            # [ASSET] Visual/staging command
            show cora_sprite guarded_travel at left_reframe
            with dissolve

            cora "I... I only wish to give satisfaction, Ma'am."
            stern "Satisfaction is a transaction, Vale. I buy your silence and your labor. See that you do not default on either."

            cora_inner "Her fingers are cold against my neck, a physical threat dressed as administrative care. I keep my breathing shallow, letting her feel the tremor she expects."

        "Stand perfectly rigid, holding my breath to mask my pulse, letting her treat me like a mannequin.":

            # [STATE] Semantic balance profile: Cora holds rigid, unreadable stillness
            $ apply_balanced_effect("defiant", intensity="standard", witness="stern")
            $ story.set_day1_stern_relation("resistant")
            $ apply_archetype_edge("ghost", 1)

            # [ASSET] Visual/staging command
            show cora_sprite base_travel at left_reframe
            with dissolve

            cora "Yes, Ma'am."
            stern "A stone does not flinch when it is touched, Vale. But stones have no thoughts of their own. Can you be a stone?"
            cora "I can, Ma'am."

            cora_inner "I turn my gaze to the brass buttons of her jacket, letting my eyes glaze. My body is a weight she may arrange as she pleases, but my mind is somewhere else entirely."
            cora_inner "Unseen, untouched. A ghost in her own skin."

        "Meet her gaze directly through the closeness, accepting the intrusion with a steady pulse.":

            # [STATE] Semantic balance profile: Cora meets Stern's gaze through the closeness
            $ apply_balanced_effect("transgressive", intensity="major")
            $ story.set_day1_stern_relation("complicit")
            $ apply_archetype_edge("predator", 1)

            # [ASSET] Visual/staging command
            show cora_sprite base_travel at left_reframe
            with dissolve

            cora "I understand the value of a proper fit, Ma'am."
            stern "Do you?"
            
            "Miss Stern's thumb presses hard against the hollow above my collarbone, a brief, sharp warning before she slowly slides her hand down to lift my chin."

            stern "A maid who looks back is a maid who wants to be noticed, Vale. And noticed maids in the Savoy do not last long enough to collect their first quarter's wages."

            cora_inner "Her touch is hot, deliberate. It is not morality that guides her hand—it is the sheer, intoxicating pleasure of absolute control."
            cora_inner "I did not look away. She knows now I am measuring her, too."

    stern "The guests here are... particular, Vale. They have expensive tastes and very short memories. Some maids think they can trade their secrets for silk, or their bodies for a gentleman's favor."
    stern "They always end up on the street, or worse."
    
    "She paces behind her desk, her gaze remaining on my lips."
    
    stern "If a gentleman offers you a trinket, or asks you to enter his room when his wife is out... do you understand what happens to girls who lose their tongue, or keep it for the wrong price?"

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day101_1_morning_interview_menu_3]
    menu:
        "How do I reply to her warning about guest secrets?"

        "Lower my head, speaking with flat utility: 'I will keep my head down, Ma'am.'":

            # [STATE] Semantic balance profile: Fearful retreat before Stern's warning
            $ apply_balanced_effect("submissive", intensity="standard")
            $ story.set_day1_stern_secret_bound("fearful")
            $ apply_archetype_edge("prey", 1)

            cora "I will keep my head down, Ma'am. I have no interest in the guests."
            stern "Interest is a luxury. Avoidance is a chore. See that you do it."

            cora_inner "The warning works. She sees a frightened country girl who knows her place is a narrow ledge."

        "Keep my tone even, professional, and empty: 'I only see the work, Ma'am.'":

            # [STATE] Semantic balance profile: Cora claims rooms are empty until cleaned
            $ apply_balanced_effect("observant", intensity="standard")
            $ story.set_day1_stern_secret_bound("loyal")
            $ apply_archetype_edge("ghost", 1)

            cora "I only see the work, Ma'am. The rooms are empty to me until they are cleaned."
            stern "An excellent answer. Keep it true, and we shall have no difficulties."

            cora_inner "Empty rooms, empty faces. I will be the draft that blows through them, leaving no trace."

        "Meet her eyes with quiet audacity: 'I know how to keep secrets, Ma'am—and those of the house.'":

            # [STATE] Semantic balance profile: Cora hints she trades in house secrets
            $ apply_balanced_effect("reckless", intensity="major", witness="stern")
            $ story.set_day1_stern_secret_bound("exploitative")
            $ apply_archetype_edge("predator", 1)

            cora "I know how to keep secrets, Ma'am—and those of the house." # SLIP: Cora lets slip a hint of inappropriate confidence and education.
            stern "Secrets? A maid has no secrets, Vale. She only has duties. Remember that, or I will ensure your references become as blank as your future."

            cora_inner "A slip. I let her see the ink beneath the starch."
            cora_inner "But her eyes flared. She knows now that I am not just a maid; I am a witness. And witnesses can be bought, or they can be feared."

    stern "You will report to the laundry first. Missy will show you the necessary route."
    stern "You will not wander. You will not question guests. You will not cultivate opinions."

    cora_inner "Too late for that."

    stern "And if a guest drops something, breaks something, or throws something, you will retrieve it without expression."

    # [ASSET] Visual/staging command
    hide stern_sprite

    jump day101_1_vance_throws_toy


# ==========================================
# 011 - VANCE THROWS TOYS
# ==========================================

# [DAG_NODE id=day101_1_vance_throws_toy type=work day=101]
label day101_1_vance_throws_toy:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning:
        zoom 1.00
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with dissolve

    "The guest wing corridor gleams—mahogany, gloss, and velvet restraint."
    "I halt at the threshold between office and stairs, arms laden with clean linen."
    "A sharp clatter cracks against the wainscoting. A silver-gilt crystal scent-bottle spins across the carpet, spilling amber jasmine oil."

    # [ASSET] Visual/staging command
    show vance_sprite angry at right_full_body:
        xalign 0.6
        yalign 1.1
        zoom 0.8

    "A footman retreats, eyes lowered, as if escaping a blow."

    vance "Stupid, useless boy! I said the lavender toilet-water, not this vulgar, suffocating grease!"

    "She paces, breath shallow, cheeks flushed high under lacquered hair. The spilled scent hangs thick and hot, filling the narrow space with floral pressure."

    "Her gaze swings wildly, landing on me. Her chest rises and falls against stiff silk."

    vance "You. Girl. Do not stand there like a post. Pick it up before it stains the master's carpet."

    # [ASSET] Visual/staging command
    show cora_sprite base_travel at left_full_body:
        yalign 1.0
        xpos 0.25
        zoom 0.75

    # [ASSET] Visual/staging command
    with moveinleft

    "Her voice is velvet and grit—authority arranged, but trembling with petulant irritation."

    cora "Yes, Miss."

    "I pause. The jasmine oil has pooled on the red wool. I step forward, bending low, my fingers finding the cold, heavy silver."
    "From this proximity, the hem of her violet gown hovers inches from my hands. I hear the sharp drag of her breath, the nervous tap of her boot."

    vance "Careful, you clumsy creature! If you chip the crystal, Miss Stern will hear of it."

    cora_inner "I have handled worse than broken glass. Debt. Lies. Men who mistook my silence for consent."
    cora_inner "I lift the bottle, feeling the warmth of her nearness. I choose not to enumerate them."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day101_1_vance_throws_toy_menu_1]
    menu:
        "How do I present the scent-bottle back to Miss Vance?"

        "Lower my chin, offering the bottle with a humble, trembling maid's hand. [[Subservient posture]]":

            # [STATE] Semantic balance profile: Cora plays the meek servant for Vance
            $ apply_balanced_effect("submissive", intensity="standard", witness="vance")
            $ story.set_day1_vance_relation("subservient")

            # [ASSET] Visual/staging command
            show cora_sprite guarded_travel at left_full_body
            with dissolve

            cora "My apologies, Miss. I wish to serve."

            "Vance takes the bottle, her fingers brushing mine with a brief, cold swipe. She lifts her chin, her face smoothing as she absorbs my submission."

            vance "At least one of you has some sense of place. Go clean your hands, girl. You smell of the laundry."

            cora_inner "She sees a stupid country maid. I let her keep that version."

        "Stand straight and meet her gaze directly, holding the bottle between us. [[Defiant posture]]":

            # [STATE] Semantic balance profile: Cora challenges Vance with direct tone
            $ apply_balanced_effect("defiant", intensity="standard", witness="vance")
            $ story.set_day1_vance_relation("defiant")

            # [ASSET] Visual/staging command
            show cora_sprite base_travel at left_full_body
            with dissolve

            cora "It is not chipped, Miss. It is sound."

            "Vance goes still. Her eyes widen, traveling from my cap to my lips, startled by the directness of my tone."
            "She steps closer—jasmine and warm skin pressing into my face. Her breathing is loud in the quiet hall."

            vance "You speak with a great deal of confidence for a girl in a borrowed apron."
            vance "Do you want me to tell Miss Stern how you look at guests?"

            cora_inner "She threatens me, but her hand shakes as she reaches for the bottle."
            cora_inner "She is not angry. She is exposed."

        "Offer it on my flat palm with a cold, blank face. [[Ghostly posture]]":

            # [STATE] Semantic balance profile: Cora remains a blank mirror to Vance
            $ apply_balanced_effect("self_protective", intensity="standard", witness="vance")
            $ story.set_day1_vance_relation("ghostly")

            # [ASSET] Visual/staging command
            show cora_sprite base_travel at left_full_body
            with dissolve

            cora "The scent-bottle, Miss."

            "Vance snatches it, her expression twisting into a scowl of irritation. My complete lack of reaction is a wall she cannot scale."

            vance "Useless post. You are like a piece of furniture that has learned to walk."

            cora_inner "A mirror does not apologize for showing dust. It only holds the shape."

    # [ASSET] Visual/staging command
    show gideon_sprite cold at right_full_body:
        xalign 0.8
        yalign 1.0
        zoom 0.8
        
    gideon "Vance."

    # [ASSET] Visual/staging command
    hide vance_sprite
    hide cora_sprite
    # [ASSET] Visual/staging command
    show cora_sprite base_travel at left_bust:
        yalign 1.0
        xpos 0.2
    # [ASSET] Visual/staging command
    show vance_sprite submissive at left_bust:
        xpos 0.5
        xzoom -1.0
    # [ASSET] Visual/staging command
    show gideon_sprite cold at right_bust:
        zoom 1.0
        xpos 0.75

    # [ASSET] Visual/staging command
    with dissolve

    "One word. The corridor temperature drops."
    "Vance's shoulders fall. Her lips part in a swallowed gasp—petulant fury folding into practiced, submissive compliance."

    vance "Gideon. I... I was only correcting the maid. She was careless with the linen."

    gideon "You were making yourself visible."
    gideon "The hallway is for passage, Vance, not for theatre. Do not teach the servants bad habits before luncheon."

    "Vance's mouth closes tightly. She nods once, her eyes fixed on the silver buttons of his vest."

    vance "Of course, Sir."

    cora_inner "Of course. Not yes. Not sorry. Of course."
    cora_inner "As if obedience were a ceremony, and surrender her only dress."

    gideon "Your name, girl?"

    cora "Cora, Sir."

    gideon "Then learn quickly, Cora. This house rewards discretion. If Ms. Vance cannot manage her temper, I expect you to manage your tongue."

    cora_inner "He does not threaten with his voice. That is why it feels like an iron collar."

    # [ASSET] Visual/staging command
    hide gideon_sprite
    with dissolve

    "Mr. Locke turns and walks back toward the Master Suite, his boots striking the floor with quiet, absolute authority."
    "Vance remains behind a moment, her hands clutching the silver scent-bottle until her knuckles whiten."
    "She turns to me, her voice a low, burning hiss."

    vance "You. Do not think this is finished. Take my lace wrap and bring it to the dressing room. Now."

    # [ASSET] Visual/staging command
    hide vance_sprite
    hide cora_sprite
    with dissolve

    jump day101_1_vance_dressing_room


# ==========================================
# ADDITIONAL SCENE 1: VANCE'S RETALIATION (DRESSING ROOM)
# ==========================================

# [DAG_NODE id=day101_1_vance_dressing_room type=work day=101]
label day101_1_vance_dressing_room:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day:
        zoom 1.00
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with dissolve

    "The private vestibule of the Master Suite is warm, quiet, and smelling of French powder and the heavy spilled jasmine."
    "Gideon has gone into the inner study, the heavy mahogany door shut behind him."
    "Miss Vance stands by the vanity, her back to me. She has unpinned her heavy hat, her hair falling in loose red coils over her shoulders."

    # [ASSET] Visual/staging command
    show vance_sprite angry_dressing_gown at right_full_body:
        xpos 0.65
        ypos 1.05
        zoom 0.8

    vance "Close the door."

    "I step inside, the door latch clicking shut behind me. I set her lace wrap on the velvet bench."

    # [ASSET] Visual/staging command
    show cora_sprite base_travel at left_full_body:
        xpos 0.25
        ypos 1.05
        zoom 0.75

    # [ASSET] Visual/staging command
    with dissolve

    cora "The wrap is here, Miss."

    "She turns on me, her eyes bright with a mixture of shame and fury. She is breathing heavily, the laces of her corset visible where her collar has been loosened."

    vance "You saw that. You saw him correct me like a child."
    vance "Do you think it's amusing? A maid watching from the shadow, counting the master's words?"

    "She steps closer, cornering me against the wardrobe. Our breath mingles, the heat of her skin radiating through the silk dress. She reaches out, her hand catching the strap of my apron, her fingers pressing into my shoulder."

    vance "Help me unpin the collar. My fingers are shaking. {w}Well? Move!"

    "I step behind her. My fingers touch the warm, smooth skin of her neck as I reach for the silver pins of her lace collar."
    "Her pulse is a frantic, fluttering bird beneath my thumb. I can feel the shiver that runs through her spine as my rough, lye-stained skin rubs against her delicate throat."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day101_1_vance_dressing_room_menu_1]
    menu:
        "How do I touch Miss Vance's collar?"

        "Handle the lace with gentle, soothing fingers, easing the pressure. [[Protected posture]]":

            # [STATE] Semantic balance profile: Cora soothes Vance behind Gideon's back
            $ apply_balanced_effect("submissive", intensity="standard", witness="vance")
            $ story.set_day1_vance_relation("protected")

            # [ASSET] Visual/staging command
            show cora_sprite flushed at left_full_body
            with dissolve

            "I adjust the lace slowly, my touch light and reassuring against her hot skin."

            cora "He was harsh, Miss. But the wainscoting carries no tales. I have already forgotten his words."

            "Vance lets out a long, trembling sigh, her shoulders dropping. For a fraction of a second, her head tilts back, her soft hair brushing against my apron."

            vance "He... he only wishes me to be perfect. But it is... suffocating."
            vance "You are surprisingly gentle for a laundry girl."

            cora_inner "She wants shelter. Let me build a small, dark wall around her."

        "Touch the red pressure mark left on her collarbone by Gideon. [[Intimate posture]]":

            # [STATE] Semantic balance profile: Cora marks Vance's submission in private
            $ apply_balanced_effect("transgressive", intensity="major", witness="vance")
            $ story.set_day1_vance_relation("intimate")

            # [ASSET] Visual/staging command
            show cora_sprite flushed at left_full_body
            with dissolve

            "My thumb slides down her neck, pressing lightly against the red, flushed mark on her skin."

            cora "The master has a heavy hand, Miss. It must be difficult to wear his marks in public."

            "Vance gasps, her back arching slightly. Her hands grip the vanity table behind her, her knuckles turning red."

            vance "You... you insolent wretch. How dare you touch me there..."
            vance "Gideon would have you thrown to the streets if he knew you were speaking of his hand."

            cora "But he does not know, Miss. We are alone."

            "She shivers, her eyes dark and wet in the mirror. The physical heat between us is thick, a shared secret of submission and command."

        "Perform the duty with cold, clinical precision. [[Observed posture]]":

            # [STATE] Semantic balance profile: Cora documents Vance's vulnerability coldly
            $ apply_balanced_effect("observant", intensity="standard", witness="vance")
            $ story.set_day1_vance_relation("observed")

            # [ASSET] Visual/staging command
            show cora_sprite base_travel at left_full_body
            with dissolve

            "I unpin the collar cleanly, stepping back the moment the silk falls open."

            cora "It is undone, Miss. You are free."

            "Vance turns, looking at me with a frustrated scowl. She feels the coldness of my gaze, the way I treat her distress like an entry in a ledger."

            vance "You are like a stone, Cora. Go. Before I find a reason to have Stern inspect your trunk."

            cora_inner "A stone sees the mark. It does not shiver."

    # [ASSET] Visual/staging command
    hide vance_sprite
    hide cora_sprite
    with dissolve

    jump day101_1_vance_stairwell_encounter


# ==========================================
# ADDITIONAL SCENE 2: STAIRWELL CONFRONTATION
# ==========================================

# [DAG_NODE id=day101_1_vance_stairwell_encounter type=work day=101]
label day101_1_vance_stairwell_encounter:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_dim:
        zoom 1.00
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with dissolve

    "I slip out of the suite, my heart beating rapidly in the quiet corridor."
    "I turn toward the narrow service stairwell that leads down to the laundry, the air growing colder and smelling of damp stone."
    "Suddenly, the heavy door above creaks open. Footsteps hurry down the stone steps behind me."

    # [ASSET] Visual/staging command
    show vance_sprite indignant at right_full_body:
        xpos 0.65
        ypos 1.05
        zoom 0.8

    vance "Wait. You."

    "I turn. Vance stands on the step above me. She has not re-laced her collar; the silk is open, exposing her pale neck and the rising flush of her skin."

    # [ASSET] Visual/staging command
    show cora_sprite base_travel at left_full_body:
        xpos 0.25
        ypos 1.05
        zoom 0.75

    # [ASSET] Visual/staging command
    with dissolve

    "Before I can bow, she steps down, her hand catching my sleeve and dragging me into the shadow beneath the landing."
    "She presses me flat against the cold brick wall, her chest pressing against mine. The scent of jasmine is sharp and close, mixed with the sweat of her panic."

    vance "Tell me. Are you going to tell that old crow Stern? Or Missy?"
    vance "If Gideon thinks I am... compromised. If he thinks the servants are whispering about us..."

    "Her fingers tighten on my arm. She is trying to look threatening, but her chest is heaving, and her lips are trembling."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day101_1_vance_stairwell_encounter_menu_1]
    menu:
        "How do I reassure Miss Vance?"

        "Assure her of my absolute maid's silence. [[Loyal witness]]":

            # [STATE] Semantic balance profile: Cora pledges maid's silence in the stairwell
            $ apply_balanced_effect("obedient", intensity="standard", witness="vance")
            $ story.set_day1_vance_relation("loyal_witness")

            cora "I only see the sheets and the carpets, Miss. I have no time for gossip."

            "Vance studies my face, searchingly. Her breathing slows, her grip on my sleeve loosening."

            vance "Good. Keep it that way. If I hear a single whisper... I will know it was you."

            cora_inner "She is relieved, but the suspicion remains. I am still a witness she must watch."

        "Feed her anxiety, turning the power dynamics. [[Accomplice posture]]":

            # [STATE] Semantic balance profile: Cora whispers complicity into Vance's fear
            $ apply_balanced_effect("reckless", intensity="standard", witness="vance")
            $ story.set_day1_vance_relation("accomplice")

            # [ASSET] Visual/staging command
            show cora_sprite flushed at left_full_body
            with dissolve

            "I lean in close, my lips brushing her ear in the cold stairwell."

            cora "I saw how you looked at him, Miss. I know what it is to want a hand that commands you."
            cora "I won't tell Stern. But we both know the weight of his shoe."

            "Vance lets out a sharp, wet gasp. Her eyes flare with terror and a sudden, dark arousal. Her head falls back against the brick, her chest pressing hard against my hands."

            vance "You... you are a wicked girl, Cora. A dangerous, wicked girl."
            vance "If Gideon found you speaking to me like this..."

            cora "But he is in his study, Miss. And you are here. With me."

            "Our skin shivers in the cold draft. She does not pull away. The collusion between us is sealed in the dark stairwell."

        "Detach myself and push past her. [[Silent observer]]":

            # [STATE] Semantic balance profile: Cora keeps clinical distance from Vance
            $ apply_balanced_effect("observant", intensity="standard", witness="vance")
            $ story.set_day1_vance_relation("silent_observer")

            cora "Miss Stern is waiting for me in the laundry, Miss. If I am late, she will ask why I was delayed in the guest corridor."

            "That silences her. She pulls her hand back as if burned, her face hardening into her lady's mask."

            vance "Then go. Before I have you dismissed myself."

            cora_inner "I have the shape of her fear. That is all the material I need."

    # [ASSET] Visual/staging command
    hide vance_sprite
    hide cora_sprite
    with dissolve

    cora_inner "She retreats up the stairs, her silk skirt rustling in the dark."
    cora_inner "I watch her go. A lady of the Savoy, bound in silk and swallowed terror."
    cora_inner "There is a chapter in that. A very long one."

    # [STATE] State/progression update
    jump day101_2_missy_meets_cora


# ==========================================
# 012 - MISSY MEETS CORA
# ==========================================
# [DAG_NODE id=day101_2_missy_meets_cora type=work day=101]
label day101_2_missy_meets_cora:

    # [ASSET] Visual/staging command
    scene bg_laundry_room_day:
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with fade

    "The laundry room is heat, lye, damp cotton, and women trying not to cough."
    "Steam beads on the walls. It turns every face soft at the edges."

    # [ASSET] Visual/staging command
    show missy_sprite smiling at right_full_body

    missy "You must be Cora. The new girl Miss Stern was sorting out."
    # [ASSET] Visual/staging command
    show cora_sprite base_travel at left_full_body
    with moveinleft

    cora "I must be. Cora Vale."

    missy "I'm Missy. Miss Stern said I'm to show you where things go. {w}Not everything, mind."
    missy "If I showed you everything we'd both be dismissed and out on the Strand before tea. This place has more rules than the Bible, and twice as many ways to fall."

    cora_inner "She says it brightly, but there is a sharp, quiet calculation in the way she eyes the door."
    cora_inner "Not simple chatter. A junior maid who has calculated the cost of a single slip."

    cora "Is the work always this warm?"
    # [ASSET] Visual/staging command
    show cora_sprite collar_travel at left_full_body
    with dissolve
    missy "Oh, this is a pleasant day. Wait until the boilers sulk and the head laundress starts counting the soap-bars like they're gold sovereigns."

    "Missy laughs at her own warning, though her eyes remain alert, and she presses a folded stack of garments into my arms."

    missy "These go up by the guest corridor. Not the grand staircase, obviously. Servants' passage only. We're to be like ghosts, Cora. Hands without noise."
    missy "And don't look too closely at anything left outside a door. Guests hate being known. And what they hate, they punish."

    cora_inner "Guests hate being known."
    cora_inner "A remarkably sharp decoding of the hotel's lethal hierarchy."

    cora "I'll remember. Discretion first."

    "Missy studies me for a second longer than comfort allows, her gaze parsing my apron, my cap, and the country stiffness I haven't quite washed off."

    missy "You looked pale out there. Miss Stern does that to a girl. She makes everyone feel as if they've violated the commandments just by breathing the air."

    cora "Have you?"

    missy "What?"

    cora "Violated the commandments. Or stolen spoons."

    missy "Certainly not. A girl's virtue and her honesty are the only shields she has in London. Lose either, and you're under the carriage wheels."

    "She hesitates, a small, knowing crease appearing between her brows."

    missy "Well. There was a silver spoon Miss Stern threw out because the silver-plate was peeling and it looked improper for the suites. I kept it to stir my tea. But that's salvage, not sin."

    missy "And where are you from, Cora? Your papers say Wiltshire."

    cora "A small village. Near Fovant."

    "Missy's eyes light up with sudden, beautiful, and terrifying recognition."

    missy "Wiltshire! Oh, bless you, I'm from Hindon myself! Just three miles down the road!"
    missy "You must know the old oak by the mill? And the curate, Mr. Harrison? He has the most wonderful, proper sermons on Sundays."

    cora_inner "My heart stops. A physical blow to my chest."
    cora_inner "She is the real thing—the innocent, pious English country girl I am pretending to be."
    cora_inner "If I slip now, if I name the wrong lane or mispronounce the local grange, she will know. And her concern will destroy me."

    cora "The old mill is quite beautiful in spring, Missy."
    cora "We lived closer to the parish line."
    cora "We did not often travel to Hindon."

    missy "Ah, that's a pity. The curate's wife was always so good to the girls in service. Such a righteous place."

    cora_inner "The irony is a cold weight. Missy is the very life I claimed to have lived, purely to get this position."
    cora_inner "We are two halves of a lie, and she has no idea she is holding the knife."
    cora_inner "I almost like her immediately. Her country armor is thicker than mine, but she knows exactly where the joints are."

    # [STATE] State/progression update
    jump day101_2_coras_path_choice


# ==========================================
# 012 - CORA'S PATH CHOICE
# ==========================================

# [DAG_NODE id=day101_2_coras_path_choice type=choice]
label day101_2_coras_path_choice:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_dim:
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with fade

    "The servants' corridor behind the guest wing is narrower than it should be."
    "The walls carry sound the way a body carries fever."

    # [ASSET] Visual/staging command
    show missy_sprite smiling at centre_bust

    missy "This way. Mind the third board. It complains, and Miss Stern hears every creak."

    "We pass a service door near the Master Suite."
    "Beyond it: a sharp sound."
    "Not a dropped tray."
    "Not a broken glass."
    "A voice pressed low, carrying a rhythmic, trembling weight."

    vance "Please. I understand. I do."

    # [ASSET] Visual/staging command
    show missy_sprite shocked at left_bust

    missy "Was that Miss Vance? She sounds... she doesn't sound proper."

    "Another sound follows. Smaller. A wet gasp."
    "Missy goes absolutely still, her fingers tightening around the wicker hamper."

    missy "If she's in distress... we ought to fetch Miss Stern. Or is it improper for us to interfere?"

    cora_inner "This is the moment."
    cora_inner "Not the sound. Not Vance's voice. Not Mr. Locke's hand, if it was his hand."
    cora_inner "The moment is the choice of what I become in order to use it."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day101_2_coras_path_choice_menu_1]
    menu:
        "How do I take the material?"

        "Let Missy's concern open the door. [[Predator path]]":

            # [STATE] Semantic balance profile: Cora weaponises Missy's concern for material
            $ apply_balanced_effect("predatory", intensity="standard", witness="vance")
            $ story.set_corridor_state("predator")
            $ apply_archetype_edge("predator", 1)

            cora "You may be right. If she's hurt, someone should check. But you know the house, Missy—if I open the wrong door on my first day, Miss Stern will have my references."
            
            cora_inner "I use her genuine moral concern as a shield."
            cora_inner "It is a calculated argument, and her sharp, protective instinct for other maids makes her accept the risk."

            missy "Only a little look, then. Only to ensure she isn't in peril."

            "She steps toward the service door, her posture cautious, her movements deliberate."
            "I step back into the shadow."
            cora_inner "Missy's hand reaches the latch. Her decency does the work my hunger asks of it."

            "Through the narrow opening, the room is revealed in fragments: Vance's white hand on dark carpet; the master's polished shoe; the silver head of his walking stick resting against his knee."
            "Missy gasps, her observant eyes taking in the transgressive tableau before her."

            gideon "The door."

            "Missy pulls it shut so fast the latch bites, her face white with immediate self-defense."

            missy "Oh. Oh, Cora. That was... he was holding her. Like she was a dog."

            cora "We saw nothing."

            "I say it to soothe her, but she is already retreating, her defensive propriety locking down like iron."
            cora_inner "I have seen enough. And I have used her to get it."

            # [STATE] State/progression update
            $ story.set_missy_day1_trust_state("unsettled")

        "Look for myself. [[Prey path]]":

            # [STATE] Semantic balance profile: Cora takes direct corridor risk for the image
            $ apply_balanced_effect("reckless", intensity=1.4, witness="vance")
            $ story.set_corridor_state("prey")
            $ apply_archetype_edge("prey", 1)

            cora "Stay there. Let me see."
            missy "Cora, no—it's sin to pry into the suites."
            cora "Quiet."

            "I move before caution can catch me."
            "The third board complains exactly as promised."

            "Through the crack I see Vance kneeling, face lifted in a desperate mix of fury and submission."
            "Mr. Locke holds her chin between two fingers, his grip light but absolute."

            gideon "Again."

            vance "I forgot myself, Sir."

            "My breath catches."
            "His eyes move toward the door with terrifying speed."

            gideon "Do we have an audience?"

            "I stumble back, my pulse hammering."
            "Missy's hand is already on my sleeve, her sharp instincts dragging me into the bend of the corridor before the latch can turn."

            missy "Have you lost your senses? If Mr. Locke sees us prying, we'll be ruined!"

            "She is terrified, but her rescue was swift and observant."
            cora_inner "I have the image. The terrible, beautiful image."

            # [STATE] State/progression update
            $ story.set_missy_day1_trust_state("shared_caution")

        "Pull Missy away. [[Ghost path]]":

            # [STATE bespoke] Multi-witness suspicion reduction; cannot map to one profile
            $ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5, insp=10, corr=0)
            $ story.set_corridor_state("ghost")
            $ apply_archetype_edge("ghost", 1)

            cora "No. We walk on."
            missy "But if she's in peril—"
            cora "If she is, Miss Stern already knows, or she has chosen to look away. Either way, simple maids are not the cure. We only get crushed in the door."

            "That silences her. Her sharp intellect recognizes the brutal logic."
            "I take her by the wrist and keep walking, our pace quick and quiet."

            "Behind us, Vance says something too low to catch. Mr. Locke answers with a quietness worse than anger."
            cora_inner "I collect the rhythm. The pause. The absolute yielding."
            cora_inner "A writer does not always need the picture."
            cora_inner "Sometimes the wall tells the truer story."

            # [STATE] State/progression update
            $ story.set_missy_day1_trust_state("soothed")

    # [ASSET] Visual/staging command
    hide missy_sprite

    jump day101_3_taking_stock_day1


# ==========================================
# 013 - TAKING STOCK DAY 1
# ==========================================

# [DAG_NODE id=day101_3_taking_stock_day1 type=work day=101]
label day101_3_taking_stock_day1:

    # [STATE] State/progression update
    $ set_time_period("Evening")

    call day101_evening_consequence_window

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk:
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with fade

    "By twilight my room has become mine in the meanest possible sense."
    "A narrow bed. A washbasin. A peg for the uniform. A desk too small for ambition."
    "Still, there is a door."
    "There is a candle."
    "There is paper."

    # [STATE] State/progression update
    $ show_ledger_ui()

    cora_inner "I open my ledger, the ink wet, and record the day's useful damages."

    if story.day1_corridor_state == "predator":
        cora_inner "Missy's shocked, wounded face returns first. I used her decency as a blunt instrument."
        cora_inner "Then Vance's hand on the carpet. Mr. Locke's shoe. The walking stick."
        cora_inner "The sentence looks uglier once written down, but it is real."

    elif story.day1_corridor_state == "prey":
        cora_inner "I can still feel the corridor board shift beneath my shoe."
        cora_inner "Mr. Locke had almost seen me."
        cora_inner "No. Not almost."
        cora_inner "He saw enough to wonder."

    else:
        cora_inner "The wall gave me less than my hunger wanted and more than my safety deserved."
        cora_inner "A voice can kneel."
        cora_inner "I had not known that before today."

    # [STATE] State/progression update
    $ _dominant = get_dominant_archetype()
    if _dominant == "ghost":
        cora_inner "My style is emerging as that of the unseen observer. A ghost, moving through the Savoy's gaps."
    elif _dominant == "prey":
        cora_inner "I survive here by reading threat and adapting. Tactically yielding, like prey that lives to run."
    elif _dominant == "predator":
        cora_inner "I find myself looking for leverage. I will bait them, test their lines, and feed on their secrets."

    # [STATE] State/progression update
    call day101_night_story_window

    # [STATE] State/progression update
    jump day102_1_cora_missy_first_shift


# [DAG_NODE id=day101_night_story_window type=dynamic_window day=101 period=Night window=story_chain returns_to=day101_3_taking_stock_day1]
label day101_night_story_window:

    # [STATE] State/progression update
    $ set_time_period("Night")

    call story_window_penance_gate("day101_night")
    if _penance_consumed:
        return

    # [CHOICE] Decision point - combined Evening / Night choice
    # [DAG_CHOICE group=day101_night_story_window_menu_1]
    menu:
        "I look at my journal, the ink drying on the page. The lay of the land is clear. How do I spend the night?"

        "Write the first chapter of my manuscript. [[Progress manuscript]]" if has_story_fuel(*WRITE_GATE_CH1):

            # [STATE] State/progression update
            call day101_4_write_the_chapter

        "Listen for Miss Stern's keys in the west corridor." if story.chain_available("stern"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("stern")
            call expression _chain_label

        "Find Missy before the laundry goes cold." if story.chain_available("missy"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("missy")
            call expression _chain_label

        "Walk the guest wing where Mr. Locke's shoe still has authority." if story.chain_available("vance"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("vance")
            call expression _chain_label

        "Stay at the desk and let the ink dry. [[Rest and reflect]]":

            # [CHOICE] Choose reflection discipline
            # [DAG_CHOICE group=day101_3_taking_stock_day1_menu_2]
            menu:
                "Which discipline keeps my hands steady?"

                "Order. Safety in structure. [[Creative discipline]]":

                    # [STATE] Semantic balance profile: Cora orders the ledger into structure
                    $ apply_balanced_effect("creative", intensity="major")
                    $ story.set_day1_ledger_focus("inspiration")

                    cora_inner "I draw three columns in the ledger."
                    cora_inner "Command. Witness. Consequence."

                    cora_inner "The shape of the scene matters more than the appetite of it."
                    cora_inner "A woman attacks downward because she cannot attack upward. A man corrects her, not from kindness, but ownership. A servant sees and becomes dangerous."

                    cora_inner "That is a story."
                    cora_inner "Not a confession."
                    cora_inner "Not yet."

                "Exposure. Safety in knowing the threat. [[Transgressive discipline]]":

                    # [STATE] Semantic balance profile: Cora writes want instead of structure
                    $ apply_balanced_effect("transgressive", intensity="standard", witness="vance")
                    $ story.set_day1_ledger_focus("corruption")

                    cora_inner "I try to write command, witness, consequence."
                    cora_inner "My hand writes want."

                    cora_inner "Not simply Vance's."
                    cora_inner "That would be easier. Cleaner."

                    cora_inner "I think of the way she yielded and hated him for making her yield."
                    cora_inner "I think of Missy reaching for the latch because I placed fear in her hand and called it concern."
                    cora_inner "I think of myself outside the door, starved for the next sound."

                    cora_inner "The ledger does not forgive me."
                    cora_inner "It records beautifully."

            # [STATE] Semantic balance profile: Reflection consolidates the day's observations
            $ apply_balanced_effect("observant", intensity="standard")

    return


# [DAG_NODE id=day101_evening_consequence_window type=dynamic_window day=101 period=Evening window=consequence penance=true returns_to=day101_3_taking_stock_day1]
label day101_evening_consequence_window:
    # Watch-only: penance consumes the night story-chain window, not this slot
    call watch_suspicion
    return


# ==========================================
# 014 - WRITE THE CHAPTER
# ==========================================

# [DAG_NODE id=day101_4_write_the_chapter type=write]
label day101_4_write_the_chapter:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night:
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with dissolve

    # [STATE] This is the main Day 1 manuscript progression route
    $ story.set_day1_night_action("write")

    # [CHOICE] Choose writing framing
    # [DAG_CHOICE group=day101_4_write_the_chapter_menu_1]
    menu:
        "How do I frame the first chapter of my novel?"

        "Frame it with order and structure. I must write what is safe. [[Creative framing]]":

            # [STATE] Semantic balance profile: Cora frames the chapter with structure
            $ apply_balanced_effect("creative", intensity="major")
            $ story.set_day1_ledger_focus("inspiration")

            cora_inner "I draw three columns in the ledger and let the structure guide my hand."
            cora_inner "The shape of the scene matters more than the appetite of it."
            cora_inner "A woman attacks downward because she cannot attack upward. A man corrects her, not from kindness, but ownership."

        "Frame it with exposure and appetite. I must write the truth. [[Transgressive framing]]":

            # [STATE] Semantic balance profile: Cora frames the chapter with appetite
            $ apply_balanced_effect("transgressive", intensity="standard", witness="vance")
            $ story.set_day1_ledger_focus("corruption")

            cora_inner "I try to write command, witness, consequence, but my hand writes want."
            cora_inner "I think of the way she yielded and hated him for making her yield."
            cora_inner "I think of Missy reaching for the latch because I placed fear in her hand."

    cora_inner "The first sentence arrives like a servant entering the wrong room: terrified, many-layered, and unable to retreat."

    if story.day1_corridor_state == "predator":

        cora_inner "I write a maid who learns that innocence is not a virtue."
        cora_inner "It is a tool left unattended."
        cora_inner "She places a sweeter girl before a dangerous door and discovers that guilt has a taste."

        if story.day1_ledger_focus == "corruption":
            cora_inner "In the chapter, the maid does not apologise."
            cora_inner "She improves."
        else:
            cora_inner "In the chapter, the maid understands the cost and writes it down anyway."

    elif story.day1_corridor_state == "prey":

        cora_inner "I write a maid who looks through a forbidden crack and is seen looking."
        cora_inner "The gentleman does not shout. He invites her closer."
        cora_inner "That is worse."

        if story.day1_ledger_focus == "corruption":
            cora_inner "On the page, fear and invitation become difficult to separate."
        else:
            cora_inner "On the page, the danger remains danger. The heat is only evidence."

    else:

        cora_inner "I write a maid who never sees the room."
        cora_inner "Only the wall. Only the voice. Only the terrible grammar of command and reply."
        cora_inner "Her ignorance becomes precision."

        if story.day1_ledger_focus == "corruption":
            cora_inner "She imagines too much and tells herself imagination is not participation."
        else:
            cora_inner "She understands that distance can sharpen a knife."

    cora_inner "By the time the candle gutters, there are pages."
    cora_inner "Not a chapter. Not a wound. Not even a proper lie."

    if player.corruption_level <= WRITE_SLOP_MAX_CORRUPTION_LEVEL:
        call book1_write_chapter(chapter_key="day1_slop_chapter", current_day=101)
        cora_inner "Flavorless slop."
        cora_inner "Unsellable, bloodless, afraid of its own pulse."
        cora_inner "I had inspiration, but no appetite, and the page told on me."
    else:

        # [STATE] State/progression update
        $ story.complete_manuscript_chapter("day1_chapter")
        call book1_write_chapter(chapter_key="day1_chapter", current_day=101)
        cora_inner "There is a shape worth keeping, but it still feels premature."
        cora_inner "Tomorrow's material will decide whether this becomes a chapter or kindling."

    # [STATE bespoke] Fixed write spend; negative inspiration not profile-scaled
    $ apply_effects(insp=-10, corr=0)

    cora_inner "I press the pages flat beneath the ledger."
    cora_inner "Tomorrow the house will expect a maid."
    cora_inner "Tonight it acquired a failed first draft."

    return


