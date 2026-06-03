# Spec: Book Writing Styling & Layout

## Purpose

Define the visual layout, coordinates, styling guidelines, and asset declarations for the book writing feature. This feature displays in-game chapter manuscript text in NVL mode on the left side of the screen, while showing book cover/illustrations and a horizontal stats HUD on the right side.

---

## 🎨 Visual Concept: Penny Dreadful Sensibilities

The screen is designed to capture the intimate, tactile feeling of Cora physically writing her manuscript pages at her desk during the night. 

1. **Left Panel (The Manuscript Page)**: A textured, aged writing paper (cream-toned parchment with deckled edges, subtle ink bleeds, and notice wear) where the chapter text reveals itself word-by-word in a clean, compact serif simulating cheap paper printing.
2. **Right Panel (The Cover & Illustration)**: Inspired directly by 19th-century penny dreadfuls and sensational serialization wrappers (e.g., *Varney the Vampire*, *Spring-Heeled Jack*).
   - **Cover Structure**: Stacked, blocky titles, central framed woodcut engraving, a diegetic price badge ("Price One Penny"), and publisher footer.
   - **Horizontal Stats HUD (Lower 20%)**: A horizontal version of the UI overlay displaying Cora's current psychological/moral state (Cora portrait, Inkwell inspiration, Corruption level, and Anxiety level).

---

## 📐 Layout & Dimensions (1920 × 1080 px Canvas)

```
+─────────────────────────────────────────┬─────────────────────────────────────────+
│                                         │                                         │
│  [LEFT SIDE: WRITING AREA]              │  [RIGHT SIDE: PENNY DREADFUL COVER]     │
│  X: 0 to 960 (Width: 960)               │  X: 960 to 1920 (Width: 960)            │
│                                         │                                         │
│  ┌───────────────────────────────────┐  │  ┌───────────────────────────────────┐  │
│  │                                   │  │  │  [BOOK TITLE BLOCK]               │  │
│  │  Parchment Paper Texture           │  │  │  "Coralie Vale; or, The..."       │  │
│  │  (ui_book_writing_paper)           │  │  ├───────────────────────────────────┤  │
│  │                                   │  │  │                                   │  │
│  │  - Left-aligned text margin       │  │  │  Woodcut Illustration Panel       │  │
│  │  - Compact serif body text        │  │  │  (High-contrast Engraving)       │  │
│  │  - Multiplied distress layers     │  │  │  X: 1056 to 1824                  │  │
│  │                                   │  │  │  Y: 200 to 760 (Height: 560)      │  │
│  │                                   │  │  │                                   │  │
│  │                                   │  │  ├───────────────────────────────────┤  │
│  │                                   │  │  │  [PRICE BLOCK]  [PUBLISHER SLUG]  │  │
│  │                                   │  │  └───────────────────────────────────┘  │
│  │                                   │  │  ┌───────────────────────────────────┐  │
│  │                                   │  │  │  Horizontal Stats HUD             │  │
│  │                                   │  │  │  [Portrait] [Ink] [Corrupt] [Anx] │  │
│  │                                   │  │  │  Height: 160px                    │  │
│  └───────────────────────────────────┘  │  └───────────────────────────────────┘  │
│                                         │                                         │
+─────────────────────────────────────────┴─────────────────────────────────────────+
```

### Coordinates Table

| Element | X Position | Y Position | Width | Height | Description / Constraints |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Left Writing Paper** | `0` | `0` | `960` | `1080` | Parchment paper texture background. |
| **Writing Margins** | `100` | `100` | `760` | `880` | Padded bounds for text rendering. |
| **Right Side Container** | `960` | `0` | `960` | `1080` | Parent container for art and stats. |
| **Cover Title Block** | `1056` | `40` | `768` | `140` | Stacked text container for title + subtitle. |
| **Illustration Box** | `1056` | `200` | `768` | `560` | Woodcut illustration framed by simple border rules (50% vertical space). |
| **Price / Publisher Footer**| `1056` | `780` | `768` | `60` | Decorative scroll/cartouche containing price slug. |
| **Horizontal HUD Bar** | `1056` | `860` | `768` | `160` | Horizontal stats panel container. |
| **HUD: Cora Portrait** | `1076` | `880` | `120` | `120` | Circular cropped portrait of Cora. |
| **HUD: Inkwell Icon** | `1216` | `885` | `60` | `110` | Re-scaled vertical inkwell vessel display. |
| **HUD: Stats Area** | `1296` | `880` | `500` | `120` | Split horizontal meters for Corruption & Anxiety. |

