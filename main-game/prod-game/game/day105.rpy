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

# day105_non_canon.rpy
# Release 1 / Day 05 non-canon Ren'Py-shaped draft
# Source intent: rewritten from legacy Day 5 confrontation script and aligned to updated Day 4 false-dawn ending.
# Conceptual role: slam the door back in Cora's face after Day 4's false dawn.
# Core thesis: Gideon is not the true antagonist; he is the first visible instrument of the structural power protecting men like him.
# Release function: close the MVP arc while opening the series arc — Cora has written, survived, and been noticed.
# Promotion note: replace story/player helper calls with exact runtime method names during implementation.
# Convergent pass: synthesized from day105_*_spec.rpy pool (thematic, humour, tension, erotic, mystery, class). Specs retained in main-game/pipeline/.

# ==========================================
# DAY 5 ANALYSIS / DESIGN INTENT
# ==========================================
# Legacy spine:
#   - Gideon summons Cora after discovering the lockbox breach.
#   - If Cora has the photograph, she believes she has leverage.
#   - Gideon laughs it off and explains why society will believe him over her.
#   - He burns or neutralises the evidence.
#   - He becomes intrigued by Cora's motive.
#   - Cora writes / reframes the manuscript climax.
#   - Demo ends with Gideon marking her as future interest.
#
# Structural revision:
#   - Day 5 should not be a simple villain confrontation.
#   - It should reveal the machine behind the villain: class, gender, reputation, law, patronage, police, publishers, employers.
#   - Gideon could end Cora here. He chooses not to because his class position makes him arrogant.
#   - This is a future hinge moment: in hindsight, this is where he should have crushed the threat.
#   - His failure is not kindness. It is bravado, curiosity, and structural overconfidence.
#
# Branching philosophy:
#   - Release 1 remains light on immediate branching.
#   - But Cora's flavour is recorded for future releases: observer / prey / predator / ghost / accomplice.
#   - Missy betrayals are not cosmetic. They become irreversible moral sediment.
#   - Gideon does not become the campaign villain. He becomes a recurring pressure line and mirror for Cora's development.


# ==========================================
# DAY 5 NODE MAP
# ==========================================
# 1-monster-reemerges
#   -> 2-the-summons
#   -> 3-leverage-collapses
#   -> 4-why-did-you-do-it
#   -> 5-gideon-marks-cora
#   -> 6-manuscript-reckoning
#   -> 7-release-one-ending
#   -> END OF RELEASE 1


# ==========================================
# 1 - MONSTER RE-EMERGES
# ==========================================

# [DAG_NODE id=day105_1_monster_reemerges type=work day=105]
label day105_1_monster_reemerges:

    # [STATE] TimeManager initializations
    $ time_manager.set_current_day(5)
    $ set_time_period("Morning")

    call day105_morning_consequence_window

    # [ASSET] Existing Day 5 / recurring Master Suite background
    scene bg_master_suite_day
    with fade

    "Morning arrives too cleanly."
    "The room simply becomes visible again, as if the hotel turned a key in me."
    cora_inner "That should have warned me."

    if story.day4_night_action == "finish_manuscript":
        "The chapter is finished."
        cora_inner "For a few hours, I believed that meant the story was."
    else:
        "The manuscript remains unfinished."
        cora_inner "Still, I woke with the stupid animal relief of someone who survived the night."

    if story.has_photograph:
        cora_inner "The photograph is no longer under the floorboard."
        cora_inner "The plank is level."
        cora_inner "That is how I know something has been taken: the house prefers surfaces without secrets."
        cora_inner "The room has the wrong silence."
    else:
        "The photograph remains where I left it: in Gideon's lockbox, where powerful men keep the things they trust the world to protect."
        cora_inner "But memory has weight."
        cora_inner "At least, I believed it did."

    "A message comes before breakfast."
    "The paper on the tray is folded too crisply for a servant's hand."
    "Mr. Locke requires me in the Master Suite."
    "Alone."

    cora_inner "The summons is not a threat."
    cora_inner "It is an appointment with the machinery."
    cora_inner "The false dawn ends without thunder."

    # [STATE] State/progression update
    jump day105_2_the_summons


