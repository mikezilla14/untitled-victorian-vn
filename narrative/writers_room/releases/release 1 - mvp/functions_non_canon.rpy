# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes

# ═══════════════════════════════════════════════════════════════
#  functions_non_canon.rpy
#  Writers' Room — promotion source for renpy_project/game/functions.rpy
#
#  NOT loaded at runtime. During Release 1 promotion, merge this file into
#  functions.rpy (or diff-merge the marked sections).
#  Baseline synced from renpy_project/game/functions.rpy at promotion time.
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
