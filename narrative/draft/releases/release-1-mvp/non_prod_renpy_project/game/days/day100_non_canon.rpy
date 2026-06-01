# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes
#
# SPRITE DIRECTION (managed by scripts/scene_direction.py — how to preserve manual staging):
# [asset auto]              -> auto-placed sprite line; the agent may rewrite/replace it on re-run
# [asset keep]              -> on a show line: lock THAT line so the agent never edits it
# [asset lock:scene]        -> before/after a `scene`: the agent skips the entire scene block
# [asset pin:Name=slot]     -> force Name into slot for the rest of the scene block
# [enter:Name] / [exit:Name] -> declare cast changes so auto placement stays correct
# Full policy: docs/contracts/sprite_layout_policy.yaml | spec: docs/specs/scene-direction-agent.md

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
    "I keep my knees pulled tight, my elbows pinned to my ribs, trying to occupy as little space as possible in the crowded third-class compartment. The heat of the passenger sitting opposite me—a stout, soot-dusted laborer—brushes against my wool skirt with every lurch of the carriage. It is improper, this unavoidable friction of strangers, yet the stifling warmth is almost a relief against the autumn chill."
    "The air is thick with the close, humid atmosphere of third-class transit—scents of wet wool, cheap coal grease, and damp skin."
    "I watch the sheep on the hillsides yield to grey slate roofs, then to brick kilns, and finally to the low, creeping soot that marks the boundary of London."

    "In Wiltshire, I had a benefactor. In Wiltshire, I had a name. And in Wiltshire, I discovered the delicious, terrifying truth of what lies beneath the buttoned-up silence of the high-born."
    "Here, I have a forged reference in my pocket, a half-filled satchel, and the silence of a girl who knows she must not be looked at too closely. But my body carries a hot, trembling inclination, a secret weight that feels heavier than the forged paper. An appetite for things no decent servant-girl should ever know, much less write down."

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

    "Sir John's library was the only territory in Wiltshire where I could breathe, a quiet sanctuary where I was allowed to enter only by license. The room was always thick with a heavy, stifling heat that seemed to belong to another climate entirely—perfumed by the sweet, decayed scent of dried roses, calfskin bindings, and the sharp bite of his private tobacco."
    "He was a man of quiet habits, immense, private wealth, and a terrifyingly cold composure, who had inexplicably permitted his library maid to learn to read."
    "Perhaps he thought a girl who could read the titles would be more efficient at dusting the bindings; perhaps he simply did not care enough to forbid it, treating me as walking furniture."

    "But a girl who learns to read does not stop at the spines. She learns to read the spaces between them, the secrets hidden in the desk drawers, and the dark, unwritten impulses of the men who rule the house."

    "It was a Tuesday afternoon. The house was quiet with the heavy, afternoon silence of Wiltshire estates, where even the grandfather clock seems to tick with a country drawl."
    "The velvet drapes hung thick, keeping the cold autumn air out and the library's heavy heat in."
    "I had been sent to the master's study to dust the mahogany bureau. The desk lay open, his keys left in the brass lock."
    "Papers lay scattered across the leather blotter, catching the pale, dusty light—an archive of things Sir John wished to bury, exposed to the chambermaid's eyes."
    "At that very moment, a sound drifted from the adjoining parlour behind the heavy oak door."
    "A sound that made the fine hair on my arms stand on end. Not a servant's heavy footfall, nor the polite clatter of tea. It was a gasp—sharp, ragged, and wet, followed by the heavy, rhythmic creak of leather."

    # [CHOICE] Decision point
    menu:
        "The parlour's raw breath, or the desk's quiet ink?"

        "Investigate the parlour door. [[Overhear dismissal: +15 Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(corr=15)
            $ story.set_prologue_found("overheard")

            jump day100_2_parlour_branch

        "Continue with duties at the desk. [[Read letters: +15 Inspiration, +10 Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")

            jump day100_2_desk_branch


label day100_2_parlour_branch:

    "The sound is not a dropped tea-service. It is not the clean, loud clatter of servants."
    "It is a soft, wet murmur. A sudden, sharp gasp that catches in the throat and is held there—desperate, improper, and raw. A sound of raw, unvarnished hunger."

    "I move without thinking, my boots making no sound on the heavy Persian rug. To touch the handle would be a dismissal; to press my ear to the panel is a theft. And I am a very hungry thief."
    "I press my ear to the cold, panelled oak of the parlour door. The heavy timber carries the warmth of the room beyond, vibrating against my cheek as the voices rise."
    "Sir John's voice has lost its parliamentary weight. It is thin, ragged, and pleading—the voice of a creature stripped of its armor and trapped in its own skin."

    "Sir John" "No... George, please. The housemaid is in the study. She has... she has the dusting-license..."
    "George" "The housemaid does not exist, John. She is only furniture that walks. Let the collar be undone—your skin is too hot for wool and starch. Let me feel your chest rise."

    "I hold my breath, pressing my forehead against the dark wood. The heavy panel seems to pulse with their heat."
    "There is a rustle of heavy velvet, the dry, quick slide of hands over broadcloth, and the sharp click of a metal buckle being undone. Then, a low, damp groan from Sir John—a sound of utter, helpless yielding that sends a sudden, electric shock straight down my spine."
    "My thighs press together in the dark corridor, rubbing against the rough linen of my undershift. The wood of the door feels hot against my skin, or perhaps it is my own cheek burning. I can feel the damp warmth blooming between my legs, my own breath coming short and shallow."
    "The words that drift through the keyhole are raw, stripped of the fine grammar Sir John uses when he speaks to the vicar."
    "It is the language of appetite—urgent, heavy, and absolute. They speak of the taste of skin, of the sweat on Sir John's neck, of the desperate, forbidden touch of a master kneeling before a younger man."
    "I feel a strange, cold heat rise in my chest. The world is not made of rules, sermons, and proper curtsies; it is made of secret rooms, private transgression, and men who kneel when the door is shut. And I... I am the one who holds the key to their secrets."

    # [STATE] State/progression update
    jump day100_2_reconvergence


