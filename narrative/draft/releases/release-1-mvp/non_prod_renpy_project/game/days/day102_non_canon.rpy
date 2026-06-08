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

# day102_non_canon.rpy
# Release 1 / Day 02 non-canon Ren'Py-shaped draft
# Source: promoted renpy_project/game/day102.rpy + writers' room divergent pool (day102)
# Spine: story_board.md Day 102; time-period routing via explicit day labels and dynamic windows

# ==========================================
# DAY 2 NODE MAP
# ==========================================
# day102_1_cora_missy_first_shift -> missy_finds_a_thing
#   -> takes_the_thing [predator] / deceives_missy [prey|ghost]
# day102_2_day2_chore_time -> insp/corr -> optional chains -> evening crisis
# day102_3 stern -> vance -> coras_choice -> gideon
# day102_4_night -> write / indulge -> day103_morning


# ── 021: CORA + MISSY FIRST SHIFT ───────────────────────────────

# [DAG_NODE id=day102_1_cora_missy_first_shift type=work day=102]
label day102_1_cora_missy_first_shift:

    # [STATE] State/progression update
    $ time_manager.set_current_day(2)
    $ set_time_period("Morning")

    scene bg_master_suite_day:
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with fade

    cora_inner "The Master Suite is larger in daylight and less honest for it."
    cora_inner "Breakfast has emptied the room of its occupants, but not of them."
    cora_inner "Vance is in the perfume lingering over the dressing table. Mr. Locke is in the chair angled toward the hearth, as if the room itself has learned to obey him."
    cora_inner "The rich do not only leave crumbs."
    cora_inner "They leave proof that someone lived loudly while pretending not to."

    # [ASSET] Visual/staging command
    show missy_sprite smiling at centre_bust

    missy "Best room in the hotel, this one. Best view, best rugs, best chance of being shouted at by Miss Stern for breathing the air wrong."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show missy_sprite smiling at right_bust with move # [asset auto]
    cora "You make it sound almost desirable."

    missy "Oh, it is, in a terrible sort of way. You should see the breakfast trays they carry up. Kippers. Proper marmalade. Soft eggs with little hats on. It's like a different country, Cora. But if you linger too long looking at the drapes, they'll have you out on the street without a character."

    "She says this while hauling a damp sheet into a basket twice her width, her face flushed but her hands exact."
    cora_inner "An intelligent country girl who has decoded the Savoy's math: luxury is paid for by the invisibility of those who clean it."

    if story.day1_night_action == "visit_missy":
        cora_inner "Missy glances at me more softly than she did yesterday."
        cora_inner "Last night's kindness—a quiet conversation in the steam, a shared warning—still has a little weight between us."
    elif story.day1_corridor_state == "predator":
        cora_inner "Missy is bright with me, but her shoulders carry a subtle stiffness."
        cora_inner "Her sharp memory hasn't forgotten the service door, even if she has decided her defensive moral shield requires her to remain silent about it."
    else:
        cora_inner "Missy moves as if yesterday can be folded away with the linen."
        cora_inner "I envy the trick. I do not share it."

    missy "You take the hearth. I'll see to the armoire. If anything bites, shout. Miss Stern says a quiet maid is a safe maid, but I say a loud maid at least gets to keep her fingers."

    cora "Does anything bite?"

    missy "In a suite like this? Only the pride of the people who pay for it."

    cora_inner "I kneel at the hearth and brush yesterday's ash into a pan."
    cora_inner "The work should empty the mind."
    cora_inner "It does not."

    # [STATE] State/progression update
    jump day102_1_missy_finds_a_thing


# [DAG_NODE id=day102_1_missy_finds_a_thing type=work day=102]
label day102_1_missy_finds_a_thing:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day:
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with dissolve

    show missy_sprite smiling at centre_bust

    "There is a soft clatter behind me."
    "Not porcelain. Not metal. Something lighter. A hatbox giving up its secret."

    # [ASSET] Visual/staging command
    show missy_sprite confused at centre_bust

    missy "Cora?"

    "Missy's voice has lost its bright shine. It has become quiet, exceptionally focused, and deliberate."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show missy_sprite confused at right_bust with move # [asset auto]
    cora "What is it?"

    missy "I... I don't know. It was tucked behind the vanity hatbox. It isn't proper, Cora. It isn't proper at all."

    "She holds it up with two fingers, her touch cautious, her face flushed with a mix of moral alarm and highly focused interest."
    cora_inner "Sheer silk lace. Expensive, transgressive, and designed with no interest whatsoever in modesty."
    cora_inner "The white silk catches the daylight, lighter than it has any right to be."

    cora_inner "The room seems to narrow around the thing."
    cora_inner "Vance's fury from yesterday. Gideon's quiet command. The service door. The sound through plaster."
    cora_inner "All of it becomes touchable."

    missy "What sort of lady owns something like this? It's like... like a sin you can wear."

    cora_inner "Her religious register is active, a protective social shield drawn instantly to draw a line in the sand."
    cora_inner "But her questions show a sharp, decoding intellect trying to comprehend the private transgressions of the suites."

    cora "The sort who does not expect a maid to find it before luncheon."

    "Missy considers this, her gaze fixed on the sheer lace, her breathing turning slightly shallow."

    if story.day1_corridor_state == "predator":

        # [STATE] State/progression update
        jump day102_1_cora_takes_the_thing
    else:

        # [STATE] State/progression update
        jump day102_1_cora_deceives_missy


