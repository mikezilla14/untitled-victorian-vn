# ==========================================
# DAY 5: MORNING (The Confrontation)
# ==========================================
# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes

label day5_morning:

    # [ASSET] Visual/staging command
    scene bg_master_suite_day

    # [ASSET] Visual/staging command
    with fade

    "I am summoned to the Master Suite. Vance is not here. Only Gideon."
    "He is sitting in the leather armchair, smoking. He does not look up when I enter."

    # [ASSET] Visual/staging command
    show gideon_sprite dominant at center
    gideon "Someone forced the lock on my private box yesterday, Cora."
    
    "He finally looks at me. His eyes are dead, cold obsidian. He isn't angry. He is swatting a fly."
    gideon "I will ask you once. Where is it?"

    if not has_photograph:
        # THE FAIL STATE (No leverage)
        "I have nothing to bargain with. My silence is a confession."
        cora "I don't know what you mean, Sir."
        "He studies me for a long, agonizing moment. He rings the bell for Ms. Stern."
        "I am nothing to him. I am already dead."

        # [STATE] State/progression update
        jump ending_fired_and_ruined

    else:
        # THE AUDACITY
        "My heart hammers against my ribs, but I do not break his gaze. I reach into my apron pocket."
        "I place the photograph face up on the polished mahogany table between us."
        
        "Gideon looks at the image. He looks at his own ruin. And then... he laughs."
        "It is a dark, terrible sound."

    # [STATE] State/progression update
    jump day5_afternoon

# ==========================================
# DAY 5: AFTERNOON (The Defusal)
# ==========================================
label day5_afternoon:
    "He stands up and slowly closes the distance between us. He picks up the photograph."

    gideon "You thought this was a weapon, didn't you? A little maid holding a knife to the throat of a Lord."
    "He taps the photograph against my cheek. A patronizing, terrifying gesture."
    
    gideon "If I rang that bell right now and the police arrived, who do you think they would believe, Cora?"
    gideon "A wealthy aristocrat claiming a scullery girl forged a scandalous image to extort him? Or a filthy little thief with stolen property in her apron?"
    
    "The reality of the Victorian machine crashes down on me. I have no power. My nuclear option is a pea-shooter."
    "But then, his hand slides to the back of my neck. His grip is firm, pulling me an inch closer."
    
    gideon "But it took steel to pick that lock. And it took pure, unadulterated venom to stand there and look me in the eye while you handed this over."
    gideon "Why did you do it, Cora?"

    # [CHOICE] Decision point
    menu:
        "The truth. What is my motivation?"
        
        "The Observer (High Inspiration): 'To finish my book.'":

            # [STATE] State/progression update
            $ inspiration += 15

            # [STATE] State/progression update
            $ day5_dynamic = "muse"
            
            cora "I am writing a manuscript. I needed the absolute truth of who you are to write the ending."
            "Gideon stares at me, genuinely taken aback. The clinical detachment fascinates him."
            gideon "A voyeur. Hiding in a maid's uniform, dissecting us like insects."
            
        "The Deviant (High Corruption): 'To stand where you stand.'":

            # [STATE] State/progression update
            $ corruption += 15

            # [STATE] State/progression update
            $ day5_dynamic = "protege"
            
            cora "Because I am suffocating in this uniform. And I want to know what it feels like to hold the whip."
            "Gideon's eyes darken. The threat fades into a sick, mutual recognition. He sees the monster blooming inside me."
            gideon "A little wolf, dressed as a sheep."

    "He drops the photograph onto the burning coals of the fireplace. The leverage burns away to ash in seconds. I am entirely at his mercy."
    
    "He reaches into his breast pocket and pulls out a crisp, fifty-pound note. He slips it into the neckline of my uniform."
    
    gideon "Print your little book, Cora. And tomorrow morning, you will report directly to me. We are going to have a very interesting time, you and I."
    
    "He walks out of the room, leaving me trembling, funded, and utterly entangled."

    # [STATE] State/progression update
    jump day5_night

# ==========================================
# DAY 5: NIGHT (The Literary Climax)
# ==========================================
label day5_night:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night

    # [ASSET] Visual/staging command
    with dissolve

    "The hotel is silent. The ledger is closed. I have my funding. But I am no longer a ghost. Gideon knows exactly what I am."
    "I dip my pen into the inkwell. It is time to write the final chapter. To put everything I have learned, stolen, and felt onto the page."

    # THE H-SCENE PAYOFF (Visualized through the Manuscript)
    if (corruption > inspiration) and (corruption > influence):
        "The prose flows hot and reckless. I write a deeply visceral, corrupted chapter."
        "The characters on the page lose all restraint, mirroring the dark desires I've kept locked behind my uniform. I write about surrendering to a predator."
        # Show Explicit H-Scene CG: The Corrupted Manuscript Visualization
        
    elif (influence > corruption) and (influence > inspiration):
        "I write a masterpiece of psychological dominance. The prose is cold, calculated, and thrilling."
        "The characters engage in a slow, agonizing power play. I write about a maid who learns to manipulate the masters of the house."
        # Show Explicit H-Scene CG: The Dominance Manuscript Visualization

    else:
        "I write a beautiful, haunting piece of voyeurism. The prose is detached but incredibly intimate, capturing the tragic beauty of submission in a gilded cage."
        # Show Explicit H-Scene CG: The Voyeuristic Manuscript Visualization

    # [STATE] State/progression update
    $ manuscript_progress = 100
    "I sign the final page. The MVP is complete."

    # THE CLIFFHANGER

    # [ASSET] Visual/staging command
    scene bg_master_suite_day

    # [ASSET] Visual/staging command
    with fade

    "The next morning."
    "I enter the Master Suite to clear the breakfast trays."
    
    # [ASSET] Visual/staging command
    show vance_sprite confused at left
    "Vance is sitting at the vanity. She looks at me, then looks away, as if sensing a shift in the air she doesn't understand."
    
    # [ASSET] Visual/staging command
    show gideon_sprite dominant at right
    "Gideon is reading the paper. As I reach across the table to take his plate, his hand closes lightly over my wrist."
    
    "He doesn't look up from the news. But his thumb slowly, deliberately strokes the pulse point on my wrist. A brand. A promise."
    "Vance watches in the mirror, her eyes wide with a sudden, dawning terror."
    "I look at Gideon. I look at Vance. And I smile."

    # HARD CUT TO BLACK

    # [ASSET] Visual/staging command
    scene black

    # [ASSET] Visual/staging command
    with fade
    
    "END OF DEMO. THE BOOK IS WRITTEN. THE GAME HAS JUST BEGUN."
    
    return
