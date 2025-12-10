import json
import random
import datetime
import copy
from pathlib import Path

# Source file for JSON elements
SOURCE_FILE = "golden_extractions/consolidated_verified_notes_v2_8_part_016.json"
OUTPUT_DIR = "Synthetic_expansions"

def generate_random_date(start_year, end_year):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + (end - start) * random.random()

def get_variations():
    # Structure: Note_Index (0-5) -> Style_Index (1-9) -> Text
    
    variations = {
        0: { # Jennifer Wang (EBUS + RUL Biopsy)
            1: "Indication: RUL mass, staging.\nProcedure: EBUS-TBNA + Bronchoscopy.\n- EBUS: Stations 2R, 4R, 7, 10R sampled. ROSE positive 2R, 4R, 7.\n- Bronchoscopy: RUL mass biopsied (forceps x6, brush x2).\nComplications: Moderate bleeding, controlled w/ epi.\nPlan: Oncology.",
            2: "PROCEDURE: Combined Endobronchial Ultrasound and Fiberoptic Bronchoscopy.\nCLINICAL SUMMARY: Ms. Wang presented with a right upper lobe neoplasm and bulky mediastinal adenopathy. \nOPERATIVE FINDINGS: Systematic EBUS evaluation (N3-N1) was conducted. Transbronchial needle aspiration of stations 2R, 4R, 7, and 10R was performed. Cytopathology confirmed malignancy in the mediastinal stations. Subsequently, the RUL endobronchial component was interrogated, revealing partial obstruction. Forceps biopsies and brushings were obtained.\nIMPRESSION: Stage IIIB Non-Small Cell Lung Carcinoma.",
            3: "CPT Coding Summary:\n- 31653 (EBUS-TBNA 3+ stations): Stations 2R, 4R, 7, and 10R were aspirated. ROSE confirms sampling adequacy.\n- 31625 (Endobronchial Biopsy): Distinct procedure on RUL tumor mass (separate from nodes). 6 forceps bites taken.\nMedical Necessity: Diagnostic and staging for lung cancer.",
            4: "Procedure Note\nPt: Jennifer Wang\nAttending: Dr. X\nSteps:\n1. Mod sedation.\n2. EBUS scope inserted.\n3. Sampled 2R, 4R, 7, 10R. 4R sent for molecular.\n4. Switched to standard scope.\n5. Biopsied RUL mass (forceps/brush).\n6. Hemostasis achieved with cold saline/epi.\nPlan: Tumor board.",
            5: "Jennifer Wang here for the staging and biopsy RUL mass. We gave midazolam and fentanyl she did okay. Did the EBUS first hit 2R 4R 7 and 10R. ROSE said cancer in the first three. Then went to the RUL saw the tumor blocking the airway a bit took 6 biopsies and brushed it. Bled a fair amount had to use epi and iced saline but it stopped. Recovering now.",
            6: "Bronchoscopy with EBUS performed for Jennifer Wang 10/22/2024. Indication RUL mass staging. Moderate sedation. EBUS-TBNA of stations 2R 4R 7 10R performed. Malignancy confirmed on ROSE for 2R 4R 7. Endobronchial biopsy of RUL mass performed x6 plus brushing. Moderate bleeding controlled intraoperatively. Patient stable.",
            7: "[Indication]\nRUL mass with mediastinal lymphadenopathy.\n[Anesthesia]\nModerate sedation (Versed/Fentanyl).\n[Description]\nEBUS-TBNA performed on stations 2R, 4R, 7, 10R. Positive for malignancy. RUL endobronchial mass biopsied (forceps/brush).\n[Plan]\nOncology referral, molecular testing pending.",
            8: "Ms. Wang was brought to the bronchoscopy suite for evaluation of her right upper lobe mass. Under moderate sedation, we initiated the procedure with EBUS-TBNA for staging. We systematically sampled stations 2R, 4R, 7, and 10R. Rapid on-site evaluation confirmed malignant cells in the mediastinal nodes. We then proceeded to direct bronchoscopy, visualizing the tumor in the right upper lobe bronchus. Forceps biopsies and brushings were collected. Moderate bleeding was noted but successfully managed with topical epinephrine.",
            9: "Indication: Pulmonary lesion and adenopathy.\nAction: Sonographic interrogation of mediastinum (EBUS).\nSampling: Aspirated stations 2R, 4R, 7, 10R. Harvested tissue from RUL mass via forceps and brush.\nResult: Malignancy confirmed. Hemostasis secured."
        },
        1: { # Mark Thompson (Traditional Bronch + REBUS - RLL Nodule)
            1: "Indication: RLL nodule (21mm).\nTechnique: Fluoroscopy + Radial EBUS (No EMN).\nFindings: Bronchus sign positive. REBUS eccentric.\nSampling: TBNA x3, Forceps x8 (5+3), Brush x2.\nComp: Minor bleeding.\nResult: Diagnostic.",
            2: "PROCEDURE: Flexible bronchoscopy with radial EBUS and fluoroscopic guidance.\nINDICATIONS: Evaluation of a 21mm solid nodule in the right lower lobe exhibiting a positive bronchus sign.\nDESCRIPTION: The bronchoscope was advanced to the RLL. Utilizing the anatomic bronchus sign, the lesion was localized. Radial probe EBUS confirmed the target (eccentric view). Under fluoroscopic visualization, transbronchial needle aspiration, forceps biopsies, and bronchial brushings were performed. \nCONCLUSION: Successful sampling of RLL pulmonary nodule.",
            3: "Code Selection:\n- 31629 (Primary): Transbronchial needle aspiration of RLL nodule.\n- 31628 (Bundled per NCCI): Transbronchial biopsy of RLL nodule (same lesion).\n- 31654 (Add-on): Radial EBUS used for target confirmation.\nNote: Navigation (31627) NOT used/billed; procedure relied on fluoroscopy and bronchus sign.",
            4: "Resident Note\nPt: Mark Thompson\nIndication: RLL nodule\n1. Sedation (Versed/Fent).\n2. Scope to RLL.\n3. Found bronchus leading to nodule.\n4. Confirmed with Radial EBUS (eccentric).\n5. TBNA x3.\n6. Biopsies x8 and Brush x2 under fluoro.\n7. No pneumo on post-procedure CXR.",
            5: "Mark Thompson 64M RLL nodule. We didn't use the robot or nav just regular scope cause there was a clear airway to it. Put the radial probe in saw the lesion eccentric. Did needle aspirates then biopsies and brushing. Little bit of bleeding stopped quick. Xray showed no pneumothorax.",
            6: "RLL nodule biopsy for Mark Thompson. Moderate sedation. Traditional bronchoscopy used. Lesion localized via bronchus sign and confirmed with Radial EBUS (eccentric) and Fluoroscopy. TBNA x3, TBBx x8, Brush x2 performed. Minor bleeding controlled. Post-proc CXR negative for PTX.",
            7: "[Indication]\nRLL solid nodule 21mm.\n[Anesthesia]\nModerate.\n[Description]\nGuided by fluoroscopy and REBUS (eccentric). TBNA, Forceps Biopsy, and Brushing of RLL nodule performed.\n[Plan]\nDischarge. Follow up pathology.",
            8: "Mr. Thompson presented for biopsy of a right lower lobe nodule. Due to the presence of a clear bronchus sign, we utilized traditional bronchoscopy with fluoroscopy and radial EBUS verification rather than electromagnetic navigation. The radial probe demonstrated an eccentric view of the lesion. We obtained diagnostic tissue using a combination of needle aspiration, forceps biopsy, and brushing. The patient tolerated the procedure well with only minor bleeding.",
            9: "Indication: RLL lesion interrogation.\nMethod: Conventional bronchoscopy with sonographic and fluoroscopic aid.\nExecution: Located target. Deployed needle for aspiration. Utilized forceps for tissue acquisition. Brushed airway.\nOutcome: Samples secured. No pneumothorax."
        },
        2: { # Sandra Lopez (EBUS Breast CA Hx)
            1: "Indication: Mediastinal LAD, Hx Breast CA.\nProcedure: EBUS-TBNA.\nNodes: 2R (8mm), 4R (12mm), 7 (9mm).\nFindings: All ROSE positive for metastatic breast adenocarcinoma.\nPlan: Oncology.",
            2: "PROCEDURE: Endobronchial Ultrasound-Guided Transbronchial Needle Aspiration.\nCLINICAL HISTORY: 70-year-old female with history of breast carcinoma and CKD presenting with mediastinal adenopathy.\nFINDINGS: Systematic EBUS evaluation revealed lymphadenopathy. Transbronchial needle aspiration was performed at stations 2R, 4R, and 7. Rapid on-site evaluation confirmed metastatic adenocarcinoma consistent with breast primary.\nIMPRESSION: Recurrent metastatic breast carcinoma.",
            3: "Billing: 31653 (EBUS 3+ stations).\nDocumentation supports sampling of:\n1. Station 2R\n2. Station 4R\n3. Station 7\nDiagnosis: Secondary malignant neoplasm of respiratory system. \nNote: Moderate sedation used despite CKD.",
            4: "Procedure: EBUS\nPt: Sandra Lopez\nIndication: Staging/Dx (Hx Breast CA)\nSteps:\n1. Mod sedation.\n2. EBUS scope passed.\n3. Sampled 2R, 4R, 7.\n4. ROSE: Mets from breast.\n5. Stable, no complications.\nPlan: Refer to onc.",
            5: "Sandra Lopez history of breast cancer came in for nodes. We did EBUS used midazolam fentanyl careful with the kidneys. Sampled 2R 4R and 7. They all came back positive for breast cancer recurrence on the rapid read. No complications sending her back to nephrology and oncology.",
            6: "EBUS-TBNA for Sandra Lopez (Hx Breast CA, CKD). Stations 2R, 4R, 7 sampled. ROSE confirmed metastatic adenocarcinoma (breast origin). Systematic evaluation performed. No complications. Oncology referral planned.",
            7: "[Indication]\nMediastinal lymphadenopathy, history of breast cancer.\n[Anesthesia]\nModerate sedation.\n[Description]\nEBUS-TBNA of stations 2R, 4R, and 7. Cytology confirmed metastatic breast cancer.\n[Plan]\nOncology for systemic therapy.",
            8: "Ms. Lopez, with a known history of breast cancer, underwent EBUS-TBNA to investigate new mediastinal lymphadenopathy. Despite her chronic kidney disease, she tolerated moderate sedation well. We identified and sampled nodes at stations 2R, 4R, and 7. All stations yielded positive results for metastatic breast adenocarcinoma on preliminary evaluation. We have referred her back to oncology.",
            9: "Indication: Suspected recurrence.\nTechnique: Ultrasonic needle aspiration.\nTargets: 2R, 4R, 7.\nAnalysis: Samples demonstrated metastatic cells.\nDisposition: Outpatient discharge."
        },
        3: { # Donald Martinez (Teaching Case)
            1: "Indication: Staging LUL Adeno.\nProcedure: EBUS-TBNA (Teaching case).\nStations: Systematic N3-N1. (Assumed 3+ stations for 31653).\nROSE: Used.\nComplications: None.",
            2: "PROCEDURE: EBUS-TBNA (Teaching Procedure).\nINDICATION: Staging of left upper lobe adenocarcinoma.\nNARRATIVE: The procedure was performed with fellow participation to meet educational objectives regarding systematic staging and needle technique. A complete N3 to N1 evaluation was conducted. Stations consistent with N3, N2, and N1 disease were assessed and sampled as indicated. ROSE was utilized for real-time feedback.",
            3: "CPT: 31653.\nRationale: Teaching physician presence documented. Systematic staging implies sampling of multiple stations (e.g., 4R, 4L, 7, 10L, 11L) satisfying the 3+ station requirement for 31653. ROSE service utilized.",
            4: "Fellow Procedure Note\nAttending: Present\nPt: Donald Martinez\nIndication: Staging\n1. Time out.\n2. EBUS scope inserted.\n3. Systematic exam performed.\n4. Multiple stations sampled (Learning points: needle angle, sheath management).\n5. ROSE review.\n6. Pt tolerated well.",
            5: "Teaching case Donald Martinez LUL cancer staging. Fellow did most of the work I supervised. We checked all the stations N3 back to N1. Sampled the relevant ones ROSE was there to check the slides. Good educational case no issues.",
            6: "EBUS-TBNA Staging for Donald Martinez. Teaching case with fellow. Systematic N3->N2->N1 evaluation performed. Multiple mediastinal stations sampled with ROSE confirmation. No complications.",
            7: "[Indication]\nLUL Adenocarcinoma Staging.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA performed by fellow under supervision. Systematic sampling of mediastinal nodes.\n[Plan]\nStandard post-proc care.",
            8: "Mr. Martinez underwent an EBUS-TBNA for staging of his LUL adenocarcinoma. This was a teaching case involving an interventional pulmonology fellow. We performed a systematic evaluation of the mediastinum, progressing from N3 to N1 stations. Multiple lymph node stations were sampled with the guidance of rapid on-site evaluation to ensure adequate tissue acquisition.",
            9: "Context: Educational staging procedure.\nMethod: EBUS-guided aspiration.\nScope: Comprehensive mediastinal survey.\nExecution: Fellow performed sampling under attending guidance.\nOutcome: Objectives met, staging complete."
        },
        4: { # Kevin Brown (Phone Note)
            1: "Procedure: EBUS + RUL Biopsy.\nEBUS: 4R(+), 7(+), 10R(-).\nBronch: RUL mass Bx x6.\nDx: RUL Adeno, N2 disease.\nPlan: Path/Molecular pending.",
            2: "COMMUNICATION: Telephone consultation regarding procedure results.\nPATIENT: Kevin Brown.\nSUMMARY: The patient underwent EBUS-TBNA and endobronchial biopsy. EBUS confirmed N2 disease with malignant involvement of stations 4R and 7; station 10R was benign. The primary RUL mass was also biopsied. Samples have been sent for molecular profiling. \nRECOMMENDATION: Tumor board discussion regarding definitive chemoradiation.",
            3: "Code Justification:\n- 31653: EBUS sampling of 3 stations (4R, 7, 10R).\n- 31625: Separate biopsy of endobronchial RUL mass.\nStatus: N2 disease confirmed.",
            4: "Resident Phone Note\nCalled Dr. Adams re: Kevin Brown.\nWe did the EBUS and bronch today.\n- EBUS: 4R and 7 positive for cancer. 10R neg.\n- RUL Mass: Biopsied.\nLooks like N2 disease / Stage IIIB.\nSent for molecular. F/U next week.",
            5: "Phone note for Kevin Brown called Dr Adams. Told him we found cancer in the mediastinum stations 4R and 7 were positive on ROSE. 10R was clear. We also took chunks of the main tumor in the RUL. No complications sending for genetic testing.",
            6: "Tele-consult note: Kevin Brown. DOS 10/27/2024. EBUS-TBNA performed at 4R, 7, 10R. 4R/7 positive for adenocarcinoma. RUL endobronchial mass biopsied. N2 disease confirmed. Molecular testing pending. No complications.",
            7: "[Indication]\nRUL mass staging.\n[Anesthesia]\nModerate.\n[Description]\nEBUS sampled 4R, 7, 10R. RUL mass biopsied. Findings: Adenocarcinoma, N2 positive.\n[Plan]\nTumor board, molecular pending.",
            8: "I called Dr. Adams to discuss Mr. Brown's bronchoscopy results. We performed an EBUS and endobronchial biopsy today. The EBUS sampling of stations 4R and 7 was positive for adenocarcinoma, confirming N2 disease, while station 10R was negative. We also obtained adequate biopsies from the primary RUL mass. We have ordered molecular testing and recommend a tumor board review.",
            9: "Communication: Verbal report to referring MD.\nFindings: EBUS detected malignancy in 4R and 7. 10R benign. RUL mass sampled.\nInterpretation: Multi-station N2 involvement.\nAction: Molecular panel ordered."
        },
        5: { # Nancy Rodriguez (Standard EBUS 3 stations)
            1: "Indication: RLL Adeno Staging.\nProcedure: EBUS-TBNA.\nStations: 4R (Pos), 7 (Pos), 10R (Neg).\nROSE: Used.\nComp: None.",
            2: "PROCEDURE: EBUS-TBNA Mediastinal Staging.\nFINDINGS: The mediastinum was systematically evaluated. Lymph node stations 4R, 7, and 10R were identified and sampled. Rapid on-site evaluation indicated malignancy in stations 4R and 7, consistent with metastatic adenocarcinoma. Station 10R was negative. \nIMPRESSION: Confirmed N2 disease.",
            3: "Billing: 31653.\nCriteria: 3 distinct nodal stations sampled (4R, 7, 10R).\nTechnique: Linear EBUS with transbronchial needle aspiration.\nPathology: Malignant (4R, 7), Benign (10R).",
            4: "Procedure Note\nPt: Nancy Rodriguez\nIndication: Staging RLL CA\n1. Sedation.\n2. EBUS scope.\n3. Sampled 4R, 7, 10R.\n4. 4R/7 Positive on ROSE.\n5. 10R Negative.\nPlan: Chemo/Rad eval.",
            5: "Nancy Rodriguez staging EBUS. We checked 4R 7 and 10R. 4R and 7 were positive for the cancer. 10R was just reactive. Good samples sent for testing. Patient woke up fine.",
            6: "EBUS-TBNA for Nancy Rodriguez. Indication: RLL adenocarcinoma staging. Sampled stations 4R (positive), 7 (positive), 10R (negative). ROSE utilized. No complications. N2 disease confirmed.",
            7: "[Indication]\nMediastinal staging RLL cancer.\n[Anesthesia]\nModerate.\n[Description]\nEBUS-TBNA stations 4R, 7, 10R. Malignancy found in 4R and 7.\n[Plan]\nMultidisciplinary management.",
            8: "Ms. Rodriguez underwent EBUS-TBNA for staging of her right lower lobe adenocarcinoma. We sampled three stations: 4R, 7, and 10R. The samples from 4R and 7 were positive for malignancy on-site, while 10R appeared benign. This confirms multi-station N2 involvement.",
            9: "Indication: Staging RLL neoplasm.\nAction: Aspirated nodes at 4R, 7, 10R.\nAnalysis: Malignant cells present in 4R/7.\nOutcome: Staging upgraded to N2."
        }
    }
    return variations

