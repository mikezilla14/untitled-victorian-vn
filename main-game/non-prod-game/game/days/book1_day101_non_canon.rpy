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

# ==========================================================
# AVAILABLE STATE FLAGS AT THE END OF DAY 1:
#
# Story State (story):
# - day1_corridor_state        -> "ghost", "predator", "prey", or "none"
# - day1_interview_state       -> "none", "meek", "competent"
# - day1_stern_relation        -> "none", "complicit", "subservient", "resistant"
# - day1_stern_secret_bound    -> "none", "loyal", "exploitative", "fearful"
# - day1_vance_relation        -> "none", "subservient", "defiant", "ghostly", "protected",
#                                 "intimate", "observed", "loyal_witness", "accomplice", "silent_observer"
# - day1_ledger_focus          -> "none", "inspiration", "corruption"
# - day1_night_action          -> "none", "write", "visit_missy"
# - has_witnessed_voyeur_scene -> True or False
# - has_written_first_chapter   -> True or False
# - missy_day1_seed            -> True or False
# - missy_day1_trust_state     -> "none", "soothed", "unsettled", "warned_cora", "shared_caution"
#
# Player Stats (player):
# - corruption_level           -> integer (e.g. 1, 2, 3...)
# - inspiration                -> integer (0 to 50)
# - anxiety                    -> integer (0 to 100)
# - ghost_focus                -> integer
# - prey_focus                 -> integer
# - predator_focus             -> integer
# ==========================================================

# ==========================================================
# STANDARD (SLOP) DAY 1 SCENE BLOCKS: RAVENSHADE CONSERVATORY
# ==========================================================