# [DAG_NODE id=day105_morning_consequence_window type=dynamic_window day=105 period=Morning window=consequence penance=true returns_to=day105_1_monster_reemerges]
label day105_morning_consequence_window:
    call watch_suspicion
    return


# ==========================================
# 2 - THE SUMMONS
# ==========================================

# [DAG_NODE id=day105_2_the_summons type=work day=105]
label day105_2_the_summons:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at centre_bust

    "The clock on the mantel has stopped."
    cora_inner "Or I have."
    cora_inner "I cannot tell which is worse."

    "Gideon sits in the leather armchair with one ankle crossed over the other."
    "He is not pacing."
    "He is not furious."
    "He reads the Morning Post as though the headlines owe him money."

    cora_inner "That is the first cruelty."

    cora_inner "I wait on the threshold until he looks up."
    cora_inner "Guests are not kept waiting. Servants are."

    gideon "Close the door, Cora."

    "I close it."
    "I do not lean on it."

    cora_inner "Footsteps pause in the corridor."
    cora_inner "Someone is listening who will report whether I flinch."

    gideon "Not for privacy. For theatre. You have a taste for theatre, I think."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "I have a taste for employment, sir."

    cora_inner "He folds the paper once, neatly."
    cora_inner "The paper was open to departures."
    cora_inner "He wanted me to see it without asking."
    "He sets it aside."

    gideon "Someone forced the lock on my private box yesterday."

    "The sentence does not accuse."
    "It merely places a fact on the table and waits to see what shape I take around it."

    if story.day4_escape_state == "bold_lie":
        gideon "A girl dusting a locked desk in an already-clean room. Admirably stupid, if it had been stupid."
        cora "The dust was aspirational, sir."
        "His mouth twitches."
        "Not amusement."
        "Appraisal."
    elif story.day4_escape_state == "fireplace":
        gideon "There was soot where no soot belonged. You left time on the wall."
    elif story.day4_escape_state == "missy_cover":
        gideon "And poor Missy appeared at precisely the moment she was useful to someone else. A coincidence with your fingerprints on it."
        cora_inner "I file the detail."
        cora_inner "Someone assigned her route."
    else:
        gideon "Do not trouble yourself with denial. We are past the inexpensive parts of the conversation."
        cora "Then we are past my favourite part of the interview, sir."

    cora_inner "I count my breaths."
    cora_inner "Four before he speaks again."
    cora_inner "He waits for five."

    cora_inner "My mouth has gone dry."

    gideon "Where is it?"

    # [STATE] State/progression update
    jump day105_3_leverage_collapses


# ==========================================
# 3 - LEVERAGE COLLAPSES
# ==========================================

