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

# day104_non_canon.rpy
# Release 1 / Day 04 non-canon Ren'Py-shaped draft
# Source intent: parsed from legacy Day 4 heist script and reframed as the false dawn / tension-release day.
# Conceptual role: Cora survives the monster's house in daylight, finishes the manuscript, and believes she has gained decisive leverage.
# Day 5 should puncture that belief: Gideon is not the true invulnerable enemy; the society protecting him is.
# Asset constraint: uses assets already present in the supplied Day 4 draft plus recurring character sprites from earlier Day drafts.
# Promotion note: delete the temporary day104_041 stub from day103_non_canon.rpy when this file is promoted.
# Promotion note: replace story/player helper calls with exact runtime method names during implementation.

# ==========================================
# DAY 4 ANALYSIS / DESIGN INTENT
# ==========================================
# Legacy spine:
#   - Cora enters Gideon's empty suite while he and Vance are out.
#   - She opens the lockbox and finds compromising evidence.
#   - Gideon and Vance return early.
#   - Cora must escape with or without the evidence.
#   - Twilight becomes a suspicion-management trap.
#   - Night branches into exhaustion or writing.
#
# Structural revision:
#   - Day 4 should not feel like escalation into the finale. It should feel like relief earned through terror.
#   - This is the horror-film false dawn: the final girl finds the weapon, escapes the house, finishes the work.
#   - The player should feel: "I did it. I have the book. I have leverage. Tomorrow I can change everything."
#   - Day 5 then proves that individual leverage is not enough against class, gender, law, money, and reputation.
#
# Key correction:
#   - The photograph is not truly "ultimate leverage." It is Cora's believed leverage.
#   - It can ruin Gideon only if the world agrees to treat Cora as credible, safe, and worth hearing.
#   - Day 4 lets her believe that. Day 5 breaks it.


# ==========================================
# DAY 4 NODE MAP
# ==========================================
# 4_false_dawn_suite_window
#   -> 1_lockbox_evidence
#   -> 2_return_early
#   -> 2_escape_fireplace / 2_escape_bold_lie / 2_escape_missy_cover
#   -> 3_stern_pressure
#   -> 4_twilight_ledger_false_dawn
#   -> 5_triumphant_chapter
#   -> 6_false_dawn_ending
#   -> day105_1_monster_reemerges


# ==========================================
# 1 - FALSE DAWN / SUITE WINDOW
# ==========================================

label day104_1_false_dawn_suite_window:

    # [ASSET] Existing Day 4 Master Suite day background
    scene bg_master_suite_day
    with fade

    "Morning enters the Master Suite as if nothing terrible has ever happened there."
    cora_inner "That is the talent of expensive rooms."
    cora_inner "They reset themselves."

    "Gideon and Vance have gone to a matinee in the West End."
    cora_inner "Stern believes I am polishing silver on the ground floor."
    cora_inner "Missy believes I am avoiding her because guilt has finally made me decent."

    cora_inner "Everyone is wrong in a useful direction."

    if story.day3_ultimatum == "defied":
        "Last night I told Gideon that my writing was not part of my service."
        "Today I prove it by committing a crime in his room."
    elif story.day3_ultimatum == "bargained":
        "Last night I gave Gideon three sentences and kept the rest."
        "Today I need something of his to balance the exchange."
    elif story.day3_ultimatum == "surrendered":
        "Last night he sent me back sharpened and ashamed."
        "Today I come looking for a blade that is not made of appetite."
    else:
        "Last night left me with too many questions and not enough power."
        "Today I come looking for the thing powerful men hide from one another."

    cora_inner "The manuscript needs an ending."
    cora_inner "Not a pretty one. Not a moral one."
    cora_inner "An ending with enough truth inside it to bite."

    "I cross to the heavy oak writing desk."
    cora_inner "The lockbox waits beneath a stack of correspondence, exactly where a careless man would not hide it and a confident man would."

    # [STATE] State/progression update
    jump day104_1_lockbox_evidence


