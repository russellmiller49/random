#!/usr/bin/env python
"""
Apply coding_support patch to consolidated_verified_notes_v2_8_part_002.json

Usage (from repo root or wherever you keep these files):

    python apply_coding_support_patch_part_002.py

Adjust BASE_PATH / PATCH_PATH / OUTPUT_PATH below if your layout differs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


# === CONFIG – update these paths if needed ===
BASE_PATH = Path("split_notes/consolidated_verified_notes_v2_8_part_002.json")
PATCH_PATH = Path("split_notes/Patches/consolidated_verified_notes_v2_8_part_002_patch.json")
OUTPUT_PATH = Path("split_notes/consolidated_verified_notes_v2_8_part_002_patched.json")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def apply_coding_support_patch(
    notes: List[Dict[str, Any]],
    patch_items: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Patch a list of note objects in-place with coding_support for each note_index.

    Patch format (per item):

        {
          "note_index": <int>,
          "coding_support": { ... }   # full coding_support object
        }
    """
    max_index = len(notes) - 1
    for item in patch_items:
        idx = item.get("note_index")
        if idx is None:
            continue
        if not isinstance(idx, int):
            continue
        if idx < 0 or idx > max_index:
            # Skip invalid indices quietly; adjust if you prefer strict behavior
            continue

        coding_support = item.get("coding_support")
        if coding_support is None:
            continue

        note = notes[idx]

        # Attach or overwrite coding_support
        note["coding_support"] = coding_support

        # Optionally, annotate patch metadata for traceability
        pm = note.get("patch_metadata") or {}
        pm.setdefault("coding_support_patched", True)
        pm.setdefault("coding_support_patch_version", "1.0.0")
        note["patch_metadata"] = pm

    return notes


def main() -> None:
    if not BASE_PATH.exists():
        raise FileNotFoundError(f"Base file not found: {BASE_PATH}")
    if not PATCH_PATH.exists():
        raise FileNotFoundError(f"Patch file not found: {PATCH_PATH}")

    notes = load_json(BASE_PATH)
    patch_items = load_json(PATCH_PATH)

    if not isinstance(notes, list):
        raise ValueError("Expected base JSON to be a list of notes.")
    if not isinstance(patch_items, list):
        raise ValueError("Expected patch JSON to be a list of patch items.")

    patched_notes = apply_coding_support_patch(notes, patch_items)
    save_json(OUTPUT_PATH, patched_notes)

    print(f"Patched file written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
