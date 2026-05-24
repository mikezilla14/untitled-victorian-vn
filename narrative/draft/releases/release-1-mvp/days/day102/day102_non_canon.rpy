# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes

# day102_non_canon.rpy
# Release 1 / Day 02 non-canon Ren'Py-shaped draft
# Source: promoted renpy_project/game/day102.rpy + writers' room divergent pool (day102)
# Spine: story_board.md Day 102; router via end_slot / advance_after_confrontation

# ==========================================
# DAY 2 NODE MAP
# ==========================================
# day102_1_cora_missy_first_shift -> missy_finds_a_thing
#   -> takes_the_thing [predator] / deceives_missy [prey|ghost]
# day102_2_day2_chore_time -> insp/corr -> optional chains -> evening crisis
# day102_3 stern -> vance -> coras_choice -> gideon
# day102_4_night -> write / indulge -> day103_morning


# ── 021: CORA + MISSY FIRST SHIFT ───────────────────────────────

label day102_1_cora_missy_first_shift:

    # [STATE] State/progression update
    $ time_manager.set_current_day(2)
    $ set_time_period("Morning")

    scene bg_master_suite_day
    with fade

    "The Master Suite is larger in daylight and less honest for it."
    "Breakfast has emptied the room of its occupants, but not of them."
    "Vance is in the perfume lingering over the dressing table. Mr. Locke is in the chair angled toward the hearth, as if the room itself has learned to obey him."
    "The rich do not only leave crumbs."
    "They leave proof that someone lived loudly while pretending not to."

    # [ASSET] Visual/staging command
    show missy_sprite smiling at center

    missy "Best room in the hotel, this one. Best view, best rugs, best chance of being shouted at for breathing wrong."

    cora "You make it sound almost desirable."

    missy "Oh, it is. You should see the breakfast trays. Kippers. Proper marmalade. Eggs with little hats on."

    "She says this while hauling damp linen into a basket twice her width."
    "The rich leave more behind than crumbs. They shed evidence."

    if story.day1_night_action == "visit_missy":
        "Missy glances at me more softly than she did yesterday."
        "Last night's kindness, or something close enough to be mistaken for it, still has a little weight between us."
    elif story.day1_corridor_state == "predator":
        "Missy is bright with me, but not unguarded."
        "Something in her remembers the service door, even if she has not yet decided what to call it."
    else:
        "Missy moves as if yesterday can be folded away with the linen."
        "I envy the trick. I do not share it."

    missy "You take the hearth. I'll see to the armoire. If anything bites, shout."

    cora "Does anything bite?"

    missy "In this room? Probably the pillows."

    "I kneel at the hearth and brush yesterday's ash into a pan."
    "The work should empty the mind."
    "It does not."

    # [STATE] State/progression update
    jump day102_1_missy_finds_a_thing


label day102_1_missy_finds_a_thing:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show missy_sprite smiling at center

    "There is a soft clatter behind me."
    "Not porcelain. Not metal. Something lighter. A hatbox giving up its secret."

    # [ASSET] Visual/staging command
    show missy_sprite confused at center

    missy "Cora?"

    "Missy's voice has lost its shine."

    cora "What is it?"

    missy "I don't know. I mean, I know it's clothing. I think."

    "She holds it up with two fingers."
    "Sheer lace. Expensive, intimate, and designed with no interest whatsoever in modesty."
    "The lace is lighter than it has any right to be."
    "Intimate things argue with a room's pretence of respectability."

    "The room seems to narrow around the thing."
    "Vance's fury from yesterday. Gideon's quiet command. The service door. The sound through plaster."
    "All of it becomes touchable."

    missy "What sort of lady owns something like this?"

    "The correct answer is: more ladies than Missy has been permitted to imagine."
    "The useful answer depends on what I am becoming."

    cora "The sort who does not expect a maid to find it before luncheon."

    "Missy considers this."
    "It does not help."

    if story.day1_corridor_state == "predator":

        # [STATE] State/progression update
        jump day102_1_cora_takes_the_thing
    else:

        # [STATE] State/progression update
        jump day102_1_cora_deceives_missy