# [DAG_NODE id=day105_3_leverage_collapses type=work day=105]
label day105_3_leverage_collapses:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at centre_bust

    "He remains seated."
    "I remain standing."
    cora_inner "The geometry is the argument."

    if story.has_photograph:

        "I reach into my apron."
        cora_inner "Not because I want to."
        cora_inner "Because keeping it hidden has already failed."

        # [ASSET] Optional CG callout retained from legacy concept
        # show cg_gideon_photograph

        cora_inner "I should not place anything on his table without permission."
        "I place the photograph face up on the polished table between us."
        "The way one lays a scalpel: carefully, knowing the cut goes both ways."
        "The paper is warm from my body."

        "Gideon looks at it."
        "At himself."
        "At his supposed ruin."
        "His eyes move over the image, then over me."

        cora_inner "Something in his face shifts."
        cora_inner "I do not have a word for it that does not sound like surrender."
        cora_inner "It is genuine. That is the worst of it."

        # [ASSET] Visual/staging command
        show cora_sprite base at left_bust with moveinleft # [asset auto]
        show gideon_sprite dominant at right_bust with move # [asset auto]
        cora "You think this is funny?"

        gideon "No. I think you are."

        gideon "You are not funny."

        cora "No, sir. I am inconvenient."

    else:

        "I have no paper to place between us."
        cora_inner "Only memory, fear, and the absurd hope that truth remains truth when a servant speaks it."

        cora "I saw what was in the envelope."

        gideon "Did you?"

        "He sounds almost kind."
        cora_inner "That is how I know the blow is coming."

        cora "I know what you are hiding."

        gideon "No. You know what you believe you saw while committing theft."

    "He stands."
    cora_inner "Only then do I understand that the room has been arranged to make standing matter."
    "He steps closer."
    "Not touching."
    "Worse."

    gideon "Shall I teach you the arithmetic of reputation?"

    "He does not raise his voice."
    "He does not need to."
    "The room is already full of men who are not here."

    gideon "Let us imagine you walk out of this hotel and tell your story."

    "He begins counting on his fingers."
    "Not hurriedly."
    "Like a tutor with a dull but promising pupil."

    gideon "The police will ask why you were in my private rooms."
    cora "They will ask you first, sir."
    gideon "They will ask me last."
    gideon "My solicitor will ask who paid you."
    gideon "Your employer will ask why she should keep a thief."
    gideon "A publisher will ask whether a maid's scandal is worth a libel suit."
    gideon "Every decent woman in London will pretend she does not understand the accusation."

    gideon "And every indecent man will understand it perfectly and still dine with me."

    cora "A crowded social calendar, sir."

    cora_inner "There it is."
    cora_inner "Not his power."
    cora_inner "The power around him."
    cora_inner "None of them need to enter to vote."
    cora_inner "The hands I cannot see because they have never needed to enter the room."

    if story.has_photograph:
        "He picks up the photograph."
        "I do not stop him."
        "That is the second defeat."
    else:
        "He does not need to take anything from me."
        "That is the second defeat."

    cora_inner "I thought I had found a knife."
    cora_inner "I had found a handle attached to a door that opens only from his side."

    # [STATE] State/progression update
    jump day105_4_why_did_you_do_it


# ==========================================
# 4 - WHY DID YOU DO IT?
# ==========================================

# [DAG_NODE id=day105_4_why_did_you_do_it type=choice]
label day105_4_why_did_you_do_it:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at centre_bust

    gideon "Still."

    "The word changes the room."
    "He is finished explaining why I cannot hurt him."
    "Now he is deciding why I tried."

    gideon "It took nerve to pick the lock."

    if story.has_photograph:
        gideon "More nerve to keep the photograph overnight."
    else:
        gideon "Less nerve to abandon it, perhaps. But enough to look. Enough to remember."

    if story.day4_escape_state == "missy_cover" or story.missy_day4_used_as_cover:
        gideon "And enough appetite to spend another girl when the corridor narrowed."

        "Missy's name is not spoken."
        "It does not need to be."
        "Some debts do not require witnesses to become permanent."

    gideon "Why?"

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day105_4_why_did_you_do_it_menu_1]
    menu:
        "Why did I do it?"

        "To finish the book. [[Observer / Muse]]":

            # [STATE] State/progression update
            jump day105_4_motivation_observer

        "To stand where you stand. [[Predator / Protégé]]":

            # [STATE] State/progression update
            jump day105_4_motivation_predator

        "Because you frightened me, and I needed something that frightened you back. [[Prey / Adversary]]":

            # [STATE] State/progression update
            jump day105_4_motivation_prey

        "Because people like you survive by not being seen. [[Ghost / Witness]]":

            # [STATE] State/progression update
            jump day105_4_motivation_ghost


# ==========================================
# 4 - MOTIVATION: OBSERVER / MUSE
# ==========================================

