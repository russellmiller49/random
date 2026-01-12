import pandas as pd
import os

# Configuration
input_file = 'Label_guide.csv'
output_file = 'Label_guide_UPDATED.csv'

# Define the new rows to add
# matching the columns: Label, Definition, Examples, Maps To Schema Field, Notes
new_entries = [
    {
        "Label": "OBS_FINDING",
        "Definition": "General clinical findings (non-lesion).",
        "Examples": "erythema; secretions; inflammation; mucous plugging",
        "Maps To Schema Field": "findings.description",
        "Notes": "Catch-all for findings that are not distinct lesions/masses."
    },
    {
        "Label": "MEDICATION",
        "Definition": "Medications administered during procedure.",
        "Examples": "Lidocaine; Fentanyl; Versed; Epinephrine",
        "Maps To Schema Field": "procedure.medications.name",
        "Notes": "Capture drug name. Dose usually captured in context or separate measure."
    },
    {
        "Label": "SPECIMEN",
        "Definition": "Physical pathology/cytology samples collected.",
        "Examples": "cell block; core tissue; fluid; lavage fluid",
        "Maps To Schema Field": "pathology.specimen_type",
        "Notes": "Distinguish from the action (Biopsy) or the result (Malignant)."
    },
    {
        "Label": "MEAS_TIME",
        "Definition": "Specific duration measurements.",
        "Examples": "30 seconds; 2 minutes; 15 sec",
        "Maps To Schema Field": "procedure.event_duration",
        "Notes": "Use for ablation durations or breath holds, distinct from general timestamps."
    },
    {
        "Label": "MEAS_TEMP",
        "Definition": "Temperature readings.",
        "Examples": "37C; 98.6 F",
        "Maps To Schema Field": "vitals.temperature",
        "Notes": "Patient or device temperature."
    },
    {
        "Label": "MEAS_ENERGY",
        "Definition": "Energy settings or delivery.",
        "Examples": "30 Watts; 200 Joules; 60W",
        "Maps To Schema Field": "procedure.energy_delivered",
        "Notes": "Common in ablation procedures."
    }
]

# Load existing guide
if os.path.exists(input_file):
    print(f"Loading {input_file}...")
    df = pd.read_csv(input_file)
else:
    print(f"Error: {input_file} not found.")
    exit()

# Append new rows if they don't already exist
added_count = 0
existing_labels = df['Label'].unique()

rows_to_add = []
for entry in new_entries:
    if entry['Label'] not in existing_labels:
        rows_to_add.append(entry)
        added_count += 1
        print(f"Adding new label definition: {entry['Label']}")
    else:
        print(f"Skipping {entry['Label']} (already exists).")

if rows_to_add:
    new_df = pd.DataFrame(rows_to_add)
    # Ensure columns match order
    df = pd.concat([df, new_df], ignore_index=True)
    
    # Save
    df.to_csv(output_file, index=False)
    print(f"\nSuccess! Added {added_count} labels.")
    print(f"Updated guide saved to: {output_file}")
else:
    print("\nNo changes made (all labels were already present).")