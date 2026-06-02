# ==========================================================
# book1_non_canon.rpy
# First-pass modular NVL artifact for writing events.
# ==========================================================

init python:
    BOOK1_CAST = {
        "cora": "Coralie Vale",
        "gideon": "Lord Caldor",
        "vance": "Lady Vayne",
        "stern": "Mr. Sterick",
        "missy": "Miri",
    }

    BOOK1_THEME_BUCKETS = {
        "ghost": (
            "day1_corridor_state=ghost",
            "day2_tea_choice=ghost",
            "day3_brush_choice=ghost",
            "day5_dynamic=witness",
        ),
        "predator": (
            "day1_corridor_state=predator",
            "day2_tea_choice=predator",
            "day3_brush_choice=predator",
            "day3_ultimatum=defied",
            "day5_dynamic=adversary",
        ),
        "prey": (
            "day1_corridor_state=prey",
            "day2_tea_choice=prey",
            "day3_brush_choice=prey",
            "day3_ultimatum=surrendered",
            "day5_dynamic=protege",
        ),
    }

    BOOK1_FLAVOR_GROUPS = {
        "ghost": (
            ("ledger_whispers", ("day1_ledger_focus=inspiration", "day3_twilight_action=prepare_mask")),
            ("witness_debt", ("day2_tea_choice=ghost", "day4_escape_state=missy_cover", "missy_day4_used_as_cover=true")),
            ("cold_strategy", ("day5_dynamic=witness", "day3_ultimatum=bargained")),
        ),
        "predator": (
            ("silk_knife", ("day1_ledger_focus=corruption", "day2_contraband_state=stolen_wearing")),
            ("refusal_game", ("day3_ultimatum=defied", "day3_brush_choice=predator")),
            ("public_mask", ("day4_escape_state=bold_lie", "day5_dynamic=adversary")),
        ),
        "prey": (
            ("dangerous_invitation", ("day1_corridor_state=prey", "day3_brush_choice=prey")),
            ("obedient_fire", ("day3_ultimatum=surrendered", "day4_night_action=finish_manuscript")),
            ("careful_confession", ("day2_tea_choice=prey", "day5_dynamic=protege")),
        ),
    }

    BOOK1_DECISION_GROUPS = {
        "missy_debt": (
            "day2_tea_choice=ghost",
            "day4_escape_state=missy_cover",
            "missy_day4_used_as_cover=true",
            "missy_day2_trust_break=true",
        ),
        "ultimatum_hardline": (
            "day3_ultimatum=defied",
            "day3_ultimatum=surrendered",
        ),
        "writing_drive": (
            "day3_twilight_action=frantic_write",
            "day4_night_action=finish_manuscript",
            "release1_manuscript_completed=true",
        ),
    }

    BOOK1_DECISION_BLOCKS = {
        "missy_debt": {
            "left": (
                "Miri is written as a courier who trusted the wrong corridor map, and Coralie keeps the betrayal visible.",
                "The scene does not absolve her; it records the debt like a stain that cannot be laundered out.",
            ),
            "right": (
                "Miri becomes a distant apprentice, cautious but present, and Coralie writes her with earned restraint.",
                "The page allows partial repair, but never pretends innocence returned unchanged.",
            ),
        },
        "ultimatum_hardline": {
            "left": (
                "Lord Caldor corners the heroine by the furnace doors, offering terms in a velvet voice.",
                "She answers with refusal sharpened into etiquette, making defiance feel like a ceremonial blade.",
            ),
            "right": (
                "Lord Caldor still corners her, but this time consent is staged as survival arithmetic.",
                "The chapter acknowledges how surrender can be chosen and still feel perilously close to coercion.",
            ),
        },
        "writing_drive": {
            "left": (
                "Coralie writes as if dawn will confiscate the pages, every paragraph urgent and thin-breathed.",
                "The prose runs hot with pursuit, turning fear into velocity.",
            ),
            "right": (
                "Coralie writes slowly, pressing each sentence into structure before allowing heat to bloom.",
                "The prose keeps its pulse but favors control over panic.",
            ),
        },
    }

    BOOK1_CHAPTER_STUBS = {
        "day1_chapter": {
            "title": "Chapter I - The Conservatory Door",
            "day_id": 101,
            "base": (
                "At Ravenshade Conservatory, Coralie Vale learns that service is theater and every corridor has an audience.",
                "She studies Lady Vayne's posture, Mr. Sterick's clipped authority, and the predatory stillness of Lord Caldor.",
                "The scandal behind the music room door becomes her first private map of power.",
            ),
            "decision_blocks": ("ultimatum_hardline",),
        },
        "day2_chapter": {
            "title": "Chapter II - The Hatbox Oath",
            "day_id": 102,
            "base": (
                "A sealed hatbox, a trembling accomplice, and a tea service become leverage in another house where rank is polished like silver.",
                "Coralie rewrites the hotel's suite politics into a conservatory salon where reputations are traded as quietly as sugar tongs.",
                "She discovers that one clean lie can furnish an entire room.",
            ),
            "decision_blocks": ("missy_debt",),
        },
        "day3_chapter": {
            "title": "Chapter III - Furnace Parlour",
            "day_id": 103,
            "base": (
                "By twilight rehearsal, Lord Caldor's attention feels less like patronage and more like choreography.",
                "Coralie stages mirror, brush, and breath as evidence, knowing witnesses can become accomplices by standing still.",
                "Every line she writes asks whether danger is a place, a person, or a desire she cannot dismiss.",
            ),
            "decision_blocks": ("ultimatum_hardline", "writing_drive"),
        },
        "day4_triumphant_chapter": {
            "title": "Chapter IV - The Sealed Envelope",
            "day_id": 104,
            "base": (
                "A hidden photograph becomes a coded sketch in the conservatory ledger, enough to threaten a lord without naming him.",
                "Coralie drafts a false victory in which the heroine traps her patron using impeccable manners and one precise secret.",
                "The chapter glows with triumph while quietly admitting the danger is merely sleeping.",
            ),
            "decision_blocks": ("missy_debt", "writing_drive"),
        },
        "day5_reckoning_chapter": {
            "title": "Chapter V - Diagnosis At Dawn",
            "day_id": 105,
            "base": (
                "On her final night in this volume, Coralie revises the ending from triumph to diagnosis.",
                "Lord Caldor is no longer a singular monster but the face of a machine that rewards silence and punishes witnesses.",
                "She keeps the physical silhouettes intact - his controlled stillness, Lady Vayne's lacquered poise, Mr. Sterick's iron posture, Miri's fragile readiness - while changing names and setting.",
            ),
            "decision_blocks": ("missy_debt", "ultimatum_hardline", "writing_drive"),
        },
    }

    def _book1_flag_equals(flag_expr):
        key, expected = flag_expr.split("=", 1)
        current = getattr(story, key, None)
        if expected == "true":
            return bool(current) is True
        if expected == "false":
            return bool(current) is False
        return current == expected

    def _book1_resolve_theme():
        theme_scores = {"ghost": 0, "predator": 0, "prey": 0}
        for theme_name, checks in BOOK1_THEME_BUCKETS.items():
            for check in checks:
                if _book1_flag_equals(check):
                    theme_scores[theme_name] += 1
        return max(theme_scores, key=theme_scores.get)

    def _book1_resolve_flavor(theme_name):
        default_flavor = "baseline"
        best_flavor = default_flavor
        best_score = 0
        for flavor_name, checks in BOOK1_FLAVOR_GROUPS.get(theme_name, ()):
            score = 0
            for check in checks:
                if _book1_flag_equals(check):
                    score += 1
            if score > best_score:
                best_score = score
                best_flavor = flavor_name
        return best_flavor

    def _book1_pick_decision_variant(group_name):
        checks = BOOK1_DECISION_GROUPS.get(group_name, ())
        for check in checks:
            if _book1_flag_equals(check):
                return "left"
        return "right"

    def build_book1_chapter_packet(chapter_key):
        chapter_stub = BOOK1_CHAPTER_STUBS.get(chapter_key, BOOK1_CHAPTER_STUBS["day1_chapter"])
        theme_name = _book1_resolve_theme()
        flavor_name = _book1_resolve_flavor(theme_name)

        lines = []
        lines.append(chapter_stub["title"])
        lines.append("Narrator: Coralie Vale recasts the Savoy into Ravenshade Conservatory.")
        lines.append("Theme profile: {} | flavor bucket: {}".format(theme_name, flavor_name))
        lines.extend(chapter_stub["base"])

        if theme_name == "ghost":
            lines.append("In this pass she writes like a witness in candlelight: detached voice, precise detail, no claim of innocence.")
        elif theme_name == "predator":
            lines.append("In this pass she writes with strategic heat: the heroine arranges people before they can arrange her.")
        else:
            lines.append("In this pass she writes from perilous attraction: consent, fear, and ambition remain intentionally entangled.")

        if flavor_name == "ledger_whispers":
            lines.append("Flavor note: ledger whispers; each chapter tracks who paid the cost rather than who won the room.")
        elif flavor_name == "witness_debt":
            lines.append("Flavor note: witness debt; side characters retain moral weight instead of dissolving into symbols.")
        elif flavor_name == "cold_strategy":
            lines.append("Flavor note: cold strategy; she advances by understatement and lets others speak into traps.")
        elif flavor_name == "silk_knife":
            lines.append("Flavor note: silk knife; polished etiquette carries a visible edge.")
        elif flavor_name == "refusal_game":
            lines.append("Flavor note: refusal game; boundaries are negotiated with deliberate friction.")
        elif flavor_name == "public_mask":
            lines.append("Flavor note: public mask; reputation is weaponized in social daylight.")
        elif flavor_name == "dangerous_invitation":
            lines.append("Flavor note: dangerous invitation; curiosity is framed as both hunger and hazard.")
        elif flavor_name == "obedient_fire":
            lines.append("Flavor note: obedient fire; outward compliance shelters inward escalation.")
        elif flavor_name == "careful_confession":
            lines.append("Flavor note: careful confession; controlled honesty replaces spectacle.")

        for decision_group in chapter_stub["decision_blocks"]:
            variant = _book1_pick_decision_variant(decision_group)
            lines.extend(BOOK1_DECISION_BLOCKS[decision_group][variant])

        lines.append("Closing line: the chapter remains a first pass, modular by design, and ready for revision in future writing events.")
        return lines


label book1_write_chapter(chapter_key="day1_chapter", current_day=101):
    $ _book1_lines = build_book1_chapter_packet(chapter_key)
    nvl clear
    for _line in _book1_lines:
        nvl_narrator "[_line]"
    nvl clear
    return
