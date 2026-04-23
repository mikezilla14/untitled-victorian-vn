# ==========================================
# DAY 1: MORNING
# ==========================================
# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes

label day1_morning:

    # [ASSET] Visual/staging command
    scene bg_savoy_corridor_morning

    # [ASSET] Visual/staging command
    with fade

    "The Savoy Hotel. A gilded cage of mahogany and brass."
    "I stand outside the Head of Housekeeping's office. My forged references burn a hole in my apron pocket."

    # [ASSET] Visual/staging command
    show stern_sprite neutral at center
    "Ms. Stern looks at me like a butcher inspecting a cut of meat."

    stern "You say you have experience in the countryside. The Savoy is not the countryside, Cora. We demand absolute invisibility."
    
    # [CHOICE] Decision point
    menu:
        "How do I present myself?"
        
        "Play the meek, terrified country girl.":

            # [STATE] State/progression update
            $ apply_effects(susp=10,insp=0,corr=0)
            cora "I only wish to work hard and keep my head down, Ma'am."
            stern "See that you do."
            "Her gaze softens a fraction. She thinks I am stupid. Good."
            
        "Show competence and sharp intelligence.":

            # [STATE] State/progression update
            $ apply_effects(susp=20,insp=0,corr=0)
            cora "I am meticulous, Ma'am. You will find no fault in my execution."
            stern "Confidence is a dangerous thing in a maid, girl. Mind your station."
            "She doesn't like me. But she believes I can do the job."

    # [ASSET] Visual/staging command
    hide stern_sprite

    "Stern dismisses me. As I step out into the plush corridor, I nearly collide with a guest."

    # [ASSET] Visual/staging command
    show vance_sprite angry at left
    vance "Watch your step, you clumsy little idiot!"
    "She is dripping in velvet and pearls. Her eyes are furious, looking for someone to punish."

    # [ASSET] Visual/staging command
    show gideon_sprite cold at right
    "Then, the door to the Master Suite opens behind her. A man steps out. The air in the hallway immediately drops ten degrees."
    gideon "Vance. Leave the girl. You are making a scene."

    "The transformation is instantaneous. The venom drains from Vance's face."

    # [ASSET] Visual/staging command
    show vance_sprite submissive at left
    "She shrinks, taking a physical step behind his shoulder. A hound brought to heel."

    gideon "Apologies for the noise. See to your duties, maid."
    cora "Yes, Sir."

    "I keep my eyes down as they walk away. But my mind is racing. The way he looked at her... the way she yielded."
    "I need to get to my desk. I need to write that down."

    # [STATE] State/progression update
    jump day1_afternoon

# ==========================================
# DAY 1: AFTERNOON
# ==========================================
label day1_afternoon:

    # [ASSET] Visual/staging command
    scene bg_laundry_room_day

    # [ASSET] Visual/staging command
    with dissolve

    "The laundry room is a suffocating cloud of lye and steam."
    
    # [ASSET] Visual/staging command
    show missy_sprite smiling at center
    missy "You're the new girl! Cora, right? I'm Missy. Isn't this place just grand?"
    
    "Missy is bright-eyed, rural, and tragically innocent. She is exactly what I am pretending to be."
    cora "It's certainly big."

    "We gather our fresh linens and head up the servant's corridor toward the guest wings."
    
    # [ASSET] Visual/staging command
    scene bg_servants_corridor_dim

    # [ASSET] Visual/staging command
    with fade

    "As we pass the janitorial access to the Master Suite, a sound bleeds through the thin plaster."
    "A sharp slap. A gasp. Vance's voice, trembling."
    vance "I'm sorry, Sir. I won't speak out of turn again."
    
    # [ASSET] Visual/staging command
    show missy_sprite shocked at left
    missy "Oh my... are they fighting? Should we fetch Ms. Stern?"

    "Missy doesn't understand. But I do. The tone isn't violence. It's discipline."
    "This is the material. I need to see it."

    # [CHOICE] INFLECTION POINT 1: The Eavesdrop
    menu:
        "How do I secure the material?"
       

        "The Meat Shield: Dare Missy to check. (+Inspiration)": 

        **Note: rather than daring missy Cora could agree that maybe someone is in danger and have Missy intervene**

            # [STATE] State/progression update
            $ apply_effects(susp=0,insp=10,corr=0)
            cora "They might need fresh towels, Missy. You should peek through the keyhole. Just to be sure."
            missy "Me? Oh... I don't know..."
            "But her curiosity wins. She creeps to the door. I stay safely in the shadows, watching her watch them."
            "If the door opens, she takes the fall. I like this feeling. Moving the pieces."

            # [STATE] State/progression update
            $ day1_corridor_choice = "predator"
            
        "The Sinner: Take the physical risk. (+Corruption, +Suspicion)":

            # [STATE] State/progression update
            $ apply_effects(susp=50,insp=10,corr=0)
            cora "Quiet. Stay here."
            "I can't help myself. The heat in Vance's voice draws me in. I creep to the crack in the door."
            "I see Vance on her knees, Gideon's hand gripping her jaw. My breath catches. The floorboard groans beneath my shoe."
            "Gideon's head snaps toward the door. I scramble backward, my heart hammering in my throat."

            # [STATE] State/progression update
            $ day1_corridor_choice = "prey"

        "The Survivor: Pull Missy away. (+Inspiration)":

            # [STATE] State/progression update
            $ apply_effects(susp=0,insp=10,corr=0)
            cora "It's none of our business. Keep walking."
            "I grab Missy's arm and pull her down the hall before she can make a sound."
            "I don't need to see it. The audio is enough. I catalogue the wet sound of the slap, the exact pitch of Vance's gasp. Pure survival. Pure observation."

            # [STATE] State/progression update
            $ day1_corridor_choice = "ghost"

    # [STATE] State/progression update
    jump day1_twilight

