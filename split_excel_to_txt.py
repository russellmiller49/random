import pandas as pd
import os
import re

def clean_text(text):
    if pd.isna(text): return ""
    return str(text).strip()

def split_excel_notes(excel_path, output_dir="granular_notes"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = output_dir if os.path.isabs(output_dir) else os.path.join(base_dir, output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Read Excel without header initially to catch the layout
    df = pd.read_csv(excel_path) if excel_path.endswith('.csv') else pd.read_excel(excel_path, header=None)
    
    current_note_id = None
    current_text_buffer = []
    
    print(f"Processing {excel_path}...")
    
    # Iterate through every row looking for "NOTE_ID:" pattern
    for index, row in df.iterrows():
        # Convert row to a single string to search for markers
        row_str = " ".join([str(x) for x in row.values if pd.notna(x)])
        
        # Check if this row marks the start of a new note
        # Looking for pattern "NOTE_ID: ... note_001"
        match = re.search(r"NOTE_ID:\s*[,;]?\s*(\w+)", row_str, re.IGNORECASE)
        
        if match:
            # Save previous note if exists
            if current_note_id and current_text_buffer:
                save_note(current_note_id, current_text_buffer, output_dir)
            
            # Start new note
            current_note_id = match.group(1)
            current_text_buffer = []
            print(f"Found start of {current_note_id}")
            
            # Add the metadata line itself to the buffer so we keep context
            current_text_buffer.append(row_str)
        else:
            # Just content lines
            if current_note_id:
                # Add non-empty cells from this row
                content_lines = [str(x) for x in row.values if pd.notna(x) and str(x).strip() != ""]
                if content_lines:
                    current_text_buffer.append("\n".join(content_lines))

    # Save the last note
    if current_note_id and current_text_buffer:
        save_note(current_note_id, current_text_buffer, output_dir)

def save_note(note_id, lines, output_dir):
    # safe filename
    filename = re.sub(r'[^\w\-]', '_', str(note_id)) + ".txt"
    out_path = os.path.join(output_dir, filename)
    
    full_text = "\n".join(lines)
    
    # Basic cleanup of multiple newlines
    full_text = re.sub(r'\n{3,}', '\n\n', full_text)
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Saved: {out_path}")

# --- CHANGE THIS PATH TO YOUR FILE ---
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "granular_notes", "Granular_notes_ 12_11 to 1_11.xlsx")
    split_excel_notes(input_file)