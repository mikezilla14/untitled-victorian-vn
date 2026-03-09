import sys
import re

file_path = "c:/Users/mikez/OneDrive/Documents/gh/git/untitled-victorian-vn/game/script.rpy"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Definition
    if "default corruption = 0" in line:
        new_lines.append(line.replace("default corruption = 0", "default corruption_level = 1\ndefault corruption_xp = 0"))
    # Stats overlay text
    elif "text \"Corruption:" in line:
        new_lines.append(line.replace("text \"Corruption: [corruption]\" size 14 color \"#ef5350\"", "text \"Corruption: Lvl [corruption_level] ([corruption_xp] XP)\" size 14 color \"#ef5350\""))
    elif "text \"Suspicion:" in line:
        new_lines.append(line.replace("text \"Suspicion: [suspicion]\"", "text \"Suspicion: [suspicion]%\""))
    # Python Block declaration
    elif "global suspicion, corruption, inspiration" in line:
        new_lines.append(line.replace("global suspicion, corruption, inspiration", "        global suspicion, corruption_level, corruption_xp, inspiration"))
    # Function renaming
    elif "def clamp_stats():" in line:
        new_lines.append(line.replace("def clamp_stats():", "def update_stats():"))
    # Call renaming
    elif "clamp_stats()" in line:
        new_lines.append(line.replace("clamp_stats()", "update_stats()"))
    # Logic in stats function
    elif "suspicion = max(0, min(100, suspicion))" in line:
        new_lines.append("        # Natural decay of suspicion each period\n")
        new_lines.append("        suspicion -= 5\n")
        new_lines.append(line)
    elif "corruption = max(0, min(100, corruption))" in line:
        new_lines.append("        corruption_xp = max(0, corruption_xp)\n")
        new_lines.append("        \n")
        new_lines.append("        # Level up logic: 20 XP per level\n")
        new_lines.append("        while corruption_xp >= 20:\n")
        new_lines.append("            corruption_xp -= 20\n")
        new_lines.append("            corruption_level += 1\n")
    elif "inspiration = max(0, min(100, inspiration))" in line:
        new_lines.append(line.replace("max(0, min(100, inspiration))", "max(0, inspiration)"))
    # Story logic updates
    elif "$ corruption +=" in line or "$ corruption -=" in line:
        new_lines.append(line.replace("$ corruption ", "$ corruption_xp "))
    elif "if corruption < 30:" in line:
        new_lines.append(line.replace("corruption < 30", "corruption_level < 2"))
    elif "if corruption >= 30:" in line:
        new_lines.append(line.replace("corruption >= 30", "corruption_level >= 2"))
    elif "if corruption >= 40:" in line:
        new_lines.append(line.replace("corruption >= 40", "corruption_level >= 3"))
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Updated script.rpy with new stat mechanics")
