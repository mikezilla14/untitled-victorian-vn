# ==========================================
# DAY 4: MORNING & AFTERNOON (The Heist)
# ==========================================
label day4_morning:
    scene bg_master_suite_day
    with fade

    "I am out of time. The manuscript needs an ending, and I need an absolute, undeniable truth to write it."
    "Gideon and Vance have left for a matinee at the West End. The suite is empty."
    
    "I shouldn't be here. Stern thinks I am polishing the ground-floor silver."
    "I move straight for Gideon’s heavy oak writing desk. The lockbox."
    
    "It takes three agonizing minutes with a purloined hairpin, my hands slick with sweat, but the lock finally gives."
    "Inside, beneath stacks of bank notes, is an envelope. I open it."
    
    # CG: The Photograph
    "It is a photograph. A silver gelatin print of Gideon and another man. It is explicit, undeniable, and utterly illegal."
    "Under the Criminal Law Amendment Act, this piece of paper is a guaranteed prison sentence. It is absolute ruin."
    "It is the ultimate leverage."

    jump day4_late_afternoon

# ==========================================
# DAY 4: LATE AFTERNOON (The Escape)
# ==========================================
label day4_late_afternoon:
    "A key turns in the outer door."
    
    vance "—and I told you, I will not tolerate that tone from her again!"
    
    "They are back early. My blood turns to ice. I am standing in the center of the room with the photograph in my hand."

    # INFLECTION POINT 1: The Escape
    menu:
        "Sixty seconds. I have to survive."
        
        "The Fireplace: Hide in the soot. (Keep photo, +40% Suspicion)":
            $ has_photograph = True
            $ suspicion += 40
            $ day4_escape = "fireplace"
            "I shove the photo into my bodice and dive into the massive unlit hearth, pressing myself into the suffocating darkness of the chimney breast."
            "I wait for an hour in absolute terror, breathing through my apron to avoid coughing. When they finally leave the sitting room, I slip out."
            "I am alive. I have the leverage. But my uniform is ruined with black soot. Stern will see."
            
        "The Bold Lie: Face them directly. (Keep photo, +40% Suspicion)":
            $ has_photograph = True
            $ suspicion += 40
            $ day4_escape = "bold_lie"
            "I shove the photo into my apron pocket and begin frantically dusting the desk just as they enter."
            show gideon_sprite angry at right
            gideon "What the devil are you doing in here? This suite was cleaned at dawn."
            cora "Checking for dust, Sir. Ms. Stern's orders."
            "He stares right through me. He doesn't believe a word of it. I am ordered out immediately. I have the photo, but I have a massive target on my back."
            
        "The Meat Shield: Flee and send Missy in. (Lose photo, -20% Suspicion)":
            $ has_photograph = False
            $ suspicion -= 20
            $ day4_escape = "meat_shield"
            "Panic wins. I drop the photo back into the box, lock it, and sprint out the servant's door just as they enter."
            "I find Missy in the hall and shove my dust rag into her hands. 'They need you in there now!' I hiss."
            "I hide around the corner as she awkwardly stumbles in, drawing their irritation. I am safe. But I lost the nuclear option."

    jump day4_twilight_ledger

# ==========================================
# DAY 4: TWILIGHT (The Ludonarrative Trap)
# ==========================================
label day4_twilight_ledger:
    scene bg_servants_quarters_dusk
    with dissolve
    
    # UI displays current stats
    $ show_ledger_ui()
    
    "The ledger sits open on my desk. My hands are shaking."
    
    if has_photograph:
        "I have the photograph. I have the leverage."
    else:
        "I survived, but my hands are empty. I am exactly where I started."

    "Stern's eyes are burning a hole in my back. I am on the absolute razor's edge of discovery."
    
    menu:
        "What must I do tonight?"
        
        "Atonement: Scrub the soot from my apron." if day4_escape == "fireplace":
            $ suspicion -= 30
            "I spend the hour shivering over the washbasin, scrubbing until my knuckles bleed. By morning, Stern will see a spotless maid."
            jump day4_night_exhaustion
            
        "Atonement: Mend uniforms and avoid Stern's gaze." if day4_escape == "bold_lie":
            $ suspicion -= 30
            "I sit in the corner of the laundry, making myself as small and invisible as possible. I must lower my profile."
            jump day4_night_exhaustion

        "Atonement: Comfort Missy." if day4_escape == "meat_shield":
            $ suspicion -= 10
            "Missy is crying after being scolded. I hold her hand and play the supportive friend. My alibi is secure."
            jump day4_night_writing
            
        "Write the Manuscript (Cost: +15% Suspicion)":
            if suspicion + 15 >= 100:
                "I reach for the candle, but I freeze. The missing wax. The ink on my fingers."
                "Stern is already watching me too closely after today. If I write tonight, she will notice tomorrow. I will be fired. The workhouse."
                "I cannot take the risk. I have to put the pen down."
                # The game physically prevents the action, looping back.
                jump day4_twilight_ledger 
            else:
                $ suspicion += 15
                "I light the stolen candle stub. Let them be suspicious. I have work to do."
                jump day4_night_writing

# ==========================================
# DAY 4: NIGHT (The Exhaustion)
# ==========================================
label day4_night_exhaustion:
    scene bg_cora_desk_night
    with fade

    "I collapse onto my thin mattress. My body is broken, and my nerves are completely shot."
    "The manuscript sits untouched in the dark. I have missed my deadline."
    "But as I press my hand against my bodice and feel the crinkle of the photograph paper, a dark, terrifying smile crosses my face."
    "Tomorrow, everything changes."

    jump day5_morning

label day4_night_writing:
    scene bg_cora_desk_night
    with fade
    
    "Despite everything, I put pen to paper. But the words feel hollow without the ultimate proof."
    "I write Chapter Four, but it lacks the venom of a true conclusion."
    $ manuscript_progress += 1

    jump day5_morning