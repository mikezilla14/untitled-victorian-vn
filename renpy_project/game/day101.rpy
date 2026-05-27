# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes

# day101.rpy
# Release 1 / Day 01
# Source intent: rewritten from Twine node map and existing Day 1 script.
# Asset constraint: uses only assets already present in the supplied Day 1 Ren'Py draft.

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
    scene bg_savoy_corridor_morning
    with fade

    "The Savoy Hotel did not welcome girls like me."
    "It consumed them quietly, polished the brass after, and called the result service."
    "I had forged my references with a steady hand. I had not accounted for the waiting."

    # [STATE] State/progression update
    jump day101_1_cora_waiting


# ==========================================
# 011 - CORA WAITING
# ==========================================

label day101_1_cora_waiting:

    # [ASSET] Existing Day 1 corridor background
    scene bg_savoy_corridor_morning
    with dissolve
    # full body standing sprite of Cora would be ideal here, but we can use the cap sprite and describe the rest in text for now
    "I stand outside Miss Stern's office with my hands folded and my pulse behaving badly."
    "Behind the door, a clock ticks with the smug confidence of paid machinery." #add sound effect?
    "My references sit in my apron pocket." #camera pan to apron pocket?
    "Good paper. Good ink. Better lies." #pan up to face?

    "A maid passes without looking at me. Then a footman. Then another maid carrying towels white enough to make sin feel visible." 
    #show sprite silhouettes of passing servants, but keep them indistinct to preserve the focus on Cora's internal experience
    # The point of this beat is to establish the social invisibility of maids in the hotel, and to contrast it with Cora's heightened self-awareness and anxiety. The passing servants should feel like a blur of activity that Cora is hyper-aware of, but that they are oblivious to her.
    "No one asks who I am."
    "That is the first rule of this place, then: be useful enough to ignore."

    stern "Enter."

    # [STATE] State/progression update
    jump day101_1_morning_interview


# ==========================================
# 011 - MORNING INTERVIEW
# ==========================================

label day101_1_morning_interview:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning
    with dissolve

    show stern_sprite neutral at center:
        zoom 0.35

    "Miss Stern stands rather than sits."
    "It is not courtesy. It is measurement."
    "Her eyes move from my cap to my boots, weighing every inch for disobedience."

    stern "Cora Vale."
    cora "Yes, Ma'am."
    stern "You have worked in service before."

    "The lie is waiting for me, neat as a folded sheet."

    cora "Yes, Ma'am. In the country."

    stern "The country forgives slowness. The Savoy does not."
    stern "A maid in this house is hands without noise, feet without weight, and memory without a tongue."
    stern "Can you be that?"

    # [CHOICE] Decision point
    menu:
        "How do I survive Stern's inspection?"

        "Lower my eyes. Let her mistake fear for obedience.":

            # [STATE] Low-risk survival posture. Cora hides sharpness, but the performance costs dignity
            $ apply_effects(stern_susp=5, insp=5, corr=0)
            $ story.set_day1_interview_state("meek")

            cora "I can, Ma'am. I only wish to work hard."
            stern "Wishing is for girls with leisure. You will work because you are told."
            cora "Yes, Ma'am."

            "She hears a dull country girl."
            "Good. Let the woman keep that version of me."

        "Answer cleanly. Let competence do what meekness cannot.":

            # [STATE] Efficient but conspicuous. Stern notices a mind behind the apron
            $ apply_effects(stern_susp=15, insp=10, corr=0)
            $ story.set_day1_interview_state("competent")

            cora "I can be quiet, quick, and exact. If I err, it will not be from carelessness."
            stern "Exact?"
            cora "Yes, Ma'am."
            stern "A dangerous word from a girl in a borrowed apron."

            "There."
            "She sees it. Not all of it, but enough to dislike me."

    stern "You will report to the laundry first. Missy will show you the necessary route."
    stern "You will not wander. You will not question guests. You will not cultivate opinions."

    "Too late for that."

    stern "And if a guest drops something, breaks something, or throws something, you will retrieve it without expression."

    # [ASSET] Visual/staging command
    hide stern_sprite

    jump day101_1_vance_throws_toy


# ==========================================
# 011 - VANCE THROWS TOY
# ==========================================

