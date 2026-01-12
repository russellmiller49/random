import pandas as pd
import re

# Load the file
input_file = 'span_annotations.csv'
output_file = 'span_annotations_CLEANED.csv'

print(f"Loading {input_file}...")
df = pd.read_csv(input_file)

# ---------------------------------------------------------
# 1. REMOVE GHOST ROWS
# ---------------------------------------------------------
initial_count = len(df)
df = df.dropna(subset=['span_text'])
print(f"Removed {initial_count - len(df)} empty rows.")

# ---------------------------------------------------------
# 2. NORMALIZE LABELS (Schema Fix)
# ---------------------------------------------------------
# Mapping dictionary: { 'Bad_Label': 'Good_Label' }
label_map = {
    'ANAT_PLEURAL_LOC': 'ANAT_PLEURA',
    'DEV_DEVICE_SIZE': 'DEV_CATHETER_SIZE', # Assuming context is pleural/catheter
    'TIME_ANCHOR': 'CTX_TIME',
    'DEV_IMPLANT': 'DEV_STENT',             # Defaulting generic implant to stent
    'MEAS_TIME': 'CTX_TIME',                # Merge measurement times into context
    # Labels without clear maps are left alone for manual review if not listed here
}

# Apply mapping
df['label'] = df['label'].replace(label_map)
print("Labels normalized.")

# ---------------------------------------------------------
# 3. FIX STENT GRANULARITY (Split Brand & Size)
# ---------------------------------------------------------
# Logic: Find DEV_STENT rows with numbers. 
# Split them into two rows: one for Brand (DEV_STENT), one for Size (DEV_STENT_SIZE).

new_rows = []
indices_to_drop = []

# Regex to capture "Brand" and "Size" 
# Looks for patterns like "Brand [digits]mm x [digits]mm"
pattern = re.compile(r'(?P<brand>.*?)\s+(?P<size>\d+.*)')

for idx, row in df.iterrows():
    if row['label'] == 'DEV_STENT' and isinstance(row['span_text'], str):
        # Check if it contains digits (indicating a size is mixed in)
        if any(char.isdigit() for char in row['span_text']):
            match = pattern.search(row['span_text'])
            if match:
                brand_text = match.group('brand').strip() + " stent" # Re-add "stent" for context if needed
                size_text = match.group('size').replace(" stent", "").strip() # Remove trailing "stent" from size

                # 1. Create the SIZE row
                size_row = row.copy()
                size_row['span_text'] = size_text
                size_row['label'] = 'DEV_STENT_SIZE'
                size_row['span_id'] = f"{row['span_id']}_size" # Unique ID
                new_rows.append(size_row)

                # 2. Update the original row to be just BRAND
                # We modify the dataframe directly later, but for now we track the change
                df.at[idx, 'span_text'] = brand_text
                # Label remains DEV_STENT
                
                print(f"Splitting: '{row['span_text']}' -> ['{brand_text}', '{size_text}']")

# Append the new size rows to the dataframe
if new_rows:
    new_rows_df = pd.DataFrame(new_rows)
    df = pd.concat([df, new_rows_df], ignore_index=True)
    print(f"Created {len(new_rows)} new rows for detached Stent Sizes.")

# ---------------------------------------------------------
# 4. EXPORT
# ---------------------------------------------------------
# Sort by note_id to keep things tidy
df = df.sort_values(by=['note_id', 'start_char'])
df.to_csv(output_file, index=False)

print(f"\nSuccess! Cleaned data saved to: {output_file}")
print("You can now upload this file to your hydration pipeline.")