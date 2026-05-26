import os
import re
import sys
from pathlib import Path

# Paths
ROOT = Path(r"c:\Users\mikez\OneDrive\Documents\gh\git\untitled-victorian-vn")
GAME_DIR = ROOT / "renpy_project" / "game"
MANIFEST_PATH = GAME_DIR / "assets_manifest.rpy"

def load_manifest_declarations():
    if not MANIFEST_PATH.exists():
        print(f"ERROR: {MANIFEST_PATH} not found.")
        sys.exit(1)
        
    text = MANIFEST_PATH.read_text(encoding="utf-8")
    
    # Matches: declare_image_with_fallback("image_id", "rel_path", ...)
    image_declarations = {}
    image_pattern = re.compile(
        r'declare_image_with_fallback\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']'
    )
    for match in image_pattern.finditer(text):
        image_id, rel_path = match.groups()
        image_declarations[image_id] = rel_path
        
    # Matches: register_audio("alias", "rel_path")
    # or audio_var = register_audio("alias", "rel_path")
    audio_declarations = {}
    audio_pattern = re.compile(
        r'(?:audio_[a-zA-Z0-9_]+\s*=\s*)?register_audio\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']'
    )
    for match in audio_pattern.finditer(text):
        alias, rel_path = match.groups()
        audio_declarations[alias] = rel_path
        
    return image_declarations, audio_declarations

def scan_game_scripts_for_assets():
    rpy_files = list(GAME_DIR.glob("*.rpy"))
    
    # We want to skip assets_manifest.rpy itself to avoid circular matching
    rpy_files = [f for f in rpy_files if f.name != "assets_manifest.rpy"]
    
    referenced_images = set()
    referenced_audios = set()
    
    # Regexes for assets used in dialogue / script lines
    # scene <image_name> [with ...]
    scene_pattern = re.compile(r'^\s*scene\s+([a-zA-Z0-9_-]+)(?:\s+[a-zA-Z0-9_-]+)*')
    # show <image_name_tag> <pose/attr> [at ...]
    show_pattern = re.compile(r'^\s*show\s+([a-zA-Z0-9_-]+)(?:\s+([a-zA-Z0-9_-]+))?(?:\s+at|\s+with|\s+as|\s+behind|$)')
    
    # play music / play sound / play audio <alias> (or voice)
    play_pattern = re.compile(r'^\s*play\s+(music|sound|audio)\s+([a-zA-Z0-9_]+|[a-zA-Z0-9_/.-]+)')
    # also check if the audio namespace is referenced: audio.xxx or audio_xxx
    audio_var_pattern = re.compile(r'\b(audio_[a-zA-Z0-9_]+)\b')
    
    for rpy_path in rpy_files:
        lines = rpy_path.read_text(encoding="utf-8").splitlines()
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
                
            # 1. Check scene
            scene_match = scene_pattern.match(line)
            if scene_match:
                # E.g., scene bg_master_suite_day
                parts = stripped.split()
                # Parts: ['scene', 'bg_master_suite_day', 'with', 'fade']
                if len(parts) > 1 and parts[1] != "expression":
                    img_name = parts[1].rstrip(":")
                    referenced_images.add(img_name)
                    
            # 2. Check show
            # For show, it can be single-word image (e.g. show ui_cora_base)
            # or multi-word (e.g. show gideon_sprite dominant at center)
            if stripped.startswith("show "):
                parts = stripped.split()
                # parts[0] is 'show'
                if len(parts) > 1 and parts[1] != "expression":
                    if parts[1] == "screen":
                        # Skip 'show screen stats_overlay'
                        continue
                    tag = parts[1].rstrip(":")
                    # Let's see if the next word is an attribute or a Ren'Py modifier (at, with, as, behind)
                    attr = None
                    if len(parts) > 2:
                        next_word = parts[2]
                        if next_word not in {"at", "with", "as", "behind", ":"}:
                            attr = next_word.rstrip(":")
                    if attr:
                        referenced_images.add(f"{tag} {attr}")
                    else:
                        referenced_images.add(tag)
                        
            # 3. Check play
            play_match = play_pattern.search(line)
            if play_match:
                channel, name = play_match.groups()
                # Remove quotes if any
                name = name.strip("\"'")
                referenced_audios.add(name)
                
            # 4. Check audio variables (like audio_themes_savoy_tension)
            for var in audio_var_pattern.findall(line):
                referenced_audios.add(var)
                
    return referenced_images, referenced_audios