label day101_1_vance_throws_toy:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning
    with dissolve

    "The corridor outside Stern's office is all gloss and restraint."
    "Then something small and silver strikes the skirting board and spins across the carpet."

    # [ASSET] Visual/staging command
    show vance_sprite angry at left:
        zoom 0.35

    vance "Useless creature. I said the blue ribbon, not that vulgar little thing."

    "The object stops near my shoe. A lady's trinket. Too expensive to be called a toy, too childish to be called anything else."

    vance "You. Girl. Pick it up."

    "Her voice lands on me before her eyes do."
    "Velvet. Pearls. A face arranged for admiration and currently sharpened for harm."

    cora "Yes, Miss."

    "I bend. I retrieve the little silver thing. I do not let my fingers tremble."

    vance "Not like that. Have you never handled anything delicate?"

    "I have handled hunger. Debt. Ink. Men's hands where they were not invited."
    "I decide not to list them."

    # [ASSET] Visual/staging command
    show gideon_sprite cold at right

    gideon "Vance."

    "One word."
    "The corridor changes temperature."

    vance "I was only correcting her."

    gideon "You were making yourself visible."

    # [ASSET] Visual/staging command
    show vance_sprite submissive at left

    "Vance's mouth closes."
    "The fury does not vanish. It folds itself away, obedient and practiced."

    gideon "The girl is new. Do not teach her bad habits before luncheon."

    vance "Of course."

    "Of course. Not yes. Not sorry. Of course."
    "As if obedience were not surrender, but etiquette."

    gideon "Your name?"

    cora "Cora, Sir."

    gideon "Then learn quickly, girl. This house rewards discretion."

    "He does not threaten me."
    "That is why it feels like one."

    # [ASSET] Visual/staging command
    hide gideon_sprite
    hide vance_sprite

    "Vance follows him down the corridor, all silk and swallowed rage."
    "I watch only long enough to know the shape of it."
    "A command. A yielding. A room full of people pretending not to notice."
    "There is a chapter in that."

    # [STATE] State/progression update
    jump day101_2_missy_meets_cora


# ==========================================
# 012 - MISSY MEETS CORA
# ==========================================

label day101_2_missy_meets_cora:

    # [ASSET] Visual/staging command
    scene bg_laundry_room_day
    with fade

    "The laundry room is heat, lye, damp cotton, and women trying not to cough."
    "Steam beads on the walls. It turns every face soft at the edges."

    # [ASSET] Visual/staging command
    show missy_sprite smiling at center

    missy "You must be Cora."
    cora "I must be."

    missy "I'm Missy. Miss Stern said I'm to show you where things go. Not everything, mind. If I showed you everything we'd both be dead before tea."

    "She says it brightly."
    "That is the alarming part."

    cora "Is the work always this warm?"
    missy "Oh, this is a pleasant day. Wait until the boilers sulk."

    "Missy laughs at her own warning and presses a folded stack of garments into my arms."

    missy "These go up by the guest corridor. Not the grand staircase, obviously. Servants' passage only."
    missy "And don't look too closely at anything left outside a room. Guests hate being known."

    "Guests hate being known."
    "Writers have built whole careers on less."

    cora "I'll remember."

    "Missy studies me for a second longer than comfort allows."

    missy "You looked pale out there. Stern does that. She makes everyone feel like they've stolen spoons."

    cora "Have you?"

    missy "What?"

    cora "Stolen spoons."

    missy "No."

    "She hesitates."

    missy "Well. One, once. But it was bent."

    "I almost like her immediately. That is inconvenient."

    # [STATE] State/progression update
    jump day101_2_coras_path_choice


# ==========================================
# 012 - CORA'S PATH CHOICE
# ==========================================

