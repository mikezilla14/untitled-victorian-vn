# SPEC SCRIPT — NON-CANON — HUMAN REVIEW
# day101_tension_spec.rpy
# Release 1 / Day 01 / Tension Lens

label day101_main_tension:
    scene bg_savoy_corridor_morning
    with fade

    "The Savoy Hotel did not welcome girls like me."
    "It consumed them quietly, polished the brass after, and called the result service."
    "Every step I take is a gamble against time and discovery."
    "The forged references in my pocket are warm from my palm. If they look too closely at the watermarks, the police will be waiting at the service exit before noon."

    jump day101_1_morning_interview_tension


label day101_1_morning_interview_tension:
    scene bg_savoy_corridor_morning
    with dissolve
    show stern_sprite neutral at center

    "Miss Stern stands rather than sits. Her posture is a threat, a silent interrogation."
    "Her eyes drill into mine, looking for the tiny tremor that betrays a liar."
    "The clock on her mantelpiece ticks like a small hammer striking iron."

    stern "Cora Vale."
    cora "Yes, Ma'am."
    stern "Wishing is for girls with leisure. You will work because you are told."
    cora "Yes, Ma'am."

    "She is waiting for me to trip on my own tongue. Every syllable is a narrow bridge."

    jump day101_1_vance_throws_toy_tension


label day101_1_vance_throws_toy_tension:
    show vance_sprite angry at left
    "Then something small and silver strikes the skirting board and spins across the carpet, stopping centimeters from my toe."
    "A lady's toy. A trap."

    vance "You. Girl. Pick it up."

    "I bend. My chest tightens. If I move too quickly, I look guilty; if too slowly, insolent."

    show gideon_sprite cold at right
    gideon "Vance."
    "The corridor changes temperature instantly."
    "Mr. Locke stands there. His eyes do not look at me; they scan the hall for any breach of his absolute order."

    vance "I was only correcting her."
    gideon "You were making yourself visible."
    gideon "The girl is new. Do not teach her bad habits before luncheon."

    "I hold my breath. If I look up, Mr. Locke might see the Wiltshire sun in my eyes. I keep my chin pinned to my collar."

    jump day101_2_coras_path_choice_tension


label day101_2_coras_path_choice_tension:
    scene bg_servants_corridor_dim
    with fade

    "The servants' corridor behind the guest wing is narrower than it should be."
    "The walls carry sound the way a body carries fever. Every floorboard is a potential alarm."
    "Beyond a service door near the Master Suite: a sharp, wet sound."

    vance "Please. I understand. I do."

    show missy_sprite shocked at left
    missy "Was that Miss Vance? Should we fetch Miss Stern?"

    "Missy's hand is shaking. My heart is a drum in my ears."
    "If we are caught eavesdropping here, we are not merely dismissed — we are ruined."

    menu:
        "The risk of the door, or the safety of silence?"

        "Look for myself. [Prey path: +Inspiration, +Suspicion]":
            $ apply_effects(vance_susp=35, insp=15, corr=5)
            $ story.set_corridor_state("prey")
            cora "Stay there."
            cora "Quiet."

            "I step toward the door. The floorboards moan under my weight like dying men."
            "Through the crack, I see Vance kneeling. Mr. Locke holds her chin with two fingers."
            "Gideon" "Do we have an audience?"
            "My breath catches. His eyes move toward the door."
            "I stumble back, my boot heel catching on a seam in the carpet."
            "Missy grabs my sleeve and drags me into the shadow of the bend just as the door latch clicks."
            "We crouch in the dark, holding our breath, waiting for the heavy tread of his boots to find us."

        "Pull Missy away. [Ghost path: +Inspiration, -Suspicion]":
            $ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5, insp=10, corr=0)
            $ story.set_corridor_state("ghost")
            cora "No."
            "I grab her wrist. The skin of her arm is cold. We must slip away like fog before the Master turns his face our way."

    call end_slot(outcome="d1_reflect_done")