label day102_1_cora_takes_the_thing:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show missy_sprite confused at center

    $ story.set_day2_contraband_state("stolen_wearing")
    $ apply_effects(susp=5, insp=0, corr=15)

    cora "Give it here."

    missy "Shouldn't we put it back?"

    cora "We should not stand in the middle of a guest's room holding it like a banner."

    "That is not an answer. It is close enough to one."
    "Missy hands it over."

    "The lace is lighter than guilt should be."
    "I cross into the washroom before Missy can form a second question."

    missy "Cora?"

    cora "Keep folding."

    "Behind the half-closed door, I remove my plain cotton and step into the stolen thing."
    "Every breath is a wager."
    "The uniform still looks obedient from the outside."
    "It sits beneath the uniform like a second, secret sentence."
    "The maid above. The witness below."

    "When I return, Missy looks at my empty hands."

    missy "Where is it?"

    cora "Safe."

    missy "That is not the same as proper."

    cora "In this house, proper is only what survives being noticed."

    "She does not like that."
    "Neither do I, particularly."
    "It remains true."

    # [STATE] State/progression update
    $ story.set_missy_day2_suspicion_state("uneasy")

    jump day102_2_day2_chore_time


label day102_1_cora_deceives_missy:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show missy_sprite confused at center

    $ story.set_day2_contraband_state("planted_in_trunk")
    $ apply_effects(susp=0, insp=5, corr=10)

    cora "Put it away. Quickly."

    missy "Back in the hatbox?"

    "The hatbox is the obvious place."
    "Obvious things are where blame waits."
    "A trunk is not a hiding place."
    "It is a question addressed to the man who owns it."

    cora "No. In the travel trunk. Deep enough that no one sees it by accident."

    missy "Mr. Locke's trunk?"

    cora "If it is private, it belongs with private things. If it is found loose, Stern will ask why we were careless."

    if story.day1_corridor_state == "prey":
        "I hear how desperate the logic sounds only after I have said it."
        "Yesterday he almost saw me at the door. Today I cannot afford another visible mistake."
    else:
        "The logic is clean."
        "That is the ugly part."

    missy "I suppose."

    "She crosses to the trunk and folds the lace beneath a layer of shirts."
    "Her hands perform the risk. Mine remain empty."

    missy "There."

    cora "Good."

    "She looks relieved."
    "I look useful."

    # [STATE] State/progression update
    $ story.set_missy_day2_suspicion_state("trusting")

    jump day102_2_day2_chore_time


# ── 022: DAY 2 CHORE TIME ───────────────────────────────────────

label day102_2_day2_chore_time:

    call check_confrontations

    # [STATE] State/progression update
    $ set_time_period("Afternoon")

    scene bg_servants_corridor_morning
    with dissolve

    "We escape the suite with the linen cart and the sort of silence that pretends nothing has happened."
    "The corridor is narrower than it was yesterday."

    # [ASSET] Visual/staging command
    show missy_sprite smiling at center

    if story.day2_contraband_state == "stolen_wearing":
        "The lace moves beneath my uniform with each step."
        "Heat and fear share the same pulse."
        "Every stair, every turn, every nod to passing staff becomes a private dare."
        "No one knows what I am carrying because I am carrying it as myself."
    else:
        "The lace remains upstairs, hidden in Gideon's trunk by Missy's hands and my instruction."
        "A fact placed in the wrong drawer is not a fact anymore. It is a trap with upholstery."

    missy "You are quiet."

    cora "I am working."

    missy "That's never stopped anyone from talking before."

    "She tries to smile."
    "It does not quite settle."

    # [STATE] State/progression update
    $ show_ledger_ui()

    menu:
        "How do I carry the morning?"

        "Work fast. Catalogue the room, the people, the risk. [[Inspiration]]":

            # [STATE] State/progression update
            jump day102_2_day2_insp_choice

        "Linger near the danger. Let the secret sharpen itself. [[Corruption]]":

            # [STATE] State/progression update
            jump day102_2_day2_corr_choice


