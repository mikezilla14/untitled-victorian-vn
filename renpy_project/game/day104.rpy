# ═══════════════════════════════════════════════════════════════
#  day104.rpy — RELEASE 1, DAY 04: THE FALSE DAWN
#  Promoted from day104_non_canon.rpy (Release 1 MVP, revised).
# ═══════════════════════════════════════════════════════════════


# ── 1: FALSE DAWN / SUITE WINDOW ────────────────────────────────

label day104_1:

    $ time_manager.set_current_day(4)
    $ set_time_period("Morning")

    scene bg_master_suite_day
    with fade

    "Morning enters the Master Suite as if nothing terrible has ever happened there."
    "That is the talent of expensive rooms."
    "They reset themselves."

    "Gideon and Vance have gone to a matinee in the West End."
    "Stern believes I am polishing silver on the ground floor."
    "Missy believes I am avoiding her because guilt has finally made me decent."

    "Everyone is wrong in a useful direction."

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

    "The manuscript needs an ending."
    "Not a pretty one. Not a moral one."
    "An ending with enough truth inside it to bite."

    "I cross to the heavy oak writing desk."
    "The lockbox waits beneath a stack of correspondence, exactly where a careless man would not hide it and a confident man would."

    jump day104_1_lockbox_evidence


# ── 1: LOCKBOX / EVIDENCE ───────────────────────────────────────

label day104_1_lockbox_evidence:

    scene bg_master_suite_day
    with dissolve

    "The hairpin bends before the lock does."
    "My hands are slick. My breath is too loud."
    "Every sound in the room becomes Stern's footstep, Gideon's voice, Vance's laugh returning early down the hall."

    "Then the lock gives."

    "Inside: bank notes, a theatre programme, two folded letters, and an envelope stiff with photographic paper."

    "The photograph is not large."
    "That feels obscene somehow."
    "A life can fit on paper smaller than a prayer book."

    "Gideon. Another gentleman."
    "Not merely friendly. Not deniable in any honest room."

    "My first feeling is triumph."
    "My second is fear."
    "My third is the writer's monstrous little gratitude."

    "Here is the ending."
    "Here is the proof."
    "Here is the thing even Gideon Locke cannot smooth over with a quiet voice and a better coat."

    $ story.set_day4_evidence_discovered(True)
    $ apply_effects(vance_susp=15, insp=20, corr=0)

    "I slide the photograph beneath my bodice."
    "It scratches once against my skin and becomes real."

    jump day104_2_return_early


# ── 2: RETURN EARLY ─────────────────────────────────────────────

label day104_2_return_early:

    scene bg_master_suite_day
    with dissolve

    "A key turns in the outer door."

    vance "—and I will not tolerate that tone from her again. Not from a dresser, not from a maid, not from anyone."

    "They are early."
    "Of course they are early."
    "False dawns do not announce the trap. They simply let the sun in first."

    "I am standing beside Gideon's desk with his lockbox open and his ruin pressed against my ribs."

    menu:
        "Sixty seconds. How do I survive?"

        "Hide in the cold hearth. Keep the evidence. [[Ghost escape: high suspicion]]":
            jump day104_2_escape_fireplace

        "Stand in the room and lie cleanly. Keep the evidence. [[Prey escape: high visibility]]":
            jump day104_2_escape_bold_lie

        "Use Missy as cover. Lose the evidence, preserve the alibi. [[Predator escape: low suspicion, moral cost]]":
            jump day104_2_escape_missy_cover


# ── 2: ESCAPE — FIREPLACE ───────────────────────────────────────

label day104_2_escape_fireplace:

    scene bg_master_suite_day
    with dissolve

    $ story.set_day4_escape_state("fireplace")
    $ story.set_has_photograph(True)
    $ apply_effects(stern_susp=35, insp=5, corr=0)

    "The hearth is enormous, black, and unlit."
    "A servant could disappear there."
    "A desperate one does."

    "I close the lockbox, shove it beneath the correspondence, and crawl into the cold soot with the photograph against my chest."

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

    hide gideon_sprite
    hide vance_sprite

    "I slide out of the hearth blackened, shaking, alive."
    "The photograph is still mine."
    "So is the soot."

    jump day104_3_stern_pressure


# ── 2: ESCAPE — BOLD LIE ────────────────────────────────────────

