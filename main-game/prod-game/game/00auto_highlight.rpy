# =============================================================================
#  00auto_highlight.rpy
#  Auto-highlight module for speaker and suspicion focus.
# =============================================================================

# This file must load before assets_manifest.rpy so sprite_highlight and
# name_callback are defined before sprite image declarations are registered.
init -60 python:
    import math

    def get_ease(t):
        return 0.5 - math.cos(math.pi * t) / 2.0

    def get_ease_back(t):
        c1 = 1.70158
        c2 = c1 * 1.525
        if t < 0.5:
            return (math.pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
        return (math.pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2

    def name_callback(event, interact=True, name=None, **kwargs):
        global speaking_char
        if event == "begin":
            speaking_char = name

    def focus_check(char_name, anim_length, anim_time, ease_func=get_ease, dict_ref=0):
        global speaking_char, sprite_focus

        if dict_ref not in sprite_focus:
            sprite_focus[dict_ref] = {}
        focus_dict = sprite_focus[dict_ref]

        if char_name not in focus_dict:
            focus_dict[char_name] = False

        status = False
        if speaking_char is not None:
            if isinstance(speaking_char, (list, tuple)):
                status = char_name in speaking_char
            else:
                status = char_name == speaking_char

        if isinstance(focus_dict[char_name], (int, float)) and anim_time < focus_dict[char_name]:
            focus_dict[char_name] = status

        if focus_dict[char_name] != status and isinstance(focus_dict[char_name], bool):
            focus_dict[char_name] = anim_time
            if renpy.is_skipping() or renpy.in_rollback():
                focus_dict[char_name] = status

        curr_time = max(anim_time - focus_dict[char_name], 0)
        curr_ease = 1.0

        if curr_time < anim_length and not isinstance(focus_dict[char_name], bool):
            t = curr_time / anim_length
            curr_ease = ease_func(t)
        else:
            focus_dict[char_name] = status

        return status, curr_ease

    class SpriteFocus(object):
        def __init__(self, sprite_name):
            self.sprite_name = sprite_name

        def __call__(self, trans, st, at):
            suspicion_target = getattr(store, "suspicion_focus", None)
            suspicion_intensity = getattr(store, "suspicion_focus_intensity", 0)
            if suspicion_target == self.sprite_name and suspicion_intensity > 0:
                boost = 0.035 if suspicion_intensity >= 2 else 0.02
                trans.matrixcolor = SaturationMatrix(1.08) * BrightnessMatrix(0.04)
                trans.zoom = 1.0 + boost
                trans.yoffset = -2 if suspicion_intensity >= 2 else -1
                return 0

            anim_length = 0.2
            bright_change = 0.08
            sat_change = 0.2
            zoom_change = 0.0025
            y_amount = 1

            status, curr_ease = focus_check(self.sprite_name, anim_length, at)
            if status:
                trans.matrixcolor = SaturationMatrix((1.0 - sat_change) + curr_ease * sat_change) * BrightnessMatrix(-bright_change + curr_ease * bright_change)
                trans.zoom = min(curr_ease * zoom_change + (1.0 - zoom_change), 1.0)
                trans.yoffset = y_amount + (-y_amount * curr_ease)
            else:
                trans.matrixcolor = SaturationMatrix(1.0 - curr_ease * sat_change) * BrightnessMatrix(curr_ease * -bright_change)
                trans.zoom = max(1.0 - curr_ease * zoom_change, (1.0 - zoom_change))
                trans.yoffset = y_amount * curr_ease
            return 0

    def sprite_highlight(sprite_name):
        return Transform(function=SpriteFocus(sprite_name))

define sprite_focus = {0: {}}
