Here is the complete rewrite of `day100.rpy`. 

This revision shifts the tone to an Adults Only dark romance, exploring the suffocating social structures of Victorian England, class hypocrisy, and the gendered double standard of ruin. Here, Cora uses linguistic camouflage to suppress her Irish heritage, mimicking the flat vowels of Wiltshire to extract a life-changing blackmail payment and elite London reference from her compromised mistress, Lady Eleanor.

This encounter installs a dangerous, false belief in Cora: that secrets are equal-opportunity currency. This sets up her future downfall when she attempts to blackmail a Lord, only to discover that while a Victorian woman's reputation is her life, a Victorian man's power is absolute and untouchable by servant-class accusations.

***

<details>
<summary><strong>1. Architectural & Narrative Design Changes</strong></summary>

### Key Narrative Shifts
* **The Victim of Leverage:** Sir John is replaced by **Lady Eleanor**. The focus shifts to the intense vulnerability of a wealthy woman's reputation. If Lady Eleanor is exposed, she faces social death, loss of her children, and total exile; if a Lord is exposed later in the story, society looks the other way. This makes Eleanor's desperation visceral.
* **The Impropriety (AO Themes):** The witnessed scene/letters are re-imagined with a dark, carnal, and transgressive edge. Whether Cora overhears Lady Eleanor's frantic, submissive tryst with the stablemaster George or reads letters detailing her raw, forbidden appetites, the atmosphere is thick with sweat, leather, and Victorian repression.
* **The Irish Erasure:** Cora’s dialogue highlights her intense linguistic monitoring. In her head, her thoughts run in her natural Cork lilt; aloud, she forces her tongue into a sterile, round-mouthed English country-girl dialect. One slip of her tongue means her instant destruction as an "Irish street-grub."
* **The Forged Future:** Cora explicitly demands two things: five gold sovereigns (travel money) and a signed, sealed personal reference to the housekeeper of the Savoy Hotel in London, setting up her fake identity.

</details>

<details>
<summary><strong>2. Structural Variable Mapping</strong></summary>

To maintain full compatibility with your existing Ren'Py systems, the variable outcomes remain mapped to your backend architecture.

| Context Variable | Value | Narrative Impact |
| :--- | :--- | :--- |
| `story.prologue_found` | `"read_letters"` | Cora discovers Lady Eleanor’s dark letters to the stablemaster. |
| `story.prologue_found` | `"overheard"` | Cora witnesses Lady Eleanor in a raw, compromised position in the parlour. |
| `story.set_prologue_holywell_posture` | `"careful"` / `"eager"` / `"desperate"` | Directs Cora's negotiation strategy with Lady Eleanor (Shrewd, Bold, or Deferential-mask). |
| `story.set_run_archetype_seed` | `"ghost"` / `"prey"` / `"predator"` | Seeds her survival mechanism for navigating the predatory streets of London. |

</details>

***

## The Rewritten Ren'Py Script

Below is the complete, production-ready code designed to replace the contents of your `day100.txt` / `day100.rpy` file.

