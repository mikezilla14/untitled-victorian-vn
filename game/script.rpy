# ═══════════════════════════════════════════════════════════════
#  HOLYWELL STREET STUDIOS — MVP GRAY-BOX SKELETON v2.0
#  Setting: The Savoy Hotel, London, Winter 1891
#  Updated for historical accuracy (no convent references)
# ═══════════════════════════════════════════════════════════════

# ── 1. CHARACTERS ──────────────────────────────────────────────
define cora = Character("Cora", color="#d4a574")
define gideon = Character("Sir Gideon", color="#a30000")
define stern = Character("Miss Stern", color="#555555")
define narrator = Character(None, kind=nvl_narrator) if False else Character(None)
define sys = Character("System", color="#ffcc00")

# ── 2. CORE VARIABLES ─────────────────────────────────────────
default current_day = 1
default time_of_day = "Morning"

# The three stats
default corruption = 0
default inspiration = 0
default suspicion = 0

# Narrative flags
default read_letters = False
default saw_voyeur_scene = False
default heard_stern_humming = False
default gideon_spoke_day2 = False
default gideon_showed_depth = False
default manuscript_sent = False
default payment_received = False
default wrote_chapter_1 = False
default wrote_chapter_2 = False
default chose_bold_day4 = False

# ── 3. STAT DISPLAY SCREEN (Ugly placeholder for testing) ────
screen stats_overlay():
    zorder 100 # Forces this screen to render on top of backgrounds and sprites
    frame:
        xalign 0.0 yalign 0.0
        xpadding 10 ypadding 10
        background "#00000088"
        vbox:
            text "Day [current_day] — [time_of_day]" size 16 color "#ffcc00"
            text "Inspiration: [inspiration]" size 14 color "#4fc3f7"
            text "Corruption: [corruption]" size 14 color "#ef5350"
            text "Suspicion: [suspicion]" size 14 color "#ffa726"

# ── 4. HELPER FUNCTIONS (Python Block) ──────────────────────────
init python:
    def clamp_stats():
        # Declare globals so Python knows to modify your Ren'Py variables
        global suspicion, corruption, inspiration 
        
        suspicion = max(0, min(100, suspicion))
        corruption = max(0, min(100, corruption))
        inspiration = max(0, min(100, inspiration))

# ── 5. HELPER LABELS ──────────────────────────────────────────

label check_suspicion:
    if suspicion >= 100:
        jump game_over_dismissed
    return

# ═══════════════════════════════════════════════════════════════
#  THE ENTRY POINT
# ═══════════════════════════════════════════════════════════════
label start:
    show screen stats_overlay

    sys "Holywell Street Studios — MVP Gray-Box v2.0"
    sys "Setting: The Savoy Hotel, London. Winter 1891."

    cora "The Savoy. Two years old and already the most famous hotel in London. Electric lights in the corridors. Hot water in the suites. And me — Cora, village girl, board school graduate, chambermaid."

    cora "The hotel is quiet this time of year. A skeleton staff. Miss Stern runs the floor like a prison warden, and we have exactly one guest on the VIP floor — a Sir Gideon Locke."

    cora "I send seven shillings home every month. My parents are so proud I secured a position here. If I lose this place..."

    cora "But I didn't come to London just to scrub floors."

    jump day1_morning


# ═══════════════════════════════════════════════════════════════
#  DAY 1 — THE ARRIVAL
# ═══════════════════════════════════════════════════════════════
label day1_morning:
    $ current_day = 1
    $ time_of_day = "Morning"

    sys "─── DAY 1: MORNING ───"

    stern "Cora. You will attend to the third-floor VIP suite. Sir Gideon Locke is our only guest of consequence this week."

    stern "Your position here reflects on me. One complaint from the guests and you will leave this hotel without a character. Do I make myself understood?"

    cora "Yes, ma'am."

    stern "Then get to work."

    cora "Miss Stern's words hung in the air like a threat — because they were one. Without a character reference, I'd never work in service again. No position, no wages, no money home."

    cora "I cleaned Sir Gideon's suite while he was out. Dusted the books, beat the rugs, polished the brass. The room smelled of tobacco and something expensive I couldn't name."

    cora "I found nothing scandalous. Just the ordinary luxury of a man who has never scrubbed a floor in his life."

    # Tutorial note
    sys "[[TUTORIAL: This is Day 1. No real choices yet. The player learns the stakes: dismissal = destitution. Miss Stern holds Cora's future in her hands.]"

    jump day1_night