# ==========================================
# 1 - LOCKBOX / EVIDENCE
# ==========================================

label day104_1_lockbox_evidence:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    "The hairpin bends before the lock does."
    cora_inner "My hands are slick. My breath is too loud."
    cora_inner "Every sound in the room becomes Stern's footstep, Gideon's voice, Vance's laugh returning early down the hall."

    "Then the lock gives."

    "Inside: bank notes, a theatre programme, two folded letters, and an envelope stiff with photographic paper."

    # [ASSET] CG callout retained from legacy draft
    # show cg_gideon_photograph

    cora_inner "The photograph is not large."
    cora_inner "That feels obscene somehow."
    cora_inner "A life can fit on paper smaller than a prayer book."

    "Gideon. Another gentleman."
    "Not merely friendly. Not deniable in any honest room."

    cora_inner "My first feeling is triumph."
    cora_inner "My second is fear."
    cora_inner "My third is the writer's monstrous little gratitude."

    cora_inner "Here is the ending."
    cora_inner "Here is the proof."
    cora_inner "Here is the thing even Gideon Locke cannot smooth over with a quiet voice and a better coat."

    # [STATE] Cora has discovered the leverage. She has not necessarily escaped with it yet
    $ story.set_day4_evidence_discovered(True)
    $ apply_effects(vance_susp=15, insp=20, corr=0)

    "I slide the photograph beneath my bodice."
    "It scratches once against my skin and becomes real."

    # [STATE] State/progression update
    jump day104_2_return_early


# ==========================================
# 2 - RETURN EARLY
# ==========================================

label day104_2_return_early:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    "A key turns in the outer door."

    # [ASSET] Visual/staging command
    show vance_sprite neutral at centre_bust with moveinright # [asset auto]
    vance "—and I will not tolerate that tone from her again. Not from a dresser, not from a maid, not from anyone."

    cora_inner "They are early."
    cora_inner "Of course they are early."
    cora_inner "False dawns do not announce the trap. They simply let the sun in first."

    cora_inner "I am standing beside Gideon's desk with his lockbox open and his ruin pressed against my ribs."

    # [CHOICE] Decision point
    menu:
        "Sixty seconds. How do I survive?"

        "Hide in the cold hearth. Keep the evidence. [[Ghost escape: high suspicion]]":

            # [STATE] State/progression update
            jump day104_2_escape_fireplace

        "Stand in the room and lie cleanly. Keep the evidence. [[Prey escape: high visibility]]":

            # [STATE] State/progression update
            jump day104_2_escape_bold_lie

        "Use Missy as cover. Lose the evidence, preserve the alibi. [[Predator escape: low suspicion, moral cost]]":

            # [STATE] State/progression update
            jump day104_2_escape_missy_cover


# ==========================================
# 2 - ESCAPE: FIREPLACE
# ==========================================

label day104_2_escape_fireplace:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    # [STATE] Keeps photograph, but creates visible physical evidence on uniform
    $ story.set_day4_escape_state("fireplace")
    $ story.set_has_photograph(True)
    $ apply_effects(stern_susp=35, insp=5, corr=0)

    "The hearth is enormous, black, and unlit."
    "A servant could disappear there."
    "A desperate one does."

    "I close the lockbox, shove it beneath the correspondence, and crawl into the cold soot with the photograph against my chest."

    # [ASSET] Visual/staging command
    show gideon_sprite angry at right
    show vance_sprite angry at left

    "They enter arguing."
    "Vance first, bright with grievance. Gideon behind her, quiet enough to make the silence arrange itself around him."

    vance "You let her smirk at me."

    gideon "I let many people do many things when their errors are instructive."

    "From the hearth, I can see only shoes, hems, the polished legs of furniture."
    "It is the brush scene again, but lower. Dirtier."
    "The room has angles gentlemen never check because they cannot imagine needing them."

    "Soot enters my nose."
    "I breathe through my apron and do not cough."

    vance "You are not listening to me."

    gideon "I am listening precisely as much as required."

    "An hour passes in pieces."
    "At last they move into the bedchamber."
    "At last the sitting room is empty."

    # [ASSET] Visual/staging command
    hide gideon_sprite
    hide vance_sprite

    "I slide out of the hearth blackened, shaking, alive."
    "The photograph is still mine."
    "So is the soot."

    # [STATE] State/progression update
    jump day104_3_stern_pressure