label day102_2_day2_insp_choice:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_morning
    with dissolve

    show missy_sprite smiling at center

    $ story.set_day2_chore_focus("inspiration")
    $ apply_effects(susp=-5, insp=15, corr=0)

    "I make the morning into inventory."
    "The direction of the light in the suite. The scent of Vance's powder. The exact stiffness in Missy's shoulders when she lies badly to herself."

    "A story cannot live on heat alone."
    "It needs furniture. It needs weather. It needs a servant who knows which board complains beneath a careless foot."

    missy "You look like you're counting things."

    cora "I am."

    missy "What things?"

    cora "Ways not to be dismissed before luncheon."

    missy "Oh. You'll need more fingers."

    "That gets a laugh out of me before I can stop it."
    "Missy notices."
    "For one small second, the house loses."

    # [STATE] State/progression update
    jump day102_2_optional_character_chain


label day102_2_day2_corr_choice:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_morning
    with dissolve

    show missy_sprite confused at center

    $ story.set_day2_chore_focus("corruption")
    $ apply_effects(susp=10, insp=0, corr=15)

    "I slow the cart near the guest wing."
    "There are always reasons. A folded towel not square enough. A dropped pin. A scuff on polished wood that may or may not exist."

    if story.day2_contraband_state == "stolen_wearing":
        "The stolen lace answers every step."
        "One wrong glance and the day becomes a different kind of day."
        "I should feel foolish. Instead, the uniform feels less like a prison and more like a disguise I have finally learned to use."
    else:
        "Upstairs, the lace waits where it should not be."
        "I imagine the trunk opened. The pause. The recalculation. Mr. Locke seeing the lie not as panic, but as intention."

    missy "Cora, we'll be missed."

    cora "Then push faster."

    missy "You were the one who slowed down."

    "There is a little steel in her now."
    "Good."
    "Or not good."
    "Useful, at least."

    # [STATE] State/progression update
    jump day102_2_optional_character_chain