label day1_night:
    $ time_of_day = "Night"

    sys "─── DAY 1: NIGHT ───"

    cora "My room is small. A narrow bed, a washstand, and a writing desk wedged beneath the window. The electric lights don't reach the servant's quarters — just a candle and the sound of London outside."

    # THE FLASHBACK — establishes publisher connection + motivation
    cora "I keep thinking about the handbill I found at the market stall last week. Crumpled between cabbages and old newsprint."

    sys "[[FLASHBACK]"

    cora "'WRITERS WANTED. Discretion Assured. Generous Terms for Suitable Material. Enquire at No. 14, Holywell Street.'"

    cora "Holywell Street. Even I know what that means. The whole of London knows. It's where they sell the books you can't find in any respectable shop."

    cora "I've been writing stories since the vicar let me loose in his library back in the village. Penny dreadfuls, adventure tales, nonsense mostly. But I can write. I know I can."

    cora "The question is whether I can write... that."

    sys "[[END FLASHBACK]"

    cora "I think about the seven shillings I send home. I think about what a publisher on Holywell Street might pay for a single chapter."

    cora "I stare at the blank page."

    jump day1_late_night


label day1_late_night:
    $ time_of_day = "Late Night"

    sys "─── DAY 1: LATE NIGHT ───"

    cora "I dip the nib in the ink. I write a sentence. I cross it out. I write another."

    cora "It's no use."

    cora "I have nothing to say. My life has been the schoolroom, the village, and this hotel. What do I know of scandal? What do I know of passion?"

    cora "My writing is as plain and scrubbed as my uniform."

    sys "[[WRITING DESK: LOCKED. Inspiration ([inspiration]) is below 30. The player sees the gate.]"

    cora "I blow out the candle."

    $ clamp_stats()
    jump day2_morning


# ═══════════════════════════════════════════════════════════════
#  DAY 2 — THE FIRST ENCOUNTER
# ═══════════════════════════════════════════════════════════════
label day2_morning:
    $ current_day = 2
    $ time_of_day = "Morning"

    sys "─── DAY 2: MORNING ───"
    
    cora "Sir Gideon was in the suite when I arrived to clean."

    cora "Gentlemen do not speak to chambermaids. That is the rule. You enter, you curtsy, you become invisible, you leave."

    gideon "Ah — you're the new girl. Cora, is it?"

    cora "He knew my name. That was... unusual."

    $ gideon_spoke_day2 = True

    gideon "Don't look so startled. I asked Mrs — Miss Stern, is it? Fearsome woman. I asked her who'd been keeping my rooms so spotless."

    cora "He gestured at a book on the mantelpiece — a volume of Keats."

    gideon "Do you read?"

    cora "My heart hammered. A gentleman asking a maid if she reads. It could mean anything. Kindness. Curiosity. Or something else entirely."

    cora "I said, 'A little, sir,' which was the safest lie."

    # FIRST REAL CHOICE
    menu:
        "What do I do while he's distracted?"

        "Clean the desk and keep my head down (Safe)":
            $ suspicion -= 10
            $ inspiration += 5
            cora "I dusted and polished and kept my eyes on the floor. Safe. Invisible. Exactly what Miss Stern expects."
            cora "I learned nothing. But I survived."

        "Glance at the letters on his writing desk (Risky)":
            $ suspicion += 20
            $ inspiration += 15
            $ read_letters = True
            cora "While Sir Gideon had his back turned, I caught a glimpse of the letters on his desk. The handwriting was feminine. The language was... heated."
            cora "One letter mentioned a 'midnight arrangement' and 'the usual discretion.'"
            cora "My pulse was racing when I left the room. Not from fear. From something far more dangerous — curiosity."

    $ clamp_stats()
    call check_suspicion
    jump day2_night


