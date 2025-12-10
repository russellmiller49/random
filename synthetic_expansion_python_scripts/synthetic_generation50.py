import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_050.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # This dictionary holds the text variations for Part 050.
    # Structure: Note_Index (0-4) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Eleanor Rigby (PleurX Removal)
            1: "Procedure: Tunneled cath removal. Local. Cuff dissected. Catheter removed intact. Suture closure.",
            2: "Ms. Rigby presented for elective explantation of an indwelling tunneled pleural catheter. Following sterile preparation and infiltration of lidocaine, the subcutaneous cuff was meticulously dissected. The catheter was withdrawn without complication, and the tract was closed with a purse-string suture.",
            3: "Procedure performed: Removal of tunneled pleural catheter (CPT 32552). The polyester cuff was identified and dissected from the subcutaneous tissue to allow removal. No imaging guidance was utilized.",
            4: "Procedure Note: Indwelling Pleural Catheter Removal. Steps: 1. Time out. 2. Local anesthesia. 3. Incision over cuff. 4. Dissection of cuff. 5. Catheter removal. 6. Closure. Patient tolerated well.",
            5: "pleurx removal for ms rigby drainage stopped so we took it out local lidocaine used cut down to the cuff and freed it up pulled the line out no issues put a stitch in sent home.",
            6: "The patient presented for removal of a PleurX catheter due to cessation of drainage. Ultrasound showed no fluid. Local anesthesia was administered. The cuff was dissected and the catheter removed smoothly. A suture was placed to close the site.",
            7: "[Indication] Malignant effusion, decreased drainage. [Anesthesia] Local. [Description] Cuff dissected, catheter removed. [Plan] Discharge.",
            8: "Ms. Rigby arrived for removal of her PleurX catheter. We prepped the site and used local anesthetic. I made an incision and dissected the cuff free from the tissue. The catheter slid out easily. We closed the site with a suture.",
            9: "Explantation of tunneled pleural drain. The device was extracted after freeing the Dacron anchor. The exit site was sutured."
        },
        1: { # Chen, Wei (Rigid Bronch FB)
            1: "Rigid bronch. Chicken bone RLL. Removed with optical forceps en bloc. No injury.",
            2: "Mr. Chen underwent rigid bronchoscopy for foreign body retrieval. The jagged osseous fragment was visualized within the right lower lobe. Utilizing optical forceps, the object was grasped and extracted en bloc with the rigid barrel to prevent glottic trauma.",
            3: "CPT 31635: Rigid bronchoscopy with removal of foreign body. The scope was introduced, and the foreign object (bone) was identified in the RLL. It was removed using forceps. No separate code for suctioning.",
            4: "Procedure: Rigid Bronchoscopy for FB Removal. Steps: 1. GA induced. 2. Rigid scope inserted. 3. FB identified RLL. 4. FB grasped and removed. 5. Airway re-inspected.",
            5: "rigid bronch for mr chen swallowed a bone saw it in the rll used the forceps to grab it had to pull the whole scope out with it cause it was big no bleeding ok.",
            6: "72-year-old male with foreign body aspiration. Rigid bronchoscopy performed. A chicken bone was seen in the RLL and removed using optical forceps. The airway was cleared of secretions.",
            7: "[Indication] Foreign body aspiration. [Anesthesia] General. [Description] Rigid scope used. Bone removed from RLL with forceps. [Plan] Antibiotics.",
            8: "Mr. Chen was brought to the OR for a rigid bronchoscopy to remove a chicken bone. We inserted the rigid scope and found the bone in the right lower lobe. We grabbed it with forceps and pulled everything out together. The airway looked fine afterwards.",
            9: "Therapeutic bronchoscopy with extraction of foreign material. A bone fragment was located in the basilar segments and withdrawn using grasping instruments."
        },
        2: { # Sarah Connors (Bronchial Thermoplasty)
            1: "BT Session 3. RUL and LUL. 62 activations total. No complications.",
            2: "Ms. Connors underwent the third and final session of bronchial thermoplasty. The Alair catheter was systematically deployed in the RUL and LUL. A total of 62 radiofrequency activations were delivered to the distal airways, completing the treatment protocol.",
            3: "CPT 31661: Bronchoscopy with bronchial thermoplasty, 2 or more lobes. RUL (30 activations) and LUL (32 activations) treated in this session.",
            4: "Procedure: Bronchial Thermoplasty. Target: RUL/LUL. Steps: 1. GA. 2. Alair catheter checked. 3. RUL treated. 4. LUL treated. 5. Total 62 activations. 6. Extubated.",
            5: "3rd thermoplasty session for sarah did the upper lobes today rul and lul lots of activations 62 total she did fine no issues with the airway extubated in room.",
            6: "Bronchial thermoplasty session 3 performed under general anesthesia. The right upper lobe and left upper lobe were treated with the Alair catheter. A total of 62 activations were delivered. The patient tolerated the procedure well.",
            7: "[Indication] Asthma. [Anesthesia] General. [Description] BT to RUL/LUL. 62 activations. [Plan] Discharge.",
            8: "We performed the final thermoplasty session for Ms. Connors. We targeted both upper lobes this time. We delivered a series of activations to the RUL and then the LUL, totaling 62. The patient woke up well.",
            9: "Bronchial thermal ablation, session 3. Radiofrequency energy was applied to the RUL and LUL airways. 62 applications were performed."
        },
        3: { # Arthur Dent (BLVR LUL)
            1: "BLVR LUL. Chartis negative (CV-). 4 Zephyr valves placed. Good occlusion.",
            2: "Mr. Dent underwent bronchoscopic lung volume reduction targeting the left upper lobe. Chartis assessment confirmed the absence of collateral ventilation. Four Zephyr endobronchial valves were sequentially deployed, achieving complete lobar atelectasis.",
            3: "CPT 31647: Bronchoscopy with placement of valves, initial lobe. LUL treated. Chartis assessment (31634 bundled) confirmed no collateral ventilation. 4 valves placed.",
            4: "Procedure: BLVR LUL. Steps: 1. GA/ETT. 2. Chartis check: No CV. 3. 4 valves deployed in LUL. 4. Occlusion confirmed.",
            5: "blvr for arthur dent lul emphysema chartis showed no cv so we put in 4 valves they sealed up good no pneumo seen right away admit for obs.",
            6: "Patient with severe LUL emphysema underwent valve placement. Chartis assessment showed no collateral ventilation. Four Zephyr valves were placed in the LUL segments. Lobar occlusion was confirmed.",
            7: "[Indication] LUL Emphysema. [Anesthesia] General. [Description] Chartis neg. 4 valves to LUL. [Plan] Admit.",
            8: "Mr. Dent came in for his valve procedure. We checked the LUL with the Chartis balloon and found no collateral ventilation. We then placed four valves to block off the lobe completely. He did well and went to recovery.",
            9: "Endobronchial valve implantation for lung volume reduction. The LUL was isolated. Four occlusion devices were inserted."
        },
        4: { # John Doe (Complex Bronch EBUS/Nav)
            1: "EBUS-TBNA 7, 4R. Radial EBUS RUL nodule. TBBx x5. Brush x1.",
            2: "Mr. Doe underwent a combined EBUS-TBNA and navigational bronchoscopy. Mediastinal staging involved sampling stations 7 and 4R. The peripheral RUL nodule was localized via radial EBUS (eccentric view) and sampled with transbronchial biopsy and brushing.",
            3: "CPT 31652 (EBUS-TBNA 2 stations), 31654 (Radial EBUS peripheral), 31628 (TBBx), 31623 (Brush). RUL nodule and mediastinal nodes sampled.",
            4: "Procedure: EBUS and Nav Bronch. Steps: 1. EBUS stations 7, 4R. 2. Radial EBUS to RUL lesion. 3. Biopsy x5. 4. Brush x1.",
            5: "bronch for john doe did ebus first hit 7 and 4r then switched scopes for the nodule in the rul used the radar probe found it eccentric took 5 biopsies and a brush rose said inflammation.",
            6: "Bronchoscopy performed for mediastinal adenopathy and RUL nodule. EBUS-TBNA of stations 7 and 4R was completed. The RUL nodule was located with radial EBUS and sampled via biopsy and brush.",
            7: "[Indication] Adenopathy/Nodule. [Anesthesia] Moderate. [Description] EBUS 7/4R. Radial EBUS RUL. TBBx/Brush. [Plan] Path pending.",
            8: "We started with the EBUS scope to sample the lymph nodes at stations 7 and 4R. Then we switched to the thin scope and used the radial probe to find the nodule in the right upper lobe. We took biopsies and a brush sample.",
            9: "Endobronchial ultrasound-guided needle aspiration of mediastinal nodes. Peripheral lesion localization via radial probe. Transbronchial sampling and brushing performed."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for new random names to ensure consistency across style indices.
    return [
        {"idx": 0, "orig_name": "Eleanor Rigby", "orig_age": 70, "names": ["Alice Moore", "Brenda Scott", "Catherine Hale", "Doris Young", "Evelyn King", "Florence Wright", "Grace Lopez", "Helen Adams", "Irene Clark"]},
        {"idx": 1, "orig_name": "Chen, Wei", "orig_age": 72, "names": ["David Chen", "Michael Wu", "Robert Liu", "James Zhang", "William Wang", "Thomas Yang", "Richard Huang", "Joseph Lin", "Charles Kim"]},
        {"idx": 2, "orig_name": "Sarah Connors", "orig_age": 40, "names": ["Emily Davis", "Jessica Miller", "Ashley Wilson", "Sarah Taylor", "Amanda Anderson", "Jennifer Thomas", "Nicole Jackson", "Stephanie White", "Melissa Harris"]},
        {"idx": 3, "orig_name": "Arthur Dent", "orig_age": 65, "names": ["Frank Adams", "George Baker", "Harry Nelson", "Ian Carter", "Jack Mitchell", "Kevin Roberts", "Larry Phillips", "Mark Campbell", "Nathan Evans"]},
        {"idx": 4, "orig_name": "John Doe", "orig_age": 60, "names": ["John Smith", "Robert Johnson", "Michael Brown", "William Jones", "David Garcia", "Richard Martinez", "Joseph Rodriguez", "Thomas Hernandez", "Charles Lopez"]},
    ]

def main():
    # Load original data from source file
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in source file: {e}")
        return
    
    if not isinstance(source_data, list):
        print(f"Error: Source file must contain a JSON array, got {type(source_data)}")
        return
    
    print(f"Loaded {len(source_data)} notes from {SOURCE_FILE}")
    
    variations_text = get_variations()
    base_data = get_base_data_mocks()
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_notes = []
    
    # Iterate through each original note in source data
    for idx, original_note in enumerate(source_data):
        if idx >= len(base_data):
            print(f"Warning: More notes in source than base_data entries. Skipping note {idx}.")
            continue
            
        record = base_data[idx]
        orig_age = record['orig_age']
        
        # Iterate through the 9 styles
        for style_num in range(1, 10):
            
            # Deep copy the original note structure
            note_entry = copy.deepcopy(original_note)
            
            # Determine new random age (+/- 3 years)
            new_age = orig_age + random.randint(-3, 3)
            
            # Determine new random date (within 2025)
            rand_date_obj = generate_random_date(2025, 2025)
            rand_date_str = rand_date_obj.strftime("%Y-%m-%d")
            
            # Get the specific name assigned in Part 1 for consistency
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry:
                if "patient_age" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_age"] = new_age
                if "procedure_date" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["procedure_date"] = rand_date_str
                # Update patient MRN to make it unique
                if "patient_mrn" in note_entry["registry_entry"]:
                    note_entry["registry_entry"]["patient_mrn"] = f"{note_entry['registry_entry']['patient_mrn']}_syn_{style_num}"
            
            # Add metadata about the synthetic generation
            note_entry["synthetic_metadata"] = {
                "source_file": SOURCE_FILE,
                "original_index": idx,
                "style_type": style_num,
                "generated_name": new_name,
                "generation_date": datetime.datetime.now().isoformat()
            }
            
            generated_notes.append(note_entry)

    # Output to JSON in Synthetic_expansions folder
    output_filename = output_dir / "synthetic_blvr_notes_part_050.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()