# [DAG_NODE id=day105_4_motivation_observer type=work day=105]
label day105_4_motivation_observer:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at centre_bust

    $ story.set_day5_dynamic("muse")
    $ story.set_cora_release1_flavour("observer")
    $ apply_effects(insp=20, corr=0)

    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "To finish my book."

    "For the first time, Gideon does not answer immediately."

    cora "I needed the truth of the ending. Not gossip. Not fear. Something absolute."

    gideon "And you thought I would provide it."

    cora "You did."

    "He studies me with new attention."
    "Not respect."
    "Respect would require equality."
    "This is curiosity. Colder. Safer for him. More dangerous for me."

    gideon "A little anatomist below stairs. Cutting open her betters for art."

    cora "Not my betters."

    "The correction slips out."
    "His smile arrives slowly."

    gideon "There she is."

    # [STATE] State/progression update
    jump day105_5_gideon_marks_cora


# ==========================================
# 4 - MOTIVATION: PREDATOR / PROTÉGÉ
# ==========================================

# [DAG_NODE id=day105_4_motivation_predator type=work day=105]
label day105_4_motivation_predator:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at centre_bust

    $ story.set_day5_dynamic("protege")
    $ story.set_cora_release1_flavour("predator")
    $ apply_effects(insp=5, corr=20)

    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "Because I wanted to know what it felt like."

    gideon "What?"

    cora "To hold something over someone. To have the room change because I entered it with power hidden on me."

    "The confession should shame me."
    "It does."
    "Not enough."

    gideon "And did you enjoy it?"

    cora "Before it failed, yes."

    "His eyes darken with recognition."
    "Not affection."
    "Recognition is not soft."
    "It is a mirror deciding whether to cut."

    gideon "A wolf does not become dangerous because it finds teeth. It becomes dangerous when it stops apologising for hunger."

    cora "Is that advice?"

    gideon "No. An inventory."

    # [STATE] State/progression update
    jump day105_5_gideon_marks_cora


# ==========================================
# 4 - MOTIVATION: PREY / ADVERSARY
# ==========================================

# [DAG_NODE id=day105_4_motivation_prey type=work day=105]
label day105_4_motivation_prey:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at centre_bust

    $ story.set_day5_dynamic("adversary")
    $ story.set_cora_release1_flavour("prey")
    $ apply_effects(vance_susp=5, insp=10, corr=10)

    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "Because you frightened me."

    gideon "Sensible."

    cora "And I wanted something that frightened you back."

    "That pleases him more than it should."
    "Or perhaps not pleasure."
    "Interest. The predator noticing that the animal in the snare has bitten the wire."

    gideon "Did it?"

    "The question is gentle enough to be cruel."

    cora "No."

    "The truth tastes like blood."

    gideon "Not yet."

    "He says it lightly."
    "He should not have said it at all."

    # [STATE] State/progression update
    jump day105_5_gideon_marks_cora


# ==========================================
# 4 - MOTIVATION: GHOST / WITNESS
# ==========================================

# [DAG_NODE id=day105_4_motivation_ghost type=work day=105]
label day105_4_motivation_ghost:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at centre_bust

    $ story.set_day5_dynamic("witness")
    $ story.set_cora_release1_flavour("ghost")
    $ apply_effects(vance_susp=-5, insp=15, corr=5)

    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "Because people like you survive by not being seen, sir."

    gideon "People like me are seen constantly."

    cora "No. You are looked at, sir. That is not the same."

    "The room goes still."

    cora "Everyone sees the coat. The money. The table manners. The names that answer your letters."
    cora "No one sees the machinery unless they are small enough to be crushed by it."

    "For one second, I think I have reached him."
    "Then I realise that reaching him is not victory."
    "It is only proximity."

    gideon "A witness, then."

    cora "Yes."

    gideon "How unfortunate for you. Witnesses are useful only when someone with authority calls them."

    # [STATE] State/progression update
    jump day105_5_gideon_marks_cora