# ==========================================
# 2 - ESCAPE: BOLD LIE
# ==========================================

label day104_2_escape_bold_lie:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    # [STATE] Keeps photograph, but Gideon has seen her too near the desk
    $ story.set_day4_escape_state("bold_lie")
    $ story.set_has_photograph(True)
    $ apply_effects(vance_susp=40, insp=10, corr=5)

    "I close the lockbox with one hand and seize the dust cloth with the other."
    "By the time the door opens, I am wiping the desk as if mahogany has personally insulted Miss Stern."

    # [ASSET] Visual/staging command
    show vance_sprite angry at left
    show gideon_sprite angry at right

    vance "What is she doing here?"

    "Gideon's eyes move from my face to the desk."
    "Then to my hands."
    "Then back to my face."

    gideon "That is my question."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show vance_sprite angry at centre_bust with move # [asset auto]
    show gideon_sprite angry at right_bust with move # [asset auto]
    cora "Checking the desk for dust, Sir. Miss Stern's orders."

    "The lie stands up."
    "Badly."
    "But standing is sometimes enough if everyone in the room prefers not to touch it."

    vance "This suite was cleaned at dawn."

    cora "Yes, Madam. Miss Stern is particular after complaints."

    "A small cruelty."
    "Not safe."
    "Useful."

    vance "Complaints?"

    gideon "Leave us."

    cora "Yes, Sir."

    "As I pass him, Gideon does not move aside until the last possible second."
    "The photograph scratches my skin like a second pulse."

    gideon "Cora."

    "I stop."

    gideon "You are developing a troubling habit of being where you ought not be."

    cora "Then I am grateful the house has so many rooms, Sir."

    "A foolish answer."
    "A glorious one."

    gideon "Go."

    # [ASSET] Visual/staging command
    hide gideon_sprite
    hide vance_sprite

    "I go before my courage notices what it has done."

    # [STATE] State/progression update
    jump day104_3_stern_pressure


# ==========================================
# 2 - ESCAPE: MISSY COVER
# ==========================================

