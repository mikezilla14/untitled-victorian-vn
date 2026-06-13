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

# Suspicion monologue prose table.
# Writers may edit this file without touching suspicion trigger/runtime logic.

init python:

    SUSPICION_CHARACTER_NAMES = {
        "stern": "Miss Stern",
        "vance": "Vance",
        "gideon": "Sir Gideon",
        "missy": "Missy",
        "generic": "Someone",
    }

    SUSPICION_MONOLOGUES = {
        ("vance", "noticed", "low"): ["Vance noticed the edge of my mask and said nothing."],
        ("vance", "noticed", "medium"): ["Vance's eyes caught on mine for half a second too long."],
        ("vance", "noticed", "high"): ["Vance saw something; not enough to accuse me, enough to remember."],
        ("vance", "watching", "low"): ["Vance had begun to read me as if we shared a language no one else could hear."],
        ("vance", "watching", "medium"): ["Vance watched with the wounded cleverness of someone who knew performance from the inside."],
        ("vance", "dangerous", "low"): ["Vance was arranging recognition into something sharper than gossip."],
        ("vance", "dangerous", "high"): ["Vance knew too much about masks to mistake mine for skin."],
        ("vance", "critical", "high"): ["Vance was one breath from naming what she recognized in me."],
        ("vance", "noticed", "high", "recognised_detail"): ["Recognition flashed in Vance's eyes, brief and intimate and impossible to unsay."],
        ("stern", "noticed", "low"): ["Miss Stern filed the moment away as neatly as a key returned to its hook."],
        ("stern", "noticed", "medium"): ["Miss Stern said nothing, which was worse than a question."],
        ("stern", "noticed", "high"): ["Miss Stern had seen the inconsistency and would not misplace it."],
        ("stern", "watching", "low"): ["Miss Stern's attention settled on me with the weight of a rulebook opening."],
        ("stern", "watching", "medium"): ["Miss Stern had begun inspecting my answers for loose threads."],
        ("stern", "dangerous", "low"): ["Miss Stern was turning suspicion into procedure."],
        ("stern", "dangerous", "high"): ["Miss Stern had nearly enough to make discipline sound like duty."],
        ("stern", "critical", "high"): ["Miss Stern's silence had reached the edge of a formal charge."],
        ("stern", "watching", "medium", "disciplinary_notice"): ["Miss Stern put the moment in order, as if misconduct were only another ledger column."],
        ("gideon", "noticed", "low"): ["Sir Gideon smiled as if I had finally become interesting."],
        ("gideon", "noticed", "medium"): ["Sir Gideon watched me as though patience were another form of ownership."],
        ("gideon", "noticed", "high"): ["Sir Gideon had caught the shape of the lie and seemed almost pleased."],
        ("gideon", "watching", "low"): ["Sir Gideon looked entertained, which was far worse than alarmed."],
        ("gideon", "watching", "medium"): ["Sir Gideon had begun treating my caution as a move in his game."],
        ("gideon", "dangerous", "low"): ["Sir Gideon was not frightened by the pattern; he was amused by it."],
        ("gideon", "dangerous", "high"): ["Sir Gideon had seen enough to wait for me to expose myself."],
        ("gideon", "critical", "high"): ["Sir Gideon stood close to the truth and smiled as if he owned the door."],
        ("gideon", "noticed", "low", "provoked_interest"): ["Sir Gideon marked the provocation and looked pleased that I had dared it."],
        ("missy", "noticed", "low"): ["Missy waited for the harmless explanation I had not prepared."],
        ("missy", "noticed", "medium"): ["Missy's trust faltered, and the cost of that was suddenly plain."],
        ("missy", "noticed", "high"): ["Missy looked at me as if I had made kindness into a trick."],
        ("missy", "watching", "low"): ["Missy watched because trust had taught her where to look."],
        ("missy", "watching", "medium"): ["Missy was trying to keep believing me, and that made every pause crueler."],
        ("missy", "dangerous", "low"): ["Missy's doubt hurt more because it had not learned to defend itself."],
        ("missy", "dangerous", "high"): ["Missy was beginning to understand that kindness could be used against her."],
        ("missy", "critical", "high"): ["Missy looked close to the truth, and the truth looked like betrayal."],
        ("missy", "noticed", "high", "hurt_trust"): ["Missy's face changed as trust became evidence against me."],
        ("generic", "noticed", "low"): ["My mask held, but someone had seen the edge of it."],
        ("generic", "noticed", "medium"): ["A glance shifted the room by an inch."],
        ("generic", "noticed", "high"): ["A pause, a look, a change in the air; I felt it before I understood it."],
        ("generic", "watching", "low"): ["The room had begun to study me back."],
        ("generic", "watching", "medium"): ["Someone was arranging the pieces now."],
        ("generic", "watching", "high"): ["The silence around me had learned to count."],
        ("generic", "dangerous", "low"): ["Suspicion had become a pattern, and patterns could be followed."],
        ("generic", "dangerous", "medium"): ["One more careless answer could make the pattern visible."],
        ("generic", "dangerous", "high"): ["The walls were closing in now; my next mistake could finish me."],
        ("generic", "critical", "low"): ["The next misstep would not be forgiven as clumsiness."],
        ("generic", "critical", "medium"): ["The room was one breath from accusation."],
        ("generic", "critical", "high"): ["There was almost no mask left to hold."],
        ("generic", "fallback"): ["Something in the room shifted, not enough to name, enough to remember."],
    }
