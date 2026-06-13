from pathlib import Path
from PIL import Image

SRC_DIR = Path("game/images/backgrounds/backgrounds_src")
DST_DIR = Path("game/images/backgrounds")

TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
OUTPUT_FORMAT = "WEBP"
QUALITY = 90

VALID_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def fit_inside(width, height, max_w, max_h):
    ratio = min(max_w / width, max_h / height)
    new_w = max(1, int(width * ratio))
    new_h = max(1, int(height * ratio))
    return new_w, new_h


def resize_image(src_path: Path, dst_path: Path) -> None:
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(src_path) as im:
        original_mode = im.mode

        if original_mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
        else:
            im = im.convert("RGB")

        new_size = fit_inside(im.width, im.height, TARGET_WIDTH, TARGET_HEIGHT)
        resized = im.resize(new_size, Image.Resampling.LANCZOS)

        dst_file = dst_path.with_suffix(f".{OUTPUT_FORMAT.lower()}")
        fmt = OUTPUT_FORMAT.upper()

        save_kwargs = {}
        if fmt in ("JPG", "JPEG"):
            if resized.mode != "RGB":
                resized = resized.convert("RGB")
            save_kwargs = {"quality": QUALITY, "optimize": True, "progressive": True}
        elif fmt == "WEBP":
            save_kwargs = {"quality": QUALITY, "method": 6}
        elif fmt == "PNG":
            save_kwargs = {"optimize": True}

        resized.save(dst_file, fmt, **save_kwargs)
        print(f"{src_path.name}: {im.width}x{im.height} -> {resized.width}x{resized.height}")


def main():
    if not SRC_DIR.exists():
        print(f"Missing source folder: {SRC_DIR.resolve()}")
        return

    for src in SRC_DIR.rglob("*"):
        if src.is_file() and src.suffix.lower() in VALID_EXTS:
            rel = src.relative_to(SRC_DIR)
            dst = DST_DIR / rel
            resize_image(src, dst)


if __name__ == "__main__":
    main()