#!/usr/bin/env python3
"""Promote new assets from non-prod to prod and remove them from non-prod."""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
non_prod_img_dir = ROOT / "main-game" / "non-prod-game" / "game" / "images"
prod_img_dir = ROOT / "main-game" / "prod-game" / "game" / "images"

def promote_images():
    if not non_prod_img_dir.exists():
        print("Non-production images directory does not exist. Nothing to promote.")
        return
        
    moved = []
    for root, _, files in os.walk(non_prod_img_dir):
        for file in files:
            src_path = Path(root) / file
            rel_path = src_path.relative_to(non_prod_img_dir)
            dest_path = prod_img_dir / rel_path
            
            # Ensure target directories exist
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move the file
            print(f"Moving: {rel_path} -> prod-game/game/images/{rel_path}")
            shutil.move(str(src_path), str(dest_path))
            moved.append(rel_path)
            
    # Clean up empty directories in non-prod
    clean_empty_dirs(non_prod_img_dir)
    
    if not moved:
        print("No new images to promote in non-prod-game/game/images.")
    else:
        print(f"Successfully promoted {len(moved)} images.")

def clean_empty_dirs(path: Path):
    if not path.exists():
        return
    for root, dirs, files in os.walk(path, topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            try:
                # This will only delete if directory is empty
                dir_path.rmdir()
            except OSError:
                pass

if __name__ == "__main__":
    promote_images()