# [DAG_NODE id=day102_1_cora_takes_the_thing type=work day=102]
label day102_1_cora_takes_the_thing:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day:
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with dissolve

    show missy_sprite confused at centre_bust

    $ story.set_day2_contraband_state("stolen_wearing")
    $ apply_effects(vance_susp=5, insp=0, corr=15)

    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show missy_sprite confused at right_bust with move # [asset auto]
    cora "Give it here."

    missy "Shouldn't we put it back? If they discover it's gone..."

    cora "We should not stand in the middle of Mr. Locke's suite holding it like a banner. If Stern walks in now, we're both ruined."

    "Missy flinches, the practical danger silencing her."
    "She hands it over, her eyes lingering on my fingers."

    cora_inner "The lace is lighter than guilt should be."
    "I cross into the washroom before Missy can form another question."

    missy "Cora? What are you doing in there?"

    cora "Keep folding, Missy. Don't look toward the door."

    "Behind the half-closed door, I remove my plain, coarse cotton uniform and step into the stolen silk."
    cora_inner "Every breath is a wager against the fabric."
    cora_inner "It sits beneath the uniform like a secret, transgressive sentence."
    cora_inner "The maid above. The sovereign desire below."

    "When I return, Missy looks at my empty hands, her sharp eyes immediately cataloging the slight shift in my posture, the way the cotton uniform sits differently."

    missy "Where is it? You didn't..."

    cora "It is safe, Missy."

    missy "Safe is not the same as proper, Cora. There's a wicked draft in this room, and you look... different."

    "She knows. Or her sharp, sheltered observancy warns her that a boundary has been crossed."

    cora "In this house, proper is only what survives being noticed. We do what we must to keep our heads."

    "She doesn't like that. Her protective moral shield is bruised, her trust unsettled."

    # [STATE] State/progression update
    $ story.set_missy_day2_suspicion_state("uneasy")

    jump day102_2_day2_chore_time


# [DAG_NODE id=day102_1_cora_deceives_missy type=work day=102]
label day102_1_cora_deceives_missy:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day:
        xysize (1920, 1080)

    # [ASSET] Visual/staging command
    with dissolve

    show missy_sprite confused at centre_bust

    $ story.set_day2_contraband_state("planted_in_trunk")
    $ apply_effects(vance_susp=0, insp=5, corr=10)

    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show missy_sprite confused at right_bust with move # [asset auto]
    cora "Put it away. Quickly."

    missy "Back in the hatbox?"

    cora_inner "The hatbox is the obvious place."
    cora_inner "Obvious things are where Miss Stern's blame waits."
    cora_inner "A trunk is not a hiding place."
    cora_inner "It is a question addressed to the gentleman who owns it."

    cora "No. In Mr. Locke's travel trunk. Folded deep beneath his shirts. If Miss Stern finds it loose, she'll ask why we were careless."

    missy "Mr. Locke's trunk? But... Cora, that's prying into a gentleman's private property. If he catches us..."

    cora "He won't. Not if you fold it cleanly and slide it in. If it's found loose in the open vanity, Stern will have us both on the street. It's safety, Missy. For both of us."

    if story.day1_corridor_state == "prey":
        cora_inner "I hear how desperate the logic sounds only after I have said it."
        cora_inner "Yesterday he almost saw me at the door. Today I cannot afford another visible mistake."
    else:
        cora_inner "The logic is clean, and Missy's sharp mind parses the risk."

    missy "I suppose. It's better than Stern finding it."

    "She crosses to the trunk, her hands performing the risk, folding the lace carefully beneath a layer of his shirts."
    cora_inner "Her hands carry the precarity; mine remain clean."

    missy "There. Folded away. God forgive me if it's sin."

    cora "You did well. It's protection, not sin."

    cora_inner "She looks relieved, her trust intact, believing we have navigated a trap together."
    cora_inner "I look useful."

    # [STATE] State/progression update
    $ story.set_missy_day2_suspicion_state("trusting")

    jump day102_2_day2_chore_time


# ── 022: DAY 2 CHORE TIME ───────────────────────────────────────

# [DAG_NODE id=day102_2_day2_chore_time type=work day=102]
label day102_2_day2_chore_time:

    # [STATE] State/progression update
    $ set_time_period("Afternoon")

    call day102_afternoon_consequence_window

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_morning:
        xysize (1920, 1080) 

    # [ASSET] Visual/staging command
    with dissolve

    cora_inner "We escape the suite with the linen cart and the sort of silence that pretends nothing has happened."
    cora_inner "The corridor is narrower than it was yesterday."

    # [ASSET] Visual/staging command
    show missy_sprite smiling at centre_bust

    if story.day2_contraband_state == "stolen_wearing":
        cora_inner "The lace moves beneath my uniform with each step."
        cora_inner "Heat and fear share the same pulse."
        cora_inner "Every stair, every turn, every nod to passing staff becomes a private dare."
        cora_inner "No one knows what I am carrying because I am carrying it as myself."
    else:
        cora_inner "The lace remains upstairs, hidden in Gideon's trunk by Missy's hands and my instruction."
        cora_inner "A fact placed in the wrong drawer is not a fact anymore. It is a trap with upholstery."

    missy "You are quiet."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show missy_sprite smiling at right_bust with move # [asset auto]
    cora "I am working."

    missy "That's never stopped anyone from talking before."

    "She tries to smile."
    "It does not quite settle."

    # [STATE] State/progression update
    $ show_ledger_ui()

    # [DAG_CHOICE group=day102_2_day2_chore_time_menu_1]
    menu:
        "How do I carry the morning?"

        "Work fast. Catalogue the room, the people, the risk. [[Inspiration]]":

            # [STATE] State/progression update
            jump day102_2_day2_insp_choice

        "Linger near the danger. Let the secret sharpen itself. [[Corruption]]":

            # [STATE] State/progression update
            jump day102_2_day2_corr_choice