label day101_2_coras_path_choice:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_dim
    with fade

    "The servants' corridor behind the guest wing is narrower than it should be."
    "The walls carry sound the way a body carries fever."

    # [ASSET] Visual/staging command
    show missy_sprite smiling at center

    missy "This way. Mind the third board. It complains."

    "We pass a service door near the Master Suite."
    "Beyond it: a sharp sound."
    "Not a dropped tray."
    "Not a broken glass."

    vance "Please. I understand. I do."

    # [ASSET] Visual/staging command
    show missy_sprite shocked at left

    missy "Was that Miss Vance?"

    "Another sound follows. Smaller. Wetter."
    "Missy goes still."

    missy "Should we fetch Miss Stern?"

    "This is the moment."
    "Not the sound. Not Vance's voice. Not Mr. Locke's hand, if it was his hand."
    "The moment is the choice of what I become in order to use it."

    # [CHOICE] Decision point
    menu:
        "How do I take the material?"

        "Let Missy's concern open the door. [[Predator path: +Inspiration, +Corruption]]":

            # [STATE] Cora weaponises plausible concern. Safer physically, morally worse
            $ apply_effects(insp=10, corr=5)
            $ story.set_corridor_state("predator")

            cora "You may be right. If she's hurt, someone should check."
            missy "Me?"
            cora "You know the house. If I open the wrong door on my first day, Stern will skin me."

            "It is a filthy argument because it is true."

            missy "Only a little look, then. Only to be sure."

            "She steps toward the service door."
            "I step back."
            "Missy's hand reaches the latch. Her innocence does the work my hunger asks of it."

            "Through the narrow opening, I glimpse only fragments: Vance's white hand on dark carpet; the master's polished shoe; the silver head of his walking stick resting against his knee."
            "Missy gasps."

            gideon "The door."

            "Missy pulls it shut so fast the latch bites."

            missy "Oh. Oh, Cora."

            cora "We saw nothing."

            "I say it for her benefit."
            "I have already seen enough."

        "Look for myself. [[Prey path: +Inspiration, +Suspicion]]":

            # [STATE] Cora takes the direct risk. Most dangerous path; strongest sensory material
            $ apply_effects(vance_susp=35, insp=15, corr=5)
            $ story.set_corridor_state("prey")

            cora "Stay there."
            missy "Cora—"
            cora "Quiet."

            "I move before caution can catch me."
            "The third board complains exactly as promised."

            "Through the crack I see Vance kneeling, face lifted in fury and need."
            "Mr. Locke holds her chin between two fingers, almost gently."

            gideon "Again."

            vance "I forgot myself, Sir."

            "My breath catches."
            "His eyes move to the door."

            gideon "Do we have an audience?"

            "I stumble back."
            "Missy grabs my sleeve and drags me into the bend of the corridor."

            missy "Have you lost your senses?"

            "Possibly."
            "But not the image. Never the image."

        "Pull Missy away. [[Ghost path: +Inspiration, -Suspicion]]":

            # [STATE] Cora refuses exposure, keeps the observation abstract, and preserves cover
            $ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5, insp=10, corr=0)
            $ story.set_corridor_state("ghost")

            cora "No."
            missy "But if she's hurt—"
            cora "Then Stern already knows, or Stern has chosen not to know. Either way, we are not the cure."

            "That silences her."
            "I take her by the wrist and keep walking."

            "Behind us, Vance says something too low to catch. The master answers with a quietness worse than anger."
            "I collect the rhythm. The pause. The obedience."
            "A writer does not always need the picture."
            "Sometimes the keyhole is less useful than the wall."

    # [ASSET] Visual/staging command
    hide missy_sprite

    jump day101_3_taking_stock_day1


# ==========================================
# 013 - TAKING STOCK DAY 1
# ==========================================

label day101_3_taking_stock_day1:

    call check_confrontations

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with fade

    "By twilight my room has become mine in the meanest possible sense."
    "A narrow bed. A washbasin. A peg for the uniform. A desk too small for ambition."
    "Still, there is a door."
    "There is a candle."
    "There is paper."

    # [STATE] State/progression update
    $ show_ledger_ui()

    "I open the ledger and set down the day's useful damages."

    if story.day1_corridor_state == "predator":
        "Missy's shocked face returns first."
        "Then Vance's hand on the carpet. Mr. Locke's shoe. The walking stick."
        "I used the girl because she was available."
        "The sentence looks uglier once written down."

    elif story.day1_corridor_state == "prey":
        "I can still feel the corridor board shift beneath my shoe."
        "Mr. Locke had almost seen me."
        "No. Not almost."
        "He saw enough to wonder."

    else:
        "The wall gave me less than my hunger wanted and more than my safety deserved."
        "A voice can kneel."
        "I had not known that before today."

    # [CHOICE] Decision point
    menu:
        "Which discipline keeps my hands steady?"

        "Order. Safety in structure. [[Inspiration]]":

            # [STATE] State/progression update
            jump day101_3_inspiration_choice

        "Exposure. Safety in knowing the threat. [[Corruption]]":

            # [STATE] State/progression update
            jump day101_3_corruption_choice


