# ═══════════════════════════════════════════════════════════════
#  functions.rpy
#  All Python-side game logic.
#  Keep Ren'Py script files free of inline Python wherever possible.
#  If you need a new mechanic, add a function here and call it
#  from the narrative with a $ prefix.
# ═══════════════════════════════════════════════════════════════

init python:

    SUSPICION_BREAKPOINTS = [15, 35, 60, 85]

    def suspicion_tier(value):
        if value >= 85:
            return "critical"
        if value >= 60:
            return "dangerous"
        if value >= 35:
            return "watching"
        if value >= 15:
            return "noticed"
        return "clear"

    def anxiety_tier(value):
        if value >= 70:
            return "high"
        if value >= 35:
            return "medium"
        return "low"

    def crossed_suspicion_breakpoints(old, new):
        if new <= old:
            return []
        return [breakpoint for breakpoint in SUSPICION_BREAKPOINTS if old < breakpoint <= new]

    def get_suspicion_monologue(character, tier, anxiety, reason=None, scene_context=None):
        candidates = []
        if scene_context is not None and reason is not None:
            candidates.append((character, tier, anxiety, reason, scene_context))
        if reason is not None:
            candidates.append((character, tier, anxiety, reason))
        candidates.extend([
            (character, tier, anxiety),
            (character, tier),
            ("generic", tier, anxiety),
            ("generic", "fallback"),
        ])
        for key in candidates:
            lines = SUSPICION_MONOLOGUES.get(key)
            if lines:
                return renpy.random.choice(lines)
        return "Something in the room shifted, not enough to name, enough to remember."

    def raise_suspicion(character, amount=0, base_amount=0, reason=None, scene_context=None, feedback=True):
        if character not in player.tracked_characters:
            raise ValueError("Unknown suspicion character '{}'. Must be one of: {}".format(
                character,
                ", ".join(player.tracked_characters),
            ))

        old = player.get_total_suspicion(character)
        player.add_suspicion(character, acute_amount=amount, base_amount=base_amount)
        new = player.get_total_suspicion(character)

        if not feedback or old == new:
            return new

        renpy.call("suspicion_feedback_minor", character, old, new)

        crossed = crossed_suspicion_breakpoints(old, new)
        unseen = player.record_suspicion_breakpoints(character, crossed)
        if unseen:
            renpy.call("suspicion_breakpoint", character, unseen[-1], reason, scene_context)

        return new

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

        # Character-specific suspicions (acute & base), processed deterministically.
        if stern_susp != 0 or stern_base != 0:
            raise_suspicion("stern", amount=stern_susp, base_amount=stern_base)
        if vance_susp != 0 or vance_base != 0:
            raise_suspicion("vance", amount=vance_susp, base_amount=vance_base)
        if gideon_susp != 0 or gideon_base != 0:
            raise_suspicion("gideon", amount=gideon_susp, base_amount=gideon_base)
        if missy_susp != 0 or missy_base != 0:
            raise_suspicion("missy", amount=missy_susp, base_amount=missy_base)

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