label day104_2_escape_missy_cover:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    # [STATE] Lowest suspicion path, but Cora extracts the physical leverage and ruthlessly harms Missy
    $ story.set_day4_escape_state("missy_cover")
    $ story.set_has_photograph(True)
    $ story.set_missy_day4_used_as_cover(True)
    $ apply_effects(vance_susp=-15, missy_susp=20, insp=5, corr=20)

    cora_inner "Panic makes the first decision."
    cora_inner "Ambition improves it."

    "I slide the photograph into my bodice and close the lockbox, leaving everything else exactly as I found it."
    "I have the proof."

    "I slip through the servants' door as the outer door opens."

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_day
    with fade


    show missy_sprite shocked at center

    "Missy is in the corridor with a stack of towels."
    cora_inner "Wrong place. Right time."
    cora_inner "For me."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show missy_sprite shocked at right_bust with move # [asset auto]
    cora "They need you in the suite. Now. Take this."

    "I push the dust cloth into her hands."

    missy "What? Cora... why are you so pale? Is there..."

    cora "Vance is asking for the room to be checked again. Hurry before she comes looking and Miss Stern hears the noise."

    "Missy's eyes flick to my hands, then to the heavy master suite door. Her sharp observancy senses the transgressive panic in my chest."
    "She hesitates, her defensive moral guard up, but the threat of Stern and the sheer habit of class-duty make her step forward."

    missy "All right. But don't you wander off, Cora. It isn't proper."

    "She goes in, her shoulders squared against the impending storm."
    "The door closes."

    "Instead of running, I find myself frozen against the mahogany paneling."
    "The wood is cold, but the keyhole is a hot eye, a direct conduit to the danger inside."
    "I press my ear to the crack of the service door, holding my breath."

    "Within the Master Suite, the air is thick and heavy. I hear the slow, rhythmic click of Mr. Locke's walking stick against the polished floorboards."
    "He is circling her."

    # [ASSET] Visual/staging command
    show missy_sprite shocked at centre_bust with move # [asset auto]
    show gideon_sprite neutral at right_bust with moveinright # [asset auto]
    gideon "And what, pray tell, are you doing in my quarters, girl? Miss Stern was quite specific about who was to clear these rooms."

    "His voice is a low, silk-wrapped growl, vibrating through the wood. Missy's reply is barely a whisper, yet steady, carrying that active, unyielding moral shield."

    missy "The towels, Mr. Locke. They were reported damp. I was sent to change them."

    "The click of the walking stick stops. Through the gap, I can see Gideon step directly into her space, his towering frame casting a shadow that completely swallows her."
    "He raises his silver-headed walking stick, the polished wood gliding slowly, suggestively up the front of her uniform. The tip rests beneath her chin, tilting it upward, forcing her head back."
    "Missy's breath catches. Her hands clench the damp towels against her chest as if they are a shield."

    gideon "Damp, you say? And who, Missy, gave you that report? A maid does not walk into a gentleman's study without a very specific command."

    "He steps closer, his boots almost touching the hem of her skirt. He leans down, his face inches from hers, his free hand rising to trail the starched edge of her collar, his fingers brushing the sensitive skin of her jaw. The class terror is absolute, yet the physical proximity burns with a dark, forbidden heat."

    gideon "Is there someone else here? Someone who sent you to find what does not belong to you?"

    "For a terrible second, I am sure she will speak my name. My pulse beats like a trapped bird in my ears."
    "But Missy does not flinch from his touch. Her chin remains high against the silver tip of his cane, her dark eyes locking onto his with a quiet, sovereign courage that defies the terror of his touch."

    missy "I was sent by the service board, Sir. No one else."

    "Gideon's thumb traces the edge of her jaw, his eyes narrowing as he studies her flushed face, her parted lips. The silence between them is taut, charged with a heavy, dangerous intimacy."

    gideon "You are either very loyal, or very foolish, Missy. Both are expensive qualities in this house."

    "He slowly lowers the cane, his fingers sliding off her jaw with a lingering touch that leaves Missy trembling yet unbowed."

    gideon "Change the towels. Then leave. Before I decide to charge you for the privilege of your presence."

    "I step back from the door, my hands trembling, my chest tight with a sudden, devastating wave of shame."
    cora_inner "I have survived."
    cora_inner "But Missy has paid for my survival in currency I did not have the courage to spend."

    # [STATE] State/progression update
    jump day104_3_stern_pressure


# ==========================================
# 3 - STERN PRESSURE
# ==========================================