label day102_2_optional_character_chain:

    # [CHOICE] Decision point
    menu:
        "The cart is still. The corridor has not forgotten yesterday."

        "Let Miss Stern find me near the linen closet." if story.chain_available("stern"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("stern")
            jump expression _chain_label

        "Steal an hour with Missy before Stern counts the sheets." if story.chain_available("missy"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("missy")
            jump expression _chain_label

        "Drift toward the Locke Suite and watch who performs for whom." if story.chain_available("vance"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("vance")
            jump expression _chain_label

        "Push the cart on and keep my hands honest.":
            if story.day2_chore_focus == "corruption":
                "Honesty is a word for people who are not wearing stolen lace."
                "I work in silence and call it restraint."
            else:
                "I count boards, hinges, and the distance between stairs."
                "Craft is safer when it has no audience."
            "The house loses interest when I stop offering it a face."
            call end_slot(outcome="d2_reflect_done")


# ── 023: STERN FETCHES CORA ─────────────────────────────────────

label day102_3_stern_fetches_cora:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_day
    with dissolve

    show stern_sprite stern at center

    "Stern finds me at the foot of the servants' stair."
    "She does not raise her voice."
    "That is how I know the matter is already dangerous."
    "Somewhere above us, a clock marks the interval between discovery and punishment."

    stern "Cora. Upstairs."

    cora "Ma'am?"

    stern "Do not make me repeat myself."

    "Her eyes flick once toward my hands. Empty. Then my face. Too still."

    stern "There is a complaint from the Master Suite. You were assigned there this morning."

    "Behind her, Missy has gone pale."

    if story.missy_day2_suspicion_state == "uneasy":
        "She knows I took it. Or knows enough to fear knowing."
    else:
        "She trusts me enough to be frightened for both of us."

    stern "Both of you. Move."

    # [STATE] State/progression update
    jump day102_3_vance_goes_incandescent


label day102_3_vance_goes_incandescent:

    # [ASSET] Visual/staging command
    scene bg_master_suite_tea
    with fade

    show vance_sprite angry at left
    show stern_sprite stern at center
    show missy_sprite shocked at right

    "The Master Suite has become a courtroom without chairs."

    "Vance stands by the armoire, one hand clenched around the edge of a hatbox."
    "Her face is controlled so tightly that the control itself has become indecent."

    vance "Something has been taken."

    stern "Madam, I assure you—"

    vance "Do not assure me. Find it."

    "Missy inhales too sharply."
    "Vance hears it."

    vance "You."

    missy "Madam?"

    vance "You were here. Both of you were here."

    "Her eyes move to me."
    "Yesterday she saw a maid. Today she sees a possible thief."
    "That is progress of a kind."

    if story.day2_contraband_state == "stolen_wearing":
        "The missing object is under my skirt."
        "The absurdity of it threatens to become laughter, which would be fatal."
    else:
        "The missing object is hidden in a trunk a few feet away."
        "Missy placed it there. I made that true."

    vance "I will not have servants pawing through my private things."

    "Private."
    "The word enters the room wearing gloves and entirely the wrong shoes."

    stern "Cora. Missy. If either of you has any knowledge of this matter, speak now."

    "Speak now."
    "As if truth from below stairs were ever heard before the floor above it decided."

    # [STATE] State/progression update
    jump day102_3_coras_choice


label day102_3_coras_choice:

    # [CHOICE] Decision point
    menu:
        "What do I do?"

        "Confess enough to control the damage. [Prey: visible risk, cleanest conscience]":

            # [STATE] State/progression update
            jump day102_3_cora_confesses

        "Produce it as if discovering it now. [Predator: controlled lie]":

            # [STATE] State/progression update
            jump day102_3_cora_pretends_to_find_it

        "Let Missy take the shape of the blame. [Ghost: clean hands, dirty outcome]":

            # [STATE] State/progression update
            jump day102_3_cora_frames_missy


label day102_3_cora_confesses:

    # [ASSET] Visual/staging command
    scene bg_master_suite_tea
    with dissolve

    show vance_sprite angry at left
    show stern_sprite stern at center
    show missy_sprite shocked at right

    $ story.set_day2_tea_choice("prey")
    $ apply_effects(susp=20, insp=15, corr=0)

    "The truth is not safe."
    "That does not make the lie safer."

    cora "Ma'am. I saw the item this morning."

    "Missy's head turns toward me."

    vance "You saw it."

    cora "Yes, Ma'am. I did not understand whether it had been left aside for laundering or packed in error. I should have reported it to Miss Stern at once."

    stern "Yes. You should have."

    "Stern's voice could cut thread."

    if story.day2_contraband_state == "stolen_wearing":
        "The lace remains beneath my uniform."
        "My confession is therefore not truth, but a smaller lie dressed as truth."
        "Still, it stands closer to honesty than anything else I have available."
        "My pulse does not agree with my mouth."
    else:
        "I do not look at the trunk."
        "Looking would condemn Missy before I choose whether I mean to."

    vance "Where is it?"

    cora "I cannot say for certain, Ma'am. I only know I failed to report it."

    "A bad answer."
    "A brave answer."
    "The two are cousins."

    # [STATE] State/progression update
    jump day102_3_gideon_interrupts_controls_vance


label day102_3_cora_pretends_to_find_it:

    # [ASSET] Visual/staging command
    scene bg_master_suite_tea
    with dissolve

    show vance_sprite angry at left
    show stern_sprite stern at center
    show missy_sprite shocked at right

    $ story.set_day2_tea_choice("predator")
    $ apply_effects(susp=10, insp=5, corr=15)

    "Helpful."
    "That is the mask."
    "Helpful girls are allowed to cross rooms that guilty girls are not."

    cora "Pardon me, Madam. May I check where the morning things were placed?"

    vance "Do you imagine I have not looked?"

    cora "No, Madam. Only that servants often look in servant ways."

    "Stern's eyes sharpen."
    "Stern's mouth tightens by a fraction."
    "That is the Savoy equivalent of laughter."
    "Too much intelligence. But the door is already open."

    if story.day2_contraband_state == "planted_in_trunk":
        "I cross to the travel trunk."
        "Missy makes a tiny sound."
        "I lift one folded shirt, then another, then pause as though surprised by what my hand has discovered."

        cora "Is this the item, Madam?"

        "I hold up the lace carefully."
        "Missy looks as if I have pulled her own heart from the trunk."

    elif story.day2_contraband_state == "stolen_wearing":
        "I cross to the armoire and open the hatbox."
        "My body is a locked drawer. The room must not know it."
        "A second small lace ribbon lies caught under the hatbox lining."
        "Not the garment itself."
        "Enough to teach the room the wrong lesson."

        cora "There is a loose piece here, Madam. Perhaps the rest was misplaced while packing."

        "It is not enough."
        "It is almost enough."
        "In a room this frightened, almost can work."

    else:
        "I cross to the armoire and make a show of checking beneath the hatbox."
        cora "Might this be it, Madam?"

    vance "Give it to me."

    "I do."
    "Our fingers do not touch."

    # [STATE] State/progression update
    jump day102_3_gideon_interrupts_controls_vance


label day102_3_cora_frames_missy:

    # [ASSET] Visual/staging command
    scene bg_master_suite_tea
    with dissolve

    show vance_sprite angry at left
    show stern_sprite stern at center
    show missy_sprite shocked at right

    $ story.set_day2_tea_choice("ghost")
    $ story.set_missy_day2_trust_break(True)
    $ apply_effects(susp=0, insp=0, corr=20)

    "There is a version of me that protects Missy."
    "She exists."
    "She is simply not the one who speaks first."

    cora "Missy handled it this morning, Ma'am."

    missy "Cora—"

    stern "Quiet."

    "Missy's mouth closes."
    "The betrayal arrives in her eyes before the fear does."

    cora "I did not know whether she had been instructed to move it. It was not my place to question a senior maid's handling of the room."

    missy "I only did what you said."

    vance "What she said?"

    "The room turns toward me."
    "I let confusion rise slowly, carefully, with no panic in it."

    cora "I told her not to leave private garments exposed, Madam. I did not instruct her to hide anything."

    "Every word is shaped to be defensible."
    "That is how cowards build knives with ivory handles."

    missy "That's not—"

    stern "Enough."

    "Missy stops."
    "She has already learned the house's first lesson: truth without rank is noise."

    # [STATE] State/progression update
    jump day102_3_gideon_interrupts_controls_vance


label day102_3_gideon_interrupts_controls_vance:

    # [STATE] State/progression update
    $ set_time_period("Evening")

    scene bg_master_suite_tea
    with dissolve

    show vance_sprite angry at left
    show stern_sprite stern at center
    show gideon_sprite cold at right

    "The door opens without a knock."
    "Mr. Locke enters as if the argument has been waiting for his permission to exist."

    gideon "Vance."

    "That is all."
    "It is enough."

    # [ASSET] Visual/staging command
    show vance_sprite cowed at left

    vance "Something was taken from my things."

    gideon "So I gather. The corridor can hear you gathering it."

    "Vance's colour changes."
    "Not shame, exactly. More intimate than that. A correction landing where others cannot see it."

    if story.day2_tea_choice == "prey":

        gideon "You."

        cora "Yes, Sir."

        gideon "You saw the item and failed to report it."

        cora "Yes, Sir."

        gideon "Yet you report your failure now."

        "His attention is not warm."
        "It is worse. It is precise."

        cora "That is correct, Sir."

        gideon "Interesting choice."

        stern "Sir, I can have the girl dismissed—"

        gideon "No."

        "Stern stops."

        gideon "A dismissal makes noise. We are finished with noise for today."

        "He does not spare me."
        "He spares the hotel's reputation, which is the same thing with better upholstery."

        "His eyes remain on me one beat too long."
        "I have not escaped notice."
        "I have been filed."

    elif story.day2_tea_choice == "predator":

        if story.day2_contraband_state == "planted_in_trunk":
            "Mr. Locke looks at the lace, then at the trunk, then at me."
        else:
            "Mr. Locke looks at the hatbox, then at my perfectly folded hands."

        "He understands too quickly."
        "Men like him do not need proof when pattern will do."

        gideon "Thank you. Leave it there."

        cora "Yes, Sir."

        vance "Thank her? She—"

        gideon "Found what you misplaced."

        "He has chosen which story the afternoon will believe."

        "Vance goes still."
        "The correction is mild enough to be polite and sharp enough to draw blood."

        gideon "You will not punish the staff for your embarrassment."

        "My gaze stays on the carpet."
        "The carpet is expensive enough to hide several sins."

        "He knows I lied."
        "He has chosen to make the lie useful."

    else:

        "Mr. Locke's gaze passes over Missy first."
        "She is pale. Terrified. Guilty-looking in the way frightened people always look guilty to those searching for a culprit."

        "Then he looks at me."
        "I am calm."
        "Too calm, perhaps."

        gideon "Miss Stern, you will not conduct an inquest in a guest room."

        stern "Sir."

        vance "But she—"

        gideon "Has been frightened enough to become useless for the afternoon. That is poor management, not justice."

        "Missy's eyes fill."
        "She does not cry."
        "That is the worst of it."

        gideon "Send the girl below. Send Cora back to work. I will discuss the rest with Miss Vance privately."

        "Privately."
        "Vance hears the word and obeys before any hand moves."

        "His eyes touch mine for the smallest fraction of time."
        "He has not believed me."
        "He has not exposed me."
        "He is keeping a note."
        "This is not mercy."
        "It is investment."

    gideon "That will be all."

    # [ASSET] Visual/staging command
    hide gideon_sprite
    hide vance_sprite
    hide stern_sprite

    scene bg_servants_corridor_day
    with fade

    show missy_sprite shocked at center

    "The corridor receives us like a throat swallowing something sharp."

    if story.day2_tea_choice == "ghost":
        missy "How could you?"

        "There are many possible answers."
        "None are small enough to fit in the corridor."

        cora "Not here."

        missy "No. Not anywhere."

        # [ASSET] Visual/staging command
        hide missy_sprite

        "She leaves me beside the cart."
        "That, too, is material."
        "I hate myself for knowing it."

    elif story.day2_tea_choice == "predator":
        missy "You knew where it was."

        cora "I guessed."

        missy "No, you didn't."

        "There is accusation in her voice now."
        "Also awe."
        "I am not sure which is more dangerous."

        # [ASSET] Visual/staging command
        hide missy_sprite

    else:
        missy "You stepped forward."

        cora "Someone had to."

        missy "No one ever has to. That's what makes it something."

        "She says it simply, which makes it unbearable."

        # [ASSET] Visual/staging command
        hide missy_sprite

    if story.manuscript_progress == 0:
        "Tonight I must write."
        "Two days inside the machine and not a single finished chapter would be its own kind of defeat."
    else:
        "Tonight I must decide whether the second chapter deserves the truth or the better lie."

    # [STATE] State/progression update
    jump day102_4_night


# ── 024: NIGHT — WRITE OR INDULGE ───────────────────────────────

label day102_4_night:

    call check_confrontations

    # [STATE] State/progression update
    $ set_time_period("Night")

    scene bg_cora_desk_night
    with dissolve

    "The candle takes reluctantly."
    "For a moment the room is only wick, breath, and the small circle of light I can afford."

    "My ledger lies open."
    "My page waits beside it."
    "One records appetite. The other pretends to tame it."

    # [STATE] State/progression update
    $ show_ledger_ui()

    menu:
        "What do I do with the night?"

        "Write. Turn the suite into fiction before it rots. [Manuscript progress]":

            # [STATE] State/progression update
            jump day102_4_cora_writes_a_chapter

        "Do not write. Stay inside the feeling a little longer. [[Indulgence]]":

            # [STATE] State/progression update
            jump day102_4_cora_sneaks_a_feel


label day102_4_cora_writes_a_chapter:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    $ story.set_day2_night_action("write")

    if story.manuscript_progress == 0:

        if has_story_fuel(15):

            "Chapter One comes late, but it comes with teeth."

            if story.day1_corridor_state == "predator":
                "I write a maid who learns that other people's innocence can open doors her own hands must not touch."
            elif story.day1_corridor_state == "prey":
                "I write a maid caught at the threshold, exposed by the very hunger that brought her there."
            else:
                "I write a maid who hears enough through walls to understand the architecture of power."

            "The prose is raw."
            "Good. Raw things bleed honestly."

            # [STATE] State/progression update
            $ story.complete_manuscript_chapter("day1_chapter")
            $ apply_effects(susp=0, insp=-10, corr=0)

            "Chapter One is done."
            "Late is not failure."
            "Blank is failure."

        else:

            "I try to begin with the corridor."
            "Then the suite."
            "Then Missy's face."
            "Each beginning collapses into accusation."

            "I do not yet have enough material."
            "Or I have too much and no discipline."
            "The page does not care which excuse I prefer."

    else:

        if has_story_fuel(30):

            "Chapter Two begins with a hatbox."
            "Not the object inside."
            "The pause before it is opened."

            if story.day2_tea_choice == "prey":
                "I write a woman who tells one clean portion of the truth and lets everyone mistake that portion for the whole."
                "Her honesty does not save her."
                "It places her exactly where the dangerous man can see her."

            elif story.day2_tea_choice == "predator":
                "I write a woman who discovers that a lie told calmly can become furniture."
                "People walk around it. Lean on it. Arrange the room to suit it."
                "By the end of the chapter, even the gentleman is using her falsehood as if he ordered it built."

            else:
                "I write a woman who survives by leaving fingerprints on other people."
                "No blood on her cuffs."
                "No proof in her pocket."
                "Only a girl in the corridor learning what betrayal sounds like when it does not raise its voice."

            # [STATE] State/progression update
            $ story.complete_manuscript_chapter("day2_chapter")
            $ apply_effects(susp=0, insp=-15, corr=0)

            "By the time the candle shortens, the second chapter exists."
            "It is better than the first."
            "That is not comforting."

        else:

            "I write three sentences and cross them out."
            "The scene is still too close to me."
            "Vance's fury. Gideon's correction. Missy's face. The lace under cloth or hidden in the trunk."
            "None of it has become art yet."
            "It remains appetite and consequence."

    call end_slot(outcome="d2_write_night")


label day102_4_cora_sneaks_a_feel:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    $ story.set_day2_night_action("indulge")
    $ apply_effects(susp=10, insp=5, corr=15)

    "I close the notebook."
    "The page has asked for discipline."
    "I am tired of discipline."

    if story.day2_contraband_state == "stolen_wearing":

        "I stand before the little mirror above the washstand."
        "The uniform is plain. Severe. Designed to erase the body beneath it."
        "I lift the hem only enough to confirm the secret is still mine."

        "The lace is ridiculous."
        "That is part of its power."

        "The mirror gives back a maid."
        "The skin beneath disagrees."

        "A woman can scrub ash from a stranger's hearth while carrying a private scandal beneath her skirt."
        "A woman can be unseen and still not be innocent."

        "I lower the hem."
        "The maid returns."
        "The witness remains."

    else:

        "There is nothing in my hands tonight."
        "The dangerous thing is upstairs, hidden where I told Missy to hide it."
        "That should make it less present."
        "It does not."

        "I replay the afternoon until the room rearranges itself around Gideon's entrance."
        "Vance's fury contained. Stern's authority paused. Missy's fear made useful."
        "And me, small enough to be overlooked until I was not."

        "No chapter comes."
        "Only heat stored where ink should have gone."
        "Only the knowledge that I could have written and chose instead to keep feeling."

    "When I finally sleep, the candle has burned lower than I meant to allow."
    "Waste has consequences."

    call end_slot(outcome="d2_write_night")

# Promotion note: deadline gate lives on day103.rpy label day103_morning (via end_slot d2_write_night).
