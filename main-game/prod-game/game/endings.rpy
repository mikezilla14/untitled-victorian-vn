# ═══════════════════════════════════════════════════════════════
#  endings.rpy — FAIL STATES AND BAD ENDINGS
#  All non-cliffhanger terminal labels live here.
#  The cliffhanger (day105_cliffhanger) stays in day105.rpy because
#  it is part of the Day 5 flow. These are branches that break
#  out of the main flow entirely.
# ═══════════════════════════════════════════════════════════════

# ── GAME OVER: DISMISSED (NERVOUS BREAKDOWN) ──────────────────
# Reached when suspicion/anxiety hits 100.
label game_over_dismissed:
    hide screen stats_overlay

    sys_msg "═══ GAME OVER: NERVOUS BREAKDOWN ═══"

    cora "I could not keep the walls of my mind standing."
    cora "It was not a single eye that caught me. It was the weight of them all."
    cora "Vance's sharp contempt, Missy's mounting fear, Stern's cold, measuring gaze... they accumulated in my chest like lead."
    cora "The weight of their combined eyes cracks my mask."
    cora "I made a fatal slip in my duties, and Miss Stern found absolute cause to dismiss me."

    stern "Pack your things. A girl whose nerves are in such tatters cannot be trusted with the Savoy's quiet."

    cora "My hands were shaking too hard to tie my trunk. I stood on the Strand with nothing but a ruined reputation and the memory of electric light."
    cora "Without a character, London is a very cold, very hungry place."

    sys_msg "[[GAME OVER. Your accumulated Anxiety reached 100%%, causing a complete breakdown and leading to your dismissal. Manage your internal strain by spreading suspicion across different characters and triggering penances before your nerves fail you.]"

    return


# ── BAD ENDING: REJECTION ─────────────────────────────────────
# Reached when corruption_level < 3 by Day 5 night.
# Cora survives but her dream dies. The 'Pure' path has a cost.
label bad_ending_rejection:
    hide screen stats_overlay

    sys_msg "═══ BAD ENDING: REJECTION ═══"

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

    sys_msg "[[BAD ENDING. You survived — but at the cost of your dream. The 'Pure' path is safe, but it is a cage. Try again, and this time, look through the grate.]"

    return


# ── GAME OVER: FIRST DEADLINE FAILED ──────────────────────────
# Reached when Chapter 1 is not written by Day 2 Night.
label game_over_deadline_1:
    hide screen stats_overlay
    sys_msg "═══ GAME OVER: FIRST DEADLINE FAILED ═══"
    cora "I stare at the blank page."
    cora "Day 2 has ended, and I have not even written the first chapter."

    if story.has_manuscript_chapter("day1_slop_chapter"):
        cora "I did write, but it was flavorless slop. Unsellable, bloodless, afraid of its own pulse."
        cora "My ambition is nothing but a childish delusion if I cannot bring myself to write the transgressive reality of this house."
        sys_msg "[[GAME OVER. You wrote a slop chapter instead of Chapter 1 because your Corruption level was too low (<= 2). Manage your choices to build appetite before writing.]"
    elif player.inspiration < 15:
        cora "My mind was a dry well. I lacked the Inspiration to form the first sentence."
        sys_msg "[[GAME OVER. You failed to write Chapter 1 because your Inspiration was below 15. Spend your time and choices wisely to gather inspiration before writing.]"
    elif player.corruption_level < 2:
        cora "I lacked the appetite, the dark resolve to write the transgressive truth of what I saw."
        sys_msg "[[GAME OVER. You failed to write Chapter 1 because your Corruption level was below 2. Look through the grates and explore the transgressive paths to build corruption.]"
    else:
        cora "I chose to rest, to walk corridors, or to search for company instead of dedicating myself to the page."
        sys_msg "[[GAME OVER. You failed to write Chapter 1 because you did not use your writing slots to progress the manuscript. Protect your writing slots!]"

    cora "I have failed before I even truly began."
    return


# ── GAME OVER: DRAFT DEADLINE FAILED ──────────────────────────
# Reached when Chapter 2 is not completed by Day 4 Night.
label game_over_deadline_2:
    hide screen stats_overlay
    sys_msg "═══ GAME OVER: DRAFT DEADLINE FAILED ═══"
    cora "The night of Day 4 passes into grey dawn."
    cora "My desk is littered with scraps of paper, but the draft is incomplete. I have only one chapter done."

    if player.inspiration < 30:
        cora "My mind was too scattered, my internal strain too high. I lacked the Inspiration to complete the second chapter."
        sys_msg "[[GAME OVER. You failed to complete Chapter 2 because your Inspiration was below 30. Ensure you build enough inspiration before the deadline.]"
    elif player.corruption_level < 3:
        cora "I lacked the appetite, the dark resolve to write the transgressive truth of the Savoy's corridors."
        sys_msg "[[GAME OVER. You failed to complete Chapter 2 because your Corruption level was below 3. Build corruption by choosing transgressive actions and observing secrets.]"
    else:
        cora "I chose safety, barricaded my door, or sneaked feels instead of committing the ink to the page."
        sys_msg "[[GAME OVER. You failed to complete Chapter 2 because you did not use your writing slots to finish the second chapter. Protect your writing slots!]"

    cora "I have lost my chance. The door is closed."
    return