def check_sync():
    print("=== Loading Asset Manifest Declarations ===")
    manifest_images, manifest_audios = load_manifest_declarations()
    print(f"Declared Images: {len(manifest_images)}")
    print(f"Declared Audios: {len(manifest_audios)}")
    
    print("\n=== Scanning Game Scripts for Referenced Assets ===")
    ref_images, ref_audios = scan_game_scripts_for_assets()
    print(f"Referenced Images in code: {len(ref_images)}")
    print(f"Referenced Audios in code: {len(ref_audios)}")
    
    print("\n=== Checking for Physical Files on Disk ===")
    missing_physical_images = []
    for img_id, rel_path in manifest_images.items():
        abs_path = GAME_DIR / rel_path
        if not abs_path.exists():
            missing_physical_images.append((img_id, rel_path))
            
    missing_physical_audios = []
    for alias, rel_path in manifest_audios.items():
        abs_path = GAME_DIR / rel_path
        if not abs_path.exists():
            missing_physical_audios.append((alias, rel_path))
            
    print(f"Missing physical images declared in manifest: {len(missing_physical_images)}")
    for img_id, rel in missing_physical_images:
        print(f"  - '{img_id}' -> '{rel}' (DOES NOT EXIST ON DISK)")
        
    print(f"Missing physical audios declared in manifest: {len(missing_physical_audios)}")
    for alias, rel in missing_physical_audios:
        print(f"  - '{alias}' -> '{rel}' (DOES NOT EXIST ON DISK)")
        
    print("\n=== Checking for Referenced Images Missing in Manifest ===")
    unmanifested_images = []
    for img in sorted(ref_images):
        # Allow transition helpers, expressions, or known build-ins
        if img in {"fade", "dissolve", "hpunch", "vpunch", "vpunch_low", "flash", "black"}:
            continue
        if img not in manifest_images:
            unmanifested_images.append(img)
            
    print(f"Images used in game scripts but not in assets_manifest.rpy: {len(unmanifested_images)}")
    for img in unmanifested_images:
        print(f"  - '{img}'")
        
    print("\n=== Checking for Referenced Audios Missing in Manifest ===")
    unmanifested_audios = []
    
    # Let's find all audio_ variables in assets_manifest.rpy
    manifest_text = MANIFEST_PATH.read_text(encoding="utf-8")
    manifest_audio_vars = set(re.findall(r'\b(audio_[a-zA-Z0-9_]+)\b', manifest_text))
    
    for aud in sorted(ref_audios):
        # If it's a standard alias (like "themes/savoy_tension") or variable name (like "audio_themes_savoy_tension")
        if aud in manifest_audios or aud in manifest_audio_vars:
            continue
        # Also skip if it is a common built-in or keyword
        if aud in {"music", "sound", "audio", "voice", "None", "False", "True"}:
            continue
        unmanifested_audios.append(aud)
        
    print(f"Audios used in game scripts but not in assets_manifest.rpy: {len(unmanifested_audios)}")
    for aud in unmanifested_audios:
        print(f"  - '{aud}'")

    print("\n=== Checking for Unused Declarations (In Manifest but not in game scripts) ===")
    unused_images = []
    for img in sorted(manifest_images.keys()):
        # Check if the tag is used, or the full name is used
        tag = img.split()[0]
        used = False
        for ref in ref_images:
            if ref == img or ref.split()[0] == tag:
                used = True
                break
        if not used:
            unused_images.append(img)
            
    print(f"Images in manifest but never referenced (or tag never shown) in game scripts: {len(unused_images)}")
    for img in unused_images:
        print(f"  - '{img}'")
        
    unused_audios = []
    for alias in sorted(manifest_audios.keys()):
        var_name = "audio_" + alias.replace("/", "_")
        if alias not in ref_audios and var_name not in ref_audios:
            unused_audios.append(alias)
            
    print(f"Audios in manifest but never referenced in game scripts: {len(unused_audios)}")
    for aud in unused_audios:
        print(f"  - '{aud}'")

if __name__ == "__main__":
    check_sync()
