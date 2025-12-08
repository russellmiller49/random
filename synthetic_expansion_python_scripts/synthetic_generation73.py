import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_073.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    """Generates a random date within the given year range."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    """
    Returns a dictionary of manually crafted text variations.
    Structure: Note_Index (0-5) -> Style_Index (1-9) -> Text
    """
    variations = {
        0: { # Samuel Ortiz (TBNA Station 7)
            1: "Indication: RLL mass, mediastinal staging.\nAnesthesia: Moderate (Versed/Fentanyl).\nProcedure:\n- Scope passed orally.\n- Normal vocal cords/trachea.\n- Station 7 subcarinal node identified.\n- 21G Wang needle used for conventional TBNA (no EBUS).\n- 4 passes complete.\n- ROSE: Malignant cells present.\nComplications: Minimal bleeding.\nPlan: Discharge. Tumor board.",
            2: "HISTORY: Mr. Ortiz, a 68-year-old male with a right lower lobe mass and PET-avid subcarinal adenopathy, presented for diagnostic bronchoscopy.\nPROCEDURE: Under moderate sedation, a flexible bronchoscope was introduced. Inspection of the tracheobronchial tree revealed no endobronchial lesions. Utilizing conventional transbronchial needle aspiration (TBNA) techniques based on anatomic landmarks, the subcarinal lymph node (Station 7) was sampled with a 21-gauge Wang needle. Four passes were obtained. Rapid on-site evaluation (ROSE) confirmed the presence of malignant epithelial cells consistent with metastatic carcinoma.\nIMPRESSION: Successful staging bronchoscopy confirming N2 disease.",
            3: "Procedure: Bronchoscopy with Transbronchial Needle Aspiration (CPT 31629).\nDevice: 21-gauge Wang Needle.\nSite: Subcarinal Lymph Node (Station 7).\nTechnique: Conventional TBNA using anatomic landmarks (blind aspiration); no endobronchial ultrasound (EBUS) utilized. Four passes were performed to ensure adequate cellularity.\nSpecimen: Cytology and cell block. ROSE confirmed malignancy.\nJustification: Mediastinal staging for lung cancer.",
            4: "Procedure Note\nPatient: Samuel Ortiz\nAttending: Dr. Desai\nProcedure: Flex Bronch, Conventional TBNA\n\nSteps:\n1. Time out performed.\n2. Moderate sedation administered.\n3. Scope inserted; airway inspection normal.\n4. Wang needle passed to Station 7 (subcarinal).\n5. 4 passes performed using landmark guidance.\n6. ROSE positive for carcinoma.\n7. Scope withdrawn.\n\nComplications: None.\nPlan: Discharge home.",
            5: "procedure note for samuel ortiz 68m we did a bronchoscopy today for staging of that lung mass sedation was fine used midazolam and fentanyl scope went down easy airway looked clear except for some compression near the carina used the wang needle 21 gauge on station 7 subcarinal node did 4 passes got good samples rose said it was cancer so we stopped bleeding was minimal patient tolerating well plan is oncology referral",
            6: "The patient, a 68-year-old male, underwent flexible bronchoscopy with conventional TBNA for mediastinal staging. Moderate sedation was provided. A flexible bronchoscope was introduced orally. The airway inspection was unremarkable. A 21-gauge Wang needle was used to aspirate the subcarinal lymph node (Station 7) utilizing anatomic landmarks without ultrasound guidance. Four passes were performed. On-site cytology confirmed metastatic carcinoma. There were no complications. The patient was discharged in stable condition.",
            7: "[Indication]\nMediastinal staging for suspected NSCLC, RLL mass, Station 7 adenopathy.\n[Anesthesia]\nModerate sedation (Midazolam/Fentanyl).\n[Description]\nFlexible bronchoscopy performed. Normal airway anatomy. Conventional TBNA of Station 7 performed using 21G Wang needle (4 passes). ROSE confirmed malignancy.\n[Plan]\nDischarge. Tumor board review.",
            8: "After obtaining informed consent, the patient was brought to the bronchoscopy suite and placed under moderate sedation. A flexible bronchoscope was introduced through the mouth. We inspected the airway and found no endobronchial abnormalities. We then targeted the subcarinal lymph node (Station 7) for staging using a conventional 21-gauge Wang needle. Four needle passes were performed based on anatomic landmarks. The on-site pathologist confirmed the presence of malignant cells. The procedure was completed without any significant complications.",
            9: "OPERATION: Flexible endoscopy with needle sampling of mediastinal node.\nINDICATION: Lung mass with enlarged lymph node.\nDETAILS: Under sedation, the scope was inserted. The subcarinal node (Station 7) was accessed using a Wang needle via conventional technique. Four samples were extracted. Rapid analysis indicated malignancy. The instrument was removed. The patient recovered well."
        },
        1: { # Laura Benson (TBNA Station 7, GA)
            1: "Dx: LUL mass, subcarinal adenopathy.\nAnesthesia: GA, 8.0 ETT.\nProcedure: Bronchoscopy with TBNA.\n- Scope via ETT.\n- Normal airway inspection.\n- Station 7 targeted w/ 22G Wang needle (conventional).\n- 3 passes.\n- ROSE: Malignant.\nComplications: None.\nDisposition: PACU.",
            2: "INDICATION: Mrs. Benson, a 62-year-old female with a central left upper lobe mass, underwent mediastinal staging.\nPROCEDURE: The patient was placed under general anesthesia with endotracheal intubation. A flexible bronchoscope was advanced. The tracheobronchial tree was patent. Conventional transbronchial needle aspiration (TBNA) of the subcarinal lymph node (Station 7) was performed using a 22-gauge Wang needle and anatomic landmarks. Three passes yielded diagnostic material confirmed by rapid on-site evaluation to be metastatic non-small cell lung carcinoma.\nCONCLUSION: Positive mediastinal staging (N2 disease).",
            3: "Service: Bronchoscopy with TBNA (31629).\nTarget: Subcarinal Lymph Node (Station 7).\nMethod: Conventional TBNA using 22-gauge Wang needle. Anatomic landmarks used for guidance (EBUS not utilized).\nSpecimen: 3 passes obtained for cytology and cell block. ROSE confirmed malignancy.\nAnesthesia: General anesthesia with ETT.",
            4: "Resident Procedure Note\nPatient: Laura Benson\nProcedure: Conventional TBNA Station 7\nStaff: Dr. Romero\n\n1. Pt intubated/GA.\n2. Scope passed through ETT.\n3. Airway exam: Normal.\n4. Needle (Wang 22G) used to sample Station 7.\n5. 3 passes completed.\n6. ROSE: Positive for malignancy.\n7. Tolerated well.\n\nPlan: Extubate, PACU.",
            5: "note for laura benson 62f procedure bronchoscopy with tbna indication lung mass subcarinal node anesthesia general with ett tube scope went in fine airway normal used 22g wang needle on station 7 did 3 passes rose showed cancer cells no bleeding patient stable extubated in or sent to recovery",
            6: "Laura Benson, a 62-year-old female, underwent flexible bronchoscopy with conventional TBNA for mediastinal staging of a central lung mass. General anesthesia was used. A bronchoscope was passed through the endotracheal tube. The airway was inspected and found to be normal. A 22-gauge Wang needle was used to aspirate the subcarinal lymph node (Station 7) using anatomic landmarks. Three passes were performed. Rapid on-site evaluation showed malignant cells. No complications occurred. The patient was extubated and transferred to the PACU.",
            7: "[Indication]\nMediastinal staging, LUL mass, Station 7 adenopathy.\n[Anesthesia]\nGeneral anesthesia (ETT).\n[Description]\nFlexible bronchoscopy via ETT. Conventional TBNA of Station 7 performed using 22G Wang needle (3 passes). ROSE confirmed malignancy. No EBUS used.\n[Plan]\nExtubate. Oncology follow-up.",
            8: "The patient was brought to the operating room and placed under general anesthesia with an endotracheal tube. A flexible bronchoscope was introduced through the tube. We inspected the airways and noted no endobronchial lesions. Using a 22-gauge Wang needle, we performed conventional transbronchial needle aspiration of the subcarinal lymph node (Station 7). Three passes were made, and on-site cytology confirmed metastatic carcinoma. The procedure concluded without complications, and the patient was extubated.",
            9: "PROCEDURE: Bronchoscopy with blind needle aspiration of subcarinal node.\nREASON: Central lung mass with nodal involvement.\nTECHNIQUE: Under general anesthesia, the scope was introduced. The Station 7 node was sampled using a Wang needle via conventional landmarks. Three samples were obtained. Rapid analysis showed carcinoma. The patient was awakened and extubated."
        },
        2: { # Omar Rahman (TBNA Station 4L)
            1: "Indication: 4L adenopathy, r/o sarcoid vs lymphoma.\nAnesthesia: Moderate.\nProcedure: Flex bronch.\n- Airway normal.\n- Station 4L targeted w/ 21G Wang needle.\n- 4 passes.\n- ROSE: Granulomas (benign).\nComplications: None.\nPlan: Rheumatology referral.",
            2: "HISTORY: Mr. Rahman presented with isolated left lower paratracheal lymphadenopathy for tissue diagnosis.\nPROCEDURE: Under moderate sedation, flexible bronchoscopy was performed. The airway examination was unremarkable. Conventional transbronchial needle aspiration (TBNA) of the Station 4L lymph node was executed using a 21-gauge Wang needle based on anatomic landmarks. Four passes were obtained. Rapid on-site evaluation revealed non-necrotizing granulomas consistent with sarcoidosis, ruling out lymphoma.\nIMPRESSION: TBNA consistent with granulomatous inflammation.",
            3: "Procedure: Bronchoscopy with Transbronchial Needle Aspiration (31629).\nSite: Left Lower Paratracheal Node (Station 4L).\nDevice: 21-gauge Wang Needle.\nTechnique: Conventional blind aspiration using anatomic landmarks. No EBUS utilized.\nSpecimen: 4 passes for cytology, cell block, and culture. ROSE showed granulomas.\nDiagnosis: Sarcoidosis suspected.",
            4: "Procedure Note\nPatient: Omar Rahman\nAttending: Dr. Grant\nProcedure: Bronchoscopy, TBNA 4L\n\nSteps:\n1. Time out.\n2. Sedation (Versed/Fentanyl).\n3. Scope inserted.\n4. Exam normal.\n5. Wang needle used for 4L node.\n6. 4 passes.\n7. ROSE: Granulomas.\n8. Cultures sent.\n\nPlan: Discharge, Rheum consult.",
            5: "bronch note for omar rahman 59m indx adenopathy rule out sarcoid sedation moderate scope in airway clear except for some compression on the left used wang needle on 4l node did 4 passes rose showed granulomas no cancer seen minimal bleeding patient did well discharge home",
            6: "The patient, a 59-year-old male, underwent flexible bronchoscopy for evaluation of mediastinal lymphadenopathy. Moderate sedation was administered. A flexible bronchoscope was inserted. The airway was patent. A 21-gauge Wang needle was used to perform conventional TBNA of the left lower paratracheal lymph node (Station 4L). Four passes were obtained. On-site cytology revealed non-necrotizing granulomas. There were no complications. The patient was discharged home.",
            7: "[Indication]\nIsolated 4L adenopathy, r/o sarcoidosis vs lymphoma.\n[Anesthesia]\nModerate sedation.\n[Description]\nFlexible bronchoscopy performed. Conventional TBNA of Station 4L using 21G Wang needle (4 passes). ROSE showed granulomas. Cultures sent.\n[Plan]\nDischarge. Rheumatology referral.",
            8: "Following consent, the patient was sedated with midazolam and fentanyl. We introduced the bronchoscope and inspected the tracheobronchial tree, which appeared normal. We then directed our attention to the left lower paratracheal station (4L) and performed conventional TBNA using a 21-gauge Wang needle. Four passes were completed. Rapid on-site evaluation demonstrated granulomas, suggesting sarcoidosis. The procedure was well-tolerated.",
            9: "OPERATION: Endoscopy with needle sampling of left paratracheal node.\nREASON: Lymphadenopathy, check for sarcoid.\nDETAILS: Under sedation, the scope was passed. The Station 4L node was accessed using a Wang needle via landmarks. Four samples were taken. Rapid testing showed granulomas. The instrument was removed. Patient stable."
        },
        3: { # Brenda Howard (TBNA Station 4L)
            1: "Indication: Breast ca hx, 4L node.\nAnesthesia: GA, 7.5 ETT.\nProcedure: Bronch w/ TBNA.\n- Scope via ETT.\n- 4L node sampled w/ 22G Wang needle.\n- 3 passes.\n- ROSE: Malignant (likely metastatic breast).\nComplications: None.\nPlan: Oncology f/u.",
            2: "HISTORY: Ms. Howard, 71, with a history of breast cancer, presented with new 4L lymphadenopathy.\nPROCEDURE: Under general anesthesia, a flexible bronchoscope was introduced via endotracheal tube. The airway was inspected. Conventional TBNA of the left lower paratracheal (Station 4L) node was performed using a 22-gauge Wang needle. Three passes were obtained. ROSE confirmed atypical cells suspicious for metastatic carcinoma. Material was sent for immunohistochemistry.\nIMPRESSION: TBNA Station 4L positive for malignancy.",
            3: "Service: Bronchoscopy with TBNA (31629).\nTarget: Station 4L (Left Lower Paratracheal).\nDevice: 22-gauge Wang Needle.\nMethod: Conventional aspiration via anatomic landmarks (No EBUS).\nSpecimen: 3 passes for cytology/IHC. ROSE positive for malignancy.\nIndication: Staging of mediastinal recurrence.",
            4: "Resident Note\nPatient: Brenda Howard\nProcedure: TBNA Station 4L\nStaff: Dr. Li\n\n1. GA/Intubation.\n2. Scope passed.\n3. 4L node identified via landmarks.\n4. Wang needle used for 3 passes.\n5. ROSE: Malignant cells.\n6. Scope removed.\n\nPlan: Extubate, PACU, Onc f/u.",
            5: "proc note brenda howard 71f hx breast cancer now has 4l node went in with general anesthesia ett tube scope looks good airway normal used 22g wang needle on 4l did 3 passes rose said cancer cells suspicious for breast met no bleeding extubated fine plan oncology",
            6: "Brenda Howard underwent flexible bronchoscopy with conventional TBNA to evaluate a PET-avid 4L node. General anesthesia was used. The bronchoscope was introduced through the ETT. A 22-gauge Wang needle was used to sample the left lower paratracheal node (Station 4L) using anatomic landmarks. Three passes were performed. On-site cytology showed malignant cells. No complications occurred. The patient was transferred to the PACU.",
            7: "[Indication]\nBreast cancer hx, PET-avid 4L node.\n[Anesthesia]\nGeneral anesthesia (ETT).\n[Description]\nFlexible bronchoscopy via ETT. Conventional TBNA of Station 4L using 22G Wang needle (3 passes). ROSE confirmed malignancy. IHC pending.\n[Plan]\nExtubate. Oncology referral.",
            8: "The patient was placed under general anesthesia. We advanced the bronchoscope through the endotracheal tube and surveyed the airway. Using anatomic landmarks, we identified the location of the left lower paratracheal node (Station 4L). We performed conventional TBNA using a 22-gauge Wang needle, obtaining three passes. On-site evaluation was consistent with metastatic disease. The procedure ended without incident.",
            9: "PROCEDURE: Bronchoscopy with blind needle biopsy of paratracheal node.\nREASON: Possible metastatic breast cancer.\nTECHNIQUE: Under general anesthesia, the scope was inserted. The Station 4L node was sampled with a Wang needle. Three samples were taken. Rapid analysis confirmed malignancy. The patient was awakened."
        },
        4: { # Victor Lin (TBNA Station 4R)
            1: "Indication: RUL mass, 4R node.\nAnesthesia: Moderate.\nProcedure: Flex bronch.\n- Airway normal.\n- Station 4R targeted w/ 21G Wang needle.\n- 3 passes.\n- ROSE: NSCLC.\nComplications: Minimal bleeding.\nPlan: Tumor board.",
            2: "HISTORY: Mr. Lin presented with a right upper lobe mass and ipsilateral mediastinal adenopathy.\nPROCEDURE: Under moderate sedation, flexible bronchoscopy was performed. Conventional TBNA of the right lower paratracheal (Station 4R) lymph node was executed using a 21-gauge Wang needle and anatomic landmarks. Three passes yielded diagnostic material. ROSE confirmed non-small cell lung carcinoma.\nIMPRESSION: N2 positive NSCLC.",
            3: "Procedure: Bronchoscopy with Transbronchial Needle Aspiration (31629).\nSite: Right Lower Paratracheal Node (Station 4R).\nDevice: 21-gauge Wang Needle.\nTechnique: Blind aspiration using anatomic landmarks (No EBUS).\nSpecimen: 3 passes for cytology/molecular. ROSE positive for NSCLC.\nJustification: Staging of lung cancer.",
            4: "Procedure Note\nPatient: Victor Lin\nAttending: Dr. Moore\nProcedure: TBNA Station 4R\n\nSteps:\n1. Moderate sedation.\n2. Scope inserted.\n3. 4R node identified.\n4. Wang needle used for 3 passes.\n5. ROSE: Positive for NSCLC.\n6. No complications.\n\nPlan: Discharge, Tumor Board.",
            5: "bronch note victor lin 64m lung mass 4r node sedation moderate scope down airway ok used wang needle 21g on station 4r did 3 passes rose showed nsclc minimal bleeding stopped on its own patient stable discharge home",
            6: "Victor Lin, a 64-year-old male, underwent flexible bronchoscopy with conventional TBNA for staging of a right upper lobe mass. Moderate sedation was administered. The bronchoscope was inserted orally. A 21-gauge Wang needle was used to sample the right lower paratracheal node (Station 4R) using anatomic landmarks. Three passes were obtained. On-site cytology confirmed non-small cell lung carcinoma. The procedure was uncomplicated.",
            7: "[Indication]\nRUL mass, 4R adenopathy, staging.\n[Anesthesia]\nModerate sedation.\n[Description]\nFlexible bronchoscopy performed. Conventional TBNA of Station 4R using 21G Wang needle (3 passes). ROSE confirmed NSCLC. Molecular testing sent.\n[Plan]\nDischarge. Tumor board.",
            8: "After informed consent, the patient was sedated and the bronchoscope was introduced. We inspected the airway and then targeted the right lower paratracheal node (Station 4R) for staging. Using a 21-gauge Wang needle and conventional technique, we performed three passes. Rapid on-site evaluation confirmed malignant cells compatible with NSCLC. The patient tolerated the procedure well.",
            9: "OPERATION: Endoscopy with needle sampling of right paratracheal node.\nREASON: Lung cancer staging.\nDETAILS: Under sedation, the scope was passed. The Station 4R node was accessed with a Wang needle. Three samples were extracted. Rapid testing showed cancer. The instrument was removed."
        },
        5: { # Evelyn Carter (TBNA Station 4R)
            1: "Indication: RUL adenocarcinoma, confirm N2 (4R).\nAnesthesia: GA, 8.0 ETT.\nProcedure: Bronch w/ TBNA.\n- Scope via ETT.\n- Station 4R sampled w/ 22G Wang needle.\n- 4 passes.\n- ROSE: Adenocarcinoma.\nComplications: None.\nPlan: Multimodality therapy.",
            2: "HISTORY: Ms. Carter, with known RUL adenocarcinoma, presented for confirmation of mediastinal involvement.\nPROCEDURE: Under general anesthesia, flexible bronchoscopy was performed via ETT. Conventional TBNA of the Station 4R lymph node was conducted using a 22-gauge Wang needle. Four passes were obtained. ROSE confirmed metastatic adenocarcinoma, establishing N2 disease.\nIMPRESSION: Stage IIIA NSCLC.",
            3: "Service: Bronchoscopy with TBNA (31629).\nTarget: Station 4R (Right Lower Paratracheal).\nDevice: 22-gauge Wang Needle.\nMethod: Conventional aspiration via anatomic landmarks (No EBUS).\nSpecimen: 4 passes for cytology/molecular. ROSE confirmed malignancy.\nIndication: Confirmation of N2 disease.",
            4: "Resident Note\nPatient: Evelyn Carter\nProcedure: TBNA Station 4R\nStaff: Dr. Cole\n\n1. GA/Intubation.\n2. Scope passed.\n3. 4R node targeted.\n4. Wang needle used for 4 passes.\n5. ROSE: Adenocarcinoma.\n6. Scope removed.\n\nPlan: Extubate, PACU, Oncology.",
            5: "note for evelyn carter 73f known rul cancer need to check 4r node general anesthesia tube in scope down airway normal used 22g wang needle on 4r did 4 passes rose positive for adeno no bleeding patient extubated plan chemo rads",
            6: "Evelyn Carter underwent flexible bronchoscopy with conventional TBNA to confirm N2 disease. General anesthesia was used. A 22-gauge Wang needle was used to sample the right lower paratracheal node (Station 4R) through the endotracheal tube using anatomic landmarks. Four passes were performed. On-site cytology confirmed adenocarcinoma. There were no complications. The patient was transferred to the PACU.",
            7: "[Indication]\nRUL adenocarcinoma, PET-avid 4R node.\n[Anesthesia]\nGeneral anesthesia (ETT).\n[Description]\nFlexible bronchoscopy via ETT. Conventional TBNA of Station 4R using 22G Wang needle (4 passes). ROSE confirmed adenocarcinoma.\n[Plan]\nExtubate. Multimodality therapy.",
            8: "The patient was placed under general anesthesia. We introduced the bronchoscope through the ETT. We identified the landmark for the right lower paratracheal node (Station 4R) and performed conventional TBNA using a 22-gauge Wang needle. Four passes were obtained, and on-site evaluation confirmed metastatic adenocarcinoma. The procedure was completed without complications.",
            9: "PROCEDURE: Bronchoscopy with blind needle biopsy of right paratracheal node.\nREASON: Confirm cancer spread.\nTECHNIQUE: Under general anesthesia, the scope was inserted. The Station 4R node was sampled with a Wang needle. Four samples were taken. Rapid analysis confirmed adenocarcinoma. The patient was awakened."
        }
    }
    return variations

def get_base_data_mocks():
    """
    Returns mock data for name replacement.
    Structure matches the input file indices.
    """
    return [
        {
            "idx": 0, 
            "orig_name": "Samuel Ortiz", 
            "orig_age": 68, 
            "names": ["Juan Perez", "Carlos Gomez", "Miguel Rodriguez", "Jose Martinez", "Luis Fernandez", "Antonio Lopez", "Manuel Diaz", "Pedro Sanchez", "Jorge Ramirez"]
        },
        {
            "idx": 1, 
            "orig_name": "Laura Benson", 
            "orig_age": 62, 
            "names": ["Sarah Miller", "Emily Davis", "Jessica Wilson", "Ashley Taylor", "Amanda Anderson", "Jennifer Thomas", "Nicole Jackson", "Stephanie White", "Melissa Harris"]
        },
        {
            "idx": 2, 
            "orig_name": "Omar Rahman", 
            "orig_age": 59, 
            "names": ["Ali Khan", "Hassan Ahmed", "Yusuf Malik", "Ibrahim Sayed", "Mohammed Ali", "Ahmed Costello", "Mustafa Lewis", "Hamza Robinson", "Bilal Walker"]
        },
        {
            "idx": 3, 
            "orig_name": "Brenda Howard", 
            "orig_age": 71, 
            "names": ["Mary Smith", "Patricia Johnson", "Linda Williams", "Barbara Brown", "Elizabeth Jones", "Jennifer Garcia", "Maria Miller", "Susan Davis", "Margaret Rodriguez"]
        },
        {
            "idx": 4, 
            "orig_name": "Victor Lin", 
            "orig_age": 64, 
            "names": ["David Chen", "Michael Wang", "James Lee", "John Liu", "Robert Zhang", "William Yang", "Richard Wu", "Thomas Ng", "Charles Huang"]
        },
        {
            "idx": 5, 
            "orig_name": "Evelyn Carter", 
            "orig_age": 73, 
            "names": ["Martha Jones", "Dorothy Wilson", "Betty Taylor", "Helen Anderson", "Nancy Thomas", "Sandra Jackson", "Carol White", "Ruth Harris", "Sharon Martin"]
        }
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
            
            # Get the specific name assigned
            new_name = record['names'][style_num - 1]
            
            # Update note_text with the variation
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing variation text for Note {idx}, Style {style_num}")
                continue
            
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
    output_filename = output_dir / "synthetic_tbna_conventional_wang_part_073.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()