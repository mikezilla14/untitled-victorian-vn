import re
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INACTIVE_PROFILES = {
    "safe": "observant",
    "obedient": "observant",
    "submissive": "observant",
    "defiant": "transgressive",
    "reckless": "transgressive",
    "predatory": "transgressive",
    "self_protective": "observant"
}

RISKY_PROFILES = {"curious", "transgressive", "deceptive"}

def determine_witness(file_name, label, current_line):
    # Determine the most likely tracked witness for the context
    fn = file_name.lower()
    lbl = (label or "").lower()
    
    if "stern" in lbl or "stern" in current_line.lower():
        return "stern"
    if "vance" in lbl or "vance" in current_line.lower():
        return "vance"
    if "missy" in lbl or "missy" in current_line.lower():
        return "missy"
    if "gideon" in lbl or "gideon" in current_line.lower():
        return "gideon"
        
    if "day101" in fn:
        if "interview" in lbl:
            return "stern"
        if "dressing" in lbl or "stairwell" in lbl or "retaliation" in lbl:
            return "vance"
    elif "day102" in fn:
        if "deceive" in lbl or "first_shift" in lbl or "thing" in lbl:
            return "missy"
        if "frame" in lbl or "tea" in lbl:
            return "stern"
    elif "day103" in fn:
        if "gideon" in lbl:
            return "vance" # Gideon interactions in day 103 use vance_susp
        if "corridor" in lbl:
            if "stern" in current_line.lower(): return "stern"
            if "vance" in current_line.lower(): return "vance"
            if "missy" in current_line.lower(): return "missy"
    elif "day104" in fn:
        if "escape" in lbl:
            if "fireplace" in lbl or "fireplace" in current_line.lower(): return "stern"
            if "bold_lie" in lbl or "bold_lie" in current_line.lower(): return "vance"
            if "missy" in lbl or "missy" in current_line.lower(): return "missy"
        if "pressure" in lbl:
            return "stern"
        if "repair" in lbl:
            return "missy"
    elif "day105" in fn:
        if "motivation" in lbl:
            if "prey" in lbl or "ghost" in lbl: return "vance"
            if "predator" in lbl: return "gideon"
        if "marks" in lbl or "money" in lbl:
            if "refused" in current_line.lower(): return "vance"
            return "gideon"
            
    return "stern" # fallback default

def parse_args_string(arg_str):
    if not arg_str:
        return {}
    # Parse key=value arguments
    kwargs = {}
    for part in re.split(r",(?![^\(]*\))", arg_str):
        part = part.strip()
        if not part or "=" not in part:
            continue
        k, v = part.split("=", 1)
        k = k.strip()
        v = v.strip()
        # strip quotes from string values
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            kwargs[k] = v[1:-1]
        elif v.lower() == "true":
            kwargs[k] = True
        elif v.lower() == "false":
            kwargs[k] = False
        else:
            try:
                kwargs[k] = int(v)
            except ValueError:
                try:
                    kwargs[k] = float(v)
                except ValueError:
                    kwargs[k] = v
    return kwargs

def clean_kwargs(kwargs, allowed_keys):
    return {k: v for k, v in kwargs.items() if k in allowed_keys and v != 0}

def split_mixed_apply_effects(kwargs, file_name, label, line_str):
    # Legacy mixed apply_effects(vance_susp=-5, insp=15, corr=5) etc.
    # Split into:
    # 1. apply_balanced_effect(profile, intensity="standard", witness=witness)
    # 2. apply_effects(susp_key=negative_value)
    
    insp = kwargs.get("insp", 0)
    corr = kwargs.get("corr", 0)
    
    # 1. Determine profile for positive part
    if corr >= 10:
        profile = "transgressive"
    elif corr >= 6:
        profile = "curious" # or deceptive
    elif corr >= 1:
        profile = "creative"
    else:
        profile = "observant" if insp <= 2 else "creative"
        
    witness = None
    if profile in RISKY_PROFILES:
        # Check if kwargs has a positive susp key we can extract witness from
        susp_keys = [k for k in kwargs if k.endswith("_susp") or k.endswith("_base")]
        for k in susp_keys:
            if kwargs[k] > 0:
                witness = k.split("_")[0]
                break
        if not witness:
            witness = determine_witness(file_name, label, line_str)
            
    # Positive part string
    if profile in RISKY_PROFILES:
        part1 = f'apply_balanced_effect("{profile}", intensity="standard", witness="{witness}")'
    else:
        part1 = f'apply_balanced_effect("{profile}", intensity="standard")'
        
    # 2. Negative susp part
    neg_susp = {}
    for k, v in kwargs.items():
        if (k.endswith("_susp") or k.endswith("_base")) and v < 0:
            neg_susp[k] = v
            
    if neg_susp:
        neg_args = ", ".join(f"{k}={v}" for k, v in neg_susp.items())
        part2 = f"# [STATE bespoke: negative_suspicion]\n            $ apply_effects({neg_args})"
        return f"$ {part1}\n            {part2}"
    else:
        return f"$ {part1}"

