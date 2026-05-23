# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day101_erotic_spec.rpy
# Release 1 / Day 01 / Erotic Lens

label day101_main_erotic:
    scene bg_savoy_corridor_morning
    with fade

    "The Savoy Hotel did not welcome girls like me."
    "It consumed them quietly, polished the brass until it shone like a mirror, and watched them sweat in the reflection."
    "The air inside was thick, smelling of beeswax, heavy French perfumes, and the warm breath of wealthy guests sleeping behind thick mahogany doors."
    "It was a house built on private appetites, and I had come to feed my own."

    jump day101_1_vance_throws_toy_erotic


label day101_1_vance_throws_toy_erotic:
    show vance_sprite angry at left
    "Then something small and silver strikes the skirting board and rolls across the plush carpet, stopping against my shoe."
    "A lady's silver toy, warm from her fingers."

    vance "You. Girl. Pick it up."

    "I bend. My thighs press against the stiff canvas of my underskirt. I feel the warmth of the corridor air on the nape of my neck as my collar pulls tight."
    "I lift the trinket. It is cool and smooth, but carries the scent of Vance's rosewater."

    vance "Not like that. Have you never handled anything delicate?"

    "My fingers brush her glove as I return it. The kidskin is soft, almost like skin, but colder."
    "She smells of expensive dust and sharp, nervous heat."

    show gideon_sprite cold at right
    gideon "Vance. You are making yourself visible."

    "Mr. Locke's voice is a low, heavy weight in the corridor. It makes the hair on my arms stand up."
    "His eyes brush over me, not as a man looks at a maid, but as a buyer touches a fabric, measuring the quality of the thread."

    gideon "The girl is new. Do not teach her bad habits before luncheon."

    "I keep my eyes lowered, but I watch the way Vance's throat moves as she swallows her reply."
    "A command. A yielding. The air between them is charged with something thick and dangerous."

    jump day101_2_coras_path_choice_erotic


label day101_2_coras_path_choice_erotic:
    scene bg_servants_corridor_dim
    with fade

    "The servants' corridor is narrow and warm, carrying the heat from the kitchens below."
    "Through the service door near the Master Suite, we hear a sound. Not a cry of pain, but a sharp, wet breath."

    vance "Please. I understand. I do."

    show missy_sprite shocked at left
    missy "Should we fetch Miss Stern?"

    "Missy's face is flushed from the laundry steam, her lips slightly parted."
    "The moment is a choice of how we consume the master's secrets."

    menu:
        "How do do I watch?"

        "Let Missy's concern open the door. [Predator path: +Inspiration, +Corruption]":
            $ apply_effects(missy_susp=10, insp=10, corr=5)
            $ story.set_corridor_state("predator")
            cora "You may be right. If she's hurt, someone should check."

            "I press my shoulder against Missy's as she reaches for the latch."
            "I feel the rapid thrum of her pulse through her sleeve, the heat of her skin. We are too close, sharing the illicit thrill of the keyhole."
            "Through the crack, I see Vance kneeling on the dark wool carpet."
            "Her head is bent, exposing the white curve of her neck."
            "Mr. Locke holds her chin with two fingers, his thumb tracing the line of her jaw with slow, deliberate pressure."
            "Gideon" "Again."
            "Vance" "I forgot myself, Sir."
            "The submission in her voice is a physical weight. I feel a slow, warm throb at the base of my throat."
            "Missy pulls the door shut, her breath coming in short, ragged gasps."
            "missy" "Oh. Oh, Cora. We shouldn't have..."
            "cora" "We saw nothing."
            "But the image remains, burned into the dark behind my eyes."

    jump day101_4_visit_missy_erotic


label day101_4_visit_missy_erotic:
    scene bg_servants_quarters_dusk
    with fade
    show missy_sprite smiling at center

    "I leave the candle unlit."
    "The dark in the quarters is soft, smelling of lavender and laundry lye."
    "I knock on Missy's door. She answers in her chemise, the white linen loose around her shoulders."

    missy "Cora? You shouldn't be here."
    cora "I couldn't sleep."

    "She shifts on the narrow straw mattress, making room for me."
    "The bed is small. When I sit, our hips touch, the thin fabric of our nightgowns offering no barrier to the heat of our bodies."

    missy "About earlier... we shouldn't have looked."
    cora "But we did."

    "I reach out, my fingers brushing a damp curl away from her cheek. Her skin is soft, slightly damp from the night air."
    "missy" "Cora..."
    "The hotel watches us through the floorboards, but in the dark, the machine feels far away."
    call end_slot(outcome="d1_visit_missy")
