#!/usr/bin/env python3
"""Scan game asset files and manifests to generate a daily asset report."""

import os
import re
import sys
import datetime
from pathlib import Path

# Paths relative to this script
ROOT = Path(__file__).resolve().parents[1]
PROD_GAME_DIR = ROOT / "main-game" / "prod-game" / "game"
NON_PROD_GAME_DIR = ROOT / "main-game" / "non-prod-game" / "game"
PROD_MANIFEST_PATH = PROD_GAME_DIR / "assets_manifest.rpy"
NON_PROD_MANIFEST_PATH = NON_PROD_GAME_DIR / "shared" / "assets_manifest.rpy"
OUTPUT_PATH = ROOT / "assets_source" / "approved_assets" / "daily_asset_manifest.md"

def parse_manifest(manifest_path):
    declared_images = []
    declared_audio = []
    
    if not manifest_path.exists():
        print(f"WARNING: Manifest not found at {manifest_path}", file=sys.stderr)
        return [], []
        
    content = manifest_path.read_text(encoding="utf-8")
        
    # Match declare_image_with_fallback
    image_pattern = re.compile(
        r'declare_image_with_fallback\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']\s*(?:,\s*["\'][^"\']+["\'])?\s*\)'
    )
    for match in image_pattern.finditer(content):
        alias, rel_path = match.groups()
        declared_images.append({
            "alias": alias,
            "path": rel_path,
            "line": content[:match.start()].count("\n") + 1
        })
        
    # Match register_audio
    audio_pattern = re.compile(
        r'register_audio\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']\s*\)'
    )
    for match in audio_pattern.finditer(content):
        alias, rel_path = match.groups()
        declared_audio.append({
            "alias": alias,
            "path": rel_path,
            "line": content[:match.start()].count("\n") + 1
        })
        
    return declared_images, declared_audio

