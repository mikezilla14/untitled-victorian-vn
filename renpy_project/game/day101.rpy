# ═══════════════════════════════════════════════════════════════
#  day101.rpy — ARRIVAL AND FIRST MATERIAL
#  Converted from day101_non_canon.md into canonical framework usage.
# ═══════════════════════════════════════════════════════════════

label day1_morning:
    $ time_manager.set_current_day(1)
    $ set_time_period("Morning")
    $ day1_corridor_choice = "ghost"

    scene bg_savoy_corridor_morning
    with fade

    sys "─── DAY 1: MORNING ───"

    "The Savoy Hotel. A gilded cage of mahogany and brass."
    "I stand outside the Head of Housekeeping's office. My forged references burn a hole in my apron pocket."

    show stern_sprite neutral at center
    stern "You say you have experience in the countryside. The Savoy is not the countryside, Cora. We demand absolute invisibility."

    menu:
        "How do I present myself?"

        "Play the meek, terrified country girl.":
            $ apply_effects(susp=10)
            cora "I only wish to work hard and keep my head down, ma'am."
            stern "See that you do."
            "Her gaze softens a fraction. She thinks I am stupid. Good."

        "Show competence and sharp intelligence.":
            $ apply_effects(susp=20)
            cora "I am meticulous, ma'am. You will find no fault in my execution."
            stern "Confidence is a dangerous thing in a maid, girl. Mind your station."
            "She doesn't like me. But she believes I can do the job."

    hide stern_sprite

    "Stern dismisses me. As I step out into the plush corridor, I nearly collide with a guest."
    show vance_sprite angry at left
    vance "Watch your step, you clumsy little idiot!"
    "She is dripping in velvet and pearls. Her eyes are furious, looking for someone to punish."

    show gideon_sprite cold at right
    "Then the door to the master suite opens behind her. A man steps out. The air in the hallway immediately drops ten degrees."
    gideon "Vance. Leave the girl. You are making a scene."
    "The transformation is instantaneous. The venom drains from Vance's face."
    show vance_sprite submissive at left
    "She shrinks, taking a physical step behind his shoulder. A hound brought to heel."
    gideon "Apologies for the noise. See to your duties, maid."
    cora "Yes, sir."

    hide vance_sprite
    hide gideon_sprite

    "I keep my eyes down as they walk away. But my mind is racing. The way he looked at her... the way she yielded."
    jump day1_afternoon


label day1_afternoon:
    $ set_time_period("Afternoon")

    scene bg_laundry_room_day
    with dissolve

    sys "─── DAY 1: AFTERNOON ───"

    "The laundry room is a suffocating cloud of lye and steam."
    show missy_sprite smiling at center
    missy "You're the new girl! Cora, right? I'm Missy. Isn't this place just grand?"
    "Missy is bright-eyed, rural, and tragically innocent. She is exactly what I am pretending to be."
    cora "It's certainly big."

    scene bg_servants_corridor_dim
    with fade

    "As we pass the janitorial access to the master suite, a sound bleeds through the thin plaster."
    "A sharp slap. A gasp. Vance's voice, trembling."
    vance "I'm sorry, sir. I won't speak out of turn again."

    show missy_sprite shocked at left
    missy "Oh my... are they fighting? Should we fetch Ms. Stern?"
    "Missy doesn't understand. But I do. The tone isn't violence. It's discipline."

    menu:
        "How do I secure the material?"

        "Send Missy to check while I stay back. (+Inspiration)":
            $ apply_effects(insp=10)
            cora "They might need fresh towels, Missy. You should peek through the keyhole. Just to be sure."
            missy "Me? Oh... I don't know..."
            "Her curiosity wins. She creeps to the door while I remain in the shadows."
            "If the door opens, she takes the risk. I memorize every detail I can gather."
            $ day1_corridor_choice = "predator"

        "Take the physical risk myself. (+Corruption, +Suspicion)":
            $ apply_effects(corr=5, susp=25, insp=10)
            cora "Quiet. Stay here."
            "I creep to the crack in the door."
            "I see Vance on her knees, Gideon's hand gripping her jaw. My breath catches. The floorboard groans beneath my shoe."
            "Gideon's head snaps toward the door. I scramble backward, my heart hammering in my throat."
            $ day1_corridor_choice = "prey"
            $ story.set_has_witnessed_voyeur_scene(True)

        "Pull Missy away and rely on what I heard. (+Inspiration)":
            $ apply_effects(insp=10)
            cora "It's none of our business. Keep walking."
            "I grab Missy's arm and pull her down the hall before she can make a sound."
            "I catalogue the wet sound of the slap, the exact pitch of Vance's gasp. Pure observation."
            $ day1_corridor_choice = "ghost"

    hide missy_sprite
    jump day1_evening


label day1_evening:
    $ set_time_period("Evening")

    scene bg_servants_quarters_dusk
    with fade

    sys "─── DAY 1: EVENING ───"

    "I lock the door to my cramped room. I have one hour before lights out."

    menu:
        "How do I spend the hour?"

        "Atonement: mend uniforms. (-Suspicion)":
            $ apply_effects(susp=-20)
            "I spend the hour painstakingly darning the fraying hem of my apron. Stern may read it as diligence."

        "Gossip: talk to Missy. (+Corruption, -Suspicion)":
            $ apply_effects(corr=5, susp=-10)
            "I visit Missy's cot. We whisper about the wealthy guests. I nudge her innocence toward darker curiosities."

        "Indulge: review my illicit notes. (+Inspiration, +Suspicion)":
            $ apply_effects(insp=10, susp=15)
            "I pace the room, replaying Gideon's voice in my head. Distracted, I knock over my washbasin."
            "Stern yells through the wall to keep quiet."

    jump day1_night


label day1_night:
    $ set_time_period("Night")

    scene bg_cora_desk_night
    with dissolve

    sys "─── DAY 1: NIGHT ───"

    cora "The hotel is asleep. It's time to write."
    cora "I keep thinking about the handbill I found at the market stall last week: Holywell Street. Discretion assured. Generous terms."
    cora "I think about the seven shillings I send home, and what one paid chapter might change."

    if attempt_write(required_insp=15, cost=0):
        "The ink flows easily tonight. The corridor scene has given me material."

        if day1_corridor_choice == "predator":
            "I write of a cunning maid who manipulates the desires of her betters."
        elif day1_corridor_choice == "prey":
            "I write of a maid caught spying, then pulled into punishment she never meant to witness."
        else:
            "I write with clinical precision about the private depravity of the wealthy."

        $ story.set_has_written_first_chapter(True)
        "Chapter One is complete. I let the candle gutter low."
    else:
        "I stare at the blank page. The terror of this place clouds every sentence."
        "No chapter tonight."

    jump day1_late_night


label day1_late_night:
    $ set_time_period("Late Night")

    sys "─── DAY 1: LATE NIGHT ───"
    cora "I blow out the candle and lie awake, already planning tomorrow."

    $ resolve_turn()
    jump day2_morning
