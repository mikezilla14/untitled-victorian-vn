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


label day101_main:

    # [BEAT] Narrator's intro. Keep brief; the horror pressure comes from Cora being trapped in procedure
    scene bg_savoy_corridor_morning:
        zoom 1.0
        xysize (1920,1080)

    # [ASSET] Visual/staging command
    with fade

    cora_inner "The Savoy Hotel did not welcome girls like me."
    cora_inner "It consumed them quietly, polished the brass after, and called the result service." # menace is a bit opaque can be rewritten
    cora_inner "I had forged my references with a steady hand. I had not accounted for the waiting."

    # [STATE] State/progression update
    jump day101_1_cora_waiting


# ==========================================
# 011 - CORA WAITING
# ==========================================

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

    cora_inner "I stand outside Miss Stern's office with my hands folded and my pulse behaving badly."
    
    "Behind the heavy mahogany door, a clock ticks with paid machinery." # sound effect?
    
    cora_inner "My references sit in my apron pocket." # camera?
    cora_inner "Good paper. Good ink. Better lies."

    "A maid passes carrying towels white enough to blind. A footman steps past with a silver tray." # silohuette image? 

    cora_inner "No one asks who I am."
    cora_inner "That is the first rule of this place, then. Be useful enough to ignore."

    stern "Enter." 

    # [STATE] State/progression update
    jump day101_1_morning_interview


# ==========================================
# 011 - MORNING INTERVIEW
# ==========================================

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
    stern "You have worked in service before."

    cora_inner "The lie is waiting for me, neat as a folded sheet."

    cora "Yes, Ma'am. In the country."

    stern "The country forgives slowness. The Savoy does not."
    stern "A maid in this house is hands without noise, feet without weight, and memory without a tongue."
    stern "Can you be that?"

    # [CHOICE] Decision point
    # This choice currently does not affect story progress there should be tie in to a future narrative flow or remove the flag and ekep the stat changes

    # [CHOICE] Decision point
    menu:
        "How do I survive Stern's inspection?" 

        "Lower my eyes. Let her mistake fear for obedience.":

            # [STATE] Low-risk survival posture. Cora hides sharpness, but the performance costs dignity
            $ apply_effects(stern_susp=5, insp=5, corr=0)
            $ story.set_day1_interview_state("meek")

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

            # [STATE] Efficient but conspicuous. Stern notices a mind behind the apron
            $ apply_effects(stern_susp=15, insp=10, corr=0)
            $ story.set_day1_interview_state("competent")

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

    stern "You will report to the laundry first. Missy will show you the necessary route."
    stern "You will not wander. You will not question guests. You will not cultivate opinions."

    cora_inner "Too late for that."

    stern "And if a guest drops something, breaks something, or throws something, you will retrieve it without expression."

    # [ASSET] Visual/staging command
    hide stern_sprite

    jump day101_1_vance_throws_toy


# ==========================================
# 011 - VANCE THROWS TOY
# ==========================================

