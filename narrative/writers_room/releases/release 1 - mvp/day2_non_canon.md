# ==========================================
# DAY 2: MORNING (The Discovery)
# ==========================================
label day2_morning:
    scene bg_master_suite_day
    with fade

    "The Master Suite. The guests are at breakfast, leaving Missy and me to strip the linens and scrub the hearth."
    "Missy is humming, blissfully unaware of the dark tension I witnessed through the door yesterday." [cite: 2283]

    show missy_sprite confused at center
    "Suddenly, there is a clatter from the armoire. Missy has knocked over a hatbox." [cite: 2284]
    
    missy "Cora... what kind of lady wears a thing like this?" [cite: 2286]
    
    "She holds up a piece of impossibly sheer, un-Victorian lace. A split-crotch undergarment that belongs in a Holywell Street catalogue, not a respectable hotel." [cite: 2285]
    "My pulse spikes. This is it. Leverage. Material."

    # INFLECTION POINT 1: The Catalyst
    menu:
        "What do I do with the contraband?"
        
        "The Thief: Claim it for myself. (+Corruption)": [cite: 2287]
            $ apply_effects(susp=0,insp=0,corr=15)
            $ day2_outfit_status = "stolen_wearing"
            cora "Give that to me, Missy. Keep your mouth shut." [cite: 2289]
            "I snatch the silk from her trembling hands. The deviance is intoxicating."
            "Before she can stop me, I slip into the washroom. I remove my sensible cotton and pull the scandalous lace up my thighs, right beneath my stiff maid's uniform." [cite: 2216, 2398]
            "The physical friction against my skin is a constant, thrilling secret." [cite: 2399]
            
        "The Saboteur: Frame Vance. (+Influence)": [cite: 2292]
            $ influence += 15
            $ day2_outfit_status = "framed_gideon_trunk"
            cora "It must be Mr. Gideon's. You'd better pack it deep inside his personal travel trunk before they return." [cite: 2293]
            missy "Oh! Yes, of course."
            "Missy unwittingly plants the bomb. I am using her as a pawn to test Gideon's reaction without getting my own hands dirty." [cite: 2294, 2295]
            
        "The Ghost: Play it safe. (+Inspiration)": [cite: 2296]
            $ apply_effects(susp=0,insp=10,corr=0)
            $ day2_outfit_status = "put_back"
            cora "Put it exactly back where you found it. We see nothing, we know nothing." [cite: 2296, 2297]
            "Missy frantically stuffs the lace back into the hatbox. I catalogue the visual details of the garment for my manuscript, terrified of the consequences of touching it." [cite: 2298]

    "We finish our duties and slip out before the guests return."
    
    jump day2_afternoon

