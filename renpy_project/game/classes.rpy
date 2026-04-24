# ═══════════════════════════════════════════════════════════════
#  classes.rpy
#  All Python class definitions.
# ═══════════════════════════════════════════════════════════════

init -1 python:

    class TimeManager(object):
        ALLOWED_PERIODS = (
            "Early Morning",
            "Morning",
            "Afternoon",
            "Evening",
            "Night",
            "Late Night",
        )

        def __init__(self):
            self.current_day = 1
            self._time_of_day = "Morning"

        @property
        def time_of_day(self):
            return self._time_of_day

        @time_of_day.setter
        def time_of_day(self, value):
            if value not in self.ALLOWED_PERIODS:
                raise ValueError(
                    "Invalid time_of_day '{}'. Allowed values: {}".format(
                        value, ", ".join(self.ALLOWED_PERIODS)
                    )
                )
            self._time_of_day = value

        def set_time_of_day(self, value):
            self.time_of_day = value

        def set_current_day(self, value):
            if not isinstance(value, int):
                raise TypeError("current_day must be an int, got {}".format(type(value).__name__))
            if value < 1:
                raise ValueError("current_day must be >= 1")
            self.current_day = value

    class PlayerStats(object):
        def __init__(self):
            self.corruption_level = 1
            self.corruption_xp = 0
            self.inspiration = 0
            self.suspicion = 0

        @property
        def inspiration_cap(self):
            return 20 + (self.corruption_level * 10)

        def update_stats(self):
            # Suspicion must never be below 0 or above 100.
            self.suspicion = max(0, min(100, self.suspicion))

            # Corruption XP must never be below 0.
            self.corruption_xp = max(0, self.corruption_xp)

            while self.corruption_xp >= 20:
                self.corruption_xp -= 20
                self.corruption_level += 1

            # Inspiration must never be below 0 or above the current cap.
            self.inspiration = max(0, min(self.inspiration_cap, self.inspiration))

        def gain_inspiration(self, amount):
            if amount < 0:
                raise ValueError("gain_inspiration() cannot receive a negative amount. Use spend_inspiration().")

            self.inspiration += amount
            self.update_stats()

        def spend_inspiration(self, amount):
            if amount < 0:
                raise ValueError("spend_inspiration() cannot receive a negative amount.")

            if self.inspiration >= amount:
                self.inspiration -= amount
                self.update_stats()
                return True

            return False

        def gain_corruption_xp(self, amount):
            if amount < 0:
                raise ValueError("Corruption cannot decrease.")

            self.corruption_xp += amount
            self.update_stats()

        def raise_suspicion(self, amount):
            if amount < 0:
                raise ValueError("raise_suspicion() cannot receive a negative amount. Use lower_suspicion().")

            self.suspicion += amount
            self.update_stats()

        def lower_suspicion(self, amount):
            if amount < 0:
                raise ValueError("lower_suspicion() cannot receive a negative amount.")

            self.suspicion -= amount
            self.update_stats()

    class StoryState(object):
        # Mutually exclusive branch: whitelist only; use set_corridor_state() in scripts.
        VALID_CORRIDOR_STATES = ("none", "ghost", "predator", "prey")

        def __init__(self):
            self.day1_corridor_state = "none"
            self.has_witnessed_voyeur_scene = False
            self.has_written_first_chapter = False

        def _set_boolean_flag(self, field_name, value):
            if not isinstance(value, bool):
                raise TypeError("{} must be a bool, got {}".format(field_name, type(value).__name__))
            setattr(self, field_name, value)

        def set_corridor_state(self, new_state):
            if new_state not in self.VALID_CORRIDOR_STATES:
                raise ValueError(
                    "Invalid corridor state '{}'. Must be one of: {}".format(
                        new_state, ", ".join(self.VALID_CORRIDOR_STATES)
                    )
                )
            self.day1_corridor_state = new_state

        def set_has_witnessed_voyeur_scene(self, value):
            self._set_boolean_flag("has_witnessed_voyeur_scene", value)

        def set_has_written_first_chapter(self, value):
            self._set_boolean_flag("has_written_first_chapter", value)
