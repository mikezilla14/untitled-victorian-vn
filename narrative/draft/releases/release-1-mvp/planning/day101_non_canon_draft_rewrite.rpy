Here is the complete, production-ready rewrite of `day101.rpy`. 

The narrative has been restructured to immerse the audience in the suffocating precarity of the Savoy. The prose emphasizes Cora’s razor-thin English mask, Stern's clinical dominance, the raw submissive collapse of Miss Vance before Gideon Locke, and the tense rapport between Cora and Missy—the true country girl Cora pretends to be.

***

<details>
<summary><strong>1. Architectural & Narrative Design Changes</strong></summary>

### Key Narrative Advancements
* **Intense introduction to the Savoy:** Cora is plunged straight into her interrogation with Ms. Stern. The atmosphere is thick with atmospheric dread; her forged papers, her forbidden manuscript, and her hidden Irish heritage are represented as direct tickets to the workhouse or the brothels of Holywell Street if she slips for even a fraction of a second.
* **Ms. Stern's Forensic Scrutiny:** Stern is presented as a cold, terrifying administrative force of nature. Her uniform is perfectly straight, but her hands are physical and diagnostic, checking Cora's collar, apron, and muscle tone like livestock, establishing the hotel's raw physical dominance immediately.
* **The Corridor Incident:** The previous "thrown toy" scene is completely replaced. Now, Cora witnesses a striking display of workplace violence: Miss Vance verbally claws at a trembling Missy. Gideon Locke appears, instantly neutralizing Vance with a single, quiet command, demonstrating his total psychological control as her public arrogance collapses into a raw, breathless apology.
* **The Rapport & The Trap:** At the laundry, Cora and Missy forge an immediate bond. Missy is from a small parish just miles from the fictional village Cora claimed as her birthplace. Missy is everything Cora pretends to be; Cora must execute a dangerous dance of evasion and linguistic vigilance to preserve her cover.
* **The Servants' Corridor Choice:**
    * **Predator Path (Manipulate Missy):** Cora exploits Missy's naive concern to make her look through the door. Missy is deeply unsettled by the raw, transgressive discipline inside, and her suspicion toward Cora's cold pragmatism spikes.
    * **Prey Path (Listen at the Vent):** Cora leans close to the ventilation grate. A floorboard creaks under her foot. Gideon is startled inside the room; he shrugs it off, but Vance's general paranoia toward the staff increases.
    * **Ghost Path (Interfere Directly):** Cora boldly knocks on the door, using her duties as an excuse. This gives her a full, direct view of Vance on her knees in transitional undress before Gideon Locke.

</details>

<details>
<summary><strong>2. Structural Variable Mapping</strong></summary>

All internal game logic, variable assignments, and branching paths are preserved exactly to prevent any broken hooks in your engine.

| Route Choice | Variable Set | Stat Changes Applied |
| :--- | :--- | :--- |
| **Meek Interview** | `story.set_day1_interview_state("meek")` | `prey` archetype $+1$ |
| **Competent Interview** | `story.set_day1_interview_state("competent")` | `ghost` archetype $+1$ |
| **Subservient Stern Relation** | `story.set_day1_stern_relation("subservient")` | `prey` archetype $+1$ |
| **Resistant Stern Relation** | `story.set_day1_stern_relation("resistant")` | `ghost` archetype $+1$ |
| **Complicit Stern Relation** | `story.set_day1_stern_relation("complicit")` | `predator` archetype $+1$ |
| **Vance - Deferential Posture** | `story.set_day1_vance_relation("subservient")` | Standard Submissive change |
| **Vance - Defiant Posture** | `story.set_day1_vance_relation("defiant")` | Standard Defiant change |
| **Vance - Ghostly Posture** | `story.set_day1_vance_relation("ghostly")` | Standard Self-Protective change |
| **Corridor - Persuade Missy** | `story.set_corridor_state("predator")` | `predator` archetype $+1$ |
| **Corridor - Listen at Vent** | `story.set_corridor_state("prey")` | `prey` archetype $+1$ |
| **Corridor - Bold Knock** | `story.set_corridor_state("ghost")` | `ghost` archetype $+1$ |