# ==========================================
# 5 - GIDEON MARKS CORA
# ==========================================

# [DAG_NODE id=day105_5_gideon_marks_cora type=work day=105]
label day105_5_gideon_marks_cora:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with dissolve

    show gideon_sprite dominant at centre_bust

    "Gideon turns away first."
    "Not because he is finished with me."
    "Because he wants me to understand that turning away is still safe for him."

    if story.has_photograph:
        "He carries the photograph to the fireplace."

        # [ASSET] Optional object/CG callout
        # show cg_photograph_burning

        "He holds the match near my face before he strikes it."
        "I feel the heat on my cheek before the paper curls."
        "The flame is small."
        "It eats the face first."

        "I expect panic."
        "Instead, I feel the strangest grief."
        "Not for the image."
        "For the version of myself who believed the image was enough."
        "Absurdly, I mourn my belief that evidence was the same as sight."

        # [STATE] State/progression update
        $ story.set_has_photograph(False)
        $ story.set_day5_evidence_destroyed(True)

    else:
        "He opens the lockbox and removes the envelope I failed to keep."
        "He does not burn it."
        "That is worse."
        "He simply places it back inside and turns the key."

        # [STATE] State/progression update
        $ story.set_day5_evidence_destroyed(False)

    gideon "There."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "You could dismiss me."

    gideon "Yes."

    cora "Have me arrested."

    gideon "Also yes."

    cora "Then why not?"

    gideon "Because ending a thing too early teaches one nothing."

    "He returns to the table and picks up his newspaper."
    "The crease is perfect."
    "He has done this before to someone."
    "The conversation, to him, has become light enough to read beside."

    "There it is."
    "The mistake."
    "Not mine."
    "His."

    "He can end this."
    "He does not."
    "Not from mercy."
    "From the obscene confidence of a man who has never needed to imagine consequence arriving late."

    gideon "You are not powerful, Cora. You are interesting. Do not confuse the two."

    "The sentence lands harder than anger would have."

    if story.day5_dynamic == "muse":
        gideon "Finish your little book. Send it somewhere vulgar. I should like to see whether ink can do what theft could not."
    elif story.day5_dynamic == "protege":
        gideon "Learn the difference between hunger and leverage. One embarrasses you. The other moves rooms."
    elif story.day5_dynamic == "adversary":
        gideon "Keep your fear. It has made you less dull than most brave people."
    else:
        gideon "Keep watching, if you must. But understand that witnesses also become exhibits."

    "He opens a drawer and removes an envelope."
    "Money."
    "Of course money."
    "The envelope is heavier than travel money should be."

    gideon "For printing. Or passage. Or a better pair of lies. Spend it as your genre requires."

    "He places it on the table."
    "Not into my hand."
    "He will not allow the gesture to look like payment unless I choose to take it that way."
    "I do not touch it until he turns away."
    "Even then, I wait one breath."
    "Servants who reach too quickly are thieves twice."

    # [CHOICE] Decision point
    # [DAG_CHOICE group=day105_5_gideon_marks_cora_menu_1]
    menu:
        "Do I take Gideon's money?"

        "Take it. Survival first. [[Pragmatic entanglement]]":

            # [STATE] State/progression update
            $ story.set_day5_money_choice("taken")
            $ story.set_gideon_entanglement_level("accepted_money")
            $ apply_effects(insp=5, corr=10)

            "I take the envelope."
            "My hand does not shake."
            "Our skin touches once."
            "He notes whether I look at the denomination."
            "That may be growth."
            "It may be damage."

            gideon "Good. Pride is most useful after one has eaten."

        "Refuse it. Keep one clean line. [[Defiant poverty]]":

            # [STATE] State/progression update
            $ story.set_day5_money_choice("refused")
            $ story.set_gideon_entanglement_level("refused_money")
            $ apply_effects(vance_susp=5, insp=10, corr=0)

            cora "I will not take your money, sir."

            gideon "You already took my photograph."

            cora "That was different."

            gideon "Yes. Less useful."

            "The envelope remains on the table between us."
            "A third object I cannot make mean only one thing."

        "Leave it untouched, but remember where he placed it. [[Ghost option]]":

            # [STATE] State/progression update
            $ story.set_day5_money_choice("deferred")
            $ story.set_gideon_entanglement_level("deferred_money")
            $ apply_effects(vance_susp=-5, insp=5, corr=5)

            "I do not touch the envelope."
            "I step back three paces."
            "I also do not refuse it."
            "I do not look away."

            gideon "Careful. That almost resembles strategy."

            cora "Almost is sometimes enough, sir."

            "He smiles at that."
            "I wish he had not."

    gideon "Go back downstairs."

    cora "And tomorrow, sir?"

    gideon "Tomorrow, I leave the Savoy."

    "The answer is a door I did not expect."

    gideon "Did you imagine I lived here? Monsters are rarely so convenient."

    "I hate that he says monsters."
    "I hate more that he says it accurately."

    gideon "We will meet again when it is interesting to do so. In the meantime, write. It seems to make you troublesome."

    cora "I shall inform the dust, sir."

    "He almost smiles."
    "Almost is a wage increase in this hotel."

    "He picks up the paper."
    "Dismissed."
    "Not defeated."
    "Not spared."
    "Marked and released."

    # [STATE] State/progression update
    jump day105_6_manuscript_reckoning


