#!/usr/bin/env python3
"""
Script to split consolidated_verified_notes_v2_8.json into multiple files
with 10 notes in each file.
"""

import json
import os
from pathlib import Path

def split_notes(input_file, notes_per_file=10):
    """
    Split a JSON file containing an array of notes into multiple files.
    
    Args:
        input_file: Path to the input JSON file
        notes_per_file: Number of notes per output file (default: 10)
    """
    # Read the input JSON file
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        notes = json.load(f)
    
    total_notes = len(notes)
    print(f"Found {total_notes} notes total")
    
    # Calculate number of output files needed
    num_files = (total_notes + notes_per_file - 1) // notes_per_file
    print(f"Will create {num_files} output files with up to {notes_per_file} notes each")
    
    # Create output directory if it doesn't exist
    output_dir = Path(input_file).parent / "split_notes"
    output_dir.mkdir(exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Split and save
    base_name = Path(input_file).stem
    for i in range(num_files):
        start_idx = i * notes_per_file
        end_idx = min(start_idx + notes_per_file, total_notes)
        
        chunk = notes[start_idx:end_idx]
        
        # Create output filename
        output_file = output_dir / f"{base_name}_part_{i+1:03d}.json"
        
        # Write chunk to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, indent=2, ensure_ascii=False)
        
        print(f"Created {output_file} with {len(chunk)} notes (indices {start_idx} to {end_idx-1})")
    
    print(f"\nDone! Created {num_files} files in {output_dir}")

if __name__ == "__main__":
    input_file = "consolidated_verified_notes_v2_8.json"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        exit(1)
    
    split_notes(input_file, notes_per_file=10)






