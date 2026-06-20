# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes
#
# SPRITE DIRECTION (managed by scripts/scene_direction.py — how to preserve manual staging):
# [asset auto]              -> auto-placed sprite line; the agent may rewrite/replace it on re-run
# [asset keep]              -> on a show line: lock THAT line so the agent never edits it
# [asset lock:scene]        -> before/after a `scene`: the agent skips the entire scene block
# [asset pin:Name=slot]     -> force Name into slot for the rest of the scene block
# [enter:Name] / [exit:Name] -> declare cast changes so auto placement stays correct
# Full policy: docs/contracts/sprite_layout_policy.yaml | spec: docs/specs/scene-direction-agent.md

# ═══════════════════════════════════════════════════════════════
#  functions_non_canon.rpy
#  Writers' Room — promotion source for main-game/prod-game/game/functions.rpy
#
#  NOT loaded at runtime. During Release 1 promotion, merge this file into
#  functions.rpy (or diff-merge the marked sections).
#  Baseline synced from main-game/prod-game/game/functions.rpy at promotion time.
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

    # Writing gates use AND semantics: inspiration AND corruption_level must both clear.
    # (required_insp, required_corr) — not a sum.
    WRITE_GATE_CH1 = (15, 2)
    WRITE_GATE_CH2 = (30, 3)
    WRITE_GATE_CH3 = (45, 3)
    # Day 101 quality: below this corruption level → slop chapter (no manuscript_progress).
    WRITE_SLOP_MAX_CORRUPTION_LEVEL = 2

    # Consolidated anxiety blocks triumphant write at Day 104 twilight.
    ANXIETY_WRITE_PARALYSIS = 85

    def missy_repair_available():
        """Missy repair twilight option — only after Day 4 cover betrayal, once."""
        return story.missy_day4_used_as_cover and story.missy_day4_repair_state == "none"

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
        renpy.call("watch_suspicion")
        return success

    def resolve_turn():
        """
        Enforce safe turn ordering: fail-state check before passive decay.
        """
        renpy.call("watch_suspicion")
        player.update_stats()

    def set_time_period(period):
        """
        Centralized time-of-day assignment with TimeManager validation.
        """
        time_manager.set_time_of_day(period)

    def attempt_write(required_insp=30, cost=20, required_corr=3):
        """
        Shared writing-gate helper.
        """
        if player.inspiration < required_insp or player.corruption_level < required_corr:
            return False
        return player.spend_inspiration(cost)

    def show_ledger_ui():
        """
        Pause the narrative and show the Ledger screen.
        Player dismisses it with a click; then the script continues.
        """
        renpy.call_screen("ledger_ui")

    def has_story_fuel(required_insp=30, required_corr=3):
        """
        Read-only writing-gate check (AND, not sum).
        Returns True only when BOTH:
            player.inspiration >= required_insp
            player.corruption_level >= required_corr
        Use WRITE_GATE_CH1 / CH2 / CH3 for manuscript slots.
        """
        return player.has_story_fuel(required_insp, required_corr)

    def set_archetype_focus(archetype):
        story.set_current_archetype_focus(archetype)

    def add_archetype_focus(archetype, amount=1):
        if archetype == "ghost":
            player.ghost_focus += amount
        elif archetype == "prey":
            player.prey_focus += amount
        elif archetype == "predator":
            player.predator_focus += amount
        elif archetype != "none":
            raise ValueError("Invalid archetype focus: {}".format(archetype))
        player.update_stats()

    def apply_archetype_edge(archetype, amount=1):
        set_archetype_focus(archetype)
        add_archetype_focus(archetype, amount)

    def get_dominant_archetype():
        scores = [
            ("ghost", player.ghost_focus),
            ("prey", player.prey_focus),
            ("predator", player.predator_focus),
        ]
        max_score = max(score for arch, score in scores)
        if max_score == 0:
            if story.run_archetype_seed != "none":
                return story.run_archetype_seed
            return "none"
        candidates = [arch for arch, score in scores if score == max_score]
        if story.run_archetype_seed in candidates:
            return story.run_archetype_seed
        return candidates[0]

    def can_choose_archetype_focus(archetype, max_anxiety=None, min_corruption_level=None):
        if max_anxiety is not None and player.anxiety > max_anxiety:
            return False
        if min_corruption_level is not None and player.corruption_level < min_corruption_level:
            return False
        return True

    def get_archetype_block_reason(archetype, max_anxiety=None, min_corruption_level=None):
        if max_anxiety is not None and player.anxiety > max_anxiety:
            return "Cora can imagine it. Her body will not carry it out. (Anxiety too high)"
        if min_corruption_level is not None and player.corruption_level < min_corruption_level:
            return "Cora lacks the dark resolve required. (Corruption too low)"
        return ""

    def apply_balanced_effect(profile, intensity="standard", witness=None, base_witness=False):
        """
        Resolve a semantic profile and apply it through the existing mutation gateway.
        Must never mutate PlayerStats directly.
        """
        kwargs = balance_resolver.resolve_balanced_effect(
            profile,
            intensity_override=intensity,
            witness=witness,
            base_witness=base_witness,
        )
        return apply_effects(**kwargs)
