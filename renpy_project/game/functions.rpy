# ═══════════════════════════════════════════════════════════════
#  functions.rpy
#  All Python-side game logic.
#  Keep Ren'Py script files free of inline Python wherever possible.
#  If you need a new mechanic, add a function here and call it
#  from the narrative with a $ prefix.
# ═══════════════════════════════════════════════════════════════

init python:

    def apply_effects(insp=0, corr=0, susp=0, stern_susp=0, vance_susp=0, missy_susp=0):
        success = True

        # Inspiration:
        # Positive = gain inspiration.
        # Negative = spend inspiration.
        if insp > 0:
            player.gain_inspiration(insp)
        elif insp < 0:
            success = player.spend_inspiration(abs(insp))

        # Corruption:
        # Positive only. Corruption must never decrease.
        if corr > 0:
            player.gain_corruption_xp(corr)
        elif corr < 0:
            raise ValueError("Corruption cannot be reduced.")

        # Legacy susp != 0 mapping to stern_susp:
        if susp != 0:
            stern_susp += susp

        # Character-specific suspicions:
        if stern_susp != 0:
            player.adjust_character_suspicion("stern", stern_susp)
        if vance_susp != 0:
            player.adjust_character_suspicion("vance", vance_susp)
        if missy_susp != 0:
            player.adjust_character_suspicion("missy", missy_susp)

        player.update_stats()
        return success

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

    def show_ledger_ui():
        """
        Pause the narrative and show the Ledger screen.
        Player dismisses it with a click; then the script continues.
        """
        renpy.call_screen("ledger_ui")

    def has_story_fuel(required_total=15):
        """
        Read-only writing-gate check.
        Returns True if (Inspiration + Corruption XP) meets the threshold.
        Does not spend any resources — use attempt_write() for the actual gate.
        """
        return (player.inspiration + player.corruption_xp) >= required_total