label day2_night:
    $ time_of_day = "Night"

    sys "─── DAY 2: NIGHT ───"

    menu:
        "My shift is over. The gas lamps are dimmed in the servant's corridor."

        "Stay in my quarters and write a letter home (Pure)":
            $ corruption -= 5
            cora "I sat at my desk and wrote to my mother. Told her the hotel was grand, the work honest, and Miss Stern fair. All of it lies, except the first."
            cora "I told her I was saving well. That was true, at least."
            cora "The blank manuscript page stared at me from under the letter. I ignored it."

        "Explore the hidden servant's passage (Scandalous)" if not read_letters:
            $ corruption += 10
            $ inspiration += 15
            $ suspicion += 10
            cora "The Savoy was built with hidden corridors behind every wall — passages for the staff to move without being seen by guests. Tonight, I moved through them for a different reason."
            cora "I pressed my ear to the thin walls of the VIP floor. Voices. A woman laughing. The clink of crystal."
            cora "I saw nothing. But I heard enough to know that Sir Gideon Locke's evenings are not spent reading Keats."

        "Sneak to the servant's passage — I know where to listen (Scandalous)" if read_letters:
            $ corruption += 10
            $ inspiration += 20
            $ suspicion += 10
            cora "The letters mentioned a midnight arrangement. The servant's passage runs directly behind the VIP suites."
            cora "I pressed my ear to the wall. The voices were muffled but unmistakable. A woman. Sir Gideon. Laughter, then silence, then sounds I had only ever read about in the penny dreadfuls."
            cora "My face burned in the dark corridor. My mind was already composing sentences."

    $ clamp_stats()
    call check_suspicion
    jump day2_late_night


label day2_late_night:
    $ time_of_day = "Late Night"

    sys "─── DAY 2: LATE NIGHT ───"

    menu:
        "Should I try the manuscript?"

        "Sit at the writing desk (Requires 30 Inspiration)":
            if inspiration >= 30:
                $ inspiration -= 20
                $ wrote_chapter_1 = True
                $ manuscript_sent = True
                cora "I wrote. It was clumsy, overwrought, and naive — a schoolgirl's idea of scandal. But it was something."
                cora "I wrapped the pages in brown paper and wrote the Holywell Street address on the front."
                cora "Tomorrow morning, before Miss Stern's rounds, I'll slip it into the outgoing deliveries at the tradesmen's entrance. The errand boys won't question a sealed package."
                cora "My hands were shaking. Not from cold."
            else:
                cora "I sat at the desk and tried. But the words wouldn't come."
                cora "I don't have enough material. My prose is hollow — all structure, no heat. I need to observe more. I need to {i}experience{/i} more."

        "Blow out the candle and sleep":
            cora "I'm too exhausted. The writing can wait. It has to."

    $ clamp_stats()
    call check_suspicion
    jump day3_morning


# ═══════════════════════════════════════════════════════════════
#  DAY 3 — THE VOYEUR
# ═══════════════════════════════════════════════════════════════
label day3_morning:
    $ current_day = 3
    $ time_of_day = "Morning"

    sys "─── DAY 3: MORNING ───"

    # MISS STERN'S HUMANITY
    cora "I was carrying fresh linens down the corridor when I heard it."

    cora "Humming. Low, almost inaudible. A lullaby — the kind my mother used to sing."

    cora "Miss Stern was standing by the window at the end of the hall, holding an envelope. Her eyes were wet."

    cora "For a single, impossible moment, she looked like a woman. Not the iron-spined tyrant who holds my future in her hands. Just a woman reading a letter that made her cry."

    $ heard_stern_humming = True

    stern "Why are you standing there gawping, girl? Those linens won't press themselves."

    cora "The mask snapped back. But I had seen behind it."

    cora "Somehow, that made everything worse. If she were simply cruel, I could hate her. But she's not. She's a woman who made her own choices in a world that gave her very few, and she expects nothing less from me."

    cora "Getting caught by Miss Stern wouldn't just be a professional disaster. It would feel like a betrayal."

    # MORNING WORK — stat maintenance
    menu:
        "I clean the VIP suite. Sir Gideon is out."

        "Clean thoroughly, nothing more (Safe)":
            $ suspicion -= 5
            $ inspiration += 5
            cora "I was a model maid today. Miss Stern would be proud."

        "Search the desk drawers while cleaning (Risky)":
            $ suspicion += 15
            $ inspiration += 15
            cora "I found a journal. Most of it was mundane — appointments, financial notes. But one entry caught my eye."
            cora "A name. An address in Mayfair. And the words: 'She will be here Thursday. Prepare the adjoining suite.'"
            cora "Thursday is tomorrow."

    $ clamp_stats()
    call check_suspicion
    jump day3_night


