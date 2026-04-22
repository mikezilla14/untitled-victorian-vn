# ═══════════════════════════════════════════════════════════════
#  day4.rpy — THE COMPLICATION
#  Gideon's humanity is revealed (mirroring Stern's on Day 3).
#  The moral stakes deepen: Cora is writing about a real person
#  who turns out to be more than a villain. Miss Stern begins
#  extra rounds, ratcheting external pressure.
# ═══════════════════════════════════════════════════════════════

label day4_morning:
    $ time_manager.current_day  = 4
    $ set_time_period("Morning")

    sys "─── DAY 4: MORNING ───"

    cora "Sir Gideon was in the suite again when I arrived."

    if story.saw_voyeur_scene:
        cora "I could barely look at him. The things I had seen. The things I had written about him."
        cora "He didn't know. He couldn't know. But my face burned all the same."

    gideon "Cora. Sit down for a moment."

    cora   "Sit down. A gentleman asking a chambermaid to sit down. In his private suite. This is not how things work."
    cora   "I remained standing."

    gideon "You're a sensible girl. You know what they say about me in the staff corridor. Don't pretend you haven't heard."

    cora   "I said nothing."

    gideon "This hotel is very quiet in winter. Very quiet. And quiet places make a man think too much."

    $ story.gideon_showed_depth = True

    cora   "For a moment, his face changed. The mask of wealth and confidence slipped, and underneath was something I didn't expect."
    cora   "Loneliness."
    cora   "Or at least, something that looked like it."
    cora   "The man I'd been writing about as a debauched villain — the 'Dark Lord' of my manuscript — was more complicated than I'd assumed. And that made what I was doing feel..."
    cora   "I pushed the thought down. I couldn't afford guilt. Not at three shillings a chapter."

    menu:
        "I continue cleaning."

        "Finish quickly and leave (Safe)":
            $ apply_effects(insp=5, susp=-5)
            cora "I curtseyed and excused myself before anything else could happen."

        "Linger. Let the silence stretch. (Curious)":
            $ apply_effects(insp=10, corr=5, susp=10)
            cora "I stayed longer than I should have. Polishing brass that was already clean. He didn't speak again, but he watched me work."
            cora "Being watched by Sir Gideon felt different from being watched by Miss Stern. I'm not sure which is more dangerous."

    $ resolve_turn()
    jump day4_night


label day4_night:
    $ set_time_period("Night")

    sys "─── DAY 4: NIGHT ───"

    cora "Miss Stern has been making extra rounds this week. Her footsteps echo down the servant's passage like a clock ticking toward judgement."

    menu:
        "Tonight is my last chance to gather material before the deadline."

        "Stay in my quarters. The risk is too great. (Pure)" if player.corruption_level < 2:
            $ apply_effects(corr=-5)
            cora "I sat on my bed and listened to my own breathing. The pages on my desk felt like an accusation."
            cora "Safe. Invisible. Exactly what I was raised to be."

        "Return to the passage — spy from a distance (Risky)":
            $ apply_effects(insp=20, corr=10, susp=20)
            cora "I crept back to the grate. Tonight was different — more urgent, more reckless. Miss Stern's footsteps had passed this corridor not ten minutes ago."
            cora "Through the lattice, I saw Sir Gideon with his guest again. This time, they had left a lamp burning."
            cora "I saw every detail. My mind catalogued it all like a ruthless, mechanical thing."

        "Stay in the passage when I hear footsteps approaching (Bold)":
            $ apply_effects(insp=10, corr=25, susp=25)
            $ story.chose_bold_day4 = True
            cora "I didn't just watch tonight. I lingered."
            cora "When I heard movement in the passage behind me, I didn't flee. I pressed myself flat against the wall and held my breath."
            cora "It might have been Miss Stern. It might have been a draught. I'll never know."
            cora "But the thrill of almost being caught — the raw, animal terror of it — was unlike anything I have ever experienced."
            cora "I am no longer the same girl who arrived at this hotel."

    $ resolve_turn()
    jump day4_late_night


label day4_late_night:
    $ set_time_period("Late Night")

    sys "─── DAY 4: LATE NIGHT ───"

    if player.inspiration >= 25:
        cora "I wrote the most explicit chapter yet."

        if player.corruption_level >= 2:
            cora "My prose was sharper tonight. More confident. I didn't flinch at the words anymore. In fact, I chose them with precision — like a surgeon."
            cora "The naive girl who blushed at the word 'bosom' two days ago was gone. In her place sat a woman who understood that the body is just another landscape to describe."
        else:
            cora "The writing came easier now, though my cheeks still burned at certain passages. I was getting better at this — technically, at least — even if my heart still raced."

        sys "[[CG #2 PLACEHOLDER — FANTASY WRITING SCENE: 'Dark Lord' Sir Gideon, filtered/dream background. 2-3 stages. Reuse Sir Gideon sprite with filtered BG-03.]"

        $ story.wrote_chapter_2 = True
        cora "I wrapped the pages. Tomorrow's delivery. My last chapter before the deadline."
    else:
        cora "I tried to write but the material wasn't there. I need more inspiration — more life in these pages."
        cora "Time is running out."

    $ resolve_turn()
    jump day5_morning