# [DAG_NODE id=book1_block_day1_slop_core type=write]
label book1_block_day1_slop_core:
    call book1_nvl_write_line("Draft Fragment - Unsellable Night Pages", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Coralie Vale tries to restage the corridor scandal at Ravenshade Conservatory, but every sentence arrives scrubbed and timid.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Lord Caldor becomes a vague, distant presence; Lady Vayne becomes posture without hunger; Mr. Sterick reads like a wax seal without heat.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Miri's fear is flattened into a polite summary, as if danger can be made respectable by removing all appetite from the telling.", word_delay=_book1_word_delay)

    call book1_block_day1_interview_state
    call book1_block_day1_stern_relation
    call book1_block_day1_vance_relation
    call book1_block_day1_missy_trust_state
    call book1_block_day1_ledger_focus
    return


# [DAG_NODE id=book1_block_day1_default_core type=write]
label book1_block_day1_default_core:
    call book1_block_day1_common_open
    call book1_block_day1_interview_state
    call book1_block_day1_stern_relation
    call book1_block_day1_vance_relation
    call book1_block_day1_missy_trust_state
    call book1_block_day1_ledger_focus
    return


# [DAG_NODE id=book1_block_day1_ghost_core type=write]
label book1_block_day1_ghost_core:
    call book1_block_day1_common_open
    call book1_nvl_write_line("The narration stays observational, dispassionate, and evidentiary; desire is implied through omission, not declaration.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("A ghost is the safest thing to be in a great house, moving through the gaps of their lives, recording each crack in the ceiling.", word_delay=_book1_word_delay)

    call book1_block_day1_interview_state
    call book1_block_day1_stern_relation
    call book1_block_day1_vance_relation
    call book1_block_day1_missy_trust_state
    call book1_block_day1_ledger_focus
    return


# [DAG_NODE id=book1_block_day1_predator_core type=write]
label book1_block_day1_predator_core:
    call book1_block_day1_common_open
    call book1_nvl_write_line("The narration is deliberate and tactical; heat appears as leverage, never as surrender.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Coralie Vale maps the house like a fortress to be besieged, marking the joints of their armor where a needle might slip in.", word_delay=_book1_word_delay)

    call book1_block_day1_interview_state
    call book1_block_day1_stern_relation
    call book1_block_day1_vance_relation
    call book1_block_day1_missy_trust_state
    call book1_block_day1_ledger_focus
    return


# [DAG_NODE id=book1_block_day1_prey_core type=write]
label book1_block_day1_prey_core:
    call book1_block_day1_common_open
    call book1_nvl_write_line("The narration is intimate and exposed; attraction and risk are allowed to coexist without tidy absolution.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Coralie Vale writes with a racing pulse, documenting the sweet terror of being observed, where the hunter's eye is both hazard and fire.", word_delay=_book1_word_delay)

    call book1_block_day1_interview_state
    call book1_block_day1_stern_relation
    call book1_block_day1_vance_relation
    call book1_block_day1_missy_trust_state
    call book1_block_day1_ledger_focus
    return


# [DAG_NODE id=book1_block_day1_common_open type=write]
label book1_block_day1_common_open:
    call book1_nvl_write_line("At Ravenshade Conservatory, Coralie Vale learns that service is theater and every corridor has an audience.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("She studies Lady Vayne's posture, Mr. Sterick's clipped authority, and the predatory stillness of Lord Caldor.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("The scandal behind the music room door becomes her first private map of power.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_ghost_subservient type=write]
label book1_block_day1_ghost_subservient:
    call book1_block_day1_ghost_core
    return


# [DAG_NODE id=book1_block_day1_predator_complicit type=write]
label book1_block_day1_predator_complicit:
    call book1_block_day1_predator_core
    return


# [DAG_NODE id=book1_block_day1_prey_resistant type=write]
label book1_block_day1_prey_resistant:
    call book1_block_day1_prey_core
    return


# ==========================================================
# ALTERNATE (CORRUPTED) DAY 1 SCENE BLOCKS: THE INCITING INCIDENT
# ==========================================================

# [DAG_NODE id=book1_block_day1_alt_default_core type=write]
label book1_block_day1_alt_default_core:
    call book1_nvl_write_line("The air in Alderwood's conservatory was heavy with the suffocating sweetness of damp jasmine, stagnant water, and the musk of rotting soil.", _book1_word_delay)
    call book1_nvl_write_line("My hands were raw, chapped red from the caustic touch of lye. I was nothing but a domestic beast to them, an invisible instrument to scrub away their refuse.", _book1_word_delay)
    call book1_nvl_write_line("But invisible beasts have eyes. And mine were trained on the heavy mahogany doors of the private study, left ajar just a finger's width.", _book1_word_delay)
    call book1_nvl_write_line("Through the gap, the stifling silence of the English countryside was broken by a sound that did not belong in a house of God—the wet, desperate gasp of a woman unravelling.", _book1_word_delay)

    nvl clear

    # [STATE] State/progression update
    $ _book1_page_line_count = 0

    call book1_nvl_write_line("I crept closer, the soles of my boots silent against the slate tiles. A single slip, and I would be thrown to the parish guards.", _book1_word_delay)
    call book1_nvl_write_line("There, in the amber glow of the hearth, was Lady Beatrice. She was pinned against the edge of her husband's oak writing desk, her heavy silk skirts bunched up around her hips like dark, glistening water.", _book1_word_delay)
    call book1_nvl_write_line("Her thighs, gleaming and pale, were spread wide. Stooped between them was the stable groom, his rough hands buried deep inside her, working her with rhythmic, violent intention.", _book1_word_delay)
    call book1_nvl_write_line("She leaned back, her neck arched, biting down on her lace handkerchief to stifle her moans. Her fingers clutched at the leather-bound ledger of her husband's estate, tearing the parchment.", _book1_word_delay)

    nvl clear

    # [STATE] State/progression update
    $ _book1_page_line_count = 0

    call book1_nvl_write_line("A high-born woman, the absolute arbiter of local morality, yielding her flesh to a stablehand's spit and sweat.", _book1_word_delay)
    call book1_nvl_write_line("A sudden warmth hummed beneath my ribs—not of shame, but of a quiet, cold realization. The law was absolute, yes, but only for those who could not pay to hide its fractures.", _book1_word_delay)
    call book1_nvl_write_line("If she were found, her name would be dragged through the mud. She had everything to lose. I had nothing but my breath.", _book1_word_delay)
    call book1_nvl_write_line("I stepped into the light of the doorway, letting the brass handle of my water-pail clink against the plaster wall. Just once. A sharp, metallic note of doom.", _book1_word_delay)

    call book1_block_day1_interview_state
    call book1_block_day1_stern_relation
    call book1_block_day1_vance_relation
    call book1_block_day1_missy_trust_state
    call book1_block_day1_ledger_focus
    return

# [DAG_NODE id=book1_block_day1_alt_predator_core type=write]
# =========================================================================
# METADATA: BOOK ENGINE IMPORT HEADER
# Target File: main-game/non-prod-game/game/days/book1_day101_non_canon.rpy
# Target Label: book1_block_day1_alt_predator_core
# Target Chapter: day1_chapter
# Target Archetype: predator
# Style Lens: Sweeney Todd / Dracula / Carmilla
# Generation Mode: multi_branch_code
# =========================================================================

label book1_block_day1_alt_predator_core:
    # CHAPTER I - THE INCITING LEVER
    # Predator Archetype: Coralie maps the house like a fortress; heat is leverage, never surrender
    
    call book1_nvl_write_line("The conservatory at Alderwood was a mausoleum of green; damp jasmine choked the glass, and the steam from the adjoining wash-house hung in the air like hot tallow-breath. I had seen Lady Beatrice's hand press against the misted pane, her palm leaving a print that told me every sin writ small in the heat of her skin.")
    
    call book1_nvl_write_line("I catalogued the room as I would a battlefield. The mahogany door, ajar a finger's width. The shadow of Lord Caldor's figure beyond the curtain. The wet, rhythmic whisper of Lady Beatrice's scandal, still humming through the corridor like a confession I had not yet been paid to hear.")

    call book1_show_tableau("cg_manuscript_retelling_d1_corridor")
    call book1_show_plate(caption="Plate I — The Service Door")

    call book1_nvl_write_line("A chambermaid is a clockwork thing in the upper houses—an automaton wound by lye-soap and leather heels—but I had learned to watch the gears before I learned to polish the brass. I watched the levers. And I saw, clear as the gas-lamp on her throat, that Lady Vayne was the one who would break first.")
    
    nvl clear
    
    # Missy's trust state - the Carmilla/Dracula hook
    if story.missy_day1_trust_state == "unsettled":
        call book1_nvl_write_line("I nudged Miri ahead of me into the stifling heat of the corridor, her slight body a shield between my own sins and the keyhole. Her face was white as fresh linen, her fingers clutching the hem of her apron as though she expected a bite at any moment. I fed her no comfort; I let the fear settle in her throat like a draught of cold tea.")
        
        call book1_nvl_write_line("She shivered against the rising steam, and I saw her pulse at the hollow of her neck—rabbit-fast, delicate, a thing that could be broken with a word. I did not break it. I held it in my ledger, this debt of trust I was spending before it was even earned. The heat of Lady Vayne's scandal touched both our faces, but Miri felt it as a brand; I felt it as leverage.")
        
        call book1_nvl_write_line("Through the keyhole, Lord Caldor's silhouette moved like a man who counted every soul in his house by the weight of their terror. Miri squeezed her eyes shut, praying. I kept mine open. The butcher does not close his eyes when the blade falls.")
        
        cora_inner "In the Savoy, I had seen Missy's trust curdle in a single afternoon. I wrote it as Miri's fear—thicker than the jasmine, sweeter than the rot. The manuscript demanded blood before it demanded beauty."
        
    else:
        # Default: Miri soothed or shared_caution
        call book1_nvl_write_line("Miri pressed close to my side in the narrow corridor, her hand finding the coarse wool of my sleeve as though I were a sister instead of a stranger. The gas-jet caught the wet shine of her eyes; she had seen something in Lady Beatrice's posture that she could not name. I gave her the name, but I wrapped it in soft, grease-soft lies that would let her sleep.")
        
        call book1_nvl_write_line("'It is only the heat,' I whispered, my voice a low Sussex murmur that held the stench of boiling lye at bay. 'The steam plays tricks. You see shadows where there are only gowns.' She nodded, greedy for the comfort, and I saw her pulse slow. I had soothed the lamb so that I might count her later, when the tally required it.")
        
        call book1_nvl_write_line("But her fingers did not leave my sleeve. The heat of her palm through the worn serge was a small, insistent warmth—a claim I had not foreseen. Lady Vayne's scandal hummed on, wet and rhythmic, but Miri's trust was a thread I could pull. I held it, careful not to snap it, and let her believe I was the wall that kept the wolves from the door.")
        
        cora_inner "I wrote Miri's hand on my sleeve as a bond. In the real hotel, Missy had clutched my arm during the corridor inspection, and I had used her fear as a pass. The page demands I admit I was grateful for the heat of it, even if I could not afford to return it."
    
    nvl clear
    
    # Interview state - the Jekyll & Hyde accent performance
    call book1_nvl_write_line("When Mr. Sterick summoned me to his study, the floorboards groaned like old bone. He sat behind a ledger that bulged with names and dates—his own private history of the house, written in iron gall ink and the dried sweat of every maid who had come before me.")
    
    if story.day1_interview_state == "meek":
        call book1_nvl_write_line("I made my voice soft, a wet cloth draped over the steel of my mind. My Sussex drawl came out like honey poured over broken glass—sweet, opaque, utterly false. I performed the country girl as though I had never seen London's gutters, as though the word 'Ravenshade' meant nothing more than a leaf's shadow. Mr. Sterick's pen scratched against the paper, and I knew he was measuring my compliance in inches.")
        
        call book1_nvl_write_line("'I am simple, sir,' I said, and let the words fall with a country lilt that masked the rattle of chains beneath. 'I know my place. The linens, the lye, the pressing of the gowns. I do not ask questions that are not mine to ask.' He peered at me over his spectacles, and I felt the weight of his assessment like a hand at my throat.")
        
        call book1_nvl_write_line("I had swallowed the draught of meekness, and it tasted like salt and submission. But beneath my tongue, the wild Irish beast stirred, patient as winter. The performance was the potion; I was the poison waiting for the right hour to pour.")
        
        cora_inner "In the Savoy, I had played the fool for Ms. Stern. It bought me three days of invisibility. On the page, I let Coralie do the same—a stitched golem of cotton and lye, dancing for a master who would never see the strings I cut."
        
    elif story.day1_interview_state == "competent":
        call book1_nvl_write_line("I met Mr. Sterick's gaze with a clinical stillness that I had practiced in the mirror of the Savoy's laundry. My Sussex accent was flawless—hard, chalk-white, a plaster cast that hid the raw Irish bone beneath. I did not perform the country girl; I performed the machine, efficient and bloodless, a cog that knew its exact place in the wheel.")
        
        call book1_nvl_write_line("'My credentials are in order, sir,' I said, and my voice did not tremble. 'I know the press of a shirt, the fold of a petticoat, the proper sheen of a polished boot. I require no supervision and will offer no complaint.' Mr. Sterick's pen did not move; he studied me as I had studied the keyhole—searching for the flaw in the armor.")
        
        call book1_nvl_write_line("I gave him none. I was a slaughterman in a maid's costume, my hands chapped from lye and my mind sharpened to a surgeon's edge. The ledger in his study was a mirror of my own—a catalogue of power and its weaknesses. He knew I was dangerous. He did not yet know that I was writing him into the book as the warden of a prison where all the prisoners had learned to count.")
        
        cora_inner "Ms. Stern had respected the efficient mask. I wrote Sterick as a man who saw through it and chose not to speak. The cold understanding between us was the engine that kept the story turning."
    
    nvl clear
    
    # Stern relation - the Sweeney Todd industrial erasure motif
    if story.day1_stern_relation == "subservient":
        call book1_nvl_write_line("I bent my spine to the work of Mr. Sterick's office as though I were a clockwork doll. Each command he issued, each ledger he opened, I met with a soft 'Yes, sir' that cost me nothing but the taste of my own pride. I moved through his study like a golem animated by his iron keys, my heels clicking in obedience to a rhythm I had not written.")
        
        call book1_nvl_write_line("He counted the maids as cattle, and I let him count me. The safety of the butcher's yard was a cold comfort, but it was comfort nonetheless. I would not be slaughtered today; I would be filed, recorded, and filed again. The tally of my sins was lost in the general census of the fallen.")
        
        call book1_nvl_write_line("But the clockwork doll has a heart of tallow. Beneath the grease of my submission, I was melting, reshaping, becoming the thing that would one day shatter the cogs. Mr. Sterick's pen scratched. I did not look at the page. I knew the name it would write when the accounting came.")
        
    elif story.day1_stern_relation == "resistant":
        call book1_nvl_write_line("I bowed my head in Mr. Sterick's study, but my fingers clawed the cheap wood of the chair as though I could draw blood from it. I answered his questions in clipped syllables, each word a small, sharp defiance wrapped in the paper of my performance. He noticed. The butcher always notices when the lamb does not flinch.")
        
        call book1_nvl_write_line("'You have a spirit, girl,' he said, and his voice was the scrape of steel on stone. 'Spirit is tallow for the furnace. It melts as quickly as any other part of you.' I did not answer. I let my silence be the blade I carried, hidden in the hollow of my throat. I would not be counted among the docile cattle.")
        
        call book1_nvl_write_line("I left his study with my back straight and my hands raw. The heat of my defiance was a small, fierce warmth in the cavern of my chest. I had not surrendered. I had simply taken a step back from the edge, biding my time, waiting for the moment when his counting would stop and my reckoning would begin.")
        
    else: # complicit
        call book1_nvl_write_line("In the silence of Mr. Sterick's study, we shared a mutuality that needed no words. Two slaughtermen, each holding the greasy bucket of discretion while the house bled around us. He knew I had seen Lady Beatrice's hand on the pane. He knew I had catalogued the rhythm of her shame. And he knew, as I knew, that some truths were more valuable unsaid.")
        
        call book1_nvl_write_line("The butcher's grease keeps the gears from screeching. I nodded once, a small gesture that sealed the compact between us. He would not count me among the fallen cattle; I would not write his name in the margin of my ledger. We were conspirators in the architecture of survival, two architects of silence, building walls of complicity from the bricks of our mutual hunger.")
        
        call book1_nvl_write_line("I left his office with his blessing and his secret. The heat of Lady Beatrice's scandal still steamed through the corridor, but I walked through it unharmed. I was no longer a cog in his machine; I was the hand that oiled the cogs, and I knew every squeak that would one day bring it crashing down.")
    
    nvl clear
    
    # Closing passage - the predatory framing
    call book1_nvl_write_line("I returned to the shadow of the corridor, where Lady Beatrice's voice still rose in thin, gasping cries. Miri had retreated to the safety of her supplicant's posture, but I stood in the steam with my eyes open, counting the beats of the scandal like a heartbeat I would one day stop.")
    
    call book1_nvl_write_line("Lord Caldor's figure had not moved from the curtain. He was watching me. I felt his gaze like a hand on my spine—measuring, clinical, predatory. I did not flinch. I smiled, the small, tight smile of a chambermaid who knows that every master has a lock, and every lock has a key.")
    
    call book1_nvl_write_line("The conservatory at Alderwood was a mausoleum of green, but I was not the corpse. I was the embalmer, the one who writes the final accounting. And in the margin of my ledger, I wrote: Lord Caldor is not the hunter. He is the game. He does not yet know it, but the page will remember.")
    
    call book1_nvl_write_line("I pressed my palm to the cold stone of the wall and felt the heat of the house through the masonry—the slow, patient burn of power waiting to be stoked. I had not chosen to be predator. I had simply refused to be prey. And in the economy of Alderwood, that was the only choice that mattered.")
    
    return


# [DAG_NODE id=book1_block_day1_alt_ghost_core type=write]
label book1_block_day1_alt_ghost_core:
    # ----- CHAPTER I: THE INCITING LEVER (GHOST ARCHETYPE) -----
    # Macro: Ghost Variant
    # Style Grafting: Jack the Ripper (Ledger/Spying) + Jekyll & Hyde (Voice Mask)
    # Sterick & Servant Labor: Sweeney Todd (Industrial Erasure)

    call book1_nvl_write_line("Chapter I - The Inciting Lever")
    call book1_nvl_write_line("")
    call book1_nvl_write_line("The air in Alderwood's conservatory was thick with the scent of damp jasmine and the cold, metallic tang of stale water. It was not a place for a chambermaid.")
    call book1_nvl_write_line("I had been at Ravenshade for three days, learning the geography of its corridors, the weight of its keys, the particular silence that clung to Lord Caldor's wing of the house.")
    call book1_nvl_write_line("Discretion was the grease on the wheels of this estate. I had learned that lesson by the time the wash-house steam had chapped my hands raw.")
    call book1_nvl_write_line("Through the ajar mahogany door, the rhythm of the house was different. It was wet. A soft, rhythmic sound that was not the pulse of boiler or servant footfall.")
    nvl clear

    call book1_nvl_write_line("I did not press my eye to the keyhole. A ghost does not need to see to know. The shadow moving beneath the door was enough. Lady Beatrice's giggle, low and animal, was enough.")
    call book1_nvl_write_line("The stable groom was with her. The rhythm was his, the soft, choked sounds of her pleasure were her surrender. I cataloged the sounds, the scents, the precise pitch of her abandoned cry.")
    call book1_nvl_write_line("The ledger in my mind opened. It recorded, it dissected, it waited.")
    call book1_nvl_write_line("A ghost records the scene. It does not interfere. It does not hunger. It observes the sin and files it away for later.")
    nvl clear

    # ---- Micro-Variant: Day1 Ledger Focus ----
    if story.day1_ledger_focus == "inspiration":
        call book1_nvl_write_line("I stepped back, my shoes silent on the cold stone. In my mind, I was already transposing the scene. The room became a print shop, the sounds a text.")
        call book1_nvl_write_line("I would not write of Lady Beatrice's wet pleasure. I would write of the pressure of a collar, the weight of a gaze, the slow constriction of a bodice. The heat was a variable.")
        call book1_nvl_write_line("My pen would dissect the scene by inches. It would record the order of the sin, the cost of the silence, the distance between the floor and the servant's quarters.")
        call book1_nvl_write_line("I would write a story of observation, not participation. A ghost's confession.")
    else:
        # story.day1_ledger_focus == "corruption"
        call book1_nvl_write_line("I stepped back, my shoes silent on the cold stone. In my mind, I was already transposing the scene. The ink would be wet. The page would know the smell of sweat.")
        call book1_nvl_write_line("The ledger in my mind recorded not just the act, but the raw hunger. The way Beatrice's breath caught, the way the groom's shirt stuck to his skin, the way her corset strained.")
        call book1_nvl_write_line("My pen would write of want. Spit, sweat, white faces, and the red of a bitten lip. I would sell it for a penny a page, and no one would know the truth of it.")
        call book1_nvl_write_line("The ghost writes the sin in crimson ink. It sells the confession for a penny.")
    nvl clear

    # ---- Micro-Variant: Missy Day1 Trust State ----
    if story.missy_day1_trust_state == "soothed":
        call book1_nvl_write_line("I found Miri in the scullery, her hands trembling over the copper pails. She was young, fresh from the country, her skin pale and her eyes still wide with the shock of the city.")
        call book1_nvl_write_line("She had heard the sounds too. I saw it in the way she clutched the lye-soap, her knuckles white. I placed a hand on her shoulder, soft as grease-soft lies.")
        call book1_nvl_write_line("\"It's only the wind,\" I said, my Sussex drawl flawless. \"The old house settles. It groans.\"")
        call book1_nvl_write_line("She nodded, believing me. She would sleep soundly tonight, unaware of the butcher's count that I was keeping in my head.")
    elif story.missy_day1_trust_state == "unsettled":
        call book1_nvl_write_line("I found Miri in the scullery, her hands trembling over the copper pails. She was young, fresh from the country, and she had heard the sounds too.")
        call book1_nvl_write_line("I saw the fear in her eyes, the same fear that had lived in my own chest when I first arrived. I did not soothe her. I leaned close, my voice low, my breath warm against her ear.")
        call book1_nvl_write_line("\"It was the groom,\" I whispered. \"He has a taste for silk. Lady Beatrice's silk.\"")
        call book1_nvl_write_line("Her trust shattered in that moment. I saw it crack. She looked at me as if I had handed her a snake. I had. I used her as a shield.")
        call book1_nvl_write_line("She shivered in the rising steam, knowing, at last, that she could be boiled for tallow just as easily as the meat.")
    else:
        # story.missy_day1_trust_state == "shared_caution"
        call book1_nvl_write_line("I found Miri in the scullery, her hands trembling over the copper pails. She was young, fresh from the country, but she was not foolish.")
        call book1_nvl_write_line("She looked at me with the same careful gaze I wore. She knew the sounds were not the wind. She was a bird caught in the same snare as I.")
        call book1_nvl_write_line("I did not speak. I simply took the other pail, my hands red from the lye, and began to scrub.")
        call book1_nvl_write_line("We clung to each other's heat in the narrow corridor of that silent understanding. Two ghosts in the same haunted house.")
    nvl clear

    # ---- Micro-Variant: Day1 Stern Relation (Sweeney Todd Graft) ----
    call book1_nvl_write_line("Mr. Sterick's study was a low-ceilinged coffin of a room, smelling of ink, cold tea, and the wax of a thousand tallow candles.")
    call book1_nvl_write_line("He sat behind his ledger, his spectacles low on his nose, his fingers, stained with ink, tapping a slow rhythm on the leather-bound book.")
    call book1_nvl_write_line("He was the overseer. The warden. He counted the cattle for the slaughter, and I was the newest calf in the pen.")

    if story.day1_stern_relation == "subservient":
        call book1_nvl_write_line("He looked up at me, and I bent like clockwork. My voice was soft, my gaze low. I moved by the current of his keys, a golem stitched from linen and lye.")
        call book1_nvl_write_line("I was the perfect maid. The stitched golem. I would not give him cause to send me to the furnace.")
        call book1_nvl_write_line("He nodded, satisfied. He wrote my name in his ledger. I was now a number, a line in his book of debts.")
    elif story.day1_stern_relation == "resistant":
        call book1_nvl_write_line("He looked up at me, and I bowed my head, but my fingers clawed the wood of the doorframe behind me.")
        call book1_nvl_write_line("I was a bird beating against the warm bars of its cage. He was the butcher, and he was counting my fat, but I would not show him my throat.")
        call book1_nvl_write_line("\"Miss Vale,\" he said, his voice flat. \"The boilers are low. See to the laundry before first light.\"")
        call book1_nvl_write_line("I held his gaze for a fraction of a second too long. Then I turned and walked away, a lamb who knew the butcher's arithmetic.")
    else:
        # story.day1_stern_relation == "complicit"
        call book1_nvl_write_line("He looked up at me, and I met his gaze with a silence of two slaughtermen. He knew that discretion was the grease that kept the gears from screeching.")
        call book1_nvl_write_line("\"Miss Vale,\" he said, his voice low. \"There is a stain on the master's floor. See to it.\"")
        call book1_nvl_write_line("\"Yes, Mr. Sterick,\" I said, my voice flat, clinical.")
        call book1_nvl_write_line("We shared the understanding of the butcher's yard. He bled their names dry, and I held the bucket.")
    nvl clear

    # ---- Micro-Variant: Day1 Vance Relation (Carmilla Graft) ----
    call book1_nvl_write_line("The corridor was dark, lit only by the amber glow of a distant hearth. The footsteps were soft, hesitant.")
    call book1_nvl_write_line("Lady Vayne was walking the hall. I heard her before I saw her, her breath quick, her silk rustling against the stone floor.")
    call book1_nvl_write_line("She was a creature of his making, a trapped bird in a gilded cage. I could see the red marks of his grip on her collarbone.")

    if story.day1_vance_relation == "protected":
        call book1_nvl_write_line("She stopped when she saw me. Her eyes were wide, her lip trembling.")
        call book1_nvl_write_line("I stepped forward, not as a servant, but as a wall. I whispered, \"You have forgotten the words, my lady.\"")
        call book1_nvl_write_line("I brushed my fingers against her neck, softly, a comfort. I was building a wall around her fear to keep the other butchers out.")
        call book1_nvl_write_line("She leaned into my touch. For a moment, she was not a lady. She was just a woman, trembling in the cold.")
    elif story.day1_vance_relation == "intimate":
        call book1_nvl_write_line("She stopped when she saw me. Her eyes were glazed with a dark and heavy heat. She was not frightened. She was aching.")
        call book1_nvl_write_line("I pressed my thumb to the red mark on her collarbone, the pressure point of his grip.")
        call book1_nvl_write_line("She gasped, her chest arching against my rough hand in a slow, intoxicating surrender.")
        call book1_nvl_write_line("Unlacing her corset would have been a slow bite. I would have fed on her pride, but I did not. I was a ghost.")
    elif story.day1_vance_relation == "observed":
        call book1_nvl_write_line("She stopped when she saw me. Her eyes were red from weeping. She was a carcass on the block, and I was the butcher's apprentice.")
        call book1_nvl_write_line("I unpinned her lace with clinical, icy distance, treating her distress like a cadaver to be dissected.")
        call book1_nvl_write_line("She flinched, but she did not resist. She was a specimen, an entry in my ledger.")
        call book1_nvl_write_line("\"The hem is torn,\" I observed. \"I shall mend it.\"")
    else:
        # story.day1_vance_relation == "accomplice" or "loyal_witness"
        call book1_nvl_write_line("She stopped when she saw me. Her eyes were dark, calculating.")
        call book1_nvl_write_line("I stepped closer, my voice a low murmur in the damp dark. \"I saw nothing, my lady. But I could see everything.\"")
        call book1_nvl_write_line("She realized then that we shared the same animal appetite. She was not afraid of me. She was afraid of her own reflection in my eyes.")
        call book1_nvl_write_line("We sealed our collusion in that moment, two conspirators in the shadow of the lord.")
    nvl clear

    # ---- Day1 Interview State (Jekyll & Hyde Graft) ----
    if story.day1_interview_state == "meek":
        call book1_nvl_write_line("In the interview, I performed the drawl. It was a coat of grease over a meat-axe, a protective draught to hide the Irish beast beneath my apron.")
        call book1_nvl_write_line("I was meek, soft, and simple. The perfect country mouse, oblivious to the cats in the halls.")
        call book1_nvl_write_line("He believed me. Lord Caldor's gaze slid over me like water over stone. I was beneath his notice.")
        call book1_nvl_write_line("That was the point. The beast was chained. The mask was fixed.")
    else:
        # story.day1_interview_state == "competent"
        call book1_nvl_write_line("In the interview, I performed the drawl. It was flawless, clinical, a hard mask of chalk and starch, hiding the hands that knew the weight of the knife.")
        call book1_nvl_write_line("I was competent, efficient, a walking ledger of service.")
        call book1_nvl_write_line("Lord Caldor looked at me for one breath longer than he should have. I felt his gaze on my throat, cataloging me, the way I cataloged Beatrice.")
        call book1_nvl_write_line("I did not flinch. The mask held. The beast was still chained, but it was looking out through the eyes.")
    nvl clear

    # ---- Chapter Conclusion (Ghost Archetype) ----
    call book1_nvl_write_line("The day was done. I had seen, I had listened, I had recorded.")
    call book1_nvl_write_line("The real hotel was a place of silence and fear. But the page demanded a bolder blood.")
    call book1_nvl_write_line("I returned to my quarters, the ink-stained paper cold beneath my fingers. The ghost had written its first confession.")
    call book1_nvl_write_line("The machine was oiled with our silence. And I was the one holding the grease.")
    nvl clear

    # ---- Optional: Night Action (Frantic Write vs. Visit Missy) ----
    # This is handled by a separate flag, but we keep the default prose focused on the ghostly observation.
    call book1_nvl_write_line("The scratch of my pen against the cheap paper was the only sound.")
    call book1_nvl_write_line("I wrote of Alderwood, of the steam, of the scent of damp jasmine.")
    call book1_nvl_write_line("I wrote of the shadows, and the secrets they held.")
    call book1_nvl_write_line("And I wrote of the ghost who watched it all, too afraid to act, but too hungry to look away.")
    nvl clear


# [DAG_NODE id=book1_block_day1_alt_prey_core type=write]
label book1_block_day1_alt_prey_core:
    # --- PROLOGUE: CONSERVATORY STEAM ---
    call book1_nvl_write_line("The air in Alderwood's conservatory was choked with the suffocating steam of the wash-house.")
    call book1_nvl_write_line("It smelled of hot tallow, stagnant water, and the faint, cloying sweetness of damp jasmine.")
    call book1_nvl_write_line("My hands were raw, chapped red from the caustic touch of lye.")
    call book1_nvl_write_line("I was nothing but a domestic beast to them, a cog in the machine that ground down servants' lives for tallow.")
    nvl clear
    
    call book1_nvl_write_line("But the machine has eyes.")
    call book1_nvl_write_line("Through the mahogany door, ajar just a finger's width, the silence was broken by the wet, rhythmic sounds of Lady Beatrice's slow slaughter.")
    call book1_nvl_write_line("I should have fled. Every instinct screamed for the corridor, for the safety of the scullery.")
    call book1_nvl_write_line("Yet my feet remained planted. My pulse hammered against my ribs.")
    nvl clear
    
    # --- MISSY TRUST STATE BRANCHING ---
    if story.missy_day1_trust_state == "soothed":
        call book1_nvl_write_line("Miri's small hand found mine in the dark. I squeezed it once, a soft, grease-soft lie of comfort.")
        call book1_nvl_write_line("\"Easy, now,\" I breathed. \"We are but shadows.\"")
        call book1_nvl_write_line("She believed me. Her trust was a warm weight in my palm, a burden I had no right to carry.")
        call book1_nvl_write_line("But I was not thinking of Miri. I was thinking of the face behind that door.")
        nvl clear
    elif story.missy_day1_trust_state == "unsettled":
        call book1_nvl_write_line("I nudged Miri ahead of me into the choking steam, her soft form blocking the keyhole.")
        call book1_nvl_write_line("She was my shield, her country decency the perfect screen to absorb whatever wrath lay behind the mahogany paneling.")
        call book1_nvl_write_line("Her breath hitched. I felt the tremor run through her thin shoulders.")
        call book1_nvl_write_line("\"Don't,\" she whispered. \"Don't make me see.\"")
        call book1_nvl_write_line("But I was already seeing. And I would not look away.")
        nvl clear
    else: # shared_caution
        call book1_nvl_write_line("Miri pressed against my back in the narrow corridor, her heat seeping through my thin cotton apron.")
        call book1_nvl_write_line("We were two birds caught in the same snare, clinging to each other in the rising steam.")
        call book1_nvl_write_line("\"We should go,\" she breathed. Her voice was a thread of panic.")
        call book1_nvl_write_line("I nodded, but my eyes remained fixed on the crack of light.")
        call book1_nvl_write_line("The sound from within—a low, guttural groan—rooted me to the spot.")
        nvl clear
    
    # --- THE CONSERVATORY SCENE (Lady Beatrice & the Groom) ---
    call book1_nvl_write_line("Lady Beatrice's eyes, glazed with a dark and heavy heat, locked onto the crack in the door.")
    call book1_nvl_write_line("The stable groom did not cease his rhythm. He only grinned, drawing her closer to the edge, matching the girl's terror as if inviting her to the hooks.")
    call book1_nvl_write_line("Her throat arched back. A pearl of sweat traced the hollow of her collarbone.")
    call book1_nvl_write_line("It was not fear I saw on her face. It was hunger. A raw, shameless appetite that mirrored my own.")
    nvl clear
    
    # --- DAY1_INTERVIEW_STATE BRANCHING ---
    if story.day1_interview_state == "meek":
        call book1_nvl_write_line("The memory of that interview with Mr. Sterick surfaced like a draught of cold tea.")
        call book1_nvl_write_line("I had performed my soft, compliant drawl—a coat of grease over a meat-axe.")
        call book1_nvl_write_line("\"Yes, sir. No, sir. I know my place, sir.\"")
        call book1_nvl_write_line("The words tasted like ash. But they were the keys to the cage, and I turned them willingly.")
        nvl clear
        
        call book1_nvl_write_line("At his desk, Mr. Sterick had peered at my credentials. His eyes were flat, clinical.")
        call book1_nvl_write_line("I curtsied low. The heavy starch of my apron scraped against my chin.")
        call book1_nvl_write_line("\"You have references,\" he said. It was not a question.")
        call book1_nvl_write_line("I nodded, letting my voice go soft and small. \"Yes, sir. From the Wiltshire estate.\"")
        call book1_nvl_write_line("The lie was a smooth pebble in my mouth, worn down by years of practice.")
        nvl clear
    else: # competent
        call book1_nvl_write_line("The memory of that interview with Mr. Sterick surfaced like a cold shard of glass.")
        call book1_nvl_write_line("I had matched his gaze, my Sussex drawl flawless and clinical. A mask of chalk and starch.")
        call book1_nvl_write_line("\"Coralie Vale, sir. Previous service at the Wiltshire estate. I am thorough.\"")
        call book1_nvl_write_line("The words were precise. Surgical. I was offering him a tool, not a servant.")
        nvl clear
        
        call book1_nvl_write_line("Mr. Sterick's pen scratched against the ledger. He did not look up.")
        call book1_nvl_write_line("\"You are precise,\" he observed. The word hung in the air like a test.")
        call book1_nvl_write_line("I did not flinch. \"Precision is the servant's only shield, sir.\"")
        call book1_nvl_write_line("For a moment—a single, electric moment—his pen stilled.")
        nvl clear
    
    # --- DAY1_STERN_RELATION BRANCHING ---
    if story.day1_stern_relation == "subservient":
        call book1_nvl_write_line("In Mr. Sterick's study, I bent like clockwork. A stitched golem of linen and lye.")
        call book1_nvl_write_line("His keys jangled at his hip as he moved. I followed the sound like a hound.")
        call book1_nvl_write_line("\"You will keep to the corridors. You will not speak to the guests. You will not look up.\"")
        call book1_nvl_write_line("I nodded. The motion was mechanical. Easier to be a puppet than to feel the strings.")
        nvl clear
    elif story.day1_stern_relation == "resistant":
        call book1_nvl_write_line("In Mr. Sterick's study, I bowed my head—but my fingers clawed the wood of his desk.")
        call book1_nvl_write_line("He noticed. His eyes flicked down to my knuckles, white with strain.")
        call book1_nvl_write_line("\"Is there something you wish to say, girl?\"")
        call book1_nvl_write_line("I shook my head. But my silence was louder than any confession.")
        call book1_nvl_write_line("I was a bird beating against warm bars, knowing the butcher was counting my fat.")
        nvl clear
    else: # complicit
        call book1_nvl_write_line("In Mr. Sterick's study, we shared the silence of two slaughtermen.")
        call book1_nvl_write_line("He did not threaten me. He did not need to. His eyes said what his mouth would not.")
        call book1_nvl_write_line("\"You understand, Miss Vale, that discretion is the butcher's grease.\"")
        call book1_nvl_write_line("I met his gaze. \"It keeps the gears from screeching, sir.\"")
        call book1_nvl_write_line("A ghost of approval flickered across his features. I had passed a test I did not know I was taking.")
        nvl clear
    
    # --- DAY1_VANCE_RELATION BRANCHING ---
    if story.day1_vance_relation == "protected":
        call book1_nvl_write_line("Later, in the dressing room, Lady Vayne's neck was bare. A column of vulnerable flesh.")
        call book1_nvl_write_line("I unpinned her hair with trembling hands. The scent of jasmine clung to her skin.")
        call book1_nvl_write_line("\"You are gentle,\" she murmured. Her voice was thick with unshed tears.")
        call book1_nvl_write_line("I said nothing. I was building a wall around her fear, brick by careful brick, to keep the other butchers out.")
        call book1_nvl_write_line("It was a kindness I could not afford. But I gave it anyway.")
        nvl clear
    elif story.day1_vance_relation == "intimate":
        call book1_nvl_write_line("In the dressing room, my thumb found the red pressure mark Lord Caldor's grip had left on Lady Vayne's collarbone.")
        call book1_nvl_write_line("She gasped. Her chest arched against my rough hand in a slow, intoxicating surrender.")
        call book1_nvl_write_line("The heat of her skin. The damp unlacing of her corset. The soft, yielding give of her stays.")
        call book1_nvl_write_line("She was a high-born beast yielding to the butcher's touch, begging for the collar that commanded her.")
        call book1_nvl_write_line("And I—I was the one holding the leash.")
        nvl clear
    elif story.day1_vance_relation == "observed":
        call book1_nvl_write_line("I unpinned Lady Vayne's dress with clinical distance. Each motion was deliberate. Dispassionate.")
        call book1_nvl_write_line("She wept softly into her handkerchief. I cataloged the tears. The tremor in her hands. The shame that painted her cheeks.")
        call book1_nvl_write_line("I treated her distress like a carcass on the block, dissecting it with cold precision.")
        call book1_nvl_write_line("It was not cruelty. It was survival. I could not afford to feel for her.")
        call book1_nvl_write_line("She was not my charge. She was my evidence.")
        nvl clear
    else: # accomplice
        call book1_nvl_write_line("In the damp dark of the corridor, Lady Vayne's breath came in ragged gasps.")
        call book1_nvl_write_line("\"You cannot tell anyone,\" she hissed. Her fingers closed around my wrist like a trap.")
        call book1_nvl_write_line("I leaned in. The scent of her fear was thick and warm.")
        call book1_nvl_write_line("\"Secrets are currency,\" I whispered. \"And I am very, very poor.\"")
        call book1_nvl_write_line("She understood. In that moment, she realized we shared the same animal appetite. The same hunger for survival.")
        call book1_nvl_write_line("Collusion sealed in the steam. I was no longer just a servant. I was her keeper.")
        nvl clear
    
    # --- LEDGER FOCUS BRANCHING ---
    if story.day1_ledger_focus == "inspiration":
        call book1_nvl_write_line("Later, in the narrow confines of my attic room, I opened my manuscript.")
        call book1_nvl_write_line("The pen dissected the scene with careful precision. Order. Cost. Distance.")
        call book1_nvl_write_line("I was a naturalist cataloging a specimen, not a sinner recording a sin.")
        call book1_nvl_write_line("\"Lady Beatrice spent exactly three sovereigns on the stable groom,\" I wrote. \"She paid in gold and in flesh.\"")
        call book1_nvl_write_line("The facts were clean. The judgment was implied.")
        nvl clear
    else: # corruption
        call book1_nvl_write_line("Later, in the narrow confines of my attic room, I opened my manuscript.")
        call book1_nvl_write_line("My pen wrote want. It wrote Beatrice's spit and sweat. It wrote Miri's white face and my own hunger outside the door.")
        call book1_nvl_write_line("I scratched the words onto the cheap gray paper like a confession. Like a prayer.")
        call book1_nvl_write_line("\"She arched. She gasped. She surrendered to the groom's rough hands,\" I wrote.")
        call book1_nvl_write_line("The ink bled. The words throbbed. I was recording the raw hunger of the house, beautifully, to sell for a penny more.")
        nvl clear
    
    # --- THE FINAL TRANSITION: CLOSING THE CHAPTER ---
    call book1_nvl_write_line("The candle burned low. My wrist ached. The manuscript pulsed with borrowed life.")
    call book1_nvl_write_line("I had grafted my terror onto the page. I had taken the heat of the conservatory and boiled it down to ink.")
    call book1_nvl_write_line("But the true horror was not what I had written.")
    call book1_nvl_write_line("It was what I had not.")
    nvl clear
    
    cora_inner "In the real hotel, I lacked the claws. I was just a girl with a forged accent and a stolen ledger. But the page demands a bolder blood."
    cora_inner "So I sharpened my nib. And I wrote myself into a monster."
    nvl clear
    
    # --- EPILOGUE HOOK FOR NEXT DAY ---
    if story.missy_day1_trust_state == "unsettled":
        call book1_nvl_write_line("Beyond my door, Miri's footsteps hesitated. Then they fled.")
        call book1_nvl_write_line("She would not look at me in the morning. She would not speak. The debt had been written into her skin.")
    else:
        call book1_nvl_write_line("Beyond my door, the house groaned. The furnace rumbled. The machine breathed.")
        call book1_nvl_write_line("I was just one cog. But my pen had teeth.")
    nvl clear
    
    call book1_nvl_write_line("I blew out the candle. The darkness was complete.")
    call book1_nvl_write_line("And in the dark, Lord Caldor's voice seemed to echo from the walls:")
    call book1_nvl_write_line("\"You cannot hide from what you hunger for.\"")
    nvl clear
    
    return


# [DAG_NODE id=book1_block_day1_alt_ghost_subservient type=write]
label book1_block_day1_alt_ghost_subservient:
    call book1_block_day1_alt_ghost_core
    return


# [DAG_NODE id=book1_block_day1_alt_predator_complicit type=write]
label book1_block_day1_alt_predator_complicit:
    call book1_block_day1_alt_predator_core
    return


# [DAG_NODE id=book1_block_day1_alt_prey_resistant type=write]
label book1_block_day1_alt_prey_resistant:
    call book1_block_day1_alt_prey_core
    return


# [DAG_NODE id=book1_block_day1_slop_chapter type=write]
label book1_block_day1_slop_chapter:
    call book1_nvl_write_line("Chapter I (Alternate) - Slop and Ash", word_delay=_book1_word_delay)
    call book1_nvl_write_line("The mundane routine of Alderwood was a slow, gray death...", word_delay=_book1_word_delay)
    return


# ==========================================================
# MINOR STATE HOOKS: LABELS GENERATING DETAIL VARIANTS
# ==========================================================

# [DAG_NODE id=book1_block_day1_interview_state type=write]
label book1_block_day1_interview_state:
    if player.corruption_level <= 2:
        # Slop version
        if story.day1_interview_state == "meek":
            call book1_nvl_write_line("Coralie Vale stood before the housekeeper with folded hands, her answers soft and compliant, the very image of a girl who knows her place.", _book1_word_delay)
        elif story.day1_interview_state == "competent":
            call book1_nvl_write_line("Coralie Vale answered the housekeeper's queries with calm, efficient precision, showing herself well-fitted for the Savoy's strict discipline.", _book1_word_delay)
    else:
        # Corrupted Alt version (Sweeney Todd / Carmilla transpositions)
        if story.day1_corridor_state == "predator":
            if story.day1_interview_state == "meek":
                call book1_nvl_write_line("In the study, Mr. Sterick peered at my Sussex credentials. I made my voice soft, performing the meek Sussex drawl like a coat of grease over a meat-axe. The accent was an act, a clean apron worn by the monster hiding in plain sight, ensuring the butcher of this play remained unseen in their parlor.", _book1_word_delay)
            elif story.day1_interview_state == "competent":
                call book1_nvl_write_line("In the study, I matched Mr. Sterick's gaze, my Sussex drawl flawless and clinical. It was the perfect mask of chalk and starch, hiding the hands that knew the weight of the knife. I was the butcher hiding in plain sight, playing the humble servant while sizing up his neck for the hook.", _book1_word_delay)
        elif story.day1_corridor_state == "prey":
            if story.day1_interview_state == "meek":
                call book1_nvl_write_line("In the study, Mr. Sterick peered at my Wiltshire credentials. I made my voice soft, performing the meek drawl like a yielding wool. The accent was a submissive wrap, letting him believe he held the leash, while the pulse in my throat hammered with the sweet terror of his authority.", _book1_word_delay)
            elif story.day1_interview_state == "competent":
                call book1_nvl_write_line("In the study, I matched Mr. Sterick's gaze, my drawl flawless and clinical. It was a mask of Sussex chalk, polished and cold, yet my fingers trembled against my apron. I played the competent servant, but inside, I was yielding to the heavy weight of his command, finding a strange heat in the threat of his inspection.", _book1_word_delay)
        else:
            if story.day1_interview_state == "meek":
                call book1_nvl_write_line("In the study, Mr. Sterick peered at my Sussex credentials. I made my voice soft, performing the meek Sussex drawl like a protective draught to hide the wild Irish beast beneath my cuffs.", _book1_word_delay)
            elif story.day1_interview_state == "competent":
                call book1_nvl_write_line("In the study, I matched Mr. Sterick's gaze with flawless, clinical Sussex drawl. The accent was a mask of Sussex chalk, polished and hard, hiding the ink-stained hands that longed to rip down their curtains.", _book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_stern_relation type=write]
label book1_block_day1_stern_relation:
    if player.corruption_level <= 2:
        # Slop version
        if story.day1_stern_relation == "subservient":
            call book1_nvl_write_line("She bowed to Mr. Sterick's command, accepting the housekeeper's authority as the iron rule of the kitchen.", _book1_word_delay)
        elif story.day1_stern_relation == "resistant":
            call book1_nvl_write_line("Though she kept her distance, Coralie felt the weight of Mr. Sterick's watchful eye following her every shift.", _book1_word_delay)
        elif story.day1_stern_relation == "complicit":
            call book1_nvl_write_line("Mr. Sterick and Coralie shared a quiet understanding, two wheels in the great clockwork machine of service.", _book1_word_delay)
    else:
        # Corrupted Alt version (Sweeney Todd / Dracula bone-grinding/submission transpositions)
        if story.day1_corridor_state == "predator":
            if story.day1_stern_relation == "subservient":
                call book1_nvl_write_line("I bowed to Mr. Sterick's command, my limbs moving like clockwork. Under his cold eye, we are but sheep in the pens of Alderwood, our days spent polishing the very bones he plans to boil for grease, moving only by the current of his keys.", _book1_word_delay)
            elif story.day1_stern_relation == "resistant":
                call book1_nvl_write_line("Mr. Sterick's eyes followed me like a warden counting the cattle before the slaughter. I felt the lash in his voice, and though my head was bowed, my fingers clawed the wood. Even a lamb knows when the butcher is counting its fat.", _book1_word_delay)
            elif story.day1_stern_relation == "complicit":
                call book1_nvl_write_line("We shared the silence of two slaughtermen. Mr. Sterick knew that discretion was the butcher's grease keeping the hotel's gears from screeching, and I was the one who would hold the bucket while he bled their names dry.", _book1_word_delay)
        elif story.day1_corridor_state == "prey":
            if story.day1_stern_relation == "subservient":
                call book1_nvl_write_line("I yielded to Mr. Sterick's command, my limbs moving in a silent, clockwork dance. We are but sleepwalkers in his hall, our knees bending to his key-rattle, finding a sweet, hypnotic peace in letting him rule our every breath.", _book1_word_delay)
            elif story.day1_stern_relation == "resistant":
                call book1_nvl_write_line("Mr. Sterick's eyes followed me like a warden tracing a prisoner. I felt the lash in his voice, and though I bowed, my heart raced. I wanted to escape his gaze, yet the terror of his attention held me fast, an intoxicating fire that bound me to the spot.", _book1_word_delay)
            elif story.day1_stern_relation == "complicit":
                call book1_nvl_write_line("We shared the silence of the master and the beast. Mr. Sterick knew my secrets, and his knowledge was a warm, heavy weight upon my neck—a silent, invisible collar I wore with a quiet, trembling pleasure.", _book1_word_delay)
        else:
            if story.day1_stern_relation == "subservient":
                call book1_nvl_write_line("I yielded to Mr. Sterick's gaze, my limbs moving like clockwork. We are but galvanized golems in this house, stitched from old linen and lye-soap, animated only by the current of the master's keys.", _book1_word_delay)
            elif story.day1_stern_relation == "resistant":
                call book1_nvl_write_line("Mr. Sterick's eyes followed me like a warden counting the cattle. I felt the lash in his voice, and though I bowed, my fingers clawed the wood, seeking a joint in his iron armor.", _book1_word_delay)
            elif story.day1_stern_relation == "complicit":
                call book1_nvl_write_line("We shared the silence of two conspirators. Mr. Sterick knew that discretion was the butcher's grease keeping the hotel's gears from screeching, and I was the grease he required.", _book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_vance_relation type=write]
label book1_block_day1_vance_relation:
    if player.corruption_level <= 2:
        # Slop version
        if story.day1_vance_relation in ["protected", "intimate"]:
            call book1_nvl_write_line("In the dressing room, Coralie assisted Lady Vayne with her laces, their proximity marked by a quiet, polite confidence.", _book1_word_delay)
        elif story.day1_vance_relation in ["observed", "silent_observer"]:
            call book1_nvl_write_line("Coralie performed her duties with cold, respectful distance, stepping back the moment the laces were untied.", _book1_word_delay)
        else:
            call book1_nvl_write_line("Lady Vayne's petulance filled the boudoir, and Coralie bore the lady's anger without reply.", _book1_word_delay)
    else:
        # Corrupted Alt version (Carmilla / Dracula / Adults-Only Dark Romance transposition)
        if story.day1_corridor_state == "predator":
            if story.day1_vance_relation == "protected":
                call book1_nvl_write_line("In the dressing room, my fingers brushed Lady Vayne's warm, trembling neck as I loosened the silver pins. 'I have already forgotten his words, My Lady,' I whispered, building a dark wall around her fear—not to save her, but to ensure no other butcher could slice into her first.", _book1_word_delay)
            elif story.day1_vance_relation == "intimate":
                call book1_nvl_write_line("In the dressing room, my thumb pressed the red pressure mark Lord Caldor's grip had left on her collarbone. She gasped, her chest arching against my rough hand in a slow, intoxicating surrender. The heat of her skin, the damp unlacing of her corset—she was a high-born beast yielding to the butcher's touch, begging for the collar that commands her.", _book1_word_delay)
            elif story.day1_vance_relation == "observed":
                call book1_nvl_write_line("I unpinned the lace with clinical, icy distance, my eyes dissecting her posture. I did not curtsy. I treated her distress like a carcass on the table, counting the joints of her pride where my scalpel would slide in.", _book1_word_delay)
            elif story.day1_vance_relation == "loyal_witness":
                call book1_nvl_write_line("In the stairwell, she pressed me against the brick, her heaving chest against mine, her perfume of jasmine and fear filling my throat. I let her believe she had bought my silence, when I had only marked her for the next day's work.", _book1_word_delay)
            elif story.day1_vance_relation == "accomplice":
                call book1_nvl_write_line("I leaned close, my lips brushing her ear in the damp dark. 'I know what it is to want a hand that commands you,' I whispered, my thumb tracing her pulse. She let out a sharp, wet moan, sealing our collusion in the brick shadow as she realized we shared the same animal appetite.", _book1_word_delay)
            elif story.day1_vance_relation == "silent_observer":
                call book1_nvl_write_line("I pushed past her in the shadow. I wanted the shape of her fear, not her touch. A writer needs only the carcass to carve, not the beast itself; I left her to rot in her own panic while I prepared the page.", _book1_word_delay)
            else:
                call book1_nvl_write_line("Lady Vayne cornered me, her red hair falling like coils of copper. She threatened me with Mr. Sterick's inspection, her anger a hot, erratic thing. She did not see the mask I wore, nor did she know that her rage was only the fat I would boil down for my next chapter.", _book1_word_delay)
        elif story.day1_corridor_state == "prey":
            if story.day1_vance_relation == "protected":
                call book1_nvl_write_line("In the dressing room, my fingers brushed Lady Vayne's warm, trembling neck as I loosened the silver pins. 'I have already forgotten his words, My Lady,' I whispered, building a dark, protective wall around her fear, wanting only to share the sweet terror of her locked boudoir.", _book1_word_delay)
            elif story.day1_vance_relation == "intimate":
                call book1_nvl_write_line("In the dressing room, my thumb pressed the red pressure mark Lord Caldor's grip had left on her collarbone. She gasped, her chest heaving against my hand in a slow, intoxicating surrender. We breathed together, a feast of velvet and fear where command and submission shared a single, fevered line.", _book1_word_delay)
            elif story.day1_vance_relation == "observed":
                call book1_nvl_write_line("I unpinned the lace with clinical, icy distance. I did not curtsy. I stood exposed under her critical gaze, letting her trace the raw red chaps on my hands, finding a quiet, shrugging thrill in my own vulnerability.", _book1_word_delay)
            elif story.day1_vance_relation == "loyal_witness":
                call book1_nvl_write_line("In the stairwell, she pressed me against the brick, her heaving chest against mine, her perfume of jasmine and fear filling my mouth, binding me to her by the sweet, dark cord of her vulnerability.", _book1_word_delay)
            elif story.day1_vance_relation == "accomplice":
                call book1_nvl_write_line("I leaned close, my lips brushing her ear in the damp dark. 'I know what it is to want a hand that commands you,' I whispered, my thumb tracing her pulse. She let out a sharp, wet moan, sealing our collusion in the brick shadow as she realized we shared the same animal appetite.", _book1_word_delay)
            elif story.day1_vance_relation == "silent_observer":
                call book1_nvl_write_line("I pushed past her in the shadow, my own pulse hammering. I did not touch her; I wanted the shape of her fear to mirror my own, a silent echo of vulnerability in the dark.", _book1_word_delay)
            else:
                call book1_nvl_write_line("Lady Vayne cornered me, her red hair falling like coils of copper. She threatened me with Mr. Sterick's inspection, her anger a hot, erratic thing against my cold posture. I stood trembling under her wrath, finding a strange, feverish excitement in the threat of her command.", _book1_word_delay)
        else:
            if story.day1_vance_relation == "protected":
                call book1_nvl_write_line("In the dressing room, my fingers brushed Lady Vayne's warm, trembling neck as I loosened the silver pins. 'I have already forgotten his words, My Lady,' I whispered, building a dark, protective wall around her fear.", _book1_word_delay)
            elif story.day1_vance_relation == "intimate":
                call book1_nvl_write_line("In the dressing room, my thumb pressed the red pressure mark Lord Caldor's grip had left on her collarbone. She gasped, her chest arching against my rough hand in a slow, intoxicating feast of submission and command.", _book1_word_delay)
            elif story.day1_vance_relation == "observed":
                call book1_nvl_write_line("I unpinned the lace with clinical, icy distance. I did not curtsy. I treated her distress like an entry in a ledger, dissecting her vulnerability with a cold, scalpel-like gaze.", _book1_word_delay)
            elif story.day1_vance_relation == "loyal_witness":
                call book1_nvl_write_line("In the stairwell, she pressed me against the brick, her heaving chest against mine, her perfume of jasmine and fear filled my throat.", _book1_word_delay)
            elif story.day1_vance_relation == "accomplice":
                call book1_nvl_write_line("I leaned close, my lips brushing her ear in the cold dark. 'I know what it is to want a hand that commands you,' I whispered, sealing our collusion in the brick shadow as she let out a sharp, wet moan.", _book1_word_delay)
            elif story.day1_vance_relation == "silent_observer":
                call book1_nvl_write_line("I pushed past her in the shadow. I wanted the shape of her fear, not her touch. A writer needs only the dissection of the beast, not the beast itself.", _book1_word_delay)
            else:
                call book1_nvl_write_line("Lady Vayne cornered me, her red hair falling like coils of copper. She threatened me with Mr. Sterick's inspection, her anger a hot, erratic thing against my cold Brighton posture.", _book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_missy_trust_state type=write]
label book1_block_day1_missy_trust_state:
    if player.corruption_level <= 2:
        # Slop version
        if story.missy_day1_trust_state == "soothed":
            call book1_nvl_write_line("Miri was reassured by Coralie's sensible advice, and they walked on with quick, quiet steps.", _book1_word_delay)
        elif story.missy_day1_trust_state == "unsettled":
            call book1_nvl_write_line("Miri remained uneasy, her mind troubled by the whispers behind the guest door.", _book1_word_delay)
        elif story.missy_day1_trust_state == "shared_caution":
            call book1_nvl_write_line("Miri and Coralie shared a quiet caution, keeping their eyes on the laundry bins.", _book1_word_delay)
    else:
        # Corrupted Alt version (Sweeney Todd / Dracula transpositions)
        if story.day1_corridor_state == "predator":
            if story.missy_day1_trust_state == "soothed":
                call book1_nvl_write_line("I pacified Miri with grease-soft lies. She believes the blood on my apron is only beet-juice from the pantry, sleeping soundly in the servants' attic while the butcher counts the sovereigns under her mattress.", _book1_word_delay)
            elif story.missy_day1_trust_state == "unsettled":
                call book1_nvl_write_line("Miri's eyes are hollowed out, her trust in the house shattered. I have fed her to the gears of Alderwood, and though she works beside me, she shivers whenever the steam rises, knowing I would boil her bones for tallow if the price were right.", _book1_word_delay)
            elif story.missy_day1_trust_state == "shared_caution":
                call book1_nvl_write_line("Miri's hand caught my sleeve, dragging me back before they could catch us. We stood close, our pulses hammering in the narrow corridor. We are two hogs in the pen, bound by the shared secret of the slaughter, clinging to each other's heat before the hook comes.", _book1_word_delay)
        elif story.day1_corridor_state == "prey":
            if story.missy_day1_trust_state == "soothed":
                call book1_nvl_write_line("I pacified Miri with soft, soothing lies. She believes the corridor was only a shadow, but the memory stays between us like a secret fever, her eyes following my hands as if she wants to be led back to the dark.", _book1_word_delay)
            elif story.missy_day1_trust_state == "unsettled":
                call book1_nvl_write_line("Miri looks at me with white, haunted eyes. She knows I dragged her to the edge of the pit, and though she shrinks from me in fear, the terror has a dark, compulsive heat that draws her back to my shadow.", _book1_word_delay)
            elif story.missy_day1_trust_state == "shared_caution":
                call book1_nvl_write_line("Miri's hand caught my sleeve, dragging me back before they could catch us. We stood in the narrow corridor, our pulses hammering. We are two birds caught in the same snare, finding a sweet, desperate warmth in our shared danger.", _book1_word_delay)
        else:
            if story.missy_day1_trust_state == "soothed":
                call book1_nvl_write_line("I took Miri by the wrist, dragging her away from the keyhole. 'Maids only get crushed in the door,' I warned, soothing her panic with cold logic until her country armor locked back down.", _book1_word_delay)
            elif story.missy_day1_trust_state == "unsettled":
                call book1_nvl_write_line("I used Miri's decency as a shield, pushing her toward the latch to see Lord Caldor's shoe pinning Lady Vayne's hand. Miri's face turned white with the terror of what she saw, her trust in the house shattered.", _book1_word_delay)
            elif story.missy_day1_trust_state == "shared_caution":
                call book1_nvl_write_line("Miri's hand caught my sleeve, dragging me back before Lord Caldor could catch us. We stood close, our pulses hammering in the narrow corridor, bound together by the shared secret of our prying.", _book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_ledger_focus type=write]
label book1_block_day1_ledger_focus:
    if player.corruption_level <= 2:
        # Slop version
        if story.day1_ledger_focus == "inspiration":
            call book1_nvl_write_line("Coralie Vale drew three columns in the ledger: command, witness, and consequence, finding comfort in order.", _book1_word_delay)
        elif story.day1_ledger_focus == "corruption":
            call book1_nvl_write_line("The ledger was filled with the details of the day, a precise record of Ravenshade's internal economy.", _book1_word_delay)
    else:
        # Corrupted Alt version (Sweeney Todd / Dracula transpositions)
        if story.day1_corridor_state == "predator":
            if story.day1_ledger_focus == "inspiration":
                call book1_nvl_write_line("By candlelight, my pen dissected the scene, recording the clean structure of command and surrender. The ledger is my chopping block, and each name I write is a cut of meat to be weighed and priced for the stalls.", _book1_word_delay)
            elif story.day1_ledger_focus == "corruption":
                call book1_nvl_write_line("I did not write order. My pen wrote want—Beatrice's spit and sweat, Miri's white face, my own hunger outside the door. The ledger is a butcher's book, filled with the grease and blood of our sins, recorded beautifully so they might sell for a penny more.", _book1_word_delay)
        elif story.day1_corridor_state == "prey":
            if story.day1_ledger_focus == "inspiration":
                call book1_nvl_write_line("By candlelight, my pen recorded the scene, but my hand was shaking. The ledger is not a shield; it is a confession. Each name I write is a mark upon my own skin, a silent, trembling yield to their power.", _book1_word_delay)
            elif story.day1_ledger_focus == "corruption":
                call book1_nvl_write_line("I did not write order. My pen wrote want—Beatrice's surrender, Miri's breath, my own racing pulse. The ledger is a record of my own submission, written beautifully so the world can see how easily the flesh yields.", _book1_word_delay)
        else:
            if story.day1_ledger_focus == "inspiration":
                call book1_nvl_write_line("By candlelight, my pen dissected the scene, recording the clean structure of command and surrender. The shape of the wound is what matters to a writer, not the blood itself.", _book1_word_delay)
            elif story.day1_ledger_focus == "corruption":
                call book1_nvl_write_line("I did not write order. My pen wrote want—Beatrice's spit and sweat, Miri's white face, my own hunger outside the door. The ledger does not forgive; it merely records our sins beautifully.", _book1_word_delay)
    return
