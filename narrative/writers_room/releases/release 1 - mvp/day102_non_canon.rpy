# ==========================================
# DAY 2: MORNING (The Discovery)
# ==========================================
# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent for scene chunks
label day2_morning:
    # [ASSET] Scene setup
    scene bg_master_suite_day
    with fade

    # [BEAT] Cora establishes private tension after yesterday's event

    "The Master Suite. The guests are at breakfast, leaving Missy and me to strip the linens and scrub the hearth."
    "Missy is humming, blissfully unaware of the dark tension I witnessed through the door yesterday." 

    # [ASSET] Character reveal
    show missy_sprite confused at center
    "Suddenly, there is a clatter from the armoire. Missy has knocked over a hatbox." 
    
    missy "Cora... what kind of lady wears a thing like this?" 
    
    "She holds up a piece of impossibly sheer, un-Victorian lace. A split-crotch undergarment that belongs in a Holywell Street catalogue, not a respectable hotel." 
    "My pulse spikes. This is it. Leverage. Material."

    # [CHOICE] INFLECTION POINT 1: The Catalyst
    menu:
        "What do I do with the contraband?"
        
        "The Thief: Claim it for myself. (+Corruption)": 
            # [STATE] Route shift toward corruption and active risk
            $ apply_effects(susp=0,insp=0,corr=15)
            $ day2_outfit_status = "stolen_wearing"

            cora "Give that to me, Missy. Keep your mouth shut." 
            "I snatch the silk from her trembling hands. The deviance is intoxicating."
            "Before she can stop me, I slip into the washroom. I remove my sensible cotton and pull the scandalous lace up my thighs, right beneath my stiff maid's uniform." 
            "The physical friction against my skin is a constant, thrilling secret." 
            
        "The Saboteur: Frame Vance. (+Corruption)": 
            # [STATE] Route shift toward manipulation and social control
            $ apply_effects(susp=0,insp=0,corr=15)
            $ day2_outfit_status = "framed_gideon_trunk"

            cora "It must be Mr. Gideon's. You'd better pack it deep inside his personal travel trunk before they return." 
            missy "Oh! Yes, of course."
            "Missy unwittingly plants the bomb. I am using her as a pawn to test Gideon's reaction without getting my own hands dirty." 
            
        "The Ghost: Play it safe. (+Inspiration)": 
            # [STATE] Route shift toward caution and observational distance
            $ apply_effects(susp=0,insp=10,corr=0)
            $ day2_outfit_status = "put_back"

            cora "Put it exactly back where you found it. We see nothing, we know nothing." 
            "Missy frantically stuffs the lace back into the hatbox. I catalogue the visual details of the garment for my manuscript, terrified of the consequences of touching it." 

    "We finish our duties and slip out before the guests return."
    
    # [STATE] Progression
    jump day2_afternoon

# ==========================================
# DAY 2: AFTERNOON (The Apology Service)
# ==========================================
label day2_afternoon:
    # [ASSET] Scene setup
    scene bg_servants_corridor_day
    with dissolve

    "The fallout was immediate. Vance had a complete meltdown over the missing item, screaming at the staff until Gideon iced her out." 
    
    # [ASSET] Character introduction
    show stern_sprite stern at center
    stern "Cora. Mr. Gideon has requested tea. You will take the silver service up and smooth over the morning's unpleasantness." 
    
    "I nod, taking the heavy tray. The air in the Master Suite is suffocating when I enter."
    
    # [ASSET] Location change
    scene bg_master_suite_tea
    with fade
    
    # [ASSET] Character staging
    show vance_sprite cowed at left
    "Vance sits at the vanity in a high-collared day dress, visibly subdued. Gideon has clearly disciplined her for the outburst." 
    
    # [ASSET] Character staging
    show gideon_sprite dominant at right
    "Gideon reads the paper. He doesn't look at Vance. He looks at me."
    
    gideon "Ms. Vance regrets her outburst this morning. She was... overtired." 
    "He forces the apology, his eyes locked on mine. He is testing me." 
    
    cora "Of course, Sir. I only hope the missing item has been recovered?" 
    
    gideon "Not yet. But I am quite certain it will turn up exactly where it belongs before too long." 

    # [CHOICE] INFLECTION POINT 2: The Subtext Duel
    menu:
        "How do I respond to his loaded statement?"
        
        "Polite Insolence: Smile at Vance's pain. (+Inspiration)": 
            # [STATE] Predatory social dominance branch
            $ apply_effects(susp=5,insp=10,corr=0)

            "I keep my eyes on Vance, offering a perfectly polite, entirely weaponized smile." 
            cora "I shall be sure to strip the bedding entirely tomorrow, Sir. We must leave no stone unturned." 
            "Gideon catches the subtle insolence. He realizes I enjoy holding the whip." 

            # [STATE] State/progression update
            $ day2_tea_choice = "predator"

        "Risky Flirtation: Hint at the dark. (+Corruption)": 
            # [STATE] Escalates sexual risk and exposure
            $ apply_effects(susp=10,insp=0,corr=10)

            "I meet Gideon's eyes directly. If I stole the lace, it feels suddenly very tight against my skin." 
            cora "I do hope so, Sir. It would be a terrible shame for something so delicate to remain hidden in the dark." 
            "Gideon's gaze tracks me, heavy and knowing. I am practically daring him to look under my skirt." 

            # [STATE] State/progression update
            $ day2_tea_choice = "prey"

        "Retreat: The Invisible Ghost. (+Inspiration)": 
            # [STATE] De-escalation branch; preserve distance
            $ apply_effects(susp=0,insp=10,corr=0)

            "The reality of what I'm doing crashes down on me. I drop my gaze immediately, retreating behind the mask of a servant." 
            cora "Yes, Sir. I will leave you to your tea." 
            "I played with fire for a second, got the psychological details I needed, and got out." 

            # [STATE] State/progression update
            $ day2_tea_choice = "ghost"

    # [STATE] Progression
    jump day2_twilight

