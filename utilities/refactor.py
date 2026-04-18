import os
import re

game_dir = r"c:\Users\mikez\OneDrive\Documents\gh\git\untitled-victorian-vn\renpy_project\game"

target_files = [
    "script.rpy", "day1.rpy", "day2.rpy", "day3.rpy", "day4.rpy", "day5.rpy", "endings.rpy", "screens.rpy"
]

story_flags = [
    "read_letters", "saw_voyeur_scene", "heard_stern_humming",
    "gideon_spoke_day2", "gideon_showed_depth", "manuscript_sent",
    "payment_received", "wrote_chapter_1", "wrote_chapter_2", "chose_bold_day4"
]

methods = [
    "update_stats", "gain_inspiration", "gain_corruption_xp", 
    "raise_suspicion", "lower_suspicion", "spend_inspiration"
]

time_vars = ["current_day", "time_of_day"]
player_stats = ["suspicion", "inspiration", "corruption_level", "corruption_xp"]

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        original = line
        
        # Determine if this line is part of logic or has bracket interpolation
        is_logic_line = re.match(r'^\s*(\$|if\b|elif\b|while\b)', line) is not None
        has_bracket_interpolation = '[' in line and ']' in line
        
        # Temporary strings to work with
        mod_line = line

        if is_logic_line:
            # Story Flags
            for flag in story_flags:
                mod_line = re.sub(r'(?<!\.)\b' + flag + r'\b', 'story.' + flag, mod_line)
            
            # Methods
            for method in methods:
                mod_line = re.sub(r'(?<!\.)\b' + method + r'\(', 'player.' + method + '(', mod_line)
                
            # Time Vars
            for tv in time_vars:
                mod_line = re.sub(r'(?<!\.)\b' + tv + r'\b', 'time_manager.' + tv, mod_line)
                
            # Player Stats
            for stat in player_stats:
                # Matches the word exactly, ensuring it isn't part of an object (no dot prefix)
                # and isn't part of a method call (no opening parens)
                mod_line = re.sub(r'(?<!\.)\b' + stat + r'\b(?!\s*\])', 'player.' + stat, mod_line)
        
        if has_bracket_interpolation:
            # Replace only within brackets [stat]
            for stat in player_stats:
                mod_line = re.sub(r'\[' + stat + r'\]', '[player.' + stat + ']', mod_line)
            for flag in story_flags:
                mod_line = re.sub(r'\[' + flag + r'\]', '[story.' + flag + ']', mod_line)
            for tv in time_vars:
                mod_line = re.sub(r'\[' + tv + r'\]', '[time_manager.' + tv + ']', mod_line)
                
        new_lines.append(mod_line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


for filename in target_files:
    filepath = os.path.join(game_dir, filename)
    if os.path.exists(filepath):
        process_file(filepath)
        print(f"Processed {filename}")