# ==========================================
# 013 - INSPIRATION CHOICE
# ==========================================

label day101_3_inspiration_choice:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with dissolve

    # [STATE] Cora processes the event as craft first. Cleaner path; supports writing
    $ apply_effects(insp=15, corr=0)
    $ story.set_day1_ledger_focus("inspiration")

    "I draw three columns in the ledger."
    "Command. Witness. Consequence."

    "The shape of the scene matters more than the appetite of it."
    "A woman attacks downward because she cannot attack upward. A man corrects her, not from kindness, but ownership. A servant sees and becomes dangerous."

    "That is a story."
    "Not a confession."
    "Not yet."

    # [STATE] State/progression update
    jump day101_3_optional_character_chain


# ==========================================
# 013 - CORRUPTION CHOICE
# ==========================================

label day101_3_corruption_choice:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with dissolve

    # [STATE] Cora accepts appetite as fuel. Higher future risk, stronger thematic contamination
    $ apply_effects(vance_susp=5, insp=5, corr=10)
    $ story.set_day1_ledger_focus("corruption")

    "I try to write command, witness, consequence."
    "My hand writes want."

    "Not simply Vance's."
    "That would be easier. Cleaner."

    "I think of the way she yielded and hated him for making her yield."
    "I think of Missy reaching for the latch because I placed fear in her hand and called it concern."
    "I think of myself outside the door, starved for the next sound."

    "The ledger does not forgive me."
    "It records beautifully."

    # [STATE] State/progression update
    jump day101_3_optional_character_chain


# ==========================================
# 013 - OPTIONAL CHARACTER CHAIN (DAY 1 EVENING)
# ==========================================

label day101_3_optional_character_chain:

    # [CHOICE] Contextual grind gate after ledger reflection; resolver picks chain beat
    menu:
        "The ledger is closed. One hour remains before the lamp must answer."

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

        "Stay at the desk and let the ink dry.":
            if story.day1_ledger_focus == "corruption":
                "I fold the page over the worst lines and pretend discipline can be borrowed from neat margins."
            else:
                "I copy the three columns again until my hand stops shaking."
            "The hotel watches less when I give it nothing to answer."

            # [STATE] State/progression update
            $ apply_effects(insp=10, corr=0)
            call end_slot(outcome="d1_reflect_done")


# ==========================================
# 014 - WRITING OR VISITING
# ==========================================

label day101_4_writing_or_visiting:

    call check_confrontations

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    "Night settles over the servants' quarters in layers."
    "Footsteps thin. Pipes mutter. Somewhere, a girl cries once and decides not to be heard again."

    "The candle waits on my desk."
    "So does the page."

    # [PROMOTION NOTE]
    # Replace this with the project-approved threshold helper.
    # The intent: Day 1 writing opens if the player has enough Inspiration/Corruption fuel.
    if has_story_fuel(15):

        # [CHOICE] Decision point
        menu:
            "The page is ready. What do I do with the night?"

            "Write the chapter. [[Progress manuscript]]":

                # [STATE] State/progression update
                jump day101_4_write_the_chapter

            "Visit Missy instead. [[Missy relationship seed, miss chapter opportunity]]":

                # [STATE] State/progression update
                jump day101_4_visit_missy

    else:

        "I dip the pen."
        "Nothing comes."
        "Not because the day was empty. Because I have not yet learned how to steal from it cleanly."

        "Missy is still awake in the next room. I can hear her turning over on the narrow bed."
        "If I cannot write, I can at least learn what the house has already done to her."

        # [STATE] State/progression update
        jump day101_4_visit_missy


# ==========================================
# 014 - WRITE THE CHAPTER
# ==========================================

