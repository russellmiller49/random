import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "bronch_extractions_patched/bronch_notes_part_004.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of text variations for each note in bronch_notes_part_004.json.
    Key: Original Note Index (0-2)
    Value: Dictionary of Style Index (1-9) -> Transformed Text
    """
    variations = {
        0: { # Note 0: EBUS-TBNA (11R, 4R)
            1: "Indication: Lung cancer staging.\nAnesthesia: General (LMA).\nProcedure:\n- Inspection: Normal anatomy (fused RUL segments). No lesions.\n- EBUS: 11R, 11Rs, 4R, 7, 2L, 4L identified. TBNA 11R (3 passes) & 4R (8 passes).\n- ROSE: Malignant.\n- EBL: 5cc. No complications.\nPlan: Recovery.",
            2: "OPERATIVE NARRATIVE: Under general anesthesia, a comprehensive airway examination was conducted using a Q190 video bronchoscope, revealing a fused apical/posterior segment of the RUL but otherwise unremarkable anatomy. Subsequently, a systematic convex probe endobronchial ultrasound (CP-EBUS) lymph node assessment was executed. Sonographic evaluation identified enlarged lymph nodes at stations 11Ri, 11Rs, 4R, 7, 2L, and 4L. Transbronchial needle aspiration (TBNA) was performed targeting the 11Rs and 4R stations using a 22-gauge needle. Rapid On-Site Evaluation (ROSE) of the aspirates suggested malignancy. The procedure concluded without immediate sequelae.",
            3: "CPT Justification: Bronchoscopy with EBUS-TBNA (31652).\nTechnique: Scope advanced to target nodes. Ultrasound localization confirmed node size >5mm at multiple stations.\n- Station 11Rs sampled (3 passes).\n- Station 4R sampled (8 passes).\nTotal of 2 distinct mediastinal/hilar stations sampled. Cytology obtained. ROSE performed.",
            4: "Resident Procedure Note\nAttending: [Attending Name]\nProcedure: EBUS-TBNA\n1. Time out performed.\n2. GA induced, LMA placed.\n3. Airway inspection: Normal mucosa, no masses.\n4. EBUS scope inserted. Systematic survey done.\n5. TBNA of 11R and 4R performed with 22G needle.\n6. ROSE: Positive for malignancy.\n7. Scope removed. Patient stable.",
            5: "we did the bronchoscopy for staging cancer used general anesthesia lma put in. airway looked fine except for the weird rul segment. switched to the ebus scope looked at all the nodes 11 4 7 2. poked the 11rs and the 4r with the 22 needle did a bunch of passes rose said it looks like cancer. minimal bleeding 5cc patient did fine sent to pacu.",
            6: "Diagnosis and staging of presumed lung cancer. General Anesthesia. Consent obtained. Inspection with Q190 bronchoscope showed normal anatomy except fused RUL segments. No endobronchial lesions. UC180F EBUS scope introduced. Nodes identified: 11ri, 11rs, 4r, 7, 2l, 4l. TBNA performed on 11Rs (3 biopsies) and 4R (8 biopsies) using 22G needle. ROSE consistent with malignancy. EBL 5cc. No complications. Stable transfer to recovery.",
            7: "[Indication]\nDiagnosis and staging of presumed lung cancer.\n[Anesthesia]\nGeneral Anesthesia (LMA).\n[Description]\nWhite light bronchoscopy revealed no endobronchial lesions. EBUS performed. Lymph nodes 11R and 4R met criteria and were sampled via TBNA (22G). ROSE confirmed likely malignancy. \n[Plan]\nAwait final pathology.",
            8: "The patient was brought to the bronchoscopy suite for staging of presumed lung cancer. After induction of general anesthesia, the airway was inspected, revealing no endobronchial abnormalities. We then utilized the linear EBUS scope to survey the mediastinum. Lymph nodes at stations 11R and 4R were selected for sampling based on size. Using a 22-gauge needle, we obtained aspirates from both stations. The on-site pathologist reviewed the slides and favored a diagnosis of malignancy. The patient tolerated the procedure well.",
            9: "Indications: Diagnosis and staging of presumed lung cancer. Medications: General Anesthesia. Following intravenous medications, the Q190 video bronchoscope was inserted through the mouth. The tracheobronchial tree was surveyed. Anatomy was normal aside from a fused apical and posterior segment of right upper lobe. The video bronchoscope was extracted and the UC180F convex probe EBUS bronchoscope was inserted. A systematic hilar and mediastinal lymph node survey was conducted. Sampling criteria were met in multiple nodes. Aspiration via transbronchial needle was executed with the Olympus 22 gauge needle on the 11Rs and 4R nodes. ROSE evaluation yielded tissue consistent with likely malignancy. All specimens were dispatched for cytology."
        },
        1: { # Note 1: Radial EBUS + TBNA (RLL)
            1: "Indication: RLL nodule.\nMethod: Radial EBUS + Fluoroscopy.\nFindings: Normal airway. RLL superior segment nodule localized (concentric view).\nAction: TBNA x6 (ROSE malignant). Forceps biopsies taken.\nComplication: Mild bleed, stopped with wedging.\nPlan: Discharge after CXR.",
            2: "PROCEDURAL REPORT: Diagnostic bronchoscopy was undertaken for a known pulmonary nodule in the right lower lobe superior segment. Initial airway inspection revealed sharp carina and healthy mucosa. A guide sheath was employed to navigate to the target lesion, where radial endobronchial ultrasound (R-EBUS) demonstrated a concentric orientation. Under fluoroscopic guidance, transbronchial needle aspiration and forceps biopsies were acquired. Immediate cytopathologic assessment (ROSE) confirmed malignancy. Hemostasis was achieved via bronchial wedging following minor hemorrhage.",
            3: "Coding: 31629 (TBNA), 31654 (Radial EBUS).\n- Localization: Radial probe inserted via guide sheath; concentric view obtained of RLL superior segment lesion.\n- Sampling: Needle aspiration (6 passes) performed under fluoroscopy. ROSE positive.\n- Biopsy: Forceps biopsies performed at same site.\n- Medical Necessity: Diagnosis of peripheral pulmonary nodule.",
            4: "Procedure Note\nProcedure: Bronchoscopy with Radial EBUS and Biopsy\nAirway: ETT\nSteps:\n1. Inspection: Normal anatomy.\n2. Navigation: Guide sheath to RLL superior segment.\n3. Verification: Radial EBUS showed concentric view.\n4. Sampling: TBNA x 6 and Forceps biopsy.\n5. Result: ROSE positive for cancer.\n6. Hemostasis: Wedging for 2 mins for mild bleed.",
            5: "patient here for lung cancer diagnosis used general anesthesia tube is in. went down with the scope airway looks fine. put the guide sheath into the rll superior segment used the radial ultrasound saw the lesion concentric view. took the probe out did 6 needle passes rose said malignant then did some biopsies with the forceps. started bleeding a bit so we wedged it for a couple minutes stopped fine. done.",
            6: "Diagnosis and staging of presumed lung cancer. General Anesthesia. T190 video bronchoscope introduced via ETT. Airways normal. Large guide sheath inserted to RLL superior segment. Radial ultrasound confirmed concentric view of lesion. Radial probe removed. 6 TBNAs obtained under fluoro. ROSE: malignancy. Forceps biopsies performed. Small bleeding resolved with wedging (2 min). Procedure completed.",
            7: "[Indication]\nDiagnosis of RLL pulmonary nodule.\n[Anesthesia]\nGeneral.\n[Description]\nScope to RLL superior segment. Lesion located via Radial EBUS (concentric). TBNA (6 passes) and forceps biopsies performed. ROSE confirmed malignancy. Mild bleeding controlled by wedging.\n[Plan]\nCXR to r/o PTX. Discharge.",
            8: "The patient was placed under general anesthesia for evaluation of a right lower lobe nodule. We inspected the airways and found no endobronchial lesions. We navigated to the superior segment of the right lower lobe using a guide sheath and confirmed the lesion's location with radial ultrasound, observing a concentric view. We proceeded to sample the lesion using transbronchial needle aspiration and forceps biopsies. The pathologist confirmed malignancy in the room. A small amount of bleeding occurred but stopped after we wedged the scope.",
            9: "Indications: Diagnosis and staging of presumed lung cancer. Medications: General Anesthesia. The T190 video bronchoscope was inserted via endotracheal tube. The tracheobronchial tree was surveyed. The large guide sheath catheter was inserted and the scope was navigated into the area of known pulmonary nodule within the superior segment of the right lower lobe. The radial ultrasound was inserted and the guide sheath was navigated into the segment of interest. Location was validated by radial probe with a concentric view. The radial probe was withdrawn and 6 TBNAs were acquired. ROSE confirmed the presence of malignancy. Samples were then taken with the radial jaw 4 forceps."
        },
        2: { # Note 2: EBUS (4R, 4L, 5) + Trans-vascular
            1: "Indication: Staging lung cancer.\nProcedure: EBUS-TBNA.\nNodes Sampled: 4R (benign), 4L (nondiagnostic). Station 5 sampled trans-vascularly (PA).\nTechnique: 25G and 22G needles used for Station 5 (7 passes).\nResult: Station 5 ROSE = Carcinoma.\nComplications: None.",
            2: "OPERATIVE SUMMARY: Following induction of general anesthesia, a systematic EBUS lymph node assessment was performed. Stations 4R and 4L were sampled via standard transbronchial approach; ROSE indicated benign lymphocytes and nondiagnostic tissue, respectively. To definitively stage the mediastinum, Station 5 (aortopulmonary window) was targeted. Due to anatomical constraints, a trans-vascular approach through the pulmonary artery was utilized. Seven passes were completed yielding poorly differentiated carcinoma. The patient tolerated this advanced maneuver without hemodynamic compromise.",
            3: "Codes: 31653 (EBUS 3+ stations).\nStation 1: 4R (TBNA).\nStation 2: 4L (TBNA).\nStation 3: Station 5 (Trans-vascular TBNA via Pulmonary Artery).\nNote: Trans-vascular approach is included in EBUS-TBNA codes. Total 3 stations sampled supporting 31653.",
            4: "Fellow Procedure Note\nIndication: Staging.\n1. EBUS scope inserted.\n2. 4R sampled -> benign.\n3. 4L sampled -> nondiagnostic.\n4. Decision made to biopsy Station 5 via PA (trans-vascular).\n5. 7 passes total to Station 5.\n6. ROSE: Carcinoma.\n7. No bleeding or complications.",
            5: "doing staging for lung cancer general anesthesia lma. looked around with the regular scope first normal. switched to ebus. poked 4r and 4l first 4r was benign 4l didn't get much. really needed to check station 5 so we went through the pulmonary artery scarry but it worked. did 7 passes there rose said poorly differentiated carcinoma. blood loss 10cc no issues.",
            6: "Diagnosis and staging of presumed lung cancer. General Anesthesia. Systematic EBUS survey performed. 4R and 4L sampled first (ROSE benign/nondiagnostic). Station 11L skipped. Station 5 sampled via trans-vascular route through pulmonary artery due to high suspicion. 7 passes total (5 with 25G, 2 with 22G). ROSE consistent with poorly differentiated carcinoma. No active bleeding post-procedure.",
            7: "[Indication]\nLung cancer staging.\n[Anesthesia]\nGeneral.\n[Description]\nEBUS performed. Stations 4R and 4L sampled. Station 5 sampled via trans-vascular approach (through PA). ROSE confirmed carcinoma at Station 5.\n[Plan]\nOncology referral.",
            8: "We proceeded with EBUS-TBNA for staging. We initially sampled the 4R and 4L lymph nodes. The 4R showed benign cells, and the 4L sample was insufficient. We identified a suspicious node at Station 5. To access this safely, we utilized a trans-vascular approach, passing the needle through the pulmonary artery. We performed seven passes in total. The preliminary results showed poorly differentiated carcinoma. The patient remained stable throughout this maneuver.",
            9: "Indications: Diagnosis and staging of presumed lung cancer. Medications: General Anesthesia. A systematic hilar and mediastinal lymph node survey was executed. Sampling by transbronchial needle aspiration was performed beginning with the 4R Lymph node, followed by the 4L. The 4R yielded benign lymphocytes on ROSE evaluation while the 4L was non-diagnostic. We decided to attempt sampling via the trans-vascular route through the pulmonary artery; a total of 7 passes were performed. ROSE was consistent with poorly differentiated carcinoma. All specimens were dispatched for routine cytology."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Mock data to assign consistent random names/ages to the variations for the 3 notes.
    """
    return [
        {"idx": 0, "orig_age": 65, "names": ["John Smith", "David Johnson", "Michael Williams", "Robert Brown", "James Jones", "William Miller", "Richard Davis", "Thomas Garcia", "Charles Rodriguez"]}, # Note 0
        {"idx": 1, "orig_age": 70, "names": ["Mary Wilson", "Patricia Martinez", "Jennifer Anderson", "Linda Taylor", "Elizabeth Thomas", "Barbara Hernandez", "Susan Moore", "Jessica Martin", "Sarah Jackson"]}, # Note 1
        {"idx": 2, "orig_age": 62, "names": ["Joseph Thompson", "Thomas White", "Christopher Lopez", "Daniel Lee", "Paul Gonzalez", "Mark Harris", "Donald Clark", "George Lewis", "Kenneth Robinson"]}, # Note 2
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
            break 
            
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
            
            # Get the specific name 
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            # Handle cases where we might have fewer text variations than notes (safety check)
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            
            # Update registry_entry fields if they exist
            if "registry_entry" in note_entry and note_entry["registry_entry"]:
                # Create registry_entry if it was null in source (though uncommon in this dataset)
                if note_entry["registry_entry"] is None:
                     note_entry["registry_entry"] = {}

                # Update patient MRN to make it unique
                current_mrn = note_entry["registry_entry"].get("patient_mrn", "UNKNOWN")
                note_entry["registry_entry"]["patient_mrn"] = f"{current_mrn}_syn_{style_num}"
                
                # Update date
                note_entry["registry_entry"]["procedure_date"] = rand_date_str
                
                # Update demographics if present, otherwise inject for realism
                if "patient_demographics" not in note_entry["registry_entry"] or note_entry["registry_entry"]["patient_demographics"] is None:
                    note_entry["registry_entry"]["patient_demographics"] = {}
                
                note_entry["registry_entry"]["patient_demographics"]["age_years"] = new_age
                # We don't have gender in the mock, keeping original or null if not present
                
            
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
    output_filename = output_dir / "synthetic_bronch_notes_part_004.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()