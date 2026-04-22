# ═══════════════════════════════════════════════════════════════
#  day3.rpy — THE VOYEUR
#  The pivotal day. Miss Stern's humanity is revealed (raising
#  the moral stakes of getting caught). The grate scene is the
#  first significant 18+ tease and the primary inspiration
#  source. Payment arrives if a chapter was sent.
# ═══════════════════════════════════════════════════════════════

label day3_morning:
    $ time_manager.set_current_day(3)
    $ set_time_period("Morning")

    sys "─── DAY 3: MORNING ───"

    cora  "I was carrying fresh linens down the corridor when I heard it."
    cora  "Humming. Low, almost inaudible. A lullaby — the kind my mother used to sing."
    cora  "Miss Stern was standing by the window at the end of the hall, holding an envelope. Her eyes were wet."
    cora  "For a single, impossible moment, she looked like a woman. Not the iron-spined tyrant who holds my future in her hands. Just a woman reading a letter that made her cry."

    $ story.set_has_heard_stern_humming(True)

    stern "Why are you standing there gawping, girl? Those linens won't press themselves."

    cora  "The mask snapped back. But I had seen behind it."
    cora  "Somehow, that made everything worse. If she were simply cruel, I could hate her. But she's not. She's a woman who made her own choices in a world that gave her very few, and she expects nothing less from me."
    cora  "Getting caught by Miss Stern wouldn't just be a professional disaster. It would feel like a betrayal."

    menu:
        "I clean the VIP suite. Sir Gideon is out."

        "Clean thoroughly, nothing more (Safe)":
            $ apply_effects(insp=5, susp=-5)
            cora "I was a model maid today. Miss Stern would be proud."

        "Search the desk drawers while cleaning (Risky)":
            $ apply_effects(insp=15, susp=15)
            cora "I found a journal. Most of it was mundane — appointments, financial notes. But one entry caught my eye."
            cora "A name. An address in Mayfair. And the words: 'She will be here Thursday. Prepare the adjoining suite.'"
            cora "Thursday is tomorrow."

    $ resolve_turn()
    jump day3_night


label day3_night:
    $ set_time_period("Night")

    sys "─── DAY 3: NIGHT ───"

    menu:
        "The hotel is silent. The gas lamps cast long shadows down the servant's passage."

        "Stay in my quarters tonight (Pure)" if player.corruption_level < 2:
            $ apply_effects(corr=-5)
            cora "I can't keep doing this. The risk is too great. If Miss Stern catches me in that corridor..."
            cora "I sat on my bed and stared at the ceiling and tried not to think about the sounds I heard two nights ago."
            cora "I failed."

        "Return to the servant's passage (The Voyeur Scene)":
            $ apply_effects(insp=25, corr=15, susp=15)
            $ story.set_has_witnessed_voyeur_scene(True)

            cora "I crept back to the passage. This time I knew exactly where to stand."
            cora "There is a ventilation grate — a lattice of iron barely wider than my hand — that looks directly into the VIP suite's private parlour."
            cora "Sir Gideon was not alone."

            sys "[[CG #1 PLACEHOLDER — THE VOYEUR SCENE: Cora watches through the servant's grate. 3-4 progression stages. This is the first significant 18+ tease. The player sees what Cora sees.]"

            cora "I stood in the dark for what felt like hours. My heart hammering so loudly I was certain they would hear it."
            cora "I saw everything."
            cora "When it was over, I walked back to my room on legs that barely held me. Not from shock — I had read about such things in the penny dreadfuls. But reading about fire and standing in the flames are very different things."
            cora "My mind was already writing the scene. Every detail. Every sound. Every shadow."

    $ resolve_turn()
    jump day3_late_night


label day3_late_night:
    $ set_time_period("Late Night")

    sys "─── DAY 3: LATE NIGHT ───"

    if story.has_witnessed_voyeur_scene and player.inspiration >= 25:
        if not story.has_written_first_chapter:
            cora "I wrote like a woman possessed."
            cora "The scene poured out of me — but exaggerated, transformed. Sir Gideon became a dark lord in a candlelit chamber. His companion became a duchess in silks that fell away like water."
            cora "It was filth. Absolute, unapologetic filth. And it was the best thing I had ever written."

            sys "[[CG #1 FANTASY VARIANT — The screen shifts to a filtered/dream version of BG-03. The player sees Cora's imagination — her manuscript brought to life. 'Early gratification' via Cora's writing, not Cora herself.]"

            $ story.set_has_written_first_chapter(True)
            $ story.set_has_sent_manuscript(True)

            cora "I wrapped the pages and addressed them to Holywell Street. The errand boy would carry them tomorrow."
        else:
            cora "I pulled out fresh paper. The first chapter was sent, but I had so much more to say..."
            cora "The dark lord's demands escalated. The duchess submitted, not with fear, but with a hunger that matched his own."

            sys "[[CG #1 FANTASY VARIANT — Part 2. Cora expands on the prior chapter's concepts.]"

            $ story.set_has_written_second_chapter(True)
            $ story.set_has_sent_manuscript(True)

            cora "I wrapped the new pages. Another envelope for Holywell Street."
    else:
        cora "I sat at the desk. The candle guttered. I wrote a few lines, crossed them out, wrote a few more."
        cora "It's not enough. I need more. I need to see what happens behind those walls."

    $ resolve_turn()

    # ── PAYMENT ARRIVES ────────────────────────────────────────
    # Only triggers if a chapter was dispatched before this point.
    if story.has_sent_manuscript:
        cora "I woke to find a folded note tucked into a package at the tradesmen's entrance, addressed to 'C. at the Savoy, Servant's Hall.'"
        cora "Inside was money. Real money."

        $ story.set_has_received_manuscript_payment(True)

        cora "Three shillings. For a single chapter."
        cora "Three shillings. I earn seven in a week scrubbing floors for sixteen hours a day."
        cora "My hands trembled. Not from the cold."
        cora "This changes everything."

    jump day4_morning