label day101_1_vance_throws_toy:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning:
        zoom 1.00
        xysize (1920,1080)

    # [ASSET] Visual/staging command
    with dissolve

    "The corridor outside Stern's office is all gloss and restraint."
    "Then something small and silver strikes the skirting board and spins across the carpet."

    # [ASSET] Visual/staging command
    show vance_sprite angry at right_full_body:
        xalign 0.6
        yalign 1.1
        zoom 0.8

    vance "Useless creature. I said the blue ribbon, not that vulgar little thing." # this needs rewriting this would be in the lobby it currently makes no sense for her to be standing around shouting about a ribbon.

    "The object stops near my shoe. A lady's trinket. Too expensive to be called a toy, too childish to be called anything else." # change or cut this, this is vestigial dialogue from a previous draft where the llm used the prompt of throwing toys literally
    
    vance "You. Girl. Pick it up." # like this performative cruelty but needs better context

    # [ASSET] Visual/staging command
    show cora_sprite base_travel at left_full_body:
        yalign 1.0
        xalign 0.2
        zoom 0.75

    # [ASSET] Visual/staging command
    with moveinleft

    "Her voice lands on me before her eyes do."
    "Velvet. Pearls. A face arranged for admiration and currently sharpened for harm."

    cora "Yes, Miss."

    "I bend. I retrieve the little silver thing. I do not let my fingers tremble." # take a beat during this to allow the moment to breath and build suspense

    vance "Not like that. Have you never handled anything delicate?" # tone is great but detail needs to be polished with the new context.

    cora_inner "I have handled hunger. Debt. Ink. Men's hands where they were not invited." # take a beat here to let it land
    cora_inner "I decide not to list them."

    # [ASSET] Visual/staging command
    show gideon_sprite cold at right_full_body:
        xalign 0.8
        yalign 1.0
        zoom 0.8
        

    gideon "Vance."

    # [ASSET] Visual/staging command
    hide vance_sprite angry
    # [ASSET] Visual/staging command
    hide cora_sprite base_travel
    # [ASSET] Visual/staging command
    show cora_sprite base_travel at left_bust:
        yalign 1.0
        xalign 0.2

    # [ASSET] Visual/staging command
    with dissolve
    # [ASSET] Visual/staging command
    show vance_sprite submissive at left_bust:
        xalign 0.5
        xzoom -1.0

    # [ASSET] Visual/staging command
    with dissolve
    # [ASSET] Visual/staging command
    show gideon_sprite at right_bust:
        zoom 1
        xalign 0.75

    # [ASSET] Visual/staging command
    with dissolve
            

    cora_inner "One word." # maybe show cora sprite with speech bubble here
    cora_inner "The corridor changes temperature."

    vance "I was only correcting her..."

    gideon "You were making yourself visible."


    "Vance's mouth closes." # hopefully the sprite change can tell this story and we can cut some of this narration
    "The fury does not vanish. It folds itself away, obedient and practiced."

    gideon "The girl is new. Do not teach her bad habits before luncheon."

    vance "Of course."

    cora_inner "Of course. Not yes. Not sorry. Of course." # this should be stronger or cut
    cora_inner "As if obedience were not surrender, but etiquette."

    gideon "Your name?"

    cora "Cora, Sir."

    gideon "Then learn quickly, girl. This house rewards discretion."

    cora_inner "He does not threaten me." # meh
    cora_inner "That is why it feels like one."

    # [ASSET] Visual/staging command
    hide gideon_sprite
    # [ASSET] Visual/staging command
    hide vance_sprite

    cora_inner "Vance follows him down the corridor, all silk and swallowed rage."
    cora_inner "I watch only long enough to know the shape of it." # meh maybe?
    cora_inner "A command. A yielding. A room full of people pretending not to notice."
    cora_inner "There is a chapter in that."

    # [STATE] State/progression update
    jump day101_2_missy_meets_cora


# ==========================================
# 012 - MISSY MEETS CORA
# ==========================================
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

    cora_inner "I almost like her immediately. Her country armor is thicker than mine, but she knows exactly where the joints are."

    # [STATE] State/progression update
    jump day101_2_coras_path_choice


# ==========================================
# 012 - CORA'S PATH CHOICE
# ==========================================

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
    menu:
        "How do I take the material?"

        "Let Missy's concern open the door. [[Predator path: +Inspiration, +Corruption]]":

            # [STATE] Cora weaponises plausible concern. Safer physically, morally worse
            $ apply_effects(insp=10, corr=5)
            $ story.set_corridor_state("predator")

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

        "Look for myself. [[Prey path: +Inspiration, +Suspicion]]":

            # [STATE] Cora takes the direct risk. Most dangerous path; strongest sensory material
            $ apply_effects(vance_susp=35, insp=15, corr=5)
            $ story.set_corridor_state("prey")

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

        "Pull Missy away. [[Ghost path: +Inspiration, -Suspicion]]":

            # [STATE] Cora refuses exposure, keeps the observation abstract, and preserves cover
            $ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5, insp=10, corr=0)
            $ story.set_corridor_state("ghost")

            cora "No. We walk on."
            missy "But if she's in peril—"
            cora "If she is, Miss Stern already knows, or she has chosen to look away. Either way, simple maids are not the cure. We only get crushed in the door."

            "That silences her. Her sharp intellect recognizes the brutal logic."
            "I take her by the wrist and keep walking, our pace quick and quiet."

            "Behind us, Vance says something too low to catch. Mr. Locke answers with a quietness worse than anger."
            cora_inner "I collect the rhythm. The pause. The absolute yielding."
            cora_inner "A writer does not always need the picture."
            cora_inner "Sometimes the wall tells the truer story."

    # [ASSET] Visual/staging command
    hide missy_sprite

    jump day101_3_taking_stock_day1


# ==========================================
# 013 - TAKING STOCK DAY 1
# ==========================================