def get_base_data_mocks():
    # Mocks for names and original ages
    return [
        {"idx": 0, "orig_name": "Jennifer Wang", "orig_age": 61, "names": ["Susan Lee", "Karen Chen", "Betty Wu", "Helen Zhang", "Margaret Liu", "Patricia Yang", "Dorothy Huang", "Lisa Lin", "Nancy Wang"]},
        {"idx": 1, "orig_name": "Mark Thompson", "orig_age": 65, "names": ["Paul Harris", "George Clark", "Kenneth Lewis", "Steven Robinson", "Edward Walker", "Brian Young", "Ronald Hall", "Anthony Allen", "Kevin King"]},
        {"idx": 2, "orig_name": "Sandra Lopez", "orig_age": 70, "names": ["Carol Martinez", "Ruth Hernandez", "Sharon Gonzalez", "Michelle Wilson", "Laura Anderson", "Sarah Thomas", "Kimberly Taylor", "Deborah Moore", "Jessica Jackson"]},
        {"idx": 3, "orig_name": "Donald Martinez", "orig_age": 65, "names": ["Gary White", "Timothy Harris", "Frank Martin", "Larry Thompson", "Scott Garcia", "Stephen Martinez", "Eric Robinson", "Raymond Clark", "Gregory Rodriguez"]},
        {"idx": 4, "orig_name": "Kevin Brown", "orig_age": 66, "names": ["Jeffrey Lewis", "Ryan Lee", "Jacob Walker", "Gary Hall", "Nicholas Allen", "Eric Young", "Jonathan King", "Stephen Wright", "Larry Scott"]},
        {"idx": 5, "orig_name": "Nancy Rodriguez", "orig_age": 69, "names": ["Kathleen Green", "Amy Baker", "Shirley Adams", "Angela Nelson", "Helen Hill", "Anna Ramirez", "Brenda Campbell", "Pamela Mitchell", "Nicole Roberts"]},
    ]

def main():
    # Load original data from source file
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found: {SOURCE_FILE}")
        print("Please ensure the file exists or update SOURCE_FILE path.")
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
            # Handle cases where variation index might not exist (safety check)
            if idx in variations_text and style_num in variations_text[idx]:
                note_entry["note_text"] = variations_text[idx][style_num]
            else:
                print(f"Warning: Missing variation text for Note {idx}, Style {style_num}. Using original.")
            
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
    output_filename = output_dir / "synthetic_blvr_notes_part_016.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(generated_notes, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(generated_notes)} synthetic notes in {output_filename}")

if __name__ == "__main__":
    main()