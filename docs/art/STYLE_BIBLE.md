# Savoy Hotel Visual Style Bible

This document locks in the visual language, core styling parameters, and aesthetic boundaries for all generated sprites, backgrounds, UI screens, and CG illustrations.

---

## 🎨 Core Aesthetic Anchors

Visual assets must strictly adhere to the following stylistic anchors:

*   **Soft Period-Anime Elegance (Violet Evergarden-adjacent)**: Delicate, flowing hair strands, elegant silhouettes, high detail density on key historical clothing folds.
*   **Grounded Facial Structures (Western-Animation-adjacent)**: Expressive but realistically proportioned features; avoid oversized glossy eyes, exaggerated facial expressions, or nose-less designs.
*   **Linework & Shading**:
    *   Clean, thin, confident charcoal or dark ink linework.
    *   Soft, painterly cel-shading combined with subtle watercolor gradients for ambient shadow falloffs.
*   **Eyes**: Restrained, deep, luminous eyes capturing interior intelligence rather than massive, glassy doll eyes.
*   **Color Palettes**: Curated, desaturated, harmonious HSL tailored colors. Avoid raw saturated primes (pure primary red, green, blue). Sprites should use a rich but natural, warm under-layer palette.

---

## ❌ Style Violations to Avoid

Reject any image generation or draft crop exhibiting these characteristics:

*   **3D Render / CGI Look**: Plastic-looking skin surfaces, generic round volumetric lighting, or artificial specular highlights on eyes and skin.
*   **Photorealism**: Overly dense texture maps that create visual noise and disrupt the hand-drawn anime aesthetic.
*   **Chibi or Moe Proportions**: Skewed head-to-body ratios, overly simplified outfits, or hyper-infantile features.
*   **Generic Modern Anime**: Modern hairstyles, blocky cel-shading, or massive neon-colored eyes.
*   **Harsh Outlines**: Thick, heavy comic-book lines or completely black silhouette seals.

---

## 🎭 Sprite Style Parameters

Sprites represent full-height character configurations placed onto the visual novel canvas:

*   **Generation Canvas**: Render sprites against a solid, neutral gray (`#808080`) background. This makes sprite masking, clean slicing, and edge-blending far simpler.
*   **Posture**: Upright, historically accurate Victorian posture reflecting societal standing. Chambermaids project reserved alertness; aristocrats project dominant, relaxed posture.
*   **Expressions**: Subtle, layered, psychologically consistent facial states (composed, guarded, cold, shocked, naive) rather than generic exaggerated cartoon smiles.

---

## 🖼️ Background Style Parameters

Backgrounds sit behind dialogue boxes and character sprites, framing the dramatic space:

*   **Painterly Depth**: Richly painted rooms with strong vertical perspective lines. Trim, molding, repeated Victorian doors, and patterned wallpaper provide atmospheric weight.
*   **Focal Separation**: Softly diffuse or slightly blur background elements that are far back or in the immediate foreground, keeping the middle ground (where sprites sit) sharp and clear.
*   **Dialogue Clarity**: Darken or desaturate the lower third of the canvas (where dialogue boxes overlay) to ensure maximum font readability at runtime.

---

## 👔 1891 London Costume & Setting Guidelines

All visual designs must respect the historical bounds of **late Victorian (1891) London**:

*   **Cora Hartley**: Simple domestic chambermaid uniform. Deep charcoal or slate gray dress made of heavy wool or cotton, a starched white collar buttoned high at the throat, a crisp white maid's cap, and a heavy white starched utility apron.
*   **Sir Gideon Locke**: Exquisite tailoring reflecting extreme wealth. Double-breasted dark wool suits, satin waistcoat lapels, a meticulously knotted dark cravat, and structural wing-collar shirts.
*   **Ms. Stern**: Rigid, severe housekeeper attire. Black buttoned high-neck dress, silver belt keys hanging from the waist, hair pulled back into a flawless, severe bun. No lace, no decoration.
*   **Vance**: Elegant but desaturated, slightly dated high-society evening gowns. Dark violet velvet, silk accents, rich folds but suggesting confinement or loss of personal freedom.
*   **Missy**: Plain, slightly ill-fitting junior maid outfit. Starch apron, soft white cap, simple cotton dress in desaturated blue or brown.
*   **The Savoy Hotel**: Late Victorian opulence meeting modern utility. Warm gaslight glows, polished brass brackets, dark mahogany woodwork, patterned carpets, and repeated paneled doors.