label day104_3_stern_pressure:

    # [STATE] State/progression update
    $ set_time_period("Evening")

    # [ASSET] Existing servants' quarters / corridor-adjacent pressure scene
    scene bg_servants_quarters_dusk
    with fade

    cora_inner "By twilight, survival has begun charging interest."

    if story.day4_escape_state == "fireplace":
        "Soot sits beneath my nails, in the seams of my cuffs, along the hem where the apron should be clean."
        "Every black mark is a witness with no loyalty."
    elif story.day4_escape_state == "bold_lie":
        "Gideon saw me near the desk."
        "He may not know what I took."
        "He knows I took the right kind of risk."
    else:
        "Missy returned from the suite with red eyes and a voice pressed flat."
        "Vance had found fault. Of course Vance had found fault."
        "I had handed her a target and called it haste."

    # [ASSET] Visual/staging command
    show stern_sprite stern at center

    stern "Cora."

    "Stern does not need evidence to suspect disorder."
    "She smells it the way laundresses smell mildew."

    stern "You were difficult to locate this afternoon."

    # [CHOICE] Decision point
    menu:
        "How do I handle Stern's pressure?"

        "Give her the boring servant answer. [[-Suspicion]]":

            # [STATE] State/progression update
            $ story.set_day4_stern_response("boring")
            $ apply_effects(stern_susp=-15, insp=0, corr=0)

            show cora_sprite base at left_bust with moveinleft # [asset auto]
            show stern_sprite stern at right_bust with move # [asset auto]
            cora "Ground-floor silver, Ma'am. Then linens. Then back stairs. I should have reported each change."

            stern "Yes. You should have."

            "She dislikes the answer because it gives her nothing but negligence."
            "Negligence is punishable."
            "It is also ordinary."

        "Let her see I am frightened, not guilty. [[+Inspiration, small suspicion]]":

            # [STATE] State/progression update
            $ story.set_day4_stern_response("frightened")
            $ apply_effects(stern_susp=5, insp=10, corr=0)

            cora "I am trying not to make mistakes, Ma'am. That is making me slower."

            "Stern studies me."

            stern "Fear is useful only when it sharpens. Yours is beginning to spill."

            cora "Yes, Ma'am."

            stern "Clean it up."

        "Hide behind Missy if she was used. [[Conditional moral cost]]" if story.day4_escape_state == "missy_cover":

            # [STATE] State/progression update
            $ story.set_day4_stern_response("missy_cover")
            $ apply_effects(stern_susp=-10, missy_susp=10, insp=0, corr=10)

            cora "Missy was with the suite, Ma'am. I was sent back down after delivering cloth."

            stern "I asked where you were."

            cora "Yes, Ma'am. Below stairs."

            "The answer is shaped to be true from a distance."
            "Stern hears the distance."
            "She cannot yet cross it."

    stern "Whatever has caught the attention of that room, remove yourself from it."

    cora "Yes, Ma'am."

    stern "Do not mistake a guest's notice for fortune. That lesson ruins girls."

    # [ASSET] Visual/staging command
    hide stern_sprite

    "She leaves me with the warning and no proof."
    cora_inner "Tonight, no proof is beginning to feel like grace."

    # [STATE] State/progression update
    jump day104_4_twilight_ledger_false_dawn


# ==========================================
# 4 - TWILIGHT LEDGER / FALSE DAWN
# ==========================================

label day104_4_twilight_ledger_false_dawn:
    call check_confrontations

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with dissolve

    $ show_ledger_ui()

    "The ledger sits open on my desk."
    "My hands have stopped shaking."
    cora_inner "This feels like improvement until I realise they have only gone numb."

    "The photograph is hidden beneath the loose board under my bed."
    "Not safe."
    "Safer than my skin."
    cora_inner "I have evidence."
    cora_inner "I have leverage."
    cora_inner "I have, for the first time since arriving, something Gideon Locke does not want me to have."

    cora_inner "The manuscript waits."
    cora_inner "Not for more material."
    cora_inner "For courage."

    # [CHOICE] Decision point
    menu:
        "Perform visible penance to lower their guard. [[Atonement]]":

            # [STATE] State/progression update
            jump day104_4_atonement

        "Risk the dark room to write the triumphant chapter. [[Triumphant Write]]" if player.anxiety < 85:

            # [STATE] State/progression update
            jump day104_5_triumphant_chapter

        "Risk the dark room to write the triumphant chapter. [[Triumphant Write]]" if player.anxiety >= 85:
            "My hand shakes too violently to hold the pen. The hotel feels alive, every creaking floorboard a footstep, every shadow a reaching hand."
            "At this level of anxiety, my panic blocks the pen."

            # [STATE] State/progression update
            jump day104_4_twilight_ledger_false_dawn

        "Find Missy and salvage what remains of her trust. [[Missy Repair]]" if getattr(story, "missy_day4_repair_state", "") == "":

            # [STATE] State/progression update
            jump day104_4_missy_repair