label day104_2_escape_bold_lie:

    scene bg_master_suite_day
    with dissolve

    $ story.set_day4_escape_state("bold_lie")
    $ story.set_has_photograph(True)
    $ apply_effects(vance_susp=40, insp=10, corr=5)

    "I close the lockbox with one hand and seize the dust cloth with the other."
    "By the time the door opens, I am wiping the desk as if mahogany has personally insulted Miss Stern."

    show vance_sprite angry at left
    show gideon_sprite angry at right

    vance "What is she doing here?"

    "Gideon's eyes move from my face to the desk."
    "Then to my hands."
    "Then back to my face."

    gideon "That is my question."

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

    hide gideon_sprite
    hide vance_sprite

    "I go before my courage notices what it has done."

    jump day104_3_stern_pressure


# ── 2: ESCAPE — MISSY COVER ─────────────────────────────────────

label day104_2_escape_missy_cover:

    scene bg_master_suite_day
    with dissolve

    $ story.set_day4_escape_state("missy_cover")
    $ story.set_has_photograph(True)
    $ story.set_missy_day4_used_as_cover(True)
    $ apply_effects(vance_susp=-15, missy_susp=20, insp=5, corr=20)

    "Panic makes the first decision."
    "Ambition improves it."

    "I slide the photograph into my bodice and close the lockbox, leaving everything else exactly as I found it."
    "I have the proof."

    "I slip through the servants' door as the outer door opens."

    scene bg_servants_corridor_day
    with fade

    show missy_sprite shocked at center

    "Missy is in the corridor with a stack of towels."
    "Wrong place. Right time."
    "For me."

    cora "They need you in the suite. Now. Take this."

    "I push the dust cloth into her hands."

    missy "What? Who?"

    cora "Vance. She's asking for the room to be checked again. Hurry before she comes looking."

    "Missy looks toward the door."
    "She believes me because she still wants the world to contain fewer traps than it does."

    missy "All right."

    "She goes in."
    "The door closes."

    "I stand in the corridor with empty hands and a perfect alibi."
    "I have survived."
    "I have also failed the part of me that came for a weapon."

    jump day104_3_stern_pressure


# ── 3: STERN PRESSURE ───────────────────────────────────────────

label day104_3_stern_pressure:

    $ set_time_period("Evening")

    scene bg_servants_quarters_dusk
    with fade

    "By twilight, survival has begun charging interest."

    if story.day4_escape_state == "fireplace":
        "Soot sits beneath my nails, in the seams of my cuffs, along the hem where the apron should be clean."
        "Every black mark is a witness with no loyalty."
    elif story.day4_escape_state == "bold_lie":
        "Gideon saw me near the desk."
        "He may not know what I took."
        "He knows I took the right kind of risk."
    else:
        "Missy returned from the suite with red eyes and a voice pressed flat."
        "Vance had found shadow. Of course Vance had found shadow."  # (Note: revised to keep consistent text formatting)
        "I had handed her a target and called it haste."

    show stern_sprite stern at center

    stern "Cora."

    "Stern does not need evidence to suspect disorder."
    "She smells it the way laundresses smell mildew."

    stern "You were difficult to locate this afternoon."

    menu:
        "How do I handle Stern's pressure?"

        "Give her the boring servant answer. [[-Suspicion]]":

            $ story.set_day4_stern_response("boring")
            $ apply_effects(stern_susp=-15, insp=0, corr=0)

            cora "Ground-floor silver, Ma'am. Then linens. Then back stairs. I should have reported each change."

            stern "Yes. You should have."

            "She dislikes the answer because it gives her nothing but negligence."
            "Negligence is punishable."
            "It is also ordinary."

        "Let her see I am frightened, not guilty. [[+Inspiration, small suspicion]]":

            $ story.set_day4_stern_response("frightened")
            $ apply_effects(stern_susp=5, insp=10, corr=0)

            cora "I am trying not to make mistakes, Ma'am. That is making me slower."

            "Stern studies me."

            stern "Fear is useful only when it sharpens. Yours is beginning to spill."

            cora "Yes, Ma'am."

            stern "Clean it up."

        "Hide behind Missy if she was used. [[Conditional moral cost]]" if story.day4_escape_state == "missy_cover":

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

    hide stern_sprite

    "She leaves me with the warning and no proof."
    "Tonight, no proof is beginning to feel like grace."

    jump day104_4_twilight_ledger_false_dawn


# ── 4: TWILIGHT LEDGER / FALSE DAWN ─────────────────────────────

