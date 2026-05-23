# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes

# day100_non_canon.rpy
# Release 1 / Day 00 / Prologue non-canon Ren'Py-shaped draft
# Source intent: rewritten from Twine node map and outline.
# Asset constraint: uses train carriage, country estate study, themes/melancholy, sfx/train_whistle.

# ==========================================
# MAIN ENTRY
# ==========================================

label day100_main:

    # [BEAT] Set the initial scene of Cora's journey to London
    # [ASSET] Visual/staging command
    scene bg_train_carriage_day
    with fade

    "The rhythm of the train carriage is a cold, mechanical pulse."
    "Every joint in the iron rails clicks like a latch closing behind me, locking the green fields of Wiltshire away in the dust."
    "I keep my knees pulled tight, my elbows pinned to my ribs, trying to occupy as little space as possible in the crowded compartment."
    "The air is thick with the close, humid atmosphere of third-class transit—scents of wet wool, cheap coal grease, and damp skin."
    "I watch the sheep on the hillsides yield to grey slate roofs, then to brick kilns, and finally to the low, creeping soot that marks the boundary of London."

    "In Wiltshire, I had a benefactor. In Wiltshire, I had a name."
    "Here, I have a forged reference in my pocket, a half-filled satchel, and the silence of a girl who knows she must not be looked at too closely."
    "My body carries a hot, trembling inclination, a secret weight that feels heavier than the forged paper."

    "My eyes grow heavy under the monotonous lull of the wheels."
    "The soot-smeared glass turns dark, and in the reflection, the carriage-glare dissolves into the dark oak and velvet drapes of a country library..."

    # [STATE] State/progression update
    jump day100_2_discovery_flashback


# ==========================================
# P-02 - THE DISCOVERY (FLASHBACK)
# ==========================================

label day100_2_discovery_flashback:

    # [ASSET] Visual/staging command
    scene bg_country_estate_study
    with dissolve

    # [ASSET] Visual/staging command
    play music "themes/melancholy" fadein 1.5

    "Sir John's library was the only territory in Wiltshire where I could breathe, a quiet sanctuary where I was allowed to enter only by license."
    "It smelled of dried roses and calfskin bindings—objects preserved for those who could afford the dust."
    "He was a man of quiet habits and immense, private wealth, who had inexplicably permitted his library maid to learn to read."
    "Perhaps he thought a girl who could read the titles would be more efficient at dusting the bindings; perhaps he simply did not care enough to forbid it, treating me as walking furniture."

    "But a girl who learns to read does not stop at the spines."

    "It was a Tuesday afternoon. The house was quiet with the heavy, afternoon silence of Wiltshire estates, where even the grandfather clock seems to tick with a country drawl."
    "The velvet drapes hung thick, keeping the cold autumn air out and the library's heavy heat in."
    "I had been sent to the master's study to dust the mahogany bureau. The desk lay open, his keys left in the brass lock."
    "Papers lay scattered across the leather blotter, catching the pale, dusty light—an archive of things Sir John wished to bury, exposed to the chambermaid's eyes."
    "At that very moment, a sound drifted from the adjoining parlour behind the heavy oak door."

    # [CHOICE] Decision point
    menu:
        "The parlour's raw breath, or the desk's quiet ink?"

        "Investigate the parlour door. [Overhear dismissal: +15 Corruption]":

            # [STATE] State/progression update
            $ apply_effects(insp=0, corr=15, susp=0)
            $ story.set_prologue_found("overheard")

            jump day100_2_parlour_branch

        "Continue with duties at the desk. [Read letters: +15 Inspiration, +10 Corruption]":

            # [STATE] State/progression update
            $ apply_effects(insp=15, corr=10, susp=0)
            $ story.set_prologue_found("read_letters")

            jump day100_2_desk_branch


label day100_2_parlour_branch:

    "The sound is not a dropped tea-service. It is not the clean, loud clatter of servants."
    "It is a soft, wet murmur. A sudden, sharp gasp that catches in the throat and is held there—desperate, improper, and raw."

    "I move without thinking, my boots making no sound on the heavy Persian rug. To touch the handle would be a dismissal; to press my ear to the panel is a theft."
    "I press my ear to the cold, panelled oak of the parlour door. The wood carries the warmth of the room beyond, and the voices."
    "Sir John's voice has lost its parliamentary weight. It is thin, ragged, and pleading like a creature trapped in its own skin."

    "Sir John" "No... George, please. The housemaid is in the hall. She has the dusting-license..."
    "George" "The housemaid does not exist, John. She is only furniture that walks. Let the door be open—your skin is too hot for locks."

    "I hold my breath."
    "A soft, damp moan follows, and my thighs press together in the dark corridor. The wood feels hot against my skin."
    "The words are raw, stripped of the fine grammar Sir John uses when he speaks to the vicar."
    "It is the language of appetite—urgent, heavy, and absolute."
    "I feel a strange, cold heat rise in my chest. The world is not made of rules and sermons; it is made of secret rooms, private transgression, and men who kneel when the door is shut."

    # [STATE] State/progression update
    jump day100_2_reconvergence