# ==========================================
# 6 - MANUSCRIPT RECKONING
# ==========================================

# [DAG_NODE id=day105_6_manuscript_reckoning type=write]
label day105_6_manuscript_reckoning:

    # [STATE] TimeManager transitions to Night
    $ set_time_period("Night")

    call day105_night_consequence_window

    if player.corruption_level < WRITE_GATE_CH2[1]:

        # [STATE] State/progression update
        jump bad_ending_rejection

    # [ASSET] Existing Cora desk night background
    scene bg_cora_desk_night
    with fade

    cora_inner "The room is exactly as I left it."
    cora_inner "That feels impossible."

    if story.day4_night_action == "finish_manuscript":
        "The triumphant chapter waits on the desk."
        "The maid outwits the master."
        "The lord is trapped by his own secret."
        "The ending is beautiful."
        "It is also wrong."
    else:
        "The unfinished pages wait on the desk."
        cora_inner "Yesterday I thought survival might be enough."
        cora_inner "Today survival feels like a room with the lock on the outside."

    cora_inner "The desk is an altar I built for a god who does not answer."

    cora_inner "I open the manuscript."
    cora_inner "I do not know whether I am correcting art or confessing defeat."

    if story.day5_dynamic == "muse":
        cora_inner "I write the machine around the man."
        "The carriage waiting outside. The solicitor's letterhead. The policeman's lowered eyes. The publisher's careful refusal dressed as taste."
        "Gideon becomes smaller on the page because the world behind him becomes vast."
        # [BEAT] Cross-day recalled moments — the machine's earlier faces
        if story.day1_interview_state == "competent":
            "Stern called precision a dangerous word from a girl in a borrowed apron."
            "She was not wrong. She was describing the machine's logic: exactness belongs to the people the machine was built to serve."
        if story.day3_brush_choice == "predator":
            "In the suite I named Vance's weakness with the accuracy of someone who has been watching rooms too long."
            "He called me a little anatomist. Even his compliments describe the altitude of the shelf where he keeps me."
        if story.day3_corridor_chain == "inspiration":
            "That morning I counted it: bell-pull rhythm, servants' stair, the distance from Stern's office to the Master Suite."
            "A hotel is a machine for sorting bodies by permission. Men like Gideon move through both halves and call the passage natural."
            "That sentence was already in the book. I only had to let the page be large enough to hold what I had seen."

    elif story.day5_dynamic == "protege":
        cora_inner "I write the hunger honestly."
        "Not as triumph. Not as corruption alone."
        cora_inner "As a tool I do not yet know how to hold without cutting someone poorer than me."
        # [BEAT] Cross-day recalled moments — the specific acts of hunger
        if story.day1_corridor_state == "predator":
            "I sent Missy to the service door first."
            "The corridor, the half-open door, the sound through plaster. I placed another girl's innocence between my hunger and the possible consequence."
            "That is what the hunger looks like before the page makes it interesting. The chapter must say so."
        if story.day2_tea_choice == "predator":
            "In the suite I crossed to the trunk and produced the missing thing with composed hands."
            "I said servant ways in a voice that meant something else, and he thanked me."
            "The chapter must ask what I gave him in exchange for that thanks. It must answer honestly."
        if story.day3_brush_choice == "predator":
            "I stood behind the seated woman with a brush in my hand and described her weakness with the precision of a naturalist."
            "On the page, the hunger that moves the maid is not cruelty. It is appetite: for the room, the view, the position, the precision."
            "The chapter must learn to hold that without apologising for it and without pretending it comes free."

    elif story.day5_dynamic == "adversary":
        cora_inner "I write fear as evidence."
        "Not weakness. Evidence."
        "The body knows power before the mind builds theories to survive it."
        # [BEAT] Cross-day recalled moments — the specific prey moments
        if story.day1_corridor_state == "prey":
            "The third board announced me. His eyes moved to the door."
            "I felt the fear and kept moving toward it. The body was already inside the danger before I had decided to enter."
            "That is the chapter's first evidence: fear and motion are not opposites."
        if story.day3_brush_choice == "prey":
            "I looked at him in the mirror when I should have looked at the floor. He saw me looking."
            "The chapter calls this the body's deposition: the face that showed too much was not failure."
            "It was the one moment in five days where I produced exactly what I felt without the maid's costume over it."
        if story.day3_ultimatum == "defied":
            "I said no to the nine o'clock room and the fear arrived correctly: sharp, specific, and located in the chest."
            "That is what the chapter calls evidence. Not proof against him. Proof of the pressure's shape."

    else:
        cora_inner "I write what witnesses cost."
        "Who is believed. Who is displayed. Who is corrected for naming the room too accurately."
        # [BEAT] Cross-day recalled moments — the cost of witnessing
        if story.day2_tea_choice == "ghost":
            "Missy said: I only did what you said."
            "Stern said: quiet."
            "The room agreed. Truth without rank is noise, and I was the one who arranged for Missy to be the noise."
            "The chapter must name this. A witness who engineers another person's exposure is not a witness. She is a user of testimony."
        if story.day1_corridor_state == "ghost":
            "I pulled her away from the service door. I said we were not the cure."
            "The chapter faces the other sentence: we were also not witnesses. We were bystanders who collected material and called the distance craft."
            "The manuscript must decide whether those are different things."
        if story.day3_brush_choice == "ghost":
            "I dropped the brush and saw the room from the floor and kept the angle."
            "From below: a polished boot, a clenched slipper, the hem of my own uniform trembling."
            "A witness that low in the room is also a witness who can be stepped on."
            "The chapter must say what that costs. Not only what it sees."

    if story.day2_tea_choice == "ghost" or story.day4_escape_state == "missy_cover" or story.missy_day4_used_as_cover:
        "Then Missy enters the page."
        "Not as symbol."
        "As debt."
        cora_inner "There are things I did to survive that the book cannot turn noble."

        # [STATE] State/progression update
        $ story.set_missy_debt_carried_forward(True)

    if story.day4_night_action == "finish_manuscript":
        cora_inner "I do not destroy yesterday's ending."
        cora_inner "I draw a line beneath it and write another."
        cora_inner "The first ending is the lie I needed."
        cora_inner "The second is the truth I can bear."
    else:
        "The ending comes now, stripped of victory."
        "Not triumphant."
        "Useful."

    # [STATE] State/progression update
    $ story.complete_manuscript_chapter("day5_reckoning_chapter")
    $ story.complete_release1_manuscript(True)
    $ story.set_release1_completed(True)
    call book1_write_chapter(chapter_key="day5_reckoning_chapter", current_day=105)

    "When the candle dies, the manuscript is complete."
    cora_inner "Not because I won."
    cora_inner "Because I finally understand the shape of the thing I lost to."
    "The ending is not victory."
    "It is diagnosis."

    # [STATE] State/progression update
    jump day105_7_release_one_ending