label day101_3_taking_stock_day1:

    # [STATE] State/progression update
    $ set_time_period("Evening")

    call check_confrontations

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

    cora_inner "I open the ledger and set down the day's useful damages."

    if story.day1_corridor_state == "predator":
        cora_inner "Missy's shocked face returns first."
        cora_inner "Then Vance's hand on the carpet. Mr. Locke's shoe. The walking stick."
        cora_inner "I used the girl because she was available."
        cora_inner "The sentence looks uglier once written down."

    elif story.day1_corridor_state == "prey":
        cora_inner "I can still feel the corridor board shift beneath my shoe."
        cora_inner "Mr. Locke had almost seen me."
        cora_inner "No. Not almost."
        cora_inner "He saw enough to wonder."

    else:
        cora_inner "The wall gave me less than my hunger wanted and more than my safety deserved."
        cora_inner "A voice can kneel."
        cora_inner "I had not known that before today."

    # [CHOICE] Decision point - combined Evening / Night choice
    menu:
        "I look at my journal, the ink drying on the page. The lay of the land is clear. How do I spend the night?"

        "Write the first chapter of my manuscript. [[Progress manuscript]]" if player.inspiration >= 15:

            # [STATE] State/progression update
            jump day101_4_write_the_chapter

        "Listen for Miss Stern's keys in the west corridor." if story.chain_available("stern"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("stern")
            jump expression _chain_label

        "Find Missy before the laundry goes cold." if story.chain_available("missy"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("missy")
            jump expression _chain_label

        "Walk the guest wing where Mr. Locke's shoe still has authority." if story.chain_available("vance"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("vance")
            jump expression _chain_label

        "Stay at the desk and let the ink dry. [[Rest and reflect]]":

            # [CHOICE] Choose reflection discipline
            menu:
                "Which discipline keeps my hands steady?"

                "Order. Safety in structure. [[Inspiration]]":

                    # [STATE] Inspiration focus
                    $ apply_effects(insp=15, corr=0)
                    $ story.set_day1_ledger_focus("inspiration")

                    cora_inner "I draw three columns in the ledger."
                    cora_inner "Command. Witness. Consequence."

                    cora_inner "The shape of the scene matters more than the appetite of it."
                    cora_inner "A woman attacks downward because she cannot attack upward. A man corrects her, not from kindness, but ownership. A servant sees and becomes dangerous."

                    cora_inner "That is a story."
                    cora_inner "Not a confession."
                    cora_inner "Not yet."

                "Exposure. Safety in knowing the threat. [[Corruption]]":

                    # [STATE] Corruption focus
                    $ apply_effects(vance_susp=5, insp=5, corr=10)
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

            # [STATE] Apply final reflection effects and end the slot
            $ apply_effects(insp=10, corr=0)
            call end_slot(outcome="d1_reflect_done")


# ==========================================
# 014 - WRITE THE CHAPTER
# ==========================================

label day101_4_write_the_chapter:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night:
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with dissolve

    # [STATE] This is the main Day 1 manuscript progression route
    $ story.set_day1_night_action("write")

    # [CHOICE] Choose writing framing
    menu:
        "How do I frame the first chapter of my novel?"

        "Frame it with order and structure. I must write what is safe. [[Inspiration]]":

            # [STATE] Inspiration choice
            $ apply_effects(insp=15, corr=0)
            $ story.set_day1_ledger_focus("inspiration")

            cora_inner "I draw three columns in the ledger and let the structure guide my hand."
            cora_inner "The shape of the scene matters more than the appetite of it."
            cora_inner "A woman attacks downward because she cannot attack upward. A man corrects her, not from kindness, but ownership."

        "Frame it with exposure and appetite. I must write the truth. [[Corruption]]":

            # [STATE] Corruption choice
            $ apply_effects(vance_susp=5, insp=5, corr=10)
            $ story.set_day1_ledger_focus("corruption")

            cora_inner "I try to write command, witness, consequence, but my hand writes want."
            cora_inner "I think of the way she yielded and hated him for making her yield."
            cora_inner "I think of Missy reaching for the latch because I placed fear in her hand."

    cora_inner "The first sentence arrives like a servant entering the wrong room: terrified, necessary, unable to retreat."

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

    if player.corruption_level < 30:
        call book1_write_chapter(chapter_key="day1_slop_chapter", current_day=101)
        cora_inner "Flavorless slop."
        cora_inner "Unsellable, bloodless, afraid of its own pulse."
        cora_inner "I had inspiration, but no appetite, and the page told on me."
    else:
        call book1_write_chapter(chapter_key="day1_chapter", current_day=101)
        cora_inner "There is a shape worth keeping, but it still feels premature."
        cora_inner "Tomorrow's material will decide whether this becomes a chapter or kindling."

    # [STATE] State/progression update
    $ apply_effects(insp=-10, corr=0)

    cora_inner "I press the pages flat beneath the ledger."
    cora_inner "Tomorrow the house will expect a maid."
    cora_inner "Tonight it acquired a failed first draft."

    # [STATE] State/progression update
    call end_slot(outcome="d1_write_ch1")