# [DAG_NODE id=day102_2_day2_insp_choice type=choice]
label day102_2_day2_insp_choice:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_morning
    with dissolve

    show missy_sprite smiling at centre_bust

    $ story.set_day2_chore_focus("inspiration")
    $ apply_effects(stern_susp=-5, insp=15, corr=0)

    cora_inner "I make the morning into inventory."
    cora_inner "The direction of the light in the suite. The scent of Vance's powder. The exact stiffness in Missy's shoulders when she lies badly to herself."

    cora_inner "A story cannot live on heat alone."
    cora_inner "It needs furniture. It needs weather. It needs a servant who knows which board complains beneath a careless foot."

    missy "You look like you're counting things."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show missy_sprite smiling at right_bust with move # [asset auto]
    cora "I am."

    missy "What things?"

    cora "Ways not to be dismissed before luncheon."

    missy "Oh. You'll need more fingers."

    cora_inner "That gets a laugh out of me before I can stop it."
    "Missy notices."
    cora_inner "For one small second, the house loses."

    # [STATE] State/progression update
    jump day102_afternoon_story_window


# [DAG_NODE id=day102_2_day2_corr_choice type=choice]
label day102_2_day2_corr_choice:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_morning
    with dissolve

    show missy_sprite smiling at centre_bust

    $ story.set_day2_chore_focus("corruption")
    $ apply_effects(vance_susp=10, insp=0, corr=15)

    cora_inner "I slow the cart near the guest wing."
    cora_inner "There are always reasons. A folded towel not square enough. A dropped pin. A scuff on polished wood that may or may not exist."

    if story.day2_contraband_state == "stolen_wearing":
        cora_inner "The stolen lace answers every step."
        cora_inner "One wrong glance and the day becomes a different kind of day."
        cora_inner "I should feel foolish. Instead, the uniform feels less like a prison and more like a disguise I have finally learned to use."
    else:
        cora_inner "Upstairs, the lace waits where it should not be."
        cora_inner "I imagine the trunk opened. The pause. The recalculation. Mr. Locke seeing the lie not as panic, but as intention."

    missy "Cora, we'll be missed."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show missy_sprite smiling at right_bust with move # [asset auto]
    cora "Then push faster."

    missy "You were the one who slowed down."

    cora_inner "There is a little steel in her now."
    cora_inner "Good."
    cora_inner "Or not good."
    cora_inner "Useful, at least."

    # [STATE] State/progression update
    jump day102_afternoon_story_window


# [DAG_NODE id=day102_2_optional_character_chain type=dynamic_window day=102 period=Afternoon window=story_chain returns_to=day102_2_day2_chore_time]
label day102_2_optional_character_chain:

    # [STATE] State/progression update
    jump day102_afternoon_story_window


