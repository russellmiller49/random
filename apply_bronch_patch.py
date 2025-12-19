import json
import jsonpatch
import re
from pathlib import Path

def extract_part_number(patch_filename):
    """Extract part number from patch filename like 'bronch_notes_part_001_patch.json'"""
    match = re.search(r'part_(\d+)_patch\.json$', patch_filename)
    if match:
        return match.group(1)
    return None

def process_patch(original_path, patch_path, output_path):
    """Apply a single patch file to an original file and write the output."""
    try:
        # load original notes
        with open(original_path, "r", encoding="utf-8") as f:
            original = json.load(f)

        # load JSON Patch operations
        with open(patch_path, "r", encoding="utf-8") as f:
            patch_ops = json.load(f)

        # Skip if patch is empty (empty array)
        if not patch_ops:
            print(f"  → Skipping: Patch file is empty, copying original as-is")
            # Copy original to output
            output_path_obj = Path(output_path)
            output_path_obj.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(original, f, indent=2)
            return True

        # apply patch
        patch = jsonpatch.JsonPatch(patch_ops)
        patched = patch.apply(original, in_place=False)

        # ensure output directory exists
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        # write patched file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(patched, f, indent=2)

        print(f"  ✓ Patched file written to {output_path}")
        return True
    except FileNotFoundError as e:
        print(f"  ✗ Error: File not found - {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"  ✗ Error: Invalid JSON in {patch_path} - {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error processing {patch_path}: {e}")
        return False

def main():
    # Find all patch files in bronch_extractions_patches directory
    patches_dir = Path("bronch_extractions_patches")
    if not patches_dir.exists():
        print(f"Error: Directory {patches_dir} not found")
        return

    patch_files = sorted(patches_dir.glob("bronch_notes_part_*_patch.json"))
    
    if not patch_files:
        print("No patch files found matching pattern 'bronch_notes_part_*_patch.json'")
        return

    print(f"Found {len(patch_files)} patch file(s) to process\n")

    success_count = 0
    for patch_file in patch_files:
        part_num = extract_part_number(patch_file.name)
        if not part_num:
            print(f"✗ Skipping {patch_file.name}: Could not extract part number")
            continue

        # Construct paths based on part number
        original_path = f"bronch_extractions/bronch_notes_part_{part_num}.json"
        patch_path = str(patch_file)
        output_path = f"bronch_extractions_patched/bronch_notes_part_{part_num}.json"

        print(f"Processing part {part_num}...")
        if process_patch(original_path, patch_path, output_path):
            success_count += 1
        print()

    print(f"Completed: {success_count}/{len(patch_files)} files processed successfully")

if __name__ == "__main__":
    main()
