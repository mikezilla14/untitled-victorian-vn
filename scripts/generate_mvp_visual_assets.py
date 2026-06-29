#!/usr/bin/env python3
"""Generate MVP UI book-plate and manuscript CG placeholder art on disk.

Produces assets declared in assets_manifest.rpy at correct dimensions.
Interim art for ship pass — replace with bespoke illustrations when ready.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ENGINES = (
    ROOT / "main-game" / "prod-game" / "game",
    ROOT / "main-game" / "non-prod-game" / "game",
)

BOOK_SIZE = (748, 600)
CG_SIZE = (1920, 1080)
BOOK_TABLEAU_SIZE = (748, 600)


def _load_bg(engine: Path, rel: str) -> Image.Image | None:
    path = engine / rel
    if path.exists():
        return Image.open(path).convert("RGB")
    return None


def _paper_texture(size: tuple[int, int]) -> Image.Image:
    base = Image.new("RGB", size, (232, 218, 190))
    pixels = base.load()
    rng = random.Random(42)
    for y in range(size[1]):
        for x in range(size[0]):
            noise = rng.randint(-8, 8)
            r, g, b = pixels[x, y]
            pixels[x, y] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise)),
            )
    return base.filter(ImageFilter.GaussianBlur(0.4))


def _hatch_overlay(size: tuple[int, int]) -> Image.Image:
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    step = 14
    for i in range(-size[1], size[0] + size[1], step):
        draw.line([(i, 0), (i + size[1], size[1])], fill=(40, 30, 20, 28), width=1)
    for i in range(-size[1], size[0] + size[1], step * 2):
        draw.line([(i + size[1], 0), (i, size[1])], fill=(40, 30, 20, 18), width=1)
    return img


def _border_plate(size: tuple[int, int]) -> Image.Image:
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    margin = 18
    draw.rectangle(
        [margin, margin, size[0] - margin, size[1] - margin],
        outline=(58, 38, 22, 255),
        width=4,
    )
    draw.rectangle(
        [margin + 8, margin + 8, size[0] - margin - 8, size[1] - margin - 8],
        outline=(120, 90, 55, 180),
        width=2,
    )
    return img


def _resize_cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageEnhance.Color(img).enhance(0.85).resize(size, Image.Resampling.LANCZOS)


def _compose_cg(engine: Path, bg_rel: str, size: tuple[int, int], vignette: float = 0.55) -> Image.Image:
    bg = _load_bg(engine, bg_rel)
    if bg is None:
        canvas = Image.new("RGB", size, (35, 28, 22))
    else:
        canvas = _resize_cover(bg, size)
    overlay = Image.new("RGBA", size, (20, 12, 8, int(255 * vignette)))
    canvas = canvas.convert("RGBA")
    canvas = Image.alpha_composite(canvas, overlay)
    return canvas.convert("RGB")


def _photograph_cg(engine: Path, burning: bool = False) -> Image.Image:
    size = CG_SIZE
    base = _compose_cg(engine, "images/backgrounds/bg_master_suite_tea.webp", size, 0.45)
    draw = ImageDraw.Draw(base)
    # Sepia "card" centre
    cx, cy = size[0] // 2, size[1] // 2
    w, h = 520, 680
    rect = [cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2]
    draw.rectangle(rect, fill=(139, 115, 85))
    draw.rectangle([rect[0] + 8, rect[1] + 8, rect[2] - 8, rect[3] - 8], fill=(90, 75, 58))
    draw.text((rect[0] + 24, rect[1] + 24), "G. Locke", fill=(210, 195, 170))
    if burning:
        for i in range(12):
            draw.polygon(
                [
                    (cx - 40 + i * 8, cy + h // 2 - 20),
                    (cx - 20 + i * 8, cy + h // 2 - 80 - i * 6),
                    (cx + i * 8, cy + h // 2 - 20),
                ],
                fill=(200, 80 + i * 8, 20),
            )
    return base


def generate_for_engine(engine: Path) -> list[str]:
    written: list[str] = []
    ui_book = engine / "images" / "ui" / "book"
    cgs = engine / "images" / "cgs"
    cgs_book1 = cgs / "book1"
    ui_book.mkdir(parents=True, exist_ok=True)
    cgs.mkdir(parents=True, exist_ok=True)
    cgs_book1.mkdir(parents=True, exist_ok=True)

    assets: list[tuple[Path, Image.Image]] = [
        (ui_book / "book_blank.png", _paper_texture(BOOK_SIZE)),
        (ui_book / "plate_paper_overlay.png", _paper_texture(BOOK_SIZE).convert("RGBA")),
        (ui_book / "plate_hatch_overlay.png", _hatch_overlay(BOOK_SIZE)),
        (engine / "images" / "ui" / "book" / "illustration_border_plate.png", _border_plate(BOOK_SIZE)),
        (
            cgs / "cg_manuscript_retelling_d1_corridor.png",
            _compose_cg(engine, "images/backgrounds/bg_savoy_corridor_morning.webp", BOOK_TABLEAU_SIZE, 0.35),
        ),
        (
            cgs / "cg_manuscript_retelling_d4_false_dawn.png",
            _compose_cg(engine, "images/backgrounds/bg_master_suite_night.webp", BOOK_TABLEAU_SIZE, 0.4),
        ),
        (cgs_book1 / "cg_book_d2_hatbox_tableau.png", _compose_cg(engine, "images/backgrounds/bg_master_suite_day.webp", BOOK_TABLEAU_SIZE, 0.3)),
        (cgs / "cg_gideon_photograph.png", _photograph_cg(engine, burning=False)),
        (cgs / "cg_photograph_burning.png", _photograph_cg(engine, burning=True)),
        (
            cgs / "cg_manuscript_retelling_d2_lace.png",
            _compose_cg(engine, "images/backgrounds/bg_master_suite_day.webp", BOOK_TABLEAU_SIZE, 0.32),
        ),
        (
            cgs / "cg_manuscript_retelling_d3_brush.png",
            _compose_cg(engine, "images/backgrounds/bg_master_suite_tea.webp", BOOK_TABLEAU_SIZE, 0.32),
        ),
    ]

    for path, img in assets:
        path.parent.mkdir(parents=True, exist_ok=True)
        if img.mode == "RGBA" and path.suffix.lower() == ".png":
            img.save(path, "PNG")
        else:
            img.convert("RGB").save(path, "PNG")
        written.append(str(path.relative_to(ROOT)))

    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", choices=("prod", "non-prod", "both"), default="both")
    args = parser.parse_args()

    targets: list[Path] = []
    if args.engine in ("prod", "both"):
        targets.append(ROOT / "main-game" / "prod-game" / "game")
    if args.engine in ("non-prod", "both"):
        targets.append(ROOT / "main-game" / "non-prod-game" / "game")

    for engine in targets:
        files = generate_for_engine(engine)
        print(f"Generated {len(files)} assets under {engine.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
