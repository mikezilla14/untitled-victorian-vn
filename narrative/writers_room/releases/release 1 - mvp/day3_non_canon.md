# ==========================================
# DAY 3: MORNING (The Contextual Grind)
# ==========================================
label day3_morning:
    scene bg_servants_corridor_morning
    with fade

    "The bell rings at 5:00 AM. My muscles ache before my feet even hit the floor."
    "The tension from yesterday's tea service hangs heavy over the hotel."

    # Branching consequences based on Day 2's choices
    if day2_tea_choice == "predator":
        "Vance must have realized I was mocking her."
        "I am assigned to the scullery. Someone shattered three crystal vases in the Master Suite overnight, and I am the one ordered to pick the shards from the rugs on my hands and knees."
        "My fingers are bleeding by 9:00 AM. But I am smiling."
        $ apply_effects(susp=10,insp=0,corr=0)
        
    elif day2_tea_choice == "prey":
        "Gideon's heavy gaze follows me in my memory. Stern is on a warpath."
        "There is a terrifying, surprise laundry inspection. Stern tears through our footlockers."
        if day2_outfit_status == "stolen_wearing":
            "My heart stops. She searches my trunk, but the stolen silk is safe beneath my uniform, pressed against my skin. I survive by a hair's breadth."
        else:
            "I stand silently as she tosses my sparse belongings. I have nothing to hide."
        $ apply_effects(susp=15,insp=0,corr=0)
        
    else:
        "The day is an agonizing stretch of silent labor. Stern has me polishing the brass banisters for six hours straight."
        "My mind races, trying to process the psychological warfare happening in the Master Suite."
        $ inspiration += 10

    jump day3_afternoon

# ==========================================
# DAY 3: AFTERNOON (The Summons)
# ==========================================
label day3_afternoon:
    scene bg_master_suite_day
    with dissolve

    "At 2:00 PM, the summons arrives. Gideon requests my presence. Alone."
    "I enter the suite to find Vance seated at the vanity, staring blankly ahead. Gideon stands behind her."
    
    show gideon_sprite neutral at right
    gideon "Ah. Cora. Come here. Vance's maid is indisposed, and her hair requires tending."
    
    "He offers me the silver-backed brush. He expects me to serve her, but he orchestrates the room so that we are all looking at each other in the large mirror."
    
    show vance_sprite defeated at left
    "As I begin to brush, Gideon begins to speak. His voice is velvet, but his words are poison."
    gideon "Vance is losing her edge. She is becoming dull, wouldn't you agree, Cora? Predictable."
    
    "Vance flinches with every word. He is breaking her down, and he is using me as his audience."

    # INFLECTION POINT 1: The Test
    menu:
        "He is testing my limits. How do I participate?"
        
        "The Accomplice: Subtly help him hurt her. (+Influence)":
            $ influence += 15
            "I catch a particularly harsh tangle in Vance's hair. Instead of easing it out, I pull. Hard."
            "Vance gasps, tears pricking her eyes. In the mirror, Gideon smiles. We share a silent, terrible understanding."
            $ day3_brush_choice = "predator"

        "The Deviant: Make eye contact in the mirror. (+Corruption)":
            $ apply_effects(susp=0,insp=0,corr=15)
            "My hands are shaking. The humiliation in the room is a physical weight. I look up, locking eyes with Gideon in the reflection."
            "My face is flushed. I let him see exactly how this twisted dynamic makes me feel."
            $ day3_brush_choice = "prey"

        "The Mouse: Panic and drop the brush. (+Suspicion, +Inspiration)":
            $ apply_effects(susp=15,insp=15,corr=0)
            "The tension is unbearable. My hands tremble violently until the silver brush slips, clattering loudly against the hardwood floor."
            gideon "Clumsy."
            "I scramble to pick it up, retreating into the shell of a terrified servant while mentally recording every detail of his cruelty."
            $ day3_brush_choice = "ghost"

    "Vance is eventually dismissed to the dressing screen. As I move to leave, Gideon steps into my path."
    
    show gideon_sprite dominant at center
    "The mask is entirely gone. He leans in close, invading my space completely."
    
    gideon "You are not like the others, Cora. I want you to bring me tea tonight. 9:00 PM. Unchaperoned."
    "He doesn't wait for an answer. He knows he doesn't need one."

    jump day3_twilight

# ==========================================
# DAY 3: TWILIGHT (The Ledger)
# ==========================================
label day3_twilight:
    scene bg_servants_quarters_dusk
    with fade

    "I am back in my room. My blood is roaring in my ears."
    
    # UI CALL: Show Player Stats
    $ show_ledger_ui()

    "I have to stabilize myself. The ledger demands attention before tonight's ultimatum."

    menu:
        "Atonement: Prepare uniform for tomorrow. (-Suspicion)":
            $ apply_effects(susp=-20,insp=0,corr=0)
            "I rigorously iron my collars and cuffs, projecting an image of the perfect, obedient maid to throw Stern off my scent."
            
        "Recon: Eavesdrop on Missy's prayers. (+Corruption, -Suspicion)":
            $ apply_effects(susp=-10,insp=0,corr=5)
            "I listen to Missy beg God for forgiveness for wicked thoughts she doesn't even understand. It emboldens me."
            
        "Indulge: Write down Gideon's words. (+Inspiration, +Suspicion)":
            $ apply_effects(susp=10,insp=15,corr=0)
            "I furiously scribble down the exact phrases Gideon used to break Vance. I am reckless with my ink, staining my cuffs."

    jump day3_night

# ==========================================
# DAY 3: NIGHT (The Ultimatum)
# ==========================================
label day3_night:
    scene bg_cora_desk_night
    with dissolve
    
    "It is 8:45 PM. The entire hotel is quiet."
    "I look at my blank manuscript page. I look at the door."
    "Gideon's order echoes in my head. If I go to him, I forfeit my writing time. If I stay, I cross a man who can destroy me."

    # INFLECTION POINT 2: The Ultimatum
    menu:
        "The Choice."
        
        "Go to Him. (Massive stat gain, forfeit chapter)":
            $ apply_effects(susp=15,insp=10,corr=20)
            $ day3_ultimatum = "surrendered"
            
            scene bg_master_suite_night
            with fade
            "I abandon my book. I walk down the shadowed corridor with a tray of cold tea."
            "He is waiting in the dark. He toys with me, asking invasive questions, breaking down my defenses."
            "I am terrified, but I have never felt so alive. He owns my night."
            # Show CG_Gideon_Night_Encounter
            
            "I return to my room hours later, exhausted and ruined. My manuscript remains untouched."
            
        "Barricade the Door. (Write the book, anger the predator)":
            if (inspiration + corruption + influence) >= 45:
                $ apply_effects(susp=20,insp=0,corr=0)
                $ day3_ultimatum = "barricaded"
                
                "I lock my door. I shove the heavy washstand against it."
                "I light my candle and grip my pen. I will not be his plaything tonight."
                
                "I write a blistering chapter about a trap set by a cruel lord, and the prey that refuses to bite."
                $ manuscript_progress += 1
                # Show CG_Writing_Defiance
                
                "At 9:30 PM, I hear heavy footsteps stop outside my door. The handle jiggles once. Slowly."
                "I hold my breath. A long, terrifying silence stretches out before the footsteps finally retreat."
                "Chapter Three is complete. But I have declared war."
            else:
                "I try to barricade the door, but my resolve fails me. I lack the inspiration or the wicked courage to defy him or go to him."
                "I cower in my bed, writing nothing, paralyzed by indecision."

    jump day4_morning