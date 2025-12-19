#!/usr/bin/env python3
"""
Convert bronch_notes_folder.csv to JSON files matching golden_extractions format.
Creates one JSON file per 5 notes.
"""

import pandas as pd
import json
import os
from pathlib import Path

def extract_cpt_codes(extraction):
    """Extract CPT codes from the extraction JSON."""
    cpt_codes = []
    if 'billing' in extraction and 'cpt_codes' in extraction['billing']:
        for cpt_entry in extraction['billing']['cpt_codes']:
            if isinstance(cpt_entry, dict) and 'code' in cpt_entry:
                try:
                    # Convert CPT code to integer
                    cpt_code = int(cpt_entry['code'])
                    cpt_codes.append(cpt_code)
                except (ValueError, TypeError):
                    # If conversion fails, skip this code
                    continue
    return cpt_codes

def convert_csv_to_json_format(csv_path, output_dir='bronch_extractions'):
    """Convert CSV to JSON files matching golden_extractions format."""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read CSV file
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path)
    
    print(f"Total rows: {len(df)}")
    
    # Process rows in batches of 5
    batch_size = 5
    file_counter = 1
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        batch_data = []
        
        for idx, row in batch.iterrows():
            try:
                # Get note text from column A (first column)
                note_text = str(row.iloc[0]).strip()
                
                # Get extraction JSON from column B (second column)
                extraction_str = str(row.iloc[1]).strip()
                
                # Skip if either is empty or invalid
                if not note_text or note_text == 'nan' or not extraction_str or extraction_str == 'nan':
                    print(f"Warning: Skipping row {idx} - empty note or extraction")
                    continue
                
                # Parse the extraction JSON
                try:
                    extraction = json.loads(extraction_str)
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping row {idx} - invalid JSON: {e}")
                    continue
                
                # Extract CPT codes
                cpt_codes = extract_cpt_codes(extraction)
                
                # Create the entry in golden_extractions format
                entry = {
                    "note_text": note_text,
                    "cpt_codes": cpt_codes,
                    "registry_entry": extraction
                }
                
                batch_data.append(entry)
                
            except Exception as e:
                print(f"Error processing row {idx}: {e}")
                continue
        
        # Skip empty batches
        if not batch_data:
            continue
        
        # Write batch to JSON file
        output_filename = f"bronch_notes_part_{file_counter:03d}.json"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, indent=2, ensure_ascii=False)
        
        print(f"Created {output_filename} with {len(batch_data)} notes")
        file_counter += 1
    
    print(f"\nConversion complete! Created {file_counter - 1} JSON files in {output_dir}/")

if __name__ == "__main__":
    csv_path = "bronch_notes_folder.csv"
    convert_csv_to_json_format(csv_path)