---

## 🎨 Aesthetic Guidelines

### Typography & Ink
* **Title Font (Masthead)**: A heavy Victorian display serif (e.g., *Playfair Display Black* or custom flared slab-serif) with high contrast and tight leading. Titles should use stacked structures or arched styling.
* **Subtitle Font**: A slab‑serif or condensed serif (e.g., *Courier Prime* or condensed sans-serif) to display subtitles like `"or, The Feast of Blood"` or chapter subdivisions.
* **Body/Chapter Font**: A plain, compact book serif (e.g., *IM Fell English* or *EB Garamond*) set in dense, clean blocks to mimic 19th-century cheap presswork.
* **Ink Color**: Warm dark sepia (`#2c1b17`) or Charcoal‑black (`#1f1f1f`) to reflect ink-press printing, avoiding flat modern digital black.

### Texture, Color & Distressing
* **Color Palette**: Desaturated and limited. Spot red or dark blue accents can be used for pricing banners, but the primary interface uses charcoal inks, warm parchment creams, and wood sepia.
* **Distress Overlays**: The book page and cover wrapper feature subtle edge wear, corner creases, uneven inking (heavy on page margins), and minor foxing.
* **Framing Rules**: The illustration panel must be enclosed within simple double-line rules with modest corner ornaments (Victorian brackets).

### Art Direction for Illustrations
* **Style**: High-contrast, scratchboard‑like woodcut engraving or etching illustrations (simulating low-cost print blocks).
* **Prompts**: AI generation prompts should include keywords: *"Victorian woodcut engraving, dense crosshatching, etching, low-color, high contrast, ink-blocked, 1891 penny dreadful illustration"*.

---

## 📦 Asset Allocation

These assets must be added to the assets manifest files (`renpy_project/game/assets_manifest.rpy` and its non-prod draft duplicate).

```renpy
    # ── UI: Book Writing Screen Assets ───────────────────────────
    #
    # ui_book_writing_paper:
    #   [960 × 1080 px] Full left-side background.
    #   Cream-toned parchment with deckled edges and subtle paper grains.
    declare_image_with_fallback("ui_book_writing_paper", "images/ui/book_writing_paper.webp", "#f4efe2")
    #
    # ui_book_cover:
    #   [768 × 764 px] Default right-side artwork.
    #   Ornate leather-bound Victorian book cover with gilded title design.
    declare_image_with_fallback("ui_book_cover", "images/ui/book_cover.webp", "#3d2314")
    #
    # ui_book_ui_bg:
    #   [768 × 160 px] Panel backing for the horizontal stats HUD.
    #   Polished mahogany or dark walnut desk strip with ornamental brass edges.
    declare_image_with_fallback("ui_book_ui_bg", "images/ui/book_ui_bg.webp", "#1c1410")
    #
    # ui_cora_mini_base:
    #   [120 × 120 px] Mini circular portrait of Cora (Base state, low corruption).
    declare_image_with_fallback("ui_cora_mini_base", "images/ui/ui_cora_mini_base.webp", "#d4a574")
    #
    # ui_cora_mini_corrupted:
    #   [120 × 120 px] Mini circular portrait of Cora (Corrupted state, corruption >= 3).
    declare_image_with_fallback("ui_cora_mini_corrupted", "images/ui/ui_cora_mini_corrupted.webp", "#8b2942")
```

---

## 🛠️ Ren'Py Screen Implementation Blueprint

The layout hierarchy (Title block, Illustration box, Price Footer, HUD) is rendered using Ren'Py's screen language.