label day104_4_twilight_ledger_false_dawn:
    call check_confrontations

    scene bg_servants_quarters_dusk
    with dissolve

    $ show_ledger_ui()

    "The ledger sits open on my desk."
    "My hands have stopped shaking."
    "This feels like improvement until I realise they have only gone numb."

    "The photograph is hidden beneath the loose board under my bed."
    "Not safe."
    "Safer than my skin."
    "I have evidence."
    "I have leverage."
    "I have, for the first time since arriving, something Gideon Locke does not want me to have."

    "The manuscript waits."
    "Not for more material."
    "For courage."

    menu:
        "Perform visible penance to lower their guard. [[Atonement]]":
            jump day104_4_atonement

        "Risk the dark room to write the triumphant chapter. [[Triumphant Write]]" if player.anxiety < 85:
            jump day104_5_triumphant_chapter

        "Risk the dark room to write the triumphant chapter. [[Triumphant Write]]" if player.anxiety >= 85:
            "My hand shakes too violently to hold the pen. The hotel feels alive, every creaking floorboard a footstep, every shadow a reaching hand."
            "At this level of anxiety, my panic blocks the pen."
            jump day104_4_twilight_ledger_false_dawn

        "Find Missy and salvage what remains of her trust. [[Missy Repair]]" if getattr(story, "missy_day4_repair_state", "") == "":
            jump day104_4_missy_repair


# ── 4: ATONEMENT / SAFETY FIRST ─────────────────────────────────

label day104_4_atonement:

    scene bg_servants_quarters_dusk
    with dissolve

    $ story.set_day4_twilight_action("atonement")

    if story.day4_escape_state == "fireplace":
        $ apply_effects(stern_susp=-30, insp=0, corr=0)

        "I scrub soot from my apron until the water turns grey, then black, then grey again."
        "My knuckles split."
        "Good. Blood is easier to explain than chimney dust."

    elif story.day4_escape_state == "bold_lie":
        $ apply_effects(stern_susp=-25, insp=0, corr=0)

        "I sit in the laundry corner and mend cuffs with saintly dullness."
        "Anyone watching sees a maid trying very hard to become furniture."
        "That is the point."

    else:
        $ apply_effects(stern_susp=-10, insp=0, corr=0)

        "I fold linens."
        "I carry water."
        "I become useful in every visible way, which is not the same as becoming good."

    "The hour does what it can."
    "It lowers the heat on my neck."
    "But the manuscript remains untouched. I am too exhausted to write."

    jump day104_6_false_dawn_ending


# ── 4: MISSY REPAIR ─────────────────────────────────────────────

label day104_4_missy_repair:

    scene bg_servants_quarters_dusk
    with dissolve

    show missy_sprite shocked at center

    $ story.set_day4_twilight_action("missy_repair")
    $ apply_effects(missy_susp=-15, insp=5, corr=0)

    "Missy sits on the edge of her bed, twisting a handkerchief until it looks strangled."

    missy "You sent me in there."

    cora "Yes."

    "The word is smaller than the harm."

    missy "You knew they were angry."

    cora "Yes."

    "No lie comes."
    "That may be decency."
    "It may be exhaustion."

    missy "Why?"

    menu:
        "How much truth do I give her?"

        "Enough to keep her from hating me completely.":

            $ story.set_missy_day4_repair_state("partial_truth")
            $ apply_effects(missy_susp=-10, vance_susp=5, insp=10, corr=0)

            cora "Because I found something I should not have found. And I panicked."

            missy "Something of his?"

            cora "Yes."

            missy "Was it worth it?"

            "No answer is safe."

            cora "I don't know yet."

        "Keep the truth. Offer comfort instead.":

            $ story.set_missy_day4_repair_state("comfort_lie")
            $ apply_effects(missy_susp=-15, insp=0, corr=5)

            cora "Because I am a coward when cornered."

            missy "That is not an answer."

            cora "No. But it is true."

            "She lets me sit beside her."
            "Not forgiveness."
            "A pause before judgment."

    hide missy_sprite

    "When I return to my room, the emotional toll weighs heavier than the fear."
    "I am safe, but the pen refuses to move. I cannot write tonight."

    jump day104_6_false_dawn_ending


# ── 5: TRIUMPHANT CHAPTER ───────────────────────────────────────

label day104_5_triumphant_chapter:
    call check_confrontations

    $ set_time_period("Night")

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

    $ story.complete_manuscript_chapter("day4_triumphant_chapter")
    $ apply_effects(stern_susp=15, insp=-15, corr=0)

    "The final sentence lands just before the candle dies."
    "For a while, I do not move."
    "It feels triumphant. It feels like an ending."
    "I mistake fiction for reality, believing that writing the victory makes it absolute."

    jump day104_6_false_dawn_ending


# ── 6: FALSE DAWN ENDING ────────────────────────────────────────

label day104_6_false_dawn_ending:

    $ set_time_period("Night")

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

    $ resolve_turn()

    if story.manuscript_progress < 2:
        jump game_over_deadline_2

    jump day105_1_monster_reemerges
