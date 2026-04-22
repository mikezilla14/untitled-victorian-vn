# ==========================================
# DAY 1: MORNING
# ==========================================
label day1_morning:
    scene bg_savoy_corridor_morning
    with fade

    "The Savoy Hotel. A gilded cage of mahogany and brass."
    "I stand outside the Head of Housekeeping's office. My forged references burn a hole in my apron pocket."

    show stern_sprite neutral at center
    "Ms. Stern looks at me like a butcher inspecting a cut of meat."

    stern "You say you have experience in the countryside. The Savoy is not the countryside, Cora. We demand absolute invisibility."
    
    menu:
        "How do I present myself?"
        
        "Play the meek, terrified country girl.":
            $ apply_effects(susp=10,insp=0,corr=0)
            cora "I only wish to work hard and keep my head down, Ma'am."
            stern "See that you do."
            "Her gaze softens a fraction. She thinks I am stupid. Good."
            
        "Show competence and sharp intelligence.":
            $ apply_effects(susp=20,insp=0,corr=0)
            cora "I am meticulous, Ma'am. You will find no fault in my execution."
            stern "Confidence is a dangerous thing in a maid, girl. Mind your station."
            "She doesn't like me. But she believes I can do the job."

    hide stern_sprite

    "Stern dismisses me. As I step out into the plush corridor, I nearly collide with a guest."

    show vance_sprite angry at left
    vance "Watch your step, you clumsy little idiot!"
    "She is dripping in velvet and pearls. Her eyes are furious, looking for someone to punish."

    show gideon_sprite cold at right
    "Then, the door to the Master Suite opens behind her. A man steps out. The air in the hallway immediately drops ten degrees."
    gideon "Vance. Leave the girl. You are making a scene."

    "The transformation is instantaneous. The venom drains from Vance's face."
    show vance_sprite submissive at left
    "She shrinks, taking a physical step behind his shoulder. A hound brought to heel."

    gideon "Apologies for the noise. See to your duties, maid."
    cora "Yes, Sir."

    "I keep my eyes down as they walk away. But my mind is racing. The way he looked at her... the way she yielded."
    "I need to get to my desk. I need to write that down."

    jump day1_afternoon

# ==========================================
# DAY 1: AFTERNOON
# ==========================================
label day1_afternoon:
    scene bg_laundry_room_day
    with dissolve

    "The laundry room is a suffocating cloud of lye and steam."
    
    show missy_sprite smiling at center
    missy "You're the new girl! Cora, right? I'm Missy. Isn't this place just grand?"
    
    "Missy is bright-eyed, rural, and tragically innocent. She is exactly what I am pretending to be."
    cora "It's certainly big."

    "We gather our fresh linens and head up the servant's corridor toward the guest wings."
    
    scene bg_servants_corridor_dim
    with fade

    "As we pass the janitorial access to the Master Suite, a sound bleeds through the thin plaster."
    "A sharp slap. A gasp. Vance's voice, trembling."
    vance "I'm sorry, Sir. I won't speak out of turn again."
    
    show missy_sprite shocked at left
    missy "Oh my... are they fighting? Should we fetch Ms. Stern?"

    "Missy doesn't understand. But I do. The tone isn't violence. It's discipline."
    "This is the material. I need to see it."

    # INFLECTION POINT 1: The Eavesdrop
    menu:
        "How do I secure the material?"
       

        "The Meat Shield: Dare Missy to check. (+Influence)": 

       **Note: rather than daring missy Cora could agree that maybe someone is in danger and have Missy intervene**

            $ apply_effects(susp=0,insp=10,corr=0)
            cora "They might need fresh towels, Missy. You should peek through the keyhole. Just to be sure."
            missy "Me? Oh... I don't know..."
            "But her curiosity wins. She creeps to the door. I stay safely in the shadows, watching her watch them."
            "If the door opens, she takes the fall. I like this feeling. Moving the pieces."
            $ day1_corridor_choice = "predator"
            
        "The Sinner: Take the physical risk. (+Corruption, +Suspicion)":
           $ apply_effects(susp=50,insp=10,corr=0)
            cora "Quiet. Stay here."
            "I can't help myself. The heat in Vance's voice draws me in. I creep to the crack in the door."
            "I see Vance on her knees, Gideon's hand gripping her jaw. My breath catches. The floorboard groans beneath my shoe."
            "Gideon's head snaps toward the door. I scramble backward, my heart hammering in my throat."
            $ day1_corridor_choice = "prey"

        "The Survivor: Pull Missy away. (+Inspiration)":
            $ apply_effects(susp=0,insp=10,corr=0)
            cora "It's none of our business. Keep walking."
            "I grab Missy's arm and pull her down the hall before she can make a sound."
            "I don't need to see it. The audio is enough. I catalogue the wet sound of the slap, the exact pitch of Vance's gasp. Pure survival. Pure observation."
            $ day1_corridor_choice = "ghost"

    jump day1_twilight

# ==========================================
# DAY 1: TWILIGHT (The Ledger)
# ==========================================
label day1_twilight:
    scene bg_servants_quarters_dusk
    with fade

    "I lock the door to my cramped room. The ledger sits open on my desk."
    
    # UI CALL: Show Player Stats here.
    $ show_ledger_ui()

    "I have one hour before lights out. What do I do with it?"

    # The Twilight Action Economy
    menu:
        "Atonement: Mend uniforms. (-Suspicion)":
            $ apply_effects(susp=-20,insp=0,corr=0)
            "I spend the hour painstakingly darning the fraying hem of my apron. It is agonizingly dull, but Stern will see a diligent servant tomorrow."
            
        "Gossip: Talk to Missy. (+Corruption, -Suspicion)":
            $ apply_effects(susp=-10,insp=0,corr=5)
            "I visit Missy's cot. We whisper about the wealthy guests. I subtly tease out her innocent thoughts about men, planting tiny, wicked seeds in her mind."
            
        "Indulge: Review my illicit notes. (+Inspiration, +Suspicion)":
           $ apply_effects(susp=15,insp=10,corr=0)
            "I pace the room, replaying the sound of Gideon's voice in my head. I am distracted. I knock over my washbasin. Stern yells through the wall to keep quiet."

    jump day1_night

# ==========================================
# DAY 1: NIGHT (The Manuscript)
# ==========================================
label day1_night:
    scene bg_cora_desk_night
    with dissolve

    "The hotel is asleep. It's time to write."
    
    # Check if player has enough stats to write a good chapter
    if (inspiration + corruption + influence) >= 15:
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

        $ manuscript_progress += 1
        "Chapter One is complete. I blow out the candle and sleep."
        
    else:
        "I stare at the blank page. My mind is too clouded with the terror of this place. I have nothing to write tonight."
        "I will have to take bigger risks tomorrow."

    jump day2_morning