# ==========================================
# 4 - ATONEMENT / SAFETY FIRST
# ==========================================

label day104_4_atonement:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with dissolve

    $ story.set_day4_twilight_action("atonement")

    if story.day4_escape_state == "fireplace":

        # [STATE] State/progression update
        $ apply_effects(stern_susp=-30, insp=0, corr=0)

        "I scrub soot from my apron until the water turns grey, then black, then grey again."
        "My knuckles split."
        "Good. Blood is easier to explain than chimney dust."

    elif story.day4_escape_state == "bold_lie":

        # [STATE] State/progression update
        $ apply_effects(stern_susp=-25, insp=0, corr=0)

        "I sit in the laundry corner and mend cuffs with saintly dullness."
        "Anyone watching sees a maid trying very hard to become furniture."
        "That is the point."

    else:

        # [STATE] State/progression update
        $ apply_effects(stern_susp=-10, insp=0, corr=0)

        "I fold linens."
        "I carry water."
        "I become useful in every visible way, which is not the same as becoming good."

    "The hour does what it can."
    "It lowers the heat on my neck."
    "But the manuscript remains untouched. I am too exhausted to write."

    # [STATE] State/progression update
    jump day104_6_false_dawn_ending


# ==========================================
# 4 - MISSY REPAIR
# ==========================================

label day104_4_missy_repair:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with dissolve

    show missy_sprite shocked at center

    $ story.set_day4_twilight_action("missy_repair")
    $ apply_effects(missy_susp=-15, insp=5, corr=0)

    "Missy sits on the edge of her narrow iron bed, twisting her linen handkerchief until her knuckles are as white as the cloth."
    "She doesn't look like a simple country girl caught in a mistake tonight. Her eyes are quiet, exceptionally focused, and dangerous with what they have resolved."

    missy "You sent me in there, Cora Vale."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show missy_sprite shocked at right_bust with move # [asset auto]
    cora "I did."

    "The word is smaller than the betrayal. It hangs in the narrow space between us, smelling of cedar oil and grey twilight."

    missy "You knew they were returning. You knew Mr. Locke was angry. You were standing by his open desk, your hands clean, while I was sent into the suite to take the blow."

    "She rises, her posture rigid, her voice losing every trace of its deferential junior maid register."

    missy "You're a spy, aren't you? Prying into the suites, stealing Mr. Locke's letters... and you used me as a shield because you thought I was too stupid to see the joints in your performance."

    cora_inner "She has decoded it. Not with empty-headed curiosity, but with a sharp, sovereign intellect."

    missy "Why, Cora? I trusted you. I thought... I thought you were the only righteous thing in this terrible hotel."

    # [CHOICE] Decision point
    menu:
        "Give her the raw, romantic truth. Offer my vulnerability. [[Tender Romance / Path B Intimacy]]":

            # [STATE] Rebuilds trust, progresses Path B romantic intimacy
            $ story.set_missy_day4_repair_state("partial_truth")
            $ apply_effects(missy_susp=-25, vance_susp=5, insp=15, corr=10)

            cora "Because I was cornered, and I was terrified of losing the only thing that keeps me alive in this place. My writing. My book."
            cora "And because when I am terrified, I am a monster. But I would rather be dismissed a hundred times than see you look at me with that wall between us."

            "I step closer, crossing the narrow floorboards, my hands reaching out to cover her raw, trembling fingers."
            "Missy flinches, her breath catching, but she does not step back. The proximity between us is suffocating, thick with lye-steam and the scent of cedar."

            cora "I do not see you as a shield, Missy. I see you as the only beautiful thing in this hotel that isn't a lie."

            "I raise my hand, my thumb tracing the damp, flushed skin of her cheek, my voice dropping the maid's mask entirely. It is a quiet, sovereign register of deep romantic tenderness."
            "Missy's eyes widen, her breathing turning shallow, her chest rising against my hands."

            missy "Cora... your touch is like... it's like a sin I want to keep."
            cora "Then let us keep it together. No more shields, Missy. Only this."

            "She leans her forehead against my shoulder, her body trembling with a self-possessed, deliberate yielding."
            "The physical heat between us is a dramatic middle ground—restrained, dangerous, but born of absolute romantic trust."

        "Keep the truth. Offer a coward's comfort. [[Guarded Distance]]":

            # [STATE] Safe but keeps Missy guarded, locks out Path B intimacy
            $ story.set_missy_day4_repair_state("comfort_lie")
            $ apply_effects(missy_susp=-10, insp=0, corr=5)

            cora "Because I am a coward when cornered, Missy. I saw the door, I saw the threat, and I used what was closest. It was cruel, and I cannot justify it."

            missy "That is a confession, Cora. It is not an apology."

            cora "No. But it is the only honest thing I have left to give you."

            "I sit on the edge of the bed, leaving a cold foot of cedar wood between us."
            "She does not ask me to leave, but her defensive moral shield is up, her posture guarded."
            "We are safe from Miss Stern tonight, but the book has lost its partner."

    # [ASSET] Visual/staging command
    hide missy_sprite

    "When I return to my room, the emotional toll weighs heavier than the fear."
    "I am safe, but the pen refuses to move. I cannot write tonight."

    # [STATE] State/progression update
    jump day104_6_false_dawn_ending