def process_file(path: Path):
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = []
    
    label_re = re.compile(r"^\s*label\s+([a-zA-Z0-9_]+)\s*:")
    balanced_re = re.compile(r'apply_balanced_effect\s*\(\s*"([^"]+)"\s*(?:,\s*(.*))?\)\s*$')
    effects_re = re.compile(r'apply_effects\s*\(\s*(.*)\)\s*$')
    
    current_label = None
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        
        # Track label
        l_match = label_re.match(line)
        if l_match:
            current_label = l_match.group(1)
            
        # 1. Match apply_balanced_effect
        b_match = balanced_re.search(line)
        if b_match:
            profile = b_match.group(1)
            arg_str = b_match.group(2)
            kwargs = parse_args_string(arg_str)
            
            # Map inactive profile
            if profile in INACTIVE_PROFILES:
                if "day100" in path.name:
                    # In day 100, we don't have witness, map to non-witness active profiles
                    if profile in ("curious", "transgressive", "reckless", "predatory"):
                        profile = "creative"
                    else:
                        profile = "observant"
                else:
                    profile = INACTIVE_PROFILES[profile]
                    
            intensity = "standard" # force standard
            
            witness = kwargs.get("witness")
            if profile in RISKY_PROFILES:
                if not witness or "day100" in path.name:
                    if "day100" in path.name:
                        # Map to creative to avoid witness
                        profile = "creative"
                    else:
                        witness = determine_witness(path.name, current_label, line)
            else:
                # observant/creative do not need witness
                witness = None
                
            # Construct new call
            indent = line[:line.find("$")]
            if witness:
                new_call = f'{indent}$ apply_balanced_effect("{profile}", intensity="standard", witness="{witness}")'
            else:
                new_call = f'{indent}$ apply_balanced_effect("{profile}", intensity="standard")'
                
            new_lines.append(new_call)
            idx += 1
            continue
            
        # 2. Match apply_effects
        e_match = effects_re.search(line)
        if e_match:
            arg_str = e_match.group(1)
            kwargs = parse_args_string(arg_str)
            
            # Check if it is an allowlisted mixed exception
            # We look up in our known list of exceptions
            is_allowlisted = False
            # 1. day104 missy repair
            if "day104" in path.name and current_label == "day104_4_missy_repair" and kwargs.get("missy_susp") == -25:
                is_allowlisted = True
                reason = "legacy_exception"
            # 2. day104 escape missy cover
            elif "day104" in path.name and current_label == "day104_2_escape_missy_cover":
                is_allowlisted = True
                reason = "legacy_exception"
            # 3. day104 stern pressure
            elif "day104" in path.name and current_label == "day104_3_stern_pressure" and kwargs.get("stern_susp") == -10:
                is_allowlisted = True
                reason = "legacy_exception"
            # 4. confrontations
            elif "story_chains" in path.name and current_label in ("confrontation_stern", "confrontation_vance", "confrontation_missy"):
                is_allowlisted = True
                reason = "legacy_exception"
                
            indent = line[:line.find("$")]
            
            if is_allowlisted:
                # Rewrite/replace preceding comment with reason
                # Pop the preceding comment line if it exists and rewrite it
                if new_lines and new_lines[-1].strip().startswith("#"):
                    new_lines.pop()
                new_lines.append(f"{indent}# [STATE bespoke: {reason}]")
                # Keep the exact clean kwargs
                clean_kw = clean_kwargs(kwargs, ("insp", "corr", "stern_susp", "vance_susp", "missy_susp", "gideon_susp"))
                kw_str = ", ".join(f"{k}={v}" for k, v in clean_kw.items())
                new_lines.append(f"{indent}$ apply_effects({kw_str})")
                idx += 1
                continue
                
            # Check if it is pure negative suspicion
            has_pos_susp = any(v > 0 for k, v in kwargs.items() if k.endswith("_susp") or k.endswith("_base"))
            has_neg_susp = any(v < 0 for k, v in kwargs.items() if k.endswith("_susp") or k.endswith("_base"))
            has_pos_insp_corr = kwargs.get("insp", 0) > 0 or kwargs.get("corr", 0) > 0
            has_neg_insp = kwargs.get("insp", 0) < 0
            
            if has_neg_susp and not has_pos_susp and not has_pos_insp_corr and not has_neg_insp:
                # Pure negative suspicion
                if new_lines and new_lines[-1].strip().startswith("#"):
                    new_lines.pop()
                new_lines.append(f"{indent}# [STATE bespoke: negative_suspicion]")
                clean_kw = clean_kwargs(kwargs, ("stern_susp", "vance_susp", "missy_susp", "gideon_susp"))
                kw_str = ", ".join(f"{k}={v}" for k, v in clean_kw.items())
                new_lines.append(f"{indent}$ apply_effects({kw_str})")
                idx += 1
                continue
                
            # Check if it is pure write spend
            if has_neg_insp and not has_pos_insp_corr and not has_neg_susp and not has_pos_susp:
                # Pure write spend
                if new_lines and new_lines[-1].strip().startswith("#"):
                    new_lines.pop()
                new_lines.append(f"{indent}# [STATE bespoke: write_spend]")
                new_lines.append(f"{indent}$ apply_effects(insp={kwargs['insp']})")
                idx += 1
                continue
                
            # Check if it is pure gate failure penalty (positive susp only, no insp/corr)
            if has_pos_susp and not has_neg_susp and not has_pos_insp_corr and not has_neg_insp:
                if new_lines and new_lines[-1].strip().startswith("#"):
                    new_lines.pop()
                new_lines.append(f"{indent}# [STATE bespoke: gate_failure_penalty]")
                clean_kw = clean_kwargs(kwargs, ("stern_susp", "vance_susp", "missy_susp", "gideon_susp"))
                kw_str = ", ".join(f"{k}={v}" for k, v in clean_kw.items())
                new_lines.append(f"{indent}$ apply_effects({kw_str})")
                idx += 1
                continue
                
            # Mixed split required!
            if has_pos_insp_corr and has_neg_susp:
                # Split it!
                if new_lines and new_lines[-1].strip().startswith("#"):
                    new_lines.pop()
                split_str = split_mixed_apply_effects(kwargs, path.name, current_label, line)
                # split_str is multiline with indentation
                # let's split and apply indentation
                for part in split_str.split("\n"):
                    new_lines.append(f"{indent}{part.strip()}")
                idx += 1
                continue
                
            # If it's a positive only apply_effects (like day103 write_gate success: insp=5, corr=5)
            if has_pos_insp_corr and not has_neg_susp and not has_pos_susp:
                # Map to creative standard!
                profile = "creative" if kwargs.get("corr", 0) < 10 else "transgressive"
                if new_lines and new_lines[-1].strip().startswith("#"):
                    new_lines.pop()
                if profile in RISKY_PROFILES:
                    witness = determine_witness(path.name, current_label, line)
                    new_lines.append(f'{indent}$ apply_balanced_effect("{profile}", intensity="standard", witness="{witness}")')
                else:
                    new_lines.append(f'{indent}$ apply_balanced_effect("{profile}", intensity="standard")')
                idx += 1
                continue
                
            # Default fallthrough (keep as is but tag as bespoke legacy_exception)
            if new_lines and new_lines[-1].strip().startswith("#"):
                new_lines.pop()
            new_lines.append(f"{indent}# [STATE bespoke: legacy_exception]")
            new_lines.append(line)
            idx += 1
            continue
            
        new_lines.append(line)
        idx += 1
        
    path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"Smart-migrated {path.name}")

def main():
    files = list((ROOT / "main-game" / "non-prod-game" / "game" / "days").glob("*.rpy"))
    files.append(ROOT / "main-game" / "non-prod-game" / "game" / "shared" / "story_chains_non_canon.rpy")
    
    for path in files:
        if path.name in ("balance_profiles_non_canon.rpy", "functions_non_canon.rpy"):
            continue
        process_file(path)

if __name__ == "__main__":
    main()
