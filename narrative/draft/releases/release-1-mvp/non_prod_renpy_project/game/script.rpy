label start:
    show screen stats_overlay

    sys_msg "Holywell Street Studios — MVP Gray-Box v2.0"
    sys_msg "Winter 1891. London."

    jump day100_main

label check_suspicion:
    if player.anxiety >= 100:
        jump game_over_dismissed
    return