label day100_2_desk_branch:

    "The parlour door remains shut, but the letters on the desk are a louder, far more dangerous invitation."
    "The bureau keys are left in the lock, exposing a wild, frantic ledger of want. I draw my fingers over the smooth, polished mahogany, my heart hammering against my ribs as I pull the top drawer open."
    "The ink is fresh. The handwriting is Sir John's, but it has lost its usual ledger-like precision."
    "The letters are sloped, frantic, crowded together as if the hand that held the pen were shaking with a fever."

    "I reach out, my fingers hovering over the open page. My eyes trace the frantic lines, consuming the forbidden words."

    "Cora (reading)" "'...the taste of your skin in the shadow of the bureau remains my only memory. I have written your name on my palms... to feel your hands undo my collar, to feel the heat of your mouth against the hollow of my throat while the household sleeps... it is a madness, George, a dark, heavy fever that burns through my veins...'"

    "My breath catches, and a flush rises on my neck, spreading down my collarbones under my rough, high-necked collar."
    "The written word has a weight I had not understood—a physical power to evoke illicit desire, a warm, thick pulsing between my thighs as I read the detailed catalog of their secret touches."
    "It can turn a baronet into a beggar; it can make the most improper desires look like liturgy. Sir John writes of their encounters in London, of the Savoy, of a locked box containing their shared, scandalous photographic plates, and of how George's skin feels under the rough slide of broadcloth."
    "In reading them, I steal the ink. A maid who can copy such a hand is no longer just a maid; she is a dangerous cataloguer, holding a key that can pick any lockbox. These letters are not just a scandal; they are a blueprint, an instruction manual for the desires I long to put onto paper."

    # [STATE] State/progression update
    jump day100_2_reconvergence


label day100_2_reconvergence:

    "The world shatters with the click of a latch."
    "I draw back, but Sir John is already in the study."
    "His chest is rising and falling in heavy, ragged gasps. His collar is completely undone, the white linen pulled open to reveal the flushed, damp skin of his throat and the dark hair of his chest. His hair is in disarray, and his eyes are wide and glassy—grey with the terror of a man who knows his secret is no longer his own."
    "He looks at me, his eyes dark with a trembling shame, fear, and a desperate, dangerous anger. He knows I have seen his undone state; he knows the air in the study still carries the scent of their transgression."

    "Sir John" "Cora Vale."
    "cora" "Sir..."
    "Sir John" "You are dismissed. You will leave the estate before nightfall. Take your trunks and go."
    "Sir John" "And if a single word of what you have seen—or read—leaves your mouth, I will see to it that no decent house in England ever takes you in. Your name will be blackened in every registry, and you will find yourself in the gutter, where your quiet eyes belong."

    "The shadow of his threat is the last thing I see in Wiltshire. A cold, sharp shiver of fear and excitement."
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
    "I jolt awake, my forehead striking the soot-chilled glass of the window, skin flushed and damp with perspiration from the memory's intense heat."
    "The train is plunging into a brick tunnel, the carriage rattling violently over the iron tracks in the sudden, suffocating dark."

    "My satchel has slipped from my lap during my sleep, its buckle open."
    "On the floorboards, scattered at my boots, are the sheets I have carried all the way from Wiltshire. The pages are covered in my neat, flowing script—a half-written manuscript of a highly improper nature, detailing the secret lives, the undone collars, and the private, shameful desires of the gentry."
    "And beneath them, the forged reference from Sir John's estate—a perfect lie written in a neat, servant's hand."
    "The gentleman sitting opposite me is slowly lowering his newspaper. In the dim carriage-light, his eyes are fixed on the floor, drifting down toward the scattered, scandalous lines."
    "My heart leaps into my throat. The visible page details a breathless encounter behind a locked door, the words 'undo his trousers' and 'the touch of skin' standing out in bold, fresh ink."

    "I scramble in a panic, my fingers burning as I sweep the sheets away from his gaze, my knuckles scraping the rough floorboards. I block his line of sight with my skirts before he can read another word."
    "If anyone were to examine these sheets... if a conductor were to read even a line of my writing..."
    "I would not merely lose my chance at the Savoy. I would be branded a degenerate, ruined before I ever stepped onto the platform."

    "The gentleman clears his throat, raising his newspaper with a quiet, polite stiffness that only underscores the sudden tension in the compartment."

    cora "I must be mindful. The city will afford no second chances to a chambermaid with such secrets."

    "I gather the papers, tucking my secrets safely back into the dark recess of the satchel and clamping the brass buckle shut. My fingers are still trembling."
    "Outside the soot-stained window, the brick tunnels give way to the sprawling, iron architecture of Waterloo Station."
    "The brooding skyline of London looms through the grey smog, magnificent, indifferent, and ripe with a thousand unseen transgressions."

    "My new position at the Savoy awaits. A grand, glittering world of wealth, propriety, and closed bedroom doors."
    "I bring my broom, my apron, and my forged references."
    "But I bring my inclinations with me. And I will find out exactly what the guests are hiding behind their locked doors."

    # [STATE] State/progression update
    jump day101_main
