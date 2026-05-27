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

    def apply_effects(insp=0, corr=0, susp=0, 
                      stern_susp=0, stern_base=0, 
                      vance_susp=0, vance_base=0, 
                      missy_susp=0, missy_base=0,
                      gideon_susp=0, gideon_base=0):
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

        # Legacy susp deprecation:
        if susp != 0:
            raise ValueError("Legacy general 'susp' is deprecated. Suspicion must target a specific witness (stern_susp, vance_susp, missy_susp, gideon_susp).")

        # Character-specific suspicions (acute & base):
        if stern_susp != 0 or stern_base != 0:
            player.add_suspicion("stern", acute_amount=stern_susp, base_amount=stern_base)
        if vance_susp != 0 or vance_base != 0:
            player.add_suspicion("vance", acute_amount=vance_susp, base_amount=vance_base)
        if missy_susp != 0 or missy_base != 0:
            player.add_suspicion("missy", acute_amount=missy_susp, base_amount=missy_base)
        if gideon_susp != 0 or gideon_base != 0:
            player.add_suspicion("gideon", acute_amount=gideon_susp, base_amount=gideon_base)

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
