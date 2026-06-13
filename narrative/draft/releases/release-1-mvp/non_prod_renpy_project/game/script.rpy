label start:
    show screen stats_overlay

    sys_msg "Holywell Street Studios — MVP Gray-Box v2.0"
    sys_msg "Winter 1891. London."

    jump day100_main

label check_suspicion:
    call watch_suspicion
    return


label suspicion_feedback_minor(character, old, new):
    $ suspicion_focus = character
    $ suspicion_focus_intensity = 1
    show screen suspicion_attention(character)
    pause 0.25
    $ suspicion_focus_intensity = 0
    $ suspicion_focus = None
    hide screen suspicion_attention
    return


label suspicion_breakpoint(character, breakpoint, reason=None, scene_context=None):
    $ tier = suspicion_tier(player.get_total_suspicion(character))
    $ anxiety = anxiety_tier(player.anxiety)
    $ line = get_suspicion_monologue(character, tier, anxiety, reason, scene_context)
    $ suspicion_focus = character
    $ suspicion_focus_intensity = 2
    show screen suspicion_attention(character)
    cora_inner "[line]"
    $ suspicion_focus_intensity = 0
    $ suspicion_focus = None
    hide screen suspicion_attention
    return
