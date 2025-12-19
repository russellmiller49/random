#!/usr/bin/env python3
"""
Script to find which synthetic generation scripts haven't been run.
Compares output filenames in scripts with files in Synthetic_expansions folder.
"""

import os
import re
from pathlib import Path

def extract_output_filename(script_path):
    """Extract the output filename from a Python script."""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # First, check for OUTPUT_FILE = "filename.json" constant at top
        pattern0 = r'OUTPUT_FILE\s*=\s*["\']([^"\']+)["\']'
        match0 = re.search(pattern0, content)
        if match0:
            return match0.group(1)
        
        # Check for OUTPUT_FILENAME = "filename.json" constant at top
        pattern0b = r'OUTPUT_FILENAME\s*=\s*["\']([^"\']+)["\']'
        match0b = re.search(pattern0b, content)
        if match0b:
            return match0b.group(1)
        
        # Look for output_filename = output_dir / "filename.json"
        pattern1 = r'output_filename\s*=\s*output_dir\s*/\s*["\']([^"\']+)["\']'
        match1 = re.search(pattern1, content)
        if match1:
            return match1.group(1)
        
        # Look for output_file = output_dir / "filename.json"
        pattern2 = r'output_file\s*=\s*output_dir\s*/\s*["\']([^"\']+)["\']'
        match2 = re.search(pattern2, content)
        if match2:
            return match2.group(1)
        
        # Look for output_file = output_path / "filename.json"
        pattern2b = r'output_file\s*=\s*output_path\s*/\s*["\']([^"\']+)["\']'
        match2b = re.search(pattern2b, content)
        if match2b:
            return match2b.group(1)
        
        # Look for output_filename = Path(...) / "filename.json"
        pattern3 = r'output_filename\s*=\s*.*?/\s*["\']([^"\']+)["\']'
        match3 = re.search(pattern3, content)
        if match3:
            return match3.group(1)
        
        # Look for output_path = output_dir / OUTPUT_FILE or OUTPUT_FILENAME
        pattern4 = r'output_path\s*=\s*output_dir\s*/\s*(OUTPUT_FILE|OUTPUT_FILENAME)'
        match4 = re.search(pattern4, content)
        if match4:
            # If we found this pattern, we already got OUTPUT_FILE or OUTPUT_FILENAME from pattern0/0b
            if match0:
                return match0.group(1)
            if match0b:
                return match0b.group(1)
        
        return None
    except Exception as e:
        print(f"Error reading {script_path}: {e}")
        return None

def main():
    scripts_dir = Path("synthetic_expansion_python_scripts")
    outputs_dir = Path("Synthetic_expansions")
    
    # Get all Python scripts
    scripts = sorted(scripts_dir.glob("synthetic_generation*.py"))
    print(f"Found {len(scripts)} scripts")
    
    # Get all output files
    output_files = {f.name for f in outputs_dir.glob("*.json")}
    print(f"Found {len(output_files)} output files")
    
    # Map each script to its expected output
    script_to_output = {}
    missing_outputs = []
    
    for script in scripts:
        output_filename = extract_output_filename(script)
        if output_filename:
            script_to_output[script.name] = output_filename
            if output_filename not in output_files:
                missing_outputs.append((script.name, output_filename))
        else:
            print(f"Warning: Could not extract output filename from {script.name}")
            missing_outputs.append((script.name, "UNKNOWN"))
    
    print("\n" + "="*80)
    print(f"SCRIPTS THAT HAVEN'T BEEN RUN ({len(missing_outputs)}):")
    print("="*80)
    
    for script_name, expected_output in sorted(missing_outputs):
        print(f"  {script_name}")
        print(f"    Expected output: {expected_output}")
        print()
    
    print(f"\nTotal scripts: {len(scripts)}")
    print(f"Scripts with outputs: {len(scripts) - len(missing_outputs)}")
    print(f"Scripts missing outputs: {len(missing_outputs)}")
    
    # Also check for output files that don't match any script
    expected_outputs = set(script_to_output.values())
    orphan_outputs = output_files - expected_outputs
    if orphan_outputs:
        print(f"\nNote: {len(orphan_outputs)} output file(s) don't match any script:")
        for orphan in sorted(orphan_outputs):
            print(f"  {orphan}")

if __name__ == "__main__":
    main()

