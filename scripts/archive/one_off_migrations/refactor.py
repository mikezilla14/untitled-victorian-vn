"""Archived one-off migration script.

Deprecated: this historical migration used hard-coded absolute paths and wrote
files immediately. It is kept only as a breadcrumb for the old class-backed state
migration and intentionally exits without modifying files.
"""

raise SystemExit(
    "Archived migration only. Use supported validators/codemods under scripts/ instead."
)