label day101_4_write_the_chapter:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    # [STATE] This is the main Day 1 manuscript progression route
    $ story.set_day1_night_action("write")

    "The first sentence arrives like a servant entering the wrong room: terrified, necessary, unable to retreat."

    if story.day1_corridor_state == "predator":

        "I write a maid who learns that innocence is not a virtue."
        "It is a tool left unattended."
        "She places a sweeter girl before a dangerous door and discovers that guilt has a taste."

        if story.day1_ledger_focus == "corruption":
            "In the chapter, the maid does not apologise."
            "She improves."
        else:
            "In the chapter, the maid understands the cost and writes it down anyway."

    elif story.day1_corridor_state == "prey":

        "I write a maid who looks through a forbidden crack and is seen looking."
        "The gentleman does not shout. He invites her closer."
        "That is worse."

        if story.day1_ledger_focus == "corruption":
            "On the page, fear and invitation become difficult to separate."
        else:
            "On the page, the danger remains danger. The heat is only evidence."

    else:

        "I write a maid who never sees the room."
        "Only the wall. Only the voice. Only the terrible grammar of command and reply."
        "Her ignorance becomes precision."

        if story.day1_ledger_focus == "corruption":
            "She imagines too much and tells herself imagination is not participation."
        else:
            "She understands that distance can sharpen a knife."

    "By the time the candle gutters, the chapter exists."
    "Not finished. Nothing true is finished on the first night."
    "But real enough to accuse me."

    # [STATE] Increment manuscript through encapsulated story method, not raw global variable
    $ story.complete_manuscript_chapter("day1_chapter")
    $ apply_effects(insp=-10, corr=0)

    "I press the pages flat beneath the ledger."
    "Tomorrow the house will expect a maid."
    "It has acquired a witness instead."

    # [STATE] State/progression update
    call end_slot(outcome="d1_write_ch1")


# ==========================================
# 014 - VISIT MISSY
# ==========================================

label day101_4_visit_missy:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with fade

    # [STATE] Relationship seed. This should be meaningful: Cora gains Missy context, but loses the Day 1 chapter
    $ story.set_day1_night_action("visit_missy")
    $ story.set_missy_day1_seed(True)
    $ apply_effects(missy_susp=-5, insp=5, corr=0)

    "I leave the candle unlit."
    "A chapter can wait. A person, mishandled, changes shape before morning."

    # [ASSET] Visual/staging command
    show missy_sprite smiling at center

    missy "Cora?"
    cora "I couldn't sleep."

    missy "No one sleeps properly their first night. The pipes knock like ghosts and the mattresses are stuffed with old grudges."

    "She shifts to make room on the edge of the bed."
    "Trusting, then. Or lonely. There is often very little difference."

    if story.day1_corridor_state == "predator":

        missy "About earlier... I shouldn't have opened that door."
        cora "You were worried."
        missy "You said I was right to be."

        "There it is. A small bruise in the conversation."

        # [CHOICE] Decision point
        menu:
            "How do I handle Missy's doubt?"

            "Soothe her. Keep her close.":

                # [STATE] State/progression update
                $ apply_effects(missy_susp=-5, insp=5, corr=0)
                $ story.set_missy_day1_trust_state("soothed")

                cora "And perhaps you were. But the house has rules beneath its rules. We must learn them before we try to mend anything."
                missy "I suppose."
                "She wants that to be wisdom. I let it be."

            "Let the guilt sit between us.":

                # [STATE] State/progression update
                $ apply_effects(corr=5)
                $ story.set_missy_day1_trust_state("unsettled")

                cora "I should not have let you go first."
                missy "No."
                "She looks at me properly then. Not as a friend. Not yet as an enemy. As a question."

    elif story.day1_corridor_state == "prey":

        missy "You scared me half to death. What if Mr. Locke complains?"
        cora "Then Stern dismisses me."
        missy "Or worse, keeps you."

        "That is the first intelligent thing anyone has said to me all day."

        cora "Does he often visit that room?"
        missy "I don't know. I try not to know things with men's names attached."

        # [STATE] State/progression update
        $ story.set_missy_day1_trust_state("warned_cora")

    else:

        missy "You were right to walk away."
        cora "Was I?"
        missy "I think so. I don't know. This place makes right and wrong feel like stairs in the dark."

        "I sit with that."
        "Missy is not stupid. She is merely undefended."

        # [STATE] State/progression update
        $ story.set_missy_day1_trust_state("shared_caution")

    missy "Do you miss home?"

    "Home."
    "A word people use when they have not had to manufacture one out of locked doors and private plans."

    cora "Sometimes."
    missy "I miss my mother's kitchen. The ceiling leaked, but only in one place. Here everything shines and still feels damp."

    "She laughs quietly."
    "I could use this."
    "I could also simply sit beside her for a minute and not turn her into material."

    cora "Tell me about the kitchen."

    "So she does."
    "The candle remains unlit in my room."
    "The page remains blank."
    "The choice costs me exactly what it should."

    # [ASSET] Visual/staging command
    hide missy_sprite

    call end_slot(outcome="d1_visit_missy")
