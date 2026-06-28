# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes
#
# SPRITE DIRECTION (managed by scripts/scene_direction.py — how to preserve manual staging):
# [asset auto]              -> auto-placed sprite line; the agent may rewrite/replace it on re-run
# [asset keep]              -> on a show line: lock THAT line so the agent never edits it
# [asset lock:scene]        -> before/after a `scene`: the agent skips the entire scene block
# [asset pin:Name=slot]     -> force Name into slot for the rest of the scene block
# [enter:Name] / [exit:Name] -> declare cast changes so auto placement stays correct
# Full policy: docs/contracts/sprite_layout_policy.yaml | spec: docs/specs/scene-direction-agent.md

# Narrative Pressure UI, Objective Journal, and Manuscript Readiness System: Core Logic

init python:

    def add_material(material_id):
        """
        Awards a new manuscript material entry to Cora's bank.
        Checks if this enables any writing assignments.
        """
        if material_id not in material_library:
            # Fallback if unknown
            return

        # Copy the static metadata to create a dynamic entry
        material = material_library[material_id].copy()
        material["consumed"] = False
        manuscript_material.append(material)

        add_bundle_item({
            "type": "inspiration",
            "title": "New Material Gained",
            "body": material.get("journal_text", "Cora has found something worth writing."),
            "icon": "quill",
        })

        check_assignment_readiness()


    def spend_focus(amount):
        """
        Consumes focus slots for the current chapter.
        Automatically checks and triggers expiration of opportunities.
        """
        global chapter_focus_remaining
        chapter_focus_remaining = max(0, chapter_focus_remaining - amount)
        
        add_bundle_item({
            "type": "opportunity",
            "title": "Focus Spent",
            "body": f"Used {amount} focus slot(s). {chapter_focus_remaining} remaining.",
            "icon": "hourglass",
        })
        
        check_expiring_opportunities()


    def check_expiring_opportunities():
        """
        Checks if any active optional objectives have faded due to focus loss.
        """
        for obj_id, obj in objectives.items():
            if obj.get("status") != "active":
                continue
            
            expires = obj.get("expires_when", {})
            if not expires:
                continue
            
            # Check chapter mismatch
            if "chapter" in expires and expires["chapter"] != current_chapter_id:
                expire_objective(obj_id)
                continue
            
            # Check focus slot threshold
            if "focus_below" in expires and chapter_focus_remaining < expires["focus_below"]:
                expire_objective(obj_id)
                continue
                
            # Check blocking flags
            if "flags_blocking" in expires:
                # Assuming story or global scope variables for custom flags
                # We check the store flags
                for flag in expires["flags_blocking"]:
                    if getattr(renpy.store, flag, False):
                        expire_objective(obj_id)
                        break


    def get_usable_material_value(assignment_id):
        """
        Returns the total value of unconsumed materials matching this assignment.
        """
        return sum(m.get("value", 0) for m in manuscript_material if m.get("assignment_id") == assignment_id and not m.get("consumed"))


    def check_assignment_readiness():
        """
        Re-evaluates the active writing assignment status.
        """
        global current_assignment_id
        if current_assignment_id not in writing_assignments:
            return

        assignment = writing_assignments[current_assignment_id]
        if assignment["status"] != "active":
            return

        usable_value = get_usable_material_value(current_assignment_id)
        if usable_value >= assignment["required_material"]:
            assignment["status"] = "ready"
            add_bundle_item({
                "type": "inspiration",
                "title": "Manuscript Ready",
                "body": f"Cora has enough material for a baseline draft of '{assignment['title']}'.",
                "icon": "quill",
            })

        update_available_variants(current_assignment_id)


    def variant_requirements_met(assignment_id, reqs):
        """
        Evaluates requirements (corruption, tag, min_tier) for a specific manuscript draft variant.
        """
        usable = [m for m in manuscript_material if m.get("assignment_id") == assignment_id and not m.get("consumed")]
        total_val = sum(m.get("value", 0) for m in usable)
        
        if total_val < reqs.get("required_material", 5):
            return False

        if corruption < reqs.get("required_corruption", 0):
            return False

        # Blackmail material requirement counts materials with the 'blackmail' or 'evidence' tag
        evidence_count = 0
        for m in usable:
            has_evidence = False
            for t in ["evidence", "blackmail"]:
                if t in m.get("tags", []):
                    has_evidence = True
                    break
            if has_evidence:
                evidence_count += 1

        if reqs.get("required_blackmail_material", 0) > 0 and evidence_count < reqs.get("required_blackmail_material", 0):
            return False

        min_tier = reqs.get("min_material_tier", 1)
        required_tags = reqs.get("required_tags", [])

        if required_tags:
            # Must contain at least one material of min_tier matching one of the required tags
            has_tag_and_tier = False
            for m in usable:
                if m.get("tier", 1) >= min_tier:
                    has_tag = False
                    for tag in required_tags:
                        if tag in m.get("tags", []):
                            has_tag = True
                            break
                    if has_tag:
                        has_tag_and_tier = True
                        break
            if not has_tag_and_tier:
                return False
        else:
            # Just ensure at least one material meets min_tier
            has_min_tier = False
            for m in usable:
                if m.get("tier", 1) >= min_tier:
                    has_min_tier = True
                    break
            if not has_min_tier:
                return False

        return True


    def update_available_variants(assignment_id):
        """
        Unlocks appropriate draft variants based on current stats and materials.
        """
        assignment = writing_assignments[assignment_id]
        if "available_variants" not in assignment:
            assignment["available_variants"] = []

        for variant_id, reqs in assignment["variants"].items():
            if variant_requirements_met(assignment_id, reqs):
                if variant_id not in assignment["available_variants"]:
                    assignment["available_variants"].append(variant_id)


    def complete_assignment(assignment_id, selected_variant):
        """
        Completes the manuscript using gathered materials.
        Converts excess overflow value into Draft Quality.
        """
        assignment = writing_assignments[assignment_id]
        
        # 1. Consume required materials
        reqs = assignment["variants"][selected_variant]
        usable = [m for m in manuscript_material if m.get("assignment_id") == assignment_id and not m.get("consumed")]
        
        # Sort usable by tier descending so high tier materials are prioritized if needed,
        # or we just consume all of them that contributed.
        # Since we consume standard value, let's mark the consumed ones.
        consumed_value = 0
        required_val = assignment["required_material"]
        
        for m in usable:
            if consumed_value < required_val:
                m["consumed"] = True
                consumed_value += m.get("value", 0)
        
        # 2. Convert overflow (remaining unconsumed materials) into Draft Quality
        overflow = sum(m.get("value", 0) for m in usable if not m["consumed"])
        if overflow > 0:
            draft_quality[assignment_id] = min(100, draft_quality.get(assignment_id, 0) + overflow * 10)
            
        # 3. Decay remaining unconsumed materials for this assignment (they cannot carry over)
        for m in usable:
            if not m["consumed"]:
                m["consumed"] = True # Mark as consumed/archived
                
        # 4. Set status and issue notification
        assignment["status"] = "complete"
        setattr(renpy.store, f"manuscript_flags_{assignment_id}_{selected_variant}", True)

        add_bundle_item({
            "type": "objective",
            "title": "Manuscript Complete",
            "body": f"Cora completed the '{selected_variant}' version of '{assignment['title']}'.",
            "icon": "journal",
        })


    def expire_chapter_material(chapter_id):
        """
        Expires unspent material tags at the end of the chapter to prevent hoarding.
        """
        expired_any = False
        for m in manuscript_material:
            if m.get("chapter_id") == chapter_id and not m.get("consumed"):
                if m.get("expires_after_chapter", True):
                    m["consumed"] = True
                    expired_any = True
                    
        if expired_any:
            add_bundle_item({
                "type": "opportunity",
                "title": "Leads Gone Cold",
                "body": "Some of Cora's temporary notes and observations have gone cold.",
                "icon": "hourglass",
            })


    def add_stat_delta(stat_name, amount, character=None, source=None):
        """
        Dynamic handler for stat updates (suspicion, corruption) that funnels into
        composite notifications and thresholds.
        """
        global corruption
        if stat_name == "corruption":
            corruption = max(0, corruption + amount)
            add_bundle_item({
                "type": "corruption",
                "title": "Corruption Changed" if amount > 0 else "Purity Restored",
                "body": "Cora's restraint slips..." if amount > 0 else "Cora pulls back.",
                "icon": "ink_bleed",
            })
        elif stat_name == "suspicion" and character:
            old_susp = suspicion.get(character, 0)
            new_susp = max(0, min(100, old_susp + amount))
            suspicion[character] = new_susp
            
            # Simple standard feedback for standard delta changes.
            # (Note: Breakpoint checks can be mapped to character-specific monologues here)
            add_bundle_item({
                "type": "suspicion",
                "title": f"{character.capitalize()} Suspicion",
                "body": f"They are watching Cora more closely." if amount > 0 else f"Their attention drifts.",
                "icon": "eye_icon",
            })


    def activate_objective(obj_id):
        """
        Activates a journal objective.
        """
        if obj_id in objectives:
            objectives[obj_id]["status"] = "active"
            add_bundle_item({
                "type": "objective",
                "title": "Objective Active",
                "body": objectives[obj_id]["title"],
                "icon": "journal",
            })


    def complete_objective(obj_id):
        """
        Completes a journal objective.
        """
        if obj_id in objectives and objectives[obj_id]["status"] == "active":
            objectives[obj_id]["status"] = "complete"
            add_bundle_item({
                "type": "objective",
                "title": "Objective Complete",
                "body": objectives[obj_id]["title"],
                "icon": "journal",
            })


    def fail_objective(obj_id):
        """
        Fails a journal objective.
        """
        if obj_id in objectives and objectives[obj_id]["status"] == "active":
            objectives[obj_id]["status"] = "failed"
            add_bundle_item({
                "type": "objective",
                "title": "Objective Failed",
                "body": objectives[obj_id]["title"],
                "icon": "journal",
            })


    def expire_objective(obj_id):
        """
        Expires a journal objective (opportunity lost).
        """
        if obj_id in objectives and objectives[obj_id]["status"] == "active":
            objectives[obj_id]["status"] = "expired"
            add_bundle_item({
                "type": "opportunity",
                "title": "Opportunity Faded",
                "body": objectives[obj_id]["title"],
                "icon": "hourglass",
            })


    def set_scene_context(location=None, present=None, relevant=None):
        """
        Updates the character context to reflect the local room situation.
        Used to feed the HUD watcher display.
        """
        present = present or []
        relevant = relevant or []
        
        for char_id in character_context:
            character_context[char_id]["present"] = (char_id in present)
            character_context[char_id]["scene_relevant"] = (char_id in relevant)
            if char_id in present:
                character_context[char_id]["location"] = location


    def character_attached_to_active_objective(char_id):
        """
        Returns true if the character is related to any active objective descriptions.
        """
        for obj in objectives.values():
            if obj.get("status") == "active":
                desc = obj.get("description", "").lower()
                title = obj.get("title", "").lower()
                if char_id in desc or char_id in title:
                    return True
        return False


    def get_hud_risk_character():
        """
        Calculates priority context scores to select which character represents
        the immediate watch threat for HUD display.
        """
        candidates = []

        for char_id, ctx in character_context.items():
            suspicion_value = suspicion.get(char_id, 0)
            if suspicion_value <= 0:
                continue

            score = suspicion_value

            if ctx.get("present"):
                score += 100

            if ctx.get("scene_relevant"):
                score += 50

            if character_attached_to_active_objective(char_id):
                score += 25

            # Assume major breakpoint threshold is 35 (noticed/watching)
            if suspicion_value >= 35:
                score += 10

            candidates.append((score, char_id))

        if not candidates:
            return None

        candidates.sort(reverse=True)
        return candidates[0][1]


    # Placeholder stub for notification card items.
    # Wires logic cleanly even before Phase B UI code is implemented.
    def add_bundle_item(item):
        global pending_notification_bundle
        if pending_notification_bundle is None:
            pending_notification_bundle = {
                "level": "standard",
                "items": []
            }
        
        pending_notification_bundle["items"].append(item)
        
        # If any item is suspicion delta or crossing a critical mark, set level to breakpoint
        if item.get("type") == "suspicion":
            # For simplicity, standard updates could elevate to breakpoint if needed,
            # or keep it as standard unless a custom rule applies.
            pass


    def initialize_narrative_pressure_states():
        import renpy.store as store
        
        # Check and populate each default variable if missing
        if getattr(store, "suspicion", None) is None:
            store.suspicion = {
                "vance": 0,
                "gideon": 0,
                "stern": 0,
                "missy": 0,
            }
        if getattr(store, "corruption", None) is None:
            store.corruption = 0
        if getattr(store, "manuscript_material", None) is None:
            store.manuscript_material = []
            
        if getattr(store, "objectives", None) is None or not store.objectives:
            store.objectives = {
                "obj_prologue_retrieve_pages": {
                    "title": "Retrieve Confiscated Pages",
                    "description": "Snoop through Lady Eleanor's withdrawing room to find the missing three pages of your manuscript.",
                    "category": "story",
                    "status": "active",
                    "required": True,
                    "hidden": False,
                    "focus_cost": 0,
                    "expires_when": {},
                    "rewards": {},
                    "risk_text": "",
                }
            }
            
        if getattr(store, "writing_assignments", None) is None or not store.writing_assignments:
            store.writing_assignments = {
                "prologue_assignment": {
                    "title": "Wiltshire Revelations",
                    "chapter_id": "prologue",
                    "status": "active",
                    "required_material": 3,
                    "variants": {
                        "respectable": {
                            "required_material": 3,
                            "min_material_tier": 1,
                            "required_tags": [],
                            "required_corruption": 0,
                            "required_blackmail_material": 0,
                        }
                    },
                    "completion_label": None,
                    "available_variants": ["respectable"],
                }
            }
            
        if getattr(store, "current_assignment_id", None) is None:
            store.current_assignment_id = "prologue_assignment"
        if getattr(store, "current_chapter_id", None) is None:
            store.current_chapter_id = "prologue"
        if getattr(store, "chapter_focus_remaining", None) is None:
            store.chapter_focus_remaining = 6
            
        if getattr(store, "character_context", None) is None or not store.character_context:
            store.character_context = {
                "vance": {
                    "present": False,
                    "location": None,
                    "scene_relevant": False,
                },
                "gideon": {
                    "present": False,
                    "location": None,
                    "scene_relevant": False,
                },
                "stern": {
                    "present": False,
                    "location": None,
                    "scene_relevant": False,
                },
                "missy": {
                    "present": False,
                    "location": None,
                    "scene_relevant": False,
                },
            }
            
        if getattr(store, "draft_quality", None) is None:
            store.draft_quality = {
                "assignment_01": 0,
            }
        if getattr(store, "journal_tab", None) is None:
            store.journal_tab = "manuscript"
        if getattr(store, "hud_enabled", None) is None:
            store.hud_enabled = True
        if getattr(store, "cinema_mode", None) is None:
            store.cinema_mode = False
        if getattr(store, "journal_updated_indicator", None) is None:
            store.journal_updated_indicator = False
            
    def transition_prologue_to_main_game():
        import renpy.store as store
        
        # 1. Archive the prologue objective
        if "obj_prologue_retrieve_pages" in store.objectives:
            store.objectives["obj_prologue_retrieve_pages"]["status"] = "complete"
            
        # 2. Clear all Wiltshire prologue snoop material from Cora's active inventory
        store.manuscript_material = []
        
        # 3. Setup the main game objectives
        store.objectives.update({
            "obj_assignment_01_material": {
                "title": "Gather material for the first manuscript",
                "description": "Cora needs enough vivid material to turn private scandal into fiction.",
                "category": "manuscript",
                "status": "active",
                "required": True,
                "hidden": False,
                "focus_cost": 0,
                "expires_when": {},
                "rewards": {},
                "risk_text": "",
            },
            "obj_follow_vance": {
                "title": "Follow Vance after supper",
                "description": "Vance may lead Cora toward stronger material than ordinary chores can provide.",
                "category": "optional",
                "status": "active",
                "required": False,
                "hidden": False,
                "focus_cost": 2,
                "expires_when": {
                    "chapter": "chapter_01",
                    "focus_below": 2,
                    "flags_blocking": ["completed_evening_duties"]
                },
                "rewards": {
                    "material_id": "mat_vance_supper_secret"
                },
                "risk_text": "Vance suspicion may increase if Cora is seen.",
            },
            "obj_blackmail_gideon": {
                "title": "Find leverage against Gideon",
                "description": "Cora needs more than suspicion before she can safely move against him.",
                "category": "story",
                "status": "inactive",
                "required": True,
                "hidden": False,
                "focus_cost": 2,
                "expires_when": {},
                "rewards": {
                    "blackmail_material": 1
                },
                "risk_text": "Failure may increase Gideon’s suspicion.",
            },
        })
        
        # 4. Setup the main game writing assignments
        store.writing_assignments = {
            "assignment_01": {
                "title": "The House Behind the Velvet Door",
                "chapter_id": "chapter_01",
                "status": "active",
                "required_material": 5,
                "variants": {
                    "respectable": {
                        "required_material": 5,
                        "min_material_tier": 1,
                        "required_tags": [],
                        "required_corruption": 0,
                        "required_blackmail_material": 0,
                    },
                    "scandalous": {
                        "required_material": 5,
                        "min_material_tier": 2,
                        "required_tags": ["scandal"],
                        "required_corruption": 2,
                        "required_blackmail_material": 0,
                    },
                    "blackmail": {
                        "required_material": 5,
                        "min_material_tier": 3,
                        "required_tags": ["evidence"],
                        "required_corruption": 2,
                        "required_blackmail_material": 1,
                    }
                },
                "completion_label": "write_assignment_01",
                "available_variants": ["respectable"],
            }
        }
        
        # 5. Transition to Savoy chapter chapter_01
        store.current_assignment_id = "assignment_01"
        store.current_chapter_id = "chapter_01"
        store.chapter_focus_remaining = 6
        
        # Trigger popup notification for the journal update
        store.journal_updated_indicator = True

