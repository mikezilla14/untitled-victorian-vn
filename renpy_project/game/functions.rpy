# ═══════════════════════════════════════════════════════════════
#  functions.rpy
#  All Python-side game logic.
#  Keep Ren'Py script files free of inline Python wherever possible.
#  If you need a new mechanic, add a function here and call it
#  from the narrative with a $ prefix.
# ═══════════════════════════════════════════════════════════════

init python:

    def apply_effects(insp=0, corr=0, susp=0):
    success = True

    # Inspiration:
    # Positive = gain inspiration.
    # Negative = spend inspiration.
    if insp > 0:
        player_stats.gain_inspiration(insp)
    elif insp < 0:
        success = player_stats.spend_inspiration(abs(insp))

    # Corruption:
    # Positive only. Corruption must never decrease.
    if corr > 0:
        player_stats.gain_corruption_xp(corr)
    elif corr < 0:
        raise ValueError("Corruption cannot be reduced.")

    # Suspicion:
    # Positive = raise suspicion.
    # Negative = lower suspicion.
    if susp > 0:
        player_stats.raise_suspicion(susp)
    elif susp < 0:
        player_stats.lower_suspicion(abs(susp))

    player_stats.update_stats()
    return successs

    def resolve_turn():
        """
        Enforce safe turn ordering: fail-state check before passive decay.
        """
        renpy.call("check_suspicion")
        player.update_stats()

    def set_time_period(period):
        """
        Centralized time-of-day assignment with TimeManager validation.
        """
        time_manager.set_time_of_day(period)

    def attempt_write(required_insp=30, cost=20):
        """
        Shared writing-gate helper.
        """
        if player.inspiration < required_insp:
            return False
        return player.spend_inspiration(cost)