label day3_night:
    $ time_of_day = "Night"

    sys "─── DAY 3: NIGHT ───"

    menu:
        "The hotel is silent. The gas lamps cast long shadows down the servant's passage."

        "Stay in my quarters tonight (Pure)" if corruption < 30:
            $ corruption -= 5
            cora "I can't keep doing this. The risk is too great. If Miss Stern catches me in that corridor..."
            cora "I sat on my bed and stared at the ceiling and tried not to think about the sounds I heard two nights ago."
            cora "I failed."

        "Return to the servant's passage (The Voyeur Scene)":
            $ corruption += 15
            $ inspiration += 25
            $ suspicion += 15
            $ saw_voyeur_scene = True

            cora "I crept back to the passage. This time I knew exactly where to stand."

            cora "There is a ventilation grate — a lattice of iron barely wider than my hand — that looks directly into the VIP suite's private parlour."

            cora "Sir Gideon was not alone."

            sys "[[CG #1 PLACEHOLDER — THE VOYEUR SCENE: Cora watches through the servant's grate. 3-4 progression stages. This is the first significant 18+ tease. The player sees what Cora sees.]"

            cora "I stood in the dark for what felt like hours. My heart hammering so loudly I was certain they would hear it."

            cora "I saw everything."

            cora "When it was over, I walked back to my room on legs that barely held me. Not from shock — I had read about such things in the penny dreadfuls. But reading about fire and standing in the flames are very different things."

            cora "My mind was already writing the scene. Every detail. Every sound. Every shadow."

    $ clamp_stats()
    call check_suspicion
    jump day3_late_night


label day3_late_night:
    $ time_of_day = "Late Night"

    sys "─── DAY 3: LATE NIGHT ───"

    if saw_voyeur_scene and inspiration >= 25:
        if not wrote_chapter_1:
            cora "I wrote like a woman possessed."
    
            cora "The scene poured out of me — but exaggerated, transformed. Sir Gideon became a dark lord in a candlelit chamber. His companion became a duchess in silks that fell away like water."
    
            cora "It was filth. Absolute, unapologetic filth. And it was the best thing I had ever written."
    
            sys "[[CG #1 FANTASY VARIANT — The screen shifts to a filtered/dream version of BG-03. The player sees Cora's imagination — her manuscript brought to life. This is the 'early gratification' hack: explicit content via Cora's writing, not Cora herself.]"
    
            $ wrote_chapter_1 = True
            $ manuscript_sent = True
    
            cora "I wrapped the pages and addressed them to Holywell Street. The errand boy would carry them tomorrow."
        else:
            cora "I pulled out fresh paper. The first chapter was sent, but I had so much more to say..."
            
            cora "The dark lord's demands escalated. The duchess submitted, not with fear, but with a hunger that matched his own."
            
            sys "[[CG #1 FANTASY VARIANT — Part 2. Cora expands on the prior chapter's concepts.]"
            
            $ wrote_chapter_2 = True
            $ manuscript_sent = True
            
            cora "I wrapped the new pages. Another envelope for Holywell Street."

    else:
        cora "I sat at the desk. The candle guttered. I wrote a few lines, crossed them out, wrote a few more."
        cora "It's not enough. I need more. I need to see what happens behind those walls."

    $ clamp_stats()
    call check_suspicion

    # PAYMENT ARRIVES (if manuscript was sent)
    if manuscript_sent:
        cora "I woke to find a folded note tucked into a package at the tradesmen's entrance, addressed to 'C. at the Savoy, Servant's Hall.'"
        cora "Inside was money. Real money."

        $ payment_received = True

        cora "Three shillings. For a single chapter."
        cora "Three shillings. I earn seven in a week scrubbing floors for sixteen hours a day."
        cora "My hands trembled. Not from the cold."
        cora "This changes everything."

    jump day4_morning