</details>

***

## The Rewritten Ren'Py Script

```renpy
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

    # [BEAT] The tense arrival at the Savoy. Cora's survival stakes are made visceral and immediate.
    scene bg_savoy_corridor_morning:
        zoom 1.0
        xysize (1920,1080)

    # [ASSET] Visual/staging command
    with fade

    cora_inner "The Savoy does not merely employ girls like me. It strips them of their names, swallows them down, and polishes the brass with whatever is left."
    cora_inner "I hold my breath against the heavy, suffocating scent of expensive coal smoke, gas lamps, and the wet lavender water used to mask the smell of London's rot."
    cora_inner "Behind my teeth, my mother's soft, looping Cork lilt scrambles to escape. I force it down. Deep. Below the floorboards."
    cora_inner "Here, I must speak with the rounded, flat, hollow vowels of a Wiltshire parson's daughter. A single slip—one wild, soft Irish consonant—and my forged references will be matches for the grate."
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

    cora_inner "I stand outside Ms. Stern's door, my traveling dress damp at the hem, my palms sweating against my small valise."
    cora_inner "Inside my pocket, the forged papers Lady Eleanor signed with a trembling hand are my only shield. If Stern smells the ink of my lies, the trap slams shut before I even begin."

    "From behind the heavy mahogany door, a clock ticks with a heavy, metallic precision—the heartbeat of a house that owns every second of my day."

    stern "Enter." 

    # [STATE] State/progression update
    jump day101_1_morning_interview


# ==========================================
# 011 - MORNING INTERVIEW
# ==========================================

# [DAG_NODE id=day101_1_morning_interview type=work day=101]
label day101_1_morning_interview:

    # [ASSET] Visual/staging command
    scene bg_stern_office_reverse:
        zoom 1.0
        xysize (1920,1080)

    # [ASSET] Visual/staging command
    with dissolve

    # [ASSET] Visual/staging command
    show stern_sprite neutral at right_full_body
    # [ASSET] Visual/staging command
    show cora_sprite base_travel at left_full_body
    with dissolve

    "Ms. Stern does not sit. She stands behind her desk, her spine a straight, black line of absolute authority."
    "Her eyes are not the eyes of an employer; they are the clinical, dissecting instruments of an inspector checking for rot."

    stern "Cora Vale."

    cora "Yes, Ma'am."

    stern "A Wiltshire reference. The Lady Eleanor speaks highly of your... quiet nature. Your lack of curiosity."

    cora_inner "Because my curiosity cost her five gold sovereigns and her private dignity."

    cora "I believe in keeping my eyes on my work, Ma'am. The country teaches one the value of a quiet tongue."

    stern "The country is a slow, soft place, Vale. It allows a girl to dream over her brooms. The Savoy does not."
    stern "A maid here is hands without weight, feet without noise, and memory without a tongue. If you carry any romantic notions about your station, discard them now. They are the first step to the street."

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

            cora "I understand, Ma'am. I only wish to perform my duties as I am directed."
            stern "Do not wish, Vale. Perform. The house does not pay for your interior aspirations."

            cora_inner "Let her see a dull, obedient cow. The smaller I appear in her eyes, the larger the space I have to move in the dark."

        "Answer cleanly. Let competence do what meekness cannot.":

            # [STATE] Semantic balance profile: Competence draws Stern's scrutiny
            $ apply_balanced_effect("defiant", intensity="standard", witness="stern")
            $ story.set_day1_interview_state("competent")
            $ apply_archetype_edge("ghost", 1)

            # [ASSET] Visual/staging command
            show cora_sprite base_travel at left_reframe
            # [ASSET] Visual/staging command
            show stern_sprite neutral at right_reframe
            with dissolve            

            cora "I am quick, exact, and I do not lose my focus. If I err, it will not be because I was looking elsewhere."
            stern "Exact? That is a word for a ledger, Vale, not a scrubbing brush."

            cora_inner "She pauses, her dark eyes narrowing. I have shown too much edge, too much education. I must tread carefully."

    "Ms. Stern steps from behind her desk. Her leather boots click with slow, deliberate pacing."
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
            stern "A girl of stone. Very well. But remember, stone can be ground to dust if it stands in the way of the carriage wheels."

            cora_inner "My eyes glaze over her shoulder, focusing on the dark wood of her cabinets. She may handle me like a doll, but my mind remains my own—unseen, untouched, and utterly free."

        "Meet her gaze directly through the closeness, accepting the intrusion with a steady pulse.":

            # [STATE] Semantic balance profile: Cora meets Stern's gaze through the closeness
            $ apply_balanced_effect("transgressive", intensity="major")
            $ story.set_day1_stern_relation("complicit")
            $ apply_archetype_edge("predator", 1)

            # [ASSET] Visual/staging command
            show cora_sprite base_travel at left_reframe
            with dissolve

            cora "I understand the value of a perfect fit, Ma'am. In all things."
            
            "Stern's thumb presses hard against the hollow above my collarbone, a brief, sharp warning before she slowly sliding her hand down to lift my chin."

            stern "A maid who looks back is a maid who wants to be noticed, Vale. And noticed maids in the Savoy do not last long enough to collect their first quarter's wages."

            cora_inner "Her touch is hot, deliberate. It is not morality that guides her hand—it is the sheer, intoxicating pleasure of absolute control."

    stern "The guests here are... peculiar, Vale. They have expensive tastes, dark habits, and very short memories. Some maids think they can trade a guest's secrets for silk, or their bodies for a gentleman's favor."
    stern "They always end up on the cobbles of Waterloo, diseased and discarded. Do you understand what happens to girls who lose their tongues for the wrong price?"

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
            stern "Interest is a luxury. Avoidance is your shield. See that you do it."

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

            cora "I know how to keep secrets, Ma'am—and those of the house."
            stern "Secrets? A maid has no secrets, Vale. She only has duties. Remember that, or I will ensure your references become as blank as your future."

            cora_inner "A slip. I let her see the ink beneath the starch."
            cora_inner "But her eyes flared. She knows now that I am not just a maid; I am a witness. And witnesses can be bought, or they can be feared."

    stern "You will report to the laundry first. Missy will show you the necessary route."
    stern "Take your travel clothes off, collect your uniform, and drop off anything that requires washing."
    stern "You will not wander. You will not question guests. You will not cultivate opinions."

    cora_inner "Too late for that."

    # [ASSET] Visual/staging command
    hide stern_sprite

    jump day101_1_vance_throws_toy


# ==========================================
# 011 - VANCE & GIDEON ENCOUNTER
# ==========================================

# [DAG_NODE id=day101_1_vance_throws_toy type=work day=101]
label day101_1_vance_throws_toy:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning:
        zoom 1.00
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with dissolve

    "The grand corridor of the guest wing is all gloss, mahogany, and heavy velvet restraint."
    "Suddenly, a sharp, vitriolic voice pierces the quiet. It is loud, erratic, and dripping with class-based cruelty."

    # [ASSET] Visual/staging command
    show vance_sprite angry at right_full_body:
        xalign 0.6
        yalign 1.1
        zoom 0.8

    # [ASSET] Visual/staging command
    show missy_sprite shocked at left_full_body:
        xalign 0.3
        yalign 1.1
        zoom 0.8

    "Miss Vance stands over a junior maid—Missy—who is trembling, a spilled laundry basket of delicate linens at her feet."

    vance "Stupid, clumsy little cow! Look at this lace! Do you think the Savoy pays for your butter-fingered country ignorance?"
    vance "This is Belgian weave! If there is a single snag, I will have your wages docked until you're working for the mud-larks!"

    missy "Please, Miss... the floorboard was loose—I didn't mean—"

    vance "Silence! You do not speak to me. You do not explain your incompetence!"

    "I stand completely frozen in the transition between the office and the guest stairs, my traveling clothes bundled under my arm, watching the display of raw, displaced fury."
    "Vance's face is flushed, her breathing shallow, her cheeks flushed high under her lacquered hair. She is treating the maid like her personal whipping boy."

    # [ASSET] Visual/staging command
    show gideon_sprite cold at right_full_body:
        xalign 0.95
        yalign 1.0
        zoom 0.8
        
    gideon "Vance."

    # [ASSET] Visual/staging command
    hide vance_sprite
    hide missy_sprite
    # [ASSET] Visual/staging command
    show missy_sprite shocked at left_bust:
        xpos 0.2
    # [ASSET] Visual/staging command
    show vance_sprite submissive at left_bust:
        xpos 0.5
        xzoom -1.0
    # [ASSET] Visual/staging command
    show gideon_sprite cold at right_bust:
        zoom 1.0
        xpos 0.8

    # [ASSET] Visual/staging command
    with dissolve

    "One word. The corridor changes temperature instantly."
    "Vance's shoulders drop. Her lips part in a quick, swallowed gasp, her erratic, petulant fury folding away into a practiced, submissive compliance."
    "Her entire demeanor turns from predator to prey in the space of a single breath. The transition is sickeningly elegant."

    vance "Gideon. I... I was only correcting her. The girl was clumsy with the private linen."

    gideon "You are making yourself loud, Vance. Quietly, if you please."

    "He does not raise his voice. He does not need to. His tone carries the absolute weight of a master who expects his property to behave itself in public."

    gideon "Go, girl."

    "Missy scrambles to her feet, gathering the linens in her basket with trembling hands. She retreats down the narrow service stairs, keeping her eyes glued to her boots."
    "I stay behind, hidden in the shadows of the staircase landing, utterly transfixed by the dark transaction between the two."

    gideon "We are guests in this house, Vance. We do not perform our discipline in the corridors. Do not force me to remind you of your place again."

    vance "Of... of course, Gideon. Forgive me."

    "Her voice is a low whisper, completely stripped of its public authority. She looks down, her eyes fixed on the silver buttons of his waistcoat."
    "Locke turns and enters the suite, his boots striking the floor with absolute authority. Vance follows him, but she stops short on the threshold."
    "She turns, her gaze catching me in the shadows. Her eyes widen with immediate shame and burning irritation."

    # [ASSET] Visual/staging command
    hide gideon_sprite
    with dissolve

    "She steps toward me, her teeth grit, her voice a low, burning hiss."

    vance "You. What are you looking at, girl?"

    cora "Nothing, Miss."

    vance "If I see you lingering in this corridor again, or if I hear a single whisper of this among the staff, I will make sure Stern throws you to the street. Do you hear me?"

    cora_inner "She is threatening me with her voice, but her hand is shaking as she reaches for her skirt. She is terrified that the servants have seen her collar undone."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day101_1_vance_throws_toy_menu_1]
    menu:
        "How do I present myself to Miss Vance?"

        "Lower my chin, offering an apologetic, humble maid's response. [[Deferential posture]]":

            # [STATE] Semantic balance profile: Cora plays the meek servant for Vance
            $ apply_balanced_effect("submissive", intensity="standard", witness="vance")
            $ story.set_day1_vance_relation("subservient")

            # [ASSET] Visual/staging command
            show cora_sprite guarded_travel at left_full_body
            with dissolve

            cora "My apologies, Miss. I only wish to reach the laundry. I saw nothing."

            "Vance lifts her chin, her face smoothing as she absorbs the submission."

            vance "At least one of you country girls has some sense of place. Run along. Before I find another chore for your hands."

            cora_inner "She hears a stupid, frightened maid. Let her keep that version."

        "Stand straight and meet her gaze directly, holding her look. [[Defiant posture]]":

            # [STATE] Semantic balance profile: Cora challenges Vance with direct tone
            $ apply_balanced_effect("defiant", intensity="standard", witness="vance")
            $ story.set_day1_vance_relation("defiant")

            # [ASSET] Visual/staging command
            show cora_sprite base_travel at left_full_body
            with dissolve

            cora "I speak with discretion, Miss. You have no need to worry about my eyes."

            "Vance goes still. Her eyes widen, startled by the directness of my tone."

            vance "You speak with a great deal of confidence, girl. Do you want me to tell Miss Stern how you look at guests?"

            cora_inner "She is threatening me, but her chest is heaving. She is not angry; she is exposed."

        "Keep a cold, blank face, acting as an invisible mirror. [[Ghostly posture]]":

            # [STATE] Semantic balance profile: Cora remains a blank mirror to Vance
            $ apply_balanced_effect("self_protective", intensity="standard", witness="vance")
            $ story.set_day1_vance_relation("ghostly")

            # [ASSET] Visual/staging command
            show cora_sprite base_travel at left_full_body
            with dissolve

            cora "I have my duties, Miss. I am on my way."

            "Vance snatches her skirt, her expression turning into a scowl of irritation. The complete lack of reaction from me is a wall she cannot climb."

            vance "Useless post. You are like a piece of furniture that has learned to walk."

            cora_inner "A mirror does not apologize. It only holds the shape."

    # [ASSET] Visual/staging command
    hide vance_sprite
    hide cora_sprite
    with dissolve

    jump day101_2_missy_meets_cora


# ==========================================
# 012 - MISSY MEETS CORA (LAUNDRY ROOM)
# ==========================================

# [DAG_NODE id=day101_2_missy_meets_cora type=work day=101]
label day101_2_missy_meets_cora:

    # [ASSET] Visual/staging command
    scene bg_laundry_room_day:
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with fade

    "The laundry room is heat, lye, damp cotton, and women trying not to cough."
    "Steam beads on the stone walls, turning every face soft and wet at the edges. I drop my travel dress into the dark wicker hamper, collecting my heavy, starch-stiff uniform."

    # [ASSET] Visual/staging command
    show missy_sprite smiling at right_full_body

    missy "You're the new girl, then. Cora Vale."

    # [ASSET] Visual/staging command
    show cora_sprite base_travel at left_full_body
    with moveinleft

    cora "I am."

    "Missy's face carries a small, lingering flush from her encounter with Vance, but she forces a desperate, eager smile, her register chatty but guarded."

    missy "I'm Missy. We're to work the laundry rotation together. But don't look so pale—Miss Stern makes everyone feel as if they've violated the commandments just by breathing the air."
    missy "But we must keep our heads down. A girl's virtue and her honesty are the only shields she has in London. Lose either, and you're under the carriage wheels."

    cora "I believe in discretion, Missy."

    missy "And where are you from, Cora? Your papers say Wiltshire."

    cora "A small village. Near East Knoyle. Very quiet."

    "Missy's eyes light up with a sudden, beautiful, and terrifying recognition."

    missy "Wiltshire! Oh, bless you, I'm from Hindon myself! Just three miles down the road!"
    missy "You must know the old oak by the mill? And the curate, Mr. Harrison? He has the most wonderful, proper sermons on Sundays."

    cora_inner "My heart stops. A physical blow to my chest."
    cora_inner "She is the real thing—the innocent, pious English country girl I am pretending to be."
    cora_inner "If I slip now, if I name the wrong lane or mispronounce the local grange, she will know. And her concern will destroy me."

    cora "The old mill is... quite beautiful in spring. Though I lived closer to the parish line. We... we did not have much occasion to travel to Hindon."

    missy "Ah, that's a pity. The curate's wife was always so good to the girls in service. Such a righteous place."

    cora_inner "The irony is a cold weight. Missy is the very life I claimed to have lived, purely to get this position."
    cora_inner "We are two halves of a lie, and she has no idea she is holding the knife."

    # [STATE] State/progression update
    jump day101_2_coras_path_choice


# ==========================================
# 012 - CORA'S PATH CHOICE (SERVANTS' CORRIDOR)
# ==========================================

# [DAG_NODE id=day101_2_coras_path_choice type=choice]
label day101_2_coras_path_choice:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_dim:
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with fade

    "The servants' corridor behind the guest wing is narrower than it should be. The plaster is damp and cold, carrying sound like a physical wire."

    # [ASSET] Visual/staging command
    show missy_sprite smiling at centre_bust

    missy "This way. Mind the third board on the landing—it complains, and Stern hears every creak."

    "We pass a service door near the Master Suite."
    "Suddenly, a sharp, clean *SLAP* rings through the wood."
    "A wet, heavy gasp of submissive pain follows, a sound so dark, so carnal, and so shocking that it physicalizes the air between us."

    vance "Ah! Gideon... please..."

    # [ASSET] Visual/staging command
    show missy_sprite shocked at left_bust

    "Missy goes absolutely still, her fingers tightening around the wicker hamper so hard her knuckles turn as white as the linens."
    "Her face is a mixture of terror, confusion, and defensive religious panic."

    missy "Oh... oh, Lord. That... that was a slap. She's in distress. Cora, we... we ought to fetch Miss Stern. Or is it wicked of us to interfere?"

    cora_inner "My survival instinct says to walk. Keep walking. Save the cover."
    cora_inner "But the writer in me... the hunger that dragged me from Wiltshire... it needs to see. It needs the raw, unvarnished truth of their depravity."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day101_2_coras_path_choice_menu_1]
    menu:
        "How do I take the material?"

        "Persuade Missy to check on the room. [[Predator path: $+1$ Predator]]":

            # [STATE] Semantic balance profile: Cora weaponises Missy's concern for material
            $ apply_balanced_effect("predatory", intensity="standard", witness="vance")
            $ story.set_corridor_state("predator")
            $ apply_archetype_edge("predator", 1)

            cora "If she's hurt, Missy, someone must check. But I am new—if I open that door, I will be dismissed before my first day is done."
            cora "You know the house. You have the right to check if the suite needs assistance."

            cora_inner "I use her decency as my shield. Let her handle the dirty work."

            missy "I... only a little look, then. Only to ensure she is safe."

            "Missy steps toward the door, her hand shaking as she pushes the heavy mahogany latch."
            "The door swings open a finger's width."
            "Behind the door, Vance is on her knees in a state of transitonal undress, her corset laced but her linen chemise pulled low, her white buttocks bared as Gideon Locke stands over her, his heavy hand raised."
            "Missy gasps, her eyes wide with absolute, horrified realization."

            gideon "Who is there?"

            "Missy pulls the door shut, her face white, her eyes darting to me with a sudden, deep, and wounding suspicion."

            missy "Cora... that was... they were... it was a sin. A terrible, wicked thing."
            missy "Why... why did you make me look?"

            cora_inner "She is terrified, and her trust is wounded. She sees the coldness in my eyes."

        "Go to the vent yourself and listen. [[Prey path: $+1$ Prey]]":

            # [STATE] Semantic balance profile: Cora takes direct corridor risk for the image
            $ apply_balanced_effect("reckless", intensity=1.4, witness="vance")
            $ story.set_corridor_state("prey")
            $ apply_archetype_edge("prey", 1)

            cora "Stay here. Let me listen."

            "I step toward the ventilation grate by the floorboards."
            "I press my ear to the cold iron, my hand leaning on the wood."
            "Suddenly, the third board creaks under my knee—a sharp, loud groan."

            gideon "Who is in the corridor?"

            "Inside, the sound of movement stops. Silence falls like a heavy axe."
            "Missy grabs my sleeve in a panic, dragging me into the shadow of the backstair bend before the door can open."

            missy "Cora, you're mad! If they catch us prying... we'll be thrown to the streets!"

            cora_inner "We escaped, but Vance's general suspicion of the staff will spike. She knows someone was watching."

        "Boldly knock on the door yourself. [[Ghost path: $+1$ Ghost]]":

            # [STATE bespoke] Multi-witness suspicion reduction; cannot map to one profile
            $ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5, insp=10, corr=0)
            $ story.set_corridor_state("ghost")
            $ apply_archetype_edge("ghost", 1)

            cora "No. We do not look. We do not run. We perform."
            
            "I step forward and knock firmly on the door, my voice loud, sterile, and perfectly professional."

            cora "Chambermaids, Miss. We have the clean towels you requested."

            "A long, heavy pause. Inside, the rustle of silk."
            "The door opens. Gideon Locke stands there, his shirt slightly open, his gaze analytical and freezing."
            "Behind him, Vance is sitting on the edge of the bed, her chemise hastily pulled over her shoulders, her face flushed with high, burning shame."

            gideon "Set them on the bench, girl."

            cora "Yes, Sir."

            "I enter, placing the towels down, my eyes taking in the entire transgressive scene before me—the heavy leather crop on the vanity, the red marks on her skin."
            "I bow and step out, my pulse slow and steady."

            cora_inner "I have seen it. A full view of their dark luxury. A writer needs no more than that."

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
    "A narrow bed. A basin of cold water. A single tallow candle. A desk too small for ambition."

    # [STATE] State/progression update
    $ show_ledger_ui()

    cora_inner "I open my ledger, the ink wet, and record the day's useful damages."

    if story.day1_corridor_state == "predator":
        cora_inner "Missy's shocked, wounded face returns first. I used her decency as a blunt instrument."
        cora_inner "Vance on her knees. Locke's raised hand."
        cora_inner "The sentence looks uglier once written down, but it is real."

    elif story.day1_corridor_state == "prey":
        cora_inner "I can still feel the loose floorboard shifting beneath my stockinged foot."
        cora_inner "Locke was so close. A single inch, and I would have been in the dirt."

    else:
        cora_inner "I knocked. I looked the devil in his eye and went back to my work."
        cora_inner "That is how a ghost moves. Unseen, untouched, but recording everything."

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

                "Order. Safety in structure. [[Creative discipline: $+10$ Inspiration]]":

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

                "Exposure. Safety in knowing the threat. [[Transgressive discipline: $+10$ Corruption]]":

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

        "Frame it with order and structure. I must write what is safe. [[Creative framing: $+10$ Inspiration]]":

            # [STATE] Semantic balance profile: Cora frames the chapter with structure
            $ apply_balanced_effect("creative", intensity="major")
            $ story.set_day1_ledger_focus("inspiration")

            cora_inner "I draw three columns in the ledger and let the structure guide my hand."
            cora_inner "The shape of the scene matters more than the appetite of it."
            cora_inner "A woman attacks downward because she cannot attack upward. A man corrects her, not from kindness, but ownership."

        "Frame it with exposure and appetite. I must write the truth. [[Transgressive framing: $+10$ Corruption]]":

            # [STATE] Semantic balance profile: Cora frames the chapter with appetite
            $ apply_balanced_effect("transgressive", intensity="standard", witness="vance")
            $ story.set_day1_ledger_focus("corruption")

            cora_inner "I try to write command, witness, consequence, but my hand writes want."
            cora_inner "I think of the way she yielded and hated him for making her yield."
            cora_inner "I think of Missy reaching for the latch because I placed fear in her hand."

    cora_inner "The first sentence arrives like a servant entering the wrong room: terrified, many-layered, and unable to retreat."

    if story.day1_corridor_state == "predator":

        cora_inner "I write a maid who learns that innocence is not a virtue."
        cora_inner "It is a tool left unattended. She places a sweeter girl before a dangerous door and discovers that guilt has a taste."

        if story.day1_ledger_focus == "corruption":
            cora_inner "In the chapter, the maid does not apologise."
            cora_inner "She improves."
        else:
            cora_inner "In the chapter, the maid understands the cost and writes it down anyway."

    elif story.day1_corridor_state == "prey":

        cora_inner "I write a maid who looks through a forbidden crack and is seen looking."
        cora_inner "The gentleman does not shout. He invites her closer. That is worse."

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

    cora_inner "By the time the candle gutters, there are pages. Not a chapter. Not a wound. Not even a proper lie."

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
```