# ==========================================
# 5 - TRIUMPHANT CHAPTER
# ==========================================

label day104_5_triumphant_chapter:
    call check_confrontations

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with fade

    $ story.set_day4_night_action("finish_manuscript")

    "Night arrives gently."
    "Suspiciously gently."

    "No summons."
    "No knock."
    "No key turning in a room where I should not be."

    "Only the candle, the page, and everything I have stolen without permission."

    "The chapter comes all at once."
    "Not because it is easy."
    "Because I finally have the knife shaped correctly."

    "In this chapter, the lord's secret is not named."
    "It is placed on a table in a sealed envelope and allowed to poison every polite sentence around it."
    "The heroine defeats him completely. She is untouchable. She has won."

    # [STATE] State/progression update
    $ story.complete_manuscript_chapter("day4_triumphant_chapter")
    call book1_write_chapter(chapter_key="day4_triumphant_chapter", current_day=104)
    $ apply_effects(stern_susp=15, insp=-15, corr=0)

    "The final sentence lands just before the candle dies."
    "For a while, I do not move."
    "It feels triumphant. It feels like an ending."
    "I mistake fiction for reality, believing that writing the victory makes it absolute."

    # [STATE] State/progression update
    jump day104_6_false_dawn_ending


# ==========================================
# 6 - FALSE DAWN ENDING
# ==========================================

label day104_6_false_dawn_ending:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    if story.day4_night_action == "finish_manuscript":
        "The chapter is complete."
        "I have told the story where the maid outwits the master."
    else:
        "The manuscript remains untouched."
        "But the danger has passed. I am still here. I have survived the day."

    "Beneath the loose floorboard, Gideon's photograph waits in the dark."
    "My leverage. My absolute proof."

    "Tomorrow I will decide how to use it."
    "Tomorrow Gideon Locke will learn that servants can keep evidence."
    "Tomorrow the balance changes."

    "For the first time since I arrived, sleep comes without asking permission."

    "Outside my room, the hotel breathes around me."
    "Not beaten."
    "Only sleeping."

    "I mistake the difference for victory."

    # IMPLEMENT DEADLINE GATE CHECK HERE
    if story.manuscript_progress < 2:

        # [STATE] State/progression update
        jump game_over_deadline_2

    jump day105_1_monster_reemerges