# ==========================================
# DAY 2: AFTERNOON (The Apology Service)
# ==========================================
label day2_afternoon:
    scene bg_servants_corridor_day
    with dissolve

    "The fallout was immediate. Vance had a complete meltdown over the missing item, screaming at the staff until Gideon iced her out." [cite: 2300, 2304]
    
    show stern_sprite stern at center
    stern "Cora. Mr. Gideon has requested tea. You will take the silver service up and smooth over the morning's unpleasantness." [cite: 2401]
    
    "I nod, taking the heavy tray. The air in the Master Suite is suffocating when I enter."
    
    scene bg_master_suite_tea
    with fade
    
    show vance_sprite cowed at left
    "Vance sits at the vanity in a high-collared day dress, visibly subdued. Gideon has clearly disciplined her for the outburst." [cite: 2403]
    
    show gideon_sprite dominant at right
    "Gideon reads the paper. He doesn't look at Vance. He looks at me."
    
    gideon "Ms. Vance regrets her outburst this morning. She was... overtired." [cite: 2439]
    "He forces the apology, his eyes locked on mine. He is testing me." [cite: 2440]
    
    cora "Of course, Sir. I only hope the missing item has been recovered?" [cite: 2441]
    
    gideon "Not yet. But I am quite certain it will turn up exactly where it belongs before too long." [cite: 2442]

    # INFLECTION POINT 2: The Subtext Duel
    menu:
        "How do I respond to his loaded statement?"
        
        "Polite Insolence: Smile at Vance's pain. (+Influence)": [cite: 2444]
            $ apply_effects(susp=5,insp=10,corr=0)
            "I keep my eyes on Vance, offering a perfectly polite, entirely weaponized smile." [cite: 2444]
            cora "I shall be sure to strip the bedding entirely tomorrow, Sir. We must leave no stone unturned." [cite: 2445]
            "Gideon catches the subtle insolence. He realizes I enjoy holding the whip." [cite: 2408, 2447]
            $ day2_tea_choice = "predator"

        "Risky Flirtation: Hint at the dark. (+Corruption)": [cite: 2448]
            $ apply_effects(susp=10,insp=0,corr=10)
            "I meet Gideon's eyes directly. If I stole the lace, it feels suddenly very tight against my skin." [cite: 2448]
            cora "I do hope so, Sir. It would be a terrible shame for something so delicate to remain hidden in the dark." [cite: 2449]
            "Gideon's gaze tracks me, heavy and knowing. I am practically daring him to look under my skirt." [cite: 2413, 2450]
            $ day2_tea_choice = "prey"

        "Retreat: The Invisible Ghost. (+Inspiration)": [cite: 2452]
            $ apply_effects(susp=0,insp=10,corr=0)
            "The reality of what I'm doing crashes down on me. I drop my gaze immediately, retreating behind the mask of a servant." [cite: 2452, 2453]
            cora "Yes, Sir. I will leave you to your tea." [cite: 2454]
            "I played with fire for a second, got the psychological details I needed, and got out." [cite: 2455]
            $ day2_tea_choice = "ghost"

    jump day2_twilight

# ==========================================
# DAY 2: TWILIGHT (The Ledger)
# ==========================================
label day2_twilight:
    scene bg_servants_quarters_dusk
    with fade

    "I return to my quarters. My heart is hammering against my ribs."
    
    # UI CALL: Show Player Stats
    $ show_ledger_ui()

    "I must balance the ledger before I can write."

    menu:
        "Atonement: Scrub boots for Ms. Stern. (-Suspicion)":
            $ apply_effects(susp=-10,insp=0,corr=0)
            "I spend an hour in the scullery, blistered hands proving my subservience."
            
        "Socialize: Check on Missy. (+Corruption, -Suspicion)":
            $ apply_effects(susp=10,insp=0,corr=0)
            "I reassure Missy about the morning's chaos, carefully molding her trust in me."
            
        "Indulge: Look in the Mirror. (+Inspiration, +Corruption, +Suspicion)":
            $ apply_effects(susp=10,insp=0,corr=10)
            if day2_outfit_status == "stolen_wearing":
                "I lift my heavy wool skirt and stare at the stolen silk hugging my hips. I have never looked so ruined." [cite: 2079, 2217]
            else:
                "I stare at my reflection, adrenaline pumping as I replay the power I held in that room."

    jump day2_night

# ==========================================
# DAY 2: NIGHT (The Manuscript)
# ==========================================
label day2_night:
    scene bg_cora_desk_night
    with dissolve
    
    "The candle is lit. It's time for Chapter Two."

    if (inspiration + corruption + influence) >= 30:
        "The words practically tear themselves from my pen."
        
        if day2_tea_choice == "predator":
            "I write from the perspective of a cruel mastermind orchestrating a downfall, watching her rival squirm." [cite: 2145]
            # Show CG_Writing_Predator_Ch2
            
        elif day2_tea_choice == "prey":
            "I write breathless prose about a desperate maid begging to take the consort's place, thrilled by the danger of exposure." [cite: 2147]
            # Show CG_Writing_Prey_Ch2
            
        else:
            "I write a tense, observational piece about the agonizing restraint of servitude while surrounded by sin."
            # Show CG_Writing_Ghost_Ch2

        $ manuscript_progress += 1
        "Chapter Two is complete. I am one step closer to freedom."
        
    else:
        "My hands are shaking too badly. I am too afraid of Stern, or too uninspired by the day. I have failed to write tonight."

    jump day3_morning