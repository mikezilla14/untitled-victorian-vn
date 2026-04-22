# ═══════════════════════════════════════════════════════════════
#  functions.rpy
#  All Python-side game logic.
#  Keep Ren'Py script files free of inline Python wherever possible.
#  If you need a new mechanic, add a function here and call it
#  from the narrative with a $ prefix.
# ═══════════════════════════════════════════════════════════════

init python:

    def apply_effects(insp=0, corr=0, susp=0):
        """
        Centralized stat mutation helper for day scripts.
        """
        if insp:
            player.gain_inspiration(insp)
        if corr:
            player.gain_corruption_xp(corr)
        if susp > 0:
            player.raise_suspicion(susp)
        elif susp < 0:
            player.lower_suspicion(-susp)

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