def scan_directory_assets(game_dir):
    """Scan the given game directory for image and audio files."""
    found_assets = {}
    valid_exts = {".png", ".webp", ".jpg", ".jpeg", ".ogg", ".mp3", ".wav"}
    
    if not game_dir.exists():
        return found_assets
        
    for root, _, files in os.walk(game_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in valid_exts:
                abs_path = Path(root) / file
                rel_path = abs_path.relative_to(game_dir).as_posix()
                found_assets[rel_path] = abs_path
                
    return found_assets

def generate_report():
    print("Parsing manifests...")
    prod_images, prod_audio = parse_manifest(PROD_MANIFEST_PATH)
    non_prod_images, non_prod_audio = parse_manifest(NON_PROD_MANIFEST_PATH)
    print(f"Parsed Prod: {len(prod_images)} images, {len(prod_audio)} audio")
    print(f"Parsed Non-Prod: {len(non_prod_images)} images, {len(non_prod_audio)} audio")
    
    print("Scanning prod-game assets on disk...")
    prod_assets = scan_directory_assets(PROD_GAME_DIR)
    print(f"Found {len(prod_assets)} assets on disk in prod-game.")
    
    print("Scanning non-prod-game assets on disk...")
    non_prod_assets = scan_directory_assets(NON_PROD_GAME_DIR)
    print(f"Found {len(non_prod_assets)} assets on disk in non-prod-game.")
    
    # Combine declared assets by category/alias to handle union
    declared_by_alias = {}
    
    def add_declarations(images, audio, env_name):
        for item in images:
            path = item["path"]
            alias = item["alias"]
            
            # Categorize
            if path.startswith("images/backgrounds/"):
                cat = "Backgrounds"
            elif path.startswith("images/sprites/") and not "/ui/" in path:
                cat = "Sprites"
            elif path.startswith("images/ui/") or "/ui/" in path:
                cat = "UI"
            elif path.startswith("images/cgs/"):
                cat = "Event Illustrations (CGs)"
            else:
                cat = "Backgrounds" # Default fallback
                
            key = (cat, alias)
            if key not in declared_by_alias:
                declared_by_alias[key] = {
                    "alias": alias,
                    "category": cat,
                    "prod_path": None,
                    "non_prod_path": None,
                    "declared_in_prod": False,
                    "declared_in_non_prod": False,
                }
            if env_name == "prod":
                declared_by_alias[key]["prod_path"] = path
                declared_by_alias[key]["declared_in_prod"] = True
            else:
                declared_by_alias[key]["non_prod_path"] = path
                declared_by_alias[key]["declared_in_non_prod"] = True
                
        for item in audio:
            path = item["path"]
            alias = item["alias"]
            cat = "Audio"
            
            key = (cat, alias)
            if key not in declared_by_alias:
                declared_by_alias[key] = {
                    "alias": alias,
                    "category": cat,
                    "prod_path": None,
                    "non_prod_path": None,
                    "declared_in_prod": False,
                    "declared_in_non_prod": False,
                }
            if env_name == "prod":
                declared_by_alias[key]["prod_path"] = path
                declared_by_alias[key]["declared_in_prod"] = True
            else:
                declared_by_alias[key]["non_prod_path"] = path
                declared_by_alias[key]["declared_in_non_prod"] = True

    add_declarations(prod_images, prod_audio, "prod")
    add_declarations(non_prod_images, non_prod_audio, "non_prod")
    
    # Resolve presence on disk
    for entry in declared_by_alias.values():
        p = entry["prod_path"]
        np = entry["non_prod_path"]
        entry["in_prod"] = (p in prod_assets) if p else False
        entry["in_non_prod"] = (np in non_prod_assets) if np else False
    
    # Categorize combined declared assets
    categorized = {
        "Backgrounds": [],
        "Sprites": [],
        "UI": [],
        "Event Illustrations (CGs)": [],
        "Audio": []
    }
    
    for entry in declared_by_alias.values():
        categorized[entry["category"]].append(entry)

    # Build set of all declared paths to check for undeclared assets
    all_declared_paths = set()
    for entry in declared_by_alias.values():
        if entry["prod_path"]:
            all_declared_paths.add(entry["prod_path"])
        if entry["non_prod_path"]:
            all_declared_paths.add(entry["non_prod_path"])

    undeclared_prod = []
    for rel_path in sorted(prod_assets.keys()):
        if not (rel_path.startswith("images/") or rel_path.startswith("audio/")):
            continue
        if rel_path not in all_declared_paths:
            undeclared_prod.append(rel_path)
            
    undeclared_non_prod = []
    for rel_path in sorted(non_prod_assets.keys()):
        if not (rel_path.startswith("images/") or rel_path.startswith("audio/")):
            continue
        if rel_path not in all_declared_paths:
            undeclared_non_prod.append(rel_path)

    # Helper to format declaration location
    def get_declared_str(entry):
        if entry["declared_in_prod"] and entry["declared_in_non_prod"]:
            return "Both"
        elif entry["declared_in_prod"]:
            return "Prod Only"
        else:
            return "Non-Prod Only"

    def format_paths(entry):
        p = entry["prod_path"]
        np = entry["non_prod_path"]
        if p == np:
            return f"`{p}`"
        elif p and np:
            return f"Prod: `{p}`<br>Non-Prod: `{np}`"
        elif p:
            return f"Prod: `{p}`"
        else:
            return f"Non-Prod: `{np}`"

    # Generate Markdown Report
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        today_str = datetime.date.today().isoformat()
        f.write("# Daily Asset Manifest & Reconciliation Report\n\n")
        f.write(f"**Generated on:** {today_str}\n")
        f.write(f"**Manifest Sources:**\n")
        f.write(f"- Prod Manifest: [assets_manifest.rpy](file:///{PROD_MANIFEST_PATH.as_posix()})\n")
        f.write(f"- Non-Prod Manifest: [assets_manifest.rpy](file:///{NON_PROD_MANIFEST_PATH.as_posix()})\n\n")
        
        # Summary Section
        f.write("## 📊 Summary of Asset Status\n\n")
        f.write("| Category | Declared (Union) | In Place (Prod) | In Place (Non-Prod) | Missing from Engine | Status |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :--- |\n")
        
        total_declared = 0
        total_prod = 0
        total_non_prod = 0
        total_missing = 0
        
        category_rows = []
        for cat in ["Backgrounds", "Sprites", "UI", "Event Illustrations (CGs)", "Audio"]:
            items = categorized[cat]
            dec_count = len(items)
            prod_count = sum(1 for x in items if x["in_prod"])
            non_prod_count = sum(1 for x in items if x["in_non_prod"])
            missing_count = sum(1 for x in items if not x["in_prod"] and not x["in_non_prod"])
            
            total_declared += dec_count
            total_prod += prod_count
            total_non_prod += non_prod_count
            total_missing += missing_count
            
            if missing_count == 0:
                status = "✅ Complete"
            elif prod_count > 0 or non_prod_count > 0:
                status = "⚠️ Partial"
            else:
                status = "❌ Missing"
                
            category_rows.append(f"| {cat} | {dec_count} | {prod_count} | {non_prod_count} | {missing_count} | {status} |")
            
        for row in category_rows:
            f.write(row + "\n")
            
        f.write(f"| **Total** | **{total_declared}** | **{total_prod}** | **{total_non_prod}** | **{total_missing}** | **-** |\n\n")
        
        # Section 1: Assets in Place (Prod / Non-Prod)
        f.write("## 🟢 Assets in Place (Prod / Non-Prod)\n")
        f.write("These assets are declared and present on disk in either production or non-production engine environments.\n\n")
        
        for cat in ["Backgrounds", "Sprites", "UI", "Event Illustrations (CGs)", "Audio"]:
            items = [x for x in categorized[cat] if x["in_prod"] or x["in_non_prod"]]
            items = sorted(items, key=lambda x: x["alias"])
            
            f.write(f"### 🎬 {cat}\n\n")
            if not items:
                f.write("*No assets in place for this category.*\n\n")
                continue
                
            f.write("| Asset Alias / Name | Expected Engine Path | Declared In | Prod | Non-Prod | Status |\n")
            f.write("| :--- | :--- | :---: | :---: | :---: | :--- |\n")
            for item in items:
                prod_status = "🟢 Yes" if item["in_prod"] else "🔴 No" if item["prod_path"] else "-"
                non_prod_status = "🟢 Yes" if item["in_non_prod"] else "🔴 No" if item["non_prod_path"] else "-"
                declared_str = get_declared_str(item)
                paths_str = format_paths(item)
                
                if item["in_prod"] and item["in_non_prod"]:
                    status = "✅ Active (Prod & Non-Prod)"
                elif item["in_prod"]:
                    status = "✅ Active (Prod Only)"
                else:
                    status = "🟡 Active (Non-Prod Only)"
                    
                f.write(f"| `{item['alias']}` | {paths_str} | {declared_str} | {prod_status} | {non_prod_status} | {status} |\n")
            f.write("\n")
            
        # Section 2: Missing Assets
        f.write("## ❌ Missing Assets\n")
        f.write("These assets are declared in the manifest files but are missing from both production and non-production folders. They need to be produced and placed.\n\n")
        
        for cat in ["Backgrounds", "Sprites", "UI", "Event Illustrations (CGs)", "Audio"]:
            items = [x for x in categorized[cat] if not x["in_prod"] and not x["in_non_prod"]]
            items = sorted(items, key=lambda x: x["alias"])
            
            f.write(f"### 🎬 {cat}\n\n")
            if not items:
                f.write("*No missing assets in this category.*\n\n")
                continue
                
            f.write("| Asset Alias / Name | Expected Engine Path | Declared In | Status |\n")
            f.write("| :--- | :--- | :---: | :--- |\n")
            for item in items:
                declared_str = get_declared_str(item)
                paths_str = format_paths(item)
                f.write(f"| `{item['alias']}` | {paths_str} | {declared_str} | ❌ Missing from both |\n")
            f.write("\n")
            
        # Section 3: Undeclared Assets
        f.write("## 🔍 Undeclared Assets on Disk\n")
        f.write("These files exist in the engine folders but are not declared in `assets_manifest.rpy`.\n\n")
        
        f.write("### 📁 Undeclared in Prod (`main-game/prod-game/game/`)\n")
        if undeclared_prod:
            f.write("| File Path | Status |\n")
            f.write("| :--- | :--- |\n")
            for rel in undeclared_prod:
                f.write(f"| `{rel}` | ⚠️ Needs registration or cleanup |\n")
        else:
            f.write("*None found (100% matched).* \n")
        f.write("\n")
        
        f.write("### 📁 Undeclared in Non-Prod (`main-game/non-prod-game/game/`)\n")
        if undeclared_non_prod:
            f.write("| File Path | Status |\n")
            f.write("| :--- | :--- |\n")
            for rel in undeclared_non_prod:
                f.write(f"| `{rel}` | ⚠️ Needs registration or cleanup |\n")
        else:
            f.write("*None found (100% matched).* \n")
        f.write("\n")
        
    print(f"Manifest written successfully to: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_report()
