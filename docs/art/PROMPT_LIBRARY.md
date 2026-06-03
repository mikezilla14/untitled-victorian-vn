# Savoy Visual Novel Prompt Library

Use this library of copy/pasteable text prompts and image-to-image templates to maintain style bible alignment.

---

## 🎨 Sprite Style Prompt Wrapper
Append this styling suffix to **every** character sprite prompt to lock in the aesthetic:

```text
--style anime --no 3d render, cg, photorealism, glossy skin, neon eyes, modern clothes, chibi, thick lines
```

---

## 👥 Character Sprite Prompt Templates

### Template 1: Character Sprite from Text
```text
A character sprite sheet of [CHARACTER NAME], late Victorian era. [AGE]-years-old. [HAIR AND EYE DESCRIPTION]. [OUTFIT DESCRIPTION]. Standing pose, front view, [MOOD/EXPRESSION]. Soft anime elegance, Violet Evergarden-adjacent style, clean thin charcoal linework, soft painterly cel-shading, restrained luminous eyes, desaturated harmonious HSL color palette. Rendered on a solid flat neutral gray (#808080) background --style anime --no 3d render, cg, photorealism, glossy skin, neon eyes, modern clothes, chibi, thick lines
```

### Template 2: Sprite Pose/Expression Variant (Image-to-Image)
```text
[URL of approved base sprite] --a sprite variant of the same character. Maintain identical face shape, hair color, and maid attire. Modify expression to [NEW EXPRESSION: guarded/shocked/cold] and shift head angle to [HEAD ANGLE: front/three-quarters]. Clean thin charcoal linework, soft painterly cel-shading, solid neutral gray (#808080) background --style anime --no 3d render, cg, photorealism, glossy skin, neon eyes, modern clothes
```

---

## 🏢 Character Specific Prompt Specifications

### 1. Cora Hartley
*   **Prompt Tokens**: `22-year-old chambermaid, Black Irish heritage, neat dark hair pulled back severely, deep piercing dark eyes, pale porcelain skin, intelligent analytical expression.`
*   **Outfit**: `Charcoal gray Victorian domestic servant dress, buttoned stiff white collar, starched white maid's cap, plain starched white apron.`
*   **Copy/Paste Sprite Prompt**:
    ```text
    A character sprite of Cora Hartley, a 22-year-old chambermaid, Black Irish heritage, neat dark hair pulled back severely, deep piercing dark eyes, pale porcelain skin, intelligent analytical expression. She wears a charcoal gray Victorian domestic servant dress, a buttoned stiff white collar, a starched white maid's cap, and a plain starched white apron. Front view, standing alertly. Soft anime elegance, Violet Evergarden-adjacent style, clean thin charcoal linework, soft painterly cel-shading, desaturated harmonious HSL color palette, solid flat neutral gray (#808080) background --style anime --no 3d render, cg, photorealism, glossy skin, neon eyes, modern clothes, chibi, thick lines
    ```

### 2. Sir Gideon Locke
*   **Prompt Tokens**: `40-year-old aristocratic gentleman, dark hair with elegant graying at the temples, cold sharp hazel eyes, pale skin, commanding posture.`
*   **Outfit**: `Premium double-breasted charcoal wool suit, velvet-lapel satin waistcoat, meticulously tied dark cravat, high wing-collar shirt.`
*   **Copy/Paste Sprite Prompt**:
    ```text
    A character sprite of Sir Gideon Locke, a 40-year-old aristocratic gentleman, dark hair with elegant graying at the temples, cold sharp hazel eyes, pale skin, commanding posture. He is dressed in a premium double-breasted charcoal wool suit, a velvet-lapel satin waistcoat, a meticulously tied dark cravat, and a high wing-collar shirt. Standing relaxed, dominant front view. Soft anime elegance, clean thin charcoal linework, soft painterly cel-shading, solid flat neutral gray (#808080) background --style anime --no 3d render, cg, photorealism, glossy skin, modern clothes
    ```

### 3. Ms. Stern
*   **Prompt Tokens**: `45-year-old severe head housekeeper, silver-black-gray hair pulled back tightly into a flawless bun, icy piercing blue eyes, rigid posture.`
*   **Outfit**: `Severely tailored high-collar black housekeeper dress, silver belt keys hanging from the waist, zero lace or ornamentation.`
*   **Copy/Paste Sprite Prompt**:
    ```text
    A character sprite of Ms. Stern, a 45-year-old severe head housekeeper, silver-black-gray hair pulled back tightly into a flawless bun, icy piercing blue eyes, rigid posture. She wears a severely tailored high-collar black housekeeper dress with silver belt keys hanging from her waist, zero lace or ornamentation. Stern standing posture, front view. Soft anime elegance, clean thin charcoal linework, soft painterly cel-shading, solid flat neutral gray (#808080) background --style anime --no 3d render, cg, photorealism
    ```