# [DAG_NODE id=day105_night_consequence_window type=dynamic_window day=105 period=Night window=consequence penance=true returns_to=day105_6_manuscript_reckoning]
label day105_night_consequence_window:
    call watch_suspicion
    return


# ==========================================
# 7 - RELEASE ONE ENDING
# ==========================================

# [DAG_NODE id=day105_7_release_one_ending type=work day=105]
label day105_7_release_one_ending:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day
    with fade

    "The next morning, Gideon Locke leaves the Savoy."

    # [ASSET] Visual/staging command
    show vance_sprite confused at left

    "Vance travels with him, dressed beautifully enough to convince strangers of almost anything."
    "She does not look at me until the footman carries down the last of the luggage."

    if story.day2_tea_choice == "ghost" or story.day4_escape_state == "missy_cover":
        "Missy stands on the opposite side of the corridor."
        "Not beside me."
        "That distance is one of the few honest things in the hotel."
    else:
        "Missy stands beside me, close enough that our sleeves almost touch."
        "Almost."

    # [ASSET] Visual/staging command
    show gideon_sprite dominant at right

    "Gideon pauses at the foot of the stairs."
    "Not long enough for anyone important to notice."
    "Long enough for me."

    if story.day5_money_choice == "taken":
        "The envelope is hidden beneath my mattress."
        "I can feel the weight of it from here, absurd as that is."
    elif story.day5_money_choice == "refused":
        "The envelope remained on his table."
        "I have kept my pride and solved nothing."
    else:
        "The envelope remained where he placed it."
        "Which means, inconveniently, that it may still become a choice later."

    gideon "Cora."

    "Vance's eyes move sharply to me."
    "There is calculation there. Fear too."
    "For once, she and I understand the same danger from different sides of the carpet."

    # [ASSET] Visual/staging command
    show cora_sprite base at left_bust with moveinleft # [asset auto]
    show vance_sprite confused at centre_bust with move # [asset auto]
    show gideon_sprite dominant at right_bust with move # [asset auto]
    cora "Sir."

    gideon "Do not become dull."

    "That is all."
    "No threat. No promise."
    "Only a man with every exit open marking a servant as a future amusement, problem, instrument, or wound."

    # [ASSET] Visual/staging command
    hide gideon_sprite
    hide vance_sprite

    "He leaves."

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk
    with dissolve

    "By evening, the Savoy has already made space for new guests."
    "Fresh trunks. Fresh flowers. Fresh lies."

    "The room resets."
    "The machine continues."

    "My manuscript lies beneath my folded apron."
    "It is not a victory."
    "It is a beginning with teeth."

    # [STATE] Carry-forward flags for Release 2
    $ story.set_gideon_recurring_pressure(True)
    $ story.set_release2_gideon_status("marked_cora")
    $ story.set_release2_guest_cast_pivot(True)

    if story.missy_debt_carried_forward:

        # [STATE] State/progression update
        $ story.set_release2_missy_status("wounded_trust")
    else:

        # [STATE] State/progression update
        $ story.set_release2_missy_status("uncertain_trust")

    scene black
    with fade

    "END OF RELEASE 1."
    "THE BOOK IS WRITTEN."
    "THE HOUSE REMAINS."

    return