# ═══════════════════════════════════════════════════════════════
#  DAY 4 — THE COMPLICATION
# ═══════════════════════════════════════════════════════════════
label day4_morning:
    $ current_day = 4
    $ time_of_day = "Morning"

    sys "─── DAY 4: MORNING ───"

    cora "Sir Gideon was in the suite again when I arrived."

    if saw_voyeur_scene:
        cora "I could barely look at him. The things I had seen. The things I had written about him."
        cora "He didn't know. He couldn't know. But my face burned all the same."

    gideon "Cora. Sit down for a moment."

    cora "Sit down. A gentleman asking a chambermaid to sit down. In his private suite. This is not how things work."

    cora "I remained standing."

    gideon "You're a sensible girl. You know what they say about me in the staff corridor. Don't pretend you haven't heard."

    cora "I said nothing."

    gideon "This hotel is very quiet in winter. Very quiet. And quiet places make a man think too much."

    $ gideon_showed_depth = True

    cora "For a moment, his face changed. The mask of wealth and confidence slipped, and underneath was something I didn't expect."

    cora "Loneliness."

    cora "Or at least, something that looked like it."

    cora "The man I'd been writing about as a debauched villain — the 'Dark Lord' of my manuscript — was more complicated than I'd assumed. And that made what I was doing feel..."

    cora "I pushed the thought down. I couldn't afford guilt. Not at three shillings a chapter."

    # Light stat maintenance
    menu:
        "I continue cleaning."

        "Finish quickly and leave (Safe)":
            $ suspicion -= 5
            $ inspiration += 5
            cora "I curtseyed and excused myself before anything else could happen."

        "Linger. Let the silence stretch. (Curious)":
            $ suspicion += 10
            $ inspiration += 10
            $ corruption += 5
            cora "I stayed longer than I should have. Polishing brass that was already clean. He didn't speak again, but he watched me work."
            cora "Being watched by Sir Gideon felt different from being watched by Miss Stern. I'm not sure which is more dangerous."

    $ clamp_stats()
    call check_suspicion
    jump day4_night


label day4_night:
    $ time_of_day = "Night"

    sys "─── DAY 4: NIGHT ───"

    cora "Miss Stern has been making extra rounds this week. Her footsteps echo down the servant's passage like a clock ticking toward judgement."

    menu:
        "Tonight is my last chance to gather material before the deadline."

        "Stay in my quarters. The risk is too great. (Pure)" if corruption < 30:
            $ corruption -= 5
            cora "I sat on my bed and listened to my own breathing. The pages on my desk felt like an accusation."
            cora "Safe. Invisible. Exactly what I was raised to be."

        "Return to the passage — spy from a distance (Risky)":
            $ corruption += 10
            $ inspiration += 20
            $ suspicion += 20
            cora "I crept back to the grate. Tonight was different — more urgent, more reckless. Miss Stern's footsteps had passed this corridor not ten minutes ago."
            cora "Through the lattice, I saw Sir Gideon with his guest again. This time, they had left a lamp burning."
            cora "I saw every detail. My mind catalogued it all like a ruthless, mechanical thing."

        "Stay in the passage when I hear footsteps approaching (Bold)":
            $ corruption += 25
            $ inspiration += 10
            $ suspicion += 25
            $ chose_bold_day4 = True
            cora "I didn't just watch tonight. I lingered."
            cora "When I heard movement in the passage behind me, I didn't flee. I pressed myself flat against the wall and held my breath."
            cora "It might have been Miss Stern. It might have been a draught. I'll never know."
            cora "But the thrill of almost being caught — the raw, animal terror of it — was unlike anything I have ever experienced."
            cora "I am no longer the same girl who arrived at this hotel."

    $ clamp_stats()
    call check_suspicion
    jump day4_late_night