### 4. Vance
*   **Prompt Tokens**: `28-year-old high-society companion, dark hair, shadowed terrified eyes, pale desaturated skin, submissive posture.`
*   **Outfit**: `Exquisite but desaturated deep purple velvet evening gown, silk-trimmed corset bodice, delicate lace sleeves.`
*   **Copy/Paste Sprite Prompt**:
    ```text
    A character sprite of Vance, a 28-year-old high-society companion, dark hair, shadowed terrified eyes, pale desaturated skin, submissive posture. She is wearing an exquisite but desaturated deep purple velvet evening gown with a silk-trimmed corset bodice and delicate lace sleeves. Standing submissively, three-quarters view. Soft anime elegance, clean thin charcoal linework, soft painterly cel-shading, solid flat neutral gray (#808080) background --style anime --no 3d render, cg, photorealism
    ```

### 5. Missy
*   **Prompt Tokens**: `18-year-old junior domestic maid, light brown hair, wide naive eyes, rosy blushing cheeks, hesitant innocent expression.`
*   **Outfit**: `Simple desaturated light-blue maid dress, slightly oversized starch apron, soft white cotton cap.`
*   **Copy/Paste Sprite Prompt**:
    ```text
    create A character sprite of Missy, an 22-year-old junior domestic maid, light brown hair, wide naive eyes, rosy blushing cheeks, hesitant innocent expression. She wears a charcoal gray Victorian domestic servant dress, a buttoned stiff white collar, a starched white maid's cap, and a plain starched white apron. Standing hesitantly, front view. Soft anime elegance, clean thin charcoal linework, soft painterly cel-shading, solid flat neutral gray (#808080) background --style anime --no 3d render, cg, photorealism
    ```

---

## 🏢 Background Location Prompt Templates

### Template 3: Background from Text
```text
An environment plate of [LOCATION DESCRIPTION], late Victorian era, 1891 London. Painterly visual novel background style, vertical perspective, rich soft watercolor textures, soft ambient light falling from [LIGHT SOURCE], moody color values, [TIME OF DAY: morning/dusk/candlelight]. Master background style, readable architectural detail, desaturated warm wood tones, no characters --no characters, 3d, photograph, modern machinery
```

### Template 4: Savoy Hotel Servants' Corridor
```text
An environment plate of a Savoy Hotel servant service corridor, 1891 late Victorian era. Moody transitional hallway with dark mahogany wainscoting, cream patterned wallpaper, brass sconce lamps lining the walls, a repeated row of paneled wooden doors recrossing in deep perspective. Soft morning sunlight filtering through a high small window, dusty ambient atmosphere. Painterly visual novel background style, watercolor washes, rich desaturated wood tones, no characters --no characters, 3d, photograph, neon
```

---

## 🎛️ UI and HUD Sprite Prompts

### 1. Cameo Portrait: Cora Base
```text
A framed bust-shot portrait of Cora Hartley, 22-year-old maid, dark hair, pale skin, reserved expression. Soft circular decorative framing borders, desaturated warm tones. Visual novel HUD cameo asset --style anime --no 3d, photorealism
```

### 2. Cameo Portrait: Cora Corrupted
```text
A framed bust-shot portrait of Cora Hartley, 22-year-old maid, dark hair. Her expression is colder, highly analytical, shadows falling across her face. Subtly desaturated, shadow shift. Visual novel HUD cameo asset --style anime --no 3d, photorealism
```

### 3. Suspicion Vignette
```text
A solid black rectangular vignette canvas with an intense, bleeding, hot deep-red and crimson bleeding border frame. Radial gradient framing, dark center, oppressive red haze bleeding inwards from the extreme borders. PNG overlay HUD asset --no 3d, textures
```

### 4. Inkwell Empty & Full
```text
A solid isolated asset of a Victorian writing inkwell on a transparent background.
- Left asset: Empty clear glass inkwell vessel, elegant ceramic rim, hollow translucent center.
- Right asset: Identical glass vessel filled to the high brim with dark thick black calligrapher's ink, light catching the ink surface.
Isolated assets, flat background --no table, background, desk
```

---

## 🖼️ CG Story Illustration Prompt Templates

### Template 5: Narrative CG / Scene Illustration
```text
A story illustration CG of [CHARACTER A] and [CHARACTER B] inside [LOCATION]. [ACTION DESCRIPTION AND INTERACTION: e.g., Character A kneeling before Character B, exchanging a tense look]. Moody dramatic candlelight casting strong shadows. Refined period-anime style, high emotional tension, delicate painterly cel-shading, desaturated color values, deep late-Victorian atmosphere --style anime --no 3d, photo, modern clothes
```

### Template 6: Professional Intimate CG (Narrative Erotic CG)
```text
A highly sensual and intimate story illustration of Cora and [PARTNER] inside the master suite. [NARRATIVE ENCOUNTER DESCRIPTION: e.g., A close shot focusing on their hands intertwining on the silk bed sheets, or a gentle touch on the neck, high romantic tension, clearly adult characters, elegant and desaturated]. Rich soft painterly folds, soft warm candlelight, delicate period-anime visual novel illustration style, emotional weight, beautiful drapery. Professionally framed narrative CG --style anime --no pornographic, explicit nudity, 3d render, photo, modern clothing
```