# ==========================================
# DAY 2: TWILIGHT (The Ledger)
# ==========================================
label day2_twilight:
    # [ASSET] Scene setup
    scene bg_servants_quarters_dusk
    with fade

    "I return to my quarters. My heart is hammering against my ribs."
    
    # [ASSET] UI CALL: Show player stats
    # [STATE] Presents current stat ledger before evening choice
    $ show_ledger_ui()

    "I must balance the ledger before I can write."

    # [CHOICE] Evening regulation choice before writing
    menu:
        "Atonement: Scrub boots for Ms. Stern. (-Suspicion)":
            # [STATE] Lowers suspicion through visible obedience
            $ apply_effects(susp=-10,insp=0,corr=0)

            "I spend an hour in the scullery, blistered hands proving my subservience."
            
        "Socialize: Check on Missy. (+Corruption, -Suspicion)":
            # [STATE] Soft-power manipulation branch
            $ apply_effects(susp=10,insp=0,corr=0)

            "I reassure Missy about the morning's chaos, carefully molding her trust in me."
            
        "Indulge: Look in the Mirror. (+Inspiration, +Corruption, +Suspicion)":
            # [STATE] High-risk introspection branch
            $ apply_effects(susp=10,insp=0,corr=10)
            if day2_outfit_status == "stolen_wearing":
                "I lift my heavy wool skirt and stare at the stolen silk hugging my hips. I have never looked so ruined." 
            else:
                "I stare at my reflection, adrenaline pumping as I replay the power I held in that room."

    # [STATE] Progression
    jump day2_night

# ==========================================
# DAY 2: NIGHT (The Manuscript)
# ==========================================
label day2_night:
    # [ASSET] Scene setup
    scene bg_cora_desk_night
    with dissolve
    
    "The candle is lit. It's time for Chapter Two."

    # [STATE] Chapter completion gate based on cumulative momentum
    if (inspiration + corruption ) >= 30:
        "The words practically tear themselves from my pen."
        
        if day2_tea_choice == "predator":
            "I write from the perspective of a cruel mastermind orchestrating a downfall, watching her rival squirm." 
        # [ASSET] Show CG_Writing_Predator_Ch2
            
        elif day2_tea_choice == "prey":
            "I write breathless prose about a desperate maid begging to take the consort's place, thrilled by the danger of exposure." 
        # [ASSET] Show CG_Writing_Prey_Ch2
            
        else:
            "I write a tense, observational piece about the agonizing restraint of servitude while surrounded by sin."
        # [ASSET] Show CG_Writing_Ghost_Ch2

        # [STATE] Chapter progress update
        $ manuscript_progress += 1

        "Chapter Two is complete. I am one step closer to freedom."
        
    else:
        "My hands are shaking too badly. I am too afraid of Stern, or too uninspired by the day. I have failed to write tonight."

    # [STATE] Progression
    jump day3_morning
