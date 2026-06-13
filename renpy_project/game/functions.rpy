# ═══════════════════════════════════════════════════════════════
#  functions.rpy
#  All Python-side game logic.
#  Keep Ren'Py script files free of inline Python wherever possible.
#  If you need a new mechanic, add a function here and call it
#  from the narrative with a $ prefix.
# ═══════════════════════════════════════════════════════════════

init python:

    SUSPICION_BREAKPOINTS = [15, 35, 60, 85]

    SUSPICION_CHARACTER_NAMES = {
        "stern": "Miss Stern",
        "vance": "Vance",
        "gideon": "Sir Gideon",
        "missy": "Missy",
        "generic": "Someone",
    }

    SUSPICION_MONOLOGUES = {
        ("vance", "noticed", "low"): ["Vance noticed the edge of my mask and said nothing."],
        ("vance", "noticed", "medium"): ["Vance's eyes caught on mine for half a second too long."],
        ("vance", "noticed", "high"): ["Vance saw something; not enough to accuse me, enough to remember."],
        ("vance", "watching", "low"): ["Vance had begun to read me as if we shared a language no one else could hear."],
        ("vance", "watching", "medium"): ["Vance watched with the wounded cleverness of someone who knew performance from the inside."],
        ("vance", "dangerous", "low"): ["Vance was arranging recognition into something sharper than gossip."],
        ("vance", "dangerous", "high"): ["Vance knew too much about masks to mistake mine for skin."],
        ("vance", "critical", "high"): ["Vance was one breath from naming what she recognized in me."],
        ("vance", "noticed", "high", "recognised_detail"): ["Recognition flashed in Vance's eyes, brief and intimate and impossible to unsay."],
        ("stern", "noticed", "low"): ["Miss Stern filed the moment away as neatly as a key returned to its hook."],
        ("stern", "noticed", "medium"): ["Miss Stern said nothing, which was worse than a question."],
        ("stern", "noticed", "high"): ["Miss Stern had seen the inconsistency and would not misplace it."],
        ("stern", "watching", "low"): ["Miss Stern's attention settled on me with the weight of a rulebook opening."],
        ("stern", "watching", "medium"): ["Miss Stern had begun inspecting my answers for loose threads."],
        ("stern", "dangerous", "low"): ["Miss Stern was turning suspicion into procedure."],
        ("stern", "dangerous", "high"): ["Miss Stern had nearly enough to make discipline sound like duty."],
        ("stern", "critical", "high"): ["Miss Stern's silence had reached the edge of a formal charge."],
        ("stern", "watching", "medium", "disciplinary_notice"): ["Miss Stern put the moment in order, as if misconduct were only another ledger column."],
        ("gideon", "noticed", "low"): ["Sir Gideon smiled as if I had finally become interesting."],
        ("gideon", "noticed", "medium"): ["Sir Gideon watched me as though patience were another form of ownership."],
        ("gideon", "noticed", "high"): ["Sir Gideon had caught the shape of the lie and seemed almost pleased."],
        ("gideon", "watching", "low"): ["Sir Gideon looked entertained, which was far worse than alarmed."],
        ("gideon", "watching", "medium"): ["Sir Gideon had begun treating my caution as a move in his game."],
        ("gideon", "dangerous", "low"): ["Sir Gideon was not frightened by the pattern; he was amused by it."],
        ("gideon", "dangerous", "high"): ["Sir Gideon had seen enough to wait for me to expose myself."],
        ("gideon", "critical", "high"): ["Sir Gideon stood close to the truth and smiled as if he owned the door."],
        ("gideon", "noticed", "low", "provoked_interest"): ["Sir Gideon marked the provocation and looked pleased that I had dared it."],
        ("missy", "noticed", "low"): ["Missy waited for the harmless explanation I had not prepared."],
        ("missy", "noticed", "medium"): ["Missy's trust faltered, and the cost of that was suddenly plain."],
        ("missy", "noticed", "high"): ["Missy looked at me as if I had made kindness into a trick."],
        ("missy", "watching", "low"): ["Missy watched because trust had taught her where to look."],
        ("missy", "watching", "medium"): ["Missy was trying to keep believing me, and that made every pause crueler."],
        ("missy", "dangerous", "low"): ["Missy's doubt hurt more because it had not learned to defend itself."],
        ("missy", "dangerous", "high"): ["Missy was beginning to understand that kindness could be used against her."],
        ("missy", "critical", "high"): ["Missy looked close to the truth, and the truth looked like betrayal."],
        ("missy", "noticed", "high", "hurt_trust"): ["Missy's face changed as trust became evidence against me."],
        ("generic", "noticed", "low"): ["My mask held, but someone had seen the edge of it."],
        ("generic", "noticed", "medium"): ["A glance shifted the room by an inch."],
        ("generic", "noticed", "high"): ["A pause, a look, a change in the air; I felt it before I understood it."],
        ("generic", "watching", "low"): ["The room had begun to study me back."],
        ("generic", "watching", "medium"): ["Someone was arranging the pieces now."],
        ("generic", "watching", "high"): ["The silence around me had learned to count."],
        ("generic", "dangerous", "low"): ["Suspicion had become a pattern, and patterns could be followed."],
        ("generic", "dangerous", "medium"): ["One more careless answer could make the pattern visible."],
        ("generic", "dangerous", "high"): ["The walls were closing in now; my next mistake could finish me."],
        ("generic", "critical", "low"): ["The next misstep would not be forgiven as clumsiness."],
        ("generic", "critical", "medium"): ["The room was one breath from accusation."],
        ("generic", "critical", "high"): ["There was almost no mask left to hold."],
        ("generic", "fallback"): ["Something in the room shifted, not enough to name, enough to remember."],
    }

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