label day4_late_night:
    $ time_of_day = "Late Night"

    sys "─── DAY 4: LATE NIGHT ───"

    if inspiration >= 25:
        cora "I wrote the most explicit chapter yet."

        if corruption >= 30:
            cora "My prose was sharper tonight. More confident. I didn't flinch at the words anymore. In fact, I chose them with precision — like a surgeon."
            cora "The naive girl who blushed at the word 'bosom' two days ago was gone. In her place sat a woman who understood that the body is just another landscape to describe."
        else:
            cora "The writing came easier now, though my cheeks still burned at certain passages. I was getting better at this — technically, at least — even if my heart still raced."

        sys "[[CG #2 PLACEHOLDER — FANTASY WRITING SCENE: 'Dark Lord' Sir Gideon, filtered/dream background. Cora's imagination made flesh on the page. 2-3 stages. Reuse Sir Gideon sprite pipeline with filtered BG-03.]"

        $ wrote_chapter_2 = True
        cora "I wrapped the pages. Tomorrow's delivery. My last chapter before the deadline."

    else:
        cora "I tried to write but the material wasn't there. I need more inspiration — more life in these pages."
        cora "Time is running out."

    $ clamp_stats()
    call check_suspicion
    jump day5_morning


# ═══════════════════════════════════════════════════════════════
#  DAY 5 — THE RECKONING
# ═══════════════════════════════════════════════════════════════
label day5_morning:
    $ current_day = 5
    $ time_of_day = "Morning"

    sys "─── DAY 5: MORNING — THE RECKONING ───"

    cora "I knew something was wrong the moment I heard her footsteps outside my door."

    stern "Cora. Open this door."

    cora "Miss Stern stood in my doorway like the angel of judgement. Her eyes swept the room — the bed, the washstand, the desk."

    stern "I've noticed you've been keeping irregular hours. The night porter reported movement in the service corridors past midnight."

    stern "Is there something you'd like to tell me?"

    cora "My manuscript was sitting in plain view on the desk, covered by a single sheet of writing paper."

    # THE CRITICAL CHOICE
    menu:
        "She's looking at the desk."

        "Hide the manuscript — destroy the draft pages (Costly)":
            $ inspiration -= 15
            cora "While her back was turned checking the wardrobe, I shoved the loose pages under the mattress and crumpled the visible sheet."
            cora "She found nothing. But I've lost material. Pages I'll have to rewrite from memory."
            stern "Hmm. See that you keep proper hours, Cora. I will not have slovenly behaviour on my floor."
            cora "She left. My knees buckled."

        "Bluff — 'It's a letter to my mother, ma'am' (Dangerous)":
            $ suspicion += 20
            cora "'It's a letter to my mother, ma'am. I write to her every week.'"
            stern "Every week, is it. You seem to do a great deal of writing for a chambermaid."
            cora "She picked up the sheet on top. My heart stopped."
            cora "It was, mercifully, the cover page — an innocuous description of the hotel. The explicit material was underneath."
            stern "See that your correspondence doesn't interfere with your duties."
            cora "She left. I almost vomited."

    $ clamp_stats()
    call check_suspicion
    jump day5_night


label day5_night:
    $ time_of_day = "Night"

    sys "─── DAY 5: NIGHT — THE CLIMAX ───"

    cora "This is it. The deadline. The publisher on Holywell Street expects the final chapter by morning."

    if corruption >= 40:
        cora "I sat at my desk. I dipped the nib in the ink."

        cora "And I wrote."

        cora "Not the timid, blushing prose of Day 1. Not the overwrought fantasies of Day 3. This was something else entirely."

        cora "It was raw. It was explicit. It was terrifyingly good."

        cora "I wrote about a woman who watches. A woman who desires. A woman who has spent her entire life being invisible and who discovers, in the act of writing, that she has a voice — and that voice is filthy, and powerful, and entirely her own."

        sys "[[CG #3 PLACEHOLDER — DAY 5 CLIMAX: The full, polished payoff scene. 3-4 stages. This is the money shot. This sells subscriptions. Cora's manuscript brought to life in its most explicit form.]"

        cora "When I finished, I stared at the pages."

        if payment_received:
            cora "Three shillings for the first chapter. What would they pay for this?"
            cora "More than I earn in a month scrubbing Sir Gideon's floors. The bitter irony was not lost on me."

        cora "I wrapped the manuscript. The errand boy would carry it to Holywell Street at dawn."

        cora "I sat in the candlelight and looked at my ink-stained fingers and realised something terrible."

        cora "I am good at this."

        cora "And I will never be able to stop."

        jump day5_cliffhanger

    else:
        # BAD ENDING — NOT ENOUGH CORRUPTION
        jump bad_ending_rejection