# ==========================================
# DAY 1: TWILIGHT (The Ledger)
# ==========================================
label day1_twilight:

    # [ASSET] Visual/staging command
    scene bg_servants_quarters_dusk

    # [ASSET] Visual/staging command
    with fade

    "I lock the door to my cramped room. The ledger sits open on my desk."
    
    # [ASSET] UI CALL: Show Player Stats here
    $ show_ledger_ui()

    "I have one hour before lights out. What do I do with it?"

    # The Twilight Action Economy

    # [CHOICE] Decision point
    menu:
        "Atonement: Mend uniforms. (-Suspicion)":

            # [STATE] State/progression update
            $ apply_effects(susp=-20,insp=0,corr=0)
            "I spend the hour painstakingly darning the fraying hem of my apron. It is agonizingly dull, but Stern will see a diligent servant tomorrow."
            
        "Gossip: Talk to Missy. (+Corruption, -Suspicion)":

            # [STATE] State/progression update
            $ apply_effects(susp=-10,insp=0,corr=5)
            "I visit Missy's cot. We whisper about the wealthy guests. I subtly tease out her innocent thoughts about men, planting tiny, wicked seeds in her mind."
            
        "Indulge: Review my illicit notes. (+Inspiration, +Suspicion)":

            # [STATE] State/progression update
            $ apply_effects(susp=15,insp=10,corr=0)
            "I pace the room, replaying the sound of Gideon's voice in my head. I am distracted. I knock over my washbasin. Stern yells through the wall to keep quiet."

    # [STATE] State/progression update
    jump day1_night

# ==========================================
# DAY 1: NIGHT (The Manuscript)
# ==========================================
label day1_night:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night

    # [ASSET] Visual/staging command
    with dissolve

    "The hotel is asleep. It's time to write."
    
    # Check if player has enough stats to write a good chapter
    if (inspiration + corruption ) >= 15:
        "The ink flows easily tonight. The events in the corridor fueled my imagination."
        
        if day1_corridor_choice == "predator":
            "I write a chapter about a cunning maid who uses the secrets of the aristocracy to pull their strings."
            # Show CG_Writing_Predator
            
        elif day1_corridor_choice == "prey":
            "I write a chapter about a maid who gets caught spying, and is dragged into the room to be punished alongside the lady of the house."
            # Show CG_Writing_Prey
            
        else:
            "I write a meticulously detailed chapter about the hidden depravities of the wealthy, observing them like insects under glass."
            # Show CG_Writing_Ghost

        # [STATE] State/progression update
        $ manuscript_progress += 1
        "Chapter One is complete. I blow out the candle and sleep."
        
    else:
        "I stare at the blank page. My mind is too clouded with the terror of this place. I have nothing to write tonight."
        "I will have to take bigger risks tomorrow."

    # [STATE] State/progression update
    jump day2_morning
