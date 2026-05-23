# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes

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
    "My hands are slick. My breath is too loud."
    "Every sound in the room becomes Stern's footstep, Gideon's voice, Vance's laugh returning early down the hall."

    "Then the lock gives."

    "Inside: bank notes, a theatre programme, two folded letters, and an envelope stiff with photographic paper."

    # [ASSET] CG callout retained from legacy draft
    # show cg_gideon_photograph

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

    vance "—and I will not tolerate that tone from her again. Not from a dresser, not from a maid, not from anyone."

    "They are early."
    "Of course they are early."
    "False dawns do not announce the trap. They simply let the sun in first."

    "I am standing beside Gideon's desk with his lockbox open and his ruin pressed against my ribs."

    # [CHOICE] Decision point
    menu:
        "Sixty seconds. How do I survive?"

        "Hide in the cold hearth. Keep the evidence. [Ghost escape: high suspicion]":

            # [STATE] State/progression update
            jump day104_2_escape_fireplace

        "Stand in the room and lie cleanly. Keep the evidence. [Prey escape: high visibility]":

            # [STATE] State/progression update
            jump day104_2_escape_bold_lie

        "Use Missy as cover. Lose the evidence, preserve the alibi. [Predator escape: low suspicion, moral cost]":

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
    $ apply_effects(vance_susp=35, insp=5, corr=0)

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

    "Panic makes the first decision."
    "Ambition improves it."

    "I slide the photograph into my bodice and close the lockbox, leaving everything else exactly as I found it."
    "I have the proof."

    "I slip through the servants' door as the outer door opens."

    # [ASSET] Visual/staging command
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

        "Give her the boring servant answer. [-Suspicion]":

            # [STATE] State/progression update
            $ story.set_day4_stern_response("boring")
            $ apply_effects(stern_susp=-15, insp=0, corr=0)

            cora "Ground-floor silver, Ma'am. Then linens. Then back stairs. I should have reported each change."

            stern "Yes. You should have."

            "She dislikes the answer because it gives her nothing but negligence."
            "Negligence is punishable."
            "It is also ordinary."

        "Let her see I am frightened, not guilty. [+Inspiration, small suspicion]":

            # [STATE] State/progression update
            $ story.set_day4_stern_response("frightened")
            $ apply_effects(stern_susp=5, insp=10, corr=0)

            cora "I am trying not to make mistakes, Ma'am. That is making me slower."

            "Stern studies me."

            stern "Fear is useful only when it sharpens. Yours is beginning to spill."

            cora "Yes, Ma'am."

            stern "Clean it up."

        "Hide behind Missy if she was used. [Conditional moral cost]" if story.day4_escape_state == "missy_cover":

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
    "Tonight, no proof is beginning to feel like grace."

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

    # [CHOICE] Decision point
    menu:
        "Perform visible penance to lower their guard. [Atonement]":

            # [STATE] State/progression update
            jump day104_4_atonement

        "Risk the dark room to write the triumphant chapter. [Triumphant Write]" if player.suspicion < 85:

            # [STATE] State/progression update
            jump day104_5_triumphant_chapter

        "Risk the dark room to write the triumphant chapter. [Triumphant Write]" if player.suspicion >= 85:
            "My hand shakes too violently to hold the pen. The hotel feels alive, every creaking floorboard a footstep, every shadow a reaching hand."
            "At this level of anxiety, my panic blocks the pen."

            # [STATE] State/progression update
            jump day104_4_twilight_ledger_false_dawn

        "Find Missy and salvage what remains of her trust. [Missy Repair]" if getattr(story, "missy_day4_repair_state", "") == "":

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
        $ apply_effects(stern_susp=-15, vance_susp=-15, insp=0, corr=0)

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

    # [CHOICE] Decision point
    menu:
        "How much truth do I give her?"

        "Enough to keep her from hating me completely.":

            # [STATE] State/progression update
            $ story.set_missy_day4_repair_state("partial_truth")
            $ apply_effects(missy_susp=-10, vance_susp=5, insp=10, corr=0)

            cora "Because I found something I should not have found. And I panicked."

            missy "Something of his?"

            cora "Yes."

            missy "Was it worth it?"

            "No answer is safe."

            cora "I don't know yet."

        "Keep the truth. Offer comfort instead.":

            # [STATE] State/progression update
            $ story.set_missy_day4_repair_state("comfort_lie")
            $ apply_effects(missy_susp=-15, insp=0, corr=5)

            cora "Because I am a coward when cornered."

            missy "That is not an answer."

            cora "No. But it is true."

            "She lets me sit beside her."
            "Not forgiveness."
            "A pause before judgment."

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

    # [BEAT] Recalled escape moment — the method of survival shapes what "having the knife" means
    if story.day4_escape_state == "fireplace":
        "I still feel the grate. Cold stone. Soot. The particular humiliation of pressing myself smaller than a flue."
        "I made myself nothing and emerged on the far side of the corridor with charcoal on my apron and the chapter already complete in my head."
        "The book was always going to come out of that contraction."
    elif story.day4_escape_state == "bold_lie":
        "I said something outrageous and watched it land."
        "Not because they believed me. Because challenging it required effort, and men in that room reserved effort for things that mattered."
        "I was not yet a thing that mattered enough to disprove. That is the armour this chapter writes itself inside."
    elif story.day4_escape_state == "missy_cover":
        "I sent her in first."
        "The corridor, the door, the timing."
        "The manuscript gets the chapter it demanded. Missy got the corridor she did not ask for."
        "That sentence must go somewhere. Here, in this chapter, it becomes a flaw with a purpose. Whether that is craft or rationalisation the page has not yet decided."
    else:
        "The escape has already become story."
        "The fear is still here. But the shape of it is cleaner now."

    # [BEAT] The knife — physical evidence vs memory
    if story.has_photograph:
        "The photograph is under the loose board beneath my bed."
        "Physical evidence. Something that can be held, shown, placed on a table and left to do its own harm."
        "I have a knife. Tonight I write what it looks like when a maid who has a knife is not afraid of it."
    else:
        "I have no paper to place between us. Only the image I carried out in my head instead of my apron pocket."
        "Memory without documentation. The chapter must convince itself that this is enough."
        "Tonight it will manage. Tomorrow Gideon will explain otherwise."

    "The chapter comes all at once."
    "Not because it is easy."
    "Because I finally understand the shape of the threat, and understanding is a kind of violence."

    # [BEAT] The chapter's content — archetype-specific false triumph
    # Primary branch on day2_tea_choice as the dominant moral frame for the story Cora is telling herself
    if story.day2_tea_choice == "predator":
        "In this chapter, the maid's composed lie becomes the only true sentence in the room."
        "She placed the dangerous thing where the dangerous man could find it and be grateful to her for finding it."
        "She said servant ways in a voice that meant something else, and he heard both meanings and chose the useful one."
        if story.day3_brush_choice == "predator":
            "In the mirror she named the seated woman's weakness with the precision of a naturalist."
            "On the page, that answer is her origin: the maid already understood the room before the gentleman finished furnishing it."
        elif story.day3_brush_choice == "prey":
            "She looked at him in the mirror when she should have looked at the lady, and the chapter decides this was strategy too."
            "The chapter is not entirely honest with itself here. Neither is she."
        else:
            "She dropped the brush and saw the room from the floor, and the chapter finds this consistent: she collects views that polished boots cannot reach."
        "The heroine in this chapter wins by being too useful to destroy and too observant to lie to without cost."

    elif story.day2_tea_choice == "prey":
        "In this chapter, the maid's partial truth becomes the sharper weapon."
        "She admitted what she saw and did not admit where she had stood to see it."
        "The gentleman recognised the gap and called it interesting. The chapter calls the gap the entire point."
        if story.day3_brush_choice == "predator":
            "In the mirror she answered clinically and he called it well. The heroine in this chapter wins through accuracy: her eye is better than his secrets."
        elif story.day3_brush_choice == "prey":
            "She was seen and let herself be seen, and this chapter insists that visibility chosen is different from visibility imposed."
            "That may even be true. The chapter believes it with more conviction than Cora does, tonight, writing it."
        else:
            "She retrieved the brush and called herself clumsy and kept the low angle. The chapter calls her restraint precision."
        "The heroine in this chapter wins because her honesty is more carefully edited than his lies."

    elif story.day2_tea_choice == "ghost":
        "In this chapter, the maid disappears between the accusation and the conviction."
        "Her hands are empty. Another girl's hands are where the blame landed."
        "She moved through the room like weather and the room forgot she had a shape."
        if story.day3_brush_choice == "predator":
            "In the mirror she was composed and direct, and in the corridor she was nowhere."
            "The chapter finds no contradiction in this. It may be wrong."
        elif story.day3_brush_choice == "prey":
            "She was too visible in the mirror and too absent in the corridor. The chapter says this is her range: she can be whatever the room requires."
        else:
            "She dropped the brush and vanished below the line of sight. The chapter calls both moments the same technique at different scales."
        "The heroine in this chapter wins because she is never precisely where the accusation points."

    else:
        "In this chapter, the maid uses what she found."
        "She gathered it, kept it, brought it out into the light, and named it correctly."
        "The chapter calls this sufficient."

    # [BEAT] The photograph in the chapter — the specific weapon and its specific limit
    if story.has_photograph:
        "The lord's sealed secret. The maid carrying it out in an apron pocket."
        "In this chapter, this is enough. The evidence is categorical. His denial would require an audience willing to call it perjury."
        "The chapter does not yet know that the audience must also be willing to hear the maid."
    else:
        "The lord's secret is real. The maid knows it, remembers it, has written it in clean declarative sentences."
        "In this chapter, memory is the same as evidence."
        "The chapter believes this completely. Tomorrow will be the first test of whether the world agrees."

    "The heroine defeats him completely. She is untouchable. She has won."

    # [STATE] State/progression update
    $ story.complete_manuscript_chapter("day4_triumphant_chapter")
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