```renpy
# Dedicated screen to handle the Book Writing UI layout
screen book_writing_nvl(dialogue, items=None):
    # Left side: Manuscript Paper
    add "ui_book_writing_paper" xpos 0 ypos 0

    # Right side Panel Wrapper
    frame:
        xpos 960
        ypos 0
        width 960
        height 1080
        background None
        padding (0, 0)

        # 1. Tall Title Block (Stacked Penny Dreadful Masthead)
        vbox:
            xpos 96
            ypos 40
            width 768
            spacing 2
            
            text "CORALIE VALE;" size 32 font "fonts/DejaVuSerif-Bold.ttf" color "#2c1b17" xalign 0.5
            text "OR," size 18 font "fonts/DejaVuSerif-Italic.ttf" color "#2c1b17" xalign 0.5
            text "THE TERROR OF THE SAVOY CORRIDORS." size 22 font "fonts/DejaVuSerif-Bold.ttf" color "#2c1b17" xalign 0.5

        # 2. Woodcut Illustration Frame (taking up central height space)
        frame:
            xpos 96
            ypos 200
            width 768
            height 560
            background Frame("images/ui/illustration_border.png", 6, 6) # simple double-line rules
            padding (10, 10)
            
            $ page_image = getattr(store, "book1_page_image", "ui_book_cover")
            add page_image xalign 0.5 yalign 0.5

        # 3. Price Banner & Publisher Slug Footer
        frame:
            xpos 96
            ypos 780
            width 768
            height 60
            background None
            
            # Diegetic "Price One Penny" cartouche on the left
            hbox:
                xalign 0.1
                yalign 0.5
                add "images/ui/price_badge.png" # Contains "Price One Penny" text/graphics
            
            # Publisher slug centered at the bottom margin
            text "LONDON: PRINTED AND PUBLISHED BY SIR GIDEON LOCKE, SAVOY STRAND." size 14 font "fonts/DejaVuSans-Condensed.ttf" color "#5f5f5f" xalign 0.5 yalign 0.5

        # 4. Horizontal Stats HUD Bar
        frame:
            xpos 96
            ypos 860
            width 768
            height 160
            background "ui_book_ui_bg"
            padding (20, 20)

            hbox:
                spacing 20
                yalign 0.5

                # Cora Mini Portrait (corruption dependent)
                if player.corruption >= 3:
                    add "ui_cora_mini_corrupted"
                else:
                    add "ui_cora_mini_base"

                # Rescaled Inkwell displaying current inspiration / capacity
                vbox:
                    spacing 5
                    yalign 0.5
                    add "ui_inkwell_empty" xsize 60 ysize 102

                # Split Horizontal Meters
                vbox:
                    spacing 15
                    yalign 0.5
                    width 500

                    # Corruption Meter
                    hbox:
                        spacing 10
                        text "Corruption" size 20 color "#d4a574" width 120
                        bar:
                            value player.corruption
                            range player.corruption_cap
                            xsize 350
                            ysize 20
                            left_bar Frame("images/ui/bar_corruption_fill.png", 5, 5)
                            right_bar Frame("images/ui/bar_empty.png", 5, 5)

                    # Anxiety Meter
                    hbox:
                        spacing 10
                        text "Anxiety" size 20 color "#8b2942" width 120
                        bar:
                            value player.anxiety
                            range 100
                            xsize 350
                            ysize 20
                            left_bar Frame("images/ui/bar_anxiety_fill.png", 5, 5)
                            right_bar Frame("images/ui/bar_empty.png", 5, 5)

    # Manuscript Text Viewport (Left Side padding)
    frame:
        xpos 100
        ypos 100
        width 760
        height 880
        background None
        padding (40, 40)

        has vbox:
            spacing 20

        # Iterate and display NVL dialogue text
        for d in dialogue:
            if d.who: # If there's a title/header
                text d.who:
                    font "fonts/DejaVuSerif.ttf"
                    size 36
                    color "#261c14"
                    xalign 0.5
                    bottom_margin 20
            text d.what:
                font "fonts/DejaVuSerif.ttf"
                size 28
                color "#261c14"
                line_spacing 1.4
                justify True
```