# ═══════════════════════════════════════════════════════════════
#  THE CLIFFHANGER
# ═══════════════════════════════════════════════════════════════
label day5_cliffhanger:
    # Block rollback so the player can't undo the cliffhanger
    $ renpy.block_rollback()
    $ time_of_day = "Late Night"

    sys "─── DAY 5: LATE NIGHT — THE CLIFFHANGER ───"

    cora "I was about to blow out the candle when I heard it."

    cora "A knock. Soft. Not Miss Stern's sharp rap — something quieter, more deliberate."

    cora "I opened the door."

    cora "Sir Gideon Locke stood in the servant's corridor. In his hand was a single page of manuscript — one I must have dropped on the stairs."

    cora "He read a line aloud. His voice was steady. His eyes were not."

    gideon "You have a very... vivid imagination, Cora."

    cora "My blood ran cold. Then hot. Then something in between."

    gideon "Lock the door."

    sys "═══════════════════════════════════════"
    sys "TO BE CONTINUED."
    sys "═══════════════════════════════════════"

    sys "[[This is the CTA screen. SubscribeStar link. 'Chapter 2 is in development. Subscribe to play it first.']"

    

    return


# ═══════════════════════════════════════════════════════════════
#  FAIL STATES
# ═══════════════════════════════════════════════════════════════

# ── GAME OVER: DISMISSED WITHOUT CHARACTER ────────────────────
label game_over_dismissed:
    hide screen stats_overlay

    sys "═══ GAME OVER: DISMISSED WITHOUT CHARACTER ═══"

    stern "Pack your things."

    cora "Miss Stern did not raise her voice. She didn't need to."

    stern "I trusted you with a position in the finest hotel in London. And you repaid that trust with deception."

    cora "She held up my character reference — the single sheet of paper that represented my entire future — and tore it in half."

    stern "You will leave by the tradesmen's entrance. You will not speak to the other staff. You will not use this hotel as a reference."

    cora "The Savoy's doors closed behind me. I stood on the Strand with nothing but the clothes on my back and the memory of electric light."

    cora "London is very large, and I am very small."

    cora "My family will learn of this. They will not understand. The seven shillings will stop. The village cannot take me back — another mouth to feed and no income to justify it."

    cora "Without a character, no respectable household will hire me. The registry offices will turn me away. The options that remain are the ones they whisper about in the servant's hall."

    cora "The workhouse. The sweatshop. Or the streets."

    cora "I had a talent. I had a chance. And I threw it away because I was too careless, too reckless, too hungry for a life that was never meant for a girl like me."

    sys "[[GAME OVER. Suggest: Load a previous save and make different choices. The margin between ambition and ruin is thinner than you think.]"

    return


# ── BAD ENDING: REJECTION ─────────────────────────────────────
label bad_ending_rejection:
    hide screen stats_overlay

    sys "═══ BAD ENDING: REJECTION ═══"

    cora "I sat at the desk. I wrote. I wrote for hours."

    cora "But the words that came out were... safe. Polite. Bloodless."

    cora "A schoolgirl's fairy tale dressed in a corset. All the right shapes, none of the heat."

    cora "I sent it to Holywell Street anyway. What else could I do?"

    cora "The errand boy returned my manuscript the next morning. Unopened. A note was pinned to the front."

    cora "'We asked for fire. You sent us porridge.'"

    cora "I stared at the note for a long time."

    cora "I am not brave enough. Not worldly enough. Not ruined enough to write what they need."

    cora "I will scrub floors until my hands are raw and my stories die inside me. I will send seven shillings home every month. I will be a good girl."

    cora "And no one will ever read a single word I've written."

    sys "[[BAD ENDING. You survived — but at the cost of your dream. The 'Pure' path is safe, but it is a cage. Try again, and this time, look through the grate.]"

    return
