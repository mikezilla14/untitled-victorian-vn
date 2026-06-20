# ═══════════════════════════════════════════════════════════════
#  characters.rpy
#  All character definitions in one place.
#  To rename, recolour, or add a character: edit only this file.
# ═══════════════════════════════════════════════════════════════

define cora    = Character("Cora",      color="#d4a574", callback=name_callback, cb_name="cora")
define cora_inner = Character(None, what_italic=True, what_color="#dfcbb5", screen="thought_overlay", callback=name_callback, cb_name=None)
define gideon  = Character("Sir Gideon", color="#a30000", callback=name_callback, cb_name="gideon")
define stern   = Character("Miss Stern", color="#555555", callback=name_callback, cb_name="stern")
define vance   = Character("Vance",      color="#7b3f98", callback=name_callback, cb_name="vance")
define missy   = Character("Missy",      color="#5fa8d3", callback=name_callback, cb_name="missy")
define lady_eleanor = Character("Lady Eleanor", color="#c9a0dc", callback=name_callback, cb_name="lady_eleanor")
define margaret = Character("Margaret", color="#8a9eb5", callback=name_callback, cb_name="margaret")
define sir_john = Character("Sir John", color="#4a5568", callback=name_callback, cb_name="sir_john")
define narrator = Character(None, callback=name_callback, cb_name=None)
define sys_msg     = Character("System",    color="#ffcc00", callback=name_callback, cb_name=None)