# [DAG_NODE id=day102_afternoon_story_window type=dynamic_window day=102 period=Afternoon window=story_chain returns_to=day102_2_day2_chore_time]
label day102_afternoon_story_window:

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day102_afternoon_story_window_menu_1]
    menu:
        "The cart is still. The corridor has not forgotten yesterday."

        "Let Miss Stern find me near the linen closet." if story.chain_available("stern"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("stern")
            call expression _chain_label

        "Steal an hour with Missy before Stern counts the sheets." if story.chain_available("missy"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("missy")
            call expression _chain_label

        "Drift toward the Locke Suite and watch who performs for whom." if story.chain_available("vance"):

            # [STATE] State/progression update
            $ _chain_label = story.resolve_chain_label("vance")
            call expression _chain_label

        "Push the cart on and keep my hands honest.":
            if story.day2_chore_focus == "corruption":
                cora_inner "Honesty is a word for people who are not wearing stolen lace."
                cora_inner "I work in silence and call it restraint."
            else:
                cora_inner "I count boards, hinges, and the distance between stairs."
                cora_inner "Craft is safer when it has no audience."
            
            "The hallway outside the Master Suite is dim, the scent of lavender and expensive powder leaking beneath the heavy mahogany door."
            "As I push the cart past the threshold, a voice filters through the crack—Miss Vance's, carrying a raw, petulant heat."
            
            cora_inner "I stop. My hand stays on the wood of the cart. I lean close to the frame and listen."
            
            "Beyond the door, Miss Vance is in a state of loose, disheveled vulnerability, her silk dressing gown half-unlaced at the shoulder as she holds a crystal glass of sherry."
            "Missy stands near the vanity, folding a linen shift. Her hands are steady, but her flushed face catches the gas-lamp light."
            
            # [ASSET] Visual/staging command
            show missy_sprite smiling at centre_bust with move # [asset auto]
            show vance_sprite neutral at right_bust with moveinright # [asset auto]
            vance "You're prying again, girl. I see your eyes moving over my perfumes. Do you want to touch them?"
            missy "No, Miss. I was only tidying the vanity as Miss Stern directed."
            
            "Vance rises, her movements slightly unsteady but deliberate, stepping directly into Missy's space until the silk of her dressing gown brushes the coarse cotton of Missy's apron."
            "She reaches out, her manicured fingers trailing slowly, provocatively along the high white collar of Missy's uniform, her thumb brushing the skin of Missy's throat."
            "Missy flinches, her breath catching, but she stands her ground, her observant eyes locking onto Vance's lips."
            
            vance "You think you're clean because you wash the soot, but the soot here gets under the skin eventually. It makes you want... things you shouldn't name."
            missy "Perhaps, Miss. But some of us have to wash the soot off. Others are permitted to wear it."
            
            cora_inner "The physical tension between them is a sudden, breathtaking flash of forbidden desire—class captivity meeting physical curiosity."
            "Vance draws her hand back with a quiet, sharp gasp, her face flushing, while Missy bows, her defensive propriety restoring itself like steel."
            
            cora_inner "I step back from the door, my pulse hammering against the stolen lace beneath my uniform."
            cora_inner "There is a brilliant, dangerous chapter in that."
            
            cora_inner "The house loses interest when I stop offering it a face."
            # [STATE] State/progression update
            jump day102_3_stern_fetches_cora

    # [STATE] Dynamic story-chain window returns to authored day flow
    jump day102_3_stern_fetches_cora


# [DAG_NODE id=day102_afternoon_consequence_window type=dynamic_window day=102 period=Afternoon window=consequence penance=true returns_to=day102_2_day2_chore_time]
label day102_afternoon_consequence_window:
    # [DAG_CHECK type=confrontation]
    call check_confrontations

    # [STATE] State/progression update
    $ _penance_label = story.pop_penance_for_window("day102_afternoon")
    if _penance_label:

        # [STATE] State/progression update
        call expression _penance_label

        # [STATE] State/progression update
        jump day102_3_stern_fetches_cora
    return


# ── 023: STERN FETCHES CORA ─────────────────────────────────────

# [DAG_NODE id=day102_3_stern_fetches_cora type=work day=102]
label day102_3_stern_fetches_cora:

    # [ASSET] Visual/staging command
    scene bg_servants_corridor_day
    with dissolve

    show stern_sprite stern at centre_bust

    cora_inner "Stern finds me at the foot of the servants' stair."
    "She does not raise her voice."
    cora_inner "That is how I know the matter is already dangerous."
    cora_inner "Somewhere above us, a clock marks the interval between discovery and punishment."

    stern "Cora. Upstairs."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show stern_sprite stern at right_bust with move # [asset auto]
    cora "Ma'am?"

    stern "Do not make me repeat myself."

    "Her eyes flick once toward my hands. Empty. Then my face. Too still."

    stern "There is a complaint from the Master Suite. You were assigned there this morning."

    "Behind her, Missy has gone pale."

    if story.missy_day2_suspicion_state == "uneasy":
        cora_inner "She knows I took it. Or knows enough to fear knowing."
    else:
        cora_inner "She trusts me enough to be frightened for both of us."

    stern "Both of you. Move."

    # [STATE] State/progression update
    jump day102_3_vance_goes_incandescent


# [DAG_NODE id=day102_3_vance_goes_incandescent type=work day=102]
label day102_3_vance_goes_incandescent:

    # [ASSET] Visual/staging command
    scene bg_master_suite_tea
    with fade

    show missy_sprite shocked at left_bust
    show stern_sprite stern at centre_bust
    show vance_sprite angry at right_bust

    cora_inner "The Master Suite has become a courtroom without chairs."

    "Vance stands by the armoire, one hand clenched around the edge of a hatbox."
    cora_inner "Her face is controlled so tightly that the control itself has become indecent."

    vance "Something has been taken."

    stern "Madam, I assure you—"

    vance "Do not assure me. Find it."

    "Missy inhales too sharply."
    "Vance hears it."

    vance "You."

    missy "Madam?"

    vance "You were here. Both of you were here."

    "Her eyes move to me."
    cora_inner "Yesterday she saw a maid. Today she sees a possible thief."
    cora_inner "That is progress of a kind."

    if story.day2_contraband_state == "stolen_wearing":
        cora_inner "The missing object is under my skirt."
        cora_inner "The absurdity of it threatens to become laughter, which would be fatal."
    else:
        cora_inner "The missing object is hidden in a trunk a few feet away."
        cora_inner "Missy placed it there. I made that true."

    vance "I will not have servants pawing through my private things."

    cora_inner "Private."
    cora_inner "The word enters the room wearing gloves and entirely the wrong shoes."

    stern "Cora. Missy. If either of you has any knowledge of this matter, speak now."

    cora_inner "Speak now."
    cora_inner "As if truth from below stairs were ever heard before the floor above it decided."

    # [STATE] State/progression update
    jump day102_3_coras_choice


# [DAG_NODE id=day102_3_coras_choice type=choice]
label day102_3_coras_choice:

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day102_3_coras_choice_menu_1]
    menu:
        "What do I do?"

        "Confess enough to control the damage. [[Prey: visible risk, cleanest conscience]]":

            # [STATE] State/progression update
            jump day102_3_cora_confesses

        "Produce it as if discovering it now. [[Predator: controlled lie]]":

            # [STATE] State/progression update
            jump day102_3_cora_pretends_to_find_it

        "Let Missy take the shape of the blame. [[Ghost: clean hands, dirty outcome]]":

            # [STATE] State/progression update
            jump day102_3_cora_frames_missy


# [DAG_NODE id=day102_3_cora_confesses type=work day=102]
label day102_3_cora_confesses:

    # [ASSET] Visual/staging command
    scene bg_master_suite_tea
    with dissolve

    show missy_sprite shocked at left_bust
    show stern_sprite stern at centre_bust
    show vance_sprite angry at right_bust

    $ story.set_day2_tea_choice("prey")
    $ apply_effects(stern_susp=20, insp=15, corr=0)

    cora_inner "The truth is not safe."
    cora_inner "That does not make the lie safer."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust4 with moveinleft # [asset auto]
    show stern_sprite stern at centre_left_bust4 with move # [asset auto]
    show missy_sprite shocked at centre_right_bust4 with move # [asset auto]
    show vance_sprite angry at right_bust4 with move # [asset auto]
    cora "Ma'am. I saw the item this morning."

    "Missy's head turns toward me."

    vance "You saw it."

    cora "Yes, Ma'am. I did not understand whether it had been left aside for laundering or packed in error. I should have reported it to Miss Stern at once."

    stern "Yes. You should have."

    "Stern's voice could cut thread."

    if story.day2_contraband_state == "stolen_wearing":
        cora_inner "The lace remains beneath my uniform."
        cora_inner "My confession is therefore not truth, but a smaller lie dressed as truth."
        cora_inner "Still, it stands closer to honesty than anything else I have available."
        cora_inner "My pulse does not agree with my mouth."
    else:
        cora_inner "I do not look at the trunk."
        cora_inner "Looking would condemn Missy before I choose whether I mean to."

    vance "Where is it?"

    cora "I cannot say for certain, Ma'am. I only know I failed to report it."

    cora_inner "A bad answer."
    cora_inner "A brave answer."
    cora_inner "The two are cousins."

    # [STATE] State/progression update
    jump day102_3_gideon_interrupts_controls_vance


# [DAG_NODE id=day102_3_cora_pretends_to_find_it type=work day=102]
label day102_3_cora_pretends_to_find_it:

    # [ASSET] Visual/staging command
    scene bg_master_suite_tea
    with dissolve

    show missy_sprite shocked at left_bust
    show stern_sprite stern at centre_bust
    show vance_sprite angry at right_bust

    $ story.set_day2_tea_choice("predator")
    $ apply_effects(stern_susp=10, insp=5, corr=15)

    cora_inner "Helpful."
    cora_inner "That is the mask."
    cora_inner "Helpful girls are allowed to cross rooms that guilty girls are not."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust4 with moveinleft # [asset auto]
    show stern_sprite stern at centre_left_bust4 with move # [asset auto]
    show missy_sprite shocked at centre_right_bust4 with move # [asset auto]
    show vance_sprite angry at right_bust4 with move # [asset auto]
    cora "Pardon me, Madam. May I check where the morning things were placed?"

    vance "Do you imagine I have not looked?"

    cora "No, Madam. Only that servants often look in servant ways."

    "Stern's eyes sharpen."
    "Stern's mouth tightens by a fraction."
    cora_inner "That is the Savoy equivalent of laughter."
    cora_inner "Too much intelligence. But the door is already open."

    if story.day2_contraband_state == "planted_in_trunk":
        "I cross to the travel trunk."
        "Missy makes a tiny sound."
        "I lift one folded shirt, then another, then pause as though surprised by what my hand has discovered."

        cora "Is this the item, Madam?"

        "I hold up the lace carefully."
        cora_inner "Missy looks as if I have pulled her own heart from the trunk."

    elif story.day2_contraband_state == "stolen_wearing":
        "I cross to the armoire and open the hatbox."
        cora_inner "My body is a locked drawer. The room must not know it."
        "A second small lace ribbon lies caught under the hatbox lining."
        cora_inner "Not the garment itself."
        cora_inner "Enough to teach the room the wrong lesson."

        cora "There is a loose piece here, Madam. Perhaps the rest was misplaced while packing."

        cora_inner "It is not enough."
        cora_inner "It is almost enough."
        cora_inner "In a room this frightened, almost can work."

    else:
        "I cross to the armoire and make a show of checking beneath the hatbox."
        cora "Might this be it, Madam?"

    vance "Give it to me."

    "I do."
    "Our fingers do not touch."

    # [STATE] State/progression update
    jump day102_3_gideon_interrupts_controls_vance


# [DAG_NODE id=day102_3_cora_frames_missy type=work day=102]
label day102_3_cora_frames_missy:

    # [ASSET] Visual/staging command
    scene bg_master_suite_tea
    with dissolve

    show missy_sprite shocked at left_bust   
    show stern_sprite stern at centre_bust
    show vance_sprite angry at right_bust

    $ story.set_day2_tea_choice("ghost")
    $ story.set_missy_day2_trust_break(True)
    $ apply_effects(vance_susp=0, insp=0, corr=20)

    cora_inner "There is a version of me that protects Missy."
    cora_inner "She exists."
    cora_inner "She is simply not the one who speaks first."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust4 with moveinleft # [asset auto]
    show stern_sprite stern at centre_left_bust4 with move # [asset auto]
    show missy_sprite shocked at centre_right_bust4 with move # [asset auto]
    show vance_sprite angry at right_bust4 with move # [asset auto]
    cora "Missy handled it this morning, Ma'am."

    missy "Cora—"

    stern "Quiet."

    "Missy's mouth closes."
    cora_inner "The betrayal arrives in her eyes before the fear does."

    cora "I did not know whether she had been instructed to move it. It was not my place to question a senior maid's handling of the room."

    missy "I only did what you said."

    vance "What she said?"

    "The room turns toward me."
    "I let confusion rise slowly, carefully, with no panic in it."

    cora "I told her not to leave private garments exposed, Madam. I did not instruct her to hide anything."

    cora_inner "Every word is shaped to be defensible."
    cora_inner "That is how cowards build knives with ivory handles."

    missy "That's not—"

    stern "Enough."

    "Missy stops."
    cora_inner "She has already learned the house's first lesson: truth without rank is noise."

    # [STATE] State/progression update
    jump day102_3_gideon_interrupts_controls_vance


# [DAG_NODE id=day102_3_gideon_interrupts_controls_vance type=work day=102]
label day102_3_gideon_interrupts_controls_vance:

    # [STATE] State/progression update
    $ set_time_period("Evening")

    scene bg_master_suite_tea
    with dissolve

    show gideon_sprite cold at right_bust
    show stern_sprite stern at centre_bust
    show vance_sprite angry at left_bust

    "The door opens without a knock."
    "Mr. Locke enters as if the argument has been waiting for his permission to exist."

    gideon "Vance."

    "That is all."
    "It is enough."

    # [ASSET] Visual/staging command
    show vance_sprite cowed at left_bust

    vance "Something was taken from my things."

    gideon "So I gather. The corridor can hear you gathering it."

    "Vance's colour changes."
    cora_inner "Not shame, exactly. More intimate than that. A correction landing where others cannot see it."

    if story.day2_tea_choice == "prey":

        gideon "You."

        # [ASSET] Visual/staging command
        show cora_sprite base at left_bust4 with moveinleft # [asset auto]
        show stern_sprite stern at centre_left_bust4 with move # [asset auto]
        show vance_sprite cowed at centre_right_bust4 with move # [asset auto]
        show gideon_sprite cold at right_bust4 with move # [asset auto]
        cora "Yes, Sir."

        gideon "You saw the item and failed to report it."

        cora "Yes, Sir."

        gideon "Yet you report your failure now."

        cora_inner "His attention is not warm."
        cora_inner "It is worse. It is precise."

        cora "That is correct, Sir."

        gideon "Interesting choice."

        stern "Sir, I can have the girl dismissed—"

        gideon "No."

        "Stern stops."

        gideon "A dismissal makes noise. We are finished with noise for today."

        cora_inner "He does not spare me."
        cora_inner "He spares the hotel's reputation, which is the same thing with better upholstery."

        "His eyes remain on me one beat too long."
        cora_inner "I have not escaped notice."
        cora_inner "I have been filed."

    elif story.day2_tea_choice == "predator":

        if story.day2_contraband_state == "planted_in_trunk":
            "Mr. Locke looks at the lace, then at the trunk, then at me."
        else:
            "Mr. Locke looks at the hatbox, then at my perfectly folded hands."

        cora_inner "He understands too quickly."
        cora_inner "Men like him do not need proof when pattern will do."

        gideon "Thank you. Leave it there."

        cora "Yes, Sir."

        vance "Thank her? She—"

        gideon "Found what you misplaced."

        cora_inner "He has chosen which story the afternoon will believe."

        "Vance goes still."
        cora_inner "The correction is mild enough to be polite and sharp enough to draw blood."

        gideon "You will not punish the staff for your embarrassment."

        "My gaze stays on the carpet."
        cora_inner "The carpet is expensive enough to hide several sins."

        cora_inner "He knows I lied."
        cora_inner "He has chosen to make the lie useful."

    else:

        "Mr. Locke's gaze passes over Missy first."
        cora_inner "She is pale. Terrified. Guilty-looking in the way frightened people always look guilty to those searching for a culprit."

        "Then he looks at me."
        "I am calm."
        cora_inner "Too calm, perhaps."

        gideon "Miss Stern, you will not conduct an inquest in a guest room."

        stern "Sir."

        vance "But she—"

        gideon "Has been frightened enough to become useless for the afternoon. That is poor management, not justice."

        "Missy's eyes fill."
        "She does not cry."
        cora_inner "That is the worst of it."

        gideon "Send the girl below. Send Cora back to work. I will discuss the rest with Miss Vance privately."

        cora_inner "Privately."
        "Vance hears the word and obeys before any hand moves."

        "His eyes touch mine for the smallest fraction of time."
        cora_inner "He has not believed me."
        cora_inner "He has not exposed me."
        cora_inner "He is keeping a note."
        cora_inner "This is not mercy."
        cora_inner "It is investment."

    gideon "That will be all."

    # [ASSET] Visual/staging command
    hide gideon_sprite
    hide vance_sprite
    hide stern_sprite

    scene bg_servants_corridor_day
    with fade

    show missy_sprite shocked at centre_bust

    cora_inner "The corridor receives us like a throat swallowing something sharp."

    if story.day2_tea_choice == "ghost":
        missy "How could you?"

        cora_inner "There are many possible answers."
        cora_inner "None are small enough to fit in the corridor."

        # [ASSET] Visual/staging command
        show cora_sprite base at left_bust with moveinleft # [asset auto]
        show missy_sprite shocked at right_bust with move # [asset auto]
        cora "Not here."

        missy "No. Not anywhere."

        # [ASSET] Visual/staging command
        hide missy_sprite

        "She leaves me beside the cart."
        cora_inner "That, too, is material."
        cora_inner "I hate myself for knowing it."

    elif story.day2_tea_choice == "predator":
        missy "You knew where it was."

        cora "I guessed."

        missy "No, you didn't."

        "There is accusation in her voice now."
        cora_inner "Also awe."
        cora_inner "I am not sure which is more dangerous."

        # [ASSET] Visual/staging command
        hide missy_sprite

    else:
        missy "You stepped forward."

        cora "Someone had to."

        missy "No one ever has to. That's what makes it something."

        cora_inner "She says it simply, which makes it unbearable."

        # [ASSET] Visual/staging command
        hide missy_sprite

    "I walk back down the narrow servants' corridor toward the quarters, the gas-lamp light casting long, uneasy shadows on the cold floorboards."
    "As I pass the dark linen closet, a sliver of yellow light escapes the door, accompanied by the distinct clink of iron keys."
    "I freeze, stepping back into the gloom. Through the half-inch gap in the heavy oak door, the air is thick with the scent of starch, cedar, and something warmer—lavender and pressed wool."
    "Inside, the space is cramped. Missy stands pinned against the high shelves, her back pressed flat against the stacked, pristine sheets."
    "Ms. Stern stands directly in her path, blocking her escape. She is closer than I have ever seen her to any servant, her disciplinary mask cracked to reveal a low, burning intensity."
    "With a slow, deliberate movement, Stern raises her hand. Her keys dangle, chiming softly, as her fingers reach out to trace Missy's collarbone above the cotton collar."
    "Missy's breath catches, her chin rising as Stern's hand slides upward, her thumb pressing firmly against the rapid beat of Missy's pulse at her throat."

    # [ASSET] Visual/staging command
    show stern_sprite neutral at centre_bust with moveinright # [asset auto]
    stern "A girl with raw fingers has no business prying into the suites, Missy."

    "Her voice is a low, husky vibration, her thumb slowly caressing the warm skin of Missy's neck."
    cora_inner "The intimacy of the gesture is sharp, almost predatory, yet wrapped in a strange, fiercely protective heat."

    stern "I can protect a quiet fool. I cannot protect a girl who lets the gentlemen see she has eyes. Do you understand me, child?"

    "Missy does not pull away. Instead, she leans slightly into the pressure of Stern's thumb, her cheeks flushed, her dark eyes locking onto Stern's with a submissive yet fiercely observant focus."

    missy "Yes, Ma'am. I only fold."

    "Stern's gaze drops to Missy's parted lips, her thumb lingering for one long, silent heartbeat against the pulse before she draws her hand back, her iron-bound keys sliding back into the folds of her skirt."

    stern "Then fold. And keep your eyes on the thread."

    "I step back into the dark corridor, my chest tight."
    cora_inner "The heavy atmosphere of the house seems to cling to my throat like soot."
    cora_inner "There is a dark, heavy chapter in that—the invisible chains that bind the prey and the protector in this building."

    if story.manuscript_progress == 0:
        cora_inner "Tonight I must write."
        cora_inner "Two days inside the machine and not a single finished chapter would be its own kind of defeat."
    else:
        cora_inner "Tonight I must decide whether the second chapter deserves the truth or the better lie."

    # [STATE] State/progression update
    jump day102_4_night


# ── 024: NIGHT — WRITE OR INDULGE ───────────────────────────────

# [DAG_NODE id=day102_4_night type=work day=102]
label day102_4_night:

    # [STATE] State/progression update
    $ set_time_period("Night")

    call day102_night_consequence_window

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    "The candle takes reluctantly."
    "For a moment the room is only wick, breath, and the small circle of light I can afford."

    cora_inner "My ledger lies open."
    cora_inner "My page waits beside it."
    cora_inner "One records appetite. The other pretends to tame it."

    # [STATE] State/progression update
    $ show_ledger_ui()

    # [DAG_CHOICE group=day102_4_night_menu_1]
    menu:
        "What do I do with the night?"

        "Write. Turn the suite into fiction before it rots. [[Manuscript progress]]":

            # [STATE] State/progression update
            jump day102_4_cora_writes_a_chapter

        "Do not write. Stay inside the feeling a little longer. [[Indulgence]]":

            # [STATE] State/progression update
            jump day102_4_cora_sneaks_a_feel


# [DAG_NODE id=day102_night_consequence_window type=dynamic_window day=102 period=Night window=consequence penance=true returns_to=day102_4_night]
label day102_night_consequence_window:
    # [DAG_CHECK type=confrontation]
    call check_confrontations

    # [STATE] State/progression update
    $ _penance_label = story.pop_penance_for_window("day102_night")
    if _penance_label:

        # [STATE] State/progression update
        call expression _penance_label

        # [STATE] State/progression update
        jump day103_morning
    return


# [DAG_NODE id=day102_4_cora_writes_a_chapter type=write]
label day102_4_cora_writes_a_chapter:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    $ story.set_day2_night_action("write")

    if story.manuscript_progress == 0:

        if has_story_fuel(15):

            cora_inner "Chapter One comes late, but it comes with teeth."

            if story.day1_corridor_state == "predator":
                cora_inner "I write a maid who learns that other people's innocence can open doors her own hands must not touch."
            elif story.day1_corridor_state == "prey":
                cora_inner "I write a maid caught at the threshold, exposed by the very hunger that brought her there."
            else:
                cora_inner "I write a maid who hears enough through walls to understand the architecture of power."

            cora_inner "The prose is raw."
            cora_inner "Good. Raw things bleed honestly."

            # [STATE] State/progression update
            $ story.complete_manuscript_chapter("day1_chapter")
            call book1_write_chapter(chapter_key="day1_chapter", current_day=102)

            # [STATE] State/progression update
            $ apply_effects(vance_susp=0, insp=-10, corr=0)

            cora_inner "Chapter One is done."
            cora_inner "Late is not failure."
            cora_inner "Blank is failure."

        else:

            cora_inner "I try to begin with the corridor."
            cora_inner "Then the suite."
            cora_inner "Then Missy's face."
            cora_inner "Each beginning collapses into accusation."

            cora_inner "I do not yet have enough material."
            cora_inner "Or I have too much and no discipline."
            cora_inner "The page does not care which excuse I prefer."

    else:

        if has_story_fuel(30):

            cora_inner "Chapter Two begins with a hatbox."
            cora_inner "Not the object inside."
            cora_inner "The pause before it is opened."

            if story.day2_tea_choice == "prey":
                cora_inner "I write a woman who tells one clean portion of the truth and lets everyone mistake that portion for the whole."
                cora_inner "Her honesty does not save her."
                cora_inner "It places her exactly where the dangerous man can see her."

            elif story.day2_tea_choice == "predator":
                cora_inner "I write a woman who discovers that a lie told calmly can become furniture."
                cora_inner "People walk around it. Lean on it. Arrange the room to suit it."
                cora_inner "By the end of the chapter, even the gentleman is using her falsehood as if he ordered it built."

            else:
                cora_inner "I write a woman who survives by leaving fingerprints on other people."
                cora_inner "No blood on her cuffs."
                cora_inner "No proof in her pocket."
                cora_inner "Only a girl in the corridor learning what betrayal sounds like when it does not raise its voice."

            # [STATE] State/progression update
            $ story.complete_manuscript_chapter("day2_chapter")
            call book1_write_chapter(chapter_key="day2_chapter", current_day=102)

            # [STATE] State/progression update
            $ apply_effects(vance_susp=0, insp=-15, corr=0)

            cora_inner "By the time the candle shortens, the second chapter exists."
            cora_inner "It is better than the first."
            cora_inner "That is not comforting."

        else:

            cora_inner "I write three sentences and cross them out."
            cora_inner "The scene is still too close to me."
            cora_inner "Vance's fury. Gideon's correction. Missy's face. The lace under cloth or hidden in the trunk."
            cora_inner "None of it has become art yet."
            cora_inner "It remains appetite and consequence."

    # [STATE] State/progression update
    jump day103_morning


# [DAG_NODE id=day102_4_cora_sneaks_a_feel type=work day=102]
label day102_4_cora_sneaks_a_feel:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    $ story.set_day2_night_action("indulge")
    $ apply_effects(susp=10, insp=5, corr=15)

    cora_inner "I close the notebook."
    cora_inner "The page has asked for discipline."
    cora_inner "I am tired of discipline."

    if story.day2_contraband_state == "stolen_wearing":

        cora_inner "I stand before the little mirror above the washstand."
        cora_inner "The uniform is plain. Severe. Designed to erase the body beneath it."
        cora_inner "I lift the hem only enough to confirm the secret is still mine."

        cora_inner "The lace is ridiculous."
        cora_inner "That is part of its power."

        cora_inner "The mirror gives back a maid."
        cora_inner "The skin beneath disagrees."

        cora_inner "A woman can scrub ash from a stranger's hearth while carrying a private scandal beneath her skirt."
        cora_inner "A woman can be unseen and still not be innocent."

        cora_inner "I lower the hem."
        cora_inner "The maid returns."
        cora_inner "The witness remains."

    else:

        cora_inner "There is nothing in my hands tonight."
        cora_inner "The dangerous thing is upstairs, hidden where I told Missy to hide it."
        cora_inner "That should make it less present."
        cora_inner "It does not."

        cora_inner "I replay the afternoon until the room rearranges itself around Gideon's entrance."
        cora_inner "Vance's fury contained. Stern's authority paused. Missy's fear made useful."
        cora_inner "And me, small enough to be overlooked until I was not."

        cora_inner "No chapter comes."
        cora_inner "Only heat stored where ink should have gone."
        cora_inner "Only the knowledge that I could have written and chose instead to keep feeling."

    cora_inner "When I finally sleep, the candle has burned lower than I meant to allow."
    cora_inner "Waste has consequences."

    # [STATE] State/progression update
    jump day103_morning

# Promotion note: deadline gate lives on day103.rpy label day103_morning.
