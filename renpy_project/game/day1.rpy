# ═══════════════════════════════════════════════════════════════
#  day1.rpy — THE ARRIVAL
#  Day 1 is a pure tutorial: no real choices, no stat gates.
#  Its job is to establish stakes (dismissal = destitution)
#  and plant the Holywell Street hook.
# ═══════════════════════════════════════════════════════════════

label day1_morning:
    $ time_manager.current_day  = 1
    $ time_manager.time_of_day  = "Morning"

    sys "─── DAY 1: MORNING ───"

    stern "Cora. You will attend to the third-floor VIP suite. Sir Gideon Locke is our only guest of consequence this week."
    stern "Your position here reflects on me. One complaint from the guests and you will leave this hotel without a character. Do I make myself understood?"
    cora  "Yes, ma'am."
    stern "Then get to work."

    cora "Miss Stern's words hung in the air like a threat — because they were one. Without a character reference, I'd never work in service again. No position, no wages, no money home."
    cora "I cleaned Sir Gideon's suite while he was out. Dusted the books, beat the rugs, polished the brass. The room smelled of tobacco and something expensive I couldn't name."
    cora "I found nothing scandalous. Just the ordinary luxury of a man who has never scrubbed a floor in his life."

    sys "[[TUTORIAL: No real choices today. The player learns the stakes: dismissal = destitution. Miss Stern holds Cora's future in her hands.]"

    jump day1_night


label day1_night:
    $ time_manager.time_of_day = "Night"

    sys "─── DAY 1: NIGHT ───"

    cora "My room is small. A narrow bed, a washstand, and a writing desk wedged beneath the window. The electric lights don't reach the servant's quarters — just a candle and the sound of London outside."
    cora "I keep thinking about the handbill I found at the market stall last week. Crumpled between cabbages and old newsprint."

    sys "[[FLASHBACK]"

    cora "'WRITERS WANTED. Discretion Assured. Generous Terms for Suitable Material. Enquire at No. 14, Holywell Street.'"
    cora "Holywell Street. Even I know what that means. The whole of London knows. It's where they sell the books you can't find in any respectable shop."
    cora "I've been writing stories since the vicar let me loose in his library back in the village. Penny dreadfuls, adventure tales, nonsense mostly. But I can write. I know I can."
    cora "The question is whether I can write... that."

    sys "[[END FLASHBACK]"

    cora "I think about the seven shillings I send home. I think about what a publisher on Holywell Street might pay for a single chapter."
    cora "I stare at the blank page."

    jump day1_late_night


label day1_late_night:
    $ time_manager.time_of_day = "Late Night"

    sys "─── DAY 1: LATE NIGHT ───"

    cora "I dip the nib in the ink. I write a sentence. I cross it out. I write another."
    cora "It's no use."
    cora "I have nothing to say. My life has been the schoolroom, the village, and this hotel. What do I know of scandal? What do I know of passion?"
    cora "My writing is as plain and scrubbed as my uniform."

    sys "[[WRITING DESK: LOCKED. Inspiration ([player.inspiration]) is below 30. The player sees the gate.]"

    cora "I blow out the candle."

    $ player.update_stats()
    jump day2_morning
