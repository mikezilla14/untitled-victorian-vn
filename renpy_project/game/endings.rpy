# ═══════════════════════════════════════════════════════════════
#  endings.rpy — FAIL STATES AND BAD ENDINGS
#  All non-cliffhanger terminal labels live here.
#  The cliffhanger (day5_cliffhanger) stays in day5.rpy because
#  it is part of the Day 5 flow. These are branches that break
#  out of the main flow entirely.
# ═══════════════════════════════════════════════════════════════

# ── GAME OVER: DISMISSED WITHOUT CHARACTER ────────────────────
# Reached when suspicion hits 100.
# The authentic historical fail state: no character reference
# means no future in service — and very few alternatives.
label game_over_dismissed:
    hide screen stats_overlay

    sys "═══ GAME OVER: DISMISSED WITHOUT CHARACTER ═══"

    stern "Pack your things."

    cora  "Miss Stern did not raise her voice. She didn't need to."

    stern "I trusted you with a position in the finest hotel in London. And you repaid that trust with deception."

    cora  "She held up my character reference — the single sheet of paper that represented my entire future — and tore it in half."

    stern "You will leave by the tradesmen's entrance. You will not speak to the other staff. You will not use this hotel as a reference."

    cora  "The Savoy's doors closed behind me. I stood on the Strand with nothing but the clothes on my back and the memory of electric light."
    cora  "London is very large, and I am very small."
    cora  "My family will learn of this. They will not understand. The seven shillings will stop. The village cannot take me back — another mouth to feed and no income to justify it."
    cora  "Without a character, no respectable household will hire me. The registry offices will turn me away. The options that remain are the ones they whisper about in the servant's hall."
    cora  "The workhouse. The sweatshop. Or the streets."
    cora  "I had a talent. I had a chance. And I threw it away because I was too careless, too reckless, too hungry for a life that was never meant for a girl like me."

    sys "[[GAME OVER. Suggest: Load a previous save and make different choices. The margin between ambition and ruin is thinner than you think.]"

    return


# ── BAD ENDING: REJECTION ─────────────────────────────────────
# Reached when corruption_level < 3 by Day 5 night.
# Cora survives but her dream dies. The 'Pure' path has a cost.
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
