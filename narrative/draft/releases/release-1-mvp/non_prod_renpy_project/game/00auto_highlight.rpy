# ═══════════════════════════════════════════════════════════════
#  00auto_highlight.rpy
#  Auto-Highlight module for Ren'Py (Sandbox Version).
# ═══════════════════════════════════════════════════════════════

# This file must be loaded before assets_manifest.rpy (which runs at init -50 and -40)
# to ensure sprite_highlight and name_callback are defined early.
init -60 python:
    import math

    # Easing functions for animations
    def get_ease(t):
        return 0.5 - math.cos(math.pi * t) / 2.0

    def get_ease_back(t):
        c1 = 1.70158
        c2 = c1 * 1.525
        return (math.pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2 if t < 0.5 else (math.pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2

    # name_callback is triggered on Character dialogue events to track the speaker
    def name_callback(event, interact=True, name=None, **kwargs):
        global speaking_char
        if event == "begin":
            speaking_char = name

    # focus_check manages the focus dictionary state and calculates animation easing
    def focus_check(char_name, anim_length, anim_time, ease_func=get_ease, dict_ref=0):
        global speaking_char, sprite_focus
        
        # Ensure focus dict references exist safely
        if dict_ref not in sprite_focus: 
            sprite_focus[dict_ref] = {}
        focus_dict = sprite_focus[dict_ref]
        
        if char_name not in focus_dict:
            focus_dict[char_name] = False
            
        status = False
        if speaking_char is not None:
            # Enhanced safety check to prevent substring matching bugs (e.g. "cora" in "cora_inner")
            if isinstance(speaking_char, (list, tuple)):
                status = char_name in speaking_char
            else:
                status = char_name == speaking_char

        # If key is numeric and animation has not caught up, reset status to boolean
        if isinstance(focus_dict[char_name], (int, float)) and anim_time < focus_dict[char_name]:
            focus_dict[char_name] = status
            
        # If the talking status has changed, start the animation timer
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

    # Callable SpriteFocus class wrapping the ATL transform logic
    class SpriteFocus(object):
        def __init__(self, sprite_name):
            self.sprite_name = sprite_name

        def __call__(self, trans, st, at):
            anim_length = 0.2       # Duration of the focus transition in seconds
            bright_change = 0.08    # Unfocused dimming amount
            sat_change = 0.2        # Unfocused desaturation amount
            zoom_change = 0.0025    # Focus scale factor
            y_amount = 1            # Vertical correction offset
            
            status, curr_ease = focus_check(self.sprite_name, anim_length, at)
            if status: # Highlight/Focus
                trans.matrixcolor = SaturationMatrix((1.0 - sat_change) + curr_ease * sat_change) * BrightnessMatrix(-bright_change + curr_ease * bright_change)
                trans.zoom = min(curr_ease * zoom_change + (1.0 - zoom_change), 1.0)
                trans.yoffset = y_amount + (-y_amount * curr_ease)
            else:      # Dim/Unfocus
                trans.matrixcolor = SaturationMatrix(1.0 - curr_ease * sat_change) * BrightnessMatrix(curr_ease * -bright_change)
                trans.zoom = max(1.0 - curr_ease * zoom_change, (1.0 - zoom_change))
                trans.yoffset = y_amount * curr_ease
            return 0

    # Transform that invokes SpriteFocus, defined in Python to compile early
    def sprite_highlight(sprite_name):
        return Transform(function=SpriteFocus(sprite_name))

# Variables must be defined as early as possible
define sprite_focus = {0:{}}