```renpy
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

# ==========================================
# NODE MAP
# ==========================================
# day100_main (Night) — Nighttime crawl in the suffocating Wiltshire mansion
# day100_1_afternoon_boredom — Choosing where to search (Bureau vs. Parlour)
# day100_2_evening_flashback — Routing bridge
# day100_2_parlour_branch / day100_2_desk_branch → day100_2_reconvergence
# day100_3_night_daydream — High-tension train reflection to Waterloo
# day100_3_arrival — High stakes arrival at Waterloo Station


# ==========================================
# MAIN ENTRY — WILTSHIRE HOUSE AT NIGHT
# ==========================================

# [DAG_NODE id=day100_main type=work day=100]
label day100_main:

    # [STATE] State/progression update
    $ set_time_period("Night")

    scene bg_country_estate_corridor_night
    with fade

    # [BEAT] The quiet, heavy terror of the domestic sphere. Cora moves through the dark holding her breath.
    
    "The manor at night is not a home; it is a velvet-lined coffin."
    "I walk with my boots clutched to my ribs, the coarse wool of my stockings catching on the splinters of the backstair boards."

    cora_inner "Quiet now. Quiet as a grave. The Wiltshire damp is in my bones, but my chest is blazing."
    cora_inner "My manuscript pages—my dirty, beautiful secrets—were taken from my trunk while I was scrubbing the grates."
    cora_inner "In this house, my thoughts are a disease. A maid who feels, who observes, who writes down the rotten truth of her betters... she is a monster."
    cora_inner "If the Master has seen those pages, I am simple garbage to be thrown to the ditch. If the Lady has them, she will have me stripped and searched."
    cora_inner "I must retrieve them. Before the dawn light unmasks me."

    "A grandfather clock tolls three. The sound vibrates through the floorboards like a low, warning growl."

    cora_inner "I am terrified. My heart beats in my fingers. But I will not leave this house empty-handed."

    # [STATE] State/progression update
    jump day100_1_afternoon_boredom_setup


# Compat stub to keep labels consistent
label day100_1_afternoon_boredom_setup:

    # [STATE] State/progression update
    jump day100_1_afternoon_boredom


# [DAG_NODE id=day100_1_afternoon_boredom type=work day=100]
label day100_1_afternoon_boredom:

    # [ASSET] Visual/staging command
    scene bg_country_estate_study
    with dissolve

    # [BEAT] Cora enters the private sanctuary of the ruling class.
    
    cora_inner "The Lady's private sanctuary. The door stands open by a mere finger’s width."
    cora_inner "It smells of costly amber, lavender-water, and the wet coal-smog leaking from the hearth."
    cora_inner "My pages are here. I can smell the ink. She seized them because she recognized the hunger in them."
    cora_inner "Where would Eleanor Wiltshire hide the evidence of a common servant’s transgressive imagination?"

    # [CHOICE] Search location determines prologue_found flag
    # [DAG_CHOICE group=day100_1_afternoon_boredom_menu_1]
    menu:
        "Where does she keep her stolen secrets?"

        "Look within the walnut bureau. [[Search the bureau: $+15$ Inspiration, $+10$ Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(insp=15, corr=10)
            $ story.set_prologue_found("read_letters")
            
            cora_inner "The walnut bureau. Where she locks away the letters that make her hands tremble."

            # [STATE] State/progression update
            jump day100_2_evening_flashback

        "Peer toward the private parlour settee. [[Search the parlour entrance: $+15$ Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(corr=15)
            $ story.set_prologue_found("overheard")

            cora_inner "The small parlour. I heard a muffled gasp from behind the heavy velvet drapes."

            # [STATE] State/progression update
            jump day100_2_evening_flashback


# Compat bridge for routing
# [DAG_NODE id=day100_2_evening_flashback type=work day=100]
label day100_2_evening_flashback:
    if story.prologue_found == "read_letters":

        # [STATE] State/progression update
        jump day100_2_desk_branch
    else:

        # [STATE] State/progression update
        jump day100_2_parlour_branch


# [DAG_NODE id=day100_2_parlour_branch type=work day=100]
label day100_2_parlour_branch:

    # [BEAT] Erotic/Tension: Cora overhears and witnesses Lady Eleanor's compromised, submissive tryst.
    
    "I press my forehead to the cool paneling of the inner door, my eye aligned with the keyhole's narrow slit."
    "The air coming through is hot, smelling of damp skin and stable sawdust."
    "Lady Eleanor is on her knees. Her silk dinner dress, worth more than three years of my wages, is piled around her waist like discarded skin."
    "George, the rugged stableman, stands over her. His rough hand is buried in her perfectly pinned hair, pulling her head back until her white throat strains."

    "Lady Eleanor" "Ah... George... please. Not so hard... if my husband returns..."
    "George" "Your husband is in London, Eleanor. And you're just another bitch in the straw when the lights are low."

    "The sound of saliva, of a harsh, breathless sob from the Lady of the house. She does not slap him. She clings to his corduroy thighs, her mouth opening in desperate, filthy submission."
    "My groin tightens. The absolute hypocrisy of it. This is the woman who lectures the village girls on modesty and chastity."

    cora_inner "So, the saint of Wiltshire kneels in the dark for a stable-hand's sweat."
    cora_inner "I feel the blood hum between my legs—not out of shame, but out of a sudden, blinding realization of power."
    
    # [STATE] State/progression update
    jump day100_2_reconvergence


# [DAG_NODE id=day100_2_desk_branch type=work day=100]
label day100_2_desk_branch:

    # [BEAT] Erotic/Mystery: Cora searches the desk and finds Lady Eleanor's incredibly detailed, scandalous letters.
    
    "My hands are deft, sliding through the drawers like a thief in the night."
    "Deep beneath Lady Eleanor's charity ledgers, wrapped in soiled ribbon, I find a packet of letters written in her fine, elegant sloped hand."

    "Cora (reading)" "'...when you held me in the carriage house, with the smell of horse-sweat and clover... I have never felt such low, delicious agony. To have my hands bound by your leather crop... to be forced to kneel...'"
    "Cora (reading)" "'...if my husband should suspect, I am ruined. But my body is no longer mine. It belongs to your boots, George...'"

    cora_inner "Ink is a confession. She preaches the Lord's temperance to us, while drowning herself in a stable-man's dirt."
    cora_inner "The words burn my fingertips. A heat blossoms between my thighs—raw, ink-wet, and heavy with opportunity."
    cora_inner "This is her throat. And my hand is on the knife."

    # [STATE] State/progression update
    jump day100_2_reconvergence


# [DAG_NODE id=day100_2_reconvergence type=work day=100]
label day100_2_reconvergence:

    # [BEAT] The discovery. Lady Eleanor catches Cora, but the power dynamic instantly shifts as Cora uses the secrets to blackmail her.
    
    "A sharp rustle behind me. The door swings wide."
    "Lady Eleanor stands there. Her hair is slightly wild, her collar crooked, her eyes wide with a manic terror."
    "She has my stolen manuscript pages clutched in her hand. But her face is white as flour. She knows what I have seen."

    "Lady Eleanor" "You... you Irish guttersnipe."
    "Lady Eleanor" "You dare search my rooms? You dare write this... this filth about flesh and touch? You are a cancer in this house."

    cora_inner "Careful. My head screams in my mother's soft, looping lilt. Swallow it. Choke it down."
    cora_inner "I must speak with the tongue of an English country maid. Flat. Clean. Sterile. I cannot let her hear the Cork in my throat."

    # [CHOICE] How to confront Lady Eleanor using the blackmail
    # [DAG_CHOICE group=day100_1_afternoon_boredom_menu_2]
    menu:
        "How do I leverage her ruin?"

        "Shrewdly demand terms. [[Careful stance: $+5$ Inspiration]]":

            # [STATE] State/progression update
            $ story.set_prologue_holywell_posture("careful")

            cora "I only seek my pages, my Lady. And perhaps... a peaceful transition to London."
            
            cora_inner "Let her hear a simple girl who knows too much. Let her think she is buying my simple silence."
            cora_inner "A quiet, English tongue is the deadliest trap."

        "Boldly state the price of her reputation. [[Bold stance: $+5$ Inspiration, $+5$ Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(insp=5, corr=5)
            $ story.set_prologue_holywell_posture("eager")

            cora "London is expensive, my Lady. And the papers of Wiltshire love a tale of a Lady kneeling in the straw."

            cora_inner "I do not cower. I see the sweat on her skin. I want her to know she is paying her master today."
            cora_inner "I will have my ticket out of this tomb."

        "Feign deferential self-preservation. [[Submissive stance: $+10$ Corruption]]":

            # [STATE] State/progression update
            $ apply_effects(corr=10)
            $ story.set_prologue_holywell_posture("desperate")

            cora "Please, my Lady. I will say nothing of what I saw... or the letters to George. I only ask for the means to go."

            cora_inner "I bend my knee. Let her believe she has frightened me. The victim's mask is the safest shield."
            cora_inner "She will pay me to run away."

    "Lady Eleanor gasps, stumbling back against the desk. The threat of social execution hangs in the cold air."
    "For a woman in her position, a single whisper in Wiltshire—or worse, a letter delivered to her husband's club in London—would strip her of her name, her children, and her humanity."

    "Lady Eleanor" "You... you devil. You wretched, unnatural creature."

    cora "I require five sovereigns for the train, my Lady. And a signed, sealed character reference for the housekeeper at the Savoy Hotel in London."
    cora "A reference that speaks of my... absolute innocence and flawless moral character."

    "Lady Eleanor's hand shakes so violently she can barely dip the quill in ink."
    "She scribbles the letter of reference, sealing it with her private wax. Then, she flings a velvet purse of gold onto the floorboards."

    "Lady Eleanor" "Take it. Take it and die in the London smog, Vale. If I ever see your face in this county again, I will have the constables drop you in a hole."

    "I pick up the gold. The weight of it is sweet, heavy, and real."

    cora_inner "She thinks she has banished me. But she has funded my birth."
    cora_inner "I have learned the golden rule of England: secrets are the only currency that never devalues."
    cora_inner "This is how I win. I will make them all kneel."

    # [STATE] State/progression update
    $ renpy.block_rollback()

    jump day100_3_night_daydream


# ==========================================
# TRAIN TRANSITION — WATERLOO & DAYDREAM
# ==========================================

# [DAG_NODE id=day100_3_night_daydream type=work day=100]
label day100_3_night_daydream:

    # [STATE] State/progression update
    $ set_time_period("Night")

    scene bg_train_carriage_day
    with dissolve

    "The train screeches over the iron track, hurtling away from Wiltshire and into the dark throat of London."
    "The soot settles on the small window-pane, and the第三 class carriage smells of wet wool and cheap gin."

    cora_inner "I touch my bodice. The letters of reference are there, flat against my skin. The five gold sovereigns are hard against my thigh."
    cora_inner "No more clearing grates. No more Wiltshire frost."
    cora_inner "I am Cora Hartley. An English girl from the country, they will think. A quiet, diligent, invisible maid."
    cora_inner "They will never know the Irish blood in my veins, or the hunger in my ink."

    # [CHOICE] Archetype seed choice
    menu:
        "How will I conquer London?"

        "By becoming an invisible ghost, gathering their filth in the dark. [[Ghost Focus: $+1$ Ghost]]":

            # [STATE] State/progression update
            $ story.set_run_archetype_seed("ghost")
            $ apply_archetype_edge("ghost", 1)
            cora_inner "I will be the draft in the corridor. The maid who pours the tea and sees the black souls of the elite."
            cora_inner "A ghost is never suspected. A ghost can never be hanged."

        "By learning their blows before they strike, surviving behind their masks. [[Prey Focus: $+1$ Prey]]":

            # [STATE] State/progression update
            $ story.set_run_archetype_seed("prey")
            $ apply_archetype_edge("prey", 1)
            cora_inner "I will learn their rules better than they know them. I will bend, mimic, and redirect their violence."
            cora_inner "When they think they have trapped me, I will already be behind them."

        "By baiting their desires, turning their hidden shame into my material. [[Predator Focus: $+1$ Predator]]":

            # [STATE] State/progression update
            $ story.set_run_archetype_seed("predator")
            $ apply_archetype_edge("predator", 1)
            cora_inner "They think they are the masters of this world. But I have seen their hunger. I will entice it, record it, and sell it back to them."
            cora_inner "Let them hunt. I am the one who will write their epitaphs."

    # [BEAT] Daydream: Erotic/sensual AO reflection on the impropriety she witnessed.

    cora_inner "The rhythmic clanking of the wheels sounds like the harsh, rhythmic breathing of George in the parlour."

    if story.prologue_found == "overheard":
        cora_inner "I close my eyes and see Lady Eleanor's pale thighs shivering in the dark."
        cora_inner "Her mouth opened in sinful, absolute surrender, her fine silk dress dragged through the hearth soot."
        cora_inner "The stark, beautiful contrast of power stripped bare."
    else:
        cora_inner "I close my eyes and see the ink on Lady Eleanor's scandalous letters."
        cora_inner "The words of submission, the leather crop, the deliberate giving over of her body to a servant's pleasure."
        cora_inner "Desire is the only force stronger than their precious, stifling class."

    cora_inner "I will write it all. I will put a pseudonym to my name, and sell these pages to the dirty publishers of Holywell Street."
    cora_inner "They want filth? I will write them the truest, darkest appetites of England."

    # [STATE] State/progression update
    jump day100_3_arrival


# [DAG_NODE id=day100_3_arrival type=work day=100]
label day100_3_arrival:

    "The train whistle screams—a dirty, metallic roar that tears the smog apart."
    "We shudder to a halt under the towering iron vault of Waterloo Station."
    "The soot is thick, a dark snow falling over the frantic, pushing crowds of London."

    "An elderly gentleman in the carriage opposite lowers his Times, peering at me with mild curiosity."

    cora "Apologies, sir. The soot has quite caught my throat."

    cora_inner "Perfect. Clear. Flat. The accent of an English country parson's daughter."
    "He offers a curt nod, returning to his paper. The lie works. It always works."

    "I step off the train and pull my thin shawl tight against the freezing, beautiful, rotten air of the capital."

    cora_inner "The Savoy waits for its new maid. The city waits for its new monster."
    cora_inner "Let us see who breaks first."

    # [STATE] Handoff to Day 101 Morning
    $ time_manager.set_current_day(1)
    $ set_time_period("Morning")

    jump day101_main
```