label day100_2_desk_branch:

    "The parlour door remains shut, but the letters on the desk are a louder invitation."
    "The bureau keys are left in the lock, exposing a wild, frantic ledger of want."
    "The ink is fresh. The handwriting is Sir John's, but it has lost its usual ledger-like precision."
    "The letters are sloped, frantic, crowded together as if the hand that held the pen were shaking with a fever."

    "I reach out, my fingers hovering over the open page. My eyes trace the frantic lines."

    "Cora (reading)" "'...the taste of your skin in the shadow of the bureau remains my only memory. I have written your name on my palms... I have catalogued every glance, every brief collision of our sleeves, like a miser counting his remaining pence...'"

    "My breath catches, and a flush rises on my neck."
    "The written word has a weight I had not understood—a physical power to evoke illicit desire."
    "It can turn a baronet into a beggar; it can make the most improper desires look like liturgy."
    "The letter is to George. It details dates, a room in London, a deposit in a London bank, and a photograph kept in a locked box at the Savoy."
    "In reading them, I steal the ink. A maid who can copy such a hand is no longer just a maid; she is a dangerous cataloguer, holding a key that can pick any lockbox."

    # [STATE] State/progression update
    jump day100_2_reconvergence


label day100_2_reconvergence:

    "The world shatters with the click of a latch."
    "I draw back, but Sir John is already in the study."
    "His chest is rising and falling, his collar slightly loose, his face grey with the terror of a man who knows his secret is no longer his own."
    "He looks at me, his eyes dark with a trembling shame and fear."

    "Sir John" "Cora Vale."
    "cora" "Sir..."
    "Sir John" "You are dismissed. You will leave the estate before nightfall."
    "Sir John" "And if a single word of what you have seen—or read—leaves your mouth, I will see to it that no decent house in England ever takes you in. Your name will be blackened in every registry."

    "The shadow of his threat is the last thing I see in Wiltshire."
    "The memories pull back, dissolving into the iron rattle of the present..."

    # [STATE] State/progression update
    $ renpy.block_rollback()

    # [STATE] State/progression update
    jump day100_3_awakening


# ==========================================
# P-03 - AWAKENING
# ==========================================

label day100_3_awakening:

    # [ASSET] Visual/staging command
    scene bg_train_carriage_day
    with dissolve

    # [ASSET] Visual/staging command
    play sound "sfx/train_whistle"

    "A sharp, metallic shriek tears through my ears."
    "I jolt awake, my forehead striking the soot-chilled glass of the window, skin flushed from the memory's heat."
    "The train is plunging into a brick tunnel, the carriage rattling violently over the iron tracks."

    "My satchel has slipped from my lap during my sleep, its buckle open."
    "On the floorboards, scattered at my boots, are the sheets I have carried all the way from Wiltshire."
    "A half-written manuscript of a highly improper nature, detailing the secret lives of the gentry."
    "And beneath them, the forged reference from Sir John's estate—a perfect lie written in a neat, servant's hand."
    "The gentleman sitting opposite me is lowering his newspaper, his eyes drifting down toward the scattered, scandalous lines."

    "I scramble in a panic, my fingers burning as I sweep the sheets away from his gaze before he can read a single paragraph."
    "If anyone were to examine these sheets... if a conductor were to read even a line..."
    "I would not merely lose my chance at the Savoy. I would be ruined before I ever stepped onto the platform."

    cora "I must be mindful. The city will afford no second chances to a chambermaid with such secrets."

    "I gather the papers, tucking my secrets safely back into the dark recess of the satchel and clamping it shut."
    "Outside the soot-stained window, the brick tunnels give way to the sprawling, iron architecture of Waterloo Station."
    "The brooding skyline of London looms through the grey smog, magnificent and indifferent."

    "My new position at the Savoy awaits."
    "I bring my broom, my apron, and my forged references."
    "But I bring my inclinations with me."

    # [STATE] State/progression update
    jump